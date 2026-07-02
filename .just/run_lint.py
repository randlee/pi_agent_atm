#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


LINT_ORDER = ("fmt", "clippy", "check")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=repo_root(), check=True)


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target == "all":
        for item in LINT_ORDER:
            run(["just", "lint", item])
        return 0

    if target == "fmt":
        run(["just", "_lint-fmt"])
        return 0

    if target == "clippy":
        run(["just", "_lint-clippy"])
        return 0

    if target == "check":
        run(["just", "_lint-check"])
        return 0

    raise SystemExit("unknown lint target: {target}; expected one of: all, fmt, clippy, check".format(target=target))


if __name__ == "__main__":
    raise SystemExit(main())
