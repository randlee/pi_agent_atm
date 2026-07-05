#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LintLane:
    name: str
    description: str
    children: tuple[str, ...] = ()
    recipe: str | None = None
    cargo_args: tuple[str, ...] = ()


LANES = {
    "all": LintLane(
        name="all",
        description="Run the required local-code lint lanes.",
        children=("clippy-bins", "clippy-lib"),
    ),
    "clippy-bins": LintLane(
        name="clippy-bins",
        description="Run Clippy on binary targets only.",
        recipe="_lint-clippy-bins",
        cargo_args=("clippy", "--no-deps", "--bins", "--", "-D", "warnings"),
    ),
    "clippy-lib": LintLane(
        name="clippy-lib",
        description="Run Clippy on the library target only.",
        recipe="_lint-clippy-lib",
        cargo_args=("clippy", "--no-deps", "--lib", "--", "-D", "warnings"),
    ),
}

DISPLAY_ORDER = (
    "all",
    "clippy-bins",
    "clippy-lib",
)


def resolve_lane(target: str) -> LintLane:
    lane = LANES.get(target)
    if lane is None:
        expected = ", ".join(DISPLAY_ORDER)
        raise SystemExit(f"unknown lint target: {target}; expected one of: {expected}")
    return lane


def display_lanes() -> list[tuple[str, str]]:
    return [(name, LANES[name].description) for name in DISPLAY_ORDER]
