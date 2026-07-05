#!/usr/bin/env python3
from __future__ import annotations

from typing import Any
import os
from pathlib import Path
import subprocess
import sys


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


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


def cargo_command(*args: str) -> list[str]:
    command = ["cargo", *args]
    if shutil_which("rch") is not None:
        return ["rch", "exec", "--", *command]
    return command


def cargo_env(*, scrub_credentials: bool = False) -> dict[str, str]:
    env = os.environ.copy()
    if not scrub_credentials:
        return env

    for key in list(env):
        if key in SCRUB_ENV_NAMES or key.startswith(SCRUB_ENV_PREFIXES):
            env.pop(key, None)
    return env


def run_cargo(
    *args: str,
    scrub_credentials: bool = False,
    check: bool = True,
    **kwargs: Any,
) -> subprocess.CompletedProcess[Any]:
    command = cargo_command(*args)
    env = cargo_env(scrub_credentials=scrub_credentials)
    return subprocess.run(command, cwd=repo_root(), check=check, env=env, **kwargs)


def main() -> int:
    args = sys.argv[1:]
    if not args:
        raise SystemExit("usage: run_cargo.py <cargo-args...>")

    run_cargo(*args, check=True)
    return 0


def shutil_which(binary: str) -> str | None:
    from shutil import which

    return which(binary)


if __name__ == "__main__":
    raise SystemExit(main())
