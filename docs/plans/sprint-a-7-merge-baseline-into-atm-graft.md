---
id: A7
title: Merge Baseline Into ATM Graft
status: planned
branch: sprint-a-7-merge-baseline-into-atm-graft
worktree: ../pi_agent_atm-worktrees/sprint-a-7-merge-baseline-into-atm-graft
target: integrate/phase-A
---

# Sprint A7 — Merge Baseline Into ATM Graft

## Goal

- Merge the stabilized Phase A baseline into the `atm-graft` integration work.

## Hard Dependencies

- Sprint A6 merged into `integrate/phase-A`.
- `feature/atm-graft-integration` remains available for merge-forward work.

## Exact Targets

- `feature/atm-graft-integration`
- `integrate/phase-A`
- `tests/`
- `tests/suite_classification.toml`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- Stabilized Phase A baseline is merged into the `atm-graft` integration work
  without reintroducing monolithic PR CI.

## Required Work

- Merge Phase A baseline into the `atm-graft` integration work.
- Ensure new `atm-graft` tests are classified correctly from the start.
- Keep the fast required PR baseline intact on the merged branch.

## Explicit Code Samples

```text
merge-forward sequence:
integrate/phase-A -> sprint-a-7-* worktree
sprint-a-7-* -> integrate/phase-A
integrate/phase-A baseline -> atm-graft integration work
```

## This Sprint Does Not Close

- It does not restore monolithic PR CI.

## Acceptance Criteria

- `atm-graft` work consumes the same `just` surface.
- New `atm-graft` tests use the established suite taxonomy correctly.
- Merged branch keeps the fast required PR baseline intact.

## Required Validation

- `git merge-base feature/atm-graft-integration integrate/phase-A`
- `just explain test`
