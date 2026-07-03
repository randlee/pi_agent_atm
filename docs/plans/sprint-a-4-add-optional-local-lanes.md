---
id: A4
title: Add Optional Local Lanes
status: planned
branch: sprint-a-4-add-optional-local-lanes
worktree: ../pi_agent_atm-worktrees/sprint-a-4-add-optional-local-lanes
target: develop
---

# Sprint A4 — Add Optional Local Lanes

## Goal

- expose richer local-only operator lanes while freezing required PR CI

## Hard Dependencies

- Sprint A3 merged into `develop`

## Exact Targets

- `justfile`
- `.just/lint_catalog.py`
- `.just/test_catalog.py`
- `.just/explain.py`
- `.just/show_suites.py`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- optional local lanes and taxonomy helpers exist without changing required PR
  CI

## Required Work

- add `just explain`
- add `just suites`
- add optional local lanes such as `just test unit`, `just test integration`,
  and `just lint all-local`
- keep required `baseline` contents exactly as Sprint A3 defined them

Reuse sources:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/explain.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/show_suites.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/lint_catalog.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/test_catalog.py`

## Explicit Code Samples

```just
explain domain='' lane='':
    {{python_cmd}} .just/explain.py {{domain}} {{lane}}

suites:
    {{python_cmd}} .just/show_suites.py
```

```python
DISPLAY_ORDER = ("baseline", "unit", "integration")
```

## This Sprint Does Not Close

- it does not change required PR CI contents
- it does not reintroduce heavyweight PR workflows
- it does not invent a new top-level `just` command

## Acceptance Criteria

- `just explain` works
- `just suites` works
- optional local lanes are documented and callable
- optional local lanes are clearly marked as non-required in docs and lane help
- required `baseline` workflow is unchanged from Sprint A3
- `baseline` remains green and under 10 minutes

## Required Validation

- `just explain lint clippy-lib`
- `just suites`
- `just test unit`
- `just test integration`
- `gh workflow view baseline`
- `gh run list --workflow baseline --limit 5`
