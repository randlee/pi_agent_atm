---
id: A4
title: Add Taxonomy Helpers
status: planned
branch: sprint-a-4-add-taxonomy-helpers
worktree: ../pi_agent_atm-worktrees/sprint-a-4-add-taxonomy-helpers
target: develop
---

# Sprint A4 — Add Taxonomy Helpers

## Goal

- expose taxonomy helpers while freezing required PR CI

## Hard Dependencies

- Sprint A3 merged into `develop`

## Exact Targets

- `justfile`
- `.just/explain.py`
- `.just/show_suites.py`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- taxonomy helpers exist without changing required PR CI

## Required Work

- add `just explain`
- add `just suites`
- make `just explain` surface lane origin, owner, blocking level, and source of
  truth so future ATM-owned lanes can reuse the same taxonomy
- keep required `baseline` contents exactly as Sprint A3 defined them

Reuse sources:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/explain.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/show_suites.py`

## Explicit Code Samples

```just
explain domain='' lane='':
    {{python_cmd}} .just/explain.py {{domain}} {{lane}}

suites:
    {{python_cmd}} .just/show_suites.py
```

## This Sprint Does Not Close

- it does not change required PR CI contents
- it does not reintroduce heavyweight PR workflows
- it does not invent a new top-level `just` command
- it does not add optional local lanes

## Acceptance Criteria

- `just explain` works
- `just suites` works
- taxonomy helper output points operators to the SSOT lane and suite surfaces
- taxonomy helper output distinguishes upstream baseline lanes from future
  ATM-owned and integration lanes
- required `baseline` workflow is unchanged from Sprint A3
- `baseline` remains green and under 10 minutes

## Required Validation

- `just explain lint clippy-lib`
- `just suites`
- `gh workflow view baseline`
- `gh run list --workflow baseline --limit 5`
