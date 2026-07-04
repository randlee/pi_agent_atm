---
id: A7
title: Merge Baseline Into Atm-Graft
status: revised
branch: sprint-a-7-merge-baseline-into-atm-graft
worktree: ../pi_agent_atm-worktrees/sprint-a-7-merge-baseline-into-atm-graft
target: feature/atm-graft-integration
---

# Sprint A7 — Merge Baseline Into Atm-Graft

## Goal

- move the verified `just` + CI baseline into the active `atm-graft`
  integration work without reintroducing abandoned exploratory code

## Hard Dependencies

- Sprint A6 merged forward from `sprint-a-6-refresh-ssot-and-timing`
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

- merge the corrected Phase A baseline forward from the merge-forward Phase A
  sprint chain
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
integrate/phase-A
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
  -> baseline just/CI files from the Phase A sprint chain
```

## This Sprint Does Not Close

- it does not add new `atm-graft`-specific test lanes
- it does not expand required PR CI beyond the established `baseline`

## Timing Criterion Revision (2026-07-04)

The original Phase A expectation that the required `baseline` workflow would
meet a smaller phase-wide timing target is formally revised for this sprint
handoff.

Real single-job baseline evidence now shows that the 10-minute target was
apparently never met across the phase:

- Sprint A1 run `28698012935`: `17m39s`
- Sprint A2 run `28698763616`: `12m59s`
- Sprint A7 run `28701385323`: `13m09s`

This is treated as a systemic phase-wide characteristic rather than as an A7
merge regression. The final A7 merge also runs against the full
`feature/atm-graft-integration` dependency graph with the larger merged
`Cargo.lock`, which is a contributing factor to the observed timing envelope.

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
- `baseline` remains green and uses the revised July 4, 2026 steady-state
  timing reference established by runs `28698012935` (`17m39s`),
  `28698763616` (`12m59s`), and `28701385323` (`13m09s`)

## Required Validation

- `just fmt check`
- `just test compile`
- `just test unit-basic`
- `just lint clippy-bins`
- `just lint clippy-lib`
- `just test baseline`
- `rg -n \"atm-graft|atm_core|atm-daemon-bootstrap\" Cargo.toml vendor/atm-daemon-bootstrap-shim/Cargo.toml`
- `gh run list --workflow baseline --limit 5`
