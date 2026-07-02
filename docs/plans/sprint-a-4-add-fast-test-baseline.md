---
id: A4
title: Add Fast Test Baseline
status: planned
branch: sprint-a-4-add-fast-test-baseline
worktree: ../pi_agent_atm-worktrees/sprint-a-4-add-fast-test-baseline
target: integrate/phase-A
---

# Sprint A4 — Add Fast Test Baseline

## Goal

- Add the fast local smoke baseline and wire the initial `just test*` surface to
  the lane SSOT.

## Hard Dependencies

- Sprint A3 merged into `integrate/phase-A`.

## Exact Targets

- `.just/`
- `scripts/smoke.sh`
- `tests/suite_classification.toml`
- `feature/just-integration:scripts/smoke.sh`
- `feature/just-integration:.just/run_test.py`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- Production-ready fast local smoke baseline exists and drives the initial
  `just test*` surface.

## Required Work

- Add `just test baseline`.
- Add `just test`, `just test unit`, `just test integration`, `just test vcr`,
  `just test e2e`, and `just test all` via the SSOT layer.
- Keep the smoke lane non-destructive.
- Ensure lane failures point to the exact source-of-truth and next action.

## Explicit Code Samples

```text
just test baseline
  -> lane catalog entry "baseline"
  -> smoke runner
  -> isolated artifact directory
```

## This Sprint Does Not Close

- It does not cut required PR CI over to the baseline workflow yet.
- It does not include fuzz, semver, or benchmarks in the default test lane.

## Acceptance Criteria

- `just test baseline` exists and is non-destructive.
- All planned `just test*` lanes resolve from the SSOT layer.
- Smoke uses temporary or isolated artifacts instead of mutating tracked
  evidence paths.
- Failure output points to the lane source-of-truth and next diagnostic step.

## Required Validation

- `just test baseline`
- `just explain test`
- `just suites`
