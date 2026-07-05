#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from lint_catalog import lane_command
from lint_catalog import resolve_lane
from run_cargo import run_cargo


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run(command: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, check=True)


def print_lane_header(target: str, command: str) -> None:
    print(f"lane={target}\ncommand={command}\nssot=.just/lint_catalog.py")


def run_step(step: tuple[str, ...]) -> int:
    kind, *args = step
    if kind == "fmt":
        return subprocess.run(
            [sys.executable, ".just/run_fmt.py", *args],
            cwd=repo_root(),
            check=False,
        ).returncode
    if kind == "lane":
        return run_lane(args[0])
    if kind == "cargo":
        return run_cargo(*args, check=False).returncode
    raise SystemExit(f"unsupported lint step kind: {kind}")


def run_lane(target: str) -> int:
    lane = resolve_lane(target)
    if lane.children:
        for child in lane.children:
            result = run_lane(child)
            if result != 0:
                return result
        return 0
    if lane.steps:
        print_lane_header(lane.name, lane_command(lane))
        for step in lane.steps:
            result = run_step(step)
            if result != 0:
                print("next=fix the failing lint step or narrow the optional lane intentionally")
                return result
        return 0
    if lane.cargo_args:
        print_lane_header(lane.name, lane_command(lane))
        result = run_cargo(*lane.cargo_args, check=False).returncode
        if result != 0:
            print("next=fix the failing local-code warnings or narrow the lane intentionally")
        return result
    raise SystemExit(f"lint lane {target} is missing both children and execution metadata")


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    return run_lane(target)


if __name__ == "__main__":
    raise SystemExit(main())
