# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Sub-agent Summaries

## Anscombe
- Confirmed the regeneration lane needs to be re-promoted from the refresh-merged `main` state, not from the older PR `#81` baseline.
- Flagged duplicated regeneration clauses inside refresh-derived rows as the main correctness risk because they make the decision surface non-reviewable even while the task claims to be bounded.
- Recommended one atomic current-pointer flip so manifest, context, summary, ledger, and bundle metadata all point to the regeneration lane together.

## Euler
- Kept the regeneration boundary inside the same Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one-plan, one-position, explicit-allowlist, small-lot, bounded-window, funded-live-forbidden envelope.
- Confirmed the planner versus adapter split still holds: runtime seams stay inherited, `manual_latched_stop_all` remains planner-owned, Dexter stays the default sleeve, and frozen Mew-X stays unchanged on `sim_live`.
- Recommended normalizing refresh-derived row fields before building regeneration outputs so trigger, locator-shape, stale-rule, and reviewability text stay single-pass and auditable.

## Parfit
- Scoped the lowest-risk update to re-promoting regeneration from current `origin/main`, refreshing the generator baselines, and rewiring the shared current-pointer regressions without touching runtime code.
- Recommended validating regeneration-specific surfaces first, then widening to the shared manifest and layout coverage because several older tests pin the repo-level current task and bundle path.
- Merge readiness depends on end-to-end pointer agreement across summary, context, proof manifest, ledger, bundle metadata, the regenerated handoff bundle, and the final exported tarball.
