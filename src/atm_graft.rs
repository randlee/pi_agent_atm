use crate::agent::{Agent, MessageFetcher};
use crate::error::{Error, Result};
use crate::model::{Message, UserContent, UserMessage};
use ::atm_graft::{Event, GraftClient, GraftObservability, GraftSession, GraftSessionOptions};
use atm_core::load_atm_config;
use atm_core::types::{AgentName, TeamName};
use chrono::Utc;
use std::collections::VecDeque;
use std::fmt::Write as _;
use std::path::Path;
use std::sync::{Arc, Mutex as StdMutex};

const MAX_ATM_STEERING_QUEUE_SIZE: usize = 100;

pub(crate) struct AtmGraftBridge {
    session: Option<GraftSession>,
}

impl AtmGraftBridge {
    pub(crate) fn activate(
        agent: &mut Agent,
        workspace_root: &Path,
        advisory_session_id: Option<&str>,
    ) -> Result<Option<Self>> {
        let Some(activation) = resolve_activation(workspace_root)? else {
            return Ok(None);
        };

        let client = GraftClient::connect()
            .map_err(|err| Error::config(format!("ATM graft daemon connection failed: {err}")))?;
        let queue = Arc::new(StdMutex::new(VecDeque::new()));
        let injector = Arc::new(AtmSteeringInjector::new(Arc::clone(&queue)));
        let session = GraftSession::activate_with_observability(
            client,
            build_session_options(
                workspace_root,
                &activation.team,
                &activation.agent,
                advisory_session_id,
            ),
            injector,
            Arc::new(LoggingObservability),
        )
        .map_err(|err| Error::config(format!("ATM graft activation failed: {err}")))?;

        agent.register_message_fetchers(Some(build_fetcher(queue)), None);

        let snapshot = session
            .snapshot()
            .map_err(|err| Error::config(format!("ATM graft snapshot failed: {err}")))?;
        tracing::info!(
            team = %activation.team,
            agent = %activation.agent,
            graft_session_id = %snapshot.session_id,
            state = ?snapshot.state,
            workspace_root = %workspace_root.display(),
            "ATM graft steering bridge activated"
        );

        Ok(Some(Self {
            session: Some(session),
        }))
    }
}

impl Drop for AtmGraftBridge {
    fn drop(&mut self) {
        if let Some(session) = self.session.take()
            && let Err(err) = session.close()
        {
            tracing::warn!(error = %err, "ATM graft session close failed during drop");
        }
    }
}

#[derive(Clone)]
struct ActivationConfig {
    team: TeamName,
    agent: AgentName,
}

fn resolve_activation(workspace_root: &Path) -> Result<Option<ActivationConfig>> {
    let Some(config) = load_atm_config(workspace_root)
        .map_err(|err| Error::config(format!("failed to load ATM config: {err}")))?
    else {
        tracing::debug!(
            workspace_root = %workspace_root.display(),
            "ATM graft not activated: no .atm.toml found"
        );
        return Ok(None);
    };

    if !config.graft.enabled {
        tracing::debug!(
            workspace_root = %workspace_root.display(),
            "ATM graft not activated: [atm.graft].enabled is false"
        );
        return Ok(None);
    }

    let Some(agent_raw) = std::env::var("ATM_IDENTITY")
        .ok()
        .map(|value| value.trim().to_string())
        .filter(|value| !value.is_empty())
    else {
        tracing::debug!(
            workspace_root = %workspace_root.display(),
            "ATM graft not activated: ATM_IDENTITY is not set"
        );
        return Ok(None);
    };
    let agent = agent_raw.parse::<AgentName>().map_err(|err| {
        Error::config(format!(
            "ATM_IDENTITY must be a valid ATM agent name: {err}"
        ))
    })?;

    let team = if let Some(raw) = std::env::var("ATM_TEAM")
        .ok()
        .map(|value| value.trim().to_string())
        .filter(|value| !value.is_empty())
    {
        raw.parse::<TeamName>().map_err(|err| {
            Error::config(format!("ATM_TEAM must be a valid ATM team name: {err}"))
        })?
    } else {
        let Some(team) = config.default_team else {
            tracing::debug!(
                workspace_root = %workspace_root.display(),
                "ATM graft not activated: ATM_TEAM unset and .atm.toml has no default team"
            );
            return Ok(None);
        };
        team
    };

    Ok(Some(ActivationConfig { team, agent }))
}

fn build_session_options(
    workspace_root: &Path,
    team: &TeamName,
    agent: &AgentName,
    advisory_session_id: Option<&str>,
) -> GraftSessionOptions {
    if let Some(raw) = advisory_session_id
        && let Ok(session_id) = ::atm_graft::SessionId::new(raw.to_string())
    {
        return GraftSessionOptions::new(
            workspace_root.to_path_buf(),
            team.clone(),
            agent.clone(),
            session_id,
        );
    }

    if let Some(raw) = advisory_session_id {
        tracing::warn!(
            advisory_session_id = raw,
            "Falling back to process-derived ATM graft session id"
        );
    }

    GraftSessionOptions::for_current_process(
        workspace_root.to_path_buf(),
        team.clone(),
        agent.clone(),
    )
}

