# TASK-007 Transport Live-Paper Observability Watchdog Regression-Pack Report

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#56` main commit `cc8996e0204b7dd149ebce85f1988d7a3abf90cd` on `2026-03-26T15:26:06Z`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Started from the merged watchdog-runtime lane on PR `#56` and kept the promoted comparison baseline frozen.
- Added a dedicated watchdog-regression-pack lane so future transport changes must preserve the watchdog/runtime observability surface instead of relying on one bounded runtime follow-up proof.
- Locked immutable handoff metadata continuity, handle lifecycle continuity, planned/runtime metadata drift detection, status sink fan-in, ack-history retention, quarantine reason completeness, reverse-order `manual_latched_stop_all` propagation, snapshot-backed terminal detail, and normalized failure-detail passthrough into durable transport assertions.
- Preserved the source-faithful Dexter `paper_live` and Mew-X `sim_live` seam without changing source logic, trust logic, thresholds, validator rules, or frozen source pins.

## Validation

- `pytest -q -m transport_livepaper_observability_watchdog_regression_pack tests/test_planner_router_transport_livepaper_observability_regression_pack.py`
- `9 passed, 2 deselected in 0.66s`

## Recommendation Among Next Tasks

### `transport_livepaper_observability_watchdog_ci_gate`

Recommended next because:

- this task packages the watchdog and watchdog-runtime conclusions into a durable regression surface, so the next highest-value step is enforcing that lane on every transport change
- the remaining risk is execution consistency, not missing watchdog categories
- a watchdog-specific CI gate operationalizes the bounded guarantees without reopening comparison or boundary design

### `livepaper_observability_spec`

Not next because:

- the observability surface is already evidenced across smoke, runtime continuity, CI gate, watchdog, watchdog runtime, and now watchdog regression coverage
- another spec-only pass would add less risk reduction than making the watchdog regression pack always-on

### `executor_boundary_code_spec`

Not next because:

- no new planner-to-transport boundary ambiguity surfaced in this task
- the risk surface remains drift inside an already-bounded interface rather than contract shape uncertainty

## Decision

- Outcome: `A`
- Key finding: `executor_transport_livepaper_observability_watchdog_regression_pack_passed`
- Claim boundary: `transport_livepaper_observability_watchdog_regression_pack_bounded`
- Decision: `transport_livepaper_observability_watchdog_ci_gate_ready`
- Recommended next step: `transport_livepaper_observability_watchdog_ci_gate`
