## Just Layering And ATM Integration Strategy

Date: 2026-07-03
Scope: define a durable `just` and repository-layering strategy so Phase A can
start with a minimal upstream-regression gate and later absorb ATM-owned code
without broad churn in the upstream fork.

## Current Repo Reality

- the repository is still a single root package in `Cargo.toml`
- there is no active Cargo workspace member layout yet
- the current ATM integration model already being developed in
  `feature/atm-graft-integration` uses root-package dependency edges to
  `atm-core` crates plus a local shim in `vendor/atm-daemon-bootstrap-shim`
- Phase A therefore must stabilize operator and CI semantics first, then layer
  additional crates additively instead of rewriting the fork boundary

## Just Strategy

The top-level operator surface should stay fixed:

- `just help`
- `just fmt`
- `just lint`
- `just test`
- `just explain`
- `just suites`

Future growth should happen through lane catalogs, not new top-level commands.

Lane classes:

1. upstream baseline lanes
   - purpose: prove the fork still behaves like the audited upstream baseline
   - examples: `compile`, `unit-basic`, `baseline`, `clippy-bins`,
     `clippy-lib`
   - rule: lane semantics stay stable once Phase A freezes them
2. ATM-owned lanes
   - purpose: prove behavior in new ATM-owned crates or adapters
   - examples: future `atm-*` lint and test lanes
   - rule: start as local/manual lanes and only become required after timing
     evidence and explicit approval
3. seam or integration lanes
   - purpose: prove the root fork still integrates correctly with ATM crates
   - examples: future `integration-*` lanes
   - rule: these augment upstream proof; they do not replace it

Recommended lane metadata for `.just/lint_catalog.py` and
`.just/test_catalog.py`:

- `origin`: `upstream`, `atm`, or `integration`
- `owner`: concrete owner module or crate
- `blocking`: `required`, `local`, `manual`, or `scheduled`
- `paths`: primary source paths covered by the lane
- `promotion_rule`: evidence needed before a lane can move into required PR CI

`just explain` should surface this metadata so operators can tell whether a
lane protects upstream parity, ATM-owned code, or the seam between them.

## Regression Framework

Required rules once ATM-owned code starts landing:

1. every PR still runs the upstream required baseline
2. any PR touching the ATM dependency wiring or local shim surfaces also runs
   the relevant ATM-owned lane set
3. any PR touching the seam between the root package and ATM-owned
   dependencies also runs the relevant integration lanes
4. no ATM-specific lane may weaken or silently redefine the meaning of the
   upstream baseline lanes

This keeps "no regression from upstream fork" measurable even while the code
base becomes more ATM-specific.

## Repository Layering Target

To minimize disruption to the upstream code base:

- keep the upstream fork boundary in the existing root package for Phase A
- treat `feature/atm-graft-integration` as the source of truth for the planned
  ATM layering surface during Phase A
- prefer ATM integration through explicit root `Cargo.toml` dependency edges
  such as `atm-graft` and `atm_core`, plus narrowly scoped vendor shims when
  needed
- keep any repo-local ATM glue bounded to the small set of integration files
  that wire those dependencies into the upstream binary/library surface rather
  than scattering ATM-specific logic through unrelated upstream modules
- keep cross-package seam tests under `tests/integration_*` or
  `tests/atm_*`, separate from the upstream baseline allowlist

Practical interpretation:

- ATM-owned business logic should continue to live in the `atm-core` line
  unless there is a separately approved reason to move it into this repo
- root-package edits here should stay thin and mostly wire ATM-owned
  dependencies into the upstream binary/library surface
- if an ATM feature requires broad edits across upstream files, treat that as a
  design smell and justify it explicitly before implementation

## Phase-A Planning Implications

- Sprint A1 should establish the upstream baseline lanes and prove displaced
  upstream workflows remain manually runnable
- Sprint A4 should teach helper output to expose lane origin/ownership metadata
- Sprint A5 should allow optional local ATM or integration lanes without
  changing required PR CI
- Sprint A6 should freeze the lane taxonomy and layering rules before the
  baseline merges into `feature/atm-graft-integration`
