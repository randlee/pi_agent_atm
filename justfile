set shell := ["bash", "-euo", "pipefail", "-c"]

python_cmd := if os_family() == "windows" { "python" } else { "python3" }

default: help

help:
    {{python_cmd}} .just/print_help.py

fmt mode='check':
    {{python_cmd}} .just/run_fmt.py {{mode}}

lint target='all':
    {{python_cmd}} .just/run_lint.py {{target}}

test lane='':
    {{python_cmd}} .just/run_test.py {{lane}}

explain domain='' lane='':
    {{python_cmd}} .just/explain.py {{domain}} {{lane}}

suites:
    {{python_cmd}} .just/show_suites.py
