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

## Unblocks

- Sprint A4 helper output can freeze around the final required baseline only
  after A3 locks the smoke lane shape
- Sprint A6 timing review depends on A3 defining the final required PR command
  list

## Exact Targets

- `justfile` (`isolation: baseline-command-surface`)
- `.just/run_test.py` (`isolation: required-test-lane-surface`)
- `.just/test_catalog.py` (`isolation: required-test-lane-surface`)
- `scripts/smoke.sh` (`isolation: required-smoke-script-surface`)
- `.github/workflows/baseline.yml` (`isolation: required-pr-workflow-edit`)

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- `just test baseline` exists and is wired into required PR CI
- the initial smoke scope is explicit and excludes these broader local test
  surfaces: `just test unit`, `just test integration`, VCR, and E2E

## Required Work

- reuse or narrow `run_test.py`
- define one smoke lane in `test_catalog.py`
- keep the smoke lane deterministic and non-destructive
- keep the initial smoke target list exactly:
  - `model_serialization`
  - `config_precedence`
  - `session_conformance`
  - `error_types`
  - `compaction`
  - `security_budgets`
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
        documented_targets=(
            "model_serialization",
            "config_precedence",
            "session_conformance",
            "error_types",
            "compaction",
            "security_budgets",
        ),
    ),
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
  - run: just test baseline
```

## This Sprint Does Not Close

- it does not add `just test unit`
- it does not add `just test integration`
- it does not invent a new top-level `just` command

## Acceptance Criteria

- `just test baseline` exits 0 and runs only the documented six-target smoke
  starter set
- required PR CI runs the smoke lane through the established `just test`
  surface
- smoke failures report lane name, command, SSOT file, and next action
- smoke coverage remains exactly the documented six-target starter set unless
  the sprint doc is separately revised
- smoke coverage excludes `just test unit`, `just test integration`, VCR, and
  E2E coverage
- `baseline` remains green and under 10 minutes

## Required Validation

- `just fmt check`
- `just test compile`
- `just test unit-basic`
- `just lint clippy-bins`
- `just lint clippy-lib`
- `just test baseline`
- verify `scripts/smoke.sh` still excludes VCR and E2E coverage from the
  required PR lane
- `gh run list --workflow baseline --limit 5`
