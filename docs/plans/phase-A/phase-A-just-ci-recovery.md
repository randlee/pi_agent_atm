# Phase A - Minimal Just / CI Recovery

Date: 2026-07-05
Status: replay plan ready for review
Branch: `plan/phase-A-attempt-3`
Worktree: `../pi_agent_atm-worktrees/plan/phase-A-attempt-3`
Planning target: docs only
Implementation target model: `integrate/phase-A` accumulation branch, `feature/atm-graft-integration` consumer
Authoritative scope: corrected Phase A salvage and replay plan

## Purpose

Phase A recovers the `just` + CI effort by replaying it as a measured,
evidence-gated sprint chain:

1. start with the smallest green baseline that still proves compile health and
   strict basic-unit health
2. add one small production-ready increment at a time
3. keep broader upstream test contracts available outside the narrow required
   gate
4. end with a measured multi-platform required gate, not just one fast Linux
   job

This corrected plan replaces the earlier failed execution attempt as the
authoritative operational model.

Supporting evidence for this correction:

- `reports/pi-agent-rust/local-test-surface-review-2026-07-03.md`
- `reports/pi-agent-rust/upstream-testing-contract-review-2026-07-03.md`
- `reports/pi-agent-rust/just-layering-and-atm-integration-strategy-2026-07-03.md`

## Authoritative Document Layout

This phase uses:

- phase overview:
  - `docs/plans/phase-A/phase-A-just-ci-recovery.md`
- phase testing strategy:
  - `docs/plans/phase-A/phase-A-testing-strategy.md`
- sprint plans:
  - `docs/plans/phase-A/sprint-a-1-establish-minimal-baseline-gate.md`
  - `docs/plans/phase-A/sprint-a-2-add-local-code-lint.md`
  - `docs/plans/phase-A/sprint-a-3-add-smoke-baseline.md`
  - `docs/plans/phase-A/sprint-a-4-add-taxonomy-helpers.md`
  - `docs/plans/phase-A/sprint-a-5-add-optional-local-lanes.md`
  - `docs/plans/phase-A/sprint-a-6-refresh-ssot-and-timing.md`
  - `docs/plans/phase-A/sprint-a-7-merge-baseline-into-atm-graft.md`
  - `docs/plans/phase-A/sprint-a-8-publish-test-category-ledger.md`
  - `docs/plans/phase-A/sprint-a-9-measure-unit-category-coverage.md`
  - `docs/plans/phase-A/sprint-a-10-expose-runnable-broad-test-surfaces.md`
  - `docs/plans/phase-A/sprint-a-11-measure-broad-test-surface-timings.md`
  - `docs/plans/phase-A/sprint-a-12-finalize-required-vs-runnable-gate.md`

Only these docs are authoritative for corrected Phase A.

## Current Diagnosis

The failed attempt showed the same root problem repeatedly: docs, branch
targets, workflow registration, and run evidence drifted apart.

Phase A replay must verify each sprint at six independent layers:

1. content parity
   - do the `just` files and workflow files on the branch actually match the
     intended source of truth
2. registration
   - did GitHub Actions register a workflow run for the exact head SHA
3. execution
   - if a run exists, did it pass, and what actually ran
4. timing
   - are the reported numbers warm, cold, local, CI, per-step, and total
     clearly labeled
5. target-branch reality
   - does the PR base branch actually contain the prerequisites the workflow
     expects
6. doc-vs-reality parity
   - do the planning docs describe the branch model and execution shape that
     were actually used

No single layer implies any of the others.

## Non-Negotiable Rules

This phase follows:

- `.claude/skills/plan-hardening/sprint-planning-guidelines.md`
- `.claude/skills/codex-orchestration/sprint-plan.md.j2`

Applied interpretation for this phase:

- one sprint, one deliverable, one PR
- each sprint must land production-ready for the scope it claims
- no sprint may rely on the old heavyweight PR workflow surface remaining active
- no sprint may silently carry a required deliverable forward
- every sprint must preserve green required PR CI for the stage it introduces
- no implementation code should merge back into `develop` until the Phase A
  salvage chain is proven
- no sprint should merge into `integrate/phase-A` without a recorded evidence
  package that includes registration, execution, and timing proof
