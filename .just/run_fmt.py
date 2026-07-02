#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode in {"check", "verify"}:
        command = ["just", "_fmt-check"]
    elif mode in {"write", "apply"}:
        command = ["just", "_fmt-write"]
    else:
        raise SystemExit(f"unknown fmt mode: {mode}")

    subprocess.run(command, cwd=repo_root(), check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
