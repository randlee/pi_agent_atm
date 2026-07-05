# Phase A - Testing Strategy

Date: 2026-07-02
Status: planning

## Purpose

Define the authoritative testing strategy for Phase A so local agent execution
and CI use the same lane definitions, the same expectations, and the same
timing budget.

## Strategy Rules

1. `just` is the primary local operator surface.
2. Required PR CI must map directly to `just` commands.
3. One lane must have one source of truth.
4. Fast lanes must fail early with actionable next steps.
5. Long-running coverage must be optional, manual, or scheduled unless proven
   necessary for required PR CI.

## Current Repo Facts

Observed from `tests/suite_classification.toml`:

- `suite.unit`: 118 targets
- `suite.vcr`: 144 targets
- `suite.e2e`: 39 targets
- top-level `tests/*.rs` integration-test crates: 301

Important distinction:

- inline unit tests in `src/**` are not the same as `suite.unit`
- the size of the `tests/*.rs` surface makes `cargo clippy --tests` and broad
  `cargo test` inherently expensive even without third-party dependency linting

## Source Of Truth Policy

Target end state:

- lint lanes defined in one `.just/` lane catalog
- test lanes defined in one `.just/` lane catalog
- suite membership defined in `tests/suite_classification.toml`
- CI workflows invoke the same `just` lanes instead of bespoke parallel shell
  commands

Exploratory candidate sources to review before reimplementation:

- `feature/just-integration:.just/lint_catalog.py`
- `feature/just-integration:.just/test_catalog.py`
- `feature/just-integration:.just/explain.py`
- `feature/just-integration:.just/show_suites.py`
- `feature/just-integration:.just/run_test.py`

## Required PR CI Policy

Required PR CI should contain one workflow:

- `baseline`

Expected required steps:

- `just fmt check`
- `just lint clippy-lib`
- `just lint clippy-bins`
- `just test baseline`

Budget:

- less than 10 minutes total wall clock

## Long-Running Lane Policy

These do not belong in required PR CI by default:

- fuzz
- semver
- benchmarks
- weekly evidence refresh
- broad certification / release-verdict lanes
- monolithic shard-based integration sweeps

## Observed Timing Baseline

### Local macOS exploratory timings

Source: prior `feature/just-integration` verification log.

| Command | Result | Observed wall time |
|---|---|---:|
| `just help` | pass | `<1s` |
| `just suites` | pass | `<1s` |
| `just fmt check` | pass | `12.46s` |
| `just lint clippy-lib` | pass | `50.66s` |
| `just lint clippy-bins` | pass | `2.87s` |
| `just test baseline` | pass | `10.59s` |
| `just lint clippy-tests` | incomplete | `>3m38s` before manual stop |
| `just test unit` | incomplete | `>120s` before timeout |
| `just test integration` | incomplete | `>120s` before timeout |
| `just test` | incomplete | `>120s` before timeout |
| `just test all` | incomplete | `>120s` before timeout |

Interpretation:

- format, narrow clippy slices, and a smoke lane fit a fast baseline
- broad `clippy --tests` and broad test orchestration do not belong in the
  default fast lane

### GitHub Actions timings

Observed from actual runs on 2026-07-02:

| Workflow | Run | Result | Approximate wall time |
|---|---|---|---:|
| `baseline` | `28622615189` | success | `~7m03s` |
| `Extension Conformance` | `28622615206` | success | `~6m25s` |
| `Fuzz CI` | `28622615217` | success | `~42m59s` |
| old monolithic `ci` | `28618082382` | cancelled | `~49m25s` before cancellation |

Baseline step timings from run `28622615189`:

| Step | Wall time |
|---|---:|
| `Format gate` | `~15s` |
| `Clippy lib` | `~2m38s` |
| `Clippy bins` | `~2s` |
| `Baseline smoke test` | `~3m19s` |

## Known Issues

### macOS / portability

1. Bash 3 portability concerns exist.
2. `just clean` previously failed against `target/agents/...` on macOS.
3. A `vergen-lib` local build-script issue was observed during exploratory runs.

### Toolchain / CI

1. Prior fuzz failures hit `sysinfo` / nightly drift.
2. Historical CI used incorrect working-directory paths.
3. A later exploratory `baseline` failure was caused by rustfmt drift from
   unrelated source changes, not by the fast-lane design itself.
4. The old monolithic `ci` workflow mixed cheap gates with 40+ minute jobs.

## Failure Reporting Rules

Every `just` lane and required CI step should report:

- failing lane name
- exact underlying command
- source-of-truth file
- one next action

Examples:

- suite classification issues:
  - point to `tests/suite_classification.toml`
- lane-definition issues:
  - point to the relevant `.just/` catalog
- smoke target issues:
  - point to the smoke-lane definition surface

Minimum failure payload:

- failing lane name
- exact command string
- source-of-truth file path
- one next action
- non-zero exit code

## Exit Criteria

The Phase A testing strategy is implemented when:

- local `just` and required PR CI share the same lane definitions
- required PR CI is under 10 minutes
- long-running workflows are explicitly classified outside required PR CI
- timing information is refreshed on the implementation branch
