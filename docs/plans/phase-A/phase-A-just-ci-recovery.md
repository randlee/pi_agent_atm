# Phase A - Just / CI Recovery

Date: 2026-07-02
Status: planning
Authoritative scope: Phase A planning only

## Purpose

Phase A recovers the `just` and CI integration effort after the failed
exploratory attempt on `feature/just-integration`.

Phase A exists to:

1. restore review trust around `main` / `master`
2. preserve useful learning from the exploratory branch without merging it
   wholesale
3. install a narrow, reviewable `just` system
4. establish a testing strategy with one source of truth for local and CI lane
   definitions
5. reduce required PR CI to a bounded fast baseline

## Authoritative Document Layout

This phase uses the following document layout and naming rules:

- phase document:
  - `docs/plans/phase-A/phase-A-just-ci-recovery.md`
- sprint documents:
  - `docs/plans/sprint-a-1-<description>.md`
  - `docs/plans/sprint-a-2-<description>.md`
  - and so on

This phase document is the authoritative overview for Phase A.

Each sprint document is authoritative for exactly one sprint and exactly one
deliverable.

Companion phase document:

- `docs/plans/phase-A/phase-A-testing-strategy.md`

Only the `docs/plans/` tree is authoritative for Phase A.

## Planning Rules

This phase follows:

- `/Volumes/Extreme Pro/github/atm-core/.claude/skills/plan-hardening/sprint-planning-guidelines.md`

Applied interpretation for this phase:

- each sprint has one deliverable
- each sprint must end in a production-ready result for its claimed scope
- no sprint may silently carry a committed deliverable forward
- acceptance criteria and required validation live in the sprint doc, not in
  duplicated checklists elsewhere

## Branch And Worktree Model

Phase A implementation will use the following branch model:

- integration branch:
  - `integrate/phase-A`
  - created off `master`
- sprint branches:
  - one branch per sprint, cut from `integrate/phase-A`
- worktrees:
  - one dedicated `sc-git-worktree` per sprint branch

Merge model:

1. `integrate/phase-A` is created from `master`
2. sprint worktree for Sprint A1 is created from `integrate/phase-A`
3. Sprint A1 lands into `integrate/phase-A`
4. sprint worktree for Sprint A2 is created from updated `integrate/phase-A`
5. work merges forward sprint-by-sprint

Expected merge-forward pattern:

- `sprint-a-1` -> `integrate/phase-A`
- `sprint-a-2` starts from updated `integrate/phase-A`
- `sprint-a-2` -> `integrate/phase-A`
- repeat for later sprints

No sprint should branch from the abandoned exploratory branch.

## Revert PR Policy

The unauthorized direct commits on `main` must be addressed first in execution
order, but not merged immediately during planning.

Required policy:

- the revert exists now as a reviewable draft PR
- the revert PR stays unmerged while Phase A planning is completed
- the revert PR is the first execution step once implementation begins
- before merging the revert PR, review whether any leaked changes have salvage
  value and should be reintroduced properly on a dedicated sprint branch

Current revert PR:

- draft PR for `fix/revert-unauthorized-main-20260702` -> `main`

This means:

- planning completes first
- codebase review of leaked commits happens during planning / sprint setup
- revert executes first when Phase A implementation starts

## Inputs Reviewed

- `sc-just` skill and references under
  `/Volumes/Extreme Pro/github/synaptic-canvas/packages/sc-just`
- `atm-core` `justfile` and `.just/` structure under
  `/Volumes/Extreme Pro/github/atm-core`
- current repo branch state
- exploratory branch `feature/just-integration`
- GitHub Actions timing/failure evidence from 2026-07-02

## Ground Rules

- do not work on `main`
- do not merge `feature/just-integration` wholesale
- do not reintroduce exploratory `src/**` churn as part of the `just` recovery
- reuse only narrow, understandable pieces from exploratory work
- `just` must unify existing command entry points rather than create parallel
  ones
- `just test` and CI must share the same lane definitions
- required PR CI must finish in under 10 minutes
- long-running workflows must be optional/manual/scheduled unless later evidence
  proves they belong in required PR CI

## Safe Reuse Inventory

Safe reuse candidates from exploratory work:

- thin root `justfile` shape
- `.just/print_help.py`
- `.just/run_fmt.py`
- `.just/run_lint.py`
- catalog-driven lane-definition approach
- `just explain` / `just suites` explanatory surface
- fast `baseline` workflow concept
- smoke-lane concept

Reuse only after revalidation:

- `run_test.py`
- any `verify --profile ...` coupling
- broad CI workflow rewrites
- artifact/shard orchestration changes

Do not reuse directly:

- exploratory `src/**` changes
- broad test rewrites done only to chase green CI
- monolithic workflow edits without a minimal target-state design

## Testing Strategy Summary

Phase A includes a testing strategy as part of the plan, not as an afterthought.

Current observed facts:

- `suite.unit`: 118 targets
- `suite.vcr`: 144 targets
- `suite.e2e`: 39 targets
- `tests/*.rs` integration-test crates: 301

Observed timing baseline:

- local macOS:
  - `just fmt check`: `12.46s`
  - `just lint clippy-lib`: `50.66s`
  - `just lint clippy-bins`: `2.87s`
  - `just test baseline`: `10.59s`
- GitHub Actions:
  - `baseline`: about `7m`
  - `Extension Conformance`: about `6m25s`
  - `Fuzz CI`: about `43m`
  - old monolithic `ci`: about `49m` before cancellation

Implications:

- a fast required PR baseline is viable
- fuzz does not belong in required PR CI
- monolithic CI does not belong in required PR gating
- broad `clippy --tests` and full test orchestration must be kept outside the
  default fast lane until separately justified

Known issues to preserve in implementation planning:

- macOS Bash 3 portability concerns
- macOS `just clean` instability against `target/agents/...`
- prior `vergen-lib` local build issue
- historical fuzz instability around `sysinfo` / nightly drift
- historical CI working-directory mistakes

## Phase Deliverables By Sprint

Phase A is split into the following sprint documents:

1. `docs/plans/sprint-a-1-stage-revert-pr.md`
2. `docs/plans/sprint-a-2-install-minimal-sc-just-skeleton.md`
3. `docs/plans/sprint-a-3-establish-lane-ssot.md`
4. `docs/plans/sprint-a-4-add-fast-test-baseline.md`
5. `docs/plans/sprint-a-5-reduce-required-pr-ci-to-baseline.md`
6. `docs/plans/sprint-a-6-classify-long-running-workflows.md`
7. `docs/plans/sprint-a-7-merge-baseline-into-atm-graft.md`

Each sprint has one deliverable only.

## Open Questions For Jen

1. Should the phase ultimately retain `verify` as the underlying test runner, or
   should Phase A treat it as replaceable plumbing behind the `just` lane SSOT?
2. Should cross-platform CI remain outside required PR CI for the fork baseline,
   with Linux baseline as the required path?
3. Should the smoke baseline remain shell-based or move into Python so the same
   catalog system owns all lane data?
4. Should `Extension Conformance` stay PR-available but non-required, or move
   to manual/nightly only?

## Exit Criteria

Phase A is complete when all of the following are true:

- the revert PR has been reviewed and then merged as the first execution step
- `integrate/phase-A` contains the new `just` baseline
- `just` lane definitions are SSOT-backed
- required PR CI is under 10 minutes
- long-running workflows are explicitly classified outside required PR CI
- the stabilized baseline is ready to merge forward into `atm-graft` work
