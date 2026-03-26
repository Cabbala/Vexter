# TASK-007 Transport Live-Paper Observability Watchdog Report

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#53` main commit `64cd0e22c284c759a64939348a59c3152afc77dc` on `2026-03-26T14:14:55Z`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Open Vexter PR `#50` remained non-authoritative relative to merged `main`.

## What This Task Did

- Started from the merged CI-gate lane on PR `#53` and kept the promoted comparison baseline frozen.
- Added a bounded, read-only live-paper observability watchdog evaluator on top of the existing executor transport surface instead of changing transport execution semantics.
- Made the watchdog explicitly detect required field omission, handle lifecycle continuity drift, planned-versus-runtime metadata drift, partial status-sink fan-in, ack-history retention collapse, quarantine-reason omission, manual stop-all visibility loss, terminal snapshot gaps, and normalized failure-detail passthrough loss.
- Added a dedicated watchdog suite plus workflow proof surfacing so CI can fail early when observability becomes partial or drifts while the source-faithful Dexter `paper_live` / Mew-X `sim_live` seam stays fixed.
- Refreshed the summary, context pack, manifest, ledger, proof bundle target, and handoff bundle metadata without collecting new evidence or reopening comparison work.

## Watchdog Outcome

- The watchdog stays bounded to transport-visible metadata and runtime-like artifacts that already exist in Vexter.
- CI-gated regression locks remain the formal baseline; the watchdog adds early warning for drift, omission, and partial visibility on top of those locked guarantees.
- The proof output is emitted at `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-check.json` and `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-summary.md`.
- Bootstrap validation now guards the new watchdog runner, marker registration, proof paths, and bundle contents so the watchdog cannot disappear silently from standard validation flows.

## Recommendation Among Next Tasks

### `transport_livepaper_observability_watchdog_runtime`

Recommended next because:

- the watchdog surface now exists as a bounded evaluator, so the next leverage point is proving runtime-oriented handoff and attachment rather than inventing more checks
- a runtime lane extends operational visibility without reopening comparison, source pins, or planner-to-transport contracts

### `livepaper_observability_spec`

Not next because:

- the watchdog target set is already explicit in source, tests, workflow wiring, and proof artifacts
- another spec-only pass would reduce less risk than exercising the watchdog through a runtime-oriented lane

### `executor_boundary_code_spec`

Not next because:

- no new planner-to-transport boundary ambiguity surfaced while adding the watchdog
- the remaining risk is runtime attachment and continued visibility, not contract uncertainty

## Decision

- Outcome: `A`
- Key finding: `executor_transport_livepaper_observability_watchdog_passed`
- Claim boundary: `transport_livepaper_observability_watchdog_bounded`
- Decision: `transport_livepaper_observability_watchdog_runtime_ready`
- Recommended next step: `transport_livepaper_observability_watchdog_runtime`
