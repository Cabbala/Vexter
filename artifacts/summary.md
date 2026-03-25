# TASK-007-RISK-CONTAINMENT-VS-EXIT-CAPTURE Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#30` merge commit `052de6ccecef1461d2291fb4f0ef5fbf8883d548` on `2026-03-25T23:15:40Z`.
- Supporting merged Vexter states remained PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`, PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`, PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`, PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Started from the completed timing-versus-retention lane and kept the promoted comparison baseline frozen.
- Reused only promoted live/replay comparison packs, committed Mew-X session summaries, and committed Dexter close-summary metrics.
- Added only minimal objective-specific regrouping needed to separate price-path containment from realized exit capture and stale-position control.

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Promoted live winner mode: `derived`
- Promoted replay winner mode: `derived`
- Stable scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Confirmatory residual: `Mew-X candidate_rejected`
- Confirmatory residual overturns promoted baseline: `no`

## Lane Result

- Mew-X keeps the price-path containment edge: median `max_adverse_excursion_pct` `0.0` vs Dexter `-6.0547`, median `time_to_peak_ms` `20.5` vs Dexter `5299.0`, and median `realized_vs_peak_gap_pct` `0.0` live / `0.0` replay vs Dexter `20.5330` live / `25.8042` replay.
- Dexter keeps the exit-capture edge: median `max_favorable_excursion_pct` `34.8443` vs Mew-X `6.7929`, median `realized_exit_pct` `7.1641` vs Mew-X `0.0`, and median quote-to-fill slippage `0.0 bps` vs Mew-X `7.7061 bps`.
- Dexter also keeps the lifecycle-control edge: `stale_position_ratio` `0.00%` vs Mew-X `100.00%`, with Dexter exits split across `safe=2` and `malicious=2`, while all Mew-X closes remain `inactivity_timeout=6`.
- Mew-X session summaries still show peak-to-close windows clustered at roughly five seconds (`5013-5028 ms`) after a very fast local peak, so its retention edge is local and timeout-shaped rather than an active downstream exit-control edge.

Source-faithful interpretation:

- The tradeoff is real, but "risk containment" splits into two surfaces instead of one.
- Mew-X is stronger when the objective weights price-path drawdown containment and local-peak retention.
- Dexter is stronger when the objective weights realized upside capture, lower slippage, and stale-position avoidance.
- The claim stays bounded because Mew-X's containment edge does not extend to realized exit or lifecycle control on the frozen baseline.

## Decision

- Outcome: `A`
- Key finding: `risk_exit_tradeoff_supported`
- Claim boundary: `tradeoff_bounded`
- Current task status: `risk_exit_tradeoff_supported`
- Recommended next step: `strategy_planning`
- Decision: `planning_ready`

## Key Paths

- Risk/exit report: `artifacts/reports/task-007-risk-containment-vs-exit-capture-report.md`
- Risk/exit status: `artifacts/reports/task-007-risk-containment-vs-exit-capture-status.md`
- Risk/exit proof: `artifacts/proofs/task-007-risk-containment-vs-exit-capture-check.json`
- Risk/exit summary: `artifacts/proofs/task-007-risk-containment-vs-exit-capture-summary.md`
- Risk/exit prompt pack: `artifacts/reports/task-007-risk-containment-vs-exit-capture`
- Risk/exit bundle: `artifacts/bundles/task-007-risk-containment-vs-exit-capture.tar.gz`
