#!/usr/bin/env python3
from __future__ import annotations

import sys

from run_cargo import cargo_command, run_cargo
from test_catalog import resolve_lane


def run_lane(target: str) -> int:
    lane = resolve_lane(target)
    for command_args in lane.commands:
        command = cargo_command(*command_args)
        print(
            f"lane={lane.name}\n"
            f"command={' '.join(command)}\n"
            f"ssot=.just/test_catalog.py"
        )
        completed = run_cargo(
            *command_args,
            scrub_credentials=True,
            check=False,
        )
        if completed.returncode != 0:
            print("next=fix the failing cargo target or narrow the lane intentionally")
            return completed.returncode
    return 0


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else ""
    return run_lane(target)


if __name__ == "__main__":
    raise SystemExit(main())
