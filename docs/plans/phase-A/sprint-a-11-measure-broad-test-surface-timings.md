---
id: A11
title: Measure Broad Test Surface Timings
status: proposed
branch: sprint-a-11-measure-broad-test-surface-timings
worktree: ../pi_agent_atm-worktrees/sprint-a-11-measure-broad-test-surface-timings
target: sprint-a-10-expose-runnable-broad-test-surfaces
---

# Sprint A11 — Measure Broad Test Surface Timings

## Goal

- attach actual or conservative timing evidence to the broad categories
- remove "unknown runtime" as a reason Phase A remains hard to evaluate

## Hard Dependencies

- A10 category mapping is published
- each category must record either an actual timing, a capped observation, or a
  conservative estimate with a justification

## Deliverables

- updated timing evidence for:
  - `unit-full`
  - `vcr-fixture`
  - `e2e-ci-smoke`
  - `e2e-full`
  - `conformance`
  - `fuzz`
  - `benchmark`
  - `semver`
  - `model-catalog-drift`
- notes identifying which categories are CI-friendly, local-only, or
  manual/scheduled only

## Acceptance Criteria

- every category row in the evidence table has a non-empty timing cell
- timing provenance is labeled as measured, capped observation, or estimate
- long-running categories remain outside the ordinary PR required gate
