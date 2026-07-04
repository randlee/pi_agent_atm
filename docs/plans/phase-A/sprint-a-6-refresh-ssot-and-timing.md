---
id: A6
title: Refresh SSOT And Timing
status: complete
branch: sprint-a-6-refresh-ssot-and-timing
worktree: ../pi_agent_atm-worktrees/sprint-a-6-refresh-ssot-and-timing
target: sprint-a-5-add-optional-local-lanes
---

# Sprint A6 — Refresh SSOT And Timing

## Goal

- produce the team-lead review pack that freezes source-of-truth ownership and
  refreshes timing evidence without changing the established `just` command
  surface
- freeze the future ATM layering framework before the baseline merges into
  `feature/atm-graft-integration`

## Hard Dependencies

- Sprint A5 merged forward from `sprint-a-5-add-optional-local-lanes`

## Unblocks

- Sprint A7 merge work should not begin until A6 freezes the final review-pack
  contract and refreshed timing evidence

## Exact Targets

- `docs/plans/phase-A/phase-A-testing-strategy.md` (`isolation: review-pack-doc`)
- `docs/plans/phase-A/phase-A-just-ci-recovery.md` (`isolation: review-pack-doc`)
- `docs/plans/phase-A/sprint-a-1-establish-minimal-baseline-gate.md` (`isolation: review-pack-doc`)
- `docs/plans/phase-A/sprint-a-2-add-local-code-lint.md` (`isolation: review-pack-doc`)
- `docs/plans/phase-A/sprint-a-3-add-smoke-baseline.md` (`isolation: review-pack-doc`)
- `docs/plans/phase-A/sprint-a-4-add-taxonomy-helpers.md` (`isolation: review-pack-doc`)
- `docs/plans/phase-A/sprint-a-5-add-optional-local-lanes.md` (`isolation: review-pack-doc`)
- `docs/plans/phase-A/sprint-a-6-refresh-ssot-and-timing.md` (`isolation: review-pack-doc`)
- `docs/plans/phase-A/sprint-a-7-merge-baseline-into-atm-graft.md` (`isolation: review-pack-doc`)
- `reports/pi-agent-rust/just-layering-and-atm-integration-strategy-2026-07-03.md` (`isolation: review-pack-report`)
- `.gitignore` (`isolation: smoke-artifact-hygiene`)
- `justfile` (`isolation: baseline-command-surface`)
- `.just/explain.py` (`isolation: ssot-validation-surface`)
- `.just/lint_catalog.py` (`isolation: ssot-validation-surface`)
- `.just/run_lint.py` (`isolation: ssot-validation-surface`)
- `.just/run_test.py` (`isolation: ssot-validation-surface`)
- `.just/test_catalog.py` (`isolation: ssot-validation-surface`)
- `.just/show_suites.py` (`isolation: ssot-validation-surface`)
- `scripts/e2e/run_all.sh` (`isolation: optional-verify-surface`)
- `scripts/smoke.sh` (`isolation: required-smoke-script-surface`)
- `tests/session_conformance.rs` (`isolation: required-smoke-test-surface`)
- `src/session.rs` (`isolation: mirrored-session-test-surface`)
- `.github/workflows/baseline.yml` (`isolation: required-pr-workflow-audit`)

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
  - refreshed Phase A overview and sprint docs if names or ownership drifted
  - current ATM layering report for `feature/atm-graft-integration`

## Required Work

- measure actual `baseline` step timings from current green runs
- update the testing strategy doc with refreshed numbers
- update the phase doc and sprint docs if any lane names, workflow names, or
  ownership statements drifted during A1-A5
- confirm the required `baseline` workflow still calls only established
  `just` commands
- confirm no new top-level `just` commands were introduced during A1-A5
- confirm lane metadata still cleanly separates upstream, ATM-owned, and
  integration surfaces
- remove duplicated lint cargo command strings from `justfile` so
  `.just/lint_catalog.py` owns both lint taxonomy and actual execution
- derive required-lane and optional-lane grouping output from lane metadata
  rather than from hardcoded lists in `.just/show_suites.py`
- confirm the planned ATM dependency and glue surfaces from
  `feature/atm-graft-integration` still fit the actual post-A5 code base
- confirm the sprint docs still match the actual lane names and workflow names
- confirm the upstream ordinary-PR workflow classification still matches the
  testing strategy after A1 trigger changes
- synchronize `session_conformance.rs::concurrent_saves_do_not_corrupt_session_file`
  with the mirrored session unit test so the required smoke target proves both
  concurrent saves survive the race instead of only tolerating partial success
- add repo ignore coverage for `tests/smoke_results/`
- record the exact review-pack artifact list in the sprint PR notes

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
- refreshed timing evidence names the exact July 4, 2026 green evidence source
  and states whether the current baseline budget is met or exceeded
- team-lead can review SSOT ownership directly from the review-pack docs
- team-lead can review the future ATM layering rules directly from the review
  pack
- the sprint PR notes name the exact review-pack artifacts and confirm no lane
  names or workflow names drifted unexpectedly
- required `baseline` workflow is unchanged from Sprint A3
- sprint docs and testing strategy remain internally consistent after the
  timing refresh
- `tests/smoke_results/` is gitignored
- `session_conformance` and `src/session.rs` use the same concurrent-save test
  contract for the smoke-covered race case

## Required Validation

- `gh run list --workflow baseline --limit 5`
- `just explain lint clippy-lib`
- `just explain test all`
- `just explain test unit`
- `just suites`
- `just fmt check`
- `just test compile`
- `just test unit-basic`
- `just lint clippy-bins`
- `just lint clippy-lib`
- `just test baseline`
- `cargo test --test session_conformance concurrent_saves_do_not_corrupt_session_file -- --nocapture`
- `cargo test concurrent_saves_do_not_corrupt_session_file_unit --lib -- --nocapture`
- `rg -n "tests/smoke_results/" .gitignore`
- verify the review-pack artifact list matches the final changed docs/report set
