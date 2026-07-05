# Phase A Test Lane Ledger

Date: 2026-07-05
Scope: operator-facing ledger for the Phase A `just` + CI system. This file is
meant to answer four questions directly:

1. What does each required `just` lane actually run?
2. What does it intentionally not run?
3. How long does it take locally and in CI?
4. What did Phase A actually prove by the end of Sprint A7?

## Executive Summary

Current Phase A state is narrower than the original intent.

- Required PR CI is one workflow named `baseline`.
- `baseline` is one Linux job on `ubuntu-latest`.
- Cross-platform CI still exists in `.github/workflows/ci.yml`, but on the
  Phase A sprint branches it is `workflow_dispatch` only, not ordinary PR
  gating.
- Extension conformance also still exists, but on the Phase A sprint branches
  it is scheduled/manual, not ordinary PR gating.
- The final merged target branch did not demonstrate a measured parallel
  multi-platform required gate.

What Phase A did prove:

- the fork can run a single required Linux baseline through `just`
- compile check landed before lint expansion
- strict `unit-basic` landed before smoke expansion
- local-only richer lanes can exist without becoming required PR blockers

What Phase A did not prove:

- final parallel multi-platform required CI
- final cross-platform timing budget
- full upstream test coverage parity inside required PR gating

## Operator Surface

Top-level `just` commands on the Phase A sprint branches:

- `just help`
- `just fmt`
- `just lint`
- `just test`
- `just explain`
- `just suites`

Source of truth:

- `justfile`
- `.just/test_catalog.py`
- `.just/lint_catalog.py`
- `.just/unit_basic_audit.py`

## Required PR Baseline: Exact Shape

The required PR workflow from Sprint A3 onward runs this fixed sequence:

1. `just help`
2. `just fmt check`
3. `just test compile`
4. `just test unit-basic`
5. `just lint clippy-bins`
6. `just lint clippy-lib`
7. `just test baseline`

Phase A sprint rollout shape:

| Sprint | Required PR contents |
| --- | --- |
| A1 | `help`, `fmt check`, `test compile`, `test unit-basic` |
| A2 | A1 + `lint clippy-bins`, `lint clippy-lib` |
| A3 | A2 + `test baseline` |
| A4 | same as A3 |
| A5 | same as A3 |
| A6 | same as A3 |
| A7 | same as A3 |

## Lane Ledger

### `just test compile`

- Lane ID: `compile`
- Backing command: `cargo check --all-targets`
- Source of truth: `.just/test_catalog.py`
- Blocking class: `required`
- What it proves:
  - the repo compiles across library, binaries, tests, benches, and examples
  - compile breakage is caught before broader runtime tests are considered
- What it does not prove:
  - that tests pass
  - that lint is clean
  - that runtime behavior is correct

### `just test unit-basic`

- Lane ID: `unit-basic`
- Backing shape: multiple `cargo test` invocations generated from
  `.just/unit_basic_audit.py` plus six explicit test binaries
- Source of truth: `.just/test_catalog.py` and `.just/unit_basic_audit.py`
- Blocking class: `required`
- Included inline module prefixes: 32
- Exclusion rules recorded in audit helper: 80

Included inline module prefixes:

- `acp::tests` with one timeout exclusion
- `agent::abort_tests`
- `agent::compatible_tool_parallelism_tests`
- `agent::extensions_integration_tests`
- `agent::message_queue_tests`
- `agent::tests`
- `agent::tool_effect_batch_planning_tests`
- `agent::turn_event_tests`
- `agent_cx::tests`
- `app::tests`
- `autocomplete::tests`
- `cli::tests`
- `compaction::tests`
- `config::tests`
- `connectors::tests`
- `crypto_shim::tests`
- `error::tests`
- `error_hints::tests`
- `flake_classifier::tests`
- `migrations::tests`
- `model::tests`
- `model_routing::tests`
- `models::tests`
- `permissions::tests`
- `platform::tests`
- `provider::tests`
- `provider_metadata::tests`
- `resources::tests`
- `sdk::tests`
- `session::tests` with 15 interactive extension-session exclusions
- `sse::tests`
- `tui::tests`

