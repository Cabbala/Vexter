# TASK-007-EXECUTION-PLANNING Package

## Verified GitHub State

- Vexter latest merged `main`: PR `#32`, `a214ff04f0662e250b01181551a8963ce8e80dd6`
- Supporting Vexter states: PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Package Does

- Reuses the fixed strategy-planning conclusion rather than reopening comparison work
- Converts Dexter-default / Mew-X-selective strategy guidance into execution-level routing boundaries
- Fixes which execution assumptions can be carried into implementation planning
- Narrows what still remains implementation-scoped and what does not require a new evidence lane

## Key Finding

- `execution_plan_ready`

## Claim Boundary

- `execution_plan_bounded`

## Core Execution Result

- Use Dexter as the default execution anchor
- Use Mew-X only as a containment-first selective option
- Keep routing objective-conditioned and ex ante
- Support portfolio split or separate sleeves, not in-run source fusion
- Keep `path_sensitive_retention_scope` optional unless a later design explicitly needs stronger retention-equivalence claims

## What Not To Redo

- Do not reopen promoted-baseline selection.
- Do not recollect live or replay evidence.
- Do not change Dexter, Mew-X, or validator rules.
- Do not claim source fusion, threshold transplant, or full path equivalence.
- Do not use Mew-X timeout-shaped behavior as a reason to widen it into the default primary engine.

## Recommended Next Step

- Continue with `implementation_planning` as the next task.
- Carry forward `execution_plan_ready` as the current execution-level conclusion.
- Preserve `execution_plan_bounded` until a separate task explicitly needs stronger path-sensitive retention scope.

