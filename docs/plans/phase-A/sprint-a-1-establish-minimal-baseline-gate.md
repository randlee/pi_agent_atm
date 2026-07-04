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
- `.github/workflows/conformance.yml`
- `.github/workflows/fuzz.yml`
- `.github/workflows/bench.yml`
- `.github/workflows/semver.yml`
- `.github/workflows/model-catalog-drift.yml`

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
- confirm the testing strategy already inventories every currently PR-triggered
  upstream workflow before any trigger changes land
- remove ordinary `pull_request` triggering from these heavyweight workflow
  files:
  - `.github/workflows/ci.yml`
  - `.github/workflows/conformance.yml`
  - `.github/workflows/fuzz.yml`
  - `.github/workflows/bench.yml`
  - `.github/workflows/semver.yml`
  - `.github/workflows/model-catalog-drift.yml`
- set the exact retained trigger policy:
  - `.github/workflows/ci.yml`: `workflow_dispatch` only
  - `.github/workflows/conformance.yml`: `workflow_dispatch` and `schedule`
  - `.github/workflows/fuzz.yml`: `workflow_dispatch` and `schedule` only
  - `.github/workflows/bench.yml`: `workflow_dispatch` only
  - `.github/workflows/semver.yml`: `workflow_dispatch` only
  - `.github/workflows/model-catalog-drift.yml`: `workflow_dispatch` and `schedule` only
- preserve current branch protection semantics by changing triggers rather than
  deleting whole workflow files

Reuse sources:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/justfile`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/print_help.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_fmt.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.github/workflows/baseline.yml`

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

```yaml
# retained trigger shape for `.github/workflows/fuzz.yml`
on:
  workflow_dispatch:
  schedule:
```

```yaml
# retained trigger shape for `.github/workflows/ci.yml`,
# `.github/workflows/bench.yml`, and `.github/workflows/semver.yml`
on:
  workflow_dispatch:
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
- `.github/workflows/ci.yml`, `.github/workflows/fuzz.yml`,
  `.github/workflows/bench.yml`, `.github/workflows/semver.yml`,
  `.github/workflows/conformance.yml`, and
  `.github/workflows/model-catalog-drift.yml` do not run on ordinary PRs
- `.github/workflows/ci.yml` retains `workflow_dispatch` only
- `.github/workflows/conformance.yml` retains `workflow_dispatch` and
  `schedule`
- `.github/workflows/fuzz.yml` retains `workflow_dispatch` and `schedule` only
- `.github/workflows/bench.yml` retains `workflow_dispatch` only
- `.github/workflows/semver.yml` retains `workflow_dispatch` only
- `.github/workflows/model-catalog-drift.yml` retains `workflow_dispatch` and
  `schedule` only
- the new `baseline` workflow does not call any raw cargo command directly
- required PR CI is green and comfortably under 10 minutes

## Required Validation

- `just help`
- `just fmt check`
- `gh workflow view baseline`
- `gh run list --workflow baseline --limit 5`
- verify no ordinary PR run triggers `ci`, `conformance`, `fuzz`, `bench`,
  `semver`, or `Model Catalog Drift`
