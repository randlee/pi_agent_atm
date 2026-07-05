---
id: A10
title: Expose Runnable Broad Test Surfaces
status: proposed
branch: sprint-a-10-expose-runnable-broad-test-surfaces
worktree: ../pi_agent_atm-worktrees/sprint-a-10-expose-runnable-broad-test-surfaces
target: sprint-a-9-measure-unit-category-coverage
---

# Sprint A10 — Expose Runnable Broad Test Surfaces

## Goal

- make broad categories visible and runnable without making them required PR
  blockers
- restore the clearer split the earlier abandoned Phase A attempt had between
  unit, integration, fuzz, benchmark, and conformance surfaces

## Hard Dependencies

- A9 unit-category evidence is published
- broad categories must be exposed through clear categories and commands, not
  buried inside one generic verify profile

## Deliverables

- authoritative mapping for:
  - `unit-full`
  - `vcr-fixture`
  - `e2e-ci-smoke`
  - `e2e-full`
  - `conformance`
  - `fuzz`
  - `benchmark`
  - `semver`
  - `model-catalog-drift`
- explicit "run now" vs "can run" status for each broad category
- updated evidence table rows for every broad category

## Acceptance Criteria

- the docs no longer force an operator to infer broad categories from
  `./verify --profile ...` comments alone
- broad categories are named in a way that matches what they actually test
- required PR CI remains unchanged unless a separate sprint explicitly changes
  it
