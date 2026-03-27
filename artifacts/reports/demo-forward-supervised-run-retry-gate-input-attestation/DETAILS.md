# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION

## 1. Intent
- Accept the blocked retry-gate lane as baseline.
- Promote retry-gate input attestation to the repo-visible current source of truth.

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

## 4. Honest Attestation Model
- `PASS` only if every attestation face is explicit enough to reopen gate review for `supervised_run_retry_execution`.
- `FAIL/BLOCKED` if any attestation face remains unresolved, stale, or unobserved enough.

## 5. Next-Step Boundary
- blocked current lane: `supervised_run_retry_gate_input_attestation`
- attestation-pass successor: `supervised_run_retry_execution`
