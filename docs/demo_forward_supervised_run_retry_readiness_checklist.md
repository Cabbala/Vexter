# Demo Forward Supervised Run Retry Readiness Checklist

This checklist fixes the minimum operator-visible surface that must be explicit before a bounded retry gate can pass.

## Current Pointers

1. Start at `artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json`.
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md`.
5. Use `docs/demo_forward_supervised_run_retry_prerequisite_matrix.md` as the single retry prerequisite matrix.

## Retry Gate Checklist

1. Accept the prior `demo_forward_supervised_run_blocked` lane as baseline and do not claim a real-demo completion.
2. Name the operator owner outside the repo and record who is responsible for the bounded retry window.
3. Resolve `DEXTER_DEMO_CREDENTIAL_SOURCE`, `DEXTER_DEMO_VENUE_REF`, `DEXTER_DEMO_ACCOUNT_REF`, and `DEXTER_DEMO_CONNECTIVITY_PROFILE` outside the repo.
4. Record the bounded supervised-window start criteria outside the repo before retry.
5. Reconfirm `DEXTER_DEMO_ALLOWED_SYMBOLS`, `DEXTER_DEMO_DEFAULT_SYMBOL`, `DEXTER_DEMO_ORDER_SIZE_LOTS`, `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`, `DEXTER_DEMO_WINDOW_MINUTES=15`, and `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`.
6. Reconfirm venue / connectivity readiness for the bounded retry window.
7. Reconfirm `manual_latched_stop_all` visibility and terminal snapshot readability for the retry path.
8. Reconfirm Mew-X remains unchanged on `sim_live`.
9. Reconfirm funded live remains forbidden.

## Retry Gate Exit Criteria

- every prerequisite row in `docs/demo_forward_supervised_run_retry_prerequisite_matrix.md` is explicit
- operator owner is named outside the repo
- venue and connectivity are confirmed for the bounded window
- allowlist, symbol, and lot-size constraints are reconfirmed
- `manual_latched_stop_all` and terminal snapshot visibility are reconfirmed
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
