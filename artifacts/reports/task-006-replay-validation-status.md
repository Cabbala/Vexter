# TASK-006 Replay Status

## Verified Start

- Vexter `origin/main` verified at PR `#22` merge commit `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`
- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Current Result

- Promoted replay input accepted: `yes`
- Confirmatory residual overturning: `no`
- Confirmatory residual note: `Mew-X candidate_rejected`
- Dexter replay package validation: `pass`
- Dexter replay coverage: `75.00%`
- Dexter `live_vs_replay_gap_pct`: `17.6205`
- Dexter uncovered live session: `6aHTh9r311kVEGTcQ3WTGoJofuqYiX6VeWoF6VwEThAb-1774461707938`
- Dexter outlier gap session: `AdCvMqzaCbEdoVk4LyVgzgU4XSUEL6QqQ453de8ZxsRa-1774461707938`
- Mew-X replay package validation: `pass`
- Mew-X replay coverage: `100.00%`
- Mew-X `live_vs_replay_gap_pct`: `0.0000`
- Replay comparison pack winner mode: `derived`

## Decision

- TASK-006: `needs replay-surface fix`
- Key finding: `replay_surface_gap_found`
- Next step: `task_006_replay_surface_fix`

The promoted comparable pack is no longer just replay-input-ready: the measured Dexter gap is now explained. One promoted Dexter close has no replay export because the frozen source never moved that mint into the stagnant replay surface before shutdown, and the `AdCv...` outlier diverges because replay reconstruction exits at the later stagnant terminal price instead of the live `safe` exit. Mew-X replay summaries still match the promoted live closes exactly, but that result should be interpreted as summary fidelity rather than full-path replay equivalence.
