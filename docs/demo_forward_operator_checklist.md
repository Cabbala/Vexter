# Demo Forward Operator Checklist

This checklist fixes the minimum operator-visible steps required before the first supervised Dexter-only forward demo run can begin.

## Pre-Run Checks

1. Confirm current source of truth starts at `artifacts/reports/demo-forward-acceptance-pack-status.md`.
2. Confirm the verified Vexter base is PR `#71` merge commit `5c1feb2561da7b16a17c5d03b71ff2bf895e20e4`.
3. Confirm Dexter remains pinned at `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
4. Confirm frozen Mew-X remains pinned at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
5. Confirm the route is `single_sleeve`.
6. Confirm the selected sleeve is `dexter_default`.
7. Confirm `DEXTER_DEMO_ALLOWED_SYMBOLS` is explicitly set and reviewed.
8. Confirm `DEXTER_DEMO_DEFAULT_SYMBOL` is on that allowlist.
9. Confirm `DEXTER_DEMO_ORDER_SIZE_LOTS` remains small lot and does not exceed `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`.
10. Confirm `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`.
11. Confirm `DEXTER_DEMO_WINDOW_MINUTES` defines a bounded supervised window.
12. Confirm `DEXTER_DEMO_CREDENTIAL_SOURCE`, `DEXTER_DEMO_VENUE_REF`, `DEXTER_DEMO_ACCOUNT_REF`, and `DEXTER_DEMO_CONNECTIVITY_PROFILE` resolve outside the repo.
13. Confirm Mew-X overlay remains disabled and unchanged on `sim_live`.
14. Confirm funded live paths remain forbidden.

## Prepare And Start Checks

1. `prepare` must pass without pin mismatch, mode mismatch, or route drift.
2. `start` must create one bounded Dexter demo handle only.
3. Entry visibility must show `demo_runtime`, `symbol_allowlist`, `demo_symbol`, and `small_lot_order_size`.
4. The first order path must remain Dexter-native and source-faithful.

## In-Window Checks

1. `status` must preserve `poll_first`.
2. Entry visibility must show `native_order_status`.
3. Fill reconciliation must surface `fill_count`, `orders`, `fills`, and `open_position_lots`.
4. No duplicate or ambiguous handle may appear.
5. No unexpected funded live path may appear.
6. Quarantine or `manual_latched_stop_all` must remain immediately actionable.

## Stop And Snapshot Checks

1. `stop` must preserve the planner stop reason.
2. `stop_all_state` must become visible and confirm cancel or flatten intent.
3. `snapshot` must retain terminal detail for rollback and handoff readability.
4. Normalized failure detail must remain visible if the run aborts.
5. The operator must update handoff continuity using the current status, report, proof, and handoff surfaces.

## Fail Closed

Do not open the supervised window if any of the following are true:

- allowlist is missing or ambiguous
- lot sizing exceeds the bounded cap
- planner boundary differs from `prepare / start / status / stop / snapshot`
- Mew-X is routed into a real-demo path
- funded live routing is visible
- terminal snapshot visibility cannot be confirmed
