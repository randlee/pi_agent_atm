# Just Integration Plan

Date: 2026-07-03
Branch: `feature/just-integration`
Status: draft

## Purpose

This document captures the integration plan requested by team-lead for adding a
repo-local `just` task surface to `pi_agent_atm`. It is intentionally scoped to:

- the `sc-just` package guidance
- the existing `atm-core` `Justfile` / `.just/` pattern
- the current exploratory `feature/just-integration` branch

It does not resolve open product or QA policy questions that belong to jen.
Those are listed explicitly instead of being guessed at here.

## Evidence Reviewed

### `sc-just` package

- `packages/sc-just/skills/setting-up-just/SKILL.md`
- `packages/sc-just/skills/setting-up-just/references/adoption-workflow.md`
- `packages/sc-just/skills/setting-up-just/references/template-catalog.md`
- `packages/sc-just/skills/setting-up-just/assets/templates/rust/Justfile`

Key constraints from that package:

- keep the root `Justfile`/`justfile` thin
- move orchestration into `.just/*.py` once recipes stop being trivial
- prefer repo-specific command wiring over helper rewrites
- reuse existing scripts instead of re-implementing them inside `just`
- verify with safe commands first (`just help`, formatting, lint, test)

### `atm-core` reference

- `/Volumes/Extreme Pro/github/atm-core/Justfile`
- `/Volumes/Extreme Pro/github/atm-core/.just/*`

Observed `atm-core` pattern:

- readable top-level task file with small recipe names
- private recipes for low-level invocations
- Python helpers under `.just/` for dispatch and argument validation
- repo-specific lint/test/view logic delegated out of the task file
- `ci` recipe composed from smaller stable entry points

### Current exploratory branch

- `justfile`
- `.just/print_help.py`
- `.just/run_fmt.py`
- `.just/run_lint.py`
- `.just/run_test.py`
- `.just/run_cargo.py`
- `.just/lint_catalog.py`
- `.just/test_catalog.py`
- `.just/show_suites.py`
- `.just/explain.py`
- `.github/workflows/baseline.yml`
- `docs/just-verification-macos.md`

Observed branch facts:

- the branch already proves that a thin `just` dispatch layer works in this repo
- the branch also mixes in broad CI/test-policy decisions and unrelated source
  changes, so it is not a safe merge-wholesale candidate
- the current baseline workflow on this branch is `fmt + clippy-lib +
  clippy-bins + smoke`, which is evidence of a working shape but not itself the
  authoritative final gate policy

## Recommended Integration Approach

### 1. Treat `just` as a dispatch layer, not as new policy

Integrate `just` by standardizing entry points that call existing repo commands
and scripts. Do not couple initial adoption to new test taxonomy, new lint
policy, or broad workflow surgery unless those decisions already have separate
approval.

Practical implication:

- reuse `cargo fmt`, `cargo clippy`, `cargo test`, `./verify`, and existing
  scripts where they are already the source of truth
- keep the `just` layer responsible for naming, composition, and basic argument
  routing
- keep QA scope decisions outside the task runner unless a separate policy doc
  names them

### 2. Promote only the `just` seam from this branch

The exploratory branch shows the right seam, but too much unrelated surface is
mixed into it. Promotion should happen by selecting the `just`-specific files,
not by merging the whole branch.

Promotion candidates from this branch:

- `justfile`
- `.just/print_help.py`
- `.just/run_fmt.py`
- `.just/run_lint.py`
- `.just/run_test.py`
- `.just/run_cargo.py`
- `.just/lint_catalog.py`
- `.just/test_catalog.py`
- `.just/show_suites.py`
- `.just/explain.py`

Files that need separate review before any adoption:

- `.github/workflows/*.yml`
- `scripts/smoke.sh`
- `tests/suite_classification.toml`
- any `src/**` or `tests/**` logic changes unrelated to dispatch

### 3. Keep the top-level task file close to the `atm-core` pattern

The `atm-core` pattern is the correct structural reference:

- top-level recipe names stay short and stable
- helper scripts own branching logic
- private recipes isolate raw Cargo or shell calls
- composition stays visible at the top level

For this repo, the stable user-facing surface should remain in the familiar
family:

- `help`
- `fmt`
- `lint`
- `test`
- `ci`
- optional repo-specific extras such as `bench` or `suites`

### 4. Prefer a reusable cargo runner helper

This branch’s `.just/run_cargo.py` is a useful seam because it centralizes:

