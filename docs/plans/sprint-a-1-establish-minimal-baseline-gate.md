---
id: A1
title: Establish Minimal Baseline Gate
status: planned
branch: sprint-a-1-establish-minimal-baseline-gate
worktree: ../pi_agent_atm-worktrees/sprint-a-1-establish-minimal-baseline-gate
target: develop
---

# Sprint A1 — Establish Minimal Baseline Gate

## Goal

- ship the smallest working `just` + CI surface
- make `baseline` the only required PR workflow immediately

## Hard Dependencies

- team-lead reviews `docs/plans/phase-A/phase-A-testing-strategy.md`
- sprint branches are cut from current `develop`

## Exact Targets

- `justfile`
- `.just/print_help.py`
- `.just/run_fmt.py`
- `.github/workflows/baseline.yml`
- `.github/workflows/ci.yml`
- `.github/workflows/fuzz.yml`
- `.github/workflows/bench.yml`
- `.github/workflows/semver.yml`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- minimal `just` surface exists and one tiny `baseline` workflow becomes the
  only required PR gate

## Required Work

- add thin root `justfile`
- reuse `print_help.py` and `run_fmt.py`
- add `baseline.yml` with only `just help` and `just fmt check`
- remove ordinary `pull_request` triggering from heavyweight workflow files
- keep `fuzz`, `bench`, and `semver` available only through non-PR trigger
  paths

## Explicit Code Samples

```just
default: help

help:
    {{python_cmd}} .just/print_help.py

fmt mode='check':
    {{python_cmd}} .just/run_fmt.py {{mode}}
```

```yaml
name: baseline
on:
  pull_request:

jobs:
  baseline:
    steps:
      - run: just help
      - run: just fmt check
```

## This Sprint Does Not Close

- it does not add compile checking
- it does not add clippy
- it does not add smoke testing
- it does not add optional local lanes

## Acceptance Criteria

- `just help` works
- `just fmt check` works
- one workflow named `baseline` runs on ordinary PRs
- old heavyweight workflows do not run on ordinary PRs
- required PR CI is green and comfortably under 10 minutes

## Required Validation

- `just help`
- `just fmt check`
- `gh workflow view baseline`
- `gh run list --workflow baseline --limit 5`
- verify no ordinary PR run triggers `ci`, `fuzz`, `bench`, or `semver`
