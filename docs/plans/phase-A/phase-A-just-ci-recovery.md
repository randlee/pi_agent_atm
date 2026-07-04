# Phase A - Minimal Just / CI Recovery

Date: 2026-07-03 (branch-model and CI-gap remediation section added 2026-07-04)
Status: open -- the 2026-07-04 CI-gap remediation below is unresolved; do not
treat this doc as fully closed until integrate/phase-A shows real, verified
green CI (see remediation steps)
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

## Branch And Worktree Model

> **2026-07-04 correction**: the branch model below (direct-to-`develop`
> sprint branches, no integration branch) was never actually followed in
> practice -- Sprints A1-A7 were all built stacked on `integrate/phase-A`,
> culminating in a merge PR into `feature/atm-graft-integration`. Team-lead
> and randlee reconfirmed on 2026-07-04 that an integration branch is the
> correct model going forward: it consolidates small changes one at a time
> and lets each be QA/CI-verified before anything lands on `develop`. This
> section is retained for historical record of the original (superseded)
> intent; see "Integration Branch Model (reconfirmed 2026-07-04)" below for
> the model actually in force. **This section (lines below, through the end
> of "Execution model") is superseded and must not be followed** -- it is
> retained only for historical record.

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

## Integration Branch Model (reconfirmed 2026-07-04)

`integrate/phase-A` is the consolidation branch for all Phase A sprint work.
Sprint branches target `integrate/phase-A` (directly or via the existing
stacked chain); `integrate/phase-A` only advances toward `develop` once its
own CI is real and green. Rationale: an integration branch lets small changes
be approved and consolidated one at a time, and no unverified code should land
on `develop` directly.

Known gap being remediated as of 2026-07-04: `integrate/phase-A` (and
`develop`) lack the `justfile` / `.just/**` operator surface that
`.github/workflows/baseline.yml` depends on for 6 of its 7 steps -- confirmed
absent on both branches via `git ls-tree`. GitHub's own Actions API
(`gh api repos/randlee/pi_agent_atm/actions/runs?branch=<branch>`) also shows
`total_count: 0` for Phase A sprint PRs A3/A4/A5 (#13/#14/#15) at their head
SHAs -- not merely a missing-tool failure, but no run recorded by GitHub at
all for those PRs. Remediation:

1. land `justfile`, `.just/**`, and `.github/workflows/baseline.yml` together
   onto `integrate/phase-A` in one PR, so the integration branch is fully
   self-sufficient (this supersedes attempting to register `baseline.yml`
   alone, which is necessary but not sufficient -- see the closed PR #19,
   which registered `baseline.yml` alone on `develop` and failed QA-1 for
   exactly this reason). Before treating `integrate/phase-A` as
   self-sufficient, verify via `gh pr checks` that a real workflow run
   triggers and completes on that bundling PR's own head SHA -- registration
   alone is not proof, since A3-A5's zero-run symptom may be independent of
   the missing `justfile` and is not yet fully explained
2. after that lands, verify -- per sprint PR, via `gh pr checks` against a
   freshly pushed commit -- that a real workflow run starts and completes;
   do not assume registration alone fixed the silent-no-run PRs
3. add `baseline` as a required branch-protection status check on
   `integrate/phase-A` -- a green run is not the same guarantee as a required
   check; branch protection must be updated explicitly, it will not follow
   automatically from the workflow existing
4. only after the full stacked chain shows real, green, individually-verified
   CI, and `baseline` is a required status check on `integrate/phase-A`, does
   `integrate/phase-A` proceed to its own gated PR into `develop`, which must
   itself show green CI before merge

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
