# Phase A - Testing Strategy

Date: 2026-07-03
Status: approved

## Purpose

Define the specific testing strategy that Phase A will implement so every
increment starts from something working, required PR CI stays under 10 minutes,
and local commands and CI share one source of truth.

## Strategy Rules

1. `just` is the only public local operator surface.
2. Required PR CI is exactly one workflow: `baseline`.
3. Required PR CI runs `just ...` commands, not bespoke cargo command strings.
4. Every sprint preserves green `baseline` CI.
5. Heavyweight workflows do not run on ordinary PRs after Sprint A1 lands.
6. Compile checking and strict basic-unit coverage come before lint expansion
   and smoke expansion.
7. Lint in required PR CI covers only code we own.
8. Broad tests, fuzz, semver, benchmarks, and evidence refresh remain outside
   required PR CI.
9. Do not invent new top-level `just` commands for Phase A. Use the established
   `just help`, `just fmt`, `just lint`, `just test`, `just explain`, and
   `just suites` surfaces only.
10. Future ATM-owned lanes must be additive and must not silently redefine the
    semantics of the upstream baseline lanes established in Phase A.
11. Future ATM-owned integration in this repo should follow the actual
    `feature/atm-graft-integration` dependency model and bounded seam files
    rather than broad rewrites across upstream-owned files.

## Fork And Upstream Audit Baseline

This repository is a fork of the public upstream
`Dicklesworthstone/pi_agent_rust`.

Phase A must treat the existing upstream workflow/test surface as a known risk
inventory, not as disposable noise. The current upstream ordinary-PR workflows
and what they prove are:

| Workflow | Current PR trigger shape | What it proves today | Phase A handling |
|---|---|---|---|
| `ci.yml` | all PRs | cross-OS compile/test/policy guard with DoD evidence checks | remove from ordinary PRs in A1, retain manual trigger |
| `conformance.yml` | all PRs | extension/runtime compatibility matrix, sibling-repo checkout health, Bun/npm legacy compatibility | remove from ordinary PRs in A1, retain manual and scheduled triggers |
| `fuzz.yml` | PRs targeting `main` | Linux fuzz smoke across selected targets | remove from ordinary PRs in A1, retain manual and scheduled triggers |
| `bench.yml` | all PRs | benchmark execution surface kept outside required gating | remove from ordinary PRs in A1, retain manual trigger |
| `semver.yml` | path-filtered PRs touching Rust/API surfaces | public API SemVer compatibility | remove from ordinary PRs in A1, retain manual trigger |
| `model-catalog-drift.yml` | path-filtered PRs touching generator/catalog inputs | Node-based catalog drift detection, advisory today | remove from ordinary PRs in A1, retain manual and scheduled triggers |

Key upstream-specific unknowns that must stay visible throughout Phase A:

- `conformance.yml` depends on sibling repositories (`asupersync`,
  `rich_rust`, `charmed_rust`, `sqlmodel_rust`) and Bun/npm installation.
- `ci.yml` is the only current cross-OS PR guard.
- `semver.yml` and `model-catalog-drift.yml` are path-filtered specialty gates,
  not generic test lanes.
- the suite taxonomy and logging/evidence contract live upstream in
  `docs/testing-policy.md` and `tests/suite_classification.toml`; Phase A may
  narrow fast gating, but it may not redefine those upstream contracts casually.

Mandatory A1 precondition:

- before ordinary-PR triggers are removed, this strategy document must already
  describe every currently PR-triggered workflow, why it is leaving the
  required gate, and what trigger path remains for it afterward

## Evidence Reports

Supporting evidence for this strategy lives in:

- `reports/pi-agent-rust/local-test-surface-review-2026-07-03.md`
- `reports/pi-agent-rust/upstream-testing-contract-review-2026-07-03.md`
- `reports/pi-agent-rust/just-layering-and-atm-integration-strategy-2026-07-03.md`
- `docs/plans/phase-A/unit-basic-inline-taxonomy.tsv`

## Steady-State Required PR Baseline

Steady-state `baseline` contents from Sprint A3 onward:

