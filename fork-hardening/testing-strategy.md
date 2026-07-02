# Testing Strategy

Date: 2026-07-02
Scope: `pi_agent_atm` fork baseline hardening

## Purpose

Define a test strategy that:

- mirrors required CI locally
- keeps one source of truth for lane membership
- fails fast with actionable diagnostics
- separates fast PR gates from long-running certification-style coverage
- records known platform and toolchain issues instead of rediscovering them

## Principles

1. `just` is the primary local operator surface.
2. Required PR CI must map directly to `just` commands.
3. The same lane must not be redefined in multiple places.
4. Fast lanes fail early and name the root source-of-truth file.
5. Long-running jobs are opt-in, scheduled, or manual unless they are proven to
   belong in required PR CI.
6. Fork-specific operating docs stay under `fork-hardening/`, not under
   upstream-facing `docs/`.

## Current Repo Facts

Observed from `tests/suite_classification.toml` on 2026-07-02:

- `suite.unit`: 118 targets
- `suite.vcr`: 144 targets
- `suite.e2e`: 39 targets
- `tests/*.rs` integration-test crates at repo root: 301

Important distinction:

- inline unit tests inside `src/**` are not the same thing as `suite.unit`
- the large number of `tests/*.rs` files means `cargo clippy --tests` and broad
  `cargo test` surfaces are inherently expensive even without third-party deps

## Command And CI Mapping

This is the intended end-state SSOT mapping.

| Surface | Meaning | Source of truth |
|---|---|---|
| `just lint` | all local lint children | `.just/lint_catalog.*` |
| `just lint fmt` | format gate | `.just/lint_catalog.*` |
| `just lint clippy-*` | local-surface clippy slices | `.just/lint_catalog.*` |
| `just test baseline` | fast smoke regression lane | `.just/test_catalog.*` plus smoke target list |
| `just test unit` | inline lib tests + classified `suite.unit` | `.just/test_catalog.*` and `tests/suite_classification.toml` |
| `just test integration` | non-E2E integration lane | `.just/test_catalog.*` |
| `just test vcr` | classified VCR targets only | `tests/suite_classification.toml` |
| `just test e2e` | classified E2E lane | `.just/test_catalog.*` |
| `just test all` | full local test surface excluding explicitly segregated long lanes | `.just/test_catalog.*` |
| required PR `baseline` workflow | fast PR gate | exact mirror of `just fmt check`, `just lint clippy-lib`, `just lint clippy-bins`, `just test baseline` |

## Proposed Lane Policy

### Required PR CI

- `baseline`

Goal:

- under 10 minutes
- Linux only unless later evidence proves cross-platform belongs in the same
  budget

Expected contents:

- format
- clippy on local lib + bins
- smoke baseline

### Optional PR Or Manual

- extension conformance fast profile
- targeted integration follow-up lanes
- cross-platform validation if needed for a specific PR

### Nightly / Scheduled / Manual Long Coverage

- fuzz
- semver
- benchmarks
- weekly evidence refresh
- broad certification or release-verdict workflows

## Timing Baseline

These timings are the best available baseline from the exploratory branch and
GitHub Actions runs on 2026-07-02. They should be replaced by fresh
measurements once the implementation branch is active.

### Local macOS exploratory timings

Source: `feature/just-integration` verification log from 2026-07-01.

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

- `fmt`, `clippy-lib`, `clippy-bins`, and a small smoke lane are compatible with
  a fast local / PR baseline.
- broad `clippy --tests` and full test orchestration are too expensive to sit in
  the default lane without further restructuring.

### GitHub Actions timings

Observed from actual runs on 2026-07-02:

| Workflow | Run | Result | Approximate wall time |
|---|---|---|---:|
| `baseline` | `28622615189` | success | `~7m03s` |
| `baseline` job only | `28622615189` | success | `~6m57s` |
| `Extension Conformance` | `28622615206` | success | `~6m25s` |
| `Fuzz CI` | `28622615217` | success | `~42m59s` |
| monolithic `ci` | `28618082382` | cancelled | `~49m25s` before cancellation |

Baseline step timings from run `28622615189`:

| Step | Wall time |
|---|---:|
| `Format gate` | `~15s` |
| `Clippy lib` | `~2m38s` |
| `Clippy bins` | `~2s` |
| `Baseline smoke test` | `~3m19s` |

Interpretation:

- the fast `baseline` concept already fits the PR budget
- `Extension Conformance` is close enough to be optional/manual if needed, but
  not required by default
- `Fuzz CI` is far outside the PR budget
- the monolithic `ci` path is not acceptable as a required PR gate

## Known Issues

## Cross-Platform / macOS

1. Bash 3 compatibility issues exist on macOS.
   - prior symptom: `mapfile: command not found`
   - implication: shell-heavy runners must either stay Bash-3-safe or move logic
     into Python

2. `just clean` was observed to fail against `target/agents/...` on one macOS
   run.
   - implication: treat `clean` as a repo behavior that needs explicit
     validation, not as a trivial wrapper

3. A `vergen-lib` build-script failure was observed during exploratory local
   runs.
   - implication: do not promise broad local `just test*` success on macOS
     until rerun on the implementation branch

## Toolchain / CI

1. Fuzz runs previously failed on `sysinfo 0.39.5` using unstable
   `cfg_select`.
   - implication: fuzz must stay outside required PR CI until nightly/toolchain
     drift is controlled

2. Historical CI used an incorrect `working-directory` path such as
   `pi_agent_rust`.
   - implication: new workflows must be path-audited from the start

3. Latest baseline failure on exploratory branch run `28624613416` was not a
   conceptual lane failure; it failed immediately at `cargo fmt --all --check`
   because exploratory source edits were not rustfmt-clean.
   - implication: the fast baseline is viable, but it must not be coupled to
     unrelated source churn

4. The old monolithic `ci` workflow mixes very cheap gates with 40+ minute
   shard jobs.
   - implication: required PR CI must be split by purpose, not just by job name

## Failure Reporting Requirements

Every `just` lane and required CI step should fail with:

- lane name
- exact underlying command
- source-of-truth file
- one next action

Examples:

- suite membership problems:
  - point to `tests/suite_classification.toml`
- smoke target definition problems:
  - point to the smoke target catalog/script
- lint lane mismatches:
  - point to `.just/lint_catalog.*`
- `verify` profile problems:
  - point to the lane catalog plus the runner entrypoint

## Implementation Constraints

- no duplicate command definitions for the same lane
- prefer data-driven catalogs over large branching `Justfile` logic
- prefer Python helpers over shell when portability or argument handling gets
  complex
- do not broaden the baseline lane until measured timings still satisfy the PR
  budget

## Review Checklist For Future Changes

When adding or changing a lane:

1. Is there exactly one source of truth for this lane?
2. Does `just explain` describe it accurately?
3. Does required PR CI call the same lane rather than a parallel shell command?
4. Is the timing recorded or updated here?
5. If it exceeds the PR budget, is it classified as optional or nightly?

## Immediate Recommendations

1. Restore `main` first via the revert PR.
2. Rebuild `just` from the `sc-just` Rust template shape, not from the entire
   exploratory branch.
3. Reintroduce only the fast baseline workflow first.
4. Keep fuzz, semver, benchmarks, and broad conformance out of required PR CI.
5. Re-measure timings on the new implementation branch and replace the
   exploratory numbers in this document once the new baseline exists.
