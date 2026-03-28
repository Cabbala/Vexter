# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Sub-agent Summaries

## Anscombe
- Reverified PR `#102` / merge commit `49aa6e363bbda7f08ca0b1dc30420a81a4b5e0b3` as latest merged `main`, then checked the repo-level current pointers remain atomically pinned to regeneration while preserving the accepted refresh baseline from PR `#101`.
- Checked the atomic current-pointer set across summary, context, manifest, ledger, bundle metadata, README, and handoff surfaces so regeneration is current, refresh is the blocked next step, and retry-gate remains only the pass successor.
- Rechecked the regeneration-side mapping against the shared canonical manifest, evidence preflight, and compatibility gap outputs so the manifest stays template-only and honest while the preflight remains fail-closed.

## Euler
- Confirmed the regeneration lane stays inside the unchanged Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one-plan, one-position, explicit-allowlist, small-lot, bounded-window, funded-live-forbidden envelope.
- Verified the planner/runtime boundary remains intact: `prepare / start / status / stop / snapshot` stay planner-bound, `manual_latched_stop_all` remains planner-owned, Dexter stays the only real-demo seam, and frozen Mew-X remains unchanged on `sim_live`.
- The strongest protections remain the fail-closed manifest/preflight logic and boundary tests, so the real risk here is provenance or pointer drift during the rerun rather than any runtime or architecture widening.

## Parfit
- The smallest safe change set is the regeneration generator provenance refresh for latest merged `main` and the attached bundle source, the generated current-pointer outputs, and the regression expectations that pin those exact values.
- Regeneration should keep consuming the shared canonical contract, manifest template, compatibility gap, and evidence-preflight outputs from the merged refresh baseline in PR `#101` instead of widening or reintroducing those surfaces.
- Validation should stay bounded: rerun the canonical evidence preflight, rerun regeneration from the refresh baseline, rebuild the proof bundle, cover the shared refresh/regeneration/retry-gate/evidence-preflight expectations, then finish with full pytest.
- Merge readiness depends on the manifest staying `template_only`, the preflight staying fail-closed, the proof bundle matching the regenerated outputs, and the final exported tarball carrying the same current-lane truth.
