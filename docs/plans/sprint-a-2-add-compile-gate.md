---
id: A2
title: Add Local-Code Lint
status: planned
branch: sprint-a-2-add-local-code-lint
worktree: ../pi_agent_atm-worktrees/sprint-a-2-add-local-code-lint
target: develop
---

# Sprint A2 — Add Local-Code Lint

## Goal

- add only the local-code lint lanes needed for required PR CI through the
  established `just lint` surface

## Hard Dependencies

- Sprint A1 merged into `develop`

## Exact Targets

- `justfile`
- `.just/run_cargo.py`
- `.just/run_lint.py`
- `.just/lint_catalog.py`
- `.github/workflows/baseline.yml`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- `just lint clippy-bins` and `just lint clippy-lib` exist and are wired into
  `baseline`

## Required Work

- reuse `run_cargo.py`, `run_lint.py`, and `lint_catalog.py`
- define only the required local-code lint lanes first
- update `baseline.yml` to run the lint lanes after formatting
- keep dependency lint and test-target lint out of required PR CI

## Explicit Code Samples

```python
LANES = {
    "clippy-bins": LintLane(...),
    "clippy-lib": LintLane(...),
}
```

```yaml
steps:
  - run: just help
  - run: just fmt check
  - run: just lint clippy-bins
  - run: just lint clippy-lib
```

## This Sprint Does Not Close

- it does not add smoke testing
- it does not add optional local lanes
- it does not invent a new top-level `just` command

## Acceptance Criteria

- `just lint clippy-bins` works
- `just lint clippy-lib` works
- required `baseline` workflow runs only the established lint surface
- `baseline` remains green and under 10 minutes
- no new PR-required workflow is introduced

## Required Validation

- `just help`
- `just fmt check`
- `just lint clippy-bins`
- `just lint clippy-lib`
- `gh workflow view baseline`
- `gh run list --workflow baseline --limit 5`
