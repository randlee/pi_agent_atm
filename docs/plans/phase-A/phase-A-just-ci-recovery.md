# Phase A - Minimal Just / CI Recovery

Date: 2026-07-04
Status: complete
Branch: `plan/phase-A`
Worktree: `../pi_agent_atm-worktrees/plan/phase-A`
Authoritative scope: corrected Phase A planning

## Purpose

Phase A recovers the `just` + CI effort by starting from a minimal working
baseline and then adding one small production-ready increment at a time.

This corrected plan replaces the invalid rollout merged by PR #5.

Supporting evidence for this correction:

- `reports/pi-agent-rust/local-test-surface-review-2026-07-03.md`
- `reports/pi-agent-rust/upstream-testing-contract-review-2026-07-03.md`
- `reports/pi-agent-rust/just-layering-and-atm-integration-strategy-2026-07-03.md`

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

- `.claude/skills/plan-hardening/sprint-planning-guidelines.md`
- `.claude/skills/codex-orchestration/sprint-plan.md.j2`

Applied interpretation for this phase:

- one sprint, one deliverable, one PR
- each sprint must land production-ready for the scope it claims
- no sprint may rely on the old heavyweight PR workflow surface remaining active
- no sprint may silently carry a required deliverable forward
- every sprint must preserve green required PR CI under 10 minutes
- standing process gap from A4 and A5 QA: sprint docs that add or widen lane
  catalogs must predeclare the runner/helper files those lanes require
  (`.just/run_*.py`, `.just/show_suites.py`, `.just/print_help.py`) in Exact
  Targets instead of only the public catalog files

## Branch And Worktree Model

Corrected Phase A now uses a merge-forward sprint chain so each sprint PR can
run CI against the immediately preceding sprint surface and fixes can merge
forward through the active worktrees.

Branch model:

- planning branch:
  - `plan/phase-A`
- merge-root branch:
  - `integrate/phase-A`
- sprint branches:
  - `sprint-a-1-establish-minimal-baseline-gate` targets `integrate/phase-A`
  - `sprint-a-2-add-local-code-lint` targets A1
  - `sprint-a-3-add-smoke-baseline` targets A2
  - `sprint-a-4-add-taxonomy-helpers` targets A3
  - `sprint-a-5-add-optional-local-lanes` targets A4
  - `sprint-a-6-refresh-ssot-and-timing` targets A5
  - `sprint-a-7-merge-baseline-into-atm-graft` merges the verified chain into
    `feature/atm-graft-integration`
- sprint worktrees:
  - one dedicated worktree per sprint branch

Execution model:

1. team-lead reviews and approves the testing strategy
2. Sprint A1 targets `integrate/phase-A`
3. Sprint A2 through A6 target the immediately previous sprint branch
4. once a sprint is fixed, merge that work forward into the next sprint
   worktree before expecting CI to run there
5. Sprint A7 merges the verified Phase A chain into
   `feature/atm-graft-integration`

This branch model is required because the sprint chain is being executed
back-to-back on separate worktrees and each PR must validate against the
actual previous increment, not against an older `develop` snapshot.

## Ground Rules

- do not work on `main`
- do not merge `feature/just-integration` wholesale
- do not reintroduce exploratory `src/**` churn as part of Phase A
- reuse only narrow proven pieces from `feature/just-integration`
- `just` is the only local operator surface
- the required `baseline` workflow and new Phase A fast-lane workflow edits must
  call `just` commands rather than bespoke cargo command strings
- compile checking and strict basic-unit coverage must land before local-code
  lint expansion or smoke-lane expansion
- required PR CI must stay below 10 minutes in every implementation sprint
- heavyweight workflows must not run on ordinary PRs after Sprint A1 lands
- the Phase A baseline lanes become the stable upstream-regression contract
- future ATM-owned lanes must layer in additively through `just lint` and
  `just test`, not by mutating the meaning of the baseline lanes
- future ATM integration should follow the actual
  `feature/atm-graft-integration` model: root `Cargo.toml` dependency wiring to
  `atm-core` crates plus narrowly scoped local shim/integration surfaces

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
- `.github/workflows/bench.yml`
  - benchmark PR workflow that remains outside ordinary required PR gating
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

Observed GitHub Actions timings from 2026-07-04:

- Sprint A1 command steps (`just help` through `just test unit-basic`):
  `9m45s` on run `28698960460`
- Sprint A2 command steps (`just help` through `just lint clippy-lib`):
  `12m07s` on run `28698763616`
- current step-level detail lives in
  `docs/plans/phase-A/phase-A-testing-strategy.md`

Implications:

- a fast required PR baseline is viable
- `clippy --tests` does not belong in required PR CI
- broad `cargo test` orchestration does not belong in required PR CI
- the current A2 green evidence is still over the 10-minute budget and must be
  reported honestly until a later green run proves otherwise
- `fuzz`, `bench`, and `semver` must stay outside ordinary PR gating
- upstream PR-only specialty workflows must be explicitly classified before
  Sprint A1 changes any triggers
