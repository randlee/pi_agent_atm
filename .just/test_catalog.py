#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TestLane:
    name: str
    description: str
    commands: tuple[tuple[str, ...], ...]


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


UNIT_BASIC_SKIP_FILTERS = (
    # Documented category: subsystem stress/endurance tests. This case
    # intentionally waits on a timeout path and is the approved A1 exclusion.
    "permission_request_times_out_fail_closed",
)


LANES = {
    "compile": TestLane(
        name="compile",
        description="Run cargo check across all targets.",
        commands=(("check", "--all-targets"),),
    ),
    "unit-basic": TestLane(
        name="unit-basic",
        description="Run the documented unit-basic base plus strict add-on tests.",
        commands=(
            # The sprint docs say "cargo test --all-targets --lib", but Cargo
            # forwards harness flags like `--skip` into benchmark/example
            # binaries under `--all-targets`; those harnesses reject `--skip`,
            # so the documented exclusion mechanism is only implementable
            # against the full library test sweep.
            cargo_test(
                "--lib",
                skip_filters=UNIT_BASIC_SKIP_FILTERS,
            ),
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
