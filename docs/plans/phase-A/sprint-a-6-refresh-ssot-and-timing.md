---
id: A6
title: Refresh SSOT And Timing
status: open
branch: sprint-a-6-refresh-ssot-and-timing
worktree: ../pi_agent_atm-worktrees/sprint-a-6-refresh-ssot-and-timing
target: integrate/phase-A
pr: 16
---

# Sprint A6 — Refresh SSOT And Timing

## Goal

- produce the team-lead review pack that freezes source-of-truth ownership and
  refreshes timing evidence without changing the established `just` command
  surface
- freeze the future ATM layering framework before the baseline merges into
  `feature/atm-graft-integration`

## Hard Dependencies

- the current open PR for A6 targets `integrate/phase-A`
- the intended logical dependency remains the A5 baseline state, but the live
  GitHub base branch is not `develop`
- carried-forward A2/A3/A5 backlog fixes already present on this branch must be
  declared explicitly instead of treated as invisible merge noise

## Unblocks

- Sprint A7 merge work should not begin until A6 freezes the final review-pack
  contract and refreshed timing evidence

## Exact Targets

- `docs/plans/phase-A/phase-A-testing-strategy.md` (`isolation: review-pack-doc`)
- `docs/plans/phase-A/sprint-a-6-refresh-ssot-and-timing.md` (`isolation: review-pack-doc`)
- `reports/pi-agent-rust/just-layering-and-atm-integration-strategy-2026-07-03.md` (`isolation: review-pack-report`)
- `.gitignore` (`isolation: smoke-artifact-hygiene`)
- `justfile` (`isolation: baseline-command-surface`)
- `.just/explain.py` (`isolation: ssot-validation-surface`)
- `.just/lint_catalog.py` (`isolation: ssot-validation-surface`)
- `.just/run_fmt.py` (`isolation: ssot-validation-surface`)
- `.just/run_lint.py` (`isolation: ssot-validation-surface`)
- `.just/run_test.py` (`isolation: ssot-validation-surface`)
- `.just/show_suites.py` (`isolation: ssot-validation-surface`)
- `.just/test_catalog.py` (`isolation: ssot-validation-surface`)
- `scripts/e2e/run_all.sh` (`isolation: optional-local-lane-surface`)
- `src/session.rs` (`isolation: mirrored-session-race-surface`)
- `tests/session_conformance.rs` (`isolation: required-smoke-test-surface`)
- `.github/workflows/baseline.yml` (`isolation: required-pr-workflow-audit-no-diff-expected`)

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- team-lead review pack exists with frozen source-of-truth ownership and
  refreshed timing evidence against a green baseline
- the review pack explicitly identifies the final authoritative artifacts QA
  and team-lead review from:
  - refreshed timing table in `phase-A-testing-strategy.md`
  - the A6 sprint doc that declares the carried-forward helper/session/e2e
    surfaces already present on this branch
  - current ATM layering report for `feature/atm-graft-integration`
- the review pack includes a consolidated A1-A6 timing ledger with links back
  to each sprint PR's local and CI timing table

## Required Work

- measure actual `baseline` step timings from current green runs
- update the testing strategy doc with refreshed numbers
- explicitly declare the carried-forward A2/A3/A5 helper, session, and e2e
  files that remain in the branch diff instead of pretending the sprint is
  docs-only
- confirm the required `baseline` workflow still calls only established
  `just` commands
- confirm no new top-level `just` commands were introduced during A1-A5
- confirm lane metadata still cleanly separates upstream, ATM-owned, and
  integration surfaces
- confirm the planned ATM dependency and glue surfaces from
  `feature/atm-graft-integration` still fit the actual post-A5 code base
- confirm the sprint doc matches the actual lane names, workflow names, and
  branch-carried file set
- keep `.github/workflows/baseline.yml` byte-identical to the accepted Sprint
  A5 state
- record the exact review-pack artifact list in the sprint PR notes
- record the consolidated A1-A6 timing ledger in the sprint PR notes
- record materially different same-SHA CI attempts when cold-cache and rerun
  timings diverge

## Explicit Code Samples

```text
baseline workflow
  -> just fmt check
  -> just test compile
  -> just test unit-basic
  -> just lint clippy-bins
  -> just lint clippy-lib
  -> just test baseline
```

```text
review pack
  -> docs/plans/phase-A/phase-A-testing-strategy.md
  -> docs/plans/phase-A/phase-A-just-ci-recovery.md
  -> docs/plans/phase-A/sprint-a-*.md
  -> reports/pi-agent-rust/just-layering-and-atm-integration-strategy-2026-07-03.md
```

## This Sprint Does Not Close

- it does not add new required PR steps
- it does not add new top-level `just` commands
- it does not merge into `feature/atm-graft-integration`

## Acceptance Criteria

- refreshed timing evidence is recorded in the testing strategy doc
- team-lead can review SSOT ownership directly from the review-pack docs
- team-lead can review the future ATM layering rules directly from the review
  pack
- the sprint PR notes name the exact review-pack artifacts and do not claim
  untouched review-pack docs changed
- the review pack and sprint PR notes include a consolidated A1-A6 local and
  CI timing ledger
- the review pack and sprint PR notes record the exact CI run URL/ID used for
  each timing measurement in that ledger
- the carried-forward `.gitignore`, `.just/*`, `justfile`,
  `scripts/e2e/run_all.sh`, `src/session.rs`, and
  `tests/session_conformance.rs` surfaces are declared explicitly in this
  sprint doc
- required `baseline` workflow is unchanged from Sprint A3
- `.github/workflows/baseline.yml` remains byte-identical to Sprint A5
- sprint docs and testing strategy remain internally consistent after the
  timing refresh
- the current A6 head has at least one same-SHA green `baseline` CI run under
  10 minutes, and any materially slower same-SHA attempt remains disclosed in
  the timing record

## Required Validation

- `gh run list --workflow baseline --branch sprint-a-6-refresh-ssot-and-timing --limit 5`
- `just fmt check`
- `just test compile`
- `just test unit-basic`
- `just lint clippy-bins`
- `just lint clippy-lib`
- `just test baseline`
- verify the review-pack artifact list matches the final changed docs/report set
- verify the consolidated A1-A6 timing ledger matches the per-sprint PR notes
