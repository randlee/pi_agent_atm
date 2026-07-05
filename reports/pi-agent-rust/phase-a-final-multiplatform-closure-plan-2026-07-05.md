# Phase A Final Multi-Platform Closure Plan

Date: 2026-07-05
Scope: the smallest set of changes needed to move Phase A from "narrow Linux
baseline only" to "measured final multi-platform baseline gate with clear
coverage boundaries".

## Goal

Close the original Phase A outcome gap:

- keep the narrow `just`-backed required baseline
- measure it on Linux, macOS, and Windows in parallel
- keep clear documentation of what the gate does and does not prove
- avoid re-expanding ordinary PR CI into the old monolithic workflow set

## Current Evidence

What is already true after the A7 fixes in this worktree:

- `just help` no longer performs import-time cargo work
- local `just help` is back to sub-second behavior
- `just test baseline` no longer false-fails after a green smoke run
- the required test lanes now have measured production-code coverage:
  - line coverage `22.90%`
  - function coverage `23.39%`
  - region coverage `21.73%`

What is still missing:

- final required CI is still one Linux-only workflow
- no measured macOS baseline runtime on the merged target branch
- no measured Windows baseline runtime on the merged target branch
- no final required parallel multi-platform run proving the intended end state

## Minimal Closure Change Set

### 1. Keep the current lane semantics

Do not widen the required baseline contents.

Required lane contents remain:

1. `just help`
2. `just fmt check`
3. `just test compile`
4. `just test unit-basic`
5. `just lint clippy-bins`
6. `just lint clippy-lib`
7. `just test baseline`

Reason:

- this preserves the audited narrow upstream-regression contract
- widening the lane while also going multi-platform would confound timing and
  blame assignment

### 2. Convert the required baseline workflow to a 3-platform matrix

Required workflow target shape:

- workflow name remains `baseline`
- job matrix:
  - `ubuntu-latest`
  - `macos-latest`
  - `windows-latest`
- same step sequence on all three platforms
- steps still invoke only `just ...` commands

Reason:

- this satisfies the original "parallel multi-platform gate" goal without
  reintroducing the old monolithic `ci.yml`

### 3. Keep heavyweight workflows out of ordinary required PR gating

Do not move these back into required ordinary PR CI:

- `ci.yml`
- `conformance.yml`
- `fuzz.yml`
- `bench.yml`
- `semver.yml`
- `model-catalog-drift.yml`

Reason:

- they are broader contracts, not the final Phase A baseline contract
- the Phase A objective is a measured narrow gate, not full repo certification

### 4. Record final measured timings on the merged target branch

The final proof artifact must use the merged target branch, not just the sprint
branch.

Required timing table:

- Linux total
- macOS total
- Windows total
- per-step times for each platform
- exact run URL / ID / SHA

Reason:

- the earlier A7 evidence problem was that the sprint branch was fast while the
  actual merged target branch was slower

## Expected Timing Outcome

Observed merged-target Linux run before the `just help` fix:

- run `28736534784`
- total `12m33s`
- `Just help` alone took `4m29s`

Measured local help behavior after the fix:

- `just help` is `0.09s`

Projected merged-target Linux total after removing the bogus help cost:

- about `8m04s`

This does not prove macOS or Windows timing, but it makes the target plausible:

- per-platform final baseline in the `10-20 minute` window
- parallel wall clock bounded by the slowest platform rather than the sum

## Acceptance Criteria

Phase A can reasonably claim it achieved its original final-state goal only when
all of the following are true:

1. `baseline` is the required PR workflow.
2. `baseline` runs on Linux, macOS, and Windows in parallel.
3. Each platform runs the same required `just` lane sequence.
4. The final merged target branch has a green run on all three platforms.
5. The final evidence package records:
   - platform runtimes
   - per-step runtimes
   - exact run URLs / IDs / SHA
6. The operator ledger remains current and states:
   - what the baseline tests
   - what it does not test
   - measured lane-specific coverage
   - relationship to broader upstream workflows

## What Phase A Should Claim After This

Once the closure steps above are completed, the accurate claim is:

- Phase A established a measured narrow upstream-regression baseline through
  `just`
- that baseline is required on Linux, macOS, and Windows in parallel
- the baseline has measured narrow coverage and explicit scope boundaries
- broader upstream workflows remain available outside the required gate

What it still should not claim:

- full upstream proof
- high production-code coverage
- replacement for conformance/fuzz/bench/semver regimes
