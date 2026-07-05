---
id: A4
title: Add Taxonomy Helpers
status: open
branch: sprint-a-4-add-taxonomy-helpers
worktree: ../pi_agent_atm-worktrees/sprint-a-4-add-taxonomy-helpers
target: sprint-a-3-add-smoke-baseline
---

# Sprint A4 — Add Taxonomy Helpers

## Goal

- expose taxonomy helpers while freezing required PR CI

## Hard Dependencies

- A4 must branch from the last proven A3 replay state, not from stale
  historical branch state

## Unblocks

- Sprint A5 optional local lanes can only be QA-readable if A4 defines the
  helper output contract first
- Sprint A6 review-pack freezing depends on A4 exposing SSOT ownership and lane
  metadata directly

## Exact Targets

- `justfile` (`isolation: baseline-command-surface`)
- `.just/explain.py` (`isolation: taxonomy-helper-surface`)
- `.just/show_suites.py` (`isolation: taxonomy-helper-surface`)

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- taxonomy helpers exist without changing required PR CI
- the Sprint A4 PR notes include:
  - refreshed local and CI timing for the unchanged A3 baseline stage
  - local timings for `just explain` and `just suites`
  - an explicit `no ci equivalent by design` note for the helper commands

## Required Work

- add `just explain`
- add `just suites`
- make `just explain` surface lane origin, owner, blocking level, and source of
  truth so future ATM-owned lanes can reuse the same taxonomy
- keep required `baseline` contents exactly as Sprint A3 defined them

Reuse sources:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/explain.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/show_suites.py`

## Explicit Code Samples

```just
explain domain='' lane='':
    {{python_cmd}} .just/explain.py {{domain}} {{lane}}

suites:
    {{python_cmd}} .just/show_suites.py
```

```text
lane=test.baseline
origin=upstream
owner=.just/test_catalog.py
blocking=required
ssot=.just/test_catalog.py
command=./scripts/smoke.sh --skip-lint --no-rch
```

## This Sprint Does Not Close

- it does not change required PR CI contents
- it does not reintroduce heavyweight PR workflows
- it does not invent a new top-level `just` command
- it does not add optional local lanes

## Acceptance Criteria

- `just explain` exits 0 for required and optional lanes
- `just suites` exits 0 and reports suite taxonomy from the documented source
- taxonomy helper output points operators to the SSOT lane and suite surfaces
- taxonomy helper output distinguishes upstream baseline lanes from future
  ATM-owned and integration lanes
- `just explain` prints lane origin, owner, blocking level, SSOT file, and
  command for the requested lane
- required `baseline` workflow is unchanged from Sprint A3
- `baseline` remains green and under 10 minutes
- the Sprint A4 PR notes record local and CI timings exactly as the sprint
  timing contract requires
- the Sprint A4 PR notes record the exact CI run URL/ID used for each timing
  measurement

## Required Validation

- `just explain lint clippy-lib`
- `just explain test baseline`
- `just suites`
- `gh workflow view baseline`
- `gh run list --workflow baseline --limit 5`
- record local timings for `just explain lint clippy-lib`, `just explain test baseline`,
  and `just suites`
- record refreshed CI step timings and total `baseline` workflow duration for
  the unchanged A3 baseline stage
