//! Host-scale resource admission control for swarm workloads.
//!
//! The governor is intentionally conservative and dependency-light: Linux hosts
//! get live `/proc` sampling, while other platforms keep deterministic fallback
//! budgets and only enforce request-local limits such as tool-output caps.

use serde::Serialize;
use serde_json::{Value, json};

const PROC_PAGE_SIZE_BYTES: u64 = 4096;
const DEFAULT_MEMORY_BYTES: u64 = 1_073_741_824;
const DEFAULT_FD_LIMIT: u64 = 1024;
const DEFAULT_TOOL_OUTPUT_BYTES: u64 = 128 * 1024 * 1024;
const DEFAULT_MAX_QUEUE_DEPTH: usize = 256;
const DEFAULT_MIN_QUEUE_DEPTH_BUDGET: usize = 128;
const DEFAULT_MAX_QUEUE_DEPTH_BUDGET: usize = 4096;
const DEFAULT_QUEUE_DEPTH_PER_CORE: u64 = 64;
const DEFAULT_TAIL_LATENCY_ENTER_SAMPLES: usize = 3;
const DEFAULT_TAIL_LATENCY_EXIT_SAMPLES: usize = 3;
const DEFAULT_TAIL_LATENCY_RECOVERY_RATIO: f64 = 0.80;
const DEFAULT_TAIL_LATENCY_RESOURCE_PRESSURE_RATIO: f64 = 0.85;
const MIN_PROCESS_BUDGET: u64 = 64;
const MIN_FD_BUDGET: u64 = 128;
const MIN_LOAD_BUDGET: f64 = 2.0;

/// Host resource budgets used by admission checks.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct HostResourceBudgets {
    /// Logical CPU cores available to this process.
    pub cpu_cores: u64,
    /// Maximum acceptable one-minute load average before denial.
    pub max_load_avg_1m: f64,
    /// Maximum RSS for this process.
    pub max_rss_bytes: u64,
    /// Maximum observed process count on the host.
    pub max_processes: u64,
    /// Maximum file descriptors open by this process.
    pub max_fds: u64,
    /// Maximum tool-output bytes admitted for one hostcall.
    pub max_tool_output_bytes: u64,
    /// Maximum queued hostcalls before queue-depth pressure is unsafe.
    pub max_queue_depth: usize,
    /// Ratio at which the governor starts delaying work.
    pub backpressure_ratio: f64,
    /// Ratio at which the governor rejects work fail-closed.
    pub deny_ratio: f64,
}

impl HostResourceBudgets {
    /// Derive conservative budgets from the current host.
    #[must_use]
    #[allow(clippy::cast_precision_loss)]
    pub fn from_host() -> Self {
        let cpu_cores = std::thread::available_parallelism()
            .ok()
            .and_then(|value| u64::try_from(value.get()).ok())
            .unwrap_or(1);
        let mem_total = read_mem_total_bytes().unwrap_or(DEFAULT_MEMORY_BYTES);
        let max_rss_bytes = (mem_total / 2).clamp(512 * 1024 * 1024, 8 * 1024 * 1024 * 1024);
        let fd_soft_limit = read_open_files_soft_limit().unwrap_or(DEFAULT_FD_LIMIT);
        let max_queue_depth = queue_depth_budget(cpu_cores);

        Self {
            cpu_cores,
            max_load_avg_1m: ((cpu_cores as f64) * 4.0).max(MIN_LOAD_BUDGET),
            max_rss_bytes,
            max_processes: cpu_cores.saturating_mul(128).max(MIN_PROCESS_BUDGET),
            max_fds: ((fd_soft_limit.saturating_mul(4)) / 5).max(MIN_FD_BUDGET),
            max_tool_output_bytes: DEFAULT_TOOL_OUTPUT_BYTES,
            max_queue_depth,
            backpressure_ratio: 0.85,
            deny_ratio: 1.10,
        }
    }

    /// Test helper for fixed budgets.
    #[must_use]
    pub const fn fixed(
        max_load_avg_1m: f64,
        max_rss_bytes: u64,
        max_processes: u64,
        max_fds: u64,
        max_tool_output_bytes: u64,
    ) -> Self {
        Self {
            cpu_cores: 1,
            max_load_avg_1m,
            max_rss_bytes,
            max_processes,
            max_fds,
            max_tool_output_bytes,
            max_queue_depth: DEFAULT_MAX_QUEUE_DEPTH,
            backpressure_ratio: 0.85,
            deny_ratio: 1.10,
        }
    }

    /// Test helper for fixed budgets with an explicit queue-depth budget.
    #[must_use]
    pub const fn fixed_with_queue_depth(
        max_load_avg_1m: f64,
        max_rss_bytes: u64,
        max_processes: u64,
        max_fds: u64,
        max_tool_output_bytes: u64,
        max_queue_depth: usize,
    ) -> Self {
        Self {
            cpu_cores: 1,
            max_load_avg_1m,
            max_rss_bytes,
            max_processes,
            max_fds,
            max_tool_output_bytes,
            max_queue_depth,
            backpressure_ratio: 0.85,
            deny_ratio: 1.10,
        }
    }

