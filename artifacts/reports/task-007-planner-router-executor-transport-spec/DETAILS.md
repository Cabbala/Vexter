# TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-SPEC Package

## Verified GitHub State

- Vexter latest merged `main`: PR `#42`, `23e6f354bf261935639941d541227b0c3f7a8435`
- Supporting Vexter states: PR `#41` `0b174515c9c0deb04b70fd38c2c2882736a22273`; PR `#40` `a4e7a3c74460dc711c3e2897ac31386272e91c27`; PR `#39` `a293d6e9260bd092297140bc82469802d6fce115`; PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`; PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Package Does

- Reuses the fixed planner/router control plane, runtime smoke, monitor/killswitch contract, and live-paper smoke without reopening comparison work
- Fixes transport ownership across `PlanStore`, `ExecutorRegistry`, `ExecutorAdapter`, and `StatusSink`
- Fixes one bounded process model, request/response envelope, idempotency, ack/failure propagation, stop confirmation, and poll-first status reconciliation contract
- Leaves wire choice, auth, host placement, and numeric timing constants deferred

## Key Finding

- `executor_transport_contract_fixed`

## Claim Boundary

- `executor_transport_spec_bounded`

## Core Result

- planner/router owns immutable plan persistence, adapter selection, retries, normalized failures, quarantine, and halt fanout
- executor runtimes own source-native session startup, handle lifetime, dedupe, source-local stop behavior, and terminal confirmation
- `prepare` is the only full-plan command and returns the stable `handle_id` boundary
- `start`, `status`, `stop`, and `snapshot` remain the only runtime transport phases
- polling is the first correctness path, while push remains optional and must reconcile back to `StatusSnapshot`
- reverse-order stop fanout and no cross-source handoff remain fixed

## What Not To Redo

- Do not reopen promoted-baseline selection.
- Do not recollect live or replay evidence.
- Do not change Dexter, Mew-X, or validator rules.
- Do not finalize wire protocol, auth, host placement, or numeric timeout/retry/poll constants in this task.
- Do not introduce funded-live execution, cross-source handoff, threshold transplant, or trust-logic transplant claims.

## Recommended Next Step

- Continue with `planner_router_executor_transport_implementation` as the next task.
- Carry forward `executor_transport_contract_fixed` as the current evidence conclusion.
- Preserve `executor_transport_spec_bounded` while wire choice and numeric timing details remain deferred.
