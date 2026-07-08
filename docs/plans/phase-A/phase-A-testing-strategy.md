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
10. Every category retained in this strategy must map to a named `just` lane,
    even when that category is not part of ordinary PR CI.
11. Phase A lane ownership must stay explicit across four blocking classes:
    `required`, `long-ci`, `local`, and `manual/scheduled`.
12. `long-ci` is a deliberate longer-timeout CI set for broad but still useful
    categories; it is not the ordinary PR baseline.
13. Future ATM-owned lanes must be additive and must not silently redefine the
    semantics of the upstream baseline lanes established in Phase A.
14. Future ATM-owned integration in this repo should follow the actual
    `feature/atm-graft-integration` dependency model and bounded seam files
    rather than broad rewrites across upstream-owned files.
15. Every sprint PR must include a timing table for local runs and equivalent
    CI runs for that sprint's stage, and the phase conclusion must roll those
    timings up across all sprints.
16. Runtime budget constrains which lanes are required; it does not justify
    inventing brittle or difficult-to-maintain test selection logic.
17. A small smoke list is acceptable; a large hand-maintained list of specific
    tests is not an acceptable side effect of chasing the 10m goal.
18. A Linux-only fast check is an intermediate milestone, not the Phase A end
    state.
19. Phase A closes only when the merged required gate has measured Linux,
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
- `docs/plans/phase-A/phase-A-current-evidence-report.md`
- `docs/plans/phase-A/phase-A-test-lane-report-template.md`

## Testing Framework

This strategy uses five testing tiers. The point is to keep the framework easy
to reason about rather than turning the 10m goal into a maze of custom test
calls.

| Tier | Purpose | Trigger | Typical scope | Budget rule |
|---|---|---|---|---|
| `build-safety` | prove the repo still formats, compiles, and lints cleanly | every PR | format, compile, local-code lint | always required |
| `upstream-fast` | prove we did not break the fork's core upstream behavior | every PR | deterministic basic-unit lane + smoke lane | always required |
| `long-ci` | prove the broad CI-friendly categories with a longer timeout than `baseline` | sprint closeout, risky PRs, pre-merge, or nightly | full unit, integration, parity, security, perf, bounded conformance | not ordinary-PR required by default |
| `upstream-broad-local` | keep every broad category runnable from `just` even when not worth routine CI time | local review and targeted debugging | the same categories as `long-ci` plus local-only variants | category-dependent |
| `specialty-evidence` | deep confidence beyond ordinary gating | manual or schedule | full E2E, fuzz, heavy conformance, benchmarks, semver, drift | never the default PR gate |

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

## Historical PR #1 Breakout To Preserve

The abandoned PR #1 attempt had a better category breakout than the current
collapsed surface. The fix is to keep that category clarity while changing only
the blocking policy.

Historical evidence anchors:

- `baseline` run `28736534784` on SHA
  `2bbd5d16f02c1e2613f31132852d04938ecb697d`
- broad `ci` run `28631117871` on SHA
  `211c4012384c9c1ba93e58f18f90f89611e01922`

The useful PR #1 broad categories were:

- `unit`
- `integration`
- `e2e`
- `extension`
- `parity`
- `security`
- `perf`

Phase A salvage should therefore do three things at once:

1. keep those categories visible as named `just` lanes
2. keep only the small baseline in ordinary PR CI
3. define a separate `long-ci` set for the broad categories that are still
   worth running in CI with a longer timeout

## Minimal Working Operator Model

The minimal model that unblocks engineering is:

- one always-on required gate:
  - `just help`
  - `just fmt check`
  - `just test compile`
  - `just test unit-basic`
  - `just lint clippy-bins`
  - `just lint clippy-lib`
  - `just test baseline`
- named `just` lanes for every broader retained category
- one bounded `just test long-ci` aggregate
- manual or scheduled handling for the categories that are known to run for
  hours or require heavy external prerequisites

