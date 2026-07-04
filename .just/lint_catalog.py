#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LintLane:
    name: str
    description: str
    origin: str
    owner: str
    blocking: str
    ssot: str
    children: tuple[str, ...] = ()
    cargo_args: tuple[str, ...] = ()
    steps: tuple[tuple[str, ...], ...] = ()


def cargo_step(*args: str) -> tuple[str, ...]:
    return ("cargo", *args)


def fmt_step(mode: str) -> tuple[str, ...]:
    return ("fmt", mode)


def lane_step(name: str) -> tuple[str, ...]:
    return ("lane", name)


LANES = {
    "all": LintLane(
        name="all",
        description="Run the required local-code lint lanes.",
        origin="upstream",
        owner=".just/lint_catalog.py",
        blocking="local-aggregate",
        ssot=".just/lint_catalog.py",
        children=("clippy-bins", "clippy-lib"),
    ),
    "clippy-bins": LintLane(
        name="clippy-bins",
        description="Run Clippy on binary targets only.",
        origin="upstream",
        owner=".just/lint_catalog.py",
        blocking="required",
        ssot=".just/lint_catalog.py",
        cargo_args=("clippy", "--no-deps", "--bins", "--", "-D", "warnings"),
    ),
    "clippy-lib": LintLane(
        name="clippy-lib",
        description="Run Clippy on the library target only.",
        origin="upstream",
        owner=".just/lint_catalog.py",
        blocking="required",
        ssot=".just/lint_catalog.py",
        cargo_args=("clippy", "--no-deps", "--lib", "--", "-D", "warnings"),
    ),
    "all-local": LintLane(
        name="all-local",
        description="Run the optional richer local-only lint sweep.",
        origin="local",
        owner=".just/lint_catalog.py",
        blocking="optional",
        ssot=".just/lint_catalog.py",
        steps=(
            fmt_step("check"),
            lane_step("clippy-bins"),
            lane_step("clippy-lib"),
            cargo_step("clippy", "--no-deps", "--tests", "--", "-D", "warnings"),
            cargo_step("clippy", "--no-deps", "--benches", "--", "-D", "warnings"),
            cargo_step("clippy", "--no-deps", "--examples", "--", "-D", "warnings"),
        ),
    ),
}

OPTIONAL_LANES = ("all-local",)

DISPLAY_ORDER = (
    "all",
    "clippy-bins",
    "clippy-lib",
    "all-local",
)


def resolve_lane(target: str) -> LintLane:
    lane = LANES.get(target)
    if lane is None:
        expected = ", ".join(DISPLAY_ORDER)
        raise SystemExit(f"unknown lint target: {target}; expected one of: {expected}")
    return lane


def display_lanes() -> list[tuple[str, str]]:
    return [(name, LANES[name].description) for name in DISPLAY_ORDER]


def lane_names_by_blocking(blocking: str) -> list[str]:
    return [name for name in DISPLAY_ORDER if LANES[name].blocking == blocking]


def step_command(step: tuple[str, ...]) -> str:
    kind, *args = step
    if kind == "cargo":
        return "cargo " + " ".join(args)
    if kind == "fmt":
        return "just fmt " + " ".join(args)
    if kind == "lane":
        return "just lint " + args[0]
    raise ValueError(f"unsupported lint step kind: {kind}")


def lane_command(lane: LintLane) -> str:
    if lane.cargo_args:
        return "cargo " + " ".join(lane.cargo_args)
    if lane.steps:
        return " && ".join(step_command(step) for step in lane.steps)
    if lane.children:
        return ", ".join(lane.children)
    return ""
