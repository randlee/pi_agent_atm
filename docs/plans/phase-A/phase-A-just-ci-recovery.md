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

- prerequisite branch state:
  - merge the revert PR first
  - synchronize `master` to the restored `main`
  - create `integrate/phase-A` from that synchronized `master`
- integration branch:
  - `integrate/phase-A`
  - created off `master`
- sprint branches:
  - one branch per sprint, cut from `integrate/phase-A`
- worktrees:
  - one dedicated `sc-git-worktree` per sprint branch

Merge model:

1. `master` is synchronized to restored `main`
2. `integrate/phase-A` is created from synchronized `master`
3. Sprint A1 stages and holds the draft revert PR against `main`
4. sprint worktree for Sprint A2 is created from `integrate/phase-A`
5. Sprint A2 lands into `integrate/phase-A`
6. later sprint worktrees are created from updated `integrate/phase-A`
7. work merges forward sprint-by-sprint

Expected merge-forward pattern:

- `sprint-a-2-*` starts from updated `integrate/phase-A`
- `sprint-a-2-*` -> `integrate/phase-A`
- repeat for later sprints

No implementation sprint should branch from:

- `plan/just-integration`
- `feature/just-integration`
- `feature/atm-graft-integration`

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

- `feature/just-integration:justfile`
- `feature/just-integration:.just/print_help.py`
- `feature/just-integration:.just/run_fmt.py`
- `feature/just-integration:.just/run_lint.py`
- `feature/just-integration:.just/lint_catalog.py`
- `feature/just-integration:.just/test_catalog.py`
- `feature/just-integration:.just/explain.py`
- `feature/just-integration:.just/show_suites.py`
- `feature/just-integration:.github/workflows/baseline.yml`
- `feature/just-integration:scripts/smoke.sh`

Reuse only after revalidation:

- `feature/just-integration:.just/run_test.py`
- any `verify --profile ...` coupling
- broad CI workflow rewrites
- artifact/shard orchestration changes

Do not reuse directly:

- exploratory `src/**` changes
- broad test rewrites done only to chase green CI
- monolithic workflow edits without a minimal target-state design

## Reverted Main Commit Restoration Ledger

No reverted direct-to-main commit is automatically restored as part of the
revert itself.

Restoration rule:

- revert first
- review each reverted commit as salvage inventory
- reintroduce only the narrow pieces that still make sense
- reintroduce them on the correct Phase A sprint branch, never by reverting the
  revert

### `9203d7df` Fix VCR suite classification and refresh review dates

Files:

- `tests/ext_conformance/reports/conformance_baseline.json`
- `tests/qa_certification_dossier.rs`
- `tests/suite_classification.toml`

Current disposition:

- `tests/suite_classification.toml`
  - candidate for restoration review during Sprint A3 if the exploratory
    reclassification is still correct
- `tests/ext_conformance/reports/conformance_baseline.json`
  - not automatically part of Phase A baseline; restore only if later workflow
    classification proves it necessary
- `tests/qa_certification_dossier.rs`
  - not automatically part of Phase A baseline; review separately if date-based
    failures remain relevant after revert

### `425e7a05` Fix baseline CI and verification regressions

Files:

- `.github/workflows/bench.yml`
- `.github/workflows/ci.yml`
- `Cargo.toml`
- `README.md`
- `fuzz/Cargo.lock`
- `fuzz/Cargo.toml`
- `scripts/ci/generate_parity_evidence.py`
- `scripts/e2e/run_all.sh`
- `tests/full_suite_gate/extension_remediation_backlog.json`
- `tests/security_budgets.rs`

Current disposition:

- `.github/workflows/ci.yml`
  - do not restore wholesale; redesign only through Sprint A5 and Sprint A6
- `.github/workflows/bench.yml`
  - review in Sprint A6 when classifying long-running workflows
- `scripts/e2e/run_all.sh`
  - candidate for narrow salvage only if `verify` remains in use and the
    fail-fast/shard behavior is still required after Sprint A4 review
- `Cargo.toml`
  - do not restore blindly; any dependency or feature changes require separate
    justification
- `README.md`
  - out of scope for Phase A unless command-surface docs must be updated after
    implementation
- `fuzz/Cargo.toml`
  - review only when fuzz classification is revisited in Sprint A6
- `fuzz/Cargo.lock`
  - never restore independently of an intentional `fuzz/Cargo.toml` change
- `scripts/ci/generate_parity_evidence.py`
  - outside initial baseline scope; review only if retained CI still needs it
- `tests/full_suite_gate/extension_remediation_backlog.json`
  - outside initial baseline scope
- `tests/security_budgets.rs`
  - outside initial baseline scope unless later retained workflow review
    requires it

### `4b762a59` Disable semver in baseline CI

Files:

- `.github/workflows/semver.yml`

Current disposition:

- do not restore as a direct revert of the revert
- decide classification in Sprint A6
- if semver remains out of required PR CI, update it there intentionally

### `5fe05e11` Trim baseline CI and ignore local artifacts

Files:

- `.github/workflows/ci.yml`
- `.gitignore`

Current disposition:

- `.github/workflows/ci.yml`
  - do not restore wholesale; redesign only through Sprint A5 and Sprint A6
- `.gitignore`
  - candidate for explicit restoration if the ignored local-only artifacts are
    still required:
    - `.DS_Store`
    - `.sc/`

### `392b209f` Fix SQLite claim guard and fuzz path invariant

Files:

- `.github/workflows/ci.yml`
- `fuzz/fuzz_targets/fuzz_tool_paths.rs`

Current disposition:

- `.github/workflows/ci.yml`
  - do not restore wholesale; redesign only through Sprint A5 and Sprint A6
- `fuzz/fuzz_targets/fuzz_tool_paths.rs`
  - review only if fuzz remains a retained workflow after Sprint A6

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
- the planning branch itself still carries pre-revert ancestry and must not be
  used as the code integration base

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

Sprint A1 is the only pre-integration gating sprint:

- it creates and holds the draft revert PR against `main`
- it does not merge into `integrate/phase-A`
- `integrate/phase-A` is created only after the revert merges and `master` is
  synchronized

Sprints A2 through A7 follow the normal merge-forward model into
`integrate/phase-A`.

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
