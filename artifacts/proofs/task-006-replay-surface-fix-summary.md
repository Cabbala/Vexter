# TASK-006 Replay Surface Fix

## Verified GitHub State

- Latest merged Vexter `main`: PR `#23` at `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`
- Dexter pinned `main`: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What Changed

- Augmented Dexter promoted package with `4` non-stagnant close-summary replay exports.
- Kept stagnant replay exports as fallback and left source strategy semantics unchanged.
- Revalidated the promoted baseline, rebuilt the comparison pack, and reran replay deepening on the augmented package.

## Result

- Dexter replay coverage: `100.00%`
- Dexter `live_vs_replay_gap_pct`: `0.0000`
- Mew-X replay coverage: `100.00%`
- Mew-X `live_vs_replay_gap_pct`: `0.0000`
- Promoted comparison winner mode: `derived`

## Decision

- Key finding: `surface_fix_applied`
- TASK-006 state: `ready_for_downstream_comparative_analysis`
- Next step: `task_006_downstream_comparative_analysis`
