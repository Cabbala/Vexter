# Demo Forward Supervised Run Retry Gate Attestation Refresh Sub-agent Summaries

## Anscombe
- Reverified PR `#95` / merge commit `6f9c6053ef6e9509fa65b57866c956363fde50f3` as latest merged `main`, then traced the atomic current-pointer set across summary, context, manifest, ledger, README, bundle metadata, and handoff surfaces that must flip from regeneration back to refresh.
- Confirmed the refresh-side gap, preflight, and handoff mappings still resolve to the shared canonical manifest template, canonical evidence preflight, and compatibility gap outputs without changing their template-only or blocked outcomes.
- Merge safety depends on every current pointer agreeing that refresh is current, regeneration is the blocked next step, and retry-gate remains only the pass successor.

## Euler
- Confirmed the unchanged guardrail envelope: Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one active plan, one open position, explicit allowlist, small lot, bounded supervised window, outside-repo credential refs, and funded-live forbidden.
- Verified the planner/runtime boundary remains `prepare / start / status / stop / snapshot`, `manual_latched_stop_all` stays planner-owned, Dexter remains the real-demo seam, and frozen Mew-X stays unchanged on `sim_live`.
- The fail-closed control point remains the canonical template-only manifest plus blocked evidence preflight; no runtime, routing, or ownership boundary widens in this promotion.

## Parfit
- The smallest safe change set is the refresh generator provenance and honesty update, the regenerated refresh-side current-pointer artifacts, and the regression expectations that pin repo-wide current-task truth.
- Refresh should keep consuming the shared canonical contract, template, compatibility gap, and evidence-preflight outputs from the regeneration baseline instead of reintroducing or widening those surfaces.
- Merge readiness depends on rerunning the refresh path, rebuilding the proof bundle, validating pointer-sensitive handoff checks, and finishing with full pytest.
