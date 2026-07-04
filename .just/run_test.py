#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from test_catalog import resolve_lane


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def cargo_command(*args: str) -> list[str]:
    command = ["cargo", *args]
    if shutil_which("rch") is not None:
        return ["rch", "exec", "--", *command]
    return command


def run_lane(target: str) -> int:
    lane = resolve_lane(target)
    for command_args in lane.commands:
        command = cargo_command(*command_args)
        print(
            f"lane={lane.name}\n"
            f"command={' '.join(command)}\n"
            f"ssot=.just/test_catalog.py"
        )
        completed = subprocess.run(command, cwd=repo_root(), check=False)
        if completed.returncode != 0:
            print("next=fix the failing cargo target or narrow the lane intentionally")
            return completed.returncode
    return 0


def shutil_which(binary: str) -> str | None:
    from shutil import which

    return which(binary)


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else ""
    return run_lane(target)


if __name__ == "__main__":
    raise SystemExit(main())
