#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class TestLane:
    name: str
    description: str
    command_factory: Callable[[], tuple[tuple[str, ...], ...]]

    @property
    def commands(self) -> tuple[tuple[str, ...], ...]:
        return self.command_factory()


def cargo_test(
    *args: str,
    skip_filters: tuple[str, ...] = (),
    nocapture: bool = False,
) -> tuple[str, ...]:
    command = ["test", *args]
    harness_args: list[str] = []
    for skip_filter in skip_filters:
        harness_args.extend(("--skip", skip_filter))
    if nocapture:
        harness_args.append("--nocapture")
    if harness_args:
        command.extend(("--", *harness_args))
    return tuple(command)


def unit_basic_inline_commands() -> tuple[tuple[str, ...], ...]:
    from unit_basic_audit import unit_basic_inline_commands as audited_unit_basic_commands

    commands: list[tuple[str, ...]] = []
    for prefix, skip_filters in audited_unit_basic_commands():
        commands.append(
            cargo_test(
                "--lib",
                prefix,
                skip_filters=skip_filters,
            )
        )
    return tuple(commands)


LANES = {
    "compile": TestLane(
        name="compile",
        description="Run cargo check across all targets.",
        command_factory=lambda: (("check", "--all-targets"),),
    ),
    "unit-basic": TestLane(
        name="unit-basic",
        description="Run the audited inline allowlist plus strict add-on tests.",
        command_factory=lambda: (
            *unit_basic_inline_commands(),
            cargo_test("--test", "capability_policy_model", nocapture=True),
            cargo_test("--test", "policy_profile_hardening", nocapture=True),
            cargo_test("--test", "extension_flag_passthrough", nocapture=True),
            cargo_test("--test", "model_serialization", nocapture=True),
            cargo_test("--test", "redaction_test", nocapture=True),
            cargo_test("--test", "extension_scoring_ope", nocapture=True),
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
