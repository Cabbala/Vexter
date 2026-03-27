# Demo Forward Supervised Run Retry Gate Checklist

This checklist fixes the minimum operator-visible surface that must be explicit before retry execution may begin.

## Current Pointers

1. Start at `artifacts/reports/demo-forward-supervised-run-retry-gate-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-gate-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`.
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md`.
5. Use `docs/demo_forward_supervised_run_retry_gate_decision_surface.md` as the single retry-gate decision surface.

## Retry Gate Checklist

1. Accept the prior `supervised_run_retry_readiness_blocked` lane as baseline and do not claim retry execution success.
2. Name the operator owner outside the repo and record who owns the bounded retry window.
3. Explicitly resolve `DEXTER_DEMO_CREDENTIAL_SOURCE`, `DEXTER_DEMO_VENUE_REF`, `DEXTER_DEMO_ACCOUNT_REF`, and `DEXTER_DEMO_CONNECTIVITY_PROFILE` outside the repo.
4. Explicitly record the bounded start time, go/no-go owner, abort owner, and stop conditions outside the repo before entry.
5. Reconfirm `DEXTER_DEMO_ALLOWED_SYMBOLS`, `DEXTER_DEMO_DEFAULT_SYMBOL`, `DEXTER_DEMO_ORDER_SIZE_LOTS`, `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`, `DEXTER_DEMO_WINDOW_MINUTES=15`, and `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`.
6. Reconfirm venue and connectivity readiness for the bounded retry window.
7. Reconfirm `manual_latched_stop_all` visibility on the retry path.
8. Reconfirm terminal snapshot readability on the retry path.
9. Reconfirm Mew-X remains unchanged on `sim_live`.
10. Reconfirm funded live remains forbidden.

## Retry Gate Exit Criteria

- every gate-input row in `docs/demo_forward_supervised_run_retry_gate_decision_surface.md` is explicit enough to allow retry execution
- operator owner is named outside the repo
- venue and connectivity are confirmed for the bounded window
- allowlist, symbol, lot-size, window, and one-position cap are reconfirmed
- `manual_latched_stop_all` visibility and terminal snapshot readability are reconfirmed
- retry remains Dexter-only `paper_live`

## Never Relax

- `prepare / start / status / stop / snapshot`
- `poll_first`
- `manual_latched_stop_all`
- explicit allowlist
- small lot
- one active real demo plan max
- one open position max
- Mew-X unchanged
- funded live forbidden
