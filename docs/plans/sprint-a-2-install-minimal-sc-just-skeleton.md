---
id: A2
title: Install Minimal sc-just Skeleton
status: planned
branch: sprint-a-2-install-minimal-sc-just-skeleton
worktree: ../pi_agent_atm-worktrees/sprint-a-2-install-minimal-sc-just-skeleton
target: integrate/phase-A
---

# Sprint A2 — Install Minimal sc-just Skeleton

## Goal

- Install the thinnest useful `sc-just` Rust-template-shaped task-runner
  surface without pulling in exploratory source or test churn.

## Hard Dependencies

- Sprint A1 merged into `integrate/phase-A`.

## Exact Targets

- `justfile`
- `.just/`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- Minimal `sc-just` / `atm-core`-style `just` skeleton exists and works for
  help, fmt, and lint.

## Required Work

- Add thin root `justfile`.
- Add dedicated `.just/` directory.
- Keep initial helpers narrow:
  - help
  - fmt
  - lint
- Keep repo-specific behavior out of application code.

## Explicit Code Samples

No code samples required for this sprint.

## This Sprint Does Not Close

- It does not add the full test-lane surface.
- It does not modify CI workflows.

## Acceptance Criteria

- Root `justfile` exists in the thin `sc-just` / `atm-core` shape.
- Dedicated `.just/` folder exists.
- `just help`, `just fmt check`, and `just lint` work.
- No application code or test behavior changes are included.

## Required Validation

- `just help`
- `just fmt check`
- `just lint fmt`
- `just lint clippy-lib`
- `just lint clippy-bins`
