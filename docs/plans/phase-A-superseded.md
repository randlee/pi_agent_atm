# Phase A Plan Superseded

The prior Phase A planning set merged by PR #5 and commit range
`fbcc8346..a689e86c` is invalid and superseded.

Superseded material:

- `docs/plans/phase-A/phase-A-just-ci-recovery.md`
- `docs/plans/phase-A/phase-A-testing-strategy.md`
- `docs/plans/sprint-a-1-stage-revert-pr.md`
- `docs/plans/sprint-a-2-install-minimal-sc-just-skeleton.md`
- `docs/plans/sprint-a-3-establish-lane-ssot.md`
- `docs/plans/sprint-a-4-add-fast-test-baseline.md`
- `docs/plans/sprint-a-5-reduce-required-pr-ci-to-baseline.md`
- `docs/plans/sprint-a-6-classify-long-running-workflows.md`
- `docs/plans/sprint-a-7-merge-baseline-into-atm-graft.md`

Why this was superseded:

- it proposed a seven-sprint rollout with an `integrate/phase-A` branch and six
  sprint worktrees before any shipped code landed
- it consumed dozens of development cycles without producing a minimal shipped
  `just` + CI baseline
- CI kept re-triggering full `ci`, `fuzz`, `bench`, and `semver` workflows on
  routine branch and push activity while the plan remained unexecuted

This corrective change retracts the prior multi-sprint Phase A plan only. It
does not introduce a replacement plan in this PR.
