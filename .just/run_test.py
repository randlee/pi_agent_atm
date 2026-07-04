#!/usr/bin/env python3
from __future__ import annotations

import os
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


SCRUB_ENV_NAMES = {
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_OAUTH_TOKEN",
    "OPENAI_API_KEY",
    "OPENAI_ACCESS_TOKEN",
    "OPENROUTER_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "GROQ_API_KEY",
    "CEREBRAS_API_KEY",
    "MISTRAL_API_KEY",
    "MOONSHOT_API_KEY",
    "DASHSCOPE_API_KEY",
    "QWEN_API_KEY",
    "DEEPSEEK_API_KEY",
    "FIREWORKS_API_KEY",
    "TOGETHER_API_KEY",
    "TOGETHER_AI_API_KEY",
    "PERPLEXITY_API_KEY",
    "XAI_API_KEY",
    "GITHUB_TOKEN",
    "GITHUB_COPILOT_API_KEY",
    "COPILOT_GITHUB_TOKEN",
    "GITLAB_TOKEN",
    "GITLAB_API_KEY",
}

SCRUB_ENV_PREFIXES = (
    "ANTHROPIC_",
    "OPENAI_",
    "OPENROUTER_",
    "AZURE_OPENAI_",
    "GOOGLE_",
    "GEMINI_",
    "GROQ_",
    "CEREBRAS_",
    "MISTRAL_",
    "MOONSHOT_",
    "GITHUB_",
    "COPILOT_",
    "GITLAB_",
    "KIMI_",
    "DASHSCOPE_",
    "QWEN_",
    "DEEPSEEK_",
    "FIREWORKS_",
    "TOGETHER_",
    "PERPLEXITY_",
    "XAI_",
    "PI_OPENROUTER_",
    "BEDROCK_",
    "AWS_",
    "SAP_",
)


def lane_env() -> dict[str, str]:
    # Keep unit-basic deterministic even when the operator shell exports live
    # provider credentials or auth metadata.
    env = os.environ.copy()
    for key in list(env):
        if key in SCRUB_ENV_NAMES or key.startswith(SCRUB_ENV_PREFIXES):
            env.pop(key, None)
    return env


def run_lane(target: str) -> int:
    lane = resolve_lane(target)
    env = lane_env()
    for command_args in lane.commands:
        command = cargo_command(*command_args)
        print(
            f"lane={lane.name}\n"
            f"command={' '.join(command)}\n"
            f"ssot=.just/test_catalog.py"
        )
        completed = subprocess.run(command, cwd=repo_root(), check=False, env=env)
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
