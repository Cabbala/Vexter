# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Plan

## Implementation Steps
1. Reverify the latest GitHub-visible Vexter `main` state at PR `#83` merge commit `5b78804188e27199e90950f610fd279ad7a133f6`.
2. Accept attestation refresh as the blocked baseline current source of truth.
3. Generate one bounded attestation record-pack regeneration lane with current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.
4. For each required face, carry forward the bounded refresh locator rule, then fix regeneration owner, regeneration trigger, minimum regenerated locator shape, freshness inheritance or reset rule, and reviewable-enough rule.
5. Keep `FAIL/BLOCKED` unless every face can regenerate from one current, fresh-enough, reviewable locator.
6. Recommend `supervised_run_retry_gate_attestation_refresh` while blocked and expose `supervised_run_retry_gate` only as the pass successor.

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
- generate the lane with `python3 scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py`
- rebuild the tarball with `./scripts/build_proof_bundle.sh`
- verify shared regression expectations with `pytest -q`
