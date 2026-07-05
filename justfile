set shell := ["bash", "-euo", "pipefail", "-c"]

python_cmd := if os_family() == "windows" { "python" } else { "python3" }

default: help

help:
    {{python_cmd}} .just/print_help.py

[private]
_fmt-check:
    cargo fmt --all --check

[private]
_fmt-write:
    cargo fmt --all

fmt mode='check':
    {{python_cmd}} .just/run_fmt.py {{mode}}

[private]
_lint-clippy-bins:
    {{python_cmd}} .just/run_cargo.py clippy --no-deps --bins -- -D warnings

[private]
_lint-clippy-lib:
    {{python_cmd}} .just/run_cargo.py clippy --no-deps --lib -- -D warnings

lint target='all':
    {{python_cmd}} .just/run_lint.py {{target}}

test lane='':
    {{python_cmd}} .just/run_test.py {{lane}}
