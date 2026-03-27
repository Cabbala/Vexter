# Demo Forward Supervised Run Retry Gate Attestation Audit Sub-agent Summaries

## Anscombe
- Confirmed the input-attestation quartet should remain the accepted baseline until a complete attestation-audit quartet exists, then switch current report, status, proof, summary, and handoff pointers atomically.
- Recommended that the audit surface carry the same attestation facts per row in one place: who attests, what is being attested, the minimum evidence shape, the stale rule, and what makes the face auditable enough.
- Recommended fail-closed wording that stays observation-based: the repo may name the required face definitions, but retry-gate review remains blocked until each face points to a current bounded-window attestation record and stale check.

## Euler
- Kept the attestation-audit boundary identical to the accepted input-attestation boundary: Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, allowlist-only, small-lot, one-plan, one-position, bounded supervision, and funded-live forbidden.
- Recommended the smallest next-step cut: hold the current lane at `supervised_run_retry_gate_attestation_audit` while blocked, and expose `supervised_run_retry_gate` only as the audit-pass successor once retry-gate review can honestly reopen.
- Confirmed there is no planner or adapter drift: `prepare / start / status / stop / snapshot` stays fixed, `manual_latched_stop_all` stays planner-owned, funded live stays forbidden, and Mew-X remains unchanged.

## Parfit
- Scoped the smallest safe change set to docs, proof-generation script, generated artifacts, manifest/context/ledger updates, and tests; no `vexter/` runtime behavior changes are needed for this lane.
- Recommended validating the generator plus the affected regression surfaces with `python3 scripts/run_demo_forward_supervised_run_retry_gate_attestation_audit.py` and focused `pytest` coverage on the supervised-run and bundle-layout tests.
- Merge readiness depends on an atomic current-pointer switch to attestation audit, a regenerated tarball at the new bundle path, and a clean blocked decision that does not claim retry execution success or a reopened retry gate.
