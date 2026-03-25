# TASK-006-REPLAY-ANALYSIS Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#22` merge commit `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b` on `2026-03-25T20:35:55Z`.
- Supporting merged Vexter states remained PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Re-read the promoted replay-deepening baseline and checked live, replay, and export surfaces session by session.
- Explained Dexter's uncovered replay session and its large outlier gap without changing frozen source logic.
- Rechecked Mew-X replay stability against exported session summaries and live `position_closed` events.
- Refreshed replay-analysis artifacts, status, handoff, and bundle outputs.

## Replay Analysis Result

### Dexter coverage hole

- Uncovered promoted live session: `6aHTh9r311kVEGTcQ3WTGoJofuqYiX6VeWoF6VwEThAb-1774461707938`
- That live session closed on the `safe` path at fill price `4.642072982663897e-08` and still had no matching replay JSON in the promoted Dexter package.
- The pinned Dexter source only moves mints into the replayable `stagnant_mints` export surface after `5m` without tx or `price <= 3e-8` with `30s` inactivity.
- This session stayed above `3e-8`, and the run ended only `120` seconds later, so the missing coverage is a source-surface omission, not a Vexter linkage bug.

### Dexter outlier gap

- Outlier session `AdCvMqzaCbEdoVk4LyVgzgU4XSUEL6QqQ453de8ZxsRa-1774461707938` exited live on the `safe` path at `+26.4375 pct`.
- Its stagnant-mint replay export continues past the live exit, peaks later, and ends at `2.7999578714853248e-08`, so replay reconstruction closes at `-26.4240 pct`.
- The `52.8615 pct` session gap is therefore explained by replay-surface semantics: the export preserves a later terminal path, not the live `safe` exit decision.

### Mew-X stability

- All six promoted Mew-X session-summary exports matched live `position_closed` values on entry price, exit price, realized return, MFE, MAE, time-to-peak, and session duration.
- Mew-X `0.0000` gap is strong evidence that exported summaries faithfully mirror live close metrics on this baseline.
- That result is still summary-driven fidelity, not proof of an independent path-level replay model.

## Decision

- Outcome: `A`
- Key finding: `replay_surface_gap_found`
- TASK-006 status: `needs replay-surface fix`
- Downstream comparative analysis ready: `no`

Inference from the replay-analysis proof:

- Dexter live-versus-replay gap is now explained as a frozen replay-surface limitation. Safe live exits and non-stagnant closes are not fully representable by the current stagnant-mint export surface, so the next narrow task is a replay-surface fix rather than another interpretation pass or downstream replay comparison.

## Key Paths

- Replay-analysis report: `artifacts/reports/task-006-replay-analysis.md`
- Updated status report: `artifacts/reports/task-006-replay-validation-status.md`
- Replay-analysis proof: `artifacts/proofs/task-006-replay-analysis-check.json`
- Replay-analysis summary: `artifacts/proofs/task-006-replay-analysis-summary.md`
- Handoff: `artifacts/reports/task-006-replay-analysis-handoff`
- Handoff bundle: `artifacts/bundles/task-006-replay-analysis.tar.gz`
