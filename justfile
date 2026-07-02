set shell := ["bash", "-euo", "pipefail", "-c"]

# Show the available task surface.
default:
    @just --list

# Run the canonical verification runner. Includes lint unless skipped explicitly.
verify profile="full":
    ./verify --profile {{profile}}

# Run every classified test suite on the repo without lint gates.
test:
    ./verify --profile full --skip-lint

# Run inline lib tests plus the classified unit suite only.
unit:
    ./verify --profile quick --skip-lint

# Run all non-E2E integration targets from tests/.
integrate:
    ./verify --profile full --skip-lint --skip-e2e

# Run only VCR / fixture replay targets from tests/suite_classification.toml.
vcr:
    #!/usr/bin/env bash
    set -euo pipefail
    if command -v rch >/dev/null 2>&1; then
      runner=(rch exec -- cargo)
    else
      runner=(cargo)
    fi
    mapfile -t targets < <(python3 - <<'PY'
    import tomllib
    from pathlib import Path

    data = tomllib.loads(Path("tests/suite_classification.toml").read_text())
    for name in data["suite"]["vcr"]["files"]:
        print(name)
    PY
    )
    for target in "${targets[@]}"; do
      "${runner[@]}" test --test "$target" -- --nocapture
    done

# Run only the classified E2E targets.
e2e:
    ./verify --profile full --skip-lint --skip-unit

# Run the quick unified fuzz pipeline (P1 + short P2 smoke).
fuzz:
    ./scripts/fuzz_e2e.sh --quick

# Run the full unified fuzz pipeline.
fuzz-full:
    ./scripts/fuzz_e2e.sh

# Run all Criterion benches.
bench:
    #!/usr/bin/env bash
    set -euo pipefail
    if command -v rch >/dev/null 2>&1; then
      exec rch exec -- cargo bench --benches
    fi
    exec cargo bench --benches

# Print the current suite taxonomy from tests/suite_classification.toml.
suites:
    #!/usr/bin/env bash
    set -euo pipefail
    python3 - <<'PY'
    import tomllib
    from pathlib import Path

    data = tomllib.loads(Path("tests/suite_classification.toml").read_text())
    for suite in ("unit", "vcr", "e2e"):
        files = data["suite"][suite]["files"]
        print(f"{suite}: {len(files)} target(s)")
        for name in files:
            print(f"  - {name}")
        print()
    PY
