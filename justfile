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

test lane='':
    {{python_cmd}} .just/run_test.py {{lane}}
