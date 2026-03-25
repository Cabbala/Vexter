# TASK-007-STRATEGY-PLANNING Package

## Verified GitHub State

- Vexter latest merged `main`: PR `#31`, `0905ec8c991ca6046b13d0c326c3224c49709a2d`
- Supporting Vexter states: PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Package Does

- Reuses the fixed candidate, timing, and risk lane conclusions from `TASK-007`
- Converts the comparison result into objective-weighted source preference
- Marks Dexter as the default primary planning source and Mew-X as the bounded selective source
- Preserves hybrid room only at the design level as selective adoption or objective-conditioned portfolio split

## Key Finding

- `strategy_plan_ready`

## Claim Boundary

- `strategy_plan_bounded`

## Core Planning Result

- Prefer Dexter for `upstream_opportunity_capture`
- Prefer Dexter for `low_slippage_entry`
- Prefer Mew-X for `drawdown_containment` and local-peak retention
- Prefer Dexter for `realized_exit_capture`
- Prefer Dexter for `stale_risk_avoidance`
- If one source must anchor execution planning now, choose Dexter

## Hybrid Guidance

- Supported: selective adoption or objective-conditioned portfolio split
- Unsupported: in-run source fusion, threshold transplant, or unproven additive claims

## What Not To Redo

- Do not reopen promoted-baseline selection.
- Do not recollect live or replay evidence.
- Do not change Dexter, Mew-X, or validator rules.
- Do not widen replay fidelity into full path equivalence.
- Do not turn Mew-X local-retention strength into a universal winner claim.

## Recommended Next Step

- Continue with `execution_planning` as the next task.
- Carry forward `strategy_plan_ready` as the current planning conclusion.
- Preserve `strategy_plan_bounded` until a separate task explicitly needs stronger path-sensitive retention scope.
