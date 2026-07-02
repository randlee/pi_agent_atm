set shell := ["bash", "-euo", "pipefail", "-c"]

python_cmd := if os_family() == "windows" { "python" } else { "python3" }

# Show the curated repo task help.
default: help

# Show the curated repo task help.
help:
    {{python_cmd}} .just/print_help.py

# Explain lint/test lane semantics from the shared catalogs.
explain domain='' lane='':
    {{python_cmd}} .just/explain.py {{domain}} {{lane}}

# Remove workspace build artifacts.
clean:
    cargo clean

[private]
_fmt-check:
    cargo fmt --all --check

[private]
_fmt-write:
    cargo fmt --all

# Format the Rust workspace or run the formatting gate.
fmt mode='check':
    {{python_cmd}} .just/run_fmt.py {{mode}}

[private]
_lint-fmt:
    @just fmt check

[private]
_lint-clippy-lib:
    {{python_cmd}} .just/run_cargo.py clippy --no-deps --lib -- -D warnings

[private]
_lint-clippy-bins:
    {{python_cmd}} .just/run_cargo.py clippy --no-deps --bins -- -D warnings

[private]
_lint-clippy-tests:
    {{python_cmd}} .just/run_cargo.py clippy --no-deps --tests -- -D warnings

[private]
_lint-clippy-benches:
    {{python_cmd}} .just/run_cargo.py clippy --no-deps --benches -- -D warnings

[private]
_lint-clippy-examples:
    {{python_cmd}} .just/run_cargo.py clippy --no-deps --examples -- -D warnings

# Run the repo lint suite or one child gate.
lint target='all':
    {{python_cmd}} .just/run_lint.py {{target}}

# Run the repo QA/test suite or one child lane.
test target='ci':
    {{python_cmd}} .just/run_test.py {{target}}

# Run the local CI-equivalent gate.
ci: lint test

# Run the quick unified fuzz pipeline (P1 + short P2 smoke).
fuzz:
    @just test fuzz

# Run the full unified fuzz pipeline.
fuzz-full:
    @just test fuzz-full

# Run all Criterion benches.
bench:
    {{python_cmd}} .just/run_cargo.py bench --benches

# Print the current suite taxonomy from tests/suite_classification.toml.
suites:
    {{python_cmd}} .just/show_suites.py
