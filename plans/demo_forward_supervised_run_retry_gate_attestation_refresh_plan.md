# Demo Forward Supervised Run Retry Gate Attestation Refresh Plan

## Implementation Steps
1. Reverify the latest GitHub-visible Vexter `main` state at PR `#104` merge commit `7a272b0e4367204397d6c4c87340365b35a599b8`.
2. Accept attestation record-pack regeneration as the blocked baseline current source of truth.
3. Keep refresh consuming the shared canonical outside-repo evidence manifest template, contract, validator, and unified evidence preflight / reopen-readiness surface from the regeneration baseline.
4. Regenerate the explicit next-human-pass checklist plus template-only false-path explanation from the canonical preflight blockers.
5. Generate one bounded attestation refresh lane with current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.
6. For each required face, carry forward the repo-visible marker and regeneration owner, then fix refresh trigger, minimum fresh evidence locator shape, stale condition, and retry-gate-usable rule from the canonical gap output.
7. Keep `FAIL/BLOCKED` unless every face points to a current, fresh-enough, reviewable evidence locator.
8. Recommend `supervised_run_retry_gate_attestation_record_pack_regeneration` while blocked and expose `supervised_run_retry_gate` only as the pass successor.

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
- generate the canonical evidence preflight with `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py`
- generate the lane with `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py`
- verify pointer-sensitive shared surfaces with `python3.12 -m pytest -q tests/test_demo_forward_supervised_run_retry_gate_attestation_refresh.py tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py tests/test_demo_forward_supervised_run_retry_gate.py tests/test_demo_forward_supervised_run_retry_gate_evidence_preflight.py tests/test_demo_forward_supervised_run_retry_gate_external_evidence_gap.py`
- rebuild the tarball with `./scripts/build_proof_bundle.sh`
- finish with `python3.12 -m pytest -q`
