# Phase A Test Lane Report Template

Use this template for any sprint, PR, or phase-closeout report that needs to
show:

- what lane exists
- what it actually runs
- whether it belongs in ordinary CI, `long-ci`, or manual/scheduled use
- how long it takes locally and in CI
- what unit-test coverage it provides

## Report Metadata

- report scope:
- branch:
- commit SHA:
- PR:
- author:
- report date:
- evidence reviewer:

## Summary

- required baseline status:
- `long-ci` status:
- manual/scheduled-only status:
- biggest timing risk:
- biggest coverage gap:
- decision:

## Lane Ledger

| Lane | Exact command | Category | Ordinary CI | Long-CI | Manual / Scheduled Only | Can run locally | Local time | CI time | Unit coverage line % | Unit coverage function % | Unit coverage branch / region % | Evidence source | Status | Notes |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| `just help` | `just help` | metadata | yes | no | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just fmt check` | `just fmt check` | formatting | yes | no | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just test compile` | `just test compile` | compile-check | yes | no | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just test unit-basic` | `just test unit-basic` | unit-curated-fast | yes | no | no | yes | | | | | | | | |
| `just lint clippy-bins` | `just lint clippy-bins` | lint-bins | yes | no | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just lint clippy-lib` | `just lint clippy-lib` | lint-lib | yes | no | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just test baseline` | `just test baseline` | smoke-baseline | yes | no | no | yes | | | | | | | | |
| `just test unit-full` | `just test unit-full` | unit-full | no | yes | no | yes | | | | | | | | |
| `just test integration` | `just test integration` | integration-broad | no | yes | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just test vcr-fixture` | `just test vcr-fixture` | vcr-fixture | no | yes | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just test parity` | `just test parity` | parity | no | yes | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just test security` | `just test security` | security | no | yes | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just test perf-benchmark` | `just test perf-benchmark` | perf-benchmark | no | yes | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just test extension-sharded` | `just test extension-sharded` | extension-sharded | no | yes | no | prereqs | | | `n/a` | `n/a` | `n/a` | | | |
| `just test e2e-ci-smoke` | `just test e2e-ci-smoke` | e2e-ci-smoke | no | yes | no | prereqs | | | `n/a` | `n/a` | `n/a` | | | |
| `just test e2e-full` | `just test e2e-full` | e2e-full | no | no | yes | prereqs | | | `n/a` | `n/a` | `n/a` | | | |
| `just test fuzz` | `just test fuzz` | fuzz | no | no | yes | prereqs | | | `n/a` | `n/a` | `n/a` | | | |
| `just test semver` | `just test semver` | semver | no | yes | no | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just test model-catalog-drift` | `just test model-catalog-drift` | model-catalog-drift | no | no | yes | yes | | | `n/a` | `n/a` | `n/a` | | | |
| `just test long-ci` | `just test long-ci` | long-ci-aggregate | no | yes | no | yes | | | `n/a` | `n/a` | `n/a` | | | |

## Unit Surface Breakdown

Use this table whenever a report needs to explain what the repo currently means
by "unit tests".

| Unit bucket | Is this a gate or a category? | Overlaps `unit-basic` | Current source surface | Example tests | Local time | CI time | Line % | Function % | Branch / Region % | Status | Notes |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| `unit-basic` | gate | `n/a` | curated inline prefixes plus `6` explicit test files | `capability_policy_model`, `model_serialization` | | | | | | | required fast gate, not a taxonomy |
| `unit-inline-core` | category | yes | inline `src/**` lib tests | `agent::tests`, `config::tests`, `model::tests` | | | | | | | |
| `unit-app-logic` | category | partial | deterministic app-logic subset of `[suite.unit]` | `config_precedence`, `session_conformance`, `provider_backward_lock` | | | | | | | |
| `unit-infra-tooling` | category | partial | deterministic CLI/RPC/SDK/CI/helper subset of `[suite.unit]` | `ci_strict_gates_validation`, `sdk_unit`, `interactive_commands_unit` | | | | | | | |
| `unit-security-policy` | category | partial | deterministic security/policy subset of `[suite.unit]` | `security_budgets`, `phase3_security_invariants`, `install_time_security_scanner` | | | | | | | |
| `unit-perf-policy` | category | partial | deterministic perf-budget subset of `[suite.unit]` | `perf_budgets`, `perf_regression`, `performance_comparison` | | | | | | | |
| `unit-contract-parity` | category | partial | deterministic contract/parity subset of `[suite.unit]` | `json_mode_parity`, `cross_surface_parity`, `vcr_parity_validation` | | | | | | | |
| `unit-curated-files` | category | yes | explicit `tests/*.rs` subset inside the fast gate | `redaction_test`, `extension_scoring_ope` | | | | | | | |
| `unit-full` | aggregate | yes | full deterministic quick-profile unit surface | entire `[suite.unit]` inventory | | | | | | | aggregate, not a narrow category |

## Totals

- required baseline total local time:
- required baseline total CI time:
- `long-ci` total local time:
- `long-ci` total CI time:

## Evidence Sources

- local timing commands:
- CI workflow names:
- CI run IDs:
- CI commit SHAs:
- coverage command(s):

## Open Gaps

- missing timing rows:
- missing coverage rows:
- missing unit-bucket rows:
- unclear lane definitions:
- blocked or flaky lanes:

## Decision Record

- keep as required:
- keep in `long-ci`:
- keep manual/scheduled only:
- postpone / split further:
