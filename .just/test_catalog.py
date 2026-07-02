#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


SUITE_ORDER = ("unit", "vcr", "e2e")


@dataclass(frozen=True)
class TestLane:
    name: str
    description: str
    kind: str
    verify_args: tuple[str, ...] = ()
    suite_name: str | None = None
    script_args: tuple[str, ...] = ()


LANES = {
    "ci": TestLane(
        name="ci",
        description="Run the CI-equivalent QA lane without lint.",
        kind="verify",
        verify_args=("--profile", "ci", "--skip-lint"),
    ),
    "all": TestLane(
        name="all",
        description="Run the full classified test surface without lint.",
        kind="verify",
        verify_args=("--profile", "full", "--skip-lint"),
    ),
    "unit": TestLane(
        name="unit",
        description="Run inline lib tests plus the classified unit suite.",
        kind="verify",
        verify_args=("--profile", "quick", "--skip-lint"),
    ),
    "integration": TestLane(
        name="integration",
        description="Run all non-E2E integration targets.",
        kind="verify",
        verify_args=("--profile", "ci", "--skip-lint", "--skip-e2e"),
    ),
    "vcr": TestLane(
        name="vcr",
        description="Run only the classified VCR / fixture replay targets.",
        kind="suite",
        suite_name="vcr",
    ),
    "e2e": TestLane(
        name="e2e",
        description="Run only the classified E2E targets.",
        kind="verify",
        verify_args=("--profile", "full", "--skip-lint", "--skip-unit"),
    ),
    "fuzz": TestLane(
        name="fuzz",
        description="Run the quick unified fuzz pipeline.",
        kind="script",
        script_args=("./scripts/fuzz_e2e.sh", "--quick"),
    ),
    "fuzz-full": TestLane(
        name="fuzz-full",
        description="Run the full unified fuzz pipeline.",
        kind="script",
        script_args=("./scripts/fuzz_e2e.sh",),
    ),
}

ALIASES = {
    "full": "all",
    "integrate": "integration",
}

DISPLAY_ORDER = ("ci", "all", "unit", "integration", "vcr", "e2e", "fuzz", "fuzz-full")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_suite_targets(suite: str) -> list[str]:
    payload = tomllib.loads((repo_root() / "tests/suite_classification.toml").read_text())
    return list(payload["suite"][suite]["files"])


def resolve_lane(target: str) -> TestLane:
    canonical = ALIASES.get(target, target)
    lane = LANES.get(canonical)
    if lane is None:
        expected = ", ".join([*DISPLAY_ORDER, *ALIASES])
        raise SystemExit(f"unknown test target: {target}; expected one of: {expected}")
    return lane


def display_targets() -> list[tuple[str, str]]:
    return [(name, LANES[name].description) for name in DISPLAY_ORDER]
