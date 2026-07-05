# Just Integration Plan

Date: 2026-07-05
Branch: `feature/just-integration`
Status: draft

## Purpose

This document is the constrained planning output requested by team-lead for
integrating a repo-local `just` task runner into `pi_agent_atm`.

It is intentionally limited to:

- the `sc-just` package guidance
- the established `atm-core` `Justfile` / `.just/` design pattern
- the currently explored `feature/just-integration` branch as a reference,
  not as a merge-wholesale candidate

It does not settle unresolved product, CI-policy, or layering decisions that
belong to jen. Those decisions are called out explicitly as decision gates.

## Output Boundary

This plan is for adoption sequencing and file selection only.

It is not:

- a request to merge `feature/just-integration` wholesale
- approval to change required CI policy
- approval to redefine test taxonomy
- approval to standardize future ATM crate layering details without jen

## Evidence Reviewed

### `sc-just` package

- `packages/sc-just/skills/setting-up-just/SKILL.md`
- `packages/sc-just/skills/setting-up-just/references/adoption-workflow.md`
- `packages/sc-just/skills/setting-up-just/references/template-catalog.md`
- `packages/sc-just/skills/setting-up-just/assets/templates/rust/Justfile`

Observed package rules:

- keep the root `Justfile` thin and readable
- move orchestration into `.just/*.py` once recipes stop being trivial
- prefer adapting repo-specific command wiring before rewriting helpers
- reuse existing scripts rather than re-implementing them inside recipes
- verify safe entry points first: `just help`, formatting, lint, test
- prefer the `atm-core` shape for Cargo-first repositories

### `atm-core` reference

- `/Volumes/Extreme Pro/github/atm-core/Justfile`
- `/Volumes/Extreme Pro/github/atm-core/.just/*`

Observed `atm-core` pattern:

- small stable top-level recipe names
- private low-level recipes for raw invocations
- Python dispatch helpers under `.just/`
- repo-specific policy logic delegated out of the task file
- `ci` composed from smaller stable entry points
- broad repository-specific policy encoded in helpers, not in YAML duplication

### Current `feature/just-integration` branch

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

- the branch demonstrates that a thin `just` surface is viable in this repo
- the branch also contains broader CI, test-surface, and unrelated source
  changes, so it is a reference branch, not an integration vehicle
- the branch diverges from the generic `sc-just` package shape by using Python
  catalogs instead of `.just/config.toml`
- the branch uses lowercase `justfile`, while both `sc-just` and `atm-core`
  use `Justfile`

## Ground Truth Summary

The available references support these conclusions without guessing:

1. `pi_agent_atm` is a Cargo-first repo, so the `sc-just` Rust template is the
   correct baseline reference.
2. `atm-core` is the correct structural style reference for recipe shape and
   helper delegation.
3. `feature/just-integration` contains a usable extraction seam for a `just`
   surface, but it is too broad to merge wholesale safely.
4. The safe plan is to adopt a bounded task-runner layer first, then let jen
   decide which policy-bearing lanes should become authoritative.

## Planning Constraints

These are the non-negotiable constraints this plan should preserve:

- the `just` layer must unify existing commands, not invent new test policy
- the root task file must stay thin
- repo-specific behavior should live in `.just/*.py`
- existing scripts such as `./verify` and `scripts/smoke.sh` remain the payload
  where already authoritative
- CI should call `just` entry points only after local equivalence is proven
- upstream-regression confidence must remain separable from ATM-owned additions

## Recommended Integration Approach

### 1. Treat `just` as a naming and dispatch layer

The initial adoption should standardize local entry points without bundling in
new policy.

Safe meaning of this rule:

- `just` names commands consistently
- `just` composes existing repo entry points
- `just` does not by itself decide what the required CI baseline should be
- `just` does not by itself decide whether `verify` or suite catalogs are the
  final test taxonomy authority

### 2. Extract only the `just` seam from the exploratory branch

Promotion should happen by selective file extraction, not by merging the whole
branch.

Safe promotion candidates:

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

Files that require separate policy review before adoption:

- `.github/workflows/*.yml`
- `scripts/smoke.sh`
- `verify`
- `tests/suite_classification.toml`
- any `src/**` or `tests/**` changes unrelated to task-runner dispatch

### 3. Keep the top-level task surface minimal and stable

The stable surface should remain a small family of recipes, close to
`atm-core`, regardless of later lane growth:

- `help`
- `fmt`
- `lint`
- `test`
- `ci`
- optional informational helpers such as `explain` or `suites`

This minimizes churn when the underlying lane catalog changes.

### 4. Preserve catalog-driven lane definitions if jen approves them

The exploratory branch’s separation between catalog definitions and execution is
structurally strong:

- lint lanes in `.just/lint_catalog.py`
- test lanes in `.just/test_catalog.py`
- dispatch in `.just/run_lint.py` and `.just/run_test.py`
- explanation/reporting in `.just/explain.py` and `.just/show_suites.py`

This is a good fit for a repo with multiple distinct test surfaces, but the
decision to keep catalogs instead of moving some configuration into
`.just/config.toml` belongs to jen.

### 5. Reuse a shared cargo runner helper

The branch’s `.just/run_cargo.py` is the right central seam for:

- optional `rch exec -- ...` wrapping
- shared environment shaping
- future workspace-wide cargo invocation rules

That is strategically useful once additional crates are layered into
`pi_agent_atm`, because it keeps cargo behavior centralized instead of
duplicated across recipes.

### 6. Define success in terms of command equivalence

The integration should prove that `just` wraps existing behavior correctly.

Minimum equivalence expectations:

