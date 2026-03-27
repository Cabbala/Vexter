# Demo Forward Supervised Run Retry Gate Attestation Audit Checklist

This checklist fixes the minimum operator-visible audit surface that must be explicit before retry-gate review may honestly reopen.

## Current Pointers

1. Start at `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json`.
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md`.
5. Use `docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md` as the single attestation-audit decision surface.

## Attestation Audit Checklist

1. Accept the prior `supervised_run_retry_gate_input_attestation_blocked` lane as baseline and do not claim retry-gate reopen or retry execution success.
2. Keep one audit row per required face: credential source, venue ref, account ref, connectivity profile, operator owner, bounded start criteria, allowlist/symbol/lot reconfirmation, `manual_latched_stop_all` visibility, and terminal snapshot readability.
3. Keep the repo-visible markers explicit: `DEXTER_DEMO_CREDENTIAL_SOURCE`, `DEXTER_DEMO_VENUE_REF`, `DEXTER_DEMO_ACCOUNT_REF`, and `DEXTER_DEMO_CONNECTIVITY_PROFILE`.
4. For every row, confirm who attests the face is explicit.
5. For every row, confirm what is being attested is explicit without embedding secrets or credential material.
6. For every row, confirm the minimal evidence shape is explicit enough for a gate reviewer to inspect the attestation outside the repo.
7. For every row, confirm when the attestation becomes stale is explicit.
8. For every row, confirm what makes the face auditable enough is explicit.
9. For every row, record whether a current bounded-window attestation reference is present without embedding secret material.
10. For every row, record whether a timestamped stale check can currently be made from repo-visible evidence.
11. Reconfirm `DEXTER_DEMO_ALLOWED_SYMBOLS`, `DEXTER_DEMO_DEFAULT_SYMBOL`, `DEXTER_DEMO_ORDER_SIZE_LOTS`, `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`, `DEXTER_DEMO_WINDOW_MINUTES=15`, and `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`.
12. Reconfirm venue/connectivity, `manual_latched_stop_all` visibility, and terminal snapshot readability remain explicit for the bounded supervised window.
13. Reconfirm Mew-X remains unchanged on `sim_live`.
14. Reconfirm funded live remains forbidden.

## Attestation Audit Exit Criteria

- every audit row in `docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md` is explicit, non-stale, and auditable enough to reopen retry-gate review
- every required face points to a current bounded-window attestation reference outside repo
- venue and connectivity attestations are current for the bounded window
- allowlist, symbol, lot-size, window, and one-position cap are reconfirmed for the bounded window
- `manual_latched_stop_all` visibility and terminal snapshot readability are reconfirmed for the bounded window
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
