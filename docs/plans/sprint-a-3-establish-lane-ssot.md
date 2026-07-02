---
id: A3
title: Establish Lane SSOT
status: planned
branch: sprint-a-3-establish-lane-ssot
worktree: ../pi_agent_atm-worktrees/sprint-a-3-establish-lane-ssot
target: integrate/phase-A
---

# Sprint A3 — Establish Lane SSOT

## Goal

- Create one authoritative source of truth for lint and test lane definitions.

## Hard Dependencies

- Sprint A2 merged into `integrate/phase-A`.

## Exact Targets

- `.just/`
- `tests/suite_classification.toml`
- `feature/just-integration:.just/lint_catalog.py`
- `feature/just-integration:.just/test_catalog.py`
- `feature/just-integration:.just/explain.py`
- `feature/just-integration:.just/show_suites.py`

## Deliverables

Every listed deliverable is expected to land at a production-ready level for
the scope this sprint claims. If that cannot be done cleanly in one sprint, the
sprint must be split before implementation begins. No deliverable may be
silently dropped or partially deferred.

- One authoritative lint/test lane-definition layer exists and drives the
  operator-facing explanation surface.

## Required Work

- Add one authoritative lint lane catalog.
- Add one authoritative test lane catalog.
- Add `just suites`.
- Add `just explain lint [lane]`.
- Add `just explain test [lane]`.
- Ensure diagnostics point to the source-of-truth file instead of generic
  failures.

## Explicit Code Samples

```python
LANES = {
    "baseline": TestLane(...),
    "unit": TestLane(...),
    "integration": TestLane(...),
    "vcr": TestLane(...),
    "e2e": TestLane(...),
    "all": TestLane(...),
}
```

```text
suite membership source of truth:
tests/suite_classification.toml
```

## This Sprint Does Not Close

- It does not add the full smoke baseline.
- It does not change required PR CI.

## Acceptance Criteria

- One authoritative lint lane catalog exists.
- One authoritative test lane catalog exists.
- `just suites` exists.
- `just explain lint [lane]` exists.
- `just explain test [lane]` exists.
- The same lane is not hard-coded through multiple command paths.

## Required Validation

- `just suites`
- `just explain lint`
- `just explain test`
- `python3 -c "import tomllib, pathlib; print(sorted(tomllib.loads(pathlib.Path('tests/suite_classification.toml').read_text())['suite'].keys()))"`
