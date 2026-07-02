#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from lint_catalog import resolve_lane


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=repo_root(), check=True)


def run_lane(target: str) -> None:
    lane = resolve_lane(target)
    if lane.children:
        for child in lane.children:
            run(["just", "lint", child])
        return
    if lane.recipe is not None:
        run(["just", lane.recipe])
        return
    raise SystemExit(f"lint lane {target} is missing both children and recipe")


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    run_lane(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
