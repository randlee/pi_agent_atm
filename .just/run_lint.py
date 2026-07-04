#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys

from lint_catalog import resolve_lane


def run(command: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, check=True)


def run_lane(target: str) -> int:
    lane = resolve_lane(target)
    if lane.children:
        for child in lane.children:
            run(["just", "lint", child])
        return 0
    if lane.recipe is not None:
        print(
            f"lane={lane.name}\n"
            f"command=cargo {' '.join(lane.cargo_args)}\n"
            f"ssot=.just/lint_catalog.py"
        )
        run(["just", lane.recipe])
        return 0
    raise SystemExit(f"lint lane {target} is missing both children and recipe")


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    return run_lane(target)


if __name__ == "__main__":
    raise SystemExit(main())
