#!/usr/bin/env python3
from __future__ import annotations

from unit_basic_audit import UNIT_BASIC_INCLUDE_PREFIXES

from lint_catalog import DISPLAY_ORDER as LINT_DISPLAY_ORDER
from lint_catalog import LANES as LINT_LANES
from test_catalog import LANES
from test_catalog import DISPLAY_ORDER as TEST_DISPLAY_ORDER
from test_catalog import SUITE_ORDER
from test_catalog import load_suite_targets


def lane_members(prefix: str, display_order: tuple[str, ...], lanes: dict[str, object], blocking: str) -> list[str]:
    return [f"{prefix}.{name}" for name in display_order if lanes[name].blocking == blocking]


def emit_record(fields: list[tuple[str, str]]) -> None:
    for key, value in fields:
        print(f"{key}={value}")
    print()


def main() -> int:
    emit_record(
        [
            ("lane_group", "upstream-required"),
            ("source", ".just/lint_catalog.py,.just/test_catalog.py"),
            (
                "members",
                ",".join(
                    [
                        *lane_members("lint", LINT_DISPLAY_ORDER, LINT_LANES, "required"),
                        *lane_members("test", TEST_DISPLAY_ORDER, LANES, "required"),
                    ]
                ),
            ),
        ]
    )
    emit_record(
        [
            ("lane_group", "local-optional"),
            ("source", ".just/lint_catalog.py,.just/test_catalog.py"),
            (
                "members",
                ",".join(
                    [
                        *lane_members("lint", LINT_DISPLAY_ORDER, LINT_LANES, "optional"),
                        *lane_members("test", TEST_DISPLAY_ORDER, LANES, "optional"),
                    ]
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
