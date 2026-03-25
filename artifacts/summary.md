# TASK-006-REPLAY-VALIDATION Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#20` merge commit `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668` on `2026-03-25T19:47:52Z`.
- Supporting merged Vexter states remained PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` on `2026-03-21T11:31:07Z`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, reverified on GitHub at `2026-03-20T16:05:19Z`.

## What This Task Did

- Re-ran `validate`, `derive-metrics`, and `build-pack` against the promoted and confirmatory pass-grade-pair packages on the PR `#20` comparison layer.
- Kept Dexter source logic, Mew-X source logic, and validator rules unchanged from the merged TASK-005 rule implementation.
- Assessed whether the promoted comparable pack is acceptable downstream replay input and whether the confirmatory residual overturns that intake decision.

## Replay-Validation Intake

### Promoted pair `task005-pass-grade-pair-20260325T180027Z`

- Validation stayed `pass/pass` with `winner_mode: derived`.
- The matched measurement window remained exact across Dexter `paper_live` and Mew-X `sim_live`.
- Dexter retained `raw_events: 1`, `replays: 92`, `db_exports: 92`, plus the required `leaderboard_snapshot` and `stagnant_mint_replay` exports.
- Mew-X retained `raw_events: 1` plus the required `candidate_refresh_snapshot` and `session_summary` exports.
- Both replayability grades remained `partial`, so the promoted pack is acceptable replay input but not a full replay closeout.

### Confirmatory pair `task005-pass-grade-pair-20260325T180604Z`

- Dexter stayed `pass`.
- Mew-X stayed `partial`, with the only active miss `candidate_rejected`.
- That residual remains a narrow note and does not overturn the promoted replay-input decision.

## Decision

- Outcome: `A`
- Key finding: `replay_input_accepted`
- TASK-006 status: `in progress`
- Replay blocker at intake: `no`
- Replay exit ready: `no`

Inference from the regenerated artifacts:

- `live_vs_replay_gap_pct` remains unmeasured because this task accepted the comparable live input but did not yet produce replay-mode run packages for gap calculation.

## Key Paths

- Replay-validation report: `artifacts/reports/task-006-replay-validation.md`
- Intermediate status report: `artifacts/reports/task-006-replay-validation-status.md`
- Replay-validation proof: `artifacts/proofs/task-006-replay-validation-check.json`
- Replay-validation summary: `artifacts/proofs/task-006-replay-validation-summary.md`
- Promoted comparison output: `artifacts/reports/task006-replay-validation-20260325T180027Z-comparison`
- Confirmatory comparison output: `artifacts/reports/task006-replay-validation-20260325T180604Z-comparison`
- Handoff bundle: `artifacts/bundles/task-006-replay-validation.tar.gz`
