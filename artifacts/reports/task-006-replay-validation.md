# TASK-006-REPLAY-VALIDATION

## Scope

This task starts downstream replay validation from the GitHub-visible promoted comparable pack that became available after PR `#20`. The work stays inside the Vexter comparison layer, keeps Dexter and Mew-X source logic frozen, and treats the promoted pair as the formal intake baseline while carrying the confirmatory Mew-X `candidate_rejected` miss only as a narrow note.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#20`, merge commit `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, merged at `2026-03-25T19:47:52Z`
- Supporting merged Vexter states: PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, reverified on GitHub at `2026-03-20T16:05:19Z`

## What This Task Did

- Re-ran `validate`, `derive-metrics`, and `build-pack` on the promoted pair into `artifacts/proofs/task006-replay-validation-20260325T180027Z-results`
- Re-ran the same workflow on the confirmatory pair into `artifacts/proofs/task006-replay-validation-20260325T180604Z-results`
- Mirrored those regenerated comparison outputs into `artifacts/reports/task006-replay-validation-20260325T180027Z-comparison` and `artifacts/reports/task006-replay-validation-20260325T180604Z-comparison`
- Added a dedicated replay-validation proof at `artifacts/proofs/task-006-replay-validation-check.json`

No changes were made to:

- Dexter source logic
- Mew-X source logic
- validator rules introduced by TASK-005

## Replay-Validation Intake

### Promoted pair `task005-pass-grade-pair-20260325T180027Z`

- Validation remained `pass/pass`
- `winner_mode` remained `derived`
- The matched measurement window remained exact between Dexter `paper_live` and Mew-X `sim_live`
- Dexter replay surface remained stronger: `raw_events: 1`, `replays: 92`, `db_exports: 92`, required source exports present
- Mew-X replay surface remained narrower but acceptable for intake: `raw_events: 1`, required `candidate_refresh_snapshot` and `session_summary` exports present
- Both replayability grades remained `partial`, so the promoted pack is accepted as replay input but not yet a replay-complete closeout

### Confirmatory pair `task005-pass-grade-pair-20260325T180604Z`

- Dexter remained `pass`
- Mew-X remained `partial`
- The only active missing event type was `candidate_rejected`
- That residual is weaker than the promoted baseline and does not overturn the intake decision

## Intermediate Decision

- Outcome: `A`
- Key finding: `replay_input_accepted`
- Downstream comparability: `accepted_for_replay_validation`
- TASK-006 state: `in_progress`
- Replay exit ready: `no`

Inference:

- `live_vs_replay_gap_pct` is still unmeasured because this task accepted the promoted live comparable pack as replay input, but did not yet generate replay-mode run packages for gap calculation.

## Next Step

Continue TASK-006 as replay deepening:

- reconstruct replay-mode evidence from the accepted promoted baseline
- measure live-versus-replay gap once replay outputs exist
- keep the confirmatory Mew-X `candidate_rejected` miss as context only unless later evidence shows it is no longer narrow
