---
id: A5
title: Reduce Required PR CI To Baseline
status: planned
branch: sprint-a-5-reduce-required-pr-ci-to-baseline
worktree: ../pi_agent_atm-worktrees/sprint-a-5-reduce-required-pr-ci-to-baseline
target: integrate/phase-A
---

# Sprint A5 — Reduce Required PR CI To Baseline

## Goal

- Replace the required PR CI surface with one bounded fast `baseline` workflow.

## Hard Dependencies

- Sprint A4 merged into `integrate/phase-A`.

## Exact Targets

- `.github/workflows/baseline.yml`
- `.github/workflows/ci.yml`
- `.just/`
- `feature/just-integration:.github/workflows/baseline.yml`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- Required PR CI is reduced to one fast `baseline` workflow that mirrors the
  local `just` baseline commands.

## Required Work

- Add or restore required `baseline` workflow.
- Ensure required steps map directly to:
  - `just fmt check`
  - `just lint clippy-lib`
  - `just lint clippy-bins`
  - `just test baseline`
- Remove slow unrelated coverage from required PR gating.
- Preserve fail-fast order.

## Explicit Code Samples

```yaml
steps:
  - run: just fmt check
  - run: just lint clippy-lib
  - run: just lint clippy-bins
  - run: just test baseline
```

## This Sprint Does Not Close

- It does not make fuzz required.
- It does not make semver required.
- It does not make benchmarks required.
- It does not make full conformance required.

## Acceptance Criteria

- One required PR workflow named `baseline` exists.
- Required steps map directly to the local `just` baseline commands.
- Required PR CI completes in under 10 minutes.
- Workflow fails fast and does not continue into slow unrelated coverage.

## Required Validation

- `gh workflow view baseline`
- `gh run list --workflow baseline --limit 5`
- `just fmt check`
- `just lint clippy-lib`
- `just lint clippy-bins`
- `just test baseline`
