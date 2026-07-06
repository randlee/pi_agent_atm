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
- split "unit tests" into meaningful deterministic sub-buckets instead of only
  `unit-basic` versus `unit-full`

## Hard Dependencies

- A8 category ledger and template are already published
- `phase-A-test-lane-report-template.md` is the report surface to update
- coverage must be measured per unit category rather than only for the combined
  required gate

## Deliverables

- measured local timings and coverage for:
  - `unit-basic`
  - `unit-inline-core`
  - `unit-app-logic`
  - `unit-infra-tooling`
  - `unit-security-policy`
  - `unit-perf-policy`
  - `unit-contract-parity`
  - `unit-curated-files`
  - `unit-curated-fast`
  - `unit-full`
- explicit maintainability assessment of `unit-curated-fast`
- explicit statement of overlap:
  - what `unit-basic` covers
  - what `unit-full` covers
  - which sub-buckets overlap the fast gate
- updated evidence table rows and unit-breakdown rows for the measured unit
  surfaces

## Required Table Rows To Update

- `unit-basic`
- `unit-inline-core`
- `unit-app-logic`
- `unit-infra-tooling`
- `unit-security-policy`
- `unit-perf-policy`
- `unit-contract-parity`
- `unit-curated-files`
- `unit-curated-fast`
- `unit-full`

## Acceptance Criteria

- the docs record line/function/region coverage for each measured unit
  category, or clearly explain why a category could not be measured
- the docs record the overlap between `unit-basic` and `unit-full` explicitly
- the docs state whether `unit-curated-fast` should remain the required fast
  gate, be renamed, or be replaced
- the docs no longer imply that one curated fast lane represents the whole unit
  surface
- the docs acknowledge that parts of `[suite.unit]` are infrastructure,
  tooling, security-policy, perf-policy, or contract/parity tests rather than
  only app-logic tests
