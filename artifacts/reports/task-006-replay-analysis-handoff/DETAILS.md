# TASK-006-REPLAY-ANALYSIS Handoff

## Verified GitHub State

- Vexter latest merged `main`: PR `#22`, `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`
- Supporting Vexter states: PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Task Did

- Reinterpreted promoted replay-deepening evidence session by session
- Explained Dexter replay coverage hole as a missing source replay export
- Explained Dexter outlier gap as a replay terminal-path versus live `safe` exit mismatch
- Confirmed that Mew-X `0.0000` gap comes from exact session-summary parity with live close metrics
- Updated task artifacts, status, and bundle outputs for TASK-006 replay analysis

## Key Finding

- `replay_surface_gap_found`

## Outcome

- Selected outcome: `A`
- Dexter replay coverage remains `3 / 4` (`75.00%`)
- Dexter `live_vs_replay_gap_pct` remains `17.6205`
- Mew-X replay coverage remains `6 / 6` (`100.00%`)
- Mew-X `live_vs_replay_gap_pct` remains `0.0000`
- TASK-006 status: `NEEDS REPLAY-SURFACE FIX`

## Recommended Next Step

- Keep Dexter and Mew-X strategy semantics frozen
- Narrow the follow-up to a Dexter replay-surface fix for safe exits and non-stagnant closed sessions
- Re-run replay analysis after that surface exists before claiming downstream replay comparability

## Key Paths

- Replay-analysis report: `artifacts/reports/task-006-replay-analysis.md`
- Status report: `artifacts/reports/task-006-replay-validation-status.md`
- Replay-analysis proof: `artifacts/proofs/task-006-replay-analysis-check.json`
- Replay-analysis summary: `artifacts/proofs/task-006-replay-analysis-summary.md`
- Prior replay packages: `artifacts/proofs/task006-replay-deepening-20260325T180027Z-replay-packages`
