#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys

from test_catalog import load_suite_targets
from test_catalog import repo_root
from test_catalog import resolve_lane


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=repo_root(), check=True)


def run_verify(*args: str) -> None:
    run(["./verify", *args])


def cargo_command(*args: str) -> list[str]:
    command = ["cargo", *args]
    if shutil_which("rch") is not None:
        return ["rch", "exec", "--", *command]
    return command


def run_suite_targets(suite: str) -> None:
    for target in load_suite_targets(suite):
        run(cargo_command("test", "--test", target, "--", "--nocapture"))


def shutil_which(binary: str) -> str | None:
    from shutil import which

    return which(binary)


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else "ci"
    lane = resolve_lane(target)
    if lane.kind == "verify":
        run_verify(*lane.verify_args)
        return 0
    if lane.kind == "suite":
        assert lane.suite_name is not None
        run_suite_targets(lane.suite_name)
        return 0
    if lane.kind == "script":
        run(list(lane.script_args))
        return 0
    raise SystemExit(f"unsupported test lane kind: {lane.kind}")


if __name__ == "__main__":
    raise SystemExit(main())
