# Demo Forward Supervised Run Retry Gate Input Attestation Sub-agent Summaries

## Anscombe
- Confirmed the retry-gate quartet should remain the accepted baseline until a complete input-attestation quartet exists, then switch current report, status, proof, summary, and handoff pointers atomically.
- Recommended that every attestation row carry the same five faces in one place: repo-visible marker, who attests, what is being attested, minimal evidence shape, and stale boundary.
- Recommended fail-closed wording that stays observation-based: the repo may name markers and attestation requirements, but gate recheck remains blocked until each attestation face is explicit enough to reopen review.

## Euler
- Kept the attestation boundary identical to the accepted retry-gate boundary: Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, allowlist-only, small-lot, one-plan, one-position, bounded supervision, and funded-live forbidden.
- Recommended the smallest next-step cut: hold the current lane at `supervised_run_retry_gate_input_attestation` while blocked, and expose `supervised_run_retry_execution` only as the attestation-pass successor once gate review can honestly reopen.
- Confirmed there is no need for planner or adapter code drift: `prepare / start / status / stop / snapshot` stays fixed, `manual_latched_stop_all` stays planner-owned, and Mew-X remains unchanged.

## Parfit
- Scoped the smallest safe change set to docs, proof-generation script, generated artifacts, manifest/context/ledger updates, and tests; no `vexter/` runtime behavior changes are needed for this lane.
- Recommended validating the generator plus the affected regression surfaces with `python3 scripts/run_demo_forward_supervised_run_retry_gate_input_attestation.py` and focused `pytest` coverage on the supervised-run and bundle-layout tests.
- Merge readiness depends on an atomic current-pointer switch to input attestation, a regenerated tarball at the new bundle path, and a clean blocked decision that does not claim retry execution success or a passed gate review.
