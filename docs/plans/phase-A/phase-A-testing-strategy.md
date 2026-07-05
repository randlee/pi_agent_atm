# Phase A - Testing Strategy

Date: 2026-07-04
Status: approved for lane design; current sprint-chain branch model recorded

## Purpose

Define the specific testing strategy that Phase A will implement so every
increment starts from something working, required PR CI stays under 10 minutes,
and local commands and CI share one source of truth.

This document governs lane design and rollout shape. Live branch targets, live
PR state, and the current CI-registration incident are tracked by
`docs/plans/phase-A/phase-A-just-ci-recovery.md` and must be re-verified from
git/GitHub evidence before implementation claims are treated as complete.

## Strategy Rules

1. `just` is the only public local operator surface.
2. Required PR CI is exactly one workflow: `baseline`.
3. Required PR CI runs `just ...` commands, not bespoke cargo command strings.
4. Every sprint preserves green `baseline` CI.
5. Heavyweight workflows do not run on ordinary PRs after Sprint A1 lands.
6. Compile checking and strict basic-unit coverage come before lint expansion
   and smoke expansion.
7. Lint in required PR CI covers only code we own.
8. Broad tests, fuzz, semver, benchmarks, and evidence refresh remain outside
   required PR CI.
9. Do not invent new top-level `just` commands for Phase A. Use the established
   `just help`, `just fmt`, `just lint`, `just test`, `just explain`, and
   `just suites` surfaces only.
10. Future ATM-owned lanes must be additive and must not silently redefine the
    semantics of the upstream baseline lanes established in Phase A.
11. Future ATM-owned integration in this repo should follow the actual
    `feature/atm-graft-integration` dependency model and bounded seam files
    rather than broad rewrites across upstream-owned files.
12. Every sprint PR must include a timing table for local runs and equivalent
    CI runs for that sprint's stage, and the phase conclusion must roll those
    timings up across all sprints.

## Fork And Upstream Audit Baseline

This repository is a fork of the public upstream
`Dicklesworthstone/pi_agent_rust`.

Phase A must treat the existing upstream workflow/test surface as a known risk
inventory, not as disposable noise. The current upstream ordinary-PR workflows
and what they prove are:

| Workflow | Current PR trigger shape | What it proves today | Phase A handling |
|---|---|---|---|
| `ci.yml` | all PRs | cross-OS compile/test/policy guard with DoD evidence checks | remove from ordinary PRs in A1, retain manual trigger |
| `conformance.yml` | all PRs | extension/runtime compatibility matrix, sibling-repo checkout health, Bun/npm legacy compatibility | remove from ordinary PRs in A1, retain manual and scheduled triggers |
| `fuzz.yml` | PRs targeting `main` | Linux fuzz smoke across selected targets | remove from ordinary PRs in A1, retain manual and scheduled triggers |
| `bench.yml` | all PRs | benchmark execution surface kept outside required gating | remove from ordinary PRs in A1, retain manual trigger |
| `semver.yml` | path-filtered PRs touching Rust/API surfaces | public API SemVer compatibility | remove from ordinary PRs in A1, retain manual trigger |
| `model-catalog-drift.yml` | path-filtered PRs touching generator/catalog inputs | Node-based catalog drift detection, advisory today | remove from ordinary PRs in A1, retain manual and scheduled triggers |

Key upstream-specific unknowns that must stay visible throughout Phase A:

- `conformance.yml` depends on sibling repositories (`asupersync`,
  `rich_rust`, `charmed_rust`, `sqlmodel_rust`) and Bun/npm installation.
- `ci.yml` is the only current cross-OS PR guard.
- `semver.yml` and `model-catalog-drift.yml` are path-filtered specialty gates,
  not generic test lanes.
- the suite taxonomy and logging/evidence contract live upstream in
  `docs/testing-policy.md` and `tests/suite_classification.toml`; Phase A may
  narrow fast gating, but it may not redefine those upstream contracts casually.

Mandatory A1 precondition:

- before ordinary-PR triggers are removed, this strategy document must already
  describe every currently PR-triggered workflow, why it is leaving the
  required gate, and what trigger path remains for it afterward

Trigger-file edits are required instead of branch-protection-only narrowing
because branch protection changes which checks block merges, but it does not
stop heavyweight `pull_request` workflows from still registering and running on
ordinary PRs.

## Evidence Reports

Supporting evidence for this strategy lives in:

- `reports/pi-agent-rust/local-test-surface-review-2026-07-03.md`
- `reports/pi-agent-rust/upstream-testing-contract-review-2026-07-03.md`
- `reports/pi-agent-rust/just-layering-and-atm-integration-strategy-2026-07-03.md`

## Steady-State Required PR Baseline

Steady-state `baseline` contents from Sprint A3 onward:

1. `just fmt check`
2. `just test compile`
3. `just test unit-basic`
4. `just lint clippy-bins`
5. `just lint clippy-lib`
6. `just test baseline`

Hard budget:

- total wall clock under 10 minutes

Per-step budget targets:

- `just fmt check`: under 30 seconds
- `just test compile`: under 90 seconds
- `just test unit-basic`: under 120 seconds
- `just lint clippy-bins`: under 30 seconds
- `just lint clippy-lib`: under 3 minutes
- `just test baseline`: under 3 minutes

These are budget allocations, not historical facts. Sprint validation must
measure and refresh them as each step is added.

## Incremental Rollout By Sprint

Required PR CI contents per sprint:

| Sprint | Required `baseline` contents |
|---|---|
| A1 | `just help`, `just fmt check`, `just test compile`, `just test unit-basic` |
| A2 | A1 + `just lint clippy-bins`, `just lint clippy-lib` |
| A3 | A2 + `just test baseline` |
| A4 | same as A3 |
| A5 | same as A3 |
| A6 | same as A3 |
| A7 | same as A3 on merge PRs |

This table is the controlling rollout rule. If a sprint would require more
than the listed contents, the plan is being violated.

Important interpretation:

- Sprint A1 intentionally starts with a small green gate.
- That green gate is only acceptable because the displaced upstream PR
  workflows remain available by explicit non-PR triggers and are documented in
  this strategy.
- The small gate is still required to prove compile health and strict
  basic-unit health first.
- A1 is a gate-reduction sprint, not a claim that the fork's broader testing
  unknowns have been solved.

## Timing Capture Contract

Each sprint PR must record, at minimum:

- local wall-clock timing for every command added or re-validated in that
  sprint
- CI step timing for the equivalent `baseline` workflow steps
- total `baseline` workflow wall time for that sprint stage

When a sprint adds local-only commands without putting them into required PR CI:

- the PR must still refresh the unchanged baseline CI timing table for that
  sprint
- local-only commands must be timed locally and marked `no ci equivalent by
  design`

Rollup ownership:

- A6 must assemble an A1-A6 timing ledger in the review pack
- A7 must publish the final A1-A7 timing ledger at phase conclusion

## Source Of Truth Policy

Target end state:

- `justfile` is the command surface
- `.just/lint_catalog.py` defines lint lanes
- `.just/test_catalog.py` defines test lanes
- `.just/explain.py` explains lane semantics
- `.just/show_suites.py` reports suite taxonomy from
  `tests/suite_classification.toml`
- the required `baseline` workflow invokes only `just ...` commands

One lane, one owner:

- format lane:
  - owner: `justfile` + `.just/run_fmt.py`
- lint lane:
  - owner: `.just/lint_catalog.py`
- test lane:
  - owner: `.just/test_catalog.py`

## Just Layering Framework For ATM Additions

Phase A needs a `just` design that stays useful after ATM-owned crates begin
landing. The stable top-level operator surface remains:

- `just help`
- `just fmt`
- `just lint`
- `just test`
- `just explain`
- `just suites`

Growth happens through lane catalogs, not new top-level commands.

Future lane families:

- upstream baseline lanes:
  - preserve the audited fork-regression contract
  - current examples: `compile`, `unit-basic`, `baseline`, `clippy-bins`,
    `clippy-lib`