- every sprint PR must record both:
  - local wall-clock timings for the sprint's in-scope commands
  - equivalent CI step and total workflow timings for the same stage, or an
    explicit `no ci equivalent by design` note for local-only lanes
- the historical A1-A7 branch and PR stack is evidence inventory only; it is
  not execution authority for this replay
- Phase A is not complete if it ends with only a Linux-required check; final
  closure requires Linux, macOS, and Windows timing evidence for the merged
  required gate

## Authoritative Branch Model

The previous docs mixed planning branches, sprint branches, integration
branches, and historical PR numbers in a way that made execution harder to
understand than the code itself.

The authoritative branch roles are now:

| Branch or branch family | Role | Allowed action |
|---|---|---|
| `plan/phase-A-attempt-3` | planning branch only | docs updates only |
| `develop` | bootstrap and upstream-sync reference | no Phase A implementation merges |
| `sprint-a-1-*` through `sprint-a-7-*` | execution branches | one sprint each, evidence-gated |
| `integrate/phase-A` | accumulation branch for proven Phase A outputs | merge only after sprint proof |
| `feature/atm-graft-integration` | consumer branch for final baseline handoff | receives proven A7 output only |

Historical PR numbers from the failed first attempt are intentionally not part
of the replay contract. They may be referenced during forensics, but they are
not the source of truth for execution.

## Sprint Replay Model

Sprint replay is a clean forward chain:

```text
develop bootstrap
  -> A1 branch, PR target integrate/phase-A
  -> A2 branch from proven A1, PR target A1
  -> A3 branch from proven A2, PR target A2
  -> A4 branch from proven A3, PR target A3
  -> A5 branch from proven A4, PR target A4
  -> A6 branch from proven A5, PR target A5
  -> A7 branch from proven A6, PR target feature/atm-graft-integration
```

Interpretation:

- A1 is the only sprint that targets `integrate/phase-A` directly.
- A2-A6 are replayed as a strict merge-forward proof chain.
- `integrate/phase-A` is updated only after the corresponding sprint is proven.
- A7 is the handoff sprint that carries the proven baseline into
  `feature/atm-graft-integration`.

## Historical Attempt Handling

The old Phase A sprint branches and PRs created useful evidence, but they also
created confusion. Replay treats them this way:

- keep them as forensic evidence and patch-source inventory
- do not treat them as automatically mergeable
- do not use their PR numbers as proof that the sprint is valid
- if a replay sprint cannot quickly prove content parity plus CI registration,
  execution, and timing, re-cut it from the last proven state instead of
  repairing the stale stack indefinitely

This is the clean-up plan for the current branch clutter: freeze the old stack
as evidence, then execute the replay chain from a clean bootstrap.

## Sprint Evidence Gate

Every replay sprint must ship an evidence package before merge-forward:

- content parity proof
  - exact file diff against the documented sprint scope
- registration proof
  - GitHub Actions run exists for the exact head SHA
- execution proof
  - run result and failed-log review if not green
- timing proof
  - local timings for in-scope commands
  - CI step timings and total workflow duration
  - exact run ID and SHA recorded in the PR notes
- target-branch proof
  - PR base branch contains the prerequisites the workflow expects
- doc parity proof
  - sprint doc, strategy doc, and PR notes all describe the same lane set and
    same branch model

If any layer fails, the sprint is not proven.

## Sprint Timing Deliverable Contract

Quality-mgr timing capture is a required artifact for every Phase A sprint PR.

Each sprint PR must include:

- a local timing table for every command added or validated in that sprint
- a CI timing table for the equivalent `baseline` step set and total workflow
  duration
- an explicit `no ci equivalent by design` note for local-only helper or
  optional lanes
- links or identifiers for the exact CI runs used for timing capture

CI timing must come from reading existing GitHub Actions run and job data for
the sprint branch; Phase A should not add timing-only instrumentation steps to
`baseline.yml`.

Rollup requirements:

- Sprint A6 review-pack materials must consolidate the timing tables for A1-A6
- Sprint A7 phase conclusion materials must consolidate the timing tables for
  A1-A7 and report the final progression of required baseline cost by sprint
