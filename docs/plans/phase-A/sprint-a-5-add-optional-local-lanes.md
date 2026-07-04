---
id: A5
title: Add Optional Local Lanes
status: planned
branch: sprint-a-5-add-optional-local-lanes
worktree: ../pi_agent_atm-worktrees/sprint-a-5-add-optional-local-lanes
target: develop
---

# Sprint A5 — Add Optional Local Lanes

## Goal

- expose richer local-only operator lanes while freezing required PR CI

## Hard Dependencies

- Sprint A4 merged into `develop`

## Exact Targets

- `justfile`
- `.just/lint_catalog.py`
- `.just/test_catalog.py`
- `.just/explain.py`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- optional local lanes exist without changing required PR CI

## Required Work

- add optional local lanes such as `just test unit`, `just test integration`,
  `just test all`, and `just lint all-local`
- reserve explicit naming room for future `atm-*` and `integration-*` lanes
  without changing the established upstream baseline lane ids
- route lane descriptions through the established helper surfaces from Sprint A4
- keep required `baseline` contents exactly as Sprint A3 defined them

Reuse sources:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/lint_catalog.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/test_catalog.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/explain.py`

## Explicit Code Samples

```python
DISPLAY_ORDER = ("baseline", "unit", "integration", "all")
```

## This Sprint Does Not Close

- it does not change required PR CI contents
- it does not reintroduce heavyweight PR workflows
- it does not invent a new top-level `just` command

## Acceptance Criteria

- optional local lanes are documented and callable
- optional local lanes are clearly marked as non-required in docs and lane help
- any new ATM-owned or integration lane shape is classified as optional unless
  separately promoted by evidence and review
- required `baseline` workflow is unchanged from Sprint A3
- `baseline` remains green and under 10 minutes

## Required Validation

- `just explain test unit`
- `just test unit`
- `just test integration`
- `just lint all-local`
- `gh workflow view baseline`
