---
id: A6
title: Classify Long-Running Workflows
status: planned
branch: sprint-a-6-classify-long-running-workflows
worktree: ../pi_agent_atm-worktrees/sprint-a-6-classify-long-running-workflows
target: integrate/phase-A
---

# Sprint A6 — Classify Long-Running Workflows

## Goal

- Classify every remaining non-baseline workflow as optional PR, manual, or
  nightly/scheduled, and document why it exists.

## Hard Dependencies

- Sprint A5 merged into `integrate/phase-A`.

## Exact Targets

- `.github/workflows/`
- `docs/plans/phase-A/phase-A-just-ci-recovery.md`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- Complete workflow-classification inventory exists for every non-baseline CI
  surface.

## Required Work

- Inventory every workflow under `.github/workflows/`.
- Classify each as:
  - optional PR
  - manual
  - nightly/scheduled
- Record the runtime reason each surviving workflow exists.
- Record local-command mapping where applicable.

## Explicit Code Samples

No code samples required for this sprint.

## This Sprint Does Not Close

- It does not expand required PR CI budget.

## Acceptance Criteria

- Every surviving workflow has an explicit classification.
- Every surviving workflow has a written reason to exist.
- Long-running lanes are not required PR gates by default.
- Local command mapping exists where applicable, or the absence is documented
  intentionally.

## Required Validation

- `find .github/workflows -maxdepth 1 -type f | sort`
