---
id: A2
title: Add Local-Code Lint
status: open
branch: sprint-a-2-add-local-code-lint
worktree: ../pi_agent_atm-worktrees/sprint-a-2-add-local-code-lint
target: sprint-a-1-establish-minimal-baseline-gate
---

# Sprint A2 — Add Local-Code Lint

## Goal

- add only the local-code lint lanes needed for required PR CI through the
  established `just lint` surface

## Hard Dependencies

- A2 must branch from the last proven A1 replay state, not from stale
  historical branch state

## Unblocks

- Sprint A3 can add smoke only after the final required lint ordering is fixed
- A5 optional local lint expansion depends on A2 defining the required lint
  lane contract first

## Exact Targets

- `justfile` (`isolation: baseline-command-surface`)
- `.just/run_cargo.py` (`isolation: reused-helper-surface`)
- `.just/run_lint.py` (`isolation: required-lint-lane-surface`)
- `.just/lint_catalog.py` (`isolation: required-lint-lane-surface`)
- `.github/workflows/baseline.yml` (`isolation: required-pr-workflow-edit`)

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- `just lint clippy-bins` exists with an exact local-code command contract and
  is wired into `baseline`
- `just lint clippy-lib` exists with an exact local-code command contract and
  is wired into `baseline`
- the Sprint A2 PR notes include a timing table with local wall-clock and CI
  wall-clock measurements for the full A2 baseline command set and total
  `baseline` workflow duration

## Required Work

- reuse `run_cargo.py`, `run_lint.py`, and `lint_catalog.py`
- define only the required local-code lint lanes first
- define the exact commands as:
  - `just lint clippy-bins` -> `cargo clippy --no-deps --bins -- -D warnings`
  - `just lint clippy-lib` -> `cargo clippy --no-deps --lib -- -D warnings`
- update `baseline.yml` to run the lint lanes after formatting
- preserve required ordering:
  - `just help`
  - `just fmt check`
  - `just test compile`
  - `just test unit-basic`
  - `just lint clippy-bins`
  - `just lint clippy-lib`
- keep dependency lint and test-target lint out of required PR CI
- keep lint ordering cheap-to-expensive: bins before lib

Reuse sources:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_cargo.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_lint.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/lint_catalog.py`

## Explicit Code Samples

```python
LANES = {
    "clippy-bins": LintLane(command=("cargo", "clippy", "--no-deps", "--bins", "--", "-D", "warnings")),
    "clippy-lib": LintLane(command=("cargo", "clippy", "--no-deps", "--lib", "--", "-D", "warnings")),
}
```

```yaml
steps:
  - run: just help
  - run: just fmt check
  - run: just test compile
  - run: just test unit-basic
  - run: just lint clippy-bins
  - run: just lint clippy-lib
```

## This Sprint Does Not Close

- it does not add smoke testing
- it does not add optional local lanes
- it does not invent a new top-level `just` command

## Acceptance Criteria

- `just lint clippy-bins` exits 0 and runs the exact documented bins-only
  command contract
- `just lint clippy-lib` exits 0 and runs the exact documented lib-only
  command contract
- required `baseline` workflow runs only the established lint surface
- required `baseline` workflow preserves the exact command ordering defined in
  this sprint doc
- required PR CI does not add `clippy --tests`, `clippy --benches`, or
  `clippy --examples`
- `baseline` remains green and under 10 minutes
- no new PR-required workflow is introduced
- the Sprint A2 PR notes record local and CI timings for the A2 baseline stage
- the Sprint A2 PR notes record the exact CI run URL/ID used for each timing
  measurement

## Required Validation

- `just help`
- `just fmt check`
- `just test compile`
- `just test unit-basic`
- `just lint clippy-bins`
- `just lint clippy-lib`
- verify `baseline.yml` orders the lint lanes after `just test unit-basic`
- `gh workflow view baseline`
- `gh run list --workflow baseline --limit 5`
- record local timings for the full A2 baseline command set through
  `just lint clippy-lib`
- record CI step timings and total `baseline` workflow duration from the A2 run