This is the plan. The rest of the document exists only to make that model
auditable.

## Sprint Evidence Table Template

Every active Phase A sprint from A8 onward must update the same evidence table
shape in both the sprint PR notes and the strategy/review-pack docs.

Primary fill-in template:

- `docs/plans/phase-A/phase-A-test-lane-report-template.md`

Required columns:

| Category | Backing lane or workflow | Exact command or profile | Runs now on ordinary PRs | Can run in CI | Can run locally | Surface size | Local time | CI time | Coverage | Evidence status | Notes |
|---|---|---|---|---|---|---:|---:|---:|---|---|---|

Column rules:

- `Category`
  - stable human-readable category name, not an implementation nickname
- `Backing lane or workflow`
  - `just` lane, `verify` profile, or workflow name that actually runs it
- `Exact command or profile`
  - literal command or profile invocation
- `Runs now on ordinary PRs`
  - `yes` only if it is part of the current required PR gate
- `Can run in CI`
  - `yes`, `manual/scheduled only`, or `no`
- `Can run locally`
  - `yes`, `prereqs`, or `no`
- `Surface size`
  - file count, suite count, explicit target count, or `n/a`
- `Local time`
  - measured wall clock, capped observation, or conservative estimate
- `CI time`
  - measured job or step time, capped observation, or conservative estimate
- `Coverage`
  - `n/a`, measured coverage, or `A9 measurement required`
- `Evidence status`
  - `measured`, `estimated`, `capped observation`, or `missing`
- `Notes`
  - why the category is narrow, expensive, flaky, prerequisite-heavy, or not
    yet trustworthy

## Authoritative Test Category Matrix

This is the category list the plan should expose to operators. It answers the
question "what is run now versus what can be run?"

