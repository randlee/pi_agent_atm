# Phase A - Testing Strategy

Date: 2026-07-05
Status: draft attempt 3; strategy consolidation in progress

## Purpose

Define the specific testing strategy that Phase A will implement so:

- the available test surfaces are easy to understand
- required PR CI stays within a sane budget instead of drifting toward 3-hour CI
- local commands and CI share one source of truth
- ATM-owned code can be added without regressing upstream fork behavior
- final Phase A success means a measured 10-20 minute parallel multi-platform
  required gate with clear coverage boundaries, not merely one fast Linux check

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
13. Runtime budget constrains which lanes are required; it does not justify
    inventing brittle or difficult-to-maintain test selection logic.
14. A small smoke list is acceptable; a large hand-maintained list of specific
    tests is not an acceptable side effect of chasing the 10m goal.
15. A Linux-only fast check is an intermediate milestone, not the Phase A end
    state.
16. Phase A closes only when the merged required gate has measured Linux,
    macOS, and Windows timings and those timings are recorded in the phase
    conclusion evidence.

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

## Testing Framework

This strategy uses four testing tiers. The point is to keep the framework easy
to reason about rather than turning the 10m goal into a maze of custom test
calls.

| Tier | Purpose | Trigger | Typical scope | Budget rule |
|---|---|---|---|---|
| `build-safety` | prove the repo still formats, compiles, and lints cleanly | every PR | format, compile, local-code lint | always required |
| `upstream-fast` | prove we did not break the fork's core upstream behavior | every PR | deterministic basic-unit lane + smoke lane | always required |
| `upstream-broad` | prove broader upstream behavior that is too expensive for every PR | risky PRs, pre-merge to important branches, or nightly | broader integration, VCR, cross-platform full CI | not ordinary-PR required by default |
| `specialty-evidence` | deep confidence beyond ordinary gating | manual or schedule | conformance, fuzz, benchmarks, semver, drift | never the default PR gate |

This is the framework Phase A should communicate to operators. The strategy is
not "optimize for a green Linux check at any cost." The strategy is:

1. keep one easy-to-understand required baseline
2. measure that baseline honestly
3. keep broader upstream contracts available outside the narrow required gate
4. layer ATM-owned checks additively rather than redefining the upstream gate

## Current Test Surfaces

At a high level, the repo already contains these test surfaces:

- compile/build checks
- lint checks
- deterministic fast tests
- broader integration / VCR / conformance tests
- E2E / workflow tests
- specialty evidence jobs:
  - extension conformance
  - fuzz
  - benchmarks
  - semver
  - model-catalog drift

Operators should understand the repo through those surfaces first. They should
not need to memorize hundreds of individual test files to understand the
strategy.

## Planned Phase A Operator Surface

The easiest way to understand Phase A is by the planned `just` lanes and what
they mean.

| Command | Tier | What it proves | What it intentionally excludes | Normal use |
|---|---|---|---|---|
| `just help` | metadata | the operator surface is discoverable and cheap | any compile or test proof | every local session and first CI step |
| `just explain <domain> <lane>` | metadata | lane semantics, ownership, blocking level, and source of truth are inspectable | any compile or test proof | pre-change review and PR documentation |
| `just suites` | metadata | upstream suite taxonomy is readable from one place | any compile or test proof | audit and classification review |
| `just fmt check` | build-safety | formatting is clean | compile and test behavior | every PR |
| `just test compile` | build-safety | the repo still compiles across all targets | runtime behavior and test semantics | every PR |
| `just test unit-basic` | upstream-fast | the narrow deterministic upstream core still works | broad `[suite.unit]`, VCR, E2E, binary-launching, audit, perf, and benchmark tests | every PR |
| `just lint clippy-bins` | build-safety | local binary-target lint health | tests, benches, examples, dependency lint | every PR after A2 |
| `just lint clippy-lib` | build-safety | local library-target lint health | tests, benches, examples, dependency lint | every PR after A2 |
| `just test baseline` | upstream-fast | the tiny required smoke subset still works | full unit, full integration, VCR, E2E, fuzz, bench, semver, drift | every PR after A3 |
| `just test unit` | upstream-broad local lane | broader deterministic unit inventory | VCR, E2E, live-provider coverage | local/manual only in Phase A |
| `just test integration` | upstream-broad local lane | explicit seam and broader integration checks | live E2E and heavyweight specialty workflows | local/manual only in Phase A |
| `just test all` | upstream-broad local lane | convenience aggregation for local confidence | specialty scheduled/manual workflows | local/manual only in Phase A |
| `just lint all-local` | upstream-broad local lane | optional broader local lint surface | dependency lint and scheduled specialty checks | local/manual only in Phase A |