fn build_fetcher(queue: Arc<StdMutex<VecDeque<Message>>>) -> MessageFetcher {
    Arc::new(move || {
        let queue = Arc::clone(&queue);
        Box::pin(async move {
            let Ok(mut queue) = queue.lock() else {
                tracing::error!("ATM graft steering queue mutex poisoned; dropping queued nudges");
                return Vec::new();
            };
            queue.drain(..).collect()
        })
    })
}

struct AtmSteeringInjector {
    queue: Arc<StdMutex<VecDeque<Message>>>,
}

impl AtmSteeringInjector {
    const fn new(queue: Arc<StdMutex<VecDeque<Message>>>) -> Self {
        Self { queue }
    }
}

impl ::atm_graft::HostNudgeInjector for AtmSteeringInjector {
    fn inject_nudge(&self, nudge: Event) -> std::result::Result<(), atm_core::error::AtmError> {
        let Ok(mut queue) = self.queue.lock() else {
            return Err(atm_core::error::AtmError::daemon_unavailable(
                "ATM graft steering queue mutex poisoned",
            ));
        };
        if queue.len() >= MAX_ATM_STEERING_QUEUE_SIZE {
            queue.pop_front();
            tracing::warn!(
                max_queue = MAX_ATM_STEERING_QUEUE_SIZE,
                "ATM graft steering queue full; dropping oldest pending nudge"
            );
        }
        queue.push_back(Message::User(UserMessage {
            content: UserContent::Text(format_nudge_message(&nudge)),
            timestamp: Utc::now().timestamp_millis(),
        }));
        Ok(())
    }
}

#[derive(Default)]
struct LoggingObservability;

impl GraftObservability for LoggingObservability {
    fn session_state_changed(&self, snapshot: &::atm_graft::SessionSnapshot) {
        tracing::debug!(
            team = %snapshot.team,
            agent = %snapshot.agent,
            graft_session_id = %snapshot.session_id,
            state = ?snapshot.state,
            "ATM graft session state changed"
        );
    }

    fn nudge_delivered(&self, session_id: &::atm_graft::SessionId, nudge: &::atm_graft::Event) {
        tracing::debug!(
            graft_session_id = %session_id,
            from = %nudge.from,
            message_id = %nudge.message_id,
            "ATM graft nudge delivered to Pi steering queue"
        );
    }

    fn session_error(
        &self,
        session_id: &::atm_graft::SessionId,
        action: &'static str,
        error: &atm_core::error::AtmError,
    ) {
        tracing::warn!(
            graft_session_id = %session_id,
            action,
            error = %error,
            "ATM graft session reported an error"
        );
    }
}

fn format_nudge_message(nudge: &Event) -> String {
    let mut text = String::new();
    let _ = write!(&mut text, "ATM advisory from {}", nudge.from);
    if let Some(task_id) = &nudge.task_id {
        let _ = write!(&mut text, " (task {task_id})");
    }
    text.push_str(":\n");
    text.push_str(nudge.message.as_str());
    text
}

#[cfg(test)]
mod tests {
    use super::*;
    use ::atm_graft::HostNudgeInjector;
    use atm_core::graft::AdvisoryMessage;
    use atm_core::schema::AtmMessageId;
    use atm_core::types::{IsoTimestamp, TaskId};
    use futures::executor::block_on;

    fn test_event(message: &str) -> Event {
        Event {
            message_id: AtmMessageId::new(),
            from: "quality-mgr".parse().expect("agent name"),
            message: AdvisoryMessage::new(message).expect("advisory message"),
            received_at: IsoTimestamp::now(),
            task_id: Some("br-123".parse::<TaskId>().expect("task id")),
        }
    }

    #[test]
    fn format_nudge_message_includes_sender_and_task() {
        let formatted = format_nudge_message(&test_event("Prefer safe edits only."));
        assert!(formatted.contains("ATM advisory from quality-mgr"));
        assert!(formatted.contains("task br-123"));
        assert!(formatted.contains("Prefer safe edits only."));
    }

    #[test]
    fn fetcher_drains_injected_nudges_in_order() {
        let queue = Arc::new(StdMutex::new(VecDeque::new()));
        let injector = AtmSteeringInjector::new(Arc::clone(&queue));
        let fetcher = build_fetcher(queue);

        injector
            .inject_nudge(test_event("First advisory"))
            .expect("inject first nudge");
        injector
            .inject_nudge(test_event("Second advisory"))
            .expect("inject second nudge");

        let drained = block_on(fetcher());
        assert_eq!(drained.len(), 2);
        let texts = drained
            .iter()
            .map(|message| match message {
                Message::User(user) => match &user.content {
                    UserContent::Text(text) => text.clone(),
                    UserContent::Blocks(_) => {
                        panic!("expected text steering message, found block content")
                    }
                },
                other => panic!("expected user message, found {other:?}"),
            })
            .collect::<Vec<_>>();
        assert!(texts[0].contains("First advisory"));
        assert!(texts[1].contains("Second advisory"));

        let second_drain = block_on(fetcher());
        assert!(second_drain.is_empty());
    }
}
