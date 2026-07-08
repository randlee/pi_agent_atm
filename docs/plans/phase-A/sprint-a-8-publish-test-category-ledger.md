---
id: A8
title: Publish Test Category Ledger
status: backlog
branch: sprint-a-8-publish-test-category-ledger
worktree: ../pi_agent_atm-worktrees/sprint-a-8-publish-test-category-ledger
target: plan/phase-A-attempt-3
---

# Sprint A8 — Publish Test Category Ledger

## Goal

- replace ambiguous lane-centric language with a category ledger you can read
  quickly
- establish the evidence table template that every later sprint must update

## Hard Dependencies

- A1-A7 are treated as historical evidence only
- this sprint is docs-first and may not claim implementation proof it did not
  measure

## Deliverables

- `phase-A-testing-strategy.md` contains the authoritative test category matrix
- `phase-A-testing-strategy.md` contains the reusable sprint evidence table
  template
- `phase-A-test-lane-report-template.md` exists as the reusable fill-in
  artifact for sprint and phase reports
- `phase-A-current-evidence-report.md` exists as the filled current-state
  evidence artifact
- `phase-A-just-ci-recovery.md` treats A8-A12 as documentation backlog that
  hardens the main plan rather than as a new mandatory engineering sprint chain
- the unit surface is explicitly split into:
  - `unit-inline-core`
  - `unit-curated-files`
  - `unit-curated-fast`
  - `unit-full`

## Required Table Rows To Update

- `compile-check`
- `unit-inline-core`
- `unit-curated-files`
- `unit-curated-fast`
- `smoke-baseline`
- `unit-full`
- `vcr-fixture`
- `e2e-ci-smoke`
- `e2e-full`
- `conformance`
- `fuzz`
- `benchmark`
- `semver`
- `model-catalog-drift`

## Acceptance Criteria

- the docs answer both questions directly:
  - what runs now on ordinary PRs
  - what can be run outside the required gate
- the report template includes lane, timing, coverage, and CI-eligibility
  columns for every named lane
- `unit-basic` is no longer treated as if it were the full unit-test category
- unknown timings or coverage values are explicitly marked as missing or
  estimated rather than implied

## Closure Details

Close A8 only when:

- `phase-A-current-evidence-report.md` exists
- the evidence table has no silent blank cells in the rows A8 owns
- A8-A12 are described consistently as planning-branch documentation backlog
  items, not as a conflicting live execution branch stack
- every unknown row is labeled `missing`, `estimated`, `partial`, or
  `not implemented` instead of being left ambiguous
