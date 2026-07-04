# Phase A - Minimal Just / CI Recovery

Date: 2026-07-04
Status: blocked pending branch-and-ci reconciliation
Branch: `docs/phase-a-plan-updates`
Worktree: `../pi_agent_atm-worktrees/docs/phase-a-plan-updates`
PR target: `develop`
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
- no implementation code should merge back into `develop` until the Phase A
  salvage chain is proven
- no sprint should merge into `integrate/phase-A` without a recorded evidence
  package that includes registration, execution, and timing proof
- every sprint PR must record both:
  - local wall-clock timings for the sprint's in-scope commands
  - equivalent CI step and total workflow timings for the same stage, or an
    explicit `no ci equivalent by design` note for local-only lanes

## Branch And Worktree Model

The previously documented branch model was incorrect.

Live evidence collected on 2026-07-04 shows:

- Sprint A1 open PR #12 targets `integrate/phase-A`
- Sprint A2 open PR #11 targets `sprint-a-1-establish-minimal-baseline-gate`
- Sprint A3 open PR #13 targets `sprint-a-2-add-local-code-lint`
- Sprint A4 open PR #14 targets `sprint-a-3-add-smoke-baseline`
- Sprint A5 open PR #15 targets `sprint-a-4-add-taxonomy-helpers`
- Sprint A6 open PR #16 targets `integrate/phase-A`
- Sprint A7 open PR #17 targets `feature/atm-graft-integration`
- earlier merged PRs also exist for A1 and A2 into `integrate/phase-A`
  (PR #9 and PR #10), so the live state is a mixed merge history plus an open
  stacked chain, not a clean one-pass rollout from `develop`

Additional branch-state evidence:

- `origin/develop` currently contains none of:
  - `justfile`
  - `.just/**`
  - `.github/workflows/baseline.yml`
- `origin/integrate/phase-A` currently contains none of:
  - `justfile`
  - `.just/**`
  - `.github/workflows/baseline.yml`

The current sprint branches themselves do contain the `just` surface and
`baseline.yml`, so the plan has to distinguish between:

- branch-local sprint content that exists on the sprint branches
- missing substrate on `origin/develop` and `origin/integrate/phase-A`
- a separate GitHub Actions registration gap on A3-A6

Historical reality, as verified, is therefore:

1. Phase A has in practice been executed as a stacked PR chain, not as direct
   merge-backs to `develop`
2. `integrate/phase-A` has been used as an integration target in the actual PR
   history
3. the current docs were encoding the wrong branch model and were a source of
   confusion

Salvage model going forward:

1. a bootstrap worktree may be created from `develop` because that branch holds
   the current planning docs
2. that bootstrap does not authorize merging unproven Phase A implementation
   code back into `develop`
3. Phase A implementation should continue as a proof-first merge chain where
   each sprint branch demonstrates real CI progression before merge-forward
4. `integrate/phase-A` should be treated as the accumulation branch for proven
   Phase A sprint outputs
5. `feature/atm-graft-integration` remains the Phase A consumer branch in A7

## Live CI Registration Findings

Evidence collected on 2026-07-04 shows this split:

- `sprint-a-1-establish-minimal-baseline-gate`
  - registered runs present
  - latest sampled result: `baseline` success
- `sprint-a-2-add-local-code-lint`
  - registered runs present
  - latest sampled result: `baseline` success
- `sprint-a-3-add-smoke-baseline`
  - zero registered runs
- `sprint-a-4-add-taxonomy-helpers`
  - zero registered runs
- `sprint-a-5-add-optional-local-lanes`
  - zero registered runs
- `sprint-a-6-refresh-ssot-and-timing`
  - zero registered runs

This means the current CI gap is not fully explained by missing `justfile` or
`.just/**` on `develop` and `integrate/phase-A`.

What the evidence does support:

- missing `just` substrate on `develop` and `integrate/phase-A` explains why a
  baseline workflow on those branches would fail immediately
- zero-run behavior on A3-A6 is a separate registration problem because those
  sprint branches do contain both `baseline.yml` and the required `just`
  surface

What the evidence does not yet explain:

- why A3-A6 registered zero runs while A1-A2 registered runs with the same
  named workflow and equivalent `just` invocation pattern

The plan must therefore preserve this as an open incident rather than papering
it over with a single-cause theory.

## Remediation Tasks

Before Phase A can be considered back on track, these live PRs must each carry
their own evidence package or be reset and re-cut:

- PR #11 `sprint-a-2-add-local-code-lint`
- PR #12 `sprint-a-1-establish-minimal-baseline-gate`
- PR #13 `sprint-a-3-add-smoke-baseline`
- PR #14 `sprint-a-4-add-taxonomy-helpers`
- PR #15 `sprint-a-5-add-optional-local-lanes`
- PR #16 `sprint-a-6-refresh-ssot-and-timing`
- PR #17 `sprint-a-7-merge-baseline-into-atm-graft`

Required backfill for each PR:

- workflow registration proof for the exact head SHA
- workflow execution proof, including failed-log review if red
- timing tables that follow the Sprint Timing Deliverable Contract:
  - local wall-clock measurements for the sprint's in-scope commands
  - CI step and total workflow measurements
  - exact CI run URL/ID recorded for each timing measurement
- confirmation that the PR base branch actually contains the expected baseline
  substrate after merge-forward

If any PR cannot supply that evidence cleanly, it should be reset or re-cut
from the last proven state instead of being treated as implicitly valid.

## Sprint Timing Deliverable Contract

Quality-mgr timing capture is a required artifact for every Phase A sprint PR.

Each sprint PR must include:

- a local timing table for every command added or validated in that sprint
- a CI timing table for the equivalent `baseline` step set and total workflow
  duration
- an explicit `no ci equivalent by design` note for local-only helper or
  optional lanes
- links or identifiers for the exact CI runs used for timing capture

CI timing must come from reading existing GitHub Actions run and job data for
the sprint branch; Phase A should not add timing-only instrumentation steps to
`baseline.yml`.

Rollup requirements:

- Sprint A6 review-pack materials must consolidate the timing tables for A1-A6
- Sprint A7 phase conclusion materials must consolidate the timing tables for
  A1-A7 and report the final progression of required baseline cost by sprint

## Ground Rules

- do not work on `main`
- do not merge `feature/just-integration` wholesale
- do not treat `develop` as the active accumulation branch for Phase A code
- do not reintroduce exploratory `src/**` churn as part of Phase A
- reuse only narrow proven pieces from `feature/just-integration`
- `just` is the only local operator surface
- the required `baseline` workflow and new Phase A fast-lane workflow edits must
  call `just` commands rather than bespoke cargo command strings
- compile checking and strict basic-unit coverage must land before local-code
  lint expansion or smoke-lane expansion
- required PR CI must stay below 10 minutes in every implementation sprint
- every sprint evidence package must include:
  - workflow registration proof
  - workflow execution proof
  - local timings
  - CI timings
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

| Sprint | Branch | Worktree | Live PR base | Live PR state | Single deliverable | Required PR CI after merge |
|---|---|---|---|---|---|---|
| A1 | `sprint-a-1-establish-minimal-baseline-gate` | `../pi_agent_atm-worktrees/sprint-a-1-establish-minimal-baseline-gate` | `integrate/phase-A` | open PR #12; earlier merged PR #9 | minimal `just` + compile/unit-baseline workflow | `just help`, `just fmt check`, `just test compile`, `just test unit-basic` |
| A2 | `sprint-a-2-add-local-code-lint` | `../pi_agent_atm-worktrees/sprint-a-2-add-local-code-lint` | `sprint-a-1-establish-minimal-baseline-gate` | open PR #11; earlier merged PR #10 to `integrate/phase-A` | local-code lint through `just lint` | A1 + `just lint clippy-bins`, `just lint clippy-lib` |
| A3 | `sprint-a-3-add-smoke-baseline` | `../pi_agent_atm-worktrees/sprint-a-3-add-smoke-baseline` | `sprint-a-2-add-local-code-lint` | open PR #13 | smoke regression lane through `just test` | A2 + `just test baseline` |
| A4 | `sprint-a-4-add-taxonomy-helpers` | `../pi_agent_atm-worktrees/sprint-a-4-add-taxonomy-helpers` | `sprint-a-3-add-smoke-baseline` | open PR #14 | taxonomy helpers only | unchanged from A3 |
| A5 | `sprint-a-5-add-optional-local-lanes` | `../pi_agent_atm-worktrees/sprint-a-5-add-optional-local-lanes` | `sprint-a-4-add-taxonomy-helpers` | open PR #15 | optional local lanes only | unchanged from A3 |
| A6 | `sprint-a-6-refresh-ssot-and-timing` | `../pi_agent_atm-worktrees/sprint-a-6-refresh-ssot-and-timing` | `integrate/phase-A` | open PR #16 | freeze SSOT and refresh timing evidence | unchanged from A3 |
| A7 | `sprint-a-7-merge-baseline-into-atm-graft` | `../pi_agent_atm-worktrees/sprint-a-7-merge-baseline-into-atm-graft` | `feature/atm-graft-integration` | open PR #17 | merge verified baseline into `feature/atm-graft-integration` | unchanged from A3 on merge PRs |

### Sprint A1

Deliverable:

- minimal `just` operator surface plus one tiny required `baseline` workflow
  that proves compile health and strict basic-unit health first

Outcome:

- old heavyweight PR workflows stop running on ordinary PRs
- required PR CI becomes `baseline` on the A1 branch path
- the first required baseline proves compile health before lint expansion
- the first required baseline proves a strict basic-unit subset rather than the
  whole broad `[suite.unit]` bucket
- the live PR target for A1 is `integrate/phase-A`, not `develop`

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
- the evidence-backed correction that live sprint PRs are stacked and do use
  `integrate/phase-A`
- the open CI-registration incident affecting A3-A6

### Team-Lead Review Record

Reviewer: `team-lead`
Review date: `2026-07-03`
Confirmation: the previous approval text is now stale because the branch model
and CI state encoded in this doc were contradicted by live git/GitHub evidence
collected on `2026-07-04`. Implementation remains blocked until the corrected
branch model and CI-registration gap are reviewed again.

Review-item record:

- `docs/plans/phase-A/phase-A-testing-strategy.md`
  - status: SUPERSEDED -- re-review required 2026-07-04; previously approved by team-lead, 2026-07-03
- the exact baseline command list
  - status: SUPERSEDED -- re-review required 2026-07-04; previously approved by team-lead, 2026-07-03
- the workflow files removed from ordinary PR gating
  - status: SUPERSEDED -- re-review required 2026-07-04; previously approved by team-lead, 2026-07-03
- the upstream PR-workflow inventory and its post-A1 trigger classification
  - status: SUPERSEDED -- re-review required 2026-07-04; previously approved by team-lead, 2026-07-03
- the `unit-basic` allowlist and exclusion rationale
  - status: SUPERSEDED -- re-review required 2026-07-04; previously approved by team-lead, 2026-07-03
- the sprint ordering that makes Sprint A1 establish the required PR gate
  - status: SUPERSEDED -- re-review required 2026-07-04; previously approved by team-lead, 2026-07-03
- the A4 / A5 split between taxonomy helpers and optional local lanes
  - status: SUPERSEDED -- re-review required 2026-07-04; previously approved by team-lead, 2026-07-03
- the future `just` lane taxonomy for upstream, ATM-owned, and integration
  lanes
  - status: SUPERSEDED -- re-review required 2026-07-04; previously approved by team-lead, 2026-07-03
- the planned dependency and glue surfaces already present on
  `feature/atm-graft-integration`
  - status: SUPERSEDED -- re-review required 2026-07-04; previously approved by team-lead, 2026-07-03

Implementation-start rule:

- this plan is not complete while the live branch model in GitHub and the doc
  content disagree
- this plan remains blocked until the corrected branch model and A3-A6
  registration gap are explicitly reviewed

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
- `integrate/phase-A` actually contains the proven baseline substrate
- the verified baseline is merged into `feature/atm-graft-integration`
- the sprint docs and live PR bases agree
- the unresolved A3-A6 zero-run registration gap is either fixed or
  independently explained with evidence
- the phase conclusion report includes the A1-A7 local and CI timing ledger
- the frozen `just` taxonomy still leaves a clean additive path for ATM-owned
  crates without broad upstream churn