| Category | Backing lane or workflow | Exact command or profile | Runs now on ordinary PRs | Can run in CI | Can run locally | Surface size | Local time | CI time | Coverage | Evidence status | Notes |
|---|---|---|---|---|---|---:|---:|---:|---|---|---|
| `compile-check` | `just test compile` | `cargo check --all-targets` | yes | yes | yes | `n/a` | about `159s-293s` retained | `3m29s` Linux retained | `n/a` | measured | compile safety only, not a test pass signal |
| `unit-inline-core` | not currently first-class | `cargo test --all-targets --lib` | no | yes | yes | inline lib tests under `src/**` | A9 measure | A9 measure | A9 measure | missing | currently buried inside `unit-basic`; should be reported separately |
| `unit-app-logic` | not currently first-class | deterministic app-logic subset of `[suite.unit]` | no | yes (`long-ci`) | yes | `28` of `124` `[suite.unit]` files = `22.58%` | not yet measured separately | not yet measured separately | not yet measured separately | partial | intended to isolate model/config/session/provider/capability logic from broader infra and policy tests |
| `unit-infra-tooling` | not currently first-class | deterministic CLI/RPC/SDK/CI/helper subset of `[suite.unit]` | no | yes (`long-ci`) | yes | `23` of `124` `[suite.unit]` files = `18.55%` | not yet measured separately | not yet measured separately | not yet measured separately | partial | supporting infrastructure and tool behavior belongs here rather than being implied as product logic |
| `unit-security-policy` | not currently first-class | deterministic security/policy subset of `[suite.unit]` | no | yes (`long-ci`) | yes | `13` of `124` `[suite.unit]` files = `10.48%` | not yet measured separately | not yet measured separately | not yet measured separately | partial | budget, sandbox, scanner, and policy enforcement tests should be measured separately |
| `unit-perf-policy` | not currently first-class | deterministic perf-budget subset of `[suite.unit]` | no | yes (`long-ci`) | yes | `9` of `124` `[suite.unit]` files = `7.26%` | not yet measured separately | not yet measured separately | not yet measured separately | partial | perf budget tests are not the same thing as core logic unit tests |
| `unit-contract-parity` | not currently first-class | deterministic contract/parity subset of `[suite.unit]` | no | yes (`long-ci`) | yes | `51` of `124` `[suite.unit]` files = `41.13%` | not yet measured separately | not yet measured separately | not yet measured separately | partial | many `*_contract`, parity, and compatibility tests live in `suite.unit` today but are not best described as app-logic unit tests |
| `unit-curated-files` | not currently first-class | six explicit `cargo test --test ...` invocations | no | yes | yes | `6` files, `4.84%` of `[suite.unit]` file inventory | A9 measure | A9 measure | A9 measure | missing | currently buried inside `unit-basic`; naming should reflect that it is curated |
| `unit-curated-fast` | `just test unit-basic` | multiple inline-prefix cargo tests plus six explicit unit files | yes | yes | yes | `32` audited inline prefixes + `6` explicit test files + `80` exclusions in current audit | `40.26s` warm instrumented rerun; retained non-instrumented about `94s-104s` | `1m23s` Linux retained | current unit-only coverage not yet isolated | partial | this is the required fast gate; it overlaps `unit-inline-core` and a narrow curated slice of `[suite.unit]` and should not be treated as a natural category |
| `smoke-baseline` | `just test baseline` | `./scripts/smoke.sh --skip-lint --no-rch --only unit` | yes | yes | yes | `6` documented smoke targets | `12.88s` warm instrumented rerun; retained non-instrumented about `14s-16s` | `13s` Linux retained | combined required-lane coverage currently measured only with `unit-curated-fast` | partial | tiny smoke slice, not a broad unit/integration proof |
| `unit-full` | planned `just test unit-full` | `./scripts/e2e/run_all.sh --profile quick --skip-lint` | no | yes (`long-ci`) | yes | `[suite.unit]` = `124` files | `>120s` capped observation retained | `6m41s` execute-lane time on old `qa-shard (unit)` from run `28631117871` | A9 measure | partial | broad unit should be visible again as a named lane even though it is not ordinary-PR required |
| `integration-broad` | planned `just test integration` | `./scripts/e2e/run_all.sh --profile ci --skip-lint --skip-e2e` | no | yes (`long-ci`) | yes | broad non-E2E shard over `suite.unit` plus `suite.vcr` | no clean retained local timing | one shard completed in `8m01s`, the other was cancelled after about `5h59m` in run `28631117871` | `n/a` for Phase A today | capped observation | this is the category that most clearly needs splitting and better bounds before promotion |
| `vcr-fixture` | planned `just test vcr-fixture` | VCR-only playback lane to be split out of current integration broad run | no | yes (`long-ci`) | yes | `[suite.vcr]` = `138` files | no clean retained local timing | current retained evidence is only the mixed integration broad lane above | `n/a` for Phase A today | estimated | A10 should expose this as its own lane instead of leaving it buried inside integration |
| `e2e-ci-smoke` | planned `just test e2e-ci-smoke` | bounded CI E2E smoke profile | no | yes (`long-ci`) | prereqs | `1` default suite in profile ci today | no clean retained local timing | no isolated retained timing yet; measure after A10 makes it first-class | `n/a` | missing | acceptable `long-ci` candidate only if it stays bounded and isolated |
| `e2e-full` | planned `just test e2e-full` | `./scripts/e2e/run_all.sh --profile full` | no | manual/scheduled only | prereqs | `[suite.e2e]` = `39` files | estimate: long | two shards were cancelled after about `5h59m-6h00m` in run `28631117871` | `n/a` | capped observation | too unbounded for ordinary PR CI or early `long-ci` promotion |
| `extension-sharded` | planned `just test extension-sharded` | sharded `ext_conformance_generated` matrix | no | yes (`long-ci`) | prereqs | `4` old shards | no clean retained local timing | retained execute-lane times `3m50s`, `4m41s`, `4m46s`, `4m42s` on run `28631117871` | `n/a` | measured | good candidate for a bounded `long-ci` category once exposed through `just` |
| `parity` | planned `just test parity` | parity cargo-test bundle from old `qa-shard (parity)` | no | yes (`long-ci`) | yes | `5` explicit parity test targets in old CI | no clean retained local timing | `3m52s` execute-lane time on run `28631117871` | `n/a` | measured | category was understandable in PR #1 and should stay visible |
| `security` | planned `just test security` | security cargo-test bundle from old `qa-shard (security)` | no | yes (`long-ci`) | yes | `3` explicit security test targets in old CI | no clean retained local timing | `3m41s` execute-lane time on run `28631117871` | `n/a` | measured | bounded and readable, unlike the current collapsed surface |
| `perf-benchmark` | planned `just test perf-benchmark` | perf cargo-build plus perf cargo-test bundle from old `qa-shard (perf)` | no | yes (`long-ci`) | yes | `4` explicit perf test targets in old CI | no clean retained local timing | `5m57s` execute-lane time on run `28631117871` | `n/a` | measured | broader than ordinary baseline but still CI-tractable |
| `conformance-fast` | planned `just test conformance-fast` | bounded fast conformance profiles | no | yes (`long-ci`) | prereqs | fast profile variants | no retained local timing in Phase A | fast-negative job `4m26s`, fast-official run step `3m52s`, fast-generated run step `22m10s` on run `28631117865` | `n/a` | partial | keep fast variants exposed separately; generated matrix is already pushing beyond the target band |
| `fuzz` | `.github/workflows/fuzz.yml` | fuzz workflow | no | manual/scheduled only | prereqs | fuzz targets | estimate: long | `~42m59s` retained | `n/a` | partial | clearly outside ordinary PR gate |
| `benchmark-full` | planned `just test benchmark-full` and `.github/workflows/bench.yml` | `./scripts/perf/orchestrate.sh --profile full` | no | manual only | yes | benchmark registry | estimate: long | no clean retained Phase A timing | `n/a` | estimated | keep a separate heavy benchmark category apart from the bounded `perf-benchmark` lane |
| `semver` | planned `just test semver` and `.github/workflows/semver.yml` | semver workflow | no | yes (`long-ci`) | yes | path-filtered API surface | estimate: medium | `24s` semver-check step and `2m38s` total job on run `28631117866` | `n/a` | measured | API compatibility check, not behavior coverage |
| `model-catalog-drift` | planned `just test model-catalog-drift` and `.github/workflows/model-catalog-drift.yml` | drift workflow | no | manual/scheduled only | yes | path-filtered catalog surface | estimate: low-medium | `15s` retained from latest drift run on reverted head | `n/a` | partial | advisory drift detection, not runtime behavior coverage |

