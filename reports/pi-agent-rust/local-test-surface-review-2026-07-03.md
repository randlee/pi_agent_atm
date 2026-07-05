# Local Test Surface Review

Date: 2026-07-03
Branch: `plan/phase-A`
Scope: classify which current local tests are safe for an early "basic unit"
gate versus which are really integration, artifact-audit, benchmark, or
binary-launching tests.

## Summary

- `suite.unit` is not the same thing as a strict basic-unit lane.
- The written policy defines unit tests as pure logic with no fixtures, VCR, or
  mocks.
- The same policy also documents a curated `tests/*.rs` subset under the unit
  umbrella, which already blurs strict unit and deterministic integration
  testing.
- Several current `[suite.unit]` files shell out to scripts, inspect fixtures,
  launch binaries, or audit generated artifacts.

## Key Evidence

### Policy mismatch

- `docs/testing-policy.md`
  - defines Suite 1 as pure logic, parsing, serialization, state machines
  - forbids fixtures, VCR, and mock-like replacements
  - shows `cargo test --all-targets --lib` plus a curated `tests/*.rs` subset
- `tests/suite_classification.toml`
  - places many non-trivial deterministic tests under `[suite.unit]`

### Heavy `[suite.unit]` examples that should not define an early basic-unit gate

- `tests/bench_schema.rs`
  - shells out to `bash`
  - drives `scripts/perf/orchestrate.sh`
- `tests/perf_regression.rs`
  - resolves `CARGO_BIN_EXE_pi`
  - launches the real `pi` binary
- `tests/franken_node_compat_harness.rs`
  - shells out to `node`, `bun`, and `which`
- `tests/qa_docs_policy_validation.rs`
  - runs `python3 -m py_compile`
  - shells out to benchmark/perf scripts
- `tests/rch_artifact_sync_preflight.rs`
  - repeatedly runs `python3 scripts/check_rch_artifact_sync.py`
- `tests/vcr_parity_validation.rs`
  - validates VCR cassette inventory
- `tests/provider_closure_truth_table.rs`
  - inspects docs JSON plus cassette presence
- `tests/mock_spec_schema.rs`
  - validates ext-conformance fixture JSON against schema
- `tests/e2e_replay_bundle_validation.rs`
  - audits E2E replay conventions and `scripts/e2e/run_all.sh`

## Recommended Early Basic-Unit Gate

Use an explicit `unit-basic` lane instead of deriving from all of
`[suite.unit]`.

Recommended first-pass contents:

1. `cargo test --all-targets --lib`
2. Small curated `tests/*.rs` allowlist:
   - `capability_policy_model`
   - `policy_profile_hardening`
   - `extension_flag_passthrough`
   - `model_serialization`
   - `redaction_test`
   - `extension_scoring_ope`

## Recommended Explicit Exclusions

Do not include these in the early basic-unit gate:

- `bench_schema`
- `perf_regression`
- `franken_node_compat_harness`
- `qa_docs_policy_validation`
- `rch_artifact_sync_preflight`
- VCR/fixture audit tests
- binary-launching tests
- artifact/regeneration audit tests
- subsystem stress or concurrency endurance tests