Explicit non-inline test binaries in `unit-basic`:

- `capability_policy_model`
- `policy_profile_hardening`
- `extension_flag_passthrough`
- `model_serialization`
- `redaction_test`
- `extension_scoring_ope`

What `unit-basic` is intended to prove:

- deterministic core logic and serialization behavior
- parsing, routing, configuration, session-core, SSE, and small TUI/helper
  invariants
- a strict early gate narrower than the broad upstream `[suite.unit]` bucket

What `unit-basic` intentionally excludes:

- timing-sensitive flows
- auth/network/device-flow tests
- conformance inventory and replay audits
- extension runtime/policy matrices beyond the strict subset
- binary-launching tests
- shell-script/perf harness tests
- VCR-heavy, artifact-audit, or broader integration surfaces

Important operator note:

- despite the name, `unit-basic` is not "all unit tests"
- it is a curated allowlist intended to stay fast and deterministic

### `just lint clippy-bins`

- Lane ID: `clippy-bins`
- Backing command:
  `cargo clippy --no-deps --bins -- -D warnings`
- Source of truth: `.just/lint_catalog.py`
- Blocking class: `required`
- What it proves:
  - binary targets build lint-clean under Clippy
- What it does not prove:
  - library target lint cleanliness
  - tests/benches/examples lint cleanliness

### `just lint clippy-lib`

- Lane ID: `clippy-lib`
- Backing command:
  `cargo clippy --no-deps --lib -- -D warnings`
- Source of truth: `.just/lint_catalog.py`
- Blocking class: `required`
- What it proves:
  - library target builds lint-clean under Clippy
- What it does not prove:
  - test/bench/example lint cleanliness

### `just test baseline`

- Lane ID: `baseline`
- Backing script:
  `./scripts/smoke.sh --skip-lint --no-rch --only unit`
- Source of truth: `.just/test_catalog.py`
- Blocking class: `required`
- Documented smoke targets:
  - `model_serialization`
  - `config_precedence`
  - `session_conformance`
  - `error_types`
  - `compaction`
  - `security_budgets`

What `baseline` is intended to prove:

- a very small smoke slice across core model/config/session/error/compaction
  behavior
- the required PR lane can catch obvious regressions without pulling in the
  broader VCR or integration universe

What `baseline` intentionally excludes in required PR CI:

- VCR smoke targets
- extension conformance
- provider matrix coverage
- E2E scenarios
- fuzz, bench, semver, and drift jobs

Optional VCR smoke targets exist in `scripts/smoke.sh`, but they are not part
of the required PR gate:

- `provider_streaming`
- `error_handling`
- `http_client`
- `sse_strict_compliance`
- `model_registry`
- `provider_factory`

## Optional Local Lanes

These exist to expose richer surfaces without making ordinary PR CI heavier.

### `just test unit`

- Backing command: `./verify --profile quick --skip-lint`
- Blocking class: `optional`
- Purpose:
  - broader quick local verification profile
- Current evidence from A5:
  - PR #15 recorded `rc127`, so this lane exposed follow-up gaps rather than a
    ready blocking lane

### `just test integration`

- Backing command: `./verify --profile ci --skip-lint --skip-e2e`
- Blocking class: `optional`
- Purpose:
  - non-E2E integration verification profile
- Current evidence from A5:
  - PR #15 recorded `rc127`

### `just test all`

- Backing command: `./verify --profile full --skip-lint`
- Blocking class: `optional`
- Safety gate:
  - requires `PI_VERIFY_E2E_READY=1`
- Purpose:
  - full local verification once external readiness is explicit
- Current evidence from A5:
  - PR #15 recorded `rc127`