- ATM-owned lanes:
  - cover new ATM crates or modules we own
  - should use explicit lane ids such as `atm-*`
- seam or integration lanes:
  - cover the boundary between upstream fork code and ATM-owned additions
  - should use explicit lane ids such as `integration-*`

Promotion rule:

- upstream baseline lanes are stable once Phase A freezes them
- new ATM-owned or integration lanes start as local/manual lanes
- they move into required PR CI only after timing evidence and team-lead review
- no ATM-owned lane may replace the upstream baseline requirement

Recommended catalog metadata for future hardening:

- `origin`: `upstream`, `atm`, or `integration`
- `owner`: owning crate or module
- `blocking`: `required`, `local`, `manual`, or `scheduled`
- `paths`: primary source paths the lane protects
- `promotion_rule`: evidence required before the lane can become blocking

`just explain` should eventually print this metadata so operators can tell
whether a lane protects upstream parity, ATM-owned code, or the seam between
them.

## Repository Layering Framework For ATM Additions

Current repo reality:

- the fork is still a single root package in `Cargo.toml`
- there is no active workspace-member layout yet
- the planned ATM integration surface already exists on
  `feature/atm-graft-integration` as root-package dependency wiring to
  `atm-core` crates plus a local vendor shim

Planning target for minimum upstream disruption:

- keep the existing root package as the upstream fork boundary through Phase A
- use `feature/atm-graft-integration` as the concrete reference for ATM
  layering decisions during Phase A
- prefer explicit root `Cargo.toml` dependency edges to `atm-core` crates such
  as `atm-graft` and `atm_core`, plus narrowly scoped vendor shims when needed
- keep repo-local glue bounded to the small integration surfaces that wire
  those dependencies into the upstream package
- keep cross-seam tests out of `unit-basic` and place them in explicit
  integration lanes under `tests/atm_*` or `tests/integration_*`

Required regression rule once ATM-owned crates exist:

1. every PR still runs the upstream required baseline
2. PRs touching the ATM dependency wiring or vendor shim surfaces run the
   relevant ATM-owned lanes as well
3. PRs touching the seam between root-package upstream code and ATM-owned
   dependencies run the relevant integration lanes as well

This is how the project verifies there is no regression from the upstream fork
while still allowing additive ATM-specific code growth.

## Compile And Basic-Unit Policy

Phase A must distinguish three different ideas that the repo currently blurs:

- inline Rust unit tests under `src/**`
- the broad deterministic bucket currently called `[suite.unit]`
- the strict early required gate Phase A needs first

Required rule:

- `unit-basic` is an explicit allowlist lane
- `unit-basic` must not blindly expand to all of `[suite.unit]`
- `compile` is an explicit lane that runs `cargo check --all-targets`

Required `unit-basic` starting point:

1. Audited inline Rust unit tests only, executed from reviewed module prefixes
   rather than a blind `cargo test --all-targets --lib` sweep
2. Exact module-path collision reconciliation whenever cargo's substring filter
   would otherwise drag non-audited tests into a lane
3. Small curated deterministic add-on targets:
   - `capability_policy_model`
   - `policy_profile_hardening`
   - `extension_flag_passthrough`
   - `model_serialization`
   - `redaction_test`
   - `extension_scoring_ope`

Required reconciliation rule:

- PR evidence must report the audited inline count separately from explicit
  add-on target counts so reviewers can verify what the lane actually ran

Explicit early exclusions from `unit-basic`:

- process-launching tests
- fixture/VCR inventory audits
- benchmark/perf harness tests
- docs/script audit tests
- artifact/regeneration audits
- subsystem stress or endurance tests

Named current examples that must stay out of `unit-basic` until separately
reclassified or split:

- `bench_schema`
- `perf_regression`
- `franken_node_compat_harness`
- `qa_docs_policy_validation`
- `rch_artifact_sync_preflight`
- `vcr_parity_validation`
- `provider_closure_truth_table`
- `mock_spec_schema`
- `e2e_replay_bundle_validation`

## Required PR Exclusions

These do not belong in required PR CI:

- `ci.yml`
- `fuzz.yml`
- `bench.yml`
- `semver.yml`
- conformance sweeps
- evidence refresh
- release or publish workflows

After Sprint A1, these workflows may remain as:

- `workflow_dispatch`
- `schedule`

They must not run on ordinary feature PRs.

Workflow classification target after Sprint A1:

| Workflow | Ordinary PRs | Allowed remaining triggers |
|---|---|---|
| `baseline.yml` | yes | `pull_request`, optionally protected-branch `push` |
| `ci.yml` | no | `workflow_dispatch` |
| `conformance.yml` | no | `workflow_dispatch`, `schedule` |
| `fuzz.yml` | no | `workflow_dispatch`, `schedule` |
| `bench.yml` | no | `workflow_dispatch` |
| `semver.yml` | no | `workflow_dispatch` |
| `model-catalog-drift.yml` | no | `workflow_dispatch`, `schedule` |
| `weekly-certification-verdict.yml` | no | `workflow_dispatch`, `schedule` |
| `weekly-evidence-refresh.yml` | no | `workflow_dispatch`, `schedule` |
| `publish.yml` | no | release-only trigger as defined in workflow |
| `release.yml` | no | release-only trigger as defined in workflow |

Protected-branch `push` triggers for heavyweight workflows are out of scope for
Phase A unless team-lead explicitly revises this strategy later.

Sprint A1 validation must prove that every displaced workflow still has a real
manual or scheduled execution path after the trigger edits land.

## Upstream Test Contracts That Phase A Must Respect

Phase A does not get to invent a new definition of "tests" for this fork.
These upstream contracts remain authoritative while Phase A narrows ordinary PR
gating:

- suite taxonomy and suite membership:
  - `docs/testing-policy.md`
  - `tests/suite_classification.toml`
- extension conformance/replay infrastructure:
  - `.github/workflows/conformance.yml`
  - `tests/ext_conformance/**`
- no-mock and evidence-policy guards:
  - `.github/workflows/ci.yml`
- specialty API/catalog verification:
  - `.github/workflows/semver.yml`
  - `.github/workflows/model-catalog-drift.yml`

Phase A is a required-gate reshaping effort. It is not an authorization to
delete or semantically weaken those upstream contracts without separate review.

## Lint Policy

Required PR CI lint rules:

- lint only local code surfaces
- do not lint third-party dependencies
- do not run `clippy --tests` in required PR CI
- do not run `clippy --benches` in required PR CI
- do not run `clippy --examples` in required PR CI

Approved required lint lanes:

- `just lint clippy-bins`
- `just lint clippy-lib`

Local-only optional lint lanes:

- `just lint all-local`
- `just lint clippy-tests`
- `just lint clippy-benches`
- `just lint clippy-examples`

## Test Policy

Required PR CI test rule:

- A1 starts with:
  - `just test compile`
  - `just test unit-basic`
- A3 later adds:
  - `just test baseline`

It must not include:

- broad `cargo test`
- full `[suite.unit]`
- full `suite.vcr`
- E2E sweeps
- fuzz
- semver
- benchmarks
- conformance matrices

Local-only optional test lanes may include:

- `just test unit`
- `just test integration`
- `just test all`
- `just test vcr`
- `just test e2e`

These remain outside required PR CI unless separately re-approved with timing
evidence.

## Reuse Policy

Phase A should prefer these reuse sources before inventing new implementation:

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

Phase A should not invent new top-level commands to avoid confusion around the
established operator surface. Narrow helper scripts are allowed only when they
remain behind `just help`, `just fmt`, `just lint`, `just test`, `just explain`,
or `just suites`.

## Failure Reporting Rules

Every `just` lane and required CI step should print:

- failing lane name
- exact underlying command
- source-of-truth file
- one next action
- non-zero exit code

Minimum example:

- `lane=baseline.lint.clippy-lib`
- `command=cargo clippy --no-deps --lib -- -D warnings`
- `ssot=.just/lint_catalog.py`
- `next=fix local lib warnings or move non-local scope out of the lane`

