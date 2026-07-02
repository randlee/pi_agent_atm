#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import tomllib


def main() -> int:
    payload = tomllib.loads((Path(__file__).resolve().parents[1] / "tests/suite_classification.toml").read_text())
    for suite in ("unit", "vcr", "e2e"):
        files = payload["suite"][suite]["files"]
        print(f"{suite}: {len(files)} target(s)")
        for name in files:
            print(f"  - {name}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
