# ATTESTATION-REFRESH Details

## Verified Starting Point
- Latest Vexter `main`: PR `#97` merge commit `1bde9ef2b19da11e8b61772e560dc3d60874c461` on `2026-03-28T13:40:06Z`
- Dexter pinned commit: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Accepted baseline: `supervised_run_retry_gate_attestation_record_pack_regeneration_blocked`

## Deliverable
Promote one bounded attestation refresh lane that keeps current status, report, summary, proof, handoff, checklist, and decision-surface pointers coherent while fail-closing retry-gate review until every required face has a current, fresh-enough, reviewable evidence locator and the current record-pack regeneration can be rerun honestly. The canonical external-evidence manifest currently sits at status `template_only`, the evidence preflight remains `blocked`, and the repo therefore stays blocker-facing rather than pass-claiming.
