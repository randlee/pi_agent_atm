#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tomllib


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=repo_root(), check=True)


def run_verify(*args: str) -> None:
    run(["./verify", *args])


def cargo_command(*args: str) -> list[str]:
    command = ["cargo", *args]
    if shutil_which("rch") is not None:
        return ["rch", "exec", "--", *command]
    return command


def load_suite_targets(suite: str) -> list[str]:
    payload = tomllib.loads((repo_root() / "tests/suite_classification.toml").read_text())
    return list(payload["suite"][suite]["files"])


def run_vcr_only() -> None:
    for target in load_suite_targets("vcr"):
        run(cargo_command("test", "--test", target, "--", "--nocapture"))


def shutil_which(binary: str) -> str | None:
    from shutil import which

    return which(binary)


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else "ci"
    if target == "ci":
        run_verify("--profile", "ci", "--skip-lint")
        return 0
    if target == "all":
        run_verify("--profile", "full", "--skip-lint")
        return 0
    if target == "full":
        run_verify("--profile", "full", "--skip-lint")
        return 0
    if target == "unit":
        run_verify("--profile", "quick", "--skip-lint")
        return 0
    if target in {"integration", "integrate"}:
        run_verify("--profile", "ci", "--skip-lint", "--skip-e2e")
        return 0
    if target == "vcr":
        run_vcr_only()
        return 0
    if target == "e2e":
        run_verify("--profile", "full", "--skip-lint", "--skip-unit")
        return 0
    if target == "fuzz":
        run(["./scripts/fuzz_e2e.sh", "--quick"])
        return 0
    if target == "fuzz-full":
        run(["./scripts/fuzz_e2e.sh"])
        return 0

    raise SystemExit(
        "unknown test target: {target}; expected one of: ci, all, full, unit, integration, vcr, e2e, fuzz, fuzz-full".format(
            target=target
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
