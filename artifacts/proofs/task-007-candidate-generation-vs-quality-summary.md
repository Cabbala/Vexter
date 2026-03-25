# TASK-007-CANDIDATE-GENERATION-VS-QUALITY Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#28` merge commit `4df259b90365787ac24085227fcc1b15b63d057d` on `2026-03-25T22:36:55Z`.
- Supporting merged Vexter states remained PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`, PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Reused the promoted live comparison, repaired replay comparison, candidate snapshots, session summaries, and close-summary metrics already committed in Vexter.
- Reaggregated only the minimum additional funnel counts needed to read `candidate_generation_vs_quality` source-faithfully.
- Tested whether Dexter's `candidate_count` lead is just breadth or whether it connects to downstream realized-edge surfaces.

## Evidence Read

- Dexter state export recorded `255 creator_candidate`, `12 mint_observed`, `4 entry_fill`, and `4 position_closed`.
- Dexter close summaries showed `2` safe winners, `2` malicious losers, `4 / 4` positive MFE closes, median realized exit `7.1641 pct`, median MFE `34.8443 pct`, median slippage `0.0 bps`, and stale ratio `0.00%`.
- Mew-X committed candidate snapshots remained empty on both `initial_selection` and `refresh`, so `candidate_precision_proxy` stayed unavailable.
- Mew-X session summaries still showed `6` closes, but median realized exit stayed `0.0 pct`, median MFE `6.7929 pct`, median slippage `7.7061 bps`, and stale ratio `100.00%`.
- The repaired replay comparison preserved the same candidate-count and downstream edge surfaces, while the known Dexter `realized_vs_peak_gap_pct` drift remained only a path-sensitive caveat.

## Interpretation

- Dexter candidate breadth looks like a real upstream screening edge rather than simple fill-volume inflation.
- The broad candidate pool narrows into fewer fills than Mew-X, but those fills land on much stronger median favorable excursion and positive median realized exit.
- This supports `candidate_edge_supported` on the frozen promoted baseline.
- Cross-source upstream quality remains `candidate_quality_bounded` because Mew-X still does not expose a comparable `creator_candidate` surface and both committed candidate snapshots are empty.

## Decision

- Outcome: `A`
- Key finding: `candidate_edge_supported`
- Claim boundary: `candidate_quality_bounded`
- Decision: `next_lane_ready`
- Recommended next lane: `execution_timing_vs_retention`

## Key Paths

- Candidate lane report: `artifacts/reports/task-007-candidate-generation-vs-quality-report.md`
- Candidate lane status: `artifacts/reports/task-007-candidate-generation-vs-quality-status.md`
- Candidate lane proof: `artifacts/proofs/task-007-candidate-generation-vs-quality-check.json`
- Candidate lane prompt pack: `artifacts/reports/task-007-candidate-generation-vs-quality`
- Candidate lane bundle: `artifacts/bundles/task-007-candidate-generation-vs-quality.tar.gz`
