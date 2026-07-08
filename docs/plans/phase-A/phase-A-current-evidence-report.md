# Phase A Current Evidence Report

Report date: 2026-07-08
Scope: current planning-branch evidence snapshot
Branch: `plan/phase-A-attempt-3`
Commit SHA: pending after evidence cleanup commit
PR: planning branch docs only
Evidence reviewer: pending

## Summary

- required baseline status: defined and historically demonstrated on Linux only
- `long-ci` status: category set identified, but not yet frozen as an
  implemented `just test long-ci` lane
- manual/scheduled-only status: `e2e-full`, `fuzz`, heavy generated
  conformance, and full benchmark remain outside ordinary CI
- biggest timing risk: `integration-broad` is still mixed and historically
  included a shard cancelled after about `5h59m`
- biggest coverage gap: only the combined required test lanes currently have
  measured production-code coverage
- decision: keep Phase A only if the missing implementation and measurement
  gaps below are closed explicitly rather than hand-waved

## Lane Ledger

| Lane | Exact command | Category | Ordinary CI | Long-CI | Manual / Scheduled Only | Can run locally | Local time | CI time | Unit coverage line % | Unit coverage function % | Unit coverage branch / region % | Evidence source | Status | Notes |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| `just help` | `just help` | metadata | yes | no | no | yes | `0.09s` after lazy-load fix | historical retained Linux step `4m29s` on run `28736534784`; re-measurement still required after the fix | `n/a` | `n/a` | `n/a` | retained local rerun plus PR #1 baseline workflow | partial | old timing was dominated by an import-time cargo bug and must not be treated as the steady-state fact |
| `just fmt check` | `just fmt check` | formatting | yes | no | no | yes | about `13s` retained | `16s` on run `28736534784` | `n/a` | `n/a` | `n/a` | retained local runs plus PR #1 baseline workflow | measured | formatting guard only |
| `just test compile` | `cargo check --all-targets` | compile-check | yes | no | no | yes | about `159s-293s` retained | `3m29s` on run `28736534784` | `n/a` | `n/a` | `n/a` | retained local runs plus PR #1 baseline workflow | measured | compile safety only, not a test pass signal |
| `just test unit-basic` | current sprint-a7 lane: audited inline allowlist plus `6` explicit unit files | unit-curated-fast | yes | no | no | yes | `40.26s` warm instrumented rerun; retained non-instrumented about `94s-104s` | `1m23s` on run `28736534784` | not isolated | not isolated | not isolated | retained local rerun, PR #1 baseline workflow, and unit-basic audit | partial | fast gate overlaps inline lib tests and a narrow curated `tests/*.rs` slice; it is a gate, not a natural category |
| `just lint clippy-bins` | `just lint clippy-bins` | lint-bins | yes | no | no | yes | about `57s-97s` retained | `1m51s` on run `28736534784` | `n/a` | `n/a` | `n/a` | retained local runs plus PR #1 baseline workflow | measured | local-code binary lint only |
| `just lint clippy-lib` | `just lint clippy-lib` | lint-lib | yes | no | no | yes | about `1s` retained | `<1s` on run `28736534784` | `n/a` | `n/a` | `n/a` | retained local runs plus PR #1 baseline workflow | measured | library lint only |
| `just test baseline` | `./scripts/smoke.sh --skip-lint --no-rch --only unit` | smoke-baseline | yes | no | no | yes | `12.88s` warm instrumented rerun; retained non-instrumented about `14s-16s` | `13s` on run `28736534784` | not isolated | not isolated | not isolated | retained local rerun plus PR #1 baseline workflow | partial | tiny deterministic smoke slice; not broad integration proof |
| `just test unit-full` | planned mapping: `./scripts/e2e/run_all.sh --profile quick --skip-lint` | unit-full | no | yes | no | yes | `>120s` capped observation retained | `6m41s` execute-lane time on old `qa-shard (unit)` in run `28631117871` | not yet measured | not yet measured | not yet measured | retained old CI run and capped local observation | partial | broad unit surface should return as a named lane, but the current planning branch has not implemented it as a first-class lane yet |
| `just test integration` | planned mapping: `./scripts/e2e/run_all.sh --profile ci --skip-lint --skip-e2e` | integration-broad | no | yes | no | yes | no clean retained local timing | one shard finished in `8m01s`; paired shard cancelled after about `5h59m` on run `28631117871` | `n/a` | `n/a` | `n/a` | old monolithic CI run only | capped observation | still too mixed and poorly bounded to trust as a clean `long-ci` member without further split-out |
| `just test vcr-fixture` | planned VCR-only playback lane; not implemented on current sprint-a7 branch | vcr-fixture | no | yes | no | yes | no isolated retained local timing | not isolated; only mixed historical evidence inside `integration-broad` from run `28631117871` | `n/a` | `n/a` | `n/a` | inferred from old CI shape and suite taxonomy | estimated | this category exists conceptually in upstream taxonomy, but not yet as a readable current `just` lane |
| `just test parity` | planned parity bundle matching old `qa-shard (parity)` | parity | no | yes | no | yes | no clean retained local timing | `3m52s` execute-lane time on run `28631117871` | `n/a` | `n/a` | `n/a` | old monolithic CI run | measured | understandable and bounded category from abandoned PR #1 that should stay visible |
| `just test security` | planned security bundle matching old `qa-shard (security)` | security | no | yes | no | yes | no clean retained local timing | `3m41s` execute-lane time on run `28631117871` | `n/a` | `n/a` | `n/a` | old monolithic CI run | measured | bounded category and a good `long-ci` candidate once restored through `just` |
| `just test perf-benchmark` | planned perf bundle matching old `qa-shard (perf)` | perf-benchmark | no | yes | no | yes | no clean retained local timing | `5m57s` execute-lane time on run `28631117871` | `n/a` | `n/a` | `n/a` | old monolithic CI run | measured | keep separate from full benchmark runs |
| `just test extension-sharded` | planned sharded extension conformance bundle | extension-sharded | no | yes | no | prereqs | no clean retained local timing | retained shard times `3m50s`, `4m41s`, `4m42s`, and `4m46s` on run `28631117871` | `n/a` | `n/a` | `n/a` | old monolithic CI run | measured | valid bounded category once exposed as a named lane with prerequisites documented |
| `just test e2e-ci-smoke` | planned bounded CI E2E smoke lane; not yet isolated | e2e-ci-smoke | no | yes | no | prereqs | no isolated retained local timing | no isolated retained CI timing yet | `n/a` | `n/a` | `n/a` | category intent only | missing | acceptable only if it is actually isolated and measured rather than inferred from a larger profile |
| `just test e2e-full` | planned full E2E profile: `./scripts/e2e/run_all.sh --profile full` | e2e-full | no | no | yes | prereqs | estimate: long | two old shards cancelled after about `5h59m-6h00m` on run `28631117871` | `n/a` | `n/a` | `n/a` | old monolithic CI run | capped observation | clearly outside routine PR CI |
| `just test fuzz` | `.github/workflows/fuzz.yml` and future `just` wrapper if desired | fuzz | no | no | yes | prereqs | estimate: long | retained workflow about `42m59s` | `n/a` | `n/a` | `n/a` | retained GitHub Actions run | partial | keep exposed, but not in ordinary CI or early `long-ci` |
| `just test semver` | semver workflow / future `just` wrapper | semver | no | yes | no | yes | estimate: medium | `24s` semver-check step and `2m38s` total job on run `28631117866` | `n/a` | `n/a` | `n/a` | retained semver workflow | measured | API compatibility check, not runtime behavior coverage |
| `just test model-catalog-drift` | drift workflow / future `just` wrapper | model-catalog-drift | no | no | yes | yes | estimate: low-medium | `15s` retained latest drift run on reverted head | `n/a` | `n/a` | `n/a` | retained drift workflow | partial | advisory drift detection only |
| `just test long-ci` | planned aggregate over bounded broad categories | long-ci-aggregate | no | yes | no | yes | not yet measured as one command | not yet bounded as one command; current candidate serial sum is already `>35m`, and historical integration evidence still contains a cancelled `~5h59m` shard | `n/a` | `n/a` | `n/a` | derived from candidate membership only | missing | Phase A cannot claim success here until the aggregate is implemented and measured honestly |

