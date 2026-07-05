#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys

from run_cargo import cargo_command, run_cargo
from test_catalog import repo_root
from test_catalog import resolve_lane


def print_lane_header(
    lane_name: str,
    command: list[str],
    *,
    documented_targets: tuple[str, ...] = (),
) -> None:
    lines = [
        f"lane={lane_name}",
        f"command={' '.join(command)}",
        "ssot=.just/test_catalog.py",
    ]
    if documented_targets:
        lines.append(f"documented_targets={','.join(documented_targets)}")
    print("\n".join(lines))


def run_cargo_lane(target: str) -> int:
    lane = resolve_lane(target)
    for command_args in lane.commands:
        command = cargo_command(*command_args)
        print_lane_header(lane.name, command)
        completed = run_cargo(
            *command_args,
            scrub_credentials=True,
            check=False,
        )
        if completed.returncode != 0:
            print("next=fix the failing cargo target or narrow the lane intentionally")
            return completed.returncode
    return 0


def run_script_lane(target: str) -> int:
    lane = resolve_lane(target)
    command = list(lane.script_args)
    print_lane_header(
        lane.name,
        command,
        documented_targets=lane.documented_targets,
    )
    completed = subprocess.run(
        command,
        cwd=repo_root(),
        check=False,
    )
    if completed.returncode != 0:
        print("next=inspect scripts/smoke.sh artifacts or narrow the smoke lane intentionally")
    return completed.returncode


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else ""
    lane = resolve_lane(target)
    if lane.kind == "cargo":
        return run_cargo_lane(target)
    if lane.kind == "script":
        return run_script_lane(target)
    raise SystemExit(f"unsupported test lane kind: {lane.kind}")


if __name__ == "__main__":
    raise SystemExit(main())
