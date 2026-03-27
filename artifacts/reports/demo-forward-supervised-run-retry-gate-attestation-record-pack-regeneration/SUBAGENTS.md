# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Sub-agent Summaries

## Anscombe
- Reverified PR `#88` / commit `1d43904d392eefdcc911f00102cdff62bce9deb2` as latest merged `main`, then preserved regeneration as the current lane instead of inventing a new pass claim.
- The main duplication before this change was that regeneration rebuilt blocker semantics from refresh text rather than consuming one canonical external-evidence manifest and validator.
- The atomic current-pointer set still matters: summary, context, manifest, ledger, README, bundle metadata, and handoff surfaces must all agree once regeneration starts consuming the shared gap report.

## Euler
- Confirmed the regeneration lane stays inside the unchanged Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one-plan, one-position, explicit-allowlist, small-lot, bounded-window, funded-live-forbidden envelope.
- Verified the planner/runtime boundary remains intact: `prepare / start / status / stop / snapshot` stay planner-bound, `manual_latched_stop_all` remains planner-owned, Dexter stays the only real-demo seam, and frozen Mew-X remains unchanged on `sim_live`.
- The canonical manifest is non-secret and fail-closed by construction, so regeneration still cannot imply funded-live access or retry execution success without real current evidence.

## Parfit
- The lowest-risk change set is one shared manifest + validator + gap report, plus regeneration/refresh rewiring and the tests that pin current task, bundle layout, and export behavior.
- Generator-first validation remains the safe path: write the canonical gap artifacts, rerun refresh, rerun regeneration, then widen to export and full pytest coverage.
- Merge readiness depends on end-to-end agreement across summary, context, manifest, ledger, bundle metadata, the regenerated handoff bundle, and the final exported tarball without touching runtime code.
