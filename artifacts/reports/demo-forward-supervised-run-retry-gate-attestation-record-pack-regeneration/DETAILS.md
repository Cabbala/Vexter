# ATTESTATION-RECORD-PACK-REGENERATION Details

## Verified Starting Point
- Latest Vexter `main`: PR `#90` merge commit `f79997cc0b619c2542cd6e9f876abcfb7ffca3f8` on `2026-03-27T21:29:43Z`
- Dexter pinned commit: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Accepted baseline: `supervised_run_retry_gate_attestation_refresh_blocked`

## Deliverable
Promote one bounded attestation record-pack regeneration lane that keeps current status, report, summary, proof, handoff, checklist, and decision-surface pointers coherent while fail-closing retry-gate review until every required regenerated face is current and reviewable. The canonical external-evidence manifest currently sits at status `template_only` and therefore remains blocker-facing rather than pass-claiming.
