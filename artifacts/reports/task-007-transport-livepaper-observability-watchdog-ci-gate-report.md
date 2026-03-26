# TASK-007 Transport Live-Paper Observability Watchdog CI Gate Report

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#57` main commit `8368b545c3ef3c32db9843ac7e958528902fe67c` on `2026-03-26T15:58:51Z`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Open Vexter PR `#50` remained non-authoritative relative to merged `main`.

## What This Task Did

- Started from the merged watchdog-regression-pack lane on PR `#57` and kept the promoted comparison baseline frozen.
- Added a grouped watchdog CI gate that runs the watchdog, watchdog-runtime, and watchdog-regression-pack suites together before the rest of validation.
- Made the gate proof name the exact locked surfaces so drift, omission, or partial visibility breaks are attributable immediately.
- Refreshed workflow ordering, marker registration, bundle targeting, and handoff metadata without changing planner/router source logic or collecting new evidence.

## Watchdog Gate Outcome

- The grouped gate preserves the source-faithful Dexter `paper_live` / frozen Mew-X `sim_live` seam.
- Immutable handoff metadata, handle lifecycle continuity, planned/runtime metadata drift detection, status sink fan-in, ack-history retention, quarantine completeness, manual stop-all propagation, snapshot-backed terminal detail, and normalized failure-detail passthrough remain the mandatory gate faces.
- Gate run result: `38 passed in 1.02s`.

## Recommendation Among Next Tasks

### `livepaper_observability_spec`

- Recommended next because the watchdog surfaces are now continuously enforced in CI and the highest-value follow-up is to codify that observability contract.

### `executor_boundary_code_spec`

- Not next because the transport boundary itself did not become ambiguous while wiring the gate.

### `transport_livepaper_observability_watchdog_watchdog_runtime`

- Not next because the runtime watchdog lane is already merged and this task already makes it fail-fast in CI.

## Decision

- Outcome: `A`
- Key finding: `executor_transport_livepaper_observability_watchdog_ci_gate_passed`
- Claim boundary: `transport_livepaper_observability_watchdog_ci_gate_bounded`
- Decision: `livepaper_observability_spec_ready`
- Recommended next step: `livepaper_observability_spec`