## Current Unit Category Breakdown

The current plan should stop pretending `unit-basic` is a natural category. It
is a gate, not a taxonomy.

Current overlap:

- `unit-basic` is a curated fast gate
- it overlaps `unit-inline-core`
- it also overlaps a tiny explicit subset of `[suite.unit]`
- `unit-full` is the broader aggregate over the deterministic quick-profile
  unit surface

That means `unit-basic` and `unit-full` are intentionally overlapping today.
The overlap exists for speed, not because those are clean categories.

| Unit category | Current meaning in repo terms | Current backing surface | Current timing evidence | Current coverage evidence | Maintenance risk |
|---|---|---|---:|---|---|
| `unit-basic` | required fast gate, not a taxonomy | curated inline prefixes plus `6` explicit test files | `1m23s` Linux retained | not yet isolated from smoke in current coverage evidence | high |
| `unit-inline-core` | inline `#[cfg(test)]` lib tests | audited inline prefix commands | A9 measure | A9 measure | medium |
| `unit-app-logic` | deterministic product logic tests | `28` audited files = `22.58%` of `[suite.unit]` | not yet measured separately | not yet measured separately | medium |
| `unit-infra-tooling` | deterministic CLI/RPC/SDK/CI/helper tests | `23` audited files = `18.55%` of `[suite.unit]` | not yet measured separately | not yet measured separately | medium |
| `unit-security-policy` | deterministic security and policy tests | `13` audited files = `10.48%` of `[suite.unit]` | not yet measured separately | not yet measured separately | medium |
| `unit-perf-policy` | deterministic perf-budget tests | `9` audited files = `7.26%` of `[suite.unit]` | not yet measured separately | not yet measured separately | medium |
| `unit-contract-parity` | deterministic contract/parity/compat tests | `51` audited files = `41.13%` of `[suite.unit]` | not yet measured separately | not yet measured separately | medium-high |
| `unit-curated-files` | explicit `tests/*.rs` subset inside the fast gate | `6` files from `[suite.unit]` = `4.84%` of listed unit files | A9 measure | A9 measure | high |
| `unit-full` | aggregate deterministic unit surface | full `[suite.unit]` = `124` files plus quick-profile inline coverage | `>120s` capped local observation retained | A9 measure | medium-high |

