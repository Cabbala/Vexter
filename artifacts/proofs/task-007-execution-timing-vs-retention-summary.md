# TASK-007-EXECUTION-TIMING-VS-RETENTION Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#29` merge commit `17af013b0383fd142e15932108c8b4da5447f1f7` on `2026-03-25T22:57:54Z`.
- Supporting merged Vexter states remained PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`, PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`, PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Reused the promoted live comparison, repaired replay comparison, committed Mew-X session summaries, and committed Dexter close-summary metrics already visible in Vexter.
- Reaggregated only the minimum additional timing and exit-path slices needed to read `execution_timing_vs_retention` source-faithfully.
- Tested whether the comparison is best read as a stage split between Dexter's earlier timing / slippage edge and Mew-X's post-attempt fill / local-retention edge.

## Evidence Read

- Dexter keeps the upstream timing edge at `signal_to_attempt_latency_ms` `0.0` versus Mew-X `891.0`.
- Mew-X keeps the post-attempt fill edge at `attempt_to_fill_latency_ms` `1.5` versus Dexter `502.5`.
- Dexter still leads on slippage `0.0 bps`, MFE `34.8443 pct`, realized exit `7.1641 pct`, and stale ratio `0.00%`.
- Mew-X still leads on MAE `0.0 pct`, time to peak `20.5 ms`, and realized-vs-peak gap `0.0 pct`.
- Mew-X session summaries show all six closes ending as `inactivity_timeout`, while Dexter close summaries show only `safe` and `malicious` exits with zero stale closes.
- The repaired replay comparison preserves the same scored winners, while Dexter `realized_vs_peak_gap_pct` remains the only path-sensitive live/replay drift.

## Interpretation

- The tradeoff is real, but it is stage-specific rather than a scalar overall winner.
- Dexter is stronger when the objective favors earlier entry, lower slippage, larger excursion capture, positive realized exit, and non-stale lifecycle control.
- Mew-X is stronger when the objective favors faster post-attempt fills, lower adverse excursion, faster local peak discovery, and minimal giveback from local peak.
- This supports `timing_retention_tradeoff_supported`, but the claim remains `tradeoff_bounded` because Mew-X does not also beat Dexter on realized exit or stale-position control.

## Decision

- Outcome: `A`
- Key finding: `timing_retention_tradeoff_supported`
- Claim boundary: `tradeoff_bounded`
- Decision: `next_lane_ready`
- Recommended next lane: `risk_containment_vs_exit_capture`

## Key Paths

- Timing/retention report: `artifacts/reports/task-007-execution-timing-vs-retention-report.md`
- Timing/retention status: `artifacts/reports/task-007-execution-timing-vs-retention-status.md`
- Timing/retention proof: `artifacts/proofs/task-007-execution-timing-vs-retention-check.json`
- Timing/retention prompt pack: `artifacts/reports/task-007-execution-timing-vs-retention`
- Timing/retention bundle: `artifacts/bundles/task-007-execution-timing-vs-retention.tar.gz`
