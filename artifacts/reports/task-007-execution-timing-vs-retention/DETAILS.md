# TASK-007-EXECUTION-TIMING-VS-RETENTION Package

## Verified GitHub State

- Vexter latest merged `main`: PR `#29`, `17af013b0383fd142e15932108c8b4da5447f1f7`
- Supporting Vexter states: PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Package Does

- Reuses the frozen promoted live and repaired replay comparisons from `TASK-006`
- Reads timing and exit-path tradeoffs from committed Mew-X session summaries and Dexter close summaries only
- Adds only minimal regrouping needed to separate upstream timing, post-attempt fill speed, slippage control, and local-retention behavior
- Preserves the path-sensitive replay caveat instead of widening it into a new replay claim

## Key Finding

- `timing_retention_tradeoff_supported`

## Claim Boundary

- `tradeoff_bounded`

## Core Evidence

- Dexter `signal_to_attempt_latency_ms`: `0.0`; Mew-X: `891.0`
- Dexter `attempt_to_fill_latency_ms`: `502.5`; Mew-X: `1.5`
- Dexter slippage / exit-capture medians: `0.0 bps`, `7.1641 pct` realized, `34.8443 pct` MFE, `0.00%` stale
- Mew-X retention medians: `0.0 pct` MAE, `20.5 ms` time-to-peak, `0.0 pct` realized-vs-peak gap
- Mew-X closes: all `6` `inactivity_timeout`
- Dexter closes: `safe=2`, `malicious=2`, stale `0`

## What Not To Redo

- Do not reopen promoted-baseline selection.
- Do not recollect live or replay evidence.
- Do not change Dexter, Mew-X, or validator rules.
- Do not widen the replay claim to full path equivalence.
- Do not turn the stage split into a scalar universal winner claim.

## Recommended Next Step

- Continue with `risk_containment_vs_exit_capture` as the next hypothesis lane.
- Carry forward `timing_retention_tradeoff_supported` as the current bounded conclusion.
- Preserve `tradeoff_bounded` until a separate task explicitly resolves risk weighting or path-sensitive retention scope.