- `just help` renders the intended surface
- `just fmt check` matches direct formatting gate behavior
- each `just lint ...` lane maps to an explicit underlying command
- each `just test ...` lane maps to an explicit underlying command or script
- any CI workflow that later switches to `just` remains traceable back to the
  same underlying repo command surface

## Proposed Adoption Phases

These are execution phases, not pre-approved code decisions. Any phase that
depends on an unresolved decision gate waits for jen.

### Phase 0 — Decision framing

Goal:

- settle the few design choices that materially affect file shape

Deliverable:

- jen answers the decision-gate questions listed below

Why first:

- otherwise the implementation agent will end up re-deciding policy while
  copying files

### Phase 1 — Thin task-runner skeleton only

Scope:

- root task file
- `.just/print_help.py`
- `.just/run_fmt.py`
- `.just/run_cargo.py` if needed immediately

Recommended command surface at this phase:

- `just help`
- `just fmt`
- `just fmt check`
- `just fmt write`

Guardrail:

- no CI workflow switch yet
- no broad lane taxonomy promotion yet

### Phase 2 — Minimal safe lint/test entry points

Scope:

- add only the least controversial dispatch surfaces
- prefer one or two lanes whose underlying commands are already stable

Examples of safe early candidates:

- one default `just lint`
- one default `just test`

Guardrail:

- no attempt to solve every repo test mode in the first adoption round
- no broad policy interpretation embedded in recipe names

### Phase 3 — Local equivalence proof

Scope:

- run direct-command vs `just` equivalence checks
- verify that wrappers do not alter command payload semantics

Deliverable:

- a short verification note or checked-in report showing the wrapper is
  behaviorally faithful

### Phase 4 — First CI consumer

Scope:

- switch one workflow or one job from raw command strings to the approved
  `just` surface

Guardrail:

- do not migrate every workflow at once
- do not use CI migration to smuggle in new required gates

### Phase 5 — Lane expansion and layering

Scope:

- only after jen settles taxonomy and crate-layering questions
- extend lane catalogs or helper configuration for broader surfaces

This is the phase where crate-aware or seam-aware lanes would grow, if approved.

## Decision Gates For Jen

These are the issues that should not be guessed at by the implementation agent.

### 1. `Justfile` vs lowercase `justfile`

Observed conflict:

- `sc-just` and `atm-core` use `Justfile`
- the exploratory branch uses `justfile`

Need from jen:

- the canonical filename to standardize on

Why it matters:

- avoids avoidable drift between this repo and the reference pattern

### 2. Catalogs vs `.just/config.toml`

Observed conflict:

- `sc-just` prefers generic helpers plus `.just/config.toml`
- this branch uses Python catalogs as the repo-specific source of truth

Need from jen:

- whether this repo should keep the catalog model
- or move part of the configuration into a TOML layer closer to `sc-just`

Why it matters:

- determines whether helper extraction should preserve current branch structure
  or refactor it

### 3. Authoritative default `test` lane meaning

Observed conflict:

- branch default `test` target is `ci`
- multiple possible authorities exist: `./verify`, `tests/suite_classification.toml`,
  smoke scripts, or a future audited contract

Need from jen:

- what `just test` is allowed to mean in this repo

Why it matters:

- changing that meaning later creates the most user-visible churn

### 4. CI baseline policy

Need from jen:

- whether the first CI consumer should be formatting-only, compile/test, smoke,
  or another explicitly approved subset

Why it matters:

- the task runner should not encode branch-policy decisions by accident

### 5. Future ATM crate lane model

Need from jen:

- whether future ATM-owned crates should be absorbed into workspace-wide lanes
  or exposed first as explicit crate-specific or seam-specific lanes

Why it matters:

- determines whether lane catalogs need origin/owner metadata early

### 6. Platform scope for first adoption

Need from jen:

- whether first-round support must cover Linux + macOS + Windows, or whether
  Linux/macOS first is acceptable

Why it matters:

- affects helper branching and verification burden immediately

## Dependencies

Hard dependencies:

- `just >= 1.0`
- `python3 >= 3.11`
- one canonical task file name chosen by jen
- stable underlying repo commands worth wrapping
- CI owner agreement for the first workflow/job migration

Soft dependencies:

- clearer authoritative test taxonomy
- clarified platform support target
- clarified future ATM crate layering expectations

## Safe File Selection Framework

If implementation starts from this branch, file selection should follow this
rule:

1. copy the smallest file subset that provides the approved task surface
2. preserve existing repo payload commands instead of rewriting them
3. refuse unrelated `src/**`, `tests/**`, or workflow changes unless a
   separate decision gate already approved them

This is the core protection against pulling exploratory branch drift into the
mainline.

## Handoff Checklist For The Implementing Agent

Before code changes begin, the implementing agent should have:

- this plan
- jen’s answers to the decision gates
- the exact file allowlist for the adoption slice
- the direct underlying commands each `just` lane is allowed to wrap
- the first CI consumer scope

If any of those are missing, implementation should stop and escalate rather
than improvise architecture.

## Suggested Execution Order

Once jen answers the decision gates, the safest order is:

1. choose canonical filename: `Justfile` or `justfile`
2. decide whether catalogs stay or partially collapse into `.just/config.toml`
3. extract the thin task-runner skeleton only
4. wire the minimal approved lint/test entry points
5. verify local command equivalence
6. migrate one approved CI consumer
7. expand lane coverage only after the baseline task-runner adoption is proven

## Non-Goals

This plan does not recommend:

- merging `feature/just-integration` wholesale
- standardizing current exploratory branch CI policy as final
- redefining repo test taxonomy inside the task-runner workstream
- guessing at ATM crate layering policy
- broad workflow rewrites as part of the initial `just` adoption
