#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TestLane:
    name: str
    description: str
    commands: tuple[tuple[str, ...], ...]


LANES = {
    "compile": TestLane(
        name="compile",
        description="Run cargo check across all targets.",
        commands=(("check", "--all-targets"),),
    ),
    "unit-basic": TestLane(
        name="unit-basic",
        description="Run lib tests plus the strict basic-unit allowlist.",
        commands=(
            ("test", "--all-targets", "--lib"),
            ("test", "--test", "capability_policy_model", "--", "--nocapture"),
            ("test", "--test", "policy_profile_hardening", "--", "--nocapture"),
            ("test", "--test", "extension_flag_passthrough", "--", "--nocapture"),
            ("test", "--test", "model_serialization", "--", "--nocapture"),
            ("test", "--test", "redaction_test", "--", "--nocapture"),
            ("test", "--test", "extension_scoring_ope", "--", "--nocapture"),
        ),
    ),
}

DISPLAY_ORDER = ("compile", "unit-basic")


def resolve_lane(target: str) -> TestLane:
    canonical = target or "unit-basic"
    lane = LANES.get(canonical)
    if lane is None:
        expected = ", ".join(DISPLAY_ORDER)
        raise SystemExit(f"unknown test target: {target}; expected one of: {expected}")
    return lane


def display_targets() -> list[tuple[str, str]]:
    return [(name, LANES[name].description) for name in DISPLAY_ORDER]
