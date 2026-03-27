# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT

## 1. Intent
- Accept the blocked input-attestation lane as baseline.
- Promote retry-gate attestation audit to the repo-visible current source of truth.

## 2. Boundary
- Dexter `paper_live` only
- frozen Mew-X `sim_live` only
- `single_sleeve`
- `dexter_default`
- one active real demo plan max
- one open position max
- allowlist only
- small lot only
- bounded supervised window only
- external refs remain outside repo

## 3. Required Current Surfaces
- status
- report
- summary
- proof
- handoff
- checklist
- decision surface
- sub-agent summary

## 4. Honest Audit Model
- `PASS` only if every attestation face is explicit, non-stale, and auditable enough to reopen `supervised_run_retry_gate`.
- `FAIL/BLOCKED` if any attestation face remains incomplete, stale, ambiguous, or not auditable enough.

## 5. Next-Step Boundary
- blocked current lane: `supervised_run_retry_gate_attestation_audit`
- audit-pass successor: `supervised_run_retry_gate`
