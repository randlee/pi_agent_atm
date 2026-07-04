#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

from lint_catalog import lane_command as lint_lane_command
from lint_catalog import resolve_lane as resolve_lint_lane
from test_catalog import lane_command as test_lane_command
from test_catalog import resolve_lane as resolve_test_lane


def repo_name() -> str:
    return Path(__file__).resolve().parent.parent.name


def emit_record(fields: list[tuple[str, str]]) -> int:
    for key, value in fields:
        print(f"{key}={value}")
    return 0


def explain_lint(target: str) -> int:
    lane = resolve_lint_lane(target)
    fields = [
        ("domain", "lint"),
        ("lane", lane.name),
        ("origin", lane.origin),
        ("owner", lane.owner),
        ("blocking", lane.blocking),
        ("ssot", lane.ssot),
        ("command", lint_lane_command(lane)),
    ]
    if lane.children:
        fields.append(("children", ",".join(lane.children)))
    return emit_record(fields)


def explain_test(target: str) -> int:
    lane = resolve_test_lane(target)
    fields = [
        ("domain", "test"),
        ("lane", lane.name),
        ("origin", lane.origin),
        ("owner", lane.owner),
        ("blocking", lane.blocking),
        ("ssot", lane.ssot),
        ("command", test_lane_command(lane)),
    ]
    if lane.documented_targets:
        fields.append(("documented_targets", ",".join(lane.documented_targets)))
    return emit_record(fields)


def main() -> int:
    domain = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else ""
    target = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else ""
    if not domain or not target:
        print(f"{repo_name()} explain")
        print()
        print("Usage:")
        print("  just explain lint <lane>")
        print("  just explain test <lane>")
        return 0
    if domain == "lint":
        return explain_lint(target)
    if domain == "test":
        return explain_test(target)
    raise SystemExit(f"unknown explain domain: {domain}; expected one of: lint, test")


if __name__ == "__main__":
    raise SystemExit(main())
