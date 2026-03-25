# TASK-006-REPLAY-ANALYSIS

## Scope

This task starts from the PR `#22` replay-deepening baseline and interprets the measured live-versus-replay gap without changing Dexter or Mew-X source logic.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#22`, merge commit `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, merged at `2026-03-25T20:35:55Z`
- Supporting merged Vexter states: PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Task Did

- Rechecked the promoted replay-deepening proof and replay packages against the accepted pass-grade pair.
- Compared live events, replay exports, and reconstructed replay results session by session for Dexter.
- Compared Mew-X exported session summaries against live `position_closed` events to interpret the zero-gap result.
- Refreshed replay-analysis artifacts, status, handoff, and bundle outputs.

## Dexter Coverage Hole

- Uncovered promoted live session key: `6aHTh9r311kVEGTcQ3WTGoJofuqYiX6VeWoF6VwEThAb-1774461707938`
- Live evidence shows a `safe` close at `2026-03-25T18:03:10.787868Z` with fill price `4.642072982663897e-08`.
- The same session never produced a replay JSON in the promoted Dexter package `replays/` directory.
- The creator leaderboard snapshot is creator-level only and has no mint or session row that can recover a missing `6aH...` replay surface.

Source-faithful interpretation:

- At pinned Dexter commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, the per-mint replayable surface comes from `stagnant_mints`, which is populated only when a mint sees either `5m` without tx or `price <= 3e-8` with `30s` inactivity.
- The `6aH...` close stayed above `3e-8`, and the run ended only `120` seconds later, so the frozen source had no opportunity to move that mint into the replay-export surface before shutdown.
- This is therefore not a Vexter package-selection or session-linkage bug. The source export is absent.

## Dexter Outlier Gap (`AdCv...`)

- Live Dexter exited `AdCvMqzaCbEdoVk4LyVgzgU4XSUEL6QqQ453de8ZxsRa-1774461707938` on the `safe` path, with exit signal `5.55560771341931e-08`, fill `4.811617746650403e-08`, and realized return `+26.4375 pct`.
- The matching stagnant-mint replay export exists, but its `price_history` continues to `2026-03-25T18:02:52.001Z`, peaks at `6.77183083289337e-08`, and ends at `2.7999578714853248e-08`.
- Replay deepening reconstructs Dexter exits from the last exported price tick and labels them `replay_terminal_price`, so the same session closes at `-26.4240 pct` in replay.
- The measured session gap is `-52.8615 pct`.

Source-faithful interpretation:

- The gap is not caused by a live or replay session mismatch. It is caused by surface semantics.
- Live Dexter sells while the session is still active when `safe`, `malicious`, or `drop-time` thresholds fire.
- The frozen replay export does not preserve that live exit decision. It only preserves a later stagnant terminal path, so Vexter can replay the post-entry price history but not the live `safe` exit itself.
- `EAD...` and `GFY...` land at `0` gap because their live exits already aligned with the terminal replay price. `AdCv...` does not.

## Mew-X `0.0000` Gap Interpretation

- All six promoted Mew-X session-summary exports matched the live `position_closed` values for entry price, exit price, realized return, MFE, MAE, time-to-peak, and session duration exactly.
- At frozen Mew-X commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, the source exports each session summary from the same session state immediately after `position_closed` is emitted.
- Replay deepening reconstructs Mew-X exits directly from those exported summary fields.

Interpretation:

- Mew-X `0.0000` gap is a strong signal that the exported session summaries faithfully mirror live close metrics on this promoted baseline.
- It is not, by itself, proof of an independent path-level replay model. The current fidelity claim is summary fidelity, not full execution replay equivalence.

## Live-versus-Replay Gap Meaning

- Dexter gap currently measures how far a live close can drift from a later stagnant-surface terminal reconstruction.
- Mew-X gap currently measures whether exported session summaries agree with the live close event they summarize.
- The two gaps are therefore not yet symmetric replay-fidelity claims. Dexter still lacks a surface that faithfully captures all promoted closes, while Mew-X already has a close-summary surface that does.

## Decision

- Outcome: `A`
- Key finding: `replay_surface_gap_found`
- TASK-006 state: `needs_replay_surface_fix`
- Downstream comparative analysis: `not yet ready`

## Recommended Next Step

Proceed to a narrow Dexter replay-surface fix task:

- preserve frozen strategy, trust, and threshold semantics
- expose a replay surface for safe exits and non-stagnant closed sessions, or otherwise export a per-session close summary that can reproduce live terminal metrics
- rerun replay analysis after that surface exists

## Key Paths

- Replay-analysis proof: `artifacts/proofs/task-006-replay-analysis-check.json`
- Replay-analysis summary: `artifacts/proofs/task-006-replay-analysis-summary.md`
- Prior replay-deepening proof: `artifacts/proofs/task-006-replay-deepening-check.json`
- Replay comparison output: `artifacts/reports/task006-replay-deepening-20260325T180027Z-replay-comparison`
- Replay package root: `artifacts/proofs/task006-replay-deepening-20260325T180027Z-replay-packages`
