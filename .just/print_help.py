#!/usr/bin/env python3
from __future__ import annotations

from lint_catalog import display_lanes
from pathlib import Path

from test_catalog import display_targets


SECTIONS = (
    (
        "General",
        (
            ("help", "Show this help."),
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
        tuple(
            [("lint", "Run the required local-code lint lanes.")]
            + [(f"lint {name}", description) for name, description in display_lanes() if name != "all"]
        ),
    ),
    (
        "Test",
        tuple(
            [("test", "Run the default strict basic-unit lane.")]
            + [(f"test {name}", description) for name, description in display_targets()]
        ),
    ),
    (
        "Taxonomy",
        (
            ("explain <domain> <lane>", "Show lane taxonomy metadata from the SSOT catalog."),
            ("suites", "Show suite taxonomy and required-lane grouping metadata."),
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
