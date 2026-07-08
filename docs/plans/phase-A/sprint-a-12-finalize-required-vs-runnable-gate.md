---
id: A12
title: Finalize Required Vs Runnable Gate
status: backlog
branch: sprint-a-12-finalize-required-vs-runnable-gate
worktree: ../pi_agent_atm-worktrees/sprint-a-12-finalize-required-vs-runnable-gate
target: plan/phase-A-attempt-3
---

# Sprint A12 — Finalize Required Vs Runnable Gate

## Goal

- freeze the final required-vs-runnable split for Phase A
- define the final multi-platform required gate and the broader runnable
  categories that remain outside it
- freeze the final `long-ci` set separately from the ordinary PR baseline

## Hard Dependencies

- A8-A11 evidence table is complete enough to compare required and runnable
  categories honestly

## Deliverables

- final required gate definition
- final `long-ci` definition
- final runnable-but-not-required category list
- final multi-platform measurement requirement for the required gate
- final ATM regression framework handoff:
  - upstream baseline categories
  - ATM-owned categories
  - seam/integration categories

## Acceptance Criteria

- the final plan makes the required gate understandable in one table
- the final plan makes the runnable broader surface and `long-ci` set
  understandable in one table
- the docs state clearly which categories protect the upstream fork, which
  categories are broader confidence surfaces, and which categories should later
  protect ATM-owned code

## Closure Details

Close A12 only when:

- one table shows the final required baseline lanes and their coverage and
  timing story
- one table shows the final runnable broader surfaces and whether they are
  `long-ci`, local-only, or manual/scheduled
- the phase closeout rules require Linux, macOS, and Windows timing evidence
  for the merged required gate
- the docs explain how future ATM-owned crates layer on top of:
  - upstream baseline regression lanes
  - ATM-owned lanes
  - seam or integration lanes
- the plan says explicitly that no code lands on `develop` or
  `integrate/phase-A` without the evidence package the phase defines
