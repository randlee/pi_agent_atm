---
id: A12
title: Finalize Required Vs Runnable Gate
status: proposed
branch: sprint-a-12-finalize-required-vs-runnable-gate
worktree: ../pi_agent_atm-worktrees/sprint-a-12-finalize-required-vs-runnable-gate
target: sprint-a-11-measure-broad-test-surface-timings
---

# Sprint A12 — Finalize Required Vs Runnable Gate

## Goal

- freeze the final required-vs-runnable split for Phase A
- define the final multi-platform required gate and the broader runnable
  categories that remain outside it

## Hard Dependencies

- A8-A11 evidence table is complete enough to compare required and runnable
  categories honestly

## Deliverables

- final required gate definition
- final runnable-but-not-required category list
- final multi-platform measurement requirement for the required gate
- final ATM regression framework handoff:
  - upstream baseline categories
  - ATM-owned categories
  - seam/integration categories

## Acceptance Criteria

- the final plan makes the required gate understandable in one table
- the final plan makes the runnable broader surface understandable in one table
- the docs state clearly which categories protect the upstream fork, which
  categories are broader confidence surfaces, and which categories should later
  protect ATM-owned code