    /// Return stricter budgets for conservative fallback mode.
    #[must_use]
    pub fn conservative_fallback(&self) -> Self {
        let backpressure_ratio = (self.backpressure_ratio * 0.75).max(0.10);
        let deny_ratio = (self.deny_ratio * 0.85)
            .max(backpressure_ratio + 0.05)
            .min(self.deny_ratio);
        Self {
            cpu_cores: self.cpu_cores,
            max_load_avg_1m: conservative_f64(self.max_load_avg_1m, 0.75),
            max_rss_bytes: conservative_u64(self.max_rss_bytes, 3, 4),
            max_processes: conservative_u64(self.max_processes, 3, 4),
            max_fds: conservative_u64(self.max_fds, 3, 4),
            max_tool_output_bytes: conservative_u64(self.max_tool_output_bytes, 1, 2),
            max_queue_depth: conservative_usize(self.max_queue_depth, 1, 2),
            backpressure_ratio,
            deny_ratio,
        }
    }
}

impl Default for HostResourceBudgets {
    fn default() -> Self {
        Self::from_host()
    }
}

/// Current host sample used for one admission decision.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct HostResourceSample {
    /// One-minute load average, when available.
    pub load_avg_1m: Option<f64>,
    /// Current process RSS in bytes, when available.
    pub rss_bytes: Option<u64>,
    /// Current host process count, when available.
    pub process_count: Option<u64>,
    /// Current open file descriptor count for this process, when available.
    pub fd_count: Option<u64>,
}

impl HostResourceSample {
    /// Sample the current process/host state.
    #[must_use]
    pub fn current() -> Self {
        Self {
            load_avg_1m: read_load_avg_1m(),
            rss_bytes: read_self_rss_bytes(),
            process_count: count_proc_processes(),
            fd_count: count_self_fds(),
        }
    }
}

/// Hostcall class submitted to the resource governor.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ResourceOperationKind {
    /// Built-in or extension-provided tool call.
    Tool,
    /// Shell command hostcall.
    Exec,
    /// HTTP hostcall.
    Http,
    /// Session metadata or persistence hostcall.
    Session,
    /// Extension UI hostcall.
    Ui,
    /// Extension event hostcall.
    Events,
    /// Extension log/telemetry hostcall.
    Log,
    /// Unknown or future hostcall kind.
    Unknown,
}

/// One unit of work being considered for admission.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ResourceRequest {
    /// Operation class.
    pub operation: ResourceOperationKind,
    /// Required capability label.
    pub capability: String,
    /// Estimated maximum output bytes retained by the operation.
    pub estimated_tool_output_bytes: u64,
    /// Current scheduler queue depth.
    pub queue_depth: usize,
}

impl ResourceRequest {
    /// Create a request for the given operation/capability.
    #[must_use]
    pub fn new(operation: ResourceOperationKind, capability: impl Into<String>) -> Self {
        Self {
            operation,
            capability: capability.into(),
            estimated_tool_output_bytes: 0,
            queue_depth: 1,
        }
    }

    /// Attach estimated output bytes.
    #[must_use]
    pub const fn with_estimated_tool_output_bytes(mut self, bytes: u64) -> Self {
        self.estimated_tool_output_bytes = bytes;
        self
    }

    /// Attach queue depth.
    #[must_use]
    pub const fn with_queue_depth(mut self, queue_depth: usize) -> Self {
        self.queue_depth = if queue_depth == 0 { 1 } else { queue_depth };
        self
    }
}

/// Admission action selected by the governor.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum AdmissionAction {
    /// Dispatch immediately.
    Admit,
    /// Delay briefly, then dispatch.
    Backpressure,
    /// Reject before dispatch.
    Deny,
}

/// Resource dimension that dominated a decision.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ResourceDimension {
    /// CPU load average.
    CpuLoad,
    /// Process resident memory.
    Rss,
    /// Host process count.
    Processes,
    /// Open file descriptors.
    FileDescriptors,
    /// Estimated tool output.
    ToolOutput,
    /// Scheduler queue depth.
    QueueDepth,
    /// No dimension is currently pressurized.
    None,
}

/// Stable schema for tail-latency regime telemetry.
pub const TAIL_LATENCY_REGIME_SCHEMA: &str = "pi.resource_governor.tail_latency_regime.v1";

/// Current tail-latency regime selected by the guard.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum TailLatencyRegime {
    /// Observed telemetry is still within the calibrated regime.
    Calibrated,
    /// Observed telemetry has left the calibrated regime; use safer budgets.
    ConservativeFallback,
}

/// Reason conservative fallback is active or pending.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum TailLatencyFallbackReason {
    /// p99 latency exceeded the calibrated threshold.
    P99Latency,
    /// p999 latency exceeded the calibrated threshold.
    P999Latency,
    /// Scheduler queue depth exceeded the calibrated threshold.
    QueueDepth,
    /// Host resource pressure exceeded the calibrated threshold.
    ResourcePressure,
    /// Samples are healthy, but hysteresis has not yet allowed recovery.
    HysteresisHold,
}

/// Live telemetry consumed by the tail-latency regime guard.
#[derive(Debug, Clone, Copy, PartialEq, Serialize)]
pub struct TailLatencyRegimeSample {
    /// Live p99 latency in milliseconds.
    pub p99_ms: u64,
    /// Live p999 latency in milliseconds.
    pub p999_ms: u64,
    /// Current scheduler queue depth.
    pub queue_depth: usize,
    /// Highest current host resource pressure ratio.
    pub resource_pressure_ratio: f64,
}