- `suite.unit` is too broad to serve as the first basic-unit gate without an
  explicit allowlist

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
| A1 | `sprint-a-1-establish-minimal-baseline-gate` | `../pi_agent_atm-worktrees/sprint-a-1-establish-minimal-baseline-gate` | minimal `just` + compile/unit-baseline workflow | `just help`, `just fmt check`, `just test compile`, `just test unit-basic` |
| A2 | `sprint-a-2-add-local-code-lint` | `../pi_agent_atm-worktrees/sprint-a-2-add-local-code-lint` | local-code lint through `just lint` | A1 + `just lint clippy-bins`, `just lint clippy-lib` |
| A3 | `sprint-a-3-add-smoke-baseline` | `../pi_agent_atm-worktrees/sprint-a-3-add-smoke-baseline` | smoke regression lane through `just test` | A2 + `just test baseline` |
| A4 | `sprint-a-4-add-taxonomy-helpers` | `../pi_agent_atm-worktrees/sprint-a-4-add-taxonomy-helpers` | taxonomy helpers only | unchanged from A3 |
| A5 | `sprint-a-5-add-optional-local-lanes` | `../pi_agent_atm-worktrees/sprint-a-5-add-optional-local-lanes` | optional local lanes only | unchanged from A3 |
| A6 | `sprint-a-6-refresh-ssot-and-timing` | `../pi_agent_atm-worktrees/sprint-a-6-refresh-ssot-and-timing` | freeze SSOT and refresh timing evidence | unchanged from A3 |
| A7 | `sprint-a-7-merge-baseline-into-atm-graft` | `../pi_agent_atm-worktrees/sprint-a-7-merge-baseline-into-atm-graft` | merge verified baseline into `feature/atm-graft-integration` | unchanged from A3 on merge PRs |

### Sprint A1

Deliverable:

- minimal `just` operator surface plus one tiny required `baseline` workflow
  that proves compile health and strict basic-unit health first

Outcome:

- old heavyweight PR workflows stop running on ordinary PRs
- required PR CI becomes `baseline` immediately
- the first required baseline proves compile health before lint expansion
- the first required baseline proves a strict basic-unit subset rather than the
  whole broad `[suite.unit]` bucket

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

- operators can inspect lane semantics, ownership, and suite taxonomy without
  changing the required PR gate

### Sprint A5

Deliverable:

- add optional local lanes without changing required PR CI

Outcome:

- agents get richer local commands, including future ATM-owned or integration
  lanes, without changing the required PR gate

### Sprint A6

Deliverable:

- freeze SSOT ownership and refresh timing evidence using the established
  command surface

Outcome:

- team-lead gets a reviewed timing-backed strategy plus the frozen ATM layering
  framework before the baseline merges into `atm-graft`

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
- the `unit-basic` allowlist and exclusion rationale
- the sprint ordering that makes Sprint A1 establish the required PR gate
- the A4 / A5 split between taxonomy helpers and optional local lanes
- the future `just` lane taxonomy for upstream, ATM-owned, and integration
  lanes
- the planned dependency and glue surfaces already present on
  `feature/atm-graft-integration`

### Team-Lead Review Record

Reviewer: `team-lead`
Review date: `2026-07-03`
Confirmation: team-lead reviewed and approved this Phase A plan on
`2026-07-03`; the review gate is closed and implementation may begin from this
approved planning baseline.

Review-item record:

- `docs/plans/phase-A/phase-A-testing-strategy.md`
  - status: approved by team-lead, 2026-07-03
- the exact baseline command list
  - status: approved by team-lead, 2026-07-03
- the workflow files removed from ordinary PR gating
  - status: approved by team-lead, 2026-07-03
- the upstream PR-workflow inventory and its post-A1 trigger classification
  - status: approved by team-lead, 2026-07-03
- the `unit-basic` allowlist and exclusion rationale
  - status: approved by team-lead, 2026-07-03
- the sprint ordering that makes Sprint A1 establish the required PR gate
  - status: approved by team-lead, 2026-07-03
- the A4 / A5 split between taxonomy helpers and optional local lanes
  - status: approved by team-lead, 2026-07-03
- the future `just` lane taxonomy for upstream, ATM-owned, and integration
  lanes
  - status: approved by team-lead, 2026-07-03
- the planned dependency and glue surfaces already present on
  `feature/atm-graft-integration`
  - status: approved by team-lead, 2026-07-03

Implementation-start rule:

- `Status: complete` now applies because team-lead explicitly closed every
  review item above on `2026-07-03` and the review gate is satisfied

## Upstream Workflow Trigger Reconciliation

Recurring upstream merges may reintroduce ordinary-PR triggers on heavyweight
workflow files. When that happens, Phase A must reconcile the conflict this way:

1. preserve the strategy rule that only `baseline` remains required on ordinary
   PRs
2. reapply the documented retained triggers for `ci`, `conformance`, `fuzz`,
   `bench`, `semver`, and `model-catalog-drift`
3. treat trigger-only workflow edits as isolated reconciliations unless the
   underlying workflow contract is intentionally being re-scoped
4. rerun the A1 workflow-view validation and record the reconciliation result in
   the sprint PR notes

## Exit Criteria

Phase A is complete when:

- `baseline` is the only required PR workflow
- `baseline` is the only required branch-protection status check for ordinary
  PRs once the Sprint A1 operational branch-protection update lands
- required PR CI on ordinary PRs is limited to the `baseline` workflow surface
- `baseline` stays below 10 minutes
- local `just` commands and required PR CI share the same lane definitions
- heavyweight workflows no longer run on ordinary PRs
- the verified baseline is merged into `feature/atm-graft-integration`
- the frozen `just` taxonomy still leaves a clean additive path for ATM-owned
  crates without broad upstream churn
