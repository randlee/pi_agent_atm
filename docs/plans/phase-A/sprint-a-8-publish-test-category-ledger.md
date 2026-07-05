---
id: A8
title: Publish Test Category Ledger
status: proposed
branch: sprint-a-8-publish-test-category-ledger
worktree: ../pi_agent_atm-worktrees/sprint-a-8-publish-test-category-ledger
target: integrate/phase-A
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
- `phase-A-just-ci-recovery.md` names A8-A12 as the active continuation plan
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
- `unit-basic` is no longer treated as if it were the full unit-test category
- unknown timings or coverage values are explicitly marked as missing or
  estimated rather than implied