impl TailLatencyRegimeSample {
    /// Create one live guard sample.
    #[must_use]
    pub const fn new(
        p99_ms: u64,
        p999_ms: u64,
        queue_depth: usize,
        resource_pressure_ratio: f64,
    ) -> Self {
        Self {
            p99_ms,
            p999_ms,
            queue_depth,
            resource_pressure_ratio,
        }
    }

    /// Build a guard sample from an admission decision and explicit tail latency.
    #[must_use]
    pub const fn from_admission_decision(
        p99_ms: u64,
        p999_ms: u64,
        queue_depth: usize,
        decision: &AdmissionDecision,
    ) -> Self {
        Self {
            p99_ms,
            p999_ms,
            queue_depth,
            resource_pressure_ratio: decision.dominant_ratio,
        }
    }
}

/// Calibrated thresholds and hysteresis controls for regime detection.
#[derive(Debug, Clone, Copy, PartialEq, Serialize)]
pub struct TailLatencyRegimeConfig {
    /// Calibrated p99 latency threshold in milliseconds.
    pub calibrated_p99_ms: u64,
    /// Calibrated p999 latency threshold in milliseconds.
    pub calibrated_p999_ms: u64,
    /// Calibrated queue-depth threshold.
    pub max_queue_depth: usize,
    /// Calibrated host resource pressure threshold.
    pub max_resource_pressure_ratio: f64,
    /// Fraction of calibrated thresholds required before exiting fallback.
    pub recovery_ratio: f64,
    /// Consecutive violating samples required to enter fallback.
    pub enter_consecutive_samples: usize,
    /// Consecutive recovered samples required to exit fallback.
    pub exit_consecutive_samples: usize,
}

impl Default for TailLatencyRegimeConfig {
    fn default() -> Self {
        Self {
            calibrated_p99_ms: 1_000,
            calibrated_p999_ms: 5_000,
            max_queue_depth: DEFAULT_MAX_QUEUE_DEPTH,
            max_resource_pressure_ratio: DEFAULT_TAIL_LATENCY_RESOURCE_PRESSURE_RATIO,
            recovery_ratio: DEFAULT_TAIL_LATENCY_RECOVERY_RATIO,
            enter_consecutive_samples: DEFAULT_TAIL_LATENCY_ENTER_SAMPLES,
            exit_consecutive_samples: DEFAULT_TAIL_LATENCY_EXIT_SAMPLES,
        }
    }
}

impl TailLatencyRegimeConfig {
    /// Create explicit guard thresholds.
    #[must_use]
    pub const fn new(
        calibrated_p99_ms: u64,
        calibrated_p999_ms: u64,
        max_queue_depth: usize,
        max_resource_pressure_ratio: f64,
        recovery_ratio: f64,
        enter_consecutive_samples: usize,
        exit_consecutive_samples: usize,
    ) -> Self {
        Self {
            calibrated_p99_ms,
            calibrated_p999_ms,
            max_queue_depth,
            max_resource_pressure_ratio,
            recovery_ratio,
            enter_consecutive_samples,
            exit_consecutive_samples,
        }
    }

    fn normalized(self) -> Self {
        let max_resource_pressure_ratio = if self.max_resource_pressure_ratio.is_finite()
            && self.max_resource_pressure_ratio > 0.0
        {
            self.max_resource_pressure_ratio
        } else {
            DEFAULT_TAIL_LATENCY_RESOURCE_PRESSURE_RATIO
        };
        let recovery_ratio = if self.recovery_ratio.is_finite() {
            self.recovery_ratio.clamp(0.10, 1.0)
        } else {
            DEFAULT_TAIL_LATENCY_RECOVERY_RATIO
        };
        Self {
            calibrated_p99_ms: self.calibrated_p99_ms,
            calibrated_p999_ms: self.calibrated_p999_ms.max(self.calibrated_p99_ms),
            max_queue_depth: self.max_queue_depth.max(1),
            max_resource_pressure_ratio,
            recovery_ratio,
            enter_consecutive_samples: self.enter_consecutive_samples.max(1),
            exit_consecutive_samples: self.exit_consecutive_samples.max(1),
        }
    }

    fn entry_reasons(&self, sample: TailLatencyRegimeSample) -> Vec<TailLatencyFallbackReason> {
        let mut reasons = Vec::new();
        if sample.p99_ms > self.calibrated_p99_ms {
            reasons.push(TailLatencyFallbackReason::P99Latency);
        }
        if sample.p999_ms > self.calibrated_p999_ms {
            reasons.push(TailLatencyFallbackReason::P999Latency);
        }
        if sample.queue_depth > self.max_queue_depth {
            reasons.push(TailLatencyFallbackReason::QueueDepth);
        }
        if sample.resource_pressure_ratio.is_finite()
            && sample.resource_pressure_ratio > self.max_resource_pressure_ratio
        {
            reasons.push(TailLatencyFallbackReason::ResourcePressure);
        }
        reasons
    }

    fn recovery_blockers(&self, sample: TailLatencyRegimeSample) -> Vec<TailLatencyFallbackReason> {
        let mut reasons = Vec::new();
        if sample.p99_ms > scale_u64_by_ratio(self.calibrated_p99_ms, self.recovery_ratio) {
            reasons.push(TailLatencyFallbackReason::P99Latency);
        }
        if sample.p999_ms > scale_u64_by_ratio(self.calibrated_p999_ms, self.recovery_ratio) {
            reasons.push(TailLatencyFallbackReason::P999Latency);
        }
        if sample.queue_depth > scale_usize_by_ratio(self.max_queue_depth, self.recovery_ratio) {
            reasons.push(TailLatencyFallbackReason::QueueDepth);
        }
        if sample.resource_pressure_ratio.is_finite()
            && sample.resource_pressure_ratio
                > self.max_resource_pressure_ratio * self.recovery_ratio
        {
            reasons.push(TailLatencyFallbackReason::ResourcePressure);
        }
        reasons
    }
}

