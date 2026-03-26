# TASK-007-IMPLEMENTATION-PLANNING Package

## Verified GitHub State

- Vexter latest merged `main`: PR `#33`, `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`
- Supporting Vexter states: PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Package Does

- Reuses the fixed execution-planning conclusion rather than reopening comparison work
- Converts Dexter-default / Mew-X-selective execution guidance into implementation-ready planner/router, sleeve, and executor boundaries
- Fixes what the first config and route contract must contain
- Narrows what still remains implementation-default work rather than evidence-fixed design

## Key Finding

- `implementation_plan_ready`

## Claim Boundary

- `implementation_plan_bounded`

## Core Implementation Result

- Route by sleeve or template before execution starts
- Keep Dexter as the default execution anchor
- Keep Mew-X as an explicit containment-first selective sleeve only
- Bind routing, budget, monitor profile, and executor profile into one immutable plan object
- Keep monitoring layered as planner gates, sleeve quarantine, and global halt
- Keep source-native lifecycle ownership inside each executor

## What Not To Redo

- Do not reopen promoted-baseline selection.
- Do not recollect live or replay evidence.
- Do not change Dexter, Mew-X, or validator rules.
- Do not claim source fusion, threshold transplant, or full path equivalence.
- Do not convert timeout-shaped Mew-X behavior into a generic default or failover story.

## Recommended Next Step

- Continue with `planner_router_interface_spec` as the next task.
- Carry forward `implementation_plan_ready` as the current implementation-level conclusion.
- Preserve `implementation_plan_bounded` until a later spec fixes numeric budget caps and monitor thresholds.
