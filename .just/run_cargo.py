#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> int:
    args = sys.argv[1:]
    if not args:
        raise SystemExit("usage: run_cargo.py <cargo-args...>")

    command = ["cargo", *args]
    if shutil_which("rch") is not None:
        command = ["rch", "exec", "--", *command]

    subprocess.run(command, cwd=repo_root(), check=True)
    return 0


def shutil_which(binary: str) -> str | None:
    from shutil import which

    return which(binary)


if __name__ == "__main__":
    raise SystemExit(main())