1. `just fmt check`
2. `just test compile`
3. `just test unit-basic`
4. `just lint clippy-bins`
5. `just lint clippy-lib`
6. `just test baseline`

Hard budget:

- total wall clock under 10 minutes

Per-step budget targets:

- `just fmt check`: under 30 seconds
- `just test compile`: under 90 seconds
- `just test unit-basic`: under 120 seconds
- `just lint clippy-bins`: under 30 seconds
- `just lint clippy-lib`: under 3 minutes
- `just test baseline`: under 3 minutes

These are budget allocations, not historical facts. Sprint validation must
measure and refresh them as each step is added.

## Incremental Rollout By Sprint

Required PR CI contents per sprint:

| Sprint | Required `baseline` contents |
|---|---|
| A1 | `just help`, `just fmt check`, `just test compile`, `just test unit-basic` |
| A2 | A1 + `just lint clippy-bins`, `just lint clippy-lib` |
| A3 | A2 + `just test baseline` |
| A4 | same as A3 |
| A5 | same as A3 |
| A6 | same as A3 |
| A7 | same as A3 on merge PRs |

This table is the controlling rollout rule. If a sprint would require more
than the listed contents, the plan is being violated.

Important interpretation:

- Sprint A1 intentionally starts with a small green gate.
- That green gate is only acceptable because the displaced upstream PR
  workflows remain available by explicit non-PR triggers and are documented in
  this strategy.
- The small gate is still required to prove compile health and strict
  basic-unit health first.
- A1 is a gate-reduction sprint, not a claim that the fork's broader testing
  unknowns have been solved.

## Source Of Truth Policy

Target end state:

- `justfile` is the command surface
- `.just/lint_catalog.py` defines lint lanes
- `.just/test_catalog.py` defines test lanes
- `.just/explain.py` explains lane semantics
- `.just/show_suites.py` reports suite taxonomy from
  `tests/suite_classification.toml`
- the required `baseline` workflow invokes only `just ...` commands

One lane, one owner:

- format lane:
  - owner: `justfile` + `.just/run_fmt.py`
- lint lane:
  - owner: `.just/lint_catalog.py`
- test lane:
  - owner: `.just/test_catalog.py`

## Just Layering Framework For ATM Additions

Phase A needs a `just` design that stays useful after ATM-owned crates begin
landing. The stable top-level operator surface remains:

- `just help`
- `just fmt`
- `just lint`
- `just test`
- `just explain`
- `just suites`

Growth happens through lane catalogs, not new top-level commands.

Future lane families:

- upstream baseline lanes:
  - preserve the audited fork-regression contract
  - current examples: `compile`, `unit-basic`, `baseline`, `clippy-bins`,
    `clippy-lib`
- ATM-owned lanes:
  - cover new ATM crates or modules we own
  - should use explicit lane ids such as `atm-*`
- seam or integration lanes:
  - cover the boundary between upstream fork code and ATM-owned additions
  - should use explicit lane ids such as `integration-*`

Promotion rule:

- upstream baseline lanes are stable once Phase A freezes them
- new ATM-owned or integration lanes start as local/manual lanes
- they move into required PR CI only after timing evidence and team-lead review
- no ATM-owned lane may replace the upstream baseline requirement

Recommended catalog metadata for future hardening:

- `origin`: `upstream`, `atm`, or `integration`
- `owner`: owning crate or module
- `blocking`: `required`, `local`, `manual`, or `scheduled`
- `paths`: primary source paths the lane protects
- `promotion_rule`: evidence required before the lane can become blocking

`just explain` should eventually print this metadata so operators can tell
whether a lane protects upstream parity, ATM-owned code, or the seam between
them.

## Repository Layering Framework For ATM Additions

Current repo reality:

- the fork is still a single root package in `Cargo.toml`
- there is no active workspace-member layout yet
- the planned ATM integration surface already exists on
  `feature/atm-graft-integration` as root-package dependency wiring to
  `atm-core` crates plus a local vendor shim

Planning target for minimum upstream disruption:

- keep the existing root package as the upstream fork boundary through Phase A
- use `feature/atm-graft-integration` as the concrete reference for ATM
  layering decisions during Phase A