/// Result of observing one tail-latency sample.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct TailLatencyRegimeDecision {
    /// Active regime after processing the sample.
    pub regime: TailLatencyRegime,
    /// True when conservative fallback should be applied.
    pub fallback_active: bool,
    /// True when this sample changed the active regime.
    pub changed: bool,
    /// Reasons fallback is active or pending.
    pub reasons: Vec<TailLatencyFallbackReason>,
    /// Consecutive violating samples seen while calibrated.
    pub bad_sample_streak: usize,
    /// Consecutive recovered samples seen while in fallback.
    pub recovery_sample_streak: usize,
    /// Sample used for this decision.
    pub sample: TailLatencyRegimeSample,
}

impl TailLatencyRegimeDecision {
    /// Render stable JSON telemetry for the regime decision.
    #[must_use]
    pub fn telemetry(&self) -> Value {
        json!({
            "schema": TAIL_LATENCY_REGIME_SCHEMA,
            "decision": self,
        })
    }

    /// Apply conservative fallback budgets only when fallback is active.
    #[must_use]
    pub fn conservative_budgets(&self, budgets: &HostResourceBudgets) -> HostResourceBudgets {
        if self.fallback_active {
            budgets.conservative_fallback()
        } else {
            budgets.clone()
        }
    }
}

/// Stateful guard that detects tail-latency regime shifts with hysteresis.
#[derive(Debug, Clone)]
pub struct TailLatencyRegimeGuard {
    config: TailLatencyRegimeConfig,
    regime: TailLatencyRegime,
    bad_sample_streak: usize,
    recovery_sample_streak: usize,
    last_reasons: Vec<TailLatencyFallbackReason>,
}

impl TailLatencyRegimeGuard {
    /// Build a guard from calibrated thresholds.
    #[must_use]
    pub fn new(config: TailLatencyRegimeConfig) -> Self {
        Self {
            config: config.normalized(),
            regime: TailLatencyRegime::Calibrated,
            bad_sample_streak: 0,
            recovery_sample_streak: 0,
            last_reasons: Vec::new(),
        }
    }

    /// Return the normalized guard config.
    #[must_use]
    pub const fn config(&self) -> TailLatencyRegimeConfig {
        self.config
    }

    /// Return the active regime.
    #[must_use]
    pub const fn regime(&self) -> TailLatencyRegime {
        self.regime
    }

    /// Observe one live telemetry sample and update the regime.
    pub fn observe(&mut self, sample: TailLatencyRegimeSample) -> TailLatencyRegimeDecision {
        let entry_reasons = self.config.entry_reasons(sample);
        let mut changed = false;

        match self.regime {
            TailLatencyRegime::Calibrated => {
                self.recovery_sample_streak = 0;
                if entry_reasons.is_empty() {
                    self.bad_sample_streak = 0;
                    self.last_reasons.clear();
                } else {
                    self.bad_sample_streak = self.bad_sample_streak.saturating_add(1);
                    self.last_reasons.clone_from(&entry_reasons);
                    if self.bad_sample_streak >= self.config.enter_consecutive_samples {
                        self.regime = TailLatencyRegime::ConservativeFallback;
                        self.recovery_sample_streak = 0;
                        changed = true;
                    }
                }
            }
            TailLatencyRegime::ConservativeFallback => {
                self.bad_sample_streak = 0;
                let blockers = self.config.recovery_blockers(sample);
                if blockers.is_empty() {
                    self.recovery_sample_streak = self.recovery_sample_streak.saturating_add(1);
                    if self.recovery_sample_streak >= self.config.exit_consecutive_samples {
                        self.regime = TailLatencyRegime::Calibrated;
                        self.bad_sample_streak = 0;
                        self.recovery_sample_streak = 0;
                        self.last_reasons.clear();
                        changed = true;
                    } else {
                        self.last_reasons = vec![TailLatencyFallbackReason::HysteresisHold];
                    }
                } else {
                    self.recovery_sample_streak = 0;
                    self.last_reasons = blockers;
                }
            }
        }

        let fallback_active = matches!(self.regime, TailLatencyRegime::ConservativeFallback);
        let reasons = if fallback_active {
            self.last_reasons.clone()
        } else {
            entry_reasons
        };
        TailLatencyRegimeDecision {
            regime: self.regime,
            fallback_active,
            changed,
            reasons,
            bad_sample_streak: self.bad_sample_streak,
            recovery_sample_streak: self.recovery_sample_streak,
            sample,
        }
    }
}

