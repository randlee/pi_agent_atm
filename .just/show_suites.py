#!/usr/bin/env python3
from __future__ import annotations

from unit_basic_audit import UNIT_BASIC_INCLUDE_PREFIXES

from lint_catalog import OPTIONAL_LANES as OPTIONAL_LINT_LANES
from test_catalog import LANES
from test_catalog import OPTIONAL_LANES as OPTIONAL_TEST_LANES
from test_catalog import SUITE_ORDER
from test_catalog import load_suite_targets


UPSTREAM_REQUIRED_LANES = (
    "lint.clippy-bins",
    "lint.clippy-lib",
    "test.compile",
    "test.unit-basic",
    "test.baseline",
)


def emit_record(fields: list[tuple[str, str]]) -> None:
    for key, value in fields:
        print(f"{key}={value}")
    print()


def main() -> int:
    emit_record(
        [
            ("lane_group", "upstream-required"),
            ("source", ".just/lint_catalog.py,.just/test_catalog.py"),
            ("members", ",".join(UPSTREAM_REQUIRED_LANES)),
        ]
    )
    emit_record(
        [
            ("lane_group", "local-optional"),
            ("source", ".just/lint_catalog.py,.just/test_catalog.py"),
            (
                "members",
                ",".join(
                    [*(f"lint.{name}" for name in OPTIONAL_LINT_LANES), *(f"test.{name}" for name in OPTIONAL_TEST_LANES)]
                ),
            ),
        ]
    )
    emit_record(
        [
            ("lane_group", "atm-owned"),
            ("source", "reserved-prefix"),
            ("prefix", "atm-"),
            ("members", "(none)"),
        ]
    )
    emit_record(
        [
            ("lane_group", "integration-owned"),
            ("source", "reserved-prefix"),
            ("prefix", "integration-"),
            ("members", "(none)"),
        ]
    )
    for suite in SUITE_ORDER:
        emit_record(
            [
                ("suite", suite),
                ("origin", "repo-classification"),
                ("source", "tests/suite_classification.toml"),
                ("targets", str(len(load_suite_targets(suite)))),
            ]
        )
    emit_record(
        [
            ("suite", "unit-basic-inline"),
            ("origin", "upstream"),
            ("source", ".just/unit_basic_audit.py"),
            ("prefixes", str(len(UNIT_BASIC_INCLUDE_PREFIXES))),
            ("strict_addons", "6"),
        ]
    )
    emit_record(
        [
            ("suite", "smoke-baseline"),
            ("origin", LANES["baseline"].origin),
            ("source", LANES["baseline"].ssot),
            ("targets", str(len(LANES["baseline"].documented_targets))),
            ("members", ",".join(LANES["baseline"].documented_targets)),
        ]
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
