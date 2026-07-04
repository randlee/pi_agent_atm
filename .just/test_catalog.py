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


UNIT_BASIC_LIB_COMMANDS = (
    cargo_test(
        "--lib",
        "acp::tests",
        skip_filters=("permission_request_times_out_fail_closed",),
    ),
    cargo_test("--lib", "agent::compatible_tool_parallelism_tests"),
    cargo_test("--lib", "agent::message_queue_tests"),
    cargo_test("--lib", "agent::tests"),
    cargo_test("--lib", "agent::tool_effect_batch_planning_tests"),
    cargo_test("--lib", "agent::turn_event_tests"),
    cargo_test("--lib", "agent_cx::tests"),
    cargo_test("--lib", "app::tests"),
    cargo_test("--lib", "cli::tests"),
    cargo_test("--lib", "compaction::tests"),
    cargo_test("--lib", "config::tests"),
    cargo_test("--lib", "flake_classifier::tests"),
    cargo_test("--lib", "model::tests"),
    cargo_test("--lib", "models::tests"),
    cargo_test("--lib", "permissions::tests"),
    cargo_test("--lib", "platform::tests"),
    cargo_test("--lib", "provider::tests"),
    cargo_test("--lib", "provider_metadata::tests"),
    cargo_test("--lib", "resources::tests"),
    cargo_test("--lib", "session::tests"),
    cargo_test("--lib", "sse::tests"),
)


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
            *UNIT_BASIC_LIB_COMMANDS,
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