/// Result of one admission check.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct AdmissionDecision {
    /// Selected action.
    pub action: AdmissionAction,
    /// Resource dimension with the highest budget ratio.
    pub dominant_dimension: ResourceDimension,
    /// Highest observed budget ratio.
    pub dominant_ratio: f64,
    /// Human-readable reason for telemetry and errors.
    pub reason: String,
    /// Delay to apply for [`AdmissionAction::Backpressure`].
    pub retry_after_ms: u64,
    /// Sample used by this decision.
    pub sample: HostResourceSample,
    /// Budgets used by this decision.
    pub budgets: HostResourceBudgets,
    /// True when the decision used conservative fallback budgets.
    #[serde(skip_serializing_if = "is_false")]
    pub conservative_fallback_active: bool,
    /// Tail-latency fallback reasons applied to this decision.
    #[serde(skip_serializing_if = "Vec::is_empty")]
    pub fallback_reasons: Vec<TailLatencyFallbackReason>,
}

impl AdmissionDecision {
    /// Render a stable JSON telemetry payload.
    #[must_use]
    pub fn telemetry(&self, request: &ResourceRequest) -> Value {
        json!({
            "schema": "pi.resource_governor.admission.v1",
            "request": request,
            "decision": self,
        })
    }
}

/// Stateless resource governor.
#[derive(Debug, Clone)]
pub struct ResourceGovernor {
    budgets: HostResourceBudgets,
}

impl ResourceGovernor {
    /// Build a governor from host-derived budgets.
    #[must_use]
    pub fn from_host() -> Self {
        Self {
            budgets: HostResourceBudgets::from_host(),
        }
    }

    /// Build a governor with explicit budgets.
    #[must_use]
    pub const fn with_budgets(budgets: HostResourceBudgets) -> Self {
        Self { budgets }
    }

    /// Return the active budgets.
    #[must_use]
    pub const fn budgets(&self) -> &HostResourceBudgets {
        &self.budgets
    }

    /// Evaluate a request against the live host sample.
    #[must_use]
    pub fn admit(&self, request: &ResourceRequest) -> AdmissionDecision {
        self.admit_sample(request, HostResourceSample::current())
    }

    /// Evaluate a request against an injected sample.
    #[must_use]
    pub fn admit_sample(
        &self,
        request: &ResourceRequest,
        sample: HostResourceSample,
    ) -> AdmissionDecision {
        Self::admit_sample_with_budgets(request, sample, self.budgets.clone(), false, Vec::new())
    }

    /// Evaluate a request using conservative budgets when a regime guard is in fallback.
    #[must_use]
    pub fn admit_sample_with_tail_latency_decision(
        &self,
        request: &ResourceRequest,
        sample: HostResourceSample,
        regime_decision: &TailLatencyRegimeDecision,
    ) -> AdmissionDecision {
        let budgets = regime_decision.conservative_budgets(&self.budgets);
        let fallback_reasons = if regime_decision.fallback_active {
            regime_decision.reasons.clone()
        } else {
            Vec::new()
        };
        Self::admit_sample_with_budgets(
            request,
            sample,
            budgets,
            regime_decision.fallback_active,
            fallback_reasons,
        )
    }

    /// Observe live tail-latency telemetry, then evaluate admission with the selected regime.
    pub fn admit_sample_with_tail_latency_guard(
        &self,
        request: &ResourceRequest,
        sample: HostResourceSample,
        guard: &mut TailLatencyRegimeGuard,
        latency_sample: TailLatencyRegimeSample,
    ) -> (AdmissionDecision, TailLatencyRegimeDecision) {
        let regime_decision = guard.observe(latency_sample);
        let admission =
            self.admit_sample_with_tail_latency_decision(request, sample, &regime_decision);
        (admission, regime_decision)
    }

    fn admit_sample_with_budgets(
        request: &ResourceRequest,
        sample: HostResourceSample,
        budgets: HostResourceBudgets,
        conservative_fallback_active: bool,
        fallback_reasons: Vec<TailLatencyFallbackReason>,
    ) -> AdmissionDecision {
        let (dominant_dimension, dominant_ratio) = dominant_pressure(&budgets, &sample, request);
        let action = if dominant_ratio >= budgets.deny_ratio {
            AdmissionAction::Deny
        } else if dominant_ratio >= budgets.backpressure_ratio {
            AdmissionAction::Backpressure
        } else {
            AdmissionAction::Admit
        };
        let retry_after_ms = match action {
            AdmissionAction::Backpressure => retry_after_ms(dominant_ratio),
            AdmissionAction::Admit | AdmissionAction::Deny => 0,
        };
        AdmissionDecision {
            action,
            dominant_dimension,
            dominant_ratio,
            reason: decision_reason(action, dominant_dimension, dominant_ratio),
            retry_after_ms,
            sample,
            budgets,
            conservative_fallback_active,
            fallback_reasons,
        }
    }
}

impl Default for ResourceGovernor {
    fn default() -> Self {
        Self::from_host()
    }
}

fn dominant_pressure(
    budgets: &HostResourceBudgets,
    sample: &HostResourceSample,
    request: &ResourceRequest,
) -> (ResourceDimension, f64) {
    let mut dominant = (ResourceDimension::None, 0.0);
    consider_ratio(
        &mut dominant,
        ResourceDimension::CpuLoad,
        sample.load_avg_1m,
        budgets.max_load_avg_1m,
    );
    consider_ratio_u64(
        &mut dominant,
        ResourceDimension::Rss,
        sample.rss_bytes,
        budgets.max_rss_bytes,
    );
    consider_ratio_u64(
        &mut dominant,
        ResourceDimension::Processes,
        sample.process_count,
        budgets.max_processes,
    );
    consider_ratio_u64(
        &mut dominant,
        ResourceDimension::FileDescriptors,
        sample.fd_count,
        budgets.max_fds,
    );
    consider_ratio_u64(
        &mut dominant,
        ResourceDimension::ToolOutput,
        Some(request.estimated_tool_output_bytes),
        budgets.max_tool_output_bytes,
    );
    consider_ratio_usize(
        &mut dominant,
        ResourceDimension::QueueDepth,
        Some(request.queue_depth),
        budgets.max_queue_depth,
    );
    dominant
}

