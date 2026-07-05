---
name: sprint-report
description: Generate a sprint status report for pi_agent_atm sprint work. Default is --table.
---

# Sprint Report Skill

Build fenced JSON and pipe it to the Jinja2 template. `mode` controls table vs detailed.

## Scope

Use this skill to summarize active sprint PRs for this repo's current planning structure.
The current repo convention uses sprint docs under `docs/plans/phase-A/` and active
branches such as `integrate/phase-A` and `feature/atm-graft-integration`.

## Usage

```bash
/sprint-report [--table | --detailed]
```

Default: `--table`

---

## Data Source

**Always use `atm gh pr list` first**. One call should return the open PRs plus
their CI and merge state.

```bash
atm gh pr list
```

This is the preferred first pass for populating `sprint_rows` and
`integration_row`. Only drill into individual `gh run view` calls if you need
failure details for a specific job.

**Dogfooding rule**: if `atm gh pr list` does not return enough information to
fill the report cleanly, file a GitHub issue describing the missing field or
format gap before relying on extra `gh` CLI calls as a silent workaround.

## Render Command

The template path is relative, so run the render from the main repo root rather
than from a worktree.

```bash
cd "${CLAUDE_PROJECT_DIR:-$(git worktree list | head -1 | awk '{print $1}')}"
echo '<json>' > /tmp/sprint-report.json
sc-compose render .claude/skills/sprint-report/report.md.j2 --var-file /tmp/sprint-report.json
```

## --table (default)

```json
{
  "mode": "table",
  "sprint_rows": "| A6 | ✅ | ✅ | 🚩 | #16 |\n| A7 | ✅ | 🌀 | 🌀 | #17 |",
  "integration_row": "| **feature/atm-graft-integration** | | — | 🌀 | — |"
}
```

## --detailed

```json
{
  "mode": "detailed",
  "sprint_rows": "Sprint: A6  Refresh SSOT and timing\nPR: #16\nQA: PASS ✓\nCI: Baseline over budget, criteria revised\n────────────────────────────────────────\nSprint: A7  Merge baseline into atm-graft\nPR: #17\nQA: IN-FLIGHT\nCI: Running (1 pending)",
  "integration_row": "Integration: feature/atm-graft-integration\nCI: Running — awaiting final sprint merge readiness"
}
```

## Icon Reference

| State | DEV | QA | CI |
|-------|-----|----|----|
| Assigned | 📥 | 📥 | |
| In progress | 🌀 | 🌀 | 🌀 |
| Done/Pass | ✅ | ✅ | ✅ |
| Findings | 🚩 | 🚩 | |
| Fixing | 🔨 | | |
| Blocked | | | 🚧 |
| Fail | | | ❌ |
| Merged | | | 🏁 |
| Ready to merge | | | 🚀 |