## Unit Surface Breakdown

| Unit bucket | Is this a gate or a category? | Overlaps `unit-basic` | Current source surface | Example tests | Local time | CI time | Line % | Function % | Branch / Region % | Status | Notes |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| `unit-basic` | gate | `n/a` | `32` audited inline prefixes plus `6` explicit test files and `80` explicit exclusions in the current audit | `capability_policy_model`, `model_serialization` | `40.26s` warm instrumented rerun; retained non-instrumented about `94s-104s` | `1m23s` on run `28736534784` | not isolated | not isolated | not isolated | partial | required fast gate, not a taxonomy |
| `unit-inline-core` | category | yes | `32` audited inline test prefixes under `src/**` | `agent::tests`, `config::tests`, `model::tests` | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | missing | cross-cuts source modules rather than `tests/*.rs` files |
| `unit-app-logic` | category | partial | `28` of `124` `[suite.unit]` files = `22.58%` of the file inventory | `config_precedence`, `provider_backward_lock`, `session_store_v2` | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | partial | taxonomy audit complete, timings and coverage still missing |
| `unit-infra-tooling` | category | partial | `23` of `124` `[suite.unit]` files = `18.55%` of the file inventory | `ci_strict_gates_validation`, `sdk_unit`, `interactive_commands_unit` | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | partial | proves that `suite.unit` is not pure product logic |
| `unit-security-policy` | category | partial | `13` of `124` `[suite.unit]` files = `10.48%` of the file inventory | `phase3_security_invariants`, `policy_profile_hardening`, `security_budgets` | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | partial | security and policy work is mixed into the current broad unit bucket |
| `unit-perf-policy` | category | partial | `9` of `124` `[suite.unit]` files = `7.26%` of the file inventory | `perf_budgets`, `perf_regression`, `performance_comparison` | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | partial | perf-budget tests are real unit inventory, but not part of the tiny required gate |
| `unit-contract-parity` | category | partial | `51` of `124` `[suite.unit]` files = `41.13%` of the file inventory | `json_mode_parity`, `cross_surface_parity`, `vcr_parity_validation` | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | partial | largest broad unit sub-bucket in the current audit |
| `unit-curated-files` | category | yes | `6` explicit `tests/*.rs` files = `4.84%` of the `[suite.unit]` file inventory | `redaction_test`, `extension_scoring_ope` | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | not yet measured separately | partial | cross-cutting subset inside the fast gate; not additive with the five file-bucket categories above |
| `unit-full` | aggregate | yes | full deterministic quick-profile unit surface over `[suite.unit]` = `124` files plus inline coverage | entire `[suite.unit]` inventory | `>120s` capped observation retained | `6m41s` old `qa-shard (unit)` execute-lane time on run `28631117871` | not yet measured separately | not yet measured separately | not yet measured separately | partial | aggregate broad unit surface, not a narrow category |

