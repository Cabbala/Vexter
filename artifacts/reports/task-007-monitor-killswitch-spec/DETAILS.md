# TASK-007-MONITOR-KILLSWITCH-SPEC Package

## Verified GitHub State

- Vexter latest merged `main`: PR `#40`, `a4e7a3c74460dc711c3e2897ac31386272e91c27`
- Supporting Vexter states: PR `#39` `a293d6e9260bd092297140bc82469802d6fce115`; PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`; PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Package Does

- Reuses the fixed planner/router control plane and bounded runtime-smoke seam instead of reopening comparison or rewriting source logic
- Fixes the monitor profile, admission gate, timeout envelope, quarantine scope, global halt, and typed failure-escalation contract
- Adds contract-level tests and a runtime invalid-transition regression without changing frozen source behavior
- Leaves numeric heartbeat, retry, timeout, and escalation thresholds deferred as bounded defaults

## Key Finding

- `monitor_killswitch_contract_fixed`

## Claim Boundary

- `monitor_killswitch_spec_bounded`

## Core Result

- monitor profiles remain immutable per-plan bindings with committed Dexter and Mew-X class tuples preserved
- admission gates stay pre-emission and fail closed on config invalidity, pin mismatch, disabled sleeve, budget overflow, or active global halt
- timeout envelopes stay source-shaped and explicitly accept Mew-X `inactivity_timeout` as source-native rather than an automatic incident
- quarantine remains sleeve-scoped, and global halt remains freeze-new-planning plus source-native stop requests only
- typed failure escalation stays on `FailureCode` / `FailureDetail` / `StatusSnapshot`, with source-native reasons carried as passthrough metadata

## What Not To Redo

- Do not reopen promoted-baseline selection.
- Do not recollect live or replay evidence.
- Do not change Dexter, Mew-X, or validator rules.
- Do not finalize numeric timeout, heartbeat, retry, or budget thresholds in this task.
- Do not introduce cross-source handoff, threshold transplant, or trust-logic transplant claims.

## Recommended Next Step

- Continue with `planner_router_livepaper_smoke` as the next task.
- Carry forward `monitor_killswitch_contract_fixed` as the current evidence conclusion.
- Preserve `monitor_killswitch_spec_bounded` while numeric thresholds remain deferred.
