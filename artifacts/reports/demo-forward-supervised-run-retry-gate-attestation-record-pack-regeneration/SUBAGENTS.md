# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Sub-agent Summaries

## Anscombe
- Confirmed merged PR `#85` / commit `aee3216c3c5091135f6bb50236883e1bdff8e2e1` is the current refresh baseline, so regeneration has to be re-promoted from that newer source of truth rather than the older PR `#83` state.
- Flagged two correctness risks to keep atomic: stale refresh-side repo pointers and repeated regeneration suffixes inside refresh-derived rows that would make the decision surface contradictory or non-reviewable.
- Recommended one atomic current-pointer flip across summary, context, manifest, ledger, README, bundle metadata, and handoff surfaces so regeneration becomes current everywhere together.

## Euler
- Confirmed the regeneration lane stays inside the unchanged Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one-plan, one-position, explicit-allowlist, small-lot, bounded-window, funded-live-forbidden envelope.
- Verified the planner/runtime boundary remains intact: `prepare / start / status / stop / snapshot` stay planner-bound, `manual_latched_stop_all` remains planner-owned, Dexter stays the only real-demo seam, and frozen Mew-X remains unchanged on `sim_live`.
- Recommended keeping regeneration logic purely surface-level by normalizing refresh-derived row text before emission instead of rewriting Dexter or Mew-X runtime/source behavior.

## Parfit
- Scoped the lowest-risk change set to the regeneration generator, the proof-bundle fallback path, the regenerated artifacts, and the shared regression expectations that pin the repo-level current task and bundle layout.
- Recommended validating the regeneration generator and proof-bundle/export path first, then widening to the shared current-pointer and full pytest coverage once the regenerated artifacts are in place.
- Merge readiness depends on end-to-end agreement across summary, context, manifest, ledger, bundle metadata, the regenerated handoff bundle, and the final exported tarball without touching runtime code.
