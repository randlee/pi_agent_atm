# Phase A Plan Superseded

The prior Phase A planning set merged by PR #5 and commit range
`fbcc8346..a689e86c` is superseded.

Why it was superseded:

- it delayed the first shipped `just` + CI baseline until too late in the
  sequence
- it kept the heavyweight PR workflow surface alive while intermediate sprints
  were landing
- it used an integration-branch rollout that added planning complexity before
  the minimal baseline existed

What remains valid from the prior plan:

- timing evidence gathered from `feature/just-integration`
- safe reuse inventory from `feature/just-integration`
- known failure notes around macOS, workflow paths, and heavyweight CI lanes

Authoritative replacement docs in this branch:

- `docs/plans/phase-A/phase-A-just-ci-recovery.md`
- `docs/plans/phase-A/phase-A-testing-strategy.md`
- `docs/plans/sprint-a-1-establish-minimal-baseline-gate.md`
- `docs/plans/sprint-a-2-add-compile-gate.md`
- `docs/plans/sprint-a-3-add-smoke-baseline.md`
- `docs/plans/sprint-a-4-add-optional-local-lanes.md`
- `docs/plans/sprint-a-5-refresh-ssot-and-timing.md`
- `docs/plans/sprint-a-6-merge-baseline-into-atm-graft.md`

The corrected plan starts from zero, reuses only narrow proven pieces from
`feature/just-integration`, and requires required PR CI to stay under 10
minutes at every implementation sprint.
