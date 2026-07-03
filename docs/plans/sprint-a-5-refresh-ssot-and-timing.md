---
id: A5
title: Refresh SSOT And Timing
status: planned
branch: sprint-a-5-refresh-ssot-and-timing
worktree: ../pi_agent_atm-worktrees/sprint-a-5-refresh-ssot-and-timing
target: develop
---

# Sprint A5 — Refresh SSOT And Timing

## Goal

- produce the team-lead review pack that freezes source-of-truth ownership and
  refreshes timing evidence without changing the established `just` command
  surface

## Hard Dependencies

- Sprint A4 merged into `develop`

## Exact Targets

- `docs/plans/phase-A/phase-A-testing-strategy.md`
- `docs/plans/phase-A/phase-A-just-ci-recovery.md`
- `docs/plans/sprint-a-1-establish-minimal-baseline-gate.md`
- `docs/plans/sprint-a-2-add-local-code-lint.md`
- `docs/plans/sprint-a-3-add-smoke-baseline.md`
- `docs/plans/sprint-a-4-add-optional-local-lanes.md`
- `docs/plans/sprint-a-5-refresh-ssot-and-timing.md`
- `docs/plans/sprint-a-6-merge-baseline-into-atm-graft.md`
- `justfile`
- `.just/lint_catalog.py`
- `.just/test_catalog.py`
- `.github/workflows/baseline.yml`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- team-lead review pack exists with frozen source-of-truth ownership and
  refreshed timing evidence against a green baseline

## Required Work

- measure actual `baseline` step timings from current green runs
- update the testing strategy doc with refreshed numbers
- update the phase doc and sprint docs if any lane names, workflow names, or
  ownership statements drifted during A1-A4
- confirm workflow YAML calls only established `just` commands
- confirm no new top-level `just` commands were introduced during A1-A4
- confirm the sprint docs still match the actual lane names and workflow names

## Explicit Code Samples

```text
baseline workflow
  -> just fmt check
  -> just lint clippy-bins
  -> just lint clippy-lib
  -> just test baseline
```

## This Sprint Does Not Close

- it does not add new required PR steps
- it does not add new top-level `just` commands
- it does not merge into `feature/atm-graft-integration`

## Acceptance Criteria

- refreshed timing evidence is recorded in the testing strategy doc
- team-lead can review SSOT ownership directly from the review-pack docs
- required `baseline` workflow is unchanged from Sprint A3
- sprint docs and testing strategy remain internally consistent after the timing refresh
- `baseline` remains green and under 10 minutes

## Required Validation

- `gh run list --workflow baseline --limit 5`
- `just fmt check`
- `just lint clippy-bins`
- `just lint clippy-lib`
- `just test baseline`