- Sprint A7 phase conclusion materials must also record the final merged-target
  Linux, macOS, and Windows timings for the required gate

## Ground Rules

- do not work on `main`
- do not merge `feature/just-integration` wholesale
- do not treat `develop` as the active accumulation branch for Phase A code
- do not reintroduce exploratory `src/**` churn as part of Phase A
- reuse only narrow proven pieces from `feature/just-integration`
- `just` is the only local operator surface
- the required `baseline` workflow and new Phase A fast-lane workflow edits must
  call `just` commands rather than bespoke cargo command strings
- compile checking and strict basic-unit coverage must land before local-code
  lint expansion or smoke-lane expansion
- required PR CI must stay within the sprint-stage budget in every
  implementation sprint
- every sprint evidence package must include:
  - workflow registration proof
  - workflow execution proof
  - local timings
  - CI timings
- heavyweight workflows must not run on ordinary PRs after Sprint A1 lands
- the Phase A baseline lanes become the stable upstream-regression contract
- future ATM-owned lanes must layer in additively through `just lint` and
  `just test`, not by mutating the meaning of the baseline lanes
- future ATM integration should follow the actual
  `feature/atm-graft-integration` model: root `Cargo.toml` dependency wiring to
  `atm-core` crates plus narrowly scoped local shim/integration surfaces
- no sprint may claim success with timing numbers that were not tied to a
  concrete command, run ID, and SHA

## Upstream Fork Testing Reality

This repository is a fork of the public upstream
`Dicklesworthstone/pi_agent_rust`.

Current upstream ordinary-PR testing surfaces that Phase A must classify rather
than ignore:

- `.github/workflows/ci.yml`
  - cross-OS build/test/policy workflow on `pull_request`
- `.github/workflows/conformance.yml`
  - extension conformance PR matrix on `pull_request`
  - checks out sibling repositories and installs Bun / npm dependencies
- `.github/workflows/fuzz.yml`
  - Linux fuzz PR workflow for PRs targeting `main`
- `.github/workflows/bench.yml`
  - benchmark PR workflow that remains outside ordinary required PR gating
- `.github/workflows/semver.yml`
  - path-filtered PR API compatibility workflow
- `.github/workflows/model-catalog-drift.yml`
  - path-filtered advisory PR drift workflow

Phase A is allowed to reduce ordinary PR gating to `baseline`, but only if the
testing strategy documents what each displaced upstream workflow currently
proves, how it will still be runnable after Sprint A1, and why the ordinary PR
gate is no longer the right place for it.

This is a fork-risk rule, not an optional note. "Simple CI green" for Sprint A1
means a deliberately reduced required PR gate, not permission to forget what
the upstream fork already validates.

## Safe Reuse Inventory

Safe reuse candidates from `feature/just-integration`:

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

Exact on-disk reference paths:

- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/justfile`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/print_help.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_fmt.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_cargo.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_lint.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/lint_catalog.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/run_test.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/test_catalog.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/explain.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.just/show_suites.py`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/.github/workflows/baseline.yml`
- `/Volumes/Extreme Pro/github/pi_agent_atm-worktrees/feature/just-integration/scripts/smoke.sh`

Do not reuse directly:

- any exploratory `src/**` change
- broad workflow rewrites that try to preserve monolithic PR CI
- shard orchestration and artifact plumbing from exploratory CI work
- broad test rewrites made only to chase green CI

## Retained Evidence

Observed local macOS timings from `feature/just-integration`:

- `just help`: `<1s`
- `just fmt check`: `12.46s`
- `just lint clippy-lib`: `50.66s`
- `just lint clippy-bins`: `2.87s`
- `just test baseline`: `10.59s`
- `just lint clippy-tests`: `>3m38s` before manual stop
- `just test unit`: `>120s` before timeout
- `just test integration`: `>120s` before timeout

Observed GitHub Actions timings from 2026-07-02:

- `baseline`: `~7m03s`
- `Extension Conformance`: `~6m25s`
- `Fuzz CI`: `~42m59s`
- old monolithic `ci`: `~49m25s` before cancellation

Implications:

- a fast required PR baseline is viable
- `clippy --tests` does not belong in required PR CI
- broad `cargo test` orchestration does not belong in required PR CI
- `fuzz`, `bench`, and `semver` must stay outside ordinary PR gating
- upstream PR-only specialty workflows must be explicitly classified before
  Sprint A1 changes any triggers
- `suite.unit` is too broad to serve as the first basic-unit gate without an
  explicit allowlist

## Known Issues To Preserve

- Bash 3 portability still matters on macOS
- `just clean` previously failed against `target/agents/...` on macOS
- a `vergen-lib` local build-script issue was observed in exploratory runs
- prior fuzz failures hit `sysinfo` / nightly drift
- historical CI used wrong working-directory paths

These notes remain valid even though the old rollout plan was superseded.

## Replay Sequence

| Sprint | Branch base | PR target | New required gate content after sprint | New deliverable in sprint |
|---|---|---|---|---|
| A1 | `develop` bootstrap | `integrate/phase-A` | `just help`, `just fmt check`, `just test compile`, `just test unit-basic` | introduce the minimal baseline gate |
| A2 | proven A1 | A1 branch | A1 + `just lint clippy-bins`, `just lint clippy-lib` | add required local-code lint |
| A3 | proven A2 | A2 branch | A2 + `just test baseline` | add required smoke lane |
| A4 | proven A3 | A3 branch | unchanged from A3 | add taxonomy helpers only |
| A5 | proven A4 | A4 branch | unchanged from A3 | add optional local lanes only |
| A6 | proven A5 | A5 branch | unchanged from A3 | freeze SSOT and consolidate timing evidence |
| A7 | proven A6 | `feature/atm-graft-integration` | unchanged from A3 | hand off the proven baseline into ATM integration |

The table above is the execution contract. If implementation diverges from it,
the docs must be revised before more work happens.

## Active Continuation Sequence

A1-A7 are now best treated as a historical failed attempt plus evidence
inventory. The active continuation plan begins at A8.

| Sprint | Purpose | Primary output |
|---|---|---|
| A8 | publish the readable test category ledger and per-sprint evidence table template | docs that say what runs now vs what can run |
| A9 | measure unit-category timings and coverage | unit coverage and maintainability evidence |
| A10 | expose broad runnable categories clearly | restored unit / VCR / E2E / conformance / fuzz / bench / semver / drift visibility |
| A11 | measure broad-category timings | actual or conservative timing evidence across the broad surfaces |
| A12 | freeze required vs runnable split | final Phase A gate definition and ATM regression handoff |

Rule for A8-A12:

- every sprint must update the same category evidence table template
- every sprint must say what changed in:
  - what runs now on ordinary PRs
  - what can run in CI outside the required gate
  - what can run locally only
  - what coverage and timing evidence exists for the affected categories

### Sprint A1

Deliverable:

- minimal `just` operator surface plus one tiny required `baseline` workflow
  that proves compile health and strict basic-unit health first

Outcome:

- old heavyweight PR workflows stop running on ordinary PRs
- required PR CI becomes `baseline` on the A1 branch path
- the first required baseline proves compile health before lint expansion
- the first required baseline proves a strict basic-unit subset rather than the
  whole broad `[suite.unit]` bucket
- the live PR target for A1 is `integrate/phase-A`, not `develop`

### Sprint A2

Deliverable:

- add local-code lint through the established `just lint` surface

Outcome:

- required PR CI gains local-code lint coverage while staying under budget

### Sprint A3

Deliverable:

- add a tiny deterministic smoke lane through the established `just test`
  surface

Outcome:

- required PR CI proves the repo still basically works without broad test churn

### Sprint A4

Deliverable:

- add taxonomy helpers only without changing required PR CI

Outcome:

- operators can inspect lane semantics, ownership, and suite taxonomy without
  changing the required PR gate

### Sprint A5

Deliverable:

- add optional local lanes without changing required PR CI

Outcome:

- agents get richer local commands, including future ATM-owned or integration
  lanes, without changing the required PR gate

### Sprint A6

Deliverable:

- freeze SSOT ownership and refresh timing evidence using the established
  command surface

Outcome:

- team-lead gets a reviewed timing-backed strategy plus the frozen ATM layering
  framework before the baseline merges into `atm-graft`

### Sprint A7

Deliverable:

- merge the verified baseline into `feature/atm-graft-integration`

Outcome:

- the `atm-graft` line starts from the corrected `just` + CI baseline instead
  of carrying forward the abandoned exploratory work

## Team-Lead Review Gate

No implementation sprint begins until team-lead reviews:

- `docs/plans/phase-A/phase-A-testing-strategy.md`
- the exact baseline command list
- the workflow files removed from ordinary PR gating
- the upstream PR-workflow inventory and its post-A1 trigger classification
- the `unit-basic` allowlist and exclusion rationale
- the sprint ordering that makes Sprint A1 establish the required PR gate
- the A4 / A5 split between taxonomy helpers and optional local lanes
- the future `just` lane taxonomy for upstream, ATM-owned, and integration
  lanes
- the planned dependency and glue surfaces already present on
  `feature/atm-graft-integration`
- the evidence-backed correction that replay uses a clean stacked proof chain
  and `integrate/phase-A` is only an accumulation branch for proven work
- the requirement that final closure includes multi-platform timing evidence,
  not Linux-only proof

### Team-Lead Review Record

Reviewer: `team-lead`
Review date: pending replay-plan review
Confirmation: prior approval history is intentionally not reused. This replay
plan requires a fresh review because the prior execution mixed historical PR
state, branch roles, and CI evidence in a way that no longer serves execution.

Review-item record:

- `docs/plans/phase-A/phase-A-testing-strategy.md`
  - status: PENDING fresh review
- the exact baseline command list
  - status: PENDING fresh review
- the workflow files removed from ordinary PR gating
  - status: PENDING fresh review
- the upstream PR-workflow inventory and its post-A1 trigger classification
  - status: PENDING fresh review
- the `unit-basic` allowlist and exclusion rationale
  - status: PENDING fresh review
- the sprint ordering that makes Sprint A1 establish the required PR gate
  - status: PENDING fresh review
- the A4 / A5 split between taxonomy helpers and optional local lanes
  - status: PENDING fresh review
- the future `just` lane taxonomy for upstream, ATM-owned, and integration
  lanes
  - status: PENDING fresh review
- the planned dependency and glue surfaces already present on
  `feature/atm-graft-integration`
  - status: PENDING fresh review
- the replay branch model and accumulation-branch rules
  - status: PENDING fresh review
- the final multi-platform timing requirement
  - status: PENDING fresh review

Implementation-start rule:

- this plan is not complete while the execution branches, doc text, and
  evidence gate disagree
- this plan remains blocked until the replay model is explicitly reviewed

## Upstream Workflow Trigger Reconciliation

Recurring upstream merges may reintroduce ordinary-PR triggers on heavyweight
workflow files. When that happens, Phase A must reconcile the conflict this way:

1. preserve the strategy rule that only `baseline` remains required on ordinary
   PRs
2. reapply the documented retained triggers for `ci`, `conformance`, `fuzz`,
   `bench`, `semver`, and `model-catalog-drift`
3. treat trigger-only workflow edits as isolated reconciliations unless the
   underlying workflow contract is intentionally being re-scoped
4. rerun the A1 workflow-view validation and record the reconciliation result in
   the sprint PR notes

## Exit Criteria

Phase A is complete when:

- `baseline` is the only required PR workflow
- `baseline` is the only required branch-protection status check for ordinary
  PRs once the Sprint A1 operational branch-protection update lands
- required PR CI on ordinary PRs is limited to the `baseline` workflow surface
- `baseline` stays within the sprint-stage budget throughout the replay
- local `just` commands and required PR CI share the same lane definitions
- heavyweight workflows no longer run on ordinary PRs
- `integrate/phase-A` actually contains the proven baseline substrate
- the verified baseline is merged into `feature/atm-graft-integration`
- the sprint docs and replay branch bases agree
- the phase conclusion report includes the A1-A7 local and CI timing ledger
- the phase conclusion report includes the final Linux, macOS, and Windows
  timings for the merged required gate
- the frozen `just` taxonomy still leaves a clean additive path for ATM-owned
  crates without broad upstream churn
