---
id: A5
title: Add Optional Local Lanes
status: complete
branch: sprint-a-5-add-optional-local-lanes
worktree: ../pi_agent_atm-worktrees/sprint-a-5-add-optional-local-lanes
target: sprint-a-4-add-taxonomy-helpers
---

# Sprint A5 — Add Optional Local Lanes

## Goal

- expose richer local-only operator lanes while freezing required PR CI

## Hard Dependencies

- Sprint A4 merged forward from `sprint-a-4-add-taxonomy-helpers`

## Unblocks

- Sprint A6 review-pack validation depends on A5 locking the optional local
  lane names and their non-required classification

## Exact Targets

- `justfile` (`isolation: baseline-command-surface`)
- `.just/lint_catalog.py` (`isolation: optional-lint-lane-surface`)
- `.just/test_catalog.py` (`isolation: optional-test-lane-surface`)
- `.just/explain.py` (`isolation: helper-output-sync`)

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- the exact optional local lanes added in this sprint exist without changing
  required PR CI:
  - `just test unit`
  - `just test integration`
  - `just test all`
  - `just lint all-local`

## Required Work

- add these exact optional local lanes:
  - `just test unit`
  - `just test integration`
  - `just test all`
  - `just lint all-local`
- reserve explicit naming room for future `atm-*` and `integration-*` lanes
  without changing the established upstream baseline lane ids
- route lane descriptions through the established helper surfaces from Sprint A4
- keep required `baseline` contents exactly as Sprint A3 defined them
- do not add `just test vcr` or `just test e2e` in this sprint

Reuse sources:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/lint_catalog.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/test_catalog.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/explain.py`

## Explicit Code Samples

```python
DISPLAY_ORDER = ("baseline", "unit", "integration", "all")
OPTIONAL_LANES = ("unit", "integration", "all", "all-local")
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
- this sprint adds exactly `just test unit`, `just test integration`,
  `just test all`, and `just lint all-local`
- this sprint does not add `just test vcr` or `just test e2e`
- required `baseline` workflow is unchanged from Sprint A3
- `baseline` remains green and under 10 minutes

## Required Validation

- `just explain test unit`
- `just test unit`
- `just test integration`
- `just test all`
- `just lint all-local`
- `gh workflow view baseline`
