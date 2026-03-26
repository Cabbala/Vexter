# TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-IMPLEMENTATION

## Scope

This task starts from merged PR `#43` and the completed `TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-SPEC` lane. It keeps the promoted comparison baseline frozen and asks one bounded implementation question:

- Can the fixed executor transport contract now be landed as working Vexter code without changing Dexter or Mew-X source logic, reopening comparison work, or inventing a new runtime/process model?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source-logic changes
- no validator-rule changes
- no comparison-baseline reopen
- no funded live trading
- no external wire, autoscaling, or numeric timing finalization
- only the bounded transport implementation needed to move beyond stub-only executor seams

## Verified GitHub State

- Latest merged Vexter `main`: PR `#43`, main commit `64ffe4a58dd9ff9e5ef707d77b59f392da9e02e0`, merged at `2026-03-26T03:48:25Z`
- Supporting merged Vexter states: PR `#42` `23e6f354bf261935639941d541227b0c3f7a8435`; PR `#41` `0b174515c9c0deb04b70fd38c2c2882736a22273`; PR `#40` `a4e7a3c74460dc711c3e2897ac31386272e91c27`; PR `#39` `a293d6e9260bd092297140bc82469802d6fce115`; PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`; PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## What Landed

### Concrete transport module

`vexter/planner_router/transport.py` now provides a bounded implementation of the fixed transport contract:

- `TransportEnvelope`, `TransportMessageType`, and `AckState`
- idempotency-key helpers for `prepare/start/stop/status/snapshot`
- source-faithful `SourceTransportSpec` for Dexter `paper_live` + `monitor_mint_session` and Mew-X `sim_live` + `start_session` / `sim_session`
- `InMemoryPlanStore` and `ReconcilingStatusSink` as separate planner-owned persistence and runtime fan-in surfaces
- `SourceFaithfulTransportAdapter` plus `TransportExecutorRegistry` and a builder for pinned Dexter/Mew-X registries

The implementation keeps the public protocol surface unchanged and lands all new behavior behind `PlanStore`, `ExecutorAdapter`, `ExecutorRegistry`, and `StatusSink`.

### Handle lifecycle and idempotency

The adapter now owns a concrete bounded handle lifecycle:

- `prepare(plan)` is the only full-plan command and returns a `DispatchHandle.native_handle` ack payload
- `handle_id` is stable and reused on duplicate `prepare`
- duplicate `start` does not create a second native session
- duplicate `stop` does not trigger a second shutdown
- stop reasons stay in the planner namespace and remain visible through the transport surface

### Stop confirmation and reconciliation

`dispatch_state_machine.py` now uses the implemented transport more faithfully:

- transport-originated `PlannerRouterError.failure` detail survives through dispatch failure handling
- rollback stop fanout still runs in reverse batch order
- stop completion now checks `status()` first and falls back to `snapshot()` before treating shutdown as confirmed
- lack of terminal confirmation maps to `shutdown_unconfirmed`
- start and status failures are normalized separately so post-start status silence can map through `status_timeout`

### What remains deferred

- any external subprocess or service transport
- autoscaling, cross-host failover, or planner-managed worker trees
- push-driven correctness as the sole status path
- numeric timing constants, heartbeat cadences, retry budgets, and funded live transport

## Tests

Validation on this branch covered:

- `tests/test_planner_router_executor_transport_implementation.py`
- `tests/test_planner_router_transport.py`
- `tests/test_planner_router_dispatch_state_machine.py`
- `tests/test_planner_router_integration_smoke.py`
- `tests/test_planner_router_runtime_smoke.py`
- `tests/test_planner_router_livepaper_smoke.py`
- `tests/test_planner_router_executor_transport_spec_contract.py`
- `tests/test_bootstrap_layout.py`

The implementation-specific coverage now checks:

- prepare handle envelope fields
- idempotent duplicate `prepare/start/stop`
- pin-mismatch propagation
- stop confirmation through `status()` then `snapshot()`
- poll-first reconciliation behavior
- registry and sink separation from plan persistence

Full repo validation landed at `pytest -q` -> `74 passed`.

## Recommendation Among Next Tasks

### `transport_runtime_smoke`

Recommended next because:

- the transport contract is now implemented but still bounded to in-memory adapter-owned runtimes
- a runtime-shaped smoke is the shortest next proof that `prepare/start/status/stop/snapshot` stay correct end to end on the implemented surface
- observability will be sharper once runtime-shaped transport behavior is proven, not just coded

### `livepaper_observability_spec`

Not next because:

- the implementation still needs runtime-shaped proof before telemetry is the main residual risk
- handle ids, stop-confirmation paths, and normalized failures now exist and can be observed after runtime smoke rather than before it

### `executor_boundary_code_spec`

Not next because:

- the abstract boundary was already fixed in earlier TASK-007 lanes and in the executor transport spec
- this lane removed the concrete implementation gap rather than exposing a new interface ambiguity

## Decision

- Outcome: `A`
- Key finding: `executor_transport_bridge_implemented`
- Claim boundary: `executor_transport_implementation_bounded`
- Current task status: `planner_router_executor_transport_implemented`
- Recommended next step: `transport_runtime_smoke`
- Decision: `transport_runtime_smoke_ready`
