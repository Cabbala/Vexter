# Demo Forward Supervised Run Retry Gate Attestation Refresh Plan

## Implementation Steps
1. Reverify the latest GitHub-visible Vexter `main` state at PR `#82` merge commit `eebfcd9b03e1e365cc4659996ea2638e6f285bbc`.
2. Accept attestation record-pack regeneration as the blocked baseline current source of truth.
3. Generate one bounded attestation refresh lane with current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.
4. For each required face, carry forward the repo-visible marker and regeneration owner, then fix refresh trigger, minimum fresh evidence locator shape, stale condition, and retry-gate-usable rule from the regeneration decision surface.
5. Keep `FAIL/BLOCKED` unless every face points to a current, fresh-enough, reviewable regenerated locator.
6. Recommend `supervised_run_retry_gate_attestation_record_pack_regeneration` while blocked and expose `supervised_run_retry_gate` only as the pass successor.

## Guardrails
- Dexter-only real demo slice
- `single_sleeve`
- `dexter_default`
- Dexter `paper_live`
- frozen Mew-X `sim_live`
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded supervised window required
- external credential refs remain outside repo
- operator owner explicit
- venue / connectivity confirmation explicit
- bounded start criteria explicit
- allowlist / symbol / lot-size reconfirmation explicit
- `manual_latched_stop_all` visibility reconfirmation explicit
- terminal snapshot readability reconfirmation explicit
- Mew-X unchanged
- funded live forbidden

## Validation
- generate the lane with `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py`
- rebuild the tarball with `./scripts/build_proof_bundle.sh`
- verify shared regression expectations with `pytest -q`
