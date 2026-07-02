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

- Sprint A1 completed.
- Revert PR merged into `main`.
- `master` synchronized to restored `main`.
- `integrate/phase-A` created from synchronized `master`.

## Exact Targets

- `justfile`
- `.just/`
- `feature/just-integration:justfile`
- `feature/just-integration:.just/print_help.py`
- `feature/just-integration:.just/run_fmt.py`
- `feature/just-integration:.just/run_lint.py`

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

```just
default: help
help:
    {{python_cmd}} .just/print_help.py

fmt mode='check':
    {{python_cmd}} .just/run_fmt.py {{mode}}

lint target='all':
    {{python_cmd}} .just/run_lint.py {{target}}
```

## This Sprint Does Not Close

- It does not add the full test-lane surface.
- It does not modify CI workflows.

## Acceptance Criteria

- Root `justfile` exists in the thin `sc-just` / `atm-core` shape.
- Dedicated `.just/` folder exists.
- `just help`, `just fmt check`, and `just lint` work.
- No application code or test behavior changes are included.
- No CI workflow changes are included.

## Required Validation

- `just help`
- `just fmt check`
- `just lint fmt`
- `just lint clippy-lib`
- `just lint clippy-bins`
