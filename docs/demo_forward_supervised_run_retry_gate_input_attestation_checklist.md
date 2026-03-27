# Demo Forward Supervised Run Retry Gate Input Attestation Checklist

This checklist fixes the minimum operator-visible surface that must be explicit before retry execution may honestly be reconsidered.

## Current Pointers

1. Start at `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`.
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md`.
5. Use `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md` as the single attestation decision surface.

## Input Attestation Checklist

1. Accept the prior `supervised_run_retry_gate_blocked` lane as baseline and do not claim retry execution success.
2. Keep one attestation row per required face: credential source, venue ref, account ref, connectivity profile, operator owner, bounded start criteria, allowlist/symbol/lot reconfirmation, `manual_latched_stop_all` visibility, and terminal snapshot readability.
3. Keep the repo-visible markers explicit: `DEXTER_DEMO_CREDENTIAL_SOURCE`, `DEXTER_DEMO_VENUE_REF`, `DEXTER_DEMO_ACCOUNT_REF`, and `DEXTER_DEMO_CONNECTIVITY_PROFILE`.
4. For every row, record who attests the face outside the repo.
5. For every row, record what is being attested without embedding secrets or credential material.
6. For every row, record the minimum evidence shape that would be enough for a gate reviewer to inspect the attestation.
7. For every row, record when the attestation becomes stale.
8. Reconfirm `DEXTER_DEMO_ALLOWED_SYMBOLS`, `DEXTER_DEMO_DEFAULT_SYMBOL`, `DEXTER_DEMO_ORDER_SIZE_LOTS`, `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`, `DEXTER_DEMO_WINDOW_MINUTES=15`, and `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`.
9. Reconfirm venue/connectivity, `manual_latched_stop_all` visibility, and terminal snapshot readability stay explicit for the bounded supervised window.
10. Reconfirm Mew-X remains unchanged on `sim_live`.
11. Reconfirm funded live remains forbidden.

## Input Attestation Exit Criteria

- every attestation row in `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md` is explicit enough to reopen gate review for retry execution
- operator owner is named outside the repo
- venue and connectivity attestations are current for the bounded window
- allowlist, symbol, lot-size, window, and one-position cap are reconfirmed
- `manual_latched_stop_all` visibility and terminal snapshot readability are reconfirmed
- the retry path remains Dexter-only `paper_live`

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