- prefer explicit root `Cargo.toml` dependency edges to `atm-core` crates such
  as `atm-graft` and `atm_core`, plus narrowly scoped vendor shims when needed
- keep repo-local glue bounded to the small integration surfaces that wire
  those dependencies into the upstream package
- keep cross-seam tests out of `unit-basic` and place them in explicit
  integration lanes under `tests/atm_*` or `tests/integration_*`

Required regression rule once ATM-owned crates exist:

1. every PR still runs the upstream required baseline
2. PRs touching the ATM dependency wiring or vendor shim surfaces run the
   relevant ATM-owned lanes as well
3. PRs touching the seam between root-package upstream code and ATM-owned
   dependencies run the relevant integration lanes as well

This is how the project verifies there is no regression from the upstream fork
while still allowing additive ATM-specific code growth.

## Compile And Basic-Unit Policy

Phase A must distinguish three different ideas that the repo currently blurs:

- inline Rust unit tests under `src/**`
- the broad deterministic bucket currently called `[suite.unit]`
- the strict early required gate Phase A needs first

Required rule:

- `unit-basic` is an explicit allowlist lane
- `unit-basic` must not blindly expand to all of `[suite.unit]`
- `compile` is an explicit lane that runs `cargo check --all-targets`

Required `unit-basic` structure:

1. an audited inline-test allowlist derived from the full `cargo test --lib
   -- --list` surface
2. small curated deterministic add-on targets:
   - `capability_policy_model`
   - `policy_profile_hardening`
   - `extension_flag_passthrough`
   - `model_serialization`
   - `redaction_test`
   - `extension_scoring_ope`

Audited inline-test source of truth:

- checked-in artifact: `docs/plans/phase-A/unit-basic-inline-taxonomy.tsv`
- reproducible generator: `.just/unit_basic_audit.py`
- reproduction commands:
  - `cargo test --lib -- --list`
  - `python3 .just/unit_basic_audit.py summary`
  - `python3 .just/unit_basic_audit.py tsv > docs/plans/phase-A/unit-basic-inline-taxonomy.tsv`

Current inline-test reconciliation from that audit:

- total inline lib tests enumerated: `6651`
- inline tests included in `unit-basic`: `1797`
- inline tests excluded from `unit-basic`: `4854`
- audited included inline prefixes: `32`
- exact per-test skip retained inside an included prefix: `1`
  - `acp::tests::permission_request_times_out_fail_closed`

Excluded inline categories and current counts:

| Category | Count | Why excluded from A1 `unit-basic` |
|---|---:|---|
| `async_timing_dependent_flow_tests` | 20 | real waits, retries, cooldowns, or timeout-path coverage that does not fit a fast required gate |
| `fixture_vcr_inventory_audits` | 451 | conformance, replay, and inventory audits that validate broader upstream compatibility |
| `network_http_streaming_dependent_tests` | 713 | auth/provider/HTTP/streaming flows that rely on transport-style behavior rather than the first unit gate |
| `extension_runtime_policy_integration_tests` | 2178 | extension runtime, hostcall, dispatcher, policy, and scheduler matrices broader than A1 |
| `interactive_tui_workflow_tests` | 493 | higher-level TUI/operator workflow coverage outside the first required gate |
| `subprocess_bash_tool_execution_tests` | 492 | doctor, package-manager, bash-tool, grep-tool, and process-surface execution tests |
| `rpc_command_queue_integration_tests` | 149 | RPC queue, retry, bridge, and extension-session integration flows |
| `persistence_index_sqlite_artifact_tests` | 258 | index/sqlite/storage/reporting persistence verification |
| `subsystem_stress_or_endurance_tests` | 100 | stress, endurance, and broader system-behavior harnesses |

Implementation rule:

- `.just/test_catalog.py` must run one `cargo test --lib <prefix>` command per
  audited included prefix, not one broad `cargo test --lib` command with a
  growing skip list
- the checked-in taxonomy artifact is the reviewable accounting surface for the
  full inline test inventory
- the six add-on integration targets above remain explicit and separate from
  the inline reconciliation

`unit-basic` must not use `cargo test --all-targets --lib` because Cargo
forwards harness flags into benchmark/example binaries under `--all-targets`,
and those binaries reject the `--skip` mechanism required for the one exact
timeout exclusion retained inside the audited inline allowlist.

## Required PR Exclusions

These do not belong in required PR CI:

- `ci.yml`
- `fuzz.yml`
- `bench.yml`
- `semver.yml`
- conformance sweeps
- evidence refresh
- release or publish workflows

After Sprint A1, these workflows may remain as:

- `workflow_dispatch`
- `schedule`

They must not run on ordinary feature PRs.

Workflow classification target after Sprint A1:

| Workflow | Ordinary PRs | Allowed remaining triggers |
|---|---|---|
| `baseline.yml` | yes | `pull_request`, optionally protected-branch `push` |
| `ci.yml` | no | `workflow_dispatch` |
| `conformance.yml` | no | `workflow_dispatch`, `schedule` |
| `fuzz.yml` | no | `workflow_dispatch`, `schedule` |
| `bench.yml` | no | `workflow_dispatch` |
| `semver.yml` | no | `workflow_dispatch` |
| `model-catalog-drift.yml` | no | `workflow_dispatch`, `schedule` |
| `weekly-certification-verdict.yml` | no | `workflow_dispatch`, `schedule` |
| `weekly-evidence-refresh.yml` | no | `workflow_dispatch`, `schedule` |
| `publish.yml` | no | release-only trigger as defined in workflow |
| `release.yml` | no | release-only trigger as defined in workflow |

Protected-branch `push` triggers for heavyweight workflows are out of scope for
Phase A unless team-lead explicitly revises this strategy later.

Sprint A1 validation must prove that every displaced workflow still has a real
manual or scheduled execution path after the trigger edits land.

## Upstream Test Contracts That Phase A Must Respect

Phase A does not get to invent a new definition of "tests" for this fork.
These upstream contracts remain authoritative while Phase A narrows ordinary PR
gating:

- suite taxonomy and suite membership:
  - `docs/testing-policy.md`
  - `tests/suite_classification.toml`
- extension conformance/replay infrastructure:
  - `.github/workflows/conformance.yml`
  - `tests/ext_conformance/**`
- no-mock and evidence-policy guards:
  - `.github/workflows/ci.yml`
- specialty API/catalog verification:
  - `.github/workflows/semver.yml`
  - `.github/workflows/model-catalog-drift.yml`

Phase A is a required-gate reshaping effort. It is not an authorization to
delete or semantically weaken those upstream contracts without separate review.

## Lint Policy

Required PR CI lint rules:

- lint only local code surfaces
- do not lint third-party dependencies
- do not run `clippy --tests` in required PR CI
- do not run `clippy --benches` in required PR CI
- do not run `clippy --examples` in required PR CI

Approved required lint lanes:

- `just lint clippy-bins`
- `just lint clippy-lib`

Local-only optional lint lanes:

- `just lint all-local`
- `just lint clippy-tests`
- `just lint clippy-benches`
- `just lint clippy-examples`

## Test Policy

Required PR CI test rule:

- A1 starts with:
  - `just test compile`
  - `just test unit-basic`
- A3 later adds:
  - `just test baseline`

It must not include:

- broad `cargo test`
- full `[suite.unit]`
- full `suite.vcr`
- E2E sweeps
- fuzz
- semver
- benchmarks
- conformance matrices

Local-only optional test lanes may include:

- `just test unit`
- `just test integration`
- `just test all`
- `just test vcr`
- `just test e2e`

These remain outside required PR CI unless separately re-approved with timing
evidence.

## Reuse Policy

Phase A should prefer these reuse sources before inventing new implementation:

- `justfile`
- `.just/print_help.py`
- `.just/run_fmt.py`
- `.just/run_cargo.py`
- `.just/run_lint.py`
- `.just/lint_catalog.py`
- `.just/run_test.py`
- `.just/test_catalog.py`
- `.just/explain.py`
- `.just/show_suites.py`
- `.github/workflows/baseline.yml`
- `scripts/smoke.sh`

