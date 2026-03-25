# TASK-006 Replay Status

## Verified Start

- Vexter `origin/main` verified at PR `#21` merge commit `d7845b665afc912da593f2601e6a3d39524964d0`
- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Current Result

- Promoted replay input accepted: `yes`
- Confirmatory residual overturning: `no`
- Confirmatory residual note: `Mew-X candidate_rejected`
- Dexter replay package validation: `pass`
- Dexter replay coverage: `75.00%`
- Dexter `live_vs_replay_gap_pct`: `17.6205`
- Mew-X replay package validation: `pass`
- Mew-X replay coverage: `100.00%`
- Mew-X `live_vs_replay_gap_pct`: `0.0000`
- Replay comparison pack winner mode: `derived`

## Decision

- TASK-006: `ready for next replay-analysis step`
- Key finding: `gap_measured`
- Next step: `task_006_replay_analysis`

The promoted comparable pack is no longer just replay-input-ready: replay-mode evidence now exists and the live-versus-replay gap is measurable. Dexter remains partially reconstructed because one promoted closed session has no stagnant-mint replay export and one reconstructed replay path diverges sharply from live exit behavior, while Mew-X replay summaries match the promoted live closes exactly on the current baseline.
