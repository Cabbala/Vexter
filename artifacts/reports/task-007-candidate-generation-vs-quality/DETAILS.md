# TASK-007-CANDIDATE-GENERATION-VS-QUALITY Package

## Verified GitHub State

- Vexter latest merged `main`: PR `#28`, `4df259b90365787ac24085227fcc1b15b63d057d`
- Supporting Vexter states: PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Package Does

- Reuses the frozen promoted live and repaired replay comparisons from intake
- Adds only minimal candidate-funnel reaggregation from already committed exports
- Tests whether Dexter's candidate breadth connects to realized edge without reopening comparison work
- Carries forward the Mew-X candidate-surface asymmetry as an explicit claim boundary

## Key Finding

- `candidate_edge_supported`

## Claim Boundary

- `candidate_quality_bounded`

## Core Evidence

- Dexter: `255 creator_candidate -> 12 mint_observed -> 4 fills -> 4 closes`
- Dexter medians: realized `7.1641 pct`, MFE `34.8443 pct`, slippage `0.0 bps`, stale `0.00%`
- Mew-X candidate snapshots: empty on both `initial_selection` and `refresh`
- Mew-X medians: realized `0.0 pct`, MFE `6.7929 pct`, slippage `7.7061 bps`, stale `100.00%`
- Live and repaired replay preserve the same candidate-count and downstream edge surfaces

## What Not To Redo

- Do not reopen promoted-baseline selection.
- Do not recollect live or replay evidence.
- Do not change Dexter, Mew-X, or validator rules.
- Do not widen the replay claim to full path equivalence.
- Do not infer a missing Mew-X upstream precision surface from empty snapshots.

## Recommended Next Step

- Continue with `execution_timing_vs_retention` as the next hypothesis lane.
- Keep `candidate_edge_supported` as the current bounded conclusion.
- Preserve `candidate_quality_bounded` until a separate task produces a truly comparable Mew-X upstream candidate surface.