## Totals

- required baseline total local time: about `5m38s-8m44s` using retained normal
  local timings
- required baseline total CI time: historical retained Linux total `12m33s` on
  run `28736534784`; projected near `8m04s` after the `just help` lazy-load
  fix, but not yet re-measured on the merged target branch
- `long-ci` total local time: not yet measured as one aggregate
- `long-ci` total CI time: not yet bounded honestly because `integration-broad`
  is still mixed with a historically cancelled multi-hour shard

## Evidence Sources

- local timing commands:
  - retained `just` lane reruns documented in
    `docs/plans/phase-A/phase-A-testing-strategy.md`
- CI workflow names:
  - `baseline`
  - old `ci`
  - `conformance`
  - `fuzz`
  - `semver`
  - `model-catalog-drift`
- CI run IDs:
  - `28736534784` baseline
  - `28631117871` old monolithic CI
  - `28631117865` conformance
  - `28631117866` semver
- CI commit SHAs:
  - `2bbd5d16f02c1e2613f31132852d04938ecb697d`
  - `211c4012384c9c1ba93e58f18f90f89611e01922`
- coverage command(s):
  - retained `cargo llvm-cov` measurement for the final required test lanes only
  - no per-category isolated coverage commands recorded yet for the broader
    unit categories

## Open Gaps

- missing timing rows:
  - `unit-inline-core`
  - `unit-app-logic`
  - `unit-infra-tooling`
  - `unit-security-policy`
  - `unit-perf-policy`
  - `unit-contract-parity`
  - `unit-curated-files`
  - `e2e-ci-smoke`
  - isolated `vcr-fixture`
- missing coverage rows:
  - every unit category except the combined required-lane result
- missing implementation rows:
  - `just test unit-full`
  - `just test vcr-fixture`
  - `just test parity`
  - `just test security`
  - `just test perf-benchmark`
  - `just test extension-sharded`
  - `just test e2e-ci-smoke`
  - `just test e2e-full`
  - `just test fuzz`
  - `just test semver`
  - `just test model-catalog-drift`
  - `just test long-ci`
- unclear lane definitions:
  - `integration-broad` still mixes VCR-like and broader non-E2E work
  - `long-ci` membership cannot be frozen until those mixed categories are
    split and measured
- blocked or flaky lanes:
  - old `integration-broad` historical evidence includes a cancelled
    `~5h59m` shard
  - old `e2e-full` historical evidence includes cancelled `~6h` shards

## Decision Record

- keep as required:
  - `just help`
  - `just fmt check`
  - `just test compile`
  - `just test unit-basic`
  - `just lint clippy-bins`
  - `just lint clippy-lib`
  - `just test baseline`
- keep in `long-ci` once implemented and re-measured:
  - `just test unit-full`
  - `just test parity`
  - `just test security`
  - `just test perf-benchmark`
  - `just test extension-sharded`
  - `just test semver`
- keep manual/scheduled only:
  - `just test e2e-full`
  - `just test fuzz`
  - full generated conformance
  - full benchmark runs
  - `just test model-catalog-drift`
- postpone / split further:
  - `just test integration`
  - `just test vcr-fixture`
  - `just test e2e-ci-smoke`
  - `just test long-ci`

## Closure Package Required Before Phase A Can Be Called Healthy

Phase A should not be called complete until:

- this evidence report has no silent blanks for any named lane or unit bucket
- every row is marked `measured`, `partial`, `estimated`, `capped
  observation`, `missing`, or `not implemented`
- the required baseline is re-measured on the final merged branch for Linux,
  macOS, and Windows
- `long-ci` exists as an actual runnable lane, not only a category idea
- the broad lanes restored from the abandoned PR #1 breakout are either:
  - implemented as named `just test ...` lanes
  - or explicitly deferred with rationale
- per-category unit coverage is measured or intentionally declined with a
  written reason
