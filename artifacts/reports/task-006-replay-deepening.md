# TASK-006-REPLAY-DEEPENING

## Scope

This task continues TASK-006 from the PR #21 replay-validation baseline. The promoted same-attempt live pack stays the formal source of truth, Dexter and Mew-X source logic stay frozen, and the confirmatory Mew-X `candidate_rejected` residual stays a narrow context note only.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#21`, merge commit `d7845b665afc912da593f2601e6a3d39524964d0`, merged at `2026-03-25T20:05:57Z`
- Supporting merged Vexter states: PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Task Did

- Reconstructed promoted-baseline `mode=replay` run packages for Dexter and Mew-X under `artifacts/proofs/task006-replay-deepening-20260325T180027Z-replay-packages`
- Re-ran `validate`, `derive-metrics`, and `build-pack` on the replay-mode packages into `artifacts/proofs/task006-replay-deepening-20260325T180027Z-replay-results`
- Mirrored the replay comparison outputs into `artifacts/reports/task006-replay-deepening-20260325T180027Z-replay-comparison`
- Measured live-versus-replay gap from matched `position_closed` sessions without changing any frozen source logic or validator rules

## Replay Reconstruction Result

### Dexter replay package

- Validation: `pass`
- Reconstructed replay session coverage: `3 / 4` (`75.00%`)
- `live_vs_replay_gap_pct`: `17.6205`
- Max absolute session gap: `52.8615`
- Remaining uncovered live session keys: `6aHTh9r311kVEGTcQ3WTGoJofuqYiX6VeWoF6VwEThAb-1774461707938`

Inference:

- Dexter replay reconstruction is now measurable, but still partial because one live closed session (`6aHTh9r311kVEGTcQ3WTGoJofuqYiX6VeWoF6VwEThAb-1774461707938`) had no matching stagnant-mint replay export and one reconstructed session (`AdCvMqzaCbEdoVk4LyVgzgU4XSUEL6QqQ453de8ZxsRa`) diverged sharply from live exit behavior.

### Mew-X replay package

- Validation: `pass`
- Reconstructed replay session coverage: `6 / 6` (`100.00%`)
- `live_vs_replay_gap_pct`: `0.0000`
- Max absolute session gap: `0.0000`

Inference:

- Mew-X replay reconstruction matched all six promoted closed sessions exactly through exported session summaries, so the measurable gap on the current promoted baseline is `0 pct`.

## Replay Comparison Pack

- Replay comparison pack: `artifacts/reports/task006-replay-deepening-20260325T180027Z-replay-comparison`
- Winner mode: `derived`
- This pack compares reconstructed replay-mode evidence source-to-source, while the gap measurements above stay source-local live-versus-replay checks.

## Decision

- Outcome: `A`
- Key finding: `gap_measured`
- TASK-006 state: `ready_for_next_replay_analysis_step`
- Confirmatory residual retained as context note: `Mew-X candidate_rejected`

## Next Step

Proceed to replay analysis / gap interpretation:

- explain the Dexter outlier replay gap and the missing replay export coverage hole
- treat Mew-X replay summaries as currently stable downstream replay evidence
- keep both source repos frozen unless a later explicitly approved task changes collection or replay surfaces
