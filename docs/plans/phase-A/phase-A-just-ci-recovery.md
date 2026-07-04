# Phase A - Minimal Just / CI Recovery

Date: 2026-07-03
Status: planning
Authoritative scope: corrected Phase A planning

## Purpose

Phase A recovers the `just` + CI effort by starting from a minimal working
baseline and then adding one small production-ready increment at a time.

This corrected plan replaces the invalid rollout merged by PR #5.

## Authoritative Document Layout

This phase uses:

- phase overview:
  - `docs/plans/phase-A/phase-A-just-ci-recovery.md`
- phase testing strategy:
  - `docs/plans/phase-A/phase-A-testing-strategy.md`
- sprint plans:
  - `docs/plans/phase-A/sprint-a-1-establish-minimal-baseline-gate.md`
  - `docs/plans/phase-A/sprint-a-2-add-local-code-lint.md`
  - `docs/plans/phase-A/sprint-a-3-add-smoke-baseline.md`
  - `docs/plans/phase-A/sprint-a-4-add-taxonomy-helpers.md`
  - `docs/plans/phase-A/sprint-a-5-add-optional-local-lanes.md`
  - `docs/plans/phase-A/sprint-a-6-refresh-ssot-and-timing.md`
  - `docs/plans/phase-A/sprint-a-7-merge-baseline-into-atm-graft.md`

Only these docs are authoritative for corrected Phase A.

## Planning Rules

This phase follows:

- `/Volumes/Extreme Pro/github/atm-core/.claude/skills/plan-hardening/sprint-planning-guidelines.md`
- `/Volumes/Extreme Pro/github/atm-core/.claude/skills/codex-orchestration/sprint-plan.md.j2`

Applied interpretation for this phase:

- one sprint, one deliverable, one PR
- each sprint must land production-ready for the scope it claims
- no sprint may rely on the old heavyweight PR workflow surface remaining active
- no sprint may silently carry a required deliverable forward
- every sprint must preserve green required PR CI under 10 minutes

## Branch And Worktree Model

Corrected Phase A does not use an `integrate/phase-A` merge-forward branch.

Instead:

- planning branch:
  - `plan/phase-A`
- implementation target branch:
  - `develop`
- sprint branches:
  - cut directly from updated `develop`
- sprint worktrees:
  - one dedicated worktree per sprint branch

Execution model:

1. team-lead reviews and approves the testing strategy
2. Sprint A1 branches from `develop`
3. Sprint A1 merges back to `develop` only after green `baseline` CI
4. Sprint A2 branches from updated `develop`
5. repeat through Sprint A7

This branch model is required because the first shipped baseline must land
immediately, not after an integration branch has accumulated multiple sprints.

## Ground Rules

- do not work on `main`
- do not merge `feature/just-integration` wholesale
- do not reintroduce exploratory `src/**` churn as part of Phase A
- reuse only narrow proven pieces from `feature/just-integration`
- `just` is the only local operator surface
- the required `baseline` workflow and new Phase A fast-lane workflow edits must
  call `just` commands rather than bespoke cargo command strings
- required PR CI must stay below 10 minutes in every implementation sprint
- heavyweight workflows must not run on ordinary PRs after Sprint A1 lands

## Upstream Fork Testing Reality

This repository is a fork of the public upstream
`Dicklesworthstone/pi_agent_rust`.

Current upstream ordinary-PR testing surfaces that Phase A must classify rather
than ignore:

- `.github/workflows/ci.yml`
  - cross-OS build/test/policy workflow on `pull_request`
- `.github/workflows/conformance.yml`
  - extension conformance PR matrix on `pull_request`
  - checks out sibling repositories and installs Bun / npm dependencies
- `.github/workflows/fuzz.yml`
  - Linux fuzz PR workflow for PRs targeting `main`
- `.github/workflows/semver.yml`
  - path-filtered PR API compatibility workflow
- `.github/workflows/model-catalog-drift.yml`
  - path-filtered advisory PR drift workflow

Phase A is allowed to reduce ordinary PR gating to `baseline`, but only if the
testing strategy documents what each displaced upstream workflow currently
proves, how it will still be runnable after Sprint A1, and why the ordinary PR
gate is no longer the right place for it.

This is a fork-risk rule, not an optional note. "Simple CI green" for Sprint A1
means a deliberately reduced required PR gate, not permission to forget what
the upstream fork already validates.

## Safe Reuse Inventory

Safe reuse candidates from `feature/just-integration`:

- `justfile`
- `.just/print_help.py`
- `.just/run_fmt.py`
- `.just/run_cargo.py`
- `.just/run_lint.py`
- `.just/lint_catalog.py`
- `.just/run_test.py`
- `.just/test_catalog.py`
- `.just/explain.py`
- `.just/show_suites.py`
- `.github/workflows/baseline.yml`
- `scripts/smoke.sh`