fn consider_ratio(
    dominant: &mut (ResourceDimension, f64),
    dimension: ResourceDimension,
    observed: Option<f64>,
    budget: f64,
) {
    let Some(observed) = observed else {
        return;
    };
    if budget <= 0.0 {
        return;
    }
    let ratio = observed.max(0.0) / budget;
    if ratio > dominant.1 {
        *dominant = (dimension, ratio);
    }
}

#[allow(clippy::cast_precision_loss)]
fn consider_ratio_u64(
    dominant: &mut (ResourceDimension, f64),
    dimension: ResourceDimension,
    observed: Option<u64>,
    budget: u64,
) {
    if budget == 0 {
        return;
    }
    consider_ratio(
        dominant,
        dimension,
        observed.map(|value| value as f64),
        budget as f64,
    );
}

#[allow(clippy::cast_precision_loss)]
fn consider_ratio_usize(
    dominant: &mut (ResourceDimension, f64),
    dimension: ResourceDimension,
    observed: Option<usize>,
    budget: usize,
) {
    if budget == 0 {
        return;
    }
    consider_ratio(
        dominant,
        dimension,
        observed.map(|value| value as f64),
        budget as f64,
    );
}

fn queue_depth_budget(cpu_cores: u64) -> usize {
    let queue_depth = cpu_cores.saturating_mul(DEFAULT_QUEUE_DEPTH_PER_CORE);
    usize::try_from(queue_depth)
        .unwrap_or(DEFAULT_MAX_QUEUE_DEPTH_BUDGET)
        .clamp(
            DEFAULT_MIN_QUEUE_DEPTH_BUDGET,
            DEFAULT_MAX_QUEUE_DEPTH_BUDGET,
        )
}

fn conservative_u64(value: u64, numerator: u64, denominator: u64) -> u64 {
    if value == 0 || denominator == 0 {
        return value;
    }
    value.saturating_mul(numerator).div_ceil(denominator).max(1)
}

fn conservative_usize(value: usize, numerator: usize, denominator: usize) -> usize {
    if value == 0 || denominator == 0 {
        return value;
    }
    value.saturating_mul(numerator).div_ceil(denominator).max(1)
}

fn conservative_f64(value: f64, ratio: f64) -> f64 {
    if !value.is_finite() || value <= 0.0 {
        return value;
    }
    (value * ratio).max(f64::MIN_POSITIVE)
}

#[allow(
    clippy::cast_sign_loss,
    clippy::cast_possible_truncation,
    clippy::cast_precision_loss
)]
fn scale_u64_by_ratio(value: u64, ratio: f64) -> u64 {
    if value == 0 {
        return 0;
    }
    ((value as f64) * ratio).ceil().max(1.0) as u64
}

#[allow(
    clippy::cast_sign_loss,
    clippy::cast_possible_truncation,
    clippy::cast_precision_loss
)]
fn scale_usize_by_ratio(value: usize, ratio: f64) -> usize {
    if value == 0 {
        return 0;
    }
    ((value as f64) * ratio).ceil().max(1.0) as usize
}

#[allow(clippy::trivially_copy_pass_by_ref)]
const fn is_false(value: &bool) -> bool {
    !*value
}

#[allow(clippy::cast_sign_loss, clippy::cast_possible_truncation)]
fn retry_after_ms(ratio: f64) -> u64 {
    let excess = (ratio - 0.85).max(0.0);
    (50.0 + (excess * 1_000.0)).clamp(50.0, 500.0) as u64
}

fn decision_reason(
    action: AdmissionAction,
    dominant_dimension: ResourceDimension,
    dominant_ratio: f64,
) -> String {
    match action {
        AdmissionAction::Admit => "host resources within budgets".to_string(),
        AdmissionAction::Backpressure => format!(
            "host resource pressure on {dominant_dimension:?} at {dominant_ratio:.2}x budget"
        ),
        AdmissionAction::Deny => format!(
            "host resource limit exceeded on {dominant_dimension:?} at {dominant_ratio:.2}x budget"
        ),
    }
}

#[cfg(target_os = "linux")]
fn read_load_avg_1m() -> Option<f64> {
    std::fs::read_to_string("/proc/loadavg")
        .ok()?
        .split_whitespace()
        .next()?
        .parse()
        .ok()
}

#[cfg(not(target_os = "linux"))]
const fn read_load_avg_1m() -> Option<f64> {
    None
}

#[cfg(target_os = "linux")]
fn read_self_rss_bytes() -> Option<u64> {
    let content = std::fs::read_to_string("/proc/self/statm").ok()?;
    let resident_pages: u64 = content.split_whitespace().nth(1)?.parse().ok()?;
    resident_pages.checked_mul(PROC_PAGE_SIZE_BYTES)
}

#[cfg(not(target_os = "linux"))]
const fn read_self_rss_bytes() -> Option<u64> {
    None
}

