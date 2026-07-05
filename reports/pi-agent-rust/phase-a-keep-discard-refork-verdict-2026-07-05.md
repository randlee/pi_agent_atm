# Phase A Keep / Discard / Re-Fork Verdict

Date: 2026-07-05
Scope: evidence-based verdict on the two Phase A attempts in this repo:

- the earlier `feature/just-integration` attempt
- the later sprint-chain Phase A attempt (`A1` through `A7`)

This document answers one practical question:

- which assets are worth preserving
- which assets should be discarded
- whether a clean re-fork is justified

## Bottom Line

The repo should not be deleted blindly, because both Phase A attempts produced a
small number of useful assets.

The current Phase A stack also should not be treated as a success that merely
needs more polish. It failed the stated goal:

- it did not end with a measured final parallel multi-platform required gate
- it did not preserve the older system's explanatory value
- it created too much branch/PR/process churn relative to the value delivered

My recommendation is:

- keep the small set of assets that are demonstrably useful
- discard the current Phase A narrative and most of the sprint-chain ceremony
- do a clean restart on a fresh branch or fresh fork with only the preserved
  assets transplanted in a few reviewable commits

Technically, a full GitHub re-fork is optional.

Operationally, a clean restart is justified.

## Evidence Review: Earlier Attempt (`feature/just-integration`)

### What it tried to do

The earlier attempt centered on `feature/just-integration` and PR #3
`Add smoke baseline just/CI lane`.

Evidence reviewed:

- branch history on `origin/feature/just-integration`
- PR #3 body
- `justfile` and `.just/test_catalog.py`
- `docs/just-verification-macos.md`
- `.github/workflows/baseline.yml`
- Actions runs on 2026-07-02

### Strengths

1. It had a richer `just` surface.

The branch exposed:

- `just help`
- `just explain`
- `just fmt`
- `just lint`
- `just test`
- `just ci`
- `just fuzz`
- `just fuzz-full`
- `just bench`
- `just suites`

It also kept explicit test lanes such as:

- `baseline`
- `ci`
- `all`
- `unit`
- `integration`
- `vcr`
- `e2e`

That was more informative than the current minimal surface.

2. It wrote down useful local timing and behavioral evidence.

`docs/just-verification-macos.md` recorded:

- `just help` `<1s`
- `just suites` `<1s`
- `just fmt check` `12.46s`
- `just lint clippy-lib` `50.66s`
- `just lint clippy-bins` `2.87s`
- `just test baseline` `10.59s`

It also stated that the broader `just test*` family entered real work but timed
out after 120 seconds on that host, which is exactly the kind of operator signal
the current sprint chain often buried.

3. It retained more semantic meaning in the baseline smoke.

The old baseline smoke included both:

- unit-style targets
- VCR-style targets

The macOS verification log listed:

- unit-style: `model_serialization`, `config_precedence`,
  `session_conformance`, `error_types`, `compaction`
- VCR-style: `provider_streaming`, `http_client`,
  `sse_strict_compliance`, `model_registry`, `provider_factory`

That gave the baseline more explanatory value than the current unit-only smoke.

4. It achieved at least one successful fast baseline run.

Successful baseline run on `feature/just-integration`:

- run `28622615189`
- total `6m57s`

Step timings:

- Format gate `15s`
- Clippy lib `2m38s`
- Clippy bins `2s`
- Baseline smoke `3m19s`

### Weaknesses

1. It never stabilized the PR CI surface.

At the same time the branch had a successful `baseline`, it was still
registering and/or failing:

- `ci`
- `Extension Conformance`
- `Fuzz CI`
- `Benchmarks`
- `semver`

That means the branch was not yet a proof-first minimal gate. It was still in a
mixed state where the old workflow world and the new `just` world overlapped.

2. The richer `just` surface was not bounded tightly enough for early PR gating.

`just test ci`, `just test all`, `just test integration`, `just test e2e`, and
fuzz lanes existed at the top level before the team had a stable story for what
should be required, local-only, or manual-only. This was useful for operators,
but it was bad discipline for a controlled CI recovery.

3. It still lacked a clean lane-to-coverage ledger.

Even the better old attempt did not provide one operator document that mapped:

- lane
- exact command
- exact test set
- exact exclusions
- local time
- CI time
- branch/run ID

4. It remained open and unfinished.

PR #3 is still open. The branch never matured into a cleanly accepted
production-ready model.

### Verdict on the earlier attempt