Examples that prove `suite.unit` is mixed rather than pure app logic:

- infra/tooling style:
  - `ci_artifact_retention`
  - `ci_strict_gates_validation`
  - `rch_artifact_sync_preflight`
  - `sdk_api`
  - `sdk_unit`
  - `interactive_commands_unit`
- security/policy style:
  - `security_budgets`
  - `security_conformance_benign`
  - `install_time_security_scanner`
  - `phase3_security_invariants`
- perf/budget style:
  - `perf_budgets`
  - `perf_regression`
  - `perf_comparison`
  - `performance_comparison`
- contract/parity style:
  - `json_mode_parity`
  - `cross_surface_parity`
  - `vcr_parity_validation`
  - `sec_compatibility_conformance`
  - many `*_contract` files

The explicit `6`-file curated subset confirms the current required fast gate is
not a representative stand-in for the full `suite.unit` inventory. The plan
must treat it as a deliberate fast regression gate, not as "the unit-test
category."

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
| `just test unit-full` | long-ci candidate | broad deterministic unit inventory | VCR, E2E, generated conformance, fuzz | local and `long-ci` |
| `just test integration` | long-ci candidate | broad non-E2E integration and seam behavior | full E2E, fuzz, generated conformance | local and `long-ci` |
| `just test vcr-fixture` | long-ci candidate | VCR playback behavior separated from generic integration | live-provider and full E2E behavior | local and `long-ci` |
| `just test parity` | long-ci candidate | parity bundle that was visible in PR #1 | full E2E and generated conformance | local and `long-ci` |
| `just test security` | long-ci candidate | bounded security regression surface | fuzz and heavyweight policy workflows | local and `long-ci` |
| `just test perf-benchmark` | long-ci candidate | bounded perf regression bundle from PR #1 | full benchmark orchestration | local and `long-ci` |
| `just test extension-sharded` | long-ci candidate | bounded sharded extension matrix | weekly community and heavy generated variants | local/prereqs and `long-ci` |
| `just test conformance-fast` | long-ci candidate | fast conformance profiles with explicit prerequisites | generated matrix and weekly community variants | local/prereqs and `long-ci` |
| `just test e2e-ci-smoke` | long-ci candidate | one bounded E2E smoke profile | full E2E inventory | local/prereqs and `long-ci` |
| `just test e2e-full` | specialty-evidence | full E2E inventory | nothing | local/prereqs and manual/scheduled CI |
| `just test fuzz` | specialty-evidence | fuzz smoke and fuzz depth lanes | unrelated correctness categories | local/prereqs and manual/scheduled CI |
| `just test semver` | specialty-evidence | API compatibility check | runtime behavior coverage | local and `long-ci` |
| `just test model-catalog-drift` | specialty-evidence | catalog drift visibility | runtime behavior coverage | local and manual/scheduled CI |
| `just test long-ci` | long-ci aggregate | bounded CI-friendly broad categories in one documented bundle | unbounded E2E, fuzz, and other known long-tail categories | sprint closeout, risky PRs, and nightly |
| `just test all` | upstream-broad local lane | convenience aggregation for local confidence | specialty scheduled/manual workflows | local/manual only in Phase A |
| `just lint all-local` | upstream-broad local lane | optional broader local lint surface | dependency lint and scheduled specialty checks | local/manual only in Phase A |

