# TASK-006-REPLAY-DEEPENING Handoff

## Verified GitHub State

- Vexter latest merged `main`: PR `#21`, `d7845b665afc912da593f2601e6a3d39524964d0`
- Supporting Vexter states: PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Task Did

- Reconstructed promoted-baseline replay packages for Dexter and Mew-X
- Re-ran replay-mode `validate`, `derive-metrics`, and `build-pack`
- Measured promoted live-versus-replay gap for both sources
- Preserved the confirmatory Mew-X `candidate_rejected` residual as context note only
- Updated task artifacts, status, and bundle outputs for TASK-006 replay deepening

## Key Finding

- `gap_measured`

## Outcome

- Selected outcome: `A`
- Dexter replay coverage: `3 / 4` (`75.00%`)
- Dexter `live_vs_replay_gap_pct`: `17.6205`
- Mew-X replay coverage: `6 / 6` (`100.00%`)
- Mew-X `live_vs_replay_gap_pct`: `0.0000`
- TASK-006 status: `READY FOR NEXT REPLAY-ANALYSIS STEP`

## Recommended Next Step

- Analyze the Dexter outlier replay gap and the uncovered replay session before claiming replay trust is uniform
- Treat Mew-X replay summaries as the stronger currently confirmed replay surface
- Keep Dexter and Mew-X source logic frozen unless a later task explicitly approves a collection or export change

## Key Paths

- Replay-deepening report: `artifacts/reports/task-006-replay-deepening.md`
- Status report: `artifacts/reports/task-006-replay-validation-status.md`
- Replay-deepening proof: `artifacts/proofs/task-006-replay-deepening-check.json`
- Replay comparison output: `artifacts/reports/task006-replay-deepening-20260325T180027Z-replay-comparison`
- Replay packages: `artifacts/proofs/task006-replay-deepening-20260325T180027Z-replay-packages`
