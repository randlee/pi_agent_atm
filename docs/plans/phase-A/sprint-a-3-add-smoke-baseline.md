---
id: A3
title: Add Smoke Baseline
status: planned
branch: sprint-a-3-add-smoke-baseline
worktree: ../pi_agent_atm-worktrees/sprint-a-3-add-smoke-baseline
target: develop
---

# Sprint A3 — Add Smoke Baseline

## Goal

- add one tiny deterministic regression test lane through the established
  `just test` surface

## Hard Dependencies

- Sprint A2 merged into `develop`

## Exact Targets

- `justfile`
- `.just/run_test.py`
- `.just/test_catalog.py`
- `scripts/smoke.sh`
- `.github/workflows/baseline.yml`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- `just test baseline` exists and is wired into required PR CI

## Required Work

- reuse or narrow `run_test.py`
- define one smoke lane in `test_catalog.py`
- keep the smoke lane deterministic and non-destructive
- ensure the smoke lane does not expand into broad `cargo test`, VCR, or E2E
  work

Reuse sources:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_test.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/test_catalog.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/scripts/smoke.sh`

## Explicit Code Samples

```python
LANES = {
    "baseline": TestLane(
        name="baseline",
        kind="script",
        script_args=("./scripts/smoke.sh", "--skip-lint", "--no-rch"),
    ),
}
```

```yaml
steps:
  - run: just help
  - run: just fmt check
  - run: just lint clippy-bins
  - run: just lint clippy-lib
  - run: just test baseline
```

## This Sprint Does Not Close

- it does not add `just test unit`
- it does not add `just test integration`
- it does not invent a new top-level `just` command

## Acceptance Criteria

- `just test baseline` works
- required PR CI runs the smoke lane through the established `just test`
  surface
- smoke failures report lane name, command, SSOT file, and next action
- smoke coverage remains materially smaller than `just test unit` and `just test integration`
- `baseline` remains green and under 10 minutes

## Required Validation

- `just fmt check`
- `just lint clippy-bins`
- `just lint clippy-lib`
- `just test baseline`
- `gh run list --workflow baseline --limit 5`
