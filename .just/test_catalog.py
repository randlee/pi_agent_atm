#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib
from unit_basic_audit import UNIT_BASIC_INCLUDE_PREFIXES
from unit_basic_audit import UNIT_BASIC_SKIP_FILTERS_BY_PREFIX


@dataclass(frozen=True)
class TestLane:
    name: str
    description: str
    kind: str
    origin: str
    owner: str
    blocking: str
    ssot: str
    verify_args: tuple[str, ...] = ()
    commands: tuple[tuple[str, ...], ...] = ()
    script_args: tuple[str, ...] = ()
    documented_targets: tuple[str, ...] = ()


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
    commands: list[tuple[str, ...]] = []
    for prefix in UNIT_BASIC_INCLUDE_PREFIXES:
        commands.append(
            cargo_test(
                "--lib",
                prefix,
                skip_filters=UNIT_BASIC_SKIP_FILTERS_BY_PREFIX.get(prefix, ()),
            )
        )
    return tuple(commands)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


SUITE_ORDER = ("unit", "vcr", "e2e")


def load_suite_targets(suite: str) -> list[str]:
    payload = tomllib.loads((repo_root() / "tests/suite_classification.toml").read_text())
    return list(payload["suite"][suite]["files"])


LANES = {
    "baseline": TestLane(
        name="baseline",
        description="Run the required six-target smoke baseline without lint.",
        kind="script",
        origin="upstream",
        owner=".just/test_catalog.py",
        blocking="required",
        ssot=".just/test_catalog.py",
        script_args=("./scripts/smoke.sh", "--skip-lint", "--no-rch", "--only", "unit"),
        documented_targets=(
            "model_serialization",
            "config_precedence",
            "session_conformance",
            "error_types",
            "compaction",
            "security_budgets",
        ),
    ),
    "compile": TestLane(
        name="compile",
        description="Run cargo check across all targets.",
        kind="cargo",
        origin="upstream",
        owner=".just/test_catalog.py",
        blocking="required",
        ssot=".just/test_catalog.py",
        commands=(("check", "--all-targets"),),
    ),
    "unit-basic": TestLane(
        name="unit-basic",
        description="Run the audited inline allowlist plus strict add-on tests.",
        kind="cargo",
        origin="upstream",
        owner=".just/test_catalog.py",
        blocking="required",
        ssot=".just/test_catalog.py",
        commands=(
            *unit_basic_inline_commands(),
            cargo_test("--test", "capability_policy_model", nocapture=True),
            cargo_test("--test", "policy_profile_hardening", nocapture=True),
            cargo_test("--test", "extension_flag_passthrough", nocapture=True),
            cargo_test("--test", "model_serialization", nocapture=True),
            cargo_test("--test", "redaction_test", nocapture=True),
            cargo_test("--test", "extension_scoring_ope", nocapture=True),
        ),
    ),
    "unit": TestLane(
        name="unit",
        description="Run the optional local quick profile for inline lib tests plus the classified unit suite.",
        kind="verify",
        origin="local",
        owner=".just/test_catalog.py",
        blocking="optional",
        ssot=".just/test_catalog.py",
        verify_args=("--profile", "quick", "--skip-lint"),
    ),
    "integration": TestLane(
        name="integration",
        description="Run the optional local non-E2E integration profile.",
        kind="verify",
        origin="local",
        owner=".just/test_catalog.py",
        blocking="optional",
        ssot=".just/test_catalog.py",
        verify_args=("--profile", "ci", "--skip-lint", "--skip-e2e"),
    ),
    "all": TestLane(
        name="all",
        description="Run the optional local full verification profile.",
        kind="verify",
        origin="local",
        owner=".just/test_catalog.py",
        blocking="optional",
        ssot=".just/test_catalog.py",
        verify_args=("--profile", "full", "--skip-lint"),
    ),
}

OPTIONAL_LANES = ("unit", "integration", "all")

DISPLAY_ORDER = ("compile", "unit-basic", "baseline", "unit", "integration", "all")


def resolve_lane(target: str) -> TestLane:
    canonical = target or "unit-basic"
    lane = LANES.get(canonical)
    if lane is None:
        expected = ", ".join(DISPLAY_ORDER)
        raise SystemExit(f"unknown test target: {target}; expected one of: {expected}")
    return lane


def display_targets() -> list[tuple[str, str]]:
    return [(name, LANES[name].description) for name in DISPLAY_ORDER]


def lane_command(lane: TestLane) -> str:
    if lane.kind == "script":
        return " ".join(lane.script_args)
    if lane.kind == "verify":
        return "./verify " + " ".join(lane.verify_args)
    if lane.name == "compile":
        return "cargo " + " ".join(lane.commands[0])
    if lane.name == "unit-basic":
        return "multiple cargo test invocations; see .just/test_catalog.py"
    return ""
