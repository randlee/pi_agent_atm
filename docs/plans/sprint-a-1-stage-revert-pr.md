---
id: A1
title: Stage Revert PR
status: planned
branch: sprint-a-1-stage-revert-pr
worktree: ../pi_agent_atm-worktrees/sprint-a-1-stage-revert-pr
target: main
---

# Sprint A1 — Stage Revert PR

## Goal

- Create the reviewable revert PR and hold it unmerged so it is ready to be the
  first execution step after Phase A planning completes.

This is a pre-integration gating sprint. It does not merge into
`integrate/phase-A`.

## Hard Dependencies

- Draft revert branch `fix/revert-unauthorized-main-20260702` exists.

## Exact Targets

- `fix/revert-unauthorized-main-20260702`
- GitHub PR metadata for `fix/revert-unauthorized-main-20260702`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- Reviewable draft PR exists for the unauthorized direct commits and is clearly
  documented as "do not merge until planning and salvage review are complete."

## Required Work

- Push `fix/revert-unauthorized-main-20260702`.
- Open draft PR against `main`.
- State explicitly in the PR body that:
  - planning completes first
  - leaked changes are reviewed for salvage value before merge
  - this is a history-preserving revert, not a force-push rewrite

## Explicit Code Samples

No code samples required for this sprint.

## This Sprint Does Not Close

- It does not merge the revert PR.
- It does not decide which leaked changes should be reintroduced later.

## Acceptance Criteria

- Draft PR exists for `fix/revert-unauthorized-main-20260702` -> `main`.
- PR body names the five reverted commits.
- PR body states that the revert must remain unmerged until planning is
  complete and leaked changes have been reviewed for salvage value.

## Required Validation

- `gh pr view --json number,title,isDraft,baseRefName,headRefName,url`
- `git log --oneline main..fix/revert-unauthorized-main-20260702`