This table is intentionally simple. The goal is to let an operator answer
"what am I proving?" without reverse-engineering the workflow YAML.

## Recommended Regression Framework For ATM Work

Once Phase A has landed, regression policy should be:

1. every PR runs the upstream required baseline
   - `just fmt check`
   - `just test compile`
   - `just test unit-basic`
   - required lint lanes
   - `just test baseline`
2. PRs touching ATM-owned crates run ATM-owned lanes in addition to the
   upstream required baseline
3. PRs touching the seam between upstream fork code and ATM-owned additions run
   explicit integration lanes in addition to the upstream required baseline
4. broad upstream confidence surfaces stay available as local, manual, nightly,
   or pre-merge lanes rather than being silently discarded

The safety model is additive:

- upstream baseline proves "we did not break the fork"
- ATM-owned lanes prove "we did not break our additions"
- integration lanes prove "we did not break the seam between them"

## Current Quantified Baseline Table

This is the single table Phase A should use for review. It mixes scope, timing,
and coverage in one place instead of scattering them across PR bodies.

Current measured state:

- lane-specific production-code coverage was measured for the final required
  test lanes only:
  - `just test unit-basic`
  - `just test baseline`
- coverage numbers below are **not** repo-wide historical numbers; they are the
  measured result for the current narrow required test lanes
- compile and lint rows do not execute tests, so coverage is `n/a`

| Lane | Purpose | Exact command | Protects | Required | Local time | CI Linux | CI macOS | CI Windows | Coverage |
|---|---|---|---|---|---:|---:|---:|---:|---|
| `help` | operator surface check | `just help` | operator ergonomics, command discovery | yes | `0.09s` after lazy-load fix | previously inflated to `4m29s` on merged target branch due to import-time cargo bug | not yet measured on final branch | not yet measured on final branch | `n/a` |
| `fmt check` | formatting guard | `just fmt check` | formatting correctness | yes | about `13s` in retained measurements | `16s` on merged target Linux run | not yet measured on final branch | not yet measured on final branch | `n/a` |
| `compile` | compile health | `just test compile` | build regressions across all targets | yes | about `159s-293s` in retained measurements depending on branch/cache state | `3m29s` on merged target Linux run | not yet measured on final branch | not yet measured on final branch | `n/a` |
| `unit-basic` | deterministic core upstream regression gate | `just test unit-basic` | core upstream logic without broad integration surfaces | yes | `40.26s` warm instrumented rerun; non-instrumented retained runs about `94s-104s` | `1m23s` on merged target Linux run | not yet measured on final branch | not yet measured on final branch | part of combined required test-lane coverage |
| `clippy-bins` | local-code binary lint | `just lint clippy-bins` | binary-target lint regressions | yes | about `57s-97s` in retained measurements | `1m51s` on merged target Linux run | not yet measured on final branch | not yet measured on final branch | `n/a` |
| `clippy-lib` | local-code library lint | `just lint clippy-lib` | library-target lint regressions | yes | about `1s` in retained measurements | `<1s` on merged target Linux run | not yet measured on final branch | not yet measured on final branch | `n/a` |
| `baseline` | small upstream smoke lane | `just test baseline` | core model/config/session/error/compaction/security smoke | yes | `12.88s` warm instrumented run; non-instrumented retained runs about `14s-16s` | `13s` on merged target Linux run | not yet measured on final branch | not yet measured on final branch | part of combined required test-lane coverage |
| `required baseline total` | final narrow PR gate | `baseline.yml` step sequence | build-safety + upstream-fast | yes | not a single local command | `12m33s` on merged target Linux run before `just help` fix; projected about `8m04s` after removing bogus `4m29s` help cost | not yet measured on final branch | not yet measured on final branch | line `22.90%`, function `23.39%`, region `21.73%` across the required test lanes only |

Interpretation:

- the current required baseline is a narrow smoke/regression gate, not a
  high-coverage proof gate
- the current required **test** lanes cover about `22.90%` of production lines
  and about `23.39%` of production functions
- this is far below the historical repo-wide coverage baseline and should be
  described honestly
- the merged-target Linux run still needs re-measurement after the `just help`
  lazy-load fix
- macOS and Windows final-branch timings are still missing

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
- The Phase A endpoint is still a measured multi-platform gate; the narrow
  Linux baseline is only the first controlled step toward that endpoint.

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

For final closure, the same table shape must be refreshed on the merged target
branch with:

- Linux timing
- macOS timing
- Windows timing
- exact run IDs and SHAs
- the final parallel wall-clock figure for the required multi-platform gate