This table is intentionally simple. The goal is to let an operator answer
"what am I proving?" without reverse-engineering the workflow YAML.

`just test long-ci` is the key correction to the current confusion. It should
aggregate the broad categories that were useful in PR #1 and keep them
available in CI with a longer timeout, while excluding the clearly unbounded
categories that hit multi-hour cancellations.

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
4. broad upstream confidence surfaces stay available as named `just` lanes and
   can be promoted into `long-ci` without being silently discarded

The safety model is additive:

- upstream baseline proves "we did not break the fork"
- ATM-owned lanes prove "we did not break our additions"
- integration lanes prove "we did not break the seam between them"

## Current Quantified Baseline Table

This is the required-baseline subset of the authoritative category matrix
above. It keeps the ordinary PR gate easy to review without losing the broader
category ledger.

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

1. `just help`
2. `just fmt check`
3. `just test compile`
4. `just test unit-basic`
5. `just lint clippy-bins`
6. `just lint clippy-lib`
7. `just test baseline`

Hard budget:

- total wall clock under 10 minutes

Per-step budget targets:

- `just help`: under 5 seconds
- `just fmt check`: under 30 seconds
- `just test compile`: under 4 minutes
- `just test unit-basic`: under 120 seconds
- `just lint clippy-bins`: under 2 minutes
- `just lint clippy-lib`: under 30 seconds
- `just test baseline`: under 30 seconds

These are budget allocations, not historical facts. Sprint validation must
measure and refresh them as each step is added.

## Proposed Long-CI Set

`long-ci` is the bounded broader CI set that sits between the tiny required
baseline and the clearly unbounded specialty workflows.

Initial candidate membership:

- `just test unit-full`
- `just test integration`
- `just test parity`
- `just test security`
- `just test perf-benchmark`
- `just test extension-sharded`
- `just test semver`

Initial exclusions until they are split or bounded better:

- `just test e2e-full`
- `just test fuzz`
- `just test benchmark-full`
- `just test conformance-fast` generated variant

Initial planning rule:

- `long-ci` may use a longer timeout than `baseline`
- `long-ci` is allowed on sprint closeout, risky PRs, pre-merge, and nightly
- `long-ci` does not replace the ordinary PR `baseline`
- a category joins `long-ci` only after its timing cell is backed by measured
  or capped evidence in the matrix above

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

Phase A must distinguish four different ideas that the repo currently blurs:

- the required fast gate called `unit-basic`
- inline Rust unit tests under `src/**`
- the broad deterministic bucket currently called `[suite.unit]`
- the cleaner deterministic sub-buckets that should be measured inside
  `[suite.unit]`

Required rule:

- `unit-basic` is currently an explicit allowlist lane because upstream
  `[suite.unit]` is too broad for an early deterministic gate
- `unit-basic` must not blindly expand to all of `[suite.unit]`
- `unit-basic` overlaps `unit-inline-core` and a narrow curated slice of
  `[suite.unit]`; it is a gate, not a category
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

Required A9 unit breakout target:

- `unit-inline-core`
- `unit-app-logic`
- `unit-infra-tooling`
- `unit-security-policy`
- `unit-perf-policy`
- `unit-contract-parity`
- `unit-curated-files`
- `unit-full`

These sub-buckets may overlap the current `unit-basic` gate, but the report
must make that overlap explicit rather than hiding it.

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