#[cfg(target_os = "linux")]
fn read_mem_total_bytes() -> Option<u64> {
    let content = std::fs::read_to_string("/proc/meminfo").ok()?;
    for line in content.lines() {
        let Some(rest) = line.strip_prefix("MemTotal:") else {
            continue;
        };
        let kb: u64 = rest.split_whitespace().next()?.parse().ok()?;
        return kb.checked_mul(1024);
    }
    None
}

#[cfg(not(target_os = "linux"))]
const fn read_mem_total_bytes() -> Option<u64> {
    None
}

#[cfg(target_os = "linux")]
fn count_proc_processes() -> Option<u64> {
    let mut count = 0_u64;
    for entry in std::fs::read_dir("/proc").ok()? {
        let entry = entry.ok()?;
        let name = entry.file_name();
        let name = name.to_string_lossy();
        if !name.is_empty() && name.bytes().all(|byte| byte.is_ascii_digit()) {
            count = count.saturating_add(1);
        }
    }
    Some(count)
}

#[cfg(not(target_os = "linux"))]
const fn count_proc_processes() -> Option<u64> {
    None
}

#[cfg(target_os = "linux")]
fn count_self_fds() -> Option<u64> {
    let count = std::fs::read_dir("/proc/self/fd").ok()?.count();
    u64::try_from(count).ok()
}

#[cfg(not(target_os = "linux"))]
const fn count_self_fds() -> Option<u64> {
    None
}

#[cfg(target_os = "linux")]
fn read_open_files_soft_limit() -> Option<u64> {
    let content = std::fs::read_to_string("/proc/self/limits").ok()?;
    for line in content.lines() {
        if !line.starts_with("Max open files") {
            continue;
        }
        let token = line.split_whitespace().nth(3)?;
        if matches!(token, "unlimited") {
            return None;
        }
        return token.parse().ok();
    }
    None
}

#[cfg(not(target_os = "linux"))]
const fn read_open_files_soft_limit() -> Option<u64> {
    None
}

#[cfg(test)]
mod tests {
    use super::{
        AdmissionAction, HostResourceBudgets, HostResourceSample, ResourceDimension,
        ResourceGovernor, ResourceOperationKind, ResourceRequest, TAIL_LATENCY_REGIME_SCHEMA,
        TailLatencyFallbackReason, TailLatencyRegime, TailLatencyRegimeConfig,
        TailLatencyRegimeGuard, TailLatencyRegimeSample,
    };

    fn budgets() -> HostResourceBudgets {
        HostResourceBudgets::fixed(10.0, 1_000, 100, 100, 1_000)
    }

    fn sample() -> HostResourceSample {
        HostResourceSample {
            load_avg_1m: Some(2.0),
            rss_bytes: Some(200),
            process_count: Some(20),
            fd_count: Some(20),
        }
    }

    fn tail_config() -> TailLatencyRegimeConfig {
        TailLatencyRegimeConfig::new(100, 500, 4, 0.80, 0.50, 2, 2)
    }

    #[test]
    fn admits_when_all_dimensions_are_below_backpressure_ratio() {
        let governor = ResourceGovernor::with_budgets(budgets());
        let request = ResourceRequest::new(ResourceOperationKind::Tool, "read")
            .with_estimated_tool_output_bytes(200);

        let decision = governor.admit_sample(&request, sample());

        assert_eq!(decision.action, AdmissionAction::Admit);
        assert_eq!(decision.dominant_dimension, ResourceDimension::CpuLoad);
    }

    #[test]
    fn backpressures_before_hard_overload() {
        let governor = ResourceGovernor::with_budgets(budgets());
        let request = ResourceRequest::new(ResourceOperationKind::Tool, "read")
            .with_estimated_tool_output_bytes(900);

        let decision = governor.admit_sample(&request, sample());

        assert_eq!(decision.action, AdmissionAction::Backpressure);
        assert_eq!(decision.dominant_dimension, ResourceDimension::ToolOutput);
        assert!(decision.retry_after_ms >= 50);
    }

    #[test]
    fn denies_when_a_dimension_exceeds_the_deny_ratio() {
        let governor = ResourceGovernor::with_budgets(budgets());
        let request = ResourceRequest::new(ResourceOperationKind::Exec, "exec")
            .with_estimated_tool_output_bytes(1_200);

        let decision = governor.admit_sample(&request, sample());

        assert_eq!(decision.action, AdmissionAction::Deny);
        assert_eq!(decision.dominant_dimension, ResourceDimension::ToolOutput);
    }

    #[test]
    fn queue_depth_participates_in_admission_pressure() {
        let governor = ResourceGovernor::with_budgets(HostResourceBudgets::fixed_with_queue_depth(
            10.0, 1_000, 100, 100, 1_000, 4,
        ));
        let request =
            ResourceRequest::new(ResourceOperationKind::Events, "events").with_queue_depth(5);

        let decision = governor.admit_sample(&request, sample());

        assert_eq!(decision.action, AdmissionAction::Deny);
        assert_eq!(decision.dominant_dimension, ResourceDimension::QueueDepth);
    }

    #[test]
    fn ignores_unavailable_host_metrics_but_still_checks_request_size() {
        let governor = ResourceGovernor::with_budgets(budgets());
        let request = ResourceRequest::new(ResourceOperationKind::Exec, "exec")
            .with_estimated_tool_output_bytes(1_200);
        let sample = HostResourceSample {
            load_avg_1m: None,
            rss_bytes: None,
            process_count: None,
            fd_count: None,
        };

        let decision = governor.admit_sample(&request, sample);

        assert_eq!(decision.action, AdmissionAction::Deny);
        assert_eq!(decision.dominant_dimension, ResourceDimension::ToolOutput);
    }

