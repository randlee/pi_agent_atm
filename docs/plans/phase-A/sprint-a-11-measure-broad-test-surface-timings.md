---
id: A11
title: Measure Broad Test Surface Timings
status: backlog
branch: sprint-a-11-measure-broad-test-surface-timings
worktree: ../pi_agent_atm-worktrees/sprint-a-11-measure-broad-test-surface-timings
target: plan/phase-A-attempt-3
---

# Sprint A11 — Measure Broad Test Surface Timings

## Goal

- attach actual or conservative timing evidence to the broad categories
- remove "unknown runtime" as a reason Phase A remains hard to evaluate
- decide which broad categories are bounded enough to belong in `long-ci`

## Hard Dependencies

- A10 category mapping is published
- each category must record either an actual timing, a capped observation, or a
  conservative estimate with a justification

## Deliverables

- updated timing evidence for:
  - `unit-full`
  - `integration-broad`
  - `vcr-fixture`
  - `e2e-ci-smoke`
  - `e2e-full`
  - `extension-sharded`
  - `parity`
  - `security`
  - `perf-benchmark`
  - `conformance-fast`
  - `fuzz`
  - `benchmark-full`
  - `semver`
  - `model-catalog-drift`
- proposed `long-ci` membership with timing justification for each included or
  excluded category
- notes identifying which categories are CI-friendly, local-only, or
  manual/scheduled only

## Acceptance Criteria

- every category row in the evidence table has a non-empty timing cell
- timing provenance is labeled as measured, capped observation, or estimate
- the plan states explicitly which categories fit inside `long-ci` and which do
  not
- long-running categories remain outside the ordinary PR required gate

## Closure Details

Close A11 only when:

- every named broad lane has a non-empty timing cell
- each timing cell is labeled as `measured`, `capped observation`, `estimate`,
  or `missing`
- the docs state whether the timing belongs to:
  - a current named lane
  - an underlying command not yet wrapped by `just`
  - or only a historical CI shard from abandoned Phase A evidence
- the `long-ci` candidate list includes timing-based inclusion and exclusion
  rationale, not only preference
