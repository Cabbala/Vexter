# Demo Forward Supervised Run Retry Gate Attestation Refresh Sub-agent Summaries

## Anscombe
- Confirmed that refresh has to be re-promoted atomically after the regeneration merge so status, report, summary, proof, handoff, checklist, decision-surface, manifest, context-pack, and bundle pointers agree again on one current lane.
- Recommended treating regeneration as baseline evidence rather than the current source of truth: refresh stays observational and fail-closed until every regenerated face points to one current, fresh-enough, reviewer-readable locator.
- Flagged stale pointer drift as the main risk, especially when README, task ledger, and bundle metadata still inherit the regeneration lane by default.

## Euler
- Kept the bounded runtime envelope unchanged: Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, explicit allowlist, small lot, one-plan, one-position, bounded supervision, and funded-live forbidden.
- Confirmed the refreshed row schema still belongs to refresh owner, refresh trigger, minimum fresh evidence locator shape, stale condition, and retry-gate usability, but it now has to be derived from the regeneration decision surface rather than the older record-pack surface.
- Found no planner or adapter seam drift: the lane stays docs/proofs/report/script only, with `prepare / start / status / stop / snapshot` and `manual_latched_stop_all` unchanged, while `build_proof_bundle.sh` fallback now needs to follow refresh again.

## Parfit
- Scoped the smallest safe change set to the refresh generator, refresh report/proof surfaces, README/current-pointer rewiring, targeted shared tests, and the bundle fallback path.
- Recommended validating generator output and the focused refresh regressions first, then widening to the shared pytest suite because several older task tests pin the repo-level current task and next-task metadata.
- Merge readiness depends on starting from PR `#82` / merge commit `eebfcd9b03e1e365cc4659996ea2638e6f285bbc`, routing the blocked next step back to record-pack regeneration, and reporting the published branch as `feat/attestation-refresh`.