    #[test]
    fn telemetry_contains_stable_schema() {
        let governor = ResourceGovernor::with_budgets(budgets());
        let request = ResourceRequest::new(ResourceOperationKind::Session, "session");
        let decision = governor.admit_sample(&request, sample());

        let telemetry = decision.telemetry(&request);

        assert_eq!(
            telemetry.get("schema").and_then(serde_json::Value::as_str),
            Some("pi.resource_governor.admission.v1")
        );
        assert_eq!(
            telemetry
                .get("decision")
                .and_then(|value| value.get("action"))
                .and_then(serde_json::Value::as_str),
            Some("admit")
        );
    }

    #[test]
    fn tail_latency_regime_telemetry_contains_stable_schema() {
        let mut guard = TailLatencyRegimeGuard::new(TailLatencyRegimeConfig::new(
            100, 500, 4, 0.80, 0.50, 1, 2,
        ));
        let decision = guard.observe(TailLatencyRegimeSample::new(150, 700, 8, 0.90));

        let telemetry = decision.telemetry();

        assert_eq!(
            telemetry.get("schema").and_then(serde_json::Value::as_str),
            Some(TAIL_LATENCY_REGIME_SCHEMA)
        );
        assert_eq!(
            telemetry
                .get("decision")
                .and_then(|value| value.get("regime"))
                .and_then(serde_json::Value::as_str),
            Some("conservative_fallback")
        );
        assert_eq!(
            telemetry
                .get("decision")
                .and_then(|value| value.get("sample"))
                .and_then(|value| value.get("queue_depth"))
                .and_then(serde_json::Value::as_u64),
            Some(8)
        );
    }

    #[test]
    fn tail_latency_guard_requires_consecutive_spikes_before_fallback() {
        let mut guard = TailLatencyRegimeGuard::new(tail_config());
        let spike = TailLatencyRegimeSample::new(150, 700, 8, 0.90);

        let first = guard.observe(spike);
        assert_eq!(first.regime, TailLatencyRegime::Calibrated);
        assert!(!first.fallback_active);
        assert_eq!(first.bad_sample_streak, 1);
        assert!(
            first
                .reasons
                .contains(&TailLatencyFallbackReason::P99Latency)
        );
        assert!(
            first
                .reasons
                .contains(&TailLatencyFallbackReason::P999Latency)
        );
        assert!(
            first
                .reasons
                .contains(&TailLatencyFallbackReason::QueueDepth)
        );
        assert!(
            first
                .reasons
                .contains(&TailLatencyFallbackReason::ResourcePressure)
        );

        let second = guard.observe(spike);
        assert_eq!(second.regime, TailLatencyRegime::ConservativeFallback);
        assert!(second.fallback_active);
        assert!(second.changed);
        assert_eq!(second.bad_sample_streak, 2);
    }

    #[test]
    fn tail_latency_guard_hysteresis_requires_recovery_sequence() {
        let mut guard = TailLatencyRegimeGuard::new(tail_config());
        let spike = TailLatencyRegimeSample::new(150, 700, 8, 0.90);
        guard.observe(spike);
        guard.observe(spike);

        let recovered = TailLatencyRegimeSample::new(40, 200, 2, 0.30);
        let first_recovery = guard.observe(recovered);
        assert_eq!(
            first_recovery.regime,
            TailLatencyRegime::ConservativeFallback
        );
        assert!(first_recovery.fallback_active);
        assert!(
            first_recovery
                .reasons
                .contains(&TailLatencyFallbackReason::HysteresisHold)
        );
        assert_eq!(first_recovery.recovery_sample_streak, 1);

        let second_recovery = guard.observe(recovered);
        assert_eq!(second_recovery.regime, TailLatencyRegime::Calibrated);
        assert!(!second_recovery.fallback_active);
        assert!(second_recovery.changed);
        assert!(second_recovery.reasons.is_empty());
    }

    #[test]
    fn tail_latency_fallback_applies_conservative_budgets_to_admission() {
        let governor = ResourceGovernor::with_budgets(HostResourceBudgets::fixed_with_queue_depth(
            10.0, 1_000, 100, 100, 1_000, 16,
        ));
        let request = ResourceRequest::new(ResourceOperationKind::Tool, "read")
            .with_estimated_tool_output_bytes(600)
            .with_queue_depth(4);
        let normal = governor.admit_sample(&request, sample());
        assert_eq!(normal.action, AdmissionAction::Admit);

        let mut guard = TailLatencyRegimeGuard::new(TailLatencyRegimeConfig::new(
            100, 500, 4, 0.80, 0.50, 1, 2,
        ));
        let (fallback, regime) = governor.admit_sample_with_tail_latency_guard(
            &request,
            sample(),
            &mut guard,
            TailLatencyRegimeSample::new(150, 700, 8, 0.90),
        );

        assert!(regime.fallback_active);
        assert_eq!(fallback.action, AdmissionAction::Deny);
        assert!(fallback.conservative_fallback_active);
        assert!(
            fallback
                .fallback_reasons
                .contains(&TailLatencyFallbackReason::P99Latency)
        );
        assert_eq!(fallback.budgets.max_tool_output_bytes, 500);
    }
}
