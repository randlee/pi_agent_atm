# Upstream Testing Contract Review

Date: 2026-07-03
Upstream: `Dicklesworthstone/pi_agent_rust`
Scope: determine which upstream testing contracts remain authoritative even if
Phase A simplifies ordinary PR CI in the fork.

## Summary

- Upstream treats suite taxonomy and test evidence as a single contract.
- Fast PR coverage is already stratified away from full certification,
  full extension validation, and long-running fuzz/perf evidence.
- Simplifying CI is viable, but only if the plan explicitly preserves the
  ability to run displaced contracts on manual or scheduled triggers.

## Core Upstream Contract Surfaces

- `docs/testing-policy.md`
  - binds taxonomy, JSONL logs, artifact schemas, failure digests, and replay
    bundles together
- `docs/qa-runbook.md`
  - defines quick-start, full verification, replay, triage, and CI lane
    expectations
- `docs/provider-test-obligations.md`
  - defines provider unit, contract, VCR, and E2E obligations
- `docs/TEST_COVERAGE_MATRIX.md`
  - machine-governed inventory and drift expectations

## Workflow-Level Conclusions

- `ci.yml`
  - broad cross-OS compile/test/policy workflow
  - still not equivalent to release or certification proof
- `conformance.yml`
  - PR mode is intentionally a fast sample only
  - full coverage is nightly or weekly
- `fuzz.yml`
  - PR mode is bounded fuzz smoke
  - long burn-ins and dashboard refresh are scheduled/manual
- `semver.yml`
  - path-filtered Rust API compatibility only
- `model-catalog-drift.yml`
  - advisory by default unless repo variables promote it to gating

## What Phase A Cannot Casually Drop

- suite classification enforcement
- no-mock and VCR leak guards
- replay/evidence artifact validation expectations
- provider test obligations if provider support remains in scope
- scenario/SLI traceability if parity or E2E claims remain in scope

## Best Simplification Target

The safest early simplification is a single required `baseline` workflow that
proves:

1. the code compiles
2. a genuinely basic unit subset passes
3. later lint and smoke layers can be added incrementally

Everything heavier should remain explicitly runnable by retained manual or
scheduled workflows, not silently discarded.
