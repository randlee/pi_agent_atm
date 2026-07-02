#!/usr/bin/env python3
"""Enforce the repository no-mock identifier allowlist."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST = ROOT / ".no-mock-allowlist"
TESTS_DIR = ROOT / "tests"
EXCLUDED_PREFIX = Path("tests/ext_conformance/artifacts")
IDENT_RE = re.compile(r"\b(Mock|Fake|Stub)[A-Za-z0-9_]+\b")


def load_allowlist() -> tuple[set[str], set[tuple[str, str]]]:
    if not ALLOWLIST.is_file():
        print(
            f"::error::missing {ALLOWLIST.name} (required by no-mock policy gate)",
            file=sys.stderr,
        )
        raise SystemExit(1)

    global_allow: set[str] = set()
    file_allow: set[tuple[str, str]] = set()
    for raw_line in ALLOWLIST.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        scope, sep, ident = line.partition(":")
        if not sep or not ident:
            continue
        if scope == "*":
            global_allow.add(ident)
        else:
            file_allow.add((scope, ident))
    return global_allow, file_allow


def iter_violations(
    global_allow: set[str], file_allow: set[tuple[str, str]]
) -> list[str]:
    violations: list[str] = []
    for path in sorted(TESTS_DIR.rglob("*")):
        if not path.is_file():
            continue
        rel_path = path.relative_to(ROOT)
        if rel_path.is_relative_to(EXCLUDED_PREFIX):
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for match in IDENT_RE.finditer(line):
                ident = match.group(0)
                rel_str = rel_path.as_posix()
                if ident in global_allow or (rel_str, ident) in file_allow:
                    continue
                column = match.start() + 1
                violations.append(f"{rel_str}:{line_no}:{column}:{ident}")
    return violations


def main() -> int:
    global_allow, file_allow = load_allowlist()
    violations = iter_violations(global_allow, file_allow)
    if not violations:
        return 0

    print("\n".join(violations))
    print()
    print("NEW no-mock policy violations detected.")
    print("Mock*/Fake*/Stub* identifiers are forbidden in tests.")
    print("Use VCR fixtures or real deps instead. See docs/TEST_COVERAGE_MATRIX.md.")
    print("If the identifier is unavoidable, add it to .no-mock-allowlist with")
    print("rationale and a follow-up issue link.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
