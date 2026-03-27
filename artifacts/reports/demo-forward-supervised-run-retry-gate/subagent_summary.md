# Demo Forward Supervised Run Retry Gate Sub-agent Summaries

## Anscombe
- Confirmed the retry-readiness quartet should remain current until a complete retry-gate quartet exists, then switch atomically to the new gate report, status, proof, summary, and handoff surfaces.
- Flagged the readiness-era prerequisite-count drift as a reason to keep the retry-gate decision surface on one explicit, stable list of gate inputs.
- Recommended keeping fail-closed wording observation-based: repo-visible markers may be named, but retry execution stays blocked until external confirmations are explicitly observed enough for the gate to pass.

## Euler
- Kept the retry-gate boundary identical to the accepted retry-readiness boundary: Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, allowlist-only, small-lot, one-plan, one-position, bounded supervision, and funded-live forbidden.
- Recommended the smallest next-step cut: hold the current lane at `supervised_run_retry_gate` while blocked, and expose `supervised_run_retry_execution` only as the gate-pass successor once every required input is explicit.
- Confirmed there is no need for planner or adapter code drift: `prepare / start / status / stop / snapshot` stays fixed, `manual_latched_stop_all` stays planner-owned, and Mew-X remains unchanged.

## Parfit
- Scoped the smallest safe change set to docs, proof-generation script, generated artifacts, manifest/context/ledger updates, and tests; no `vexter/` runtime behavior changes are needed for this lane.
- Recommended validating the generator plus the affected regression surfaces with `python3 scripts/run_demo_forward_supervised_run_retry_gate.py` and focused `pytest` coverage on the supervised-run and bundle-layout tests.
- Merge readiness depends on an atomic current-pointer switch to retry-gate, a regenerated tarball at the new bundle path, and a clean blocked decision that does not claim retry execution success.
