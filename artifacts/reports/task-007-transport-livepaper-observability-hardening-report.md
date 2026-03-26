# TASK-007 Transport Live-Paper Observability Hardening Report

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#49` main commit `05ce9f2889da68cdb7336b667e6ad3adf8f5884b` on `2026-03-26T12:53:16Z`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Started from the merged runtime observability lane on PR `#49` and kept the promoted comparison baseline frozen.
- Hardened `vexter/planner_router/transport.py` plus the dispatch starting snapshot path so the runtime-oriented path keeps one shared observability payload across prepared handles, polled status, push-promoted status, terminal snapshots, and rejection detail.
- Added explicit ack-history retention so first accepted requests and later duplicate requests remain visible after follow-up transitions instead of collapsing to only the latest ack state.
- Preserved immutable handoff metadata and lifecycle fields on the source-faithful Dexter `paper_live` and Mew-X `sim_live` seam without changing source logic or transport semantics.
- Refreshed the proof, report, status, context pack, ledger, and bundle metadata for the hardening lane.

## Hardening Outcome

- Prepared handles now keep immutable handoff metadata such as `plan_batch_id`, `objective_profile_id`, `monitor_profile_id`, and `quarantine_scope`.
- Status snapshots now keep the same handoff fields together with lifecycle fields such as `prepared_at_utc`, `native_session_id`, `executor_status`, and ack history.
- Push-promoted reconciled snapshots now retain both `poll_detail` and `push_detail`, so quarantine reason does not displace source-faithful runtime context.
- Snapshot-backed terminal detail now retains the same handoff and ack-history fields that appear on runtime status.
- Rejection and timeout detail now preserve source-faithful execution metadata instead of collapsing to minimal error-only payloads.

## Validation

- `pytest -q`
- `90 passed`

## Recommendation Among Next Tasks

### `transport_livepaper_observability_regression_pack`

Recommended next because:

- the bounded hardening work now closes the main completeness gaps, so the highest-value next step is to lock these guarantees into a durable regression pack
- the planner-to-transport boundary remained unchanged, so regression risk is higher than interface ambiguity risk
- a regression lane will protect the new ack-history and metadata continuity guarantees across future transport work

### `livepaper_observability_spec`

Not next because:

- the observability surface is already evidenced across smoke, runtime continuity, and hardening lanes
- another spec-only pass would add less confidence than regression-focused verification

### `executor_boundary_code_spec`

Not next because:

- no new boundary ambiguity surfaced in this task
- the change surface stayed inside runtime observability payload retention rather than contract shape

## Decision

- Outcome: `A`
- Key finding: `executor_transport_livepaper_observability_hardening_passed`
- Claim boundary: `transport_livepaper_observability_hardening_bounded`
- Decision: `transport_livepaper_observability_regression_pack_ready`
- Recommended next step: `transport_livepaper_observability_regression_pack`
