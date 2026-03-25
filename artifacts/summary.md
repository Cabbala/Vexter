# TASK-006-REPLAY-DEEPENING Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#21` merge commit `d7845b665afc912da593f2601e6a3d39524964d0` on `2026-03-25T20:05:57Z`.
- Supporting merged Vexter states remained PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Reconstructed promoted-baseline `mode=replay` packages for Dexter and Mew-X from the accepted same-attempt live pair.
- Re-ran `validate`, `derive-metrics`, and `build-pack` on those replay packages.
- Measured source-local live-versus-replay gap from matched reconstructed `position_closed` sessions.
- Preserved the confirmatory Mew-X `candidate_rejected` residual as a narrow context note only.

## Replay Deepening Result

### Promoted pair `task005-pass-grade-pair-20260325T180027Z`

- Dexter replay package validated `pass` and reconstructed `3 / 4` live closed sessions.
- Dexter `live_vs_replay_gap_pct` measured `17.6205` with one uncovered live session and one large outlier gap (`52.8615` max abs gap).
- Mew-X replay package validated `pass` and reconstructed `6 / 6` live closed sessions.
- Mew-X `live_vs_replay_gap_pct` measured `0.0000`.
- Replay comparison pack on reconstructed replay evidence stayed `winner_mode: derived`.

### Confirmatory context

- Residual note remains `Mew-X candidate_rejected` only.
- That residual still does not overturn the promoted replay baseline.

## Decision

- Outcome: `A`
- Key finding: `gap_measured`
- TASK-006 status: `ready for next replay-analysis step`
- Replay blocker at measurement: `partial Dexter coverage only`

Inference from the replay-deepening proof:

- Mew-X replay summaries currently reproduce the promoted live closes exactly, while Dexter replay evidence is now measurable but not yet uniformly trustworthy because one promoted closed session lacks replay export coverage and one reconstructed replay path diverges sharply from live exit behavior.

## Key Paths

- Replay-deepening report: `artifacts/reports/task-006-replay-deepening.md`
- Updated status report: `artifacts/reports/task-006-replay-validation-status.md`
- Replay-deepening proof: `artifacts/proofs/task-006-replay-deepening-check.json`
- Replay-deepening summary: `artifacts/proofs/task-006-replay-deepening-summary.md`
- Replay comparison output: `artifacts/reports/task006-replay-deepening-20260325T180027Z-replay-comparison`
- Replay package root: `artifacts/proofs/task006-replay-deepening-20260325T180027Z-replay-packages`
- Handoff bundle: `artifacts/bundles/task-006-replay-deepening.tar.gz`
