# TASK-007-CANDIDATE-GENERATION-VS-QUALITY Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#28` merge commit `4df259b90365787ac24085227fcc1b15b63d057d` on `2026-03-25T22:36:55Z`.
- Supporting merged Vexter states remained PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`, PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Started from the merged downstream research intake and kept the promoted baseline frozen.
- Reused only committed live/replay comparisons, Mew-X candidate snapshots, Mew-X session summaries, and Dexter close-summary metrics.
- Added the minimum funnel reaggregation needed to test whether Dexter's candidate breadth reaches realized edge.

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

- Dexter funnel: `255 creator_candidate -> 12 mint_observed -> 4 entry_fill -> 4 position_closed`
- Dexter downstream medians: realized `7.1641 pct`, MFE `34.8443 pct`, slippage `0.0 bps`, stale `0.00%`
- Mew-X candidate snapshots: `initial_selection=0`, `refresh=0`
- Mew-X downstream medians: realized `0.0 pct`, MFE `6.7929 pct`, slippage `7.7061 bps`, stale `100.00%`
- Live and repaired replay preserve the same candidate-count and downstream edge surfaces

Source-faithful interpretation:

- Dexter candidate breadth looks like upstream screening that lands on stronger realized-edge outcomes, not simple breadth alone.
- Cross-source candidate quality remains bounded because Mew-X still lacks a comparable `creator_candidate` surface and both committed candidate snapshots are empty.

## Decision

- Outcome: `A`
- Key finding: `candidate_edge_supported`
- Claim boundary: `candidate_quality_bounded`
- Current task status: `candidate_edge_supported`
- Recommended next lane: `execution_timing_vs_retention`
- Decision: `next_lane_ready`

## Key Paths

- Candidate lane report: `artifacts/reports/task-007-candidate-generation-vs-quality-report.md`
- Candidate lane status: `artifacts/reports/task-007-candidate-generation-vs-quality-status.md`
- Candidate lane proof: `artifacts/proofs/task-007-candidate-generation-vs-quality-check.json`
- Candidate lane summary: `artifacts/proofs/task-007-candidate-generation-vs-quality-summary.md`
- Candidate lane prompt pack: `artifacts/reports/task-007-candidate-generation-vs-quality`
- Candidate lane bundle: `artifacts/bundles/task-007-candidate-generation-vs-quality.tar.gz`
