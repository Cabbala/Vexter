# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Sub-agent Summaries

## Anscombe
- Confirmed merged PR `#87` / commit `857f62c78129fecd71793744864ce12653d62141` is the exact current refresh baseline on `origin/main`, so regeneration has to be re-promoted from that merged source of truth rather than the older PR `#85` branch state.
- Flagged the atomic current-pointer set as summary, context, manifest, ledger, README, bundle metadata, and handoff surfaces, and called out stale refresh metadata plus duplicate historical regeneration clauses in `README.md` as the main contradiction risk.
- Recommended keeping the refresh proof/history intact as baseline while flipping only the repo-level current pointers and regenerated-lane surfaces together.

## Euler
- Confirmed the regeneration lane stays inside the unchanged Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one-plan, one-position, explicit-allowlist, small-lot, bounded-window, funded-live-forbidden envelope.
- Verified the planner/runtime boundary remains intact: `prepare / start / status / stop / snapshot` stay planner-bound, `manual_latched_stop_all` remains planner-owned, Dexter stays the only real-demo seam, and frozen Mew-X remains unchanged on `sim_live`.
- Focused guardrail verification passed without findings, so regeneration stays a surface-only change that must not rewrite Dexter or Mew-X runtime/source behavior.

## Parfit
- Scoped the lowest-risk change set to the regeneration generator, the proof-bundle fallback path, the regenerated artifacts, and the shared regression expectations that pin the repo-level current task and bundle layout.
- Confirmed the minimal safe path is generator-only plus current-pointer tests: do not rewrite the baseline refresh lane, just re-promote regeneration from merged PR `#87` and validate the exporter/proof-bundle flow.
- Merge readiness depends on end-to-end agreement across summary, context, manifest, ledger, bundle metadata, the regenerated handoff bundle, and the final exported tarball without touching runtime code.
