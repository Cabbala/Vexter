# Demo Forward Supervised Run Operator Follow-Up

This follow-up fixes the minimum post-run surface after the bounded supervised run lane is promoted to current source of truth.

## Current Pointers

1. Start at `artifacts/reports/demo-forward-supervised-run-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-check.json`.
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run/HANDOFF.md`.

## If The Outcome Is `FAIL/BLOCKED`

1. Do not claim a real-demo completion.
2. Resolve `DEXTER_DEMO_CREDENTIAL_SOURCE`, `DEXTER_DEMO_VENUE_REF`, `DEXTER_DEMO_ACCOUNT_REF`, and `DEXTER_DEMO_CONNECTIVITY_PROFILE` outside the repo.
3. Name the operator owner and the bounded supervised-window start time outside the repo.
4. Reconfirm `DEXTER_DEMO_ALLOWED_SYMBOLS`, `DEXTER_DEMO_DEFAULT_SYMBOL`, `DEXTER_DEMO_ORDER_SIZE_LOTS`, and `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`.
5. Reconfirm Mew-X remains unchanged on `sim_live`.
6. Reconfirm funded live remains forbidden.
7. Retry only after venue connectivity and cancel / stop-all visibility can be observed.

## If The Outcome Is `PASS`

1. Preserve the current report, proof, summary, and handoff pointers.
2. Confirm the terminal snapshot stays readable for rollback and audit.
3. Prepare the smallest next cut only after the bounded run is fully closed.

## Never Relax

- `prepare / start / status / stop / snapshot`
- `poll_first`
- `manual_latched_stop_all`
- explicit allowlist
- small lot
- one active real demo plan max
- one open position max
- funded live forbidden
