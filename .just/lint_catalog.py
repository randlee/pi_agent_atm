#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LintLane:
    name: str
    description: str
    children: tuple[str, ...] = ()
    recipe: str | None = None


LANES = {
    "all": LintLane(
        name="all",
        description="Run the repo lint suite across all local surfaces.",
        children=("fmt", "clippy"),
    ),
    "fmt": LintLane(
        name="fmt",
        description="Run only the format check.",
        recipe="_lint-fmt",
    ),
    "clippy": LintLane(
        name="clippy",
        description="Run Clippy across all local target classes without dependencies.",
        children=(
            "clippy-lib",
            "clippy-bins",
            "clippy-tests",
            "clippy-benches",
            "clippy-examples",
        ),
    ),
    "clippy-lib": LintLane(
        name="clippy-lib",
        description="Run Clippy on the library target.",
        recipe="_lint-clippy-lib",
    ),
    "clippy-bins": LintLane(
        name="clippy-bins",
        description="Run Clippy on binary targets.",
        recipe="_lint-clippy-bins",
    ),
    "clippy-tests": LintLane(
        name="clippy-tests",
        description="Run Clippy on integration-test targets.",
        recipe="_lint-clippy-tests",
    ),
    "clippy-benches": LintLane(
        name="clippy-benches",
        description="Run Clippy on benchmark targets.",
        recipe="_lint-clippy-benches",
    ),
    "clippy-examples": LintLane(
        name="clippy-examples",
        description="Run Clippy on example targets.",
        recipe="_lint-clippy-examples",
    ),
    "check": LintLane(
        name="check",
        description="Run broad cargo check coverage across all local targets.",
        recipe="_lint-check",
    ),
}

DISPLAY_ORDER = (
    "all",
    "fmt",
    "clippy",
    "clippy-lib",
    "clippy-bins",
    "clippy-tests",
    "clippy-benches",
    "clippy-examples",
    "check",
)


def resolve_lane(target: str) -> LintLane:
    lane = LANES.get(target)
    if lane is None:
        expected = ", ".join(DISPLAY_ORDER)
        raise SystemExit(f"unknown lint target: {target}; expected one of: {expected}")
    return lane


def display_lanes() -> list[tuple[str, str]]:
    return [(name, LANES[name].description) for name in DISPLAY_ORDER]
