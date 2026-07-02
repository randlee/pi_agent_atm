# Just Verification Log (macOS)

Date: July 1, 2026
Branch: `feature/just-integration`
Branch tip at time of log: `cbce0310`
Host: macOS arm64
Shell baseline: `GNU bash, version 3.2.57(1)-release`

## Purpose

This log records the current state of the `just` command surface on macOS so we
can separate:

- command-surface problems
- macOS-specific portability problems
- deeper repo/build/test failures unrelated to the `just` layout

## Successful Basic Commands

These completed successfully on this macOS host:

| Command | Result | Notes | Observed wall time |
|---|---|---|---:|
| `just help` | PASS | Help surface renders correctly from `.just/print_help.py` | `<1s` |
| `just suites` | PASS | Suite taxonomy renders correctly from shared catalog-backed loader | `<1s` |
| `just lint fmt` | PASS | Full lint subtarget dispatch works for the format lane | `61.79s` |
| `just fmt check` | PASS | Direct format gate works | `13.32s` |

Observed bounded timings from isolated lint runs:

| Command | Observed wall time | End state |
|---|---:|---|
| `just lint fmt` | `61.79s` | completed successfully |
| `just lint check` | `120.03s` | timed out while still compiling/checking |
| `just lint clippy` | `120.02s` | timed out while still compiling/checking |
| `just lint` | `120.06s` | timed out after format lane passed and while clippy/check work was still running |

## Commands That Currently Reach Real Work

These no longer fail at `just` dispatch time. They enter the shared runner and
start real build/verification work:

| Command | Current state |
|---|---|
| `just test unit` | Enters `./verify --profile quick --skip-lint` and begins target compilation |
| `just test integration` | Enters `./verify --profile ci --skip-lint --skip-e2e` and begins target compilation |
| `just test` | Enters `./verify --profile ci --skip-lint` and begins target compilation |
| `just test all` | Enters `./verify --profile full --skip-lint` and begins target compilation |

Observed bounded timings from isolated runs:

| Command | Observed wall time | End state |
|---|---:|---|
| `just test unit` | `120.03s` | timed out while still building |
| `just test integration` | `120.04s` | timed out while still building |
| `just test` | `120.02s` | timed out while still building |
| `just test all` | `120.02s` | timed out while still building |

These are lower bounds, not completion times.

## Timing Estimates

Current estimates on this macOS host:

| Command | Estimate |
|---|---|
| `just test` | More than 2 minutes even before the current build blocker is resolved |
| `just test all` | More than 2 minutes to get through startup/build phase; likely much longer once the full 262 non-E2E targets plus 39 E2E suites run to completion |

Notes:

- The only prior in-tree suite duration artifact that was easy to reuse here was
  one historical summary with `duration_ms = 47863` for a single suite, which
  is roughly `47.86s` for that one suite.
- That is not enough to produce a trustworthy full-suite completion forecast, so
  the current estimate for `just test all` is intentionally conservative rather
  than pretending to be precise.

## Confirmed macOS-Specific Portability Bug

### Fixed

1. `scripts/e2e/run_all.sh` used Bash `mapfile`, which is unavailable in the
   system Bash shipped on macOS (`bash 3.2`).

Observed symptom before fix:

```text
scripts/e2e/run_all.sh: line 172: mapfile: command not found
```

Impact:

- Broke every `just test*` path on macOS before any real verification work began.

Status:

- Fixed in branch commit `cbce0310` by removing the Bash 4+ dependency from the
  shared verification runner.

## Bugs Observed On macOS (scope not yet proven)

1. `vergen-lib` build script failure during the shared Rust build path:

```text
error[E0428]: the name 'nightly' is defined multiple times
.../vergen-lib-9.1.0/build.rs:13:1
```

Current assessment:

- Observed consistently on this macOS host across the `just test*` family.
- Not yet proven macOS-specific.
- Likely a deeper toolchain/dependency interaction rather than a `just` surface
  problem.

Impact:

- Blocks successful completion of `just test`, `just test ci`,
  `just test integration`, `just test integrate`, `just test all`,
  `just test full`, `just test vcr`, and `just test e2e`.

2. `just clean` failure after agent-created target trees were active or partially
   removed:

```text
error: IO error for operation on .../target/agents/.../debug/deps/...: No such file or directory
```

Current assessment:

- Reproduced on this macOS host in a single-process run of `just clean`.
- The failing path was under `target/agents/...`, so the problem still appears
  related to the shared agent target tree or stale Cargo clean metadata.
- Not yet proven macOS-specific.

Impact:

- Makes `just clean` unreliable even after prior agent/background Cargo work has
  already finished.

Observed failure timing:

| Command | Observed wall time | End state |
|---|---:|---|
| `just clean` | `65.73s` | failed with `No such file or directory` while cleaning `target/agents/...` |

## Interpretation

The current `just` structure itself is in acceptable shape:

- command naming matches the intended cross-repo pattern better
- test-lane definitions now come from a single source of truth
- the macOS-specific Bash portability failure in the shared runner is fixed

The remaining failures are no longer command-surface failures. They are deeper
build/test/runtime issues that happen after the `just` dispatch layer has already
worked correctly.
