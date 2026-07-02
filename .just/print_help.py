#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from test_catalog import display_targets


SECTIONS = (
    (
        "General",
        (
            ("help", "Show this help."),
            ("ci", "Run the local CI-equivalent lint + test gate."),
            ("clean", "Remove workspace build artifacts."),
            ("bench", "Run the Criterion benchmark suite."),
            ("suites", "Print the current classified test-suite taxonomy."),
        ),
    ),
    (
        "Formatting",
        (
            ("fmt", "Check Rust formatting."),
            ("fmt check", "Check Rust formatting."),
            ("fmt write", "Format the Rust workspace in place."),
        ),
    ),
    (
        "Lint",
        (
            ("lint", "Run the full repo lint suite."),
            ("lint fmt", "Run only the format check."),
            ("lint clippy", "Run only Clippy with warnings denied."),
            ("lint check", "Run only cargo check across all targets."),
        ),
    ),
    (
        "Test",
        tuple(
            [("test", "Run the CI-equivalent QA lane without lint.")]
            + [(f"test {name}", description) for name, description in display_targets()]
        ),
    ),
)


def render_help(repo_name: str) -> str:
    lines = [
        f"{repo_name} task runner",
        "",
        "Usage:",
        "  just <recipe>",
        "",
    ]
    width = max(len(name) for _, recipes in SECTIONS for name, _ in recipes)
    for section_name, recipes in SECTIONS:
        lines.append(f"{section_name}:")
        for name, description in recipes:
            lines.append(f"  {name.ljust(width)}  {description}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    repo_name = Path(__file__).resolve().parent.parent.name
    print(render_help(repo_name), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
