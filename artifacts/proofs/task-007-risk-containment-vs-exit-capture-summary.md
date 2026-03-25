# TASK-007-RISK-CONTAINMENT-VS-EXIT-CAPTURE Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#30` merge commit `052de6ccecef1461d2291fb4f0ef5fbf8883d548` on `2026-03-25T23:15:40Z`.
- Supporting merged Vexter states remained PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`, PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`, PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`, PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Reused the promoted live comparison, repaired replay comparison, committed Mew-X session summaries, and committed Dexter close-summary metrics already visible in Vexter.
- Reaggregated only the minimum additional risk/exit slices needed to read `risk_containment_vs_exit_capture` source-faithfully.
- Tested whether the current comparison is best read as price-path containment for Mew-X versus exit capture and lifecycle control for Dexter.

## Evidence Read

- Mew-X keeps the price-path containment edge at median MAE `0.0 pct` versus Dexter `-6.0547 pct`.
- Mew-X also keeps the fast-local-peak / retention edge at median `time_to_peak_ms` `20.5` and median `realized_vs_peak_gap_pct` `0.0 pct`.
- Dexter keeps the favorable-excursion / realized-exit edge at median MFE `34.8443 pct` versus Mew-X `6.7929 pct`, and median realized exit `7.1641 pct` versus Mew-X `0.0 pct`.
- Dexter keeps the lifecycle-control edge at stale ratio `0.00%` versus Mew-X `100.00%`, while all six Mew-X closes remain `inactivity_timeout`.
- The repaired replay comparison preserves the same scored winners, while Dexter `realized_vs_peak_gap_pct` remains the only path-sensitive live/replay drift.

## Interpretation

- The tradeoff is real, but "risk containment" is not a single scalar surface.
- Mew-X is stronger for price-path drawdown containment and local-peak retention.
- Dexter is stronger for realized upside capture, lower slippage, and stale-position avoidance.
- This supports `risk_exit_tradeoff_supported`, but the claim remains `tradeoff_bounded` because Mew-X does not also beat Dexter on realized exit or lifecycle control.

## Decision

- Outcome: `A`
- Key finding: `risk_exit_tradeoff_supported`
- Claim boundary: `tradeoff_bounded`
- Decision: `planning_ready`
- Recommended next step: `strategy_planning`

## Key Paths

- Risk/exit report: `artifacts/reports/task-007-risk-containment-vs-exit-capture-report.md`
- Risk/exit status: `artifacts/reports/task-007-risk-containment-vs-exit-capture-status.md`
- Risk/exit proof: `artifacts/proofs/task-007-risk-containment-vs-exit-capture-check.json`
- Risk/exit prompt pack: `artifacts/reports/task-007-risk-containment-vs-exit-capture`
- Risk/exit bundle: `artifacts/bundles/task-007-risk-containment-vs-exit-capture.tar.gz`