- `cargo` invocation shape
- optional `rch exec -- ...` wrapping
- shared environment handling for task-runner commands

That is strategically important once additional local crates are layered into
`pi_agent_atm`, because it gives one place to evolve workspace-wide invocation
rules instead of duplicating them across recipes.

### 5. Separate lane catalogs from execution

The current branch already separates:

- lint lane definitions in `.just/lint_catalog.py`
- test lane definitions in `.just/test_catalog.py`
- execution in `.just/run_lint.py` / `.just/run_test.py`

That split should be preserved. It is the cleanest way to:

- keep help output and behavior aligned
- let lane naming evolve without rewriting the dispatcher
- support future crate additions with minimal disruption

### 6. Define regression checks around equivalence, not around wrapper code

The integration should prove that `just` does not introduce regression by
checking wrapper equivalence against the underlying commands it dispatches.

Minimum verification framework:

- `just help` renders the intended lane surface
- `just fmt check` matches direct `cargo fmt --all --check`
- each `just lint ...` lane maps to a known direct command
- each `just test ...` lane maps to a known direct command or script
- CI workflows call `just`, but the underlying payload remains traceable to
  pre-existing commands

This keeps upstream regression analysis focused on behavior, not on whether a
wrapper exists.

## Layering Framework For Future Local Crates

The `just` surface should be one of the tools that keeps local additions
layered on top of the upstream fork instead of scattering repo-specific policy.

Recommended framework:

### A. Keep workspace growth behind lane catalogs

When new crates are added, extend lane catalogs rather than editing many
workflow files or adding ad hoc commands.

Examples of the intended layering seam:

- add new crate-aware lint slices in `.just/lint_catalog.py`
- add new crate-aware test slices in `.just/test_catalog.py`
- keep `justfile` recipe names stable

### B. Keep workflow jobs thin

GitHub Actions should call a small set of `just` entry points instead of
re-encoding Cargo/test logic in YAML. That reduces drift between local and CI
execution when new crates land.

### C. Preserve an upstream-verifiable baseline

To show that local crates do not regress the upstream fork, keep at least one
baseline lane defined only in terms of upstream-safe checks. Local-crate lanes
can be added alongside it rather than replacing it.

The exact baseline contents are a policy decision for jen, but the structural
rule should be:

- one documented baseline lane for upstream-regression confidence
- additional lanes for local-crate coverage
- each lane declared in one catalog source of truth

## Open Questions For Jen

These questions affect policy or repo direction and should not be guessed at in
implementation:

1. Should this repo standardize on `Justfile` to match `atm-core` and the
   `sc-just` template, or keep the already-working lowercase `justfile`?

2. Should repo-specific lane configuration stay in Python catalogs, or should
   part of it move into a `.just/config.toml` layer closer to the generic
   `sc-just` package model?

3. What is the authoritative required CI baseline for this fork:
   compile/unit-first, smoke-first, or a staged sequence where the baseline
   changes by sprint?

4. Which test taxonomy source is authoritative for `just test` lanes:
   `./verify` profiles, `tests/suite_classification.toml`, or a new documented
   audit artifact?

5. How should future local crates be represented:
   folded into existing workspace-wide lanes, or exposed as separate
   crate-specific lanes for phased rollout?

6. Is Windows parity in scope for the first adoption round, or is the initial
   requirement Linux/macOS only?

7. Should CI always invoke `cargo` directly in hosted runners, or should the
   task-runner layer preserve optional `rch` wrapping semantics only for local
   use?

## Dependencies

Known implementation dependencies:

- `just >= 1.0`
- `python3 >= 3.11`
- a checked-in root task file plus `.just/` helper directory
- an agreed authoritative test/lint policy outside the task runner itself
- stable underlying repo entry points (`cargo`, `./verify`, existing scripts)
- CI workflow ownership for whichever jobs will switch to `just`

## Suggested Execution Order

This is the safest order for actual implementation work once jen resolves the
open questions:

1. land the thin task-runner skeleton only
2. wire `help`, `fmt`, and one or two uncontroversial lint/test entry points
3. prove command equivalence locally
4. switch one CI workflow to the new entry points
5. expand lane catalogs only after the authoritative test policy is settled

## Non-Goals

This plan does not recommend:

- merging the exploratory branch wholesale
- treating current branch timings as final gate policy
- changing core repo testing policy inside the task-runner workstream
- inventing unresolved crate-layering or CI-policy decisions without jen
