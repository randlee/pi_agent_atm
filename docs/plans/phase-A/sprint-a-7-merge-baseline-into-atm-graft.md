---
id: A7
title: Merge Baseline Into Atm-Graft
status: planned
branch: sprint-a-7-merge-baseline-into-atm-graft
worktree: ../pi_agent_atm-worktrees/sprint-a-7-merge-baseline-into-atm-graft
target: feature/atm-graft-integration
---

# Sprint A7 — Merge Baseline Into Atm-Graft

## Goal

- move the verified `just` + CI baseline into the active `atm-graft`
  integration work without reintroducing abandoned exploratory code

## Hard Dependencies

- Sprint A6 merged into `develop`
- `feature/atm-graft-integration` is the active integration branch

## Unblocks

- no further Phase A sprint; this sprint hands the verified baseline to the
  active ATM integration branch

## Exact Targets

- `feature/atm-graft-integration` (`isolation: merge-target-branch`)
- `justfile` (`isolation: baseline-command-surface`)
- `.just/**` (`isolation: baseline-helper-surface`)
- `.github/workflows/baseline.yml` (`isolation: required-pr-workflow-sync`)
- `Cargo.toml` (`isolation: atm-dependency-wiring-surface`)
- `vendor/atm-daemon-bootstrap-shim/**` (`isolation: atm-shim-surface`)
- any additional merge-conflict files Git reports during the forward merge
  (`isolation: merge-conflict-surface`)

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- verified baseline merges into `feature/atm-graft-integration` and stays green

## Required Work

- merge the corrected Phase A baseline forward from `develop`
- resolve conflicts without pulling exploratory `feature/just-integration`
  source churn back in
- keep `baseline` as the required PR workflow on the merged branch
- preserve the same lane names and SSOT ownership on the merged branch
- preserve the future ATM layering boundaries so
  `feature/atm-graft-integration` can keep its root dependency wiring to
  `atm-core` crates and bounded local shim/glue surfaces without redefining the
  upstream baseline lanes
- preserve the existing `atm-graft`, `atm_core`, and
  `atm-daemon-bootstrap-shim` dependency/glue surfaces while merging the Phase A
  baseline

## Explicit Code Samples

```text
develop
  -> sprint-a-1
  -> sprint-a-2
  -> sprint-a-3
  -> sprint-a-4
  -> sprint-a-5
  -> sprint-a-6
  -> feature/atm-graft-integration
```

```text
merge surfaces to preserve
  -> Cargo.toml: atm-graft + atm_core dependency wiring
  -> vendor/atm-daemon-bootstrap-shim/Cargo.toml
  -> baseline just/CI files from develop
```

## This Sprint Does Not Close

- it does not add new `atm-graft`-specific test lanes
- it does not expand required PR CI beyond the established `baseline`

## Acceptance Criteria

- `feature/atm-graft-integration` contains the verified `just` + CI baseline
- merge resolution does not restore abandoned exploratory `src/**` changes
- `baseline` remains the required PR workflow
- the merged branch keeps the same `just fmt`, `just lint`, and `just test baseline`
  surface defined in Phase A, including `just test compile` and
  `just test unit-basic`
- the merge keeps a clean additive path for future ATM-owned crates and
  integration lanes
- the merge preserves the existing `atm-graft`, `atm_core`, and vendor shim
  integration surfaces
- `baseline` remains green and under 10 minutes

## Required Validation

- `just fmt check`
- `just test compile`
- `just test unit-basic`
- `just lint clippy-bins`
- `just lint clippy-lib`
- `just test baseline`
- `rg -n \"atm-graft|atm_core|atm-daemon-bootstrap\" Cargo.toml vendor/atm-daemon-bootstrap-shim/Cargo.toml`
- `gh run list --workflow baseline --limit 5`