The earlier attempt was more useful for understanding the upstream repo, but it
was not disciplined enough to serve as the final Phase A delivery.

Keep from the earlier attempt:

- macOS timing and behavior evidence in `docs/just-verification-macos.md`
- the idea that `just` should expose broad meaningful lane families
- the smoke-script operational knowledge
- `ci` operator runbook-style documentation patterns

Discard from the earlier attempt:

- trying to leave the full old PR workflow world alive while introducing the new
  `just` lane world
- treating the branch as if a single successful baseline run meant the whole
  rollout was coherent

## Evidence Review: Current Sprint-Chain Phase A Attempt

### What it tried to do

The current attempt reframed Phase A as a proof-first sprint chain:

- A1 establish minimal baseline gate
- A2 add local-code lint
- A3 add smoke baseline
- A4 taxonomy helpers
- A5 optional local lanes
- A6 timing/SSOT refresh
- A7 merge into `feature/atm-graft-integration`

### Strengths

1. It created a tighter required lane structure.

The final required lane sequence is explicit:

1. `just help`
2. `just fmt check`
3. `just test compile`
4. `just test unit-basic`
5. `just lint clippy-bins`
6. `just lint clippy-lib`
7. `just test baseline`

2. It introduced a disciplined `unit-basic` audit.

This is the best technical asset created by the current attempt.

It made explicit that:

- broad upstream `[suite.unit]` is not the same as an early deterministic gate
- many nominal "unit" tests are actually integration, artifact, VCR, or
  binary-launching surfaces
- a strict allowlist plus exclusions is required if the early gate is meant to
  be fast and deterministic

3. It produced one required Linux baseline gate that actually runs.

There are successful branch runs for A1-A7, and the sprint branches mostly show
`~7m` steady-state Linux required CI.

4. It clarified required vs optional lanes better than the old attempt.

Optional local lanes now exist explicitly for:

- `just test unit`
- `just test integration`
- `just test all`
- `just lint all-local`

That is cleaner than letting broad lanes masquerade as ready required surfaces.

### Weaknesses

1. It did not meet the stated final goal.

The stated goal was a measured A1->A7 progression toward a final 10-20 minute
parallel multi-platform gate with clear coverage boundaries.

The current final state is instead:

- one Linux-only required gate
- no required parallel multi-platform gate
- no final measured cross-platform timing story

2. It removed too much explanatory value.

Compared to the earlier attempt, the current state is easier to gate but harder
to understand.

The current top-level `just` surface is tidy, but most operators still cannot
tell what `unit-basic` or `baseline` really mean without opening Python catalog
code.

3. It fragmented evidence across too many places.

To understand the current result, an operator had to read:

- plan docs
- sprint docs
- PR bodies
- lane catalogs
- helper code
- Actions runs

That is exactly the opposite of what a recovery phase should optimize for.

4. The timing story is materially inconsistent at the actual handoff point.

The A7 sprint branch showed:

- run `28735967657`
- total `7m09s`

But the actual merged target branch showed:

- run `28736534784`
- total `12m33s`

That means the final handoff branch is slower than the headline sprint-branch
number and does not satisfy the under-10-minute final story that was implicitly
being sold.

5. The final state still lacks lane-specific coverage percentages.

This was true at the start of this review, but it is no longer true.

Measured lane-specific production-code coverage for the final required test
lanes (`just test unit-basic` + `just test baseline`) is:

- line coverage `22.90%`
- function coverage `23.39%`
- region coverage `21.73%`

This confirms two things:

- the final Phase A gate is a narrow smoke/regression gate
- the historical repo-wide `79.08%` line coverage number cannot be used to
  justify the current required baseline

6. The sprint chain added large coordination overhead.

Open/reopened PRs, merge-forward complexity, branch-state confusion, and doc
churn became a significant part of the work. The delivered technical value does
not justify that level of process overhead.

### Verdict on the current attempt

The current attempt is technically better at defining a strict fast gate, but it
is worse at helping humans understand the system and it failed the final goal.

Keep from the current attempt:

- `justfile`
- `.just/test_catalog.py`
- `.just/lint_catalog.py`
- `.just/unit_basic_audit.py`
- `.github/workflows/baseline.yml`
- the idea of separating required lanes from optional/manual lanes
- the new operator ledger added in this branch

Discard from the current attempt:

- the claim that Phase A is complete in the way originally intended
- the seven-sprint narrative as a success story
- the assumption that a green Linux baseline alone is enough evidence
- any expectation that operators should assemble understanding from PR bodies

