# TASK-006-REPLAY-SURFACE-FIX Handoff

## Verified GitHub State

- Vexter latest merged `main`: PR `#23`, `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`
- Supporting Vexter states: PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Task Did

- Added Vexter-side close-summary replay exports for all promoted non-stagnant Dexter closes
- Preserved stagnant replay exports and frozen source semantics
- Rebuilt the promoted comparable pack and replay packages from the augmented Dexter package
- Confirmed full promoted replay coverage and zero live-versus-replay gap on both sides
- Updated task artifacts, status, and bundle outputs for TASK-006 replay surface fix

## Key Finding

- `surface_fix_applied`

## Outcome

- Selected outcome: `A`
- Dexter replay coverage: `4 / 4` (`100.00%`)
- Dexter `live_vs_replay_gap_pct`: `0.0000`
- Mew-X replay coverage: `6 / 6` (`100.00%`)
- Mew-X `live_vs_replay_gap_pct`: `0.0000`
- TASK-006 status: `ready_for_downstream_comparative_analysis`

## Recommended Next Step

- Keep Dexter and Mew-X strategy semantics frozen
- Use the replay-surface-fixed promoted baseline for downstream comparative analysis
- Preserve the interpretation that current replay parity is summary fidelity for non-stagnant closes, not a broader path-level claim than the artifacts support

## Key Paths

- Replay-surface-fix report: `artifacts/reports/task-006-replay-surface-fix.md`
- Status report: `artifacts/reports/task-006-replay-validation-status.md`
- Replay-surface-fix proof: `artifacts/proofs/task-006-replay-surface-fix-check.json`
- Replay-surface-fix summary: `artifacts/proofs/task-006-replay-surface-fix-summary.md`
- Augmented Dexter package: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-augmented-dexter-package`
- Replay packages: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-replay-packages`
