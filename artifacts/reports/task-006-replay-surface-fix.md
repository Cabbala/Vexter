# TASK-006-REPLAY-SURFACE-FIX

## Scope

This task starts from the merged PR `#23` replay-analysis baseline and repairs the Dexter replay surface on the promoted comparable package without changing frozen Dexter or Mew-X source semantics.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#23`, merge commit `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, merged at `2026-03-25T21:05:35Z`
- Supporting merged Vexter states: PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Task Did

- Copied the promoted Dexter live package into an augmented package and materialized `4` non-stagnant close-summary replay exports from the frozen live event stream.
- Indexed those close-summary exports inside the augmented Dexter package while preserving the original stagnant-mint replay exports as fallback evidence.
- Revalidated the promoted baseline, rebuilt the promoted comparison pack, and reran replay reconstruction / gap measurement against the augmented Dexter package.
- Refreshed replay-surface-fix artifacts, status, handoff, and bundle outputs.

## Dexter Replay Surface Repair

- The promoted Dexter package now carries close-summary replay exports for all `4` promoted `position_closed` sessions.
- The previously uncovered live session `6aHTh9r311kVEGTcQ3WTGoJofuqYiX6VeWoF6VwEThAb-1774461707938` is no longer missing from replay evidence.
- The prior outlier session `AdCvMqzaCbEdoVk4LyVgzgU4XSUEL6QqQ453de8ZxsRa-1774461707938` now replays with the same live close metrics instead of the later stagnant terminal path.
- Stagnant-mint replay exports remain present in the package; the close-summary surface is a narrow additive repair for non-stagnant close fidelity.

## Replay Measurement Result

- Dexter replay validation: `pass`
- Dexter replay coverage: `100.00%` (`4 / 4`)
- Dexter `live_vs_replay_gap_pct`: `0.0000`
- Dexter unmatched live sessions: `[]`
- Mew-X replay validation: `pass`
- Mew-X replay coverage: `100.00%`
- Mew-X `live_vs_replay_gap_pct`: `0.0000`
- Promoted comparison pack winner mode: `derived`

## Decision

- Outcome: `A`
- Key finding: `surface_fix_applied`
- TASK-006 state: `ready_for_downstream_comparative_analysis`
- Downstream comparative analysis: `ready`

Interpretation:

- On the promoted baseline, Dexter replay parity is now a close-summary fidelity claim for non-stagnant closes, analogous in shape to the existing Mew-X summary-fidelity interpretation. That is sufficient to clear the replay-surface blocker identified in replay analysis and move TASK-006 forward.

## Key Paths

- Replay-surface-fix proof: `artifacts/proofs/task-006-replay-surface-fix-check.json`
- Replay-surface-fix summary: `artifacts/proofs/task-006-replay-surface-fix-summary.md`
- Augmented Dexter package: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-augmented-dexter-package`
- Promoted baseline rebuild: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-results`
- Replay package root: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-replay-packages`
- Replay comparison output: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