### `just lint all-local`

- Backing sequence:
  - `just fmt check`
  - `just lint clippy-bins`
  - `just lint clippy-lib`
  - `cargo clippy --no-deps --tests -- -D warnings`
  - `cargo clippy --no-deps --benches -- -D warnings`
  - `cargo clippy --no-deps --examples -- -D warnings`
- Blocking class: `optional`
- Current evidence from A5:
  - PR #15 recorded failure (`rc1`) after `246.77s`

## Upstream Workflow Boundaries After Phase A

What remains outside the required PR gate on the Phase A sprint branches:

| Workflow | Trigger shape after Phase A changes | What it still covers |
| --- | --- | --- |
| `baseline.yml` | `pull_request` | single required Linux fast gate |
| `ci.yml` | `workflow_dispatch` | broader cross-OS compile/test/policy checks |
| `conformance.yml` | `schedule`, `workflow_dispatch` | extension/runtime compatibility matrix |
| `fuzz.yml` | `schedule`, `workflow_dispatch` | fuzz smoke / longer fuzz evidence |
| `bench.yml` | `workflow_dispatch` | benchmark surface |
| `semver.yml` | `workflow_dispatch` | API compatibility checks |
| `model-catalog-drift.yml` | `schedule`, `workflow_dispatch` | catalog drift checks |

Operator conclusion:

- the repo still has broader testing machinery
- Phase A chose not to keep that machinery in required ordinary PR CI
- this is why GitHub mostly shows one visible check during the sprint chain

## Timing Ledger

### Per-Sprint Timing Progression Recorded In PRs

These numbers come from the Phase A sprint PR notes.

| Sprint | PR | Local aggregate | CI run | CI total | Note |
| --- | --- | --- | --- | --- | --- |
| A1 | #12 | `52.60s` | `28698960460` | `10m35s` | over target on accepted A1 rerun |
| A2 | #11 | `~1021s` | `28730331129` | `6m55s` | CI under target; local cold compile heavy |
| A3 | #13 | `~517s` | `28731407499` | `7m09s` | first steady-state baseline under target |
| A4 | #14 | helper timings + unchanged baseline rerun `183.74s` | `28732090084` | `7m27s` | helper sprint; baseline unchanged |
| A5 | #15 | optional lanes failed; unchanged baseline rerun `59.73s` | `28732849880` | `7m03s` | required CI unchanged |
| A6 | #16 | `511.57s` | `28734239450` attempt 2 | `7m04s` | same-SHA attempt 1 was `12m11s` |
| A7 | #17 | `568.00s` | `28735967657` | `7m09s` | sprint branch handoff run |

### A7 Sprint Branch Timing

Branch: `sprint-a-7-merge-baseline-into-atm-graft`
Run ID: `28735967657`
Head SHA: `c3e16e49f0a855659bbdd9668446f099353d06ec`
Conclusion: success

| Step | Time |
| --- | --- |
| total | `7m09s` |
| Just help | `1m41s` |
| Format gate | `16s` |
| Compile gate | `1m48s` |
| Basic unit gate | `1m26s` |
| Clippy bins | `57s` |
| Clippy lib | `<1s` |
| Smoke baseline | `14s` |

### Final Merged Target Branch Timing

Branch: `feature/atm-graft-integration`
Run ID: `28736534784`
Head SHA: `2bbd5d16f02c1e2613f31132852d04938ecb697d`
Conclusion: success

This is the timing that matters for the actual Phase A handoff target.

| Step | Time |
| --- | --- |
| total | `12m33s` |
| Just help | `4m29s` |
| Format gate | `16s` |
| Compile gate | `3m29s` |
| Basic unit gate | `1m23s` |
| Clippy bins | `1m51s` |
| Clippy lib | `<1s` |
| Smoke baseline | `13s` |

Operator conclusion:

- the sprint branch demonstrated a `~7m` Linux baseline
- the merged target branch demonstrated a `~12m33s` Linux baseline
- Phase A therefore did not finish with one stable, measured final timing story

## Coverage Notes

There is no Phase A-specific coverage measurement attached to the required
baseline lanes.

### Best Available Production-Code Coverage Evidence

The best available percentage-based production-code coverage evidence in this
repo is the historical `cargo-llvm-cov` baseline summarized in
`docs/TEST_COVERAGE_MATRIX.md` and backed by `docs/coverage-baseline-map.json`.

These percentages do **not** come from:

- `just test unit-basic`
- `just test baseline`
- the final required Phase A lane set
- the A7 `1m23s` CI `Basic unit gate`

They come from a much broader historical coverage run over the repo's larger
test surface.

That historical baseline reports:

| Metric | Value |
| --- | --- |
| Generated at | `2026-02-14T14:00:00Z` |
| Source files in baseline | `107` |
| Current source files when the matrix was written | `110` |
| Line coverage | `79.08%` |
| Function coverage | `78.01%` |
| Branch coverage | `51.95%` lower bound |
| Branch-measurable files | `63` |
| Branch export SIGSEGV fallback files | `44` |

Interpretation:

- these percentages are repo-wide production-code coverage evidence from a
  broader historical suite
- they are not lane-specific
- they are not evidence that the current Phase A required baseline achieves
  anything close to `79.08%` line coverage
- they include test surfaces that are outside the final Phase A required gate

### Critical Coverage Gap

We do not have a measured "% of production code covered by `unit-basic`" or
"% of production code covered by the final required Phase A baseline".

What we have instead:

- lane definitions
- included/excluded test targets
- repo-wide historical coverage percentages

What we do not have:

- isolated coverage percentages for:
  - `just test unit-basic`
  - `just test baseline`
  - the exact A7 required PR lane set as a combined coverage profile

Practical implication:

- the final required Phase A lane is fast because it is selective
- that selectivity is exactly why you should assume its real production-code
  coverage is materially lower than the historical repo-wide percentages until
  someone measures it directly

### Measured Coverage For The Final Required Test Lanes

Measured on 2026-07-05 in the A7 worktree by instrumenting the exact required
test lanes only:

- `just test unit-basic`
- `just test baseline`

Lint and compile lanes were not included because they do not execute tests and
do not contribute runtime coverage.

Measured production-code coverage across `src/**/*.rs`:

| Metric | Covered | Total | Percent |
| --- | ---: | ---: | ---: |
| Line coverage | `55,260` | `241,293` | `22.90%` |
| Function coverage | `4,930` | `21,073` | `23.39%` |
| Region coverage | `75,597` | `347,844` | `21.73%` |
| Source files included in aggregate | `108` | n/a | n/a |

Timing notes from the same instrumented run:

- `just test unit-basic`: `40.26s` warm instrumented rerun
- `just test baseline`: smoke targets completed in `12.88s`, but the script
  then failed on a Bash-array `set -u` bug that was subsequently fixed

Interpretation:

- the final required Phase A lane is a smoke/regression gate, not a high-coverage
  test gate
- the lane-specific measured coverage is far below the historical repo-wide
  coverage numbers
- this measured result is consistent with your intuition that a `~1m23s`
  non-instrumented unit gate cannot plausibly deliver ~80% production-code
  coverage by itself

Operator conclusion:

- the repo has historical production-code coverage evidence
- the Phase A work did not convert that into lane-specific coverage evidence for
  the final required baseline
- this is one reason the current Phase A result remains hard to justify

## Honest Final Assessment

If the question is "do we have a working `just`-backed required PR baseline?",
the answer is yes.

If the question is "do we have an understandable operator-grade system that
shows exactly what is tested, what is excluded, and how long it takes?", the
answer was no until this ledger was added.

If the question is "did Phase A prove a final measured parallel multi-platform
required gate?", the answer is no.