## Keep / Discard Decision

### Keep

Preserve these assets into the restart:

- `justfile`
- `.just/run_fmt.py`
- `.just/run_lint.py`
- `.just/run_test.py`
- `.just/explain.py`
- `.just/show_suites.py`
- `.just/lint_catalog.py`
- `.just/test_catalog.py`
- `.just/unit_basic_audit.py`
- `.github/workflows/baseline.yml`
- `scripts/smoke.sh`
- `docs/just-verification-macos.md` from the earlier attempt
- `reports/pi-agent-rust/phase-a-test-lane-ledger-2026-07-05.md`

### Discard

Do not preserve as authoritative:

- the claim that the current Phase A stack already achieved the original goal
- the current A1-A7 sprint-story framing as proof of successful progression
- PR-body-only timing ledgers as the primary evidence surface
- any workflow or doc claim that treats sprint-branch timings as equivalent to
  merged-target timings

### Re-fork?

#### Technical answer

Not strictly necessary.

The useful code and docs can be transplanted onto a clean branch from the
current repo or onto a fresh upstream fork.

#### Operational answer

A clean restart is justified.

Reasons:

1. Trust in the current Phase A narrative is low.
2. The git/PR history now obscures more than it clarifies.
3. The preserved asset set is small enough to transplant cleanly.
4. Starting clean makes it easier to enforce a tighter acceptance contract:
   - one operator ledger
   - one timing table per lane
   - one explicit coverage-boundary table
   - one clear distinction between required, optional, manual, and scheduled

#### Recommended path

Prefer a "soft re-fork" or clean restart branch:

1. Start from a fresh upstream-aligned integration base.
2. Cherry-pick or transplant only the preserved assets listed above.
3. Rebuild the CI surface in a few commits, not another seven-sprint ceremony.
4. Keep one evidence document live from the first commit:
   - lane
   - command
   - tests run
   - exclusions
   - local timing
   - CI timing
   - coverage note
   - run ID / SHA

## Final Recommendation

Do not delete the repo in anger.

Do treat the current Phase A effort as a failed reduction attempt that produced
a small number of valuable salvage assets.

Recommended decision:

- keep the salvage assets
- discard the current Phase A story
- restart clean from a fresh branch or fresh fork
- require operator-grade evidence from day one

## Small-Change Salvage Path

If the team wants to argue that Phase A should be kept rather than deleted, the
strongest evidence-based version of that argument is not "Phase A is already
done." It is:

- Phase A is close to a usable narrow baseline, but only after a few concrete
  fixes and one scope correction

The few concrete fixes are:

1. Keep the lazy `unit-basic` expansion fix.

Evidence:

- `just help` was previously paying for `cargo test --lib -- --list` during
  Python import
- local measurement after the fix: `just help` is `0.04s`
- the final merged target branch baseline had a bogus `Just help` step of
  `4m29s`

Projected effect:

- final merged target branch Linux baseline run `28736534784` was `12m33s`
- replacing `4m29s` help with `~0s` projects that run to about `8m04s`

2. Keep the `scripts/smoke.sh` Bash-array fix.

Evidence:

- the smoke targets all passed, but the script failed afterward with
  `FAILED_NAMES[@]: unbound variable`

Effect:

- this removes a false-negative failure mode from the required smoke lane

3. Replace the final claim, not the baseline.

Required wording correction:

- Phase A should claim it establishes a measured narrow upstream-regression gate
- it should not claim high coverage or final upstream proof

Measured required-lane production-code coverage is only:

- `22.90%` line
- `23.39%` function
- `21.73%` region

4. Add a final parallel multi-platform baseline workflow or matrix.

This is the one remaining change that is still needed to actually satisfy the
original end goal.

Why this now looks plausible:

- the inflated `just help` cost was a major false source of Linux runtime
- after removing that defect, the Linux required gate projects to around
  `8m04s`
- that is inside the intended `10-20 minute` per-platform parallel window

What still must be measured:

- macOS baseline runtime with the corrected `just help`
- Windows baseline runtime with the corrected `just help`
- merged-target branch timing, not just sprint-branch timing

Evidence-based conclusion:

- if the goal is kept as "minimal measured upstream smoke gate through `just`",
  Phase A is salvageable with a few small changes
- if the goal is kept as "already-finished final multi-platform proof gate",
  it is not there yet