Phase A should not invent new top-level commands to avoid confusion around the
established operator surface. Narrow helper scripts are allowed only when they
remain behind `just help`, `just fmt`, `just lint`, `just test`, `just explain`,
or `just suites`.

## Failure Reporting Rules

Every `just` lane and required CI step should print:

- failing lane name
- exact underlying command
- source-of-truth file
- one next action
- non-zero exit code

Minimum example:

- `lane=baseline.lint.clippy-lib`
- `command=cargo clippy --no-deps --lib -- -D warnings`
- `ssot=.just/lint_catalog.py`
- `next=fix local lib warnings or move non-local scope out of the lane`

## Retained Evidence

Observed local macOS timings from `feature/just-integration`:

| Command | Result | Observed wall time |
|---|---|---:|
| `just help` | pass | `<1s` |
| `just fmt check` | pass | `12.46s` |
| `just lint clippy-lib` | pass | `50.66s` |
| `just lint clippy-bins` | pass | `2.87s` |
| `just test baseline` | pass | `10.59s` |
| `just lint clippy-tests` | incomplete | `>3m38s` before manual stop |
| `just test unit` | incomplete | `>120s` before timeout |
| `just test integration` | incomplete | `>120s` before timeout |

Observed GitHub Actions timings from 2026-07-02:

| Workflow | Result | Approximate wall time |
|---|---|---:|
| `baseline` | success | `~7m03s` |
| `Extension Conformance` | success | `~6m25s` |
| `Fuzz CI` | success | `~42m59s` |
| old monolithic `ci` | cancelled | `~49m25s` before cancellation |

## Team-Lead Review Checklist

Team-lead approval should explicitly confirm:

- the upstream ordinary-PR workflow inventory and post-A1 trigger plan
- the `compile` lane definition
- the `unit-basic` audited taxonomy, allowlist, and add-on set
- the steady-state `baseline` command list
- the per-sprint rollout table
- the decision to remove heavyweight workflows from ordinary PRs in Sprint A1
- the rule that required PR CI stays under 10 minutes in every sprint
- the SSOT owner files for lint and test lanes
- the list of local-only and manual-only lanes
- the rule that Phase A does not invent new top-level `just` commands
- the future lane taxonomy for `upstream`, `atm`, and `integration`
- the intended repository layering surfaces for ATM-owned crates and glue code

### Team-Lead Approval Record

Reviewer: `team-lead`
Review date: `2026-07-03`
Approval state: team-lead approved this testing strategy on `2026-07-03`; the
strategy is the approved control document for Phase A implementation.

Checklist record:

- the upstream ordinary-PR workflow inventory and post-A1 trigger plan
  - status: approved by team-lead, 2026-07-03
- the `compile` lane definition
  - status: approved by team-lead, 2026-07-03
- the `unit-basic` audited taxonomy, allowlist, and add-on set
  - status: approved by team-lead, 2026-07-03
- the steady-state `baseline` command list
  - status: approved by team-lead, 2026-07-03
- the per-sprint rollout table
  - status: approved by team-lead, 2026-07-03
- the decision to remove heavyweight workflows from ordinary PRs in Sprint A1
  - status: approved by team-lead, 2026-07-03
- the rule that required PR CI stays under 10 minutes in every sprint
  - status: approved by team-lead, 2026-07-03
- the SSOT owner files for lint and test lanes
  - status: approved by team-lead, 2026-07-03
- the list of local-only and manual-only lanes
  - status: approved by team-lead, 2026-07-03
- the rule that Phase A does not invent new top-level `just` commands
  - status: approved by team-lead, 2026-07-03
- the future lane taxonomy for `upstream`, `atm`, and `integration`
  - status: approved by team-lead, 2026-07-03
- the intended repository layering surfaces for ATM-owned crates and glue code
  - status: approved by team-lead, 2026-07-03

## Exit Criteria

The strategy is implemented when:

- required PR CI is exactly one workflow named `baseline`
- `baseline` is the only required branch-protection status check for ordinary
  PRs once the Sprint A1 operational branch-protection update lands
- `baseline` stays under 10 minutes
- CI and local execution share the same lane definitions
- heavyweight workflows no longer run on ordinary PRs
- timing data is refreshed after each baseline expansion sprint
