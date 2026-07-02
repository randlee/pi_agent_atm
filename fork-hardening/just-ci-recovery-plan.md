# Just / CI Recovery Plan

Date: 2026-07-02
Branch: `plan/just-integration`
Authoring scope: planning only

## Purpose

Recover from the failed first pass at `just` + CI integration by:

1. restoring `main` to the pre-leak state
2. reusing only the safe parts of the exploratory `feature/just-integration`
   work
3. reintroducing `just` and CI in small sprints that each end with a passing,
   bounded CI state
4. documenting the test strategy so local agent runs and GitHub Actions share a
   single source of truth

This plan is authoritative for the recovery effort. It is intentionally
separate from `docs/` so future upstream merges from `pi-agent-rust` stay
simpler.

## Inputs Reviewed

- `sc-just` skill and references under
  `/Volumes/Extreme Pro/github/synaptic-canvas/packages/sc-just`
- `atm-core` `justfile` and `.just/` structure under
  `/Volumes/Extreme Pro/github/atm-core`
- current `main` branch state in `pi_agent_atm`
- exploratory branch `feature/just-integration`
- GitHub Actions runs from 2026-07-02:
  - `baseline` success run `28622615189`
  - `baseline` failure run `28624613416`
  - `Extension Conformance` success run `28622615206`
  - `Fuzz CI` success run `28622615217`
  - cancelled monolithic `ci` run `28618082382`

## Ground Rules

- Do not work on `main`.
- Do not merge `feature/just-integration` wholesale.
- Do not carry forward unrelated `src/`, broad test, or CI churn from the
  exploratory branch.
- Reuse only components that are both understandable and narrow enough to
  review in isolation.
- `just` should unify existing repo entry points, not invent competing command
  paths.
- `just test` and CI must share the same lane definitions.
- Required PR CI must finish in under 10 minutes.
- Long-running coverage such as fuzz, benches, semver, and full conformance
  must move out of required PR CI unless a later sprint explicitly proves they
  belong.

## Reuse Classification

### Safe Reuse Candidates

- root `justfile` shape from `feature/just-integration`
- `.just/print_help.py`
- `.just/run_fmt.py`
- `.just/run_lint.py`
- catalog-driven command idea from:
  - `.just/lint_catalog.py`
  - `.just/test_catalog.py`
  - `.just/explain.py`
  - `.just/show_suites.py`
- fast `baseline` workflow concept from
  `.github/workflows/baseline.yml`
- smoke-lane concept from `scripts/smoke.sh`

### Reuse Only After Revalidation

- `.just/run_test.py`
- any use of `./verify --profile ...`
- workflow wiring into `.github/workflows/ci.yml`
- any scripts that touched artifact bundling, shard orchestration, or E2E
  control flow

### Do Not Reuse Directly

- exploratory changes under `src/**`
- broad edits to `tests/**` done to make CI pass
- direct edits to large existing workflows without a minimal target-state design
- any branch changes whose only justification was "get current CI green"

## Target End State

### Local Command Surface

- `just help`
- `just fmt check`
- `just fmt write`
- `just lint`
- `just lint fmt`
- `just lint clippy`
- `just lint clippy-lib`
- `just lint clippy-bins`
- `just lint clippy-tests`
- `just lint clippy-benches`
- `just lint clippy-examples`
- `just test`
- `just test baseline`
- `just test unit`
- `just test integration`
- `just test vcr`
- `just test e2e`
- `just test all`
- `just ci`
- `just clean`
- `just suites`
- `just explain lint [lane]`
- `just explain test [lane]`

### Required PR CI

- one required fast workflow named `baseline`
- fail-fast order:
  1. format
  2. narrow local clippy slices
  3. fast smoke baseline
- target wall clock: less than 10 minutes

### Non-Required CI

- `Extension Conformance`
- `Fuzz CI`
- semver checks
- benchmarks
- long shard-based integration runs
- evidence refresh / weekly jobs

These remain available, but they are not part of the minimum PR gate until
their runtime and ownership are re-justified.

## Sprint Structure

## Sprint 0 - Restore Trust In `main`

### Deliverables

