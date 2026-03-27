# Demo Forward Supervised Run Retry Gate Attestation Refresh Sub-agent Summaries

## Anscombe
- Reverified PR `#91` / merge commit `014723587b100fb0046646d40b445537584b44ea` as latest merged `main`, then treated the record-pack-regeneration lane as the current repo-visible baseline rather than reopening older refresh assumptions.
- The shared evidence-preflight path now owns the reopen-readiness mapping, aggregated blocker reasons, and canonical manifest-to-proof references so refresh and regeneration stop re-deriving them separately.
- Current-pointer risk remains atomic: summary, context, manifest, ledger, README, bundle metadata, and handoff surfaces must all reflect the same fail-closed truth once the canonical preflight and compatibility gap outputs are written together.

## Euler
- Confirmed no architecture drift: the planner boundary stays `prepare / start / status / stop / snapshot`, `manual_latched_stop_all` stays planner-owned, Dexter remains `paper_live`, and frozen Mew-X remains `sim_live`.
- Kept the fail-closed split crisp: refresh now consumes the canonical evidence preflight for freshness and usability, while regeneration consumes the same shared preflight plus compatibility gap output for inheritance and reviewability without widening runtime scope.
- The new contract remains non-secret and bounded; it never implies funded-live access, broader venue scope, or Dexter / Mew-X runtime rewrites.

## Parfit
- The smallest safe implementation is one canonical manifest validator plus a unified preflight/readiness output, with the legacy gap surfaces preserved as compatibility mirrors while refresh and regeneration consume the same shared data.
- Validation should start with the evidence-preflight script plus refresh/regeneration tests, then widen to bundle/export coverage and the full pytest suite.
- Merge readiness depends on exact agreement across summary, context, manifest, ledger, README, refresh bundle metadata, and the canonical external-evidence paths from the PR `#91` baseline.
