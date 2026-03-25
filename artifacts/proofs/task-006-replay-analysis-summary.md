# TASK-006 Replay Analysis

## GitHub Basis

- Latest merged Vexter main: PR `#22` commit `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`
- Dexter main: PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Key Findings

- Dexter coverage hole is a missing source replay export, not a Vexter linkage bug.
- Dexter outlier gap comes from replay terminal price history continuing past the live `safe` exit.
- Mew-X session summaries match all six promoted live close metrics exactly.
- Mew-X `0.0000` gap therefore proves summary fidelity on this baseline, not independent full-path replay.

## Decision

- Key finding: `replay_surface_gap_found`
- TASK-006 state: `needs_replay_surface_fix`
- Next step: `task_006_replay_surface_fix`