## Retained Evidence

Observed local macOS timings from `sprint-a-1-establish-minimal-baseline-gate`
on 2026-07-04:

| Command | Result | Observed wall time |
|---|---|---:|
| `just help` | pass | `0.06s` |
| `just fmt check` | pass | `13.63s` |
| `just test compile` | pass | `1.41s` |
| `just test unit-basic` | pass | `37.50s` |

Observed GitHub Actions timings from baseline run 28722267950 for head SHA 869928bf3a1623d8a106d763dd75fb1ce6231142 on 2026-07-04:

| Workflow / Step | Result | Approximate wall time |
|---|---|---:|
| baseline total | success | ~6m23s |
| Just help | success | <1s |
| Format gate | success | 17s |
| Compile gate | success | 1m52s |
| Basic unit gate | success | 3m15s |

## Merge-Forward Record

merge-forwarded from integrate/phase-A base a99911f0, confirmed current as of this commit.

`just test unit-basic` currently reconciles as:

- 1,797 audited inline tests
- 244 explicit add-on target tests
- 2,041 total executed tests in the lane
- 15 substring-collision exclusions under `session::tests` for
  `interactive::ext_session::*`

## Team-Lead Review Checklist

Team-lead approval should explicitly confirm:

- the upstream ordinary-PR workflow inventory and post-A1 trigger plan
- the `compile` lane definition
- the `unit-basic` allowlist and exclusion list
- the steady-state `baseline` command list
- the per-sprint rollout table
- the decision to remove heavyweight workflows from ordinary PRs in Sprint A1
- the rule that required PR CI stays under 10 minutes in every sprint
- the SSOT owner files for lint and test lanes
- the list of local-only and manual-only lanes
- the rule that Phase A does not invent new top-level `just` commands
- the future lane taxonomy for `upstream`, `atm`, and `integration`
- the intended repository layering surfaces for ATM-owned crates and glue code

### Team-Lead Approval Record

Reviewer: `team-lead`
Review date: `2026-07-04`
Approval state: the `2026-07-03` lane-strategy approval was superseded by the
live sprint-chain evidence review on `2026-07-04`. This document now records
the current branch model and lane strategy. Sprint implementation claims still
require per-PR git/GitHub evidence.

Checklist record:

- the upstream ordinary-PR workflow inventory and post-A1 trigger plan
  - status: current on 2026-07-04; sprint PR evidence still required
- the `compile` lane definition
  - status: current on 2026-07-04; sprint PR evidence still required
- the `unit-basic` allowlist and exclusion list
  - status: current on 2026-07-04; sprint PR evidence still required
- the steady-state `baseline` command list
  - status: current on 2026-07-04; sprint PR evidence still required
- the per-sprint rollout table
  - status: current on 2026-07-04; sprint PR evidence still required
- the decision to remove heavyweight workflows from ordinary PRs in Sprint A1
  - status: current on 2026-07-04; sprint PR evidence still required
- the rule that required PR CI stays under 10 minutes in every sprint
  - status: current on 2026-07-04; sprint PR evidence still required
- the SSOT owner files for lint and test lanes
  - status: current on 2026-07-04; sprint PR evidence still required
- the list of local-only and manual-only lanes
  - status: current on 2026-07-04; sprint PR evidence still required
- the rule that Phase A does not invent new top-level `just` commands
  - status: current on 2026-07-04; sprint PR evidence still required
- the future lane taxonomy for `upstream`, `atm`, and `integration`
  - status: current on 2026-07-04; sprint PR evidence still required
- the intended repository layering surfaces for ATM-owned crates and glue code
  - status: current on 2026-07-04; sprint PR evidence still required

## Exit Criteria

The strategy is implemented when:

- required PR CI is exactly one workflow named `baseline`
- `baseline` is the only required branch-protection status check for ordinary
  PRs once the Sprint A1 operational branch-protection update lands
- `baseline` stays under 10 minutes
- CI and local execution share the same lane definitions
- heavyweight workflows no longer run on ordinary PRs
- timing data is refreshed after each baseline expansion sprint
