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
- make compile checking and strict basic-unit coverage the first required test
  layers

## Hard Dependencies

- team-lead reviews `docs/plans/phase-A/phase-A-testing-strategy.md`
- sprint branches are cut from current `develop`

## Unblocks

- Sprint A2 can add required lint only after A1 proves the reduced PR gate is
  real and stable
- all later Phase A sprints depend on A1 defining the stable baseline lane
  names and retained upstream-workflow trigger model

## Exact Targets

- `justfile` (`isolation: baseline-command-surface`)
- `.just/print_help.py` (`isolation: reused-helper-surface`)
- `.just/run_fmt.py` (`isolation: reused-helper-surface`)
- `.just/run_cargo.py` (`isolation: reused-helper-surface`)
- `.just/run_test.py` (`isolation: reused-helper-surface`)
- `.just/test_catalog.py` (`isolation: required-test-lane-surface`)
- `.github/workflows/baseline.yml` (`isolation: new-required-pr-workflow`)
- `.github/workflows/ci.yml` (`isolation: trigger-only-edit`)
- `.github/workflows/conformance.yml` (`isolation: trigger-only-edit`)
- `.github/workflows/fuzz.yml` (`isolation: trigger-only-edit`)
- `.github/workflows/bench.yml` (`isolation: trigger-only-edit`)
- `.github/workflows/semver.yml` (`isolation: trigger-only-edit`)
- `.github/workflows/model-catalog-drift.yml` (`isolation: trigger-only-edit`)

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- minimal `just` surface exists and one tiny `baseline` workflow becomes the
  only required PR gate
- the first required gate proves compile health and strict basic-unit health
  before lint or smoke expansion

## Required Work

- add thin root `justfile`
- reuse `print_help.py` and `run_fmt.py`
- reuse `run_cargo.py`, `run_test.py`, and `test_catalog.py`
- add `baseline.yml` with:
  - `just help`
  - `just fmt check`
  - `just test compile`
  - `just test unit-basic`
- define `just test compile` as `cargo check --all-targets`
- define `just test unit-basic` as:
  - `cargo test --all-targets --lib`
  - plus the explicit strict add-on allowlist from the testing strategy
- do not treat all of `[suite.unit]` as the first baseline unit lane
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
- update the repository's required branch-protection status checks for ordinary
  PRs so `baseline` is the only required workflow after the Sprint A1 trigger
  reduction lands
- prove each displaced upstream workflow is still manually runnable after the
  trigger edits and record that proof in the Sprint A1 PR notes
- keep the Phase A baseline lane names stable so later ATM-owned lanes can
  layer in additively instead of mutating the upstream-regression contract

Reuse sources:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/justfile`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/print_help.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_fmt.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_cargo.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_test.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.github/workflows/baseline.yml`

## Explicit Code Samples

```just
default: help

help:
    {{python_cmd}} .just/print_help.py

fmt mode='check':
    {{python_cmd}} .just/run_fmt.py {{mode}}

test lane='':
    {{python_cmd}} .just/run_test.py {{lane}}
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
      - run: just test compile
      - run: just test unit-basic
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

- it does not add clippy
- it does not add smoke testing
- it does not add optional local lanes

## Acceptance Criteria

- `just help` exits 0 and lists the established Phase A command surface
- `just fmt check` exits 0
- `just test compile` exits 0
- `just test unit-basic` exits 0
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
- each displaced workflow still has a verified manual or scheduled execution
  path after the trigger edits
- branch protection for ordinary PRs requires only the `baseline` workflow once
  the Sprint A1 operational update lands
- the new `baseline` workflow does not call any raw cargo command directly
- `unit-basic` is explicitly narrower than the full broad `[suite.unit]` bucket
- required PR CI is green and comfortably under 10 minutes

## Required Validation

- `just help`
- `just fmt check`
- `just test compile`
- `just test unit-basic`
- `gh workflow view baseline`
- `gh run list --workflow baseline --limit 5`
- `gh workflow view ci`
- `gh workflow view conformance`
- `gh workflow view fuzz`
- `gh workflow view bench`
- `gh workflow view semver`
- `gh workflow view model-catalog-drift`
- `gh workflow run ci --ref <sprint-branch>`
- `gh workflow run conformance --ref <sprint-branch>`
- `gh workflow run fuzz --ref <sprint-branch>`
- `gh workflow run bench --ref <sprint-branch>`
- `gh workflow run semver --ref <sprint-branch>`
- `gh workflow run model-catalog-drift --ref <sprint-branch>`
- verify ordinary-PR required status checks are reduced to `baseline` only
- verify no ordinary PR run triggers `ci`, `conformance`, `fuzz`, `bench`,
  `semver`, or `Model Catalog Drift`