- complete the `fix/revert-unauthorized-main-20260702` PR
- confirm `main` returns to the pre-leak state
- freeze further `just`/CI implementation work on `main`
- declare `plan/just-integration` as the planning branch and future
  implementation source

### Acceptance Criteria

- `main` no longer contains the five unauthorized commits from 2026-07-02
- the revert lands as ordinary history, not a force-push rewrite
- a short branch note exists linking:
  - the revert PR
  - this planning folder
  - the future implementation branch

### Required Validation

- `git log --oneline eecf8253..main` on updated `main`
- GitHub branch view confirms the revert PR merged
- no new direct commits appear on `main`

### Out of Scope

- no `just` implementation
- no CI redesign

### Dependencies

- none

## Sprint 1 - Install The Minimal `sc-just` Rust Skeleton

### Deliverables

- add the `sc-just` Rust-template-shaped root `justfile`
- add a dedicated root `.just/` folder
- keep the initial helper set narrow:
  - `print_help.py`
  - `run_fmt.py`
  - `run_lint.py`
  - minimal config and lane metadata
- create the dedicated root-level fork docs folder now used by this plan

### Acceptance Criteria

- `just help` works
- `just fmt check` works
- `just lint` works with local-code-only scope
- no application code, tests, or existing CI workflows are changed in this
  sprint beyond wiring the new command surface

### Required Validation

- `just help`
- `just fmt check`
- `just lint fmt`
- `just lint clippy-lib`
- `just lint clippy-bins`

### Out of Scope

- no `just test*` lanes yet
- no PR CI changes yet

### Dependencies

- Sprint 0

### Notes

- Start from the `sc-just` Rust template shape, not from the larger `atm-core`
  lint inventory.
- Repo-specific commands belong in data/config where possible, not in the
  `Justfile`.

## Sprint 2 - Define Test SSOT And Explanatory Surface

### Deliverables

- one authoritative test lane catalog under `.just/`
- one authoritative lint lane catalog under `.just/`
- `just suites`
- `just explain lint [lane]`
- `just explain test [lane]`
- written mapping from each `just test*` lane to the exact underlying command
  path

### Acceptance Criteria

- every `just test*` lane resolves from a single data source
- no duplicate hard-coded command lines exist for the same lane
- the distinction between:
  - inline lib tests
  - `suite.unit`
  - `suite.vcr`
  - `suite.e2e`
  is documented and visible via `just explain`

### Required Validation

- `just suites`
- `just explain lint`
- `just explain test`
- targeted dry-run or safe invocation checks for each lane resolver

### Out of Scope

- no required PR workflow changes yet
- no new tests

### Dependencies

- Sprint 1

## Sprint 3 - Add Fast Local Test Lanes And Smoke Baseline

### Deliverables

- `just test baseline`
- `just test unit`
- `just test integration`
- `just test vcr`
- `just test e2e`
- `just test all`
- one smoke script or runner that remains intentionally small and
  non-destructive
- fail-fast error messages that name:
  - the failing lane
  - the source-of-truth file
  - the next document/script to inspect

### Acceptance Criteria

- `just test baseline` completes successfully on a developer machine without
  needing the entire repo CI graph
- `just test` maps to the intended local CI-equivalent lane
- `just test all` is explicitly documented as broader than default PR CI
- `just test*` paths do not mutate tracked evidence directories by default

### Required Validation

- successful local runs of:
  - `just test baseline`
  - `just test unit` or a clearly documented bounded substitute if the repo
    cannot yet complete it
- update `fork-hardening/testing-strategy.md` with measured timings

### Out of Scope

- no broad workflow redesign beyond baseline prerequisites
- no fuzz / semver / bench in `just test`

### Dependencies

- Sprint 2

## Sprint 4 - Replace Monolithic PR CI With Fast Baseline

### Deliverables

- add or restore a dedicated `.github/workflows/baseline.yml`
- reduce required PR CI to the fast baseline workflow
- move monolithic `ci` work out of required PR gating
- make the workflow mirror `just` lanes instead of shelling bespoke commands

### Acceptance Criteria