Exact on-disk reference paths:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/justfile`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/print_help.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_fmt.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_cargo.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_lint.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/lint_catalog.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_test.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/test_catalog.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/explain.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/show_suites.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.github/workflows/baseline.yml`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/scripts/smoke.sh`

Do not reuse directly:

- any exploratory `src/**` change
- broad workflow rewrites that try to preserve monolithic PR CI
- shard orchestration and artifact plumbing from exploratory CI work
- broad test rewrites made only to chase green CI

## Retained Evidence

Observed local macOS timings from `feature/just-integration`:

- `just help`: `<1s`
- `just fmt check`: `12.46s`
- `just lint clippy-lib`: `50.66s`
- `just lint clippy-bins`: `2.87s`
- `just test baseline`: `10.59s`
- `just lint clippy-tests`: `>3m38s` before manual stop
- `just test unit`: `>120s` before timeout
- `just test integration`: `>120s` before timeout

Observed GitHub Actions timings from 2026-07-02:

- `baseline`: `~7m03s`
- `Extension Conformance`: `~6m25s`
- `Fuzz CI`: `~42m59s`
- old monolithic `ci`: `~49m25s` before cancellation

Implications:

- a fast required PR baseline is viable
- `clippy --tests` does not belong in required PR CI
- broad `cargo test` orchestration does not belong in required PR CI
- `fuzz`, `bench`, and `semver` must stay outside ordinary PR gating
- upstream PR-only specialty workflows must be explicitly classified before
  Sprint A1 changes any triggers

## Known Issues To Preserve

- Bash 3 portability still matters on macOS
- `just clean` previously failed against `target/agents/...` on macOS
- a `vergen-lib` local build-script issue was observed in exploratory runs
- prior fuzz failures hit `sysinfo` / nightly drift
- historical CI used wrong working-directory paths

These notes remain valid even though the old rollout plan was superseded.

## Corrected Sprint Sequence

| Sprint | Branch | Worktree | Single deliverable | Required PR CI after merge |
|---|---|---|---|---|
| A1 | `sprint-a-1-establish-minimal-baseline-gate` | `../pi_agent_atm-worktrees/sprint-a-1-establish-minimal-baseline-gate` | minimal `just` + tiny `baseline` workflow | `just help`, `just fmt check` |
| A2 | `sprint-a-2-add-local-code-lint` | `../pi_agent_atm-worktrees/sprint-a-2-add-local-code-lint` | local-code lint through `just lint` | A1 + `just lint clippy-bins`, `just lint clippy-lib` |
| A3 | `sprint-a-3-add-smoke-baseline` | `../pi_agent_atm-worktrees/sprint-a-3-add-smoke-baseline` | smoke regression lane through `just test` | A2 + `just test baseline` |
| A4 | `sprint-a-4-add-taxonomy-helpers` | `../pi_agent_atm-worktrees/sprint-a-4-add-taxonomy-helpers` | taxonomy helpers only | unchanged from A3 |
| A5 | `sprint-a-5-add-optional-local-lanes` | `../pi_agent_atm-worktrees/sprint-a-5-add-optional-local-lanes` | optional local lanes only | unchanged from A3 |
| A6 | `sprint-a-6-refresh-ssot-and-timing` | `../pi_agent_atm-worktrees/sprint-a-6-refresh-ssot-and-timing` | freeze SSOT and refresh timing evidence | unchanged from A3 |
| A7 | `sprint-a-7-merge-baseline-into-atm-graft` | `../pi_agent_atm-worktrees/sprint-a-7-merge-baseline-into-atm-graft` | merge verified baseline into `feature/atm-graft-integration` | unchanged from A3 on merge PRs |

### Sprint A1

Deliverable:

- minimal `just` operator surface plus one tiny required `baseline` workflow

Outcome:

- old heavyweight PR workflows stop running on ordinary PRs
- required PR CI becomes `baseline` immediately

### Sprint A2

Deliverable:

- add local-code lint through the established `just lint` surface

Outcome:

- required PR CI gains local-code lint coverage while staying under budget

### Sprint A3

Deliverable:

- add a tiny deterministic smoke lane through the established `just test`
  surface

Outcome:

- required PR CI proves the repo still basically works without broad test churn

### Sprint A4

Deliverable:

- add taxonomy helpers only without changing required PR CI

Outcome:

- operators can inspect lane semantics and suite taxonomy without changing the
  required PR gate

### Sprint A5

Deliverable:

- add optional local lanes without changing required PR CI

Outcome:

- agents get richer local commands without changing the required PR gate

### Sprint A6

Deliverable:

- freeze SSOT ownership and refresh timing evidence using the established
  command surface

Outcome:

- team-lead gets a reviewed timing-backed strategy before the baseline merges
  into `atm-graft`

### Sprint A7

Deliverable:

- merge the verified baseline into `feature/atm-graft-integration`

Outcome:

- the `atm-graft` line starts from the corrected `just` + CI baseline instead
  of carrying forward the abandoned exploratory work

## Team-Lead Review Gate

No implementation sprint begins until team-lead reviews:

- `docs/plans/phase-A/phase-A-testing-strategy.md`
- the exact baseline command list
- the workflow files removed from ordinary PR gating
- the upstream PR-workflow inventory and its post-A1 trigger classification
- the sprint ordering that makes Sprint A1 establish the required PR gate
- the A4 / A5 split between taxonomy helpers and optional local lanes

## Exit Criteria

Phase A is complete when:

- `baseline` is the only required PR workflow
- required PR CI on ordinary PRs is limited to the `baseline` workflow surface
- `baseline` stays below 10 minutes
- local `just` commands and required PR CI share the same lane definitions
- heavyweight workflows no longer run on ordinary PRs
- the verified baseline is merged into `feature/atm-graft-integration`
