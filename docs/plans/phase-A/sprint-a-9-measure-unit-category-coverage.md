---
id: A9
title: Measure Unit Category Coverage
status: proposed
branch: sprint-a-9-measure-unit-category-coverage
worktree: ../pi_agent_atm-worktrees/sprint-a-9-measure-unit-category-coverage
target: sprint-a-8-publish-test-category-ledger
---

# Sprint A9 — Measure Unit Category Coverage

## Goal

- replace vague unit coverage claims with measured coverage for each unit
  category
- determine whether the current curated fast lane is maintainable enough to
  keep

## Hard Dependencies

- A8 category ledger and template are already published
- coverage must be measured per unit category rather than only for the combined
  required gate

## Deliverables

- measured local timings and coverage for:
  - `unit-inline-core`
  - `unit-curated-files`
  - `unit-curated-fast`
  - `unit-full`
- explicit maintainability assessment of `unit-curated-fast`
- updated evidence table rows for all four unit categories

## Required Table Rows To Update

- `unit-inline-core`
- `unit-curated-files`
- `unit-curated-fast`
- `unit-full`

## Acceptance Criteria

- the docs record line/function/region coverage for each measured unit
  category, or clearly explain why a category could not be measured
- the docs state whether `unit-curated-fast` should remain the required fast
  gate, be renamed, or be replaced
- the docs no longer imply that one curated fast lane represents the whole unit
  surface