- required PR workflow finishes in less than 10 minutes on GitHub-hosted Linux
- workflow steps correspond directly to local commands:
  - `just fmt check`
  - `just lint clippy-lib`
  - `just lint clippy-bins`
  - `just test baseline`
- the workflow fails at the first actionable gate and does not continue into
  slow downstream work

### Required Validation

- one green PR run of `baseline`
- step timing recorded in `fork-hardening/testing-strategy.md`

### Out of Scope

- no full cross-platform CI in required PR gating
- no fuzz, semver, bench, or weekly evidence refresh in required PR gating

### Dependencies

- Sprint 3

## Sprint 5 - Reintroduce Extended Lanes Outside Required PR CI

### Deliverables

- classify each remaining workflow/job as one of:
  - required PR
  - optional PR/manual
  - nightly/scheduled
  - branch-specific or feature-specific
- define ownership and entry points for:
  - `Extension Conformance`
  - `Fuzz CI`
  - semver
  - benchmarks
  - evidence refresh

### Acceptance Criteria

- every surviving workflow has a documented reason to exist
- every surviving workflow has a corresponding local command or a written reason
  why no local mirror exists
- workflows that exceed the PR budget are not required for ordinary fork PRs

### Required Validation

- documentation review against live workflow files
- at least one manual or scheduled success run for each retained long lane

### Out of Scope

- no expansion of required PR CI budget

### Dependencies

- Sprint 4

## Sprint 6 - Merge Baseline Into `atm-graft` Work And Add New Coverage

### Deliverables

- merge the stabilized `just` + baseline CI layer into the
  `feature/atm-graft-integration` worktree
- add tests for `atm-graft` additions using the stabilized lane taxonomy
- keep new `atm-graft` tests classified correctly from the start

### Acceptance Criteria

- `atm-graft` branch reuses the same `just` and CI surfaces
- new `atm-graft` tests are placed in the right suite with no VCR/classification
  leakage
- branch CI remains within the bounded baseline model

### Required Validation

- green baseline PR run on the merged `atm-graft` branch
- targeted local lane runs for new `atm-graft` test files

### Out of Scope

- no re-expansion into monolithic CI

### Dependencies

- Sprint 5

## Open Questions For Jen

These are intentionally unresolved here.

1. Should `pi_agent_atm` adopt only the narrow `sc-just` Rust-template surface,
   or should it also adopt a persistent config-first layer like
   `.just/config.toml` from the outset?
2. Should `just test` map to the current `verify --profile ci --skip-lint`
   behavior, or should `verify` be treated as an implementation detail that a
   new slimmer runner may replace later?
3. Should `Extension Conformance` remain a separate workflow for fork PRs, or
   should it move fully to manual/nightly once the fork baseline is stable?
4. Should cross-platform validation be part of baseline for this fork, or only a
   follow-on lane once Linux baseline is consistently green?
5. Should the smoke baseline remain a script (`scripts/smoke.sh`) or move into a
   Python helper so its target list lives in the same catalog system as other
   `just` lanes?
6. Is the long-term standard folder name for fork-specific planning docs
   `fork-hardening/`, or should a broader cross-repo namespace be adopted later?

## Risks And Controls

| Risk | Control |
|---|---|
| Repeating the prior branch's scope creep | No `src/**` or broad test edits during Sprints 1-4 unless separately reviewed |
| Reintroducing multiple command paths for the same lane | Catalog-backed SSOT before workflow wiring |
| Required PR CI grows back above 10 minutes | Budget gate in Sprint 4 acceptance criteria |
| Cross-platform/macOS breakage gets rediscovered late | Track platform issues in `testing-strategy.md` from Sprint 2 onward |
| Future upstream merges become painful | Keep planning and fork-ops docs in `fork-hardening/` at repo root |

## Exit Criteria

This recovery plan is complete when all of the following are true:

- `main` is restored via the revert PR
- `just` exists in a narrow, reviewable form derived from `sc-just`
- `just test` and required PR CI share the same lane definitions
- required PR CI is under 10 minutes
- long-running workflows are explicitly non-required and documented
- `atm-graft` work can build on the stabilized baseline instead of the abandoned
  exploratory branch
