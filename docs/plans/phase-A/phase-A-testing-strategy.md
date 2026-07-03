# Phase A - Testing Strategy

Date: 2026-07-03
Status: proposed for team-lead review

## Purpose

Define the specific testing strategy that Phase A will implement so every
increment starts from something working, required PR CI stays under 10 minutes,
and local commands and CI share one source of truth.

## Strategy Rules

1. `just` is the only public local operator surface.
2. Required PR CI is exactly one workflow: `baseline`.
3. CI runs `just ...` commands, not bespoke cargo command strings.
4. Every sprint preserves green `baseline` CI.
5. Heavyweight workflows do not run on ordinary PRs after Sprint A1 lands.
6. Lint in required PR CI covers only code we own.
7. Broad tests, fuzz, semver, benchmarks, and evidence refresh remain outside
   required PR CI.
8. Do not invent new top-level `just` commands for Phase A. Use the established
   `just fmt`, `just lint`, `just test`, `just explain`, and `just suites`
   surfaces only.

## Final Required PR Baseline

Steady-state `baseline` contents after Sprint A4:

1. `just fmt check`
2. `just lint clippy-bins`
3. `just lint clippy-lib`
4. `just test baseline`

Hard budget:

- total wall clock under 10 minutes

Per-step budget targets:

- `just fmt check`: under 30 seconds
- `just lint clippy-bins`: under 30 seconds
- `just lint clippy-lib`: under 3 minutes
- `just test baseline`: under 4 minutes

These are budget allocations, not historical facts. Sprint validation must
measure and refresh them as each step is added.

## Incremental Rollout By Sprint

Required PR CI contents per sprint:

| Sprint | Required `baseline` contents |
|---|---|
| A1 | `just help`, `just fmt check` |
| A2 | A1 + `just lint clippy-bins`, `just lint clippy-lib` |
| A3 | A2 + `just test baseline` |
| A4 | same as A3 |
| A5 | same as A3 |
| A6 | same as A3 on merge PRs |

This table is the controlling rollout rule. If a sprint would require more
than the listed contents, the plan is being violated.

## Source Of Truth Policy

Target end state:

- `justfile` is the command surface
- `.just/lint_catalog.py` defines lint lanes
- `.just/test_catalog.py` defines test lanes
- `.just/explain.py` explains lane semantics
- `.just/show_suites.py` reports suite taxonomy from
  `tests/suite_classification.toml`
- GitHub Actions invokes only `just ...` commands

One lane, one owner:

- format lane:
  - owner: `justfile` + `.just/run_fmt.py`
- lint lane:
  - owner: `.just/lint_catalog.py`
- test lane:
  - owner: `.just/test_catalog.py`

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
- `push` to protected branches where explicitly justified

They must not run on ordinary feature PRs.

Workflow classification target after Sprint A1:

| Workflow | Ordinary PRs | Allowed remaining triggers |
|---|---|---|
| `baseline.yml` | yes | `pull_request`, optionally protected-branch `push` |
| `ci.yml` | no | `workflow_dispatch`, optional protected-branch `push` only if separately justified |
| `fuzz.yml` | no | `workflow_dispatch`, `schedule`, optional protected-branch `push` only if separately justified |
| `bench.yml` | no | `workflow_dispatch`, optional protected-branch `push` only if separately justified |
| `semver.yml` | no | `workflow_dispatch`, optional protected-branch `push` only if separately justified |

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

- `just test baseline` is a tiny deterministic smoke lane only

It must not include:

- broad `cargo test`
- full `suite.unit`
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
remain behind `just fmt`, `just lint`, `just test`, `just explain`, or `just suites`.

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

## Team-Lead Review Checklist

Team-lead approval should explicitly confirm:

- the steady-state `baseline` command list
- the per-sprint rollout table
- the decision to remove heavyweight workflows from ordinary PRs in Sprint A1
- the rule that required PR CI stays under 10 minutes in every sprint
- the SSOT owner files for lint and test lanes
- the list of local-only and manual-only lanes
- the rule that Phase A does not invent new top-level `just` commands

## Exit Criteria

The strategy is implemented when:

- required PR CI is exactly one workflow named `baseline`
- `baseline` stays under 10 minutes
- CI and local execution share the same lane definitions
- heavyweight workflows no longer run on ordinary PRs
- timing data is refreshed after each baseline expansion sprint
