#!/usr/bin/env python3
from __future__ import annotations

from test_catalog import load_suite_targets
from test_catalog import SUITE_ORDER


def main() -> int:
    for suite in SUITE_ORDER:
        files = load_suite_targets(suite)
        print(f"{suite}: {len(files)} target(s)")
        for name in files:
            print(f"  - {name}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
