#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

from lint_catalog import DISPLAY_ORDER as LINT_DISPLAY_ORDER
from lint_catalog import LANES as LINT_LANES
from lint_catalog import resolve_lane as resolve_lint_lane
from test_catalog import DISPLAY_ORDER as TEST_DISPLAY_ORDER
from test_catalog import LANES as TEST_LANES
from test_catalog import SUITE_ORDER
from test_catalog import load_suite_targets
from test_catalog import resolve_lane as resolve_test_lane


def repo_name() -> str:
    return Path(__file__).resolve().parent.parent.name


def lint_command(name: str) -> str:
    return {
        "fmt": "cargo fmt --all --check",
        "clippy-lib": "cargo clippy --no-deps --lib -- -D warnings",
        "clippy-bins": "cargo clippy --no-deps --bins -- -D warnings",
        "clippy-tests": "cargo clippy --no-deps --tests -- -D warnings",
        "clippy-benches": "cargo clippy --no-deps --benches -- -D warnings",
        "clippy-examples": "cargo clippy --no-deps --examples -- -D warnings",
    }.get(name, "")


def explain_lint(target: str | None) -> str:
    if not target:
        lines = [
            "Lint lanes",
            "",
            "`just lint` means local surfaces only. It does not lint third-party dependencies.",
            "",
            "Default aggregate:",
            "- `just lint` runs `fmt` and `clippy`.",
            "",
            "Child lanes:",
        ]
        for name in LINT_DISPLAY_ORDER:
            if name == "all":
                continue
            lane = LINT_LANES[name]
            lines.append(f"- `just lint {name}`: {lane.description}")
            command = lint_command(name)
            if command:
                lines.append(f"  command: `{command}`")
        return "\n".join(lines)

    lane = resolve_lint_lane(target)
    lines = [f"Lint lane: `{target}`", "", lane.description]
    if lane.children:
        lines.append("")
        lines.append("Children:")
        for child in lane.children:
            child_lane = LINT_LANES[child]
            lines.append(f"- `{child}`: {child_lane.description}")
    command = lint_command(target)
    if command:
        lines.append("")
        lines.append(f"Command: `{command}`")
    if target.startswith("clippy-"):
        lines.append("")
        lines.append("Scope: local code only (`--no-deps`).")
    return "\n".join(lines)


def test_command(name: str) -> str:
    lane = TEST_LANES[name]
    if lane.kind == "verify":
        return "./verify " + " ".join(lane.verify_args)
    if lane.kind == "script":
        return " ".join(lane.script_args)
    if lane.kind == "suite":
        assert lane.suite_name is not None
        return f"cargo test --test <each target in suite.{lane.suite_name}> -- --nocapture"
    return ""


def explain_test(target: str | None) -> str:
    if not target:
        unit_count = len(load_suite_targets("unit"))
        vcr_count = len(load_suite_targets("vcr"))
        e2e_count = len(load_suite_targets("e2e"))
        lines = [
            "Test lanes",
            "",
            "Repo taxonomy:",
            f"- `unit`: classified unit-style test targets in `tests/suite_classification.toml` ({unit_count} targets)",
            f"- `vcr`: deterministic replay / fixture-backed targets ({vcr_count} targets)",
            f"- `e2e`: live/full-system workflow targets ({e2e_count} targets)",
            "",
            "Important distinction:",
            "- `cargo test --lib` runs inline unit tests inside `src/**`.",
            "- `just test unit` means inline lib tests plus the repo-classified `suite.unit` targets.",
            "",
            "Available lanes:",
        ]
        for name in TEST_DISPLAY_ORDER:
            lane = TEST_LANES[name]
            lines.append(f"- `just test {name}`: {lane.description}")
            lines.append(f"  command: `{test_command(name)}`")
        return "\n".join(lines)

    lane = resolve_test_lane(target)
    lines = [f"Test lane: `{target}`", "", lane.description, ""]
    lines.append(f"Command: `{test_command(lane.name)}`")
    if lane.name == "baseline":
        lines.extend(
            [
                "",
                "Behavior:",
                "- runs the smoke baseline in a temp artifact directory",
                "- sanitizes provider credential env vars before executing targets",
                "- covers a curated subset of unit-style and VCR-style targets",
            ]
        )
    elif lane.name == "unit":
        unit_count = len(load_suite_targets("unit"))
        lines.extend(
            [
                "",
                "Behavior:",
                "- includes inline lib tests via `./verify --profile quick`",
                f"- includes the repo-classified `suite.unit` targets ({unit_count} targets)",
            ]
        )
    elif lane.kind == "suite" and lane.suite_name is not None:
        suite_targets = load_suite_targets(lane.suite_name)
        lines.extend(
            [
                "",
                f"Suite `{lane.suite_name}` target count: {len(suite_targets)}",
                "Source of truth: `tests/suite_classification.toml`",
            ]
        )
    elif lane.kind == "verify":
        lines.extend(
            [
                "",
                "Source of truth:",
                "- `tests/suite_classification.toml` for target membership",
                "- `scripts/e2e/run_all.sh` for `verify` profile semantics",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    domain = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else ""
    target = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else None
    if not domain:
        print(f"{repo_name()} explain")
        print()
        print("Usage:")
        print("  just explain lint [lane]")
        print("  just explain test [lane]")
        return 0
    if domain == "lint":
        print(explain_lint(target))
        return 0
    if domain == "test":
        print(explain_test(target))
        return 0
    raise SystemExit(f"unknown explain domain: {domain}; expected one of: lint, test")


if __name__ == "__main__":
    raise SystemExit(main())