## Source Of Truth Policy

Target end state:

- `justfile` is the command surface
- `.just/lint_catalog.py` defines lint lanes
- `.just/test_catalog.py` defines test lanes
- `.just/explain.py` explains lane semantics
- `.just/show_suites.py` reports suite taxonomy from
  `tests/suite_classification.toml`
- the required `baseline` workflow invokes only `just ...` commands

Important guardrail:

- `just help` and other metadata commands must stay cheap
- they must never trigger cargo compilation or test enumeration during import
- if a lane requires expensive discovery work, that work must happen only when
  the lane is executed, not when help or explanation is rendered

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

`just explain` should print this metadata so operators can tell whether a lane
protects upstream parity, ATM-owned code, or the seam between them.

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

- `unit-basic` is currently an explicit allowlist lane because upstream
  `[suite.unit]` is too broad for an early deterministic gate
- `unit-basic` must not blindly expand to all of `[suite.unit]`
- `compile` is an explicit lane that runs `cargo check --all-targets`

Maintenance rule:

- the long-term strategy is stable category-driven lane semantics plus a small
  smoke list
- the strategy is **not** "keep growing a giant brittle list of specific test
  names forever"

Required `unit-basic` starting point:

1. `cargo test --all-targets --lib`
2. Small curated deterministic add-on targets:
   - `capability_policy_model`
   - `policy_profile_hardening`
   - `extension_flag_passthrough`
   - `model_serialization`
   - `redaction_test`
   - `extension_scoring_ope`

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

Observed local macOS timings from `feature/just-integration`:

| Command | Result | Observed wall time |
|---|---|---:|
| `just help` | pass | `<1s` |
| `just fmt check` | pass | `12.46s` |
| `just lint clippy-lib` | pass | `50.66s` |
| `just lint clippy-bins` | pass | `2.87s` |
| `just test baseline` | pass | `10.59s` |
| `just lint clippy-tests` | incomplete | `>3m38s` before manual stop |
| `just test unit` | incomplete | `>120s` before timeout |
| `just test integration` | incomplete | `>120s` before timeout |

Observed GitHub Actions timings from 2026-07-02:

| Workflow | Result | Approximate wall time |
|---|---|---:|
| `baseline` | success | `~7m03s` |
| `Extension Conformance` | success | `~6m25s` |
| `Fuzz CI` | success | `~42m59s` |
| old monolithic `ci` | cancelled | `~49m25s` before cancellation |

Measured lane-specific coverage for the final required test lanes on
2026-07-05:

| Scope | Line coverage | Function coverage | Region coverage |
|---|---:|---:|---:|
| `just test unit-basic` + `just test baseline` | `22.90%` | `23.39%` | `21.73%` |

This is the honest current coverage story for the required test lanes. It is a
narrow upstream-regression gate, not a broad proof of repo correctness.

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
Review date: pending replay-plan review
Approval state: prior approval history is intentionally not reused. This
strategy now requires a fresh review because the earlier execution mixed stale
branch assumptions with incomplete CI evidence.

Checklist record:

- the upstream ordinary-PR workflow inventory and post-A1 trigger plan
  - status: PENDING fresh review
- the `compile` lane definition
  - status: PENDING fresh review
- the `unit-basic` allowlist and exclusion list
  - status: PENDING fresh review
- the steady-state `baseline` command list
  - status: PENDING fresh review
- the per-sprint rollout table
  - status: PENDING fresh review
- the decision to remove heavyweight workflows from ordinary PRs in Sprint A1
  - status: PENDING fresh review
- the staged budget rule during rollout and the final multi-platform timing goal
  - status: PENDING fresh review
- the SSOT owner files for lint and test lanes
  - status: PENDING fresh review
- the list of local-only and manual-only lanes
  - status: PENDING fresh review
- the rule that Phase A does not invent new top-level `just` commands
  - status: PENDING fresh review
- the future lane taxonomy for `upstream`, `atm`, and `integration`
  - status: PENDING fresh review
- the intended repository layering surfaces for ATM-owned crates and glue code
  - status: PENDING fresh review

## Exit Criteria

The strategy is implemented when:

- required PR CI is exactly one workflow named `baseline`
- `baseline` is the only required branch-protection status check for ordinary
  PRs once the Sprint A1 operational branch-protection update lands
- the rollout-stage required baseline stays within its documented budget at
  every sprint
- the final merged required gate has recorded Linux, macOS, and Windows
  timings plus the final parallel wall-clock figure
- CI and local execution share the same lane definitions
- heavyweight workflows no longer run on ordinary PRs
- timing data is refreshed after each baseline expansion sprint
