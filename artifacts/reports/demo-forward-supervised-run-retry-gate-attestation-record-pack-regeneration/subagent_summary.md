# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Sub-agent Summaries

## Anscombe
- Reverified PR `#90` / commit `f79997cc0b619c2542cd6e9f876abcfb7ffca3f8` as latest merged `main`, then re-promoted regeneration from the current refresh baseline instead of inventing a new pass claim.
- The main duplication before this change was that regeneration handoff text still relied on human interpretation instead of carrying per-face manifest fields, proof paths, and template-only blocker guidance from the canonical external-evidence gap output.
- The atomic current-pointer set still matters: summary, context, manifest, ledger, README, bundle metadata, and handoff surfaces must all agree once regeneration becomes the current lane from the refresh baseline.

## Euler
- Confirmed the regeneration lane stays inside the unchanged Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one-plan, one-position, explicit-allowlist, small-lot, bounded-window, funded-live-forbidden envelope.
- Verified the planner/runtime boundary remains intact: `prepare / start / status / stop / snapshot` stay planner-bound, `manual_latched_stop_all` remains planner-owned, Dexter stays the only real-demo seam, and frozen Mew-X remains unchanged on `sim_live`.
- The canonical manifest is non-secret and fail-closed by construction, so regeneration still cannot imply funded-live access or retry execution success without real current evidence.

## Parfit
- The lowest-risk change set is one regeneration-side metadata refresh, one tighter operator handoff that reuses the canonical gap output directly, one small closeout-bundle expansion, and the tests that pin the repo-level current pointer.
- Generator-first validation remains the safe path: rerun the canonical gap script, rerun regeneration from the refresh baseline, rebuild the proof bundle, then widen to targeted coverage and full pytest.
- Merge readiness depends on end-to-end agreement across summary, context, manifest, ledger, bundle metadata, the regenerated handoff bundle, and the final exported tarball without touching runtime code.
