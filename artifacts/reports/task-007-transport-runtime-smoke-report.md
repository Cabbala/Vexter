# TASK-007-TRANSPORT-RUNTIME-SMOKE

## Scope

This task starts from merged PR `#44` and the completed `TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-IMPLEMENTATION` lane. It keeps the promoted comparison baseline frozen and asks one bounded question:

- Does the implemented handle-based transport now hold up under a runtime-like smoke that exercises `prepare/start/status/stop/snapshot`, duplicate command idempotency, poll-first reconciliation, normalized transport failure handling, and reverse-order rollback stop fanout without changing Dexter or Mew-X source logic?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source-logic changes
- no validator-rule changes
- no comparison-baseline reopen
- no external wire, subprocess, or autoscaling finalization
- only runtime smoke tests, task artifacts, and the refreshed handoff bundle required to prove the implemented transport behaves coherently end to end

## Verified GitHub State

- Latest merged Vexter `main`: PR `#44`, main commit `ae1dd7ddc3ffbae893887baf042ea5e5d53bc5f3`, merged at `2026-03-26T11:00:22Z`
- Supporting merged Vexter states: PR `#43` `64ffe4a58dd9ff9e5ef707d77b59f392da9e02e0`; PR `#42` `23e6f354bf261935639941d541227b0c3f7a8435`; PR `#41` `0b174515c9c0deb04b70fd38c2c2882736a22273`; PR `#40` `a4e7a3c74460dc711c3e2897ac31386272e91c27`; PR `#39` `a293d6e9260bd092297140bc82469802d6fce115`; PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`; PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior implementation source of truth: `artifacts/reports/task-007-planner-router-executor-transport-implementation-report.md`
- Prior implementation proof: `artifacts/proofs/task-007-planner-router-executor-transport-implementation-check.json`
- Current inherited implementation conclusion: `planner_router_executor_transport_implemented`
- Current inherited claim boundary: `executor_transport_implementation_bounded`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from comparison closeout through transport implementation:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- no mid-trade handoff, threshold transplant, trust-logic transplant, or fused-engine claim

## What Landed

### Runtime smoke coverage

Committed transport runtime smoke now lives at `tests/test_planner_router_transport_runtime_smoke.py` and stays on the implemented transport surface plus the public `plan_request()` / `plan_and_dispatch()` entrypoints.

The new smoke covers:

- handle-based runtime progression across `prepare/start/status/stop/snapshot` while keeping Dexter `paper_live` + `monitor_mint_session` and Mew-X `sim_live` + `start_session` / `sim_session` source-faithful
- duplicate `prepare/start/stop` handling that stays idempotent while preserving a stable `handle_id` and visible duplicate ack metadata
- poll-first reconciliation that accepts push promotion over a running poll, then confirms stop via `status()` followed by `snapshot()` fallback
- transport-originated `status_timeout` normalization into failed `StatusSnapshot` detail with rollback confirmation still attached
- reverse-order rollback stop fanout when Mew-X runtime status times out after Dexter has already entered runtime, proving active handles stop in reverse batch order

### Behavior now evidenced

- `prepare` remains the only full-plan command, and all later runtime calls address the same stable handle identity.
- Dexter still stays on the bounded `paper_live` seam and Mew-X still stays on the bounded `sim_live` seam; this smoke does not reopen source selection or source logic.
- duplicate transport commands stay runtime-safe rather than replaying a second prepare, second start, or second stop.
- poll-first reconciliation remains the primary runtime view, but push data can still be promoted when it is the latest valid monotonic state.
- stop confirmation is bounded but real: a non-terminal poll falls back to `snapshot()` before rollback is treated as confirmed.
- transport errors normalize into planner/router failure detail rather than leaking raw adapter exceptions into the status stream.

### What did not change

- No Dexter source behavior changed.
- No Mew-X source behavior changed.
- No validator rules changed.
- No comparison evidence was recollected.
- No external transport wire, process topology, heartbeat cadence, or retry budget was finalized.

## Tests

Planner/router transport coverage now includes:

- `tests/test_planner_router_executor_transport_implementation.py`
- `tests/test_planner_router_transport.py`
- `tests/test_planner_router_transport_runtime_smoke.py`
- `tests/test_planner_router_livepaper_smoke.py`
- `tests/test_planner_router_runtime_smoke.py`
- `tests/test_planner_router_integration_smoke.py`
- `tests/test_planner_router_dispatch_state_machine.py`
- `tests/test_planner_router_executor_transport_spec_contract.py`

Validation run on this branch:

- `pytest -q`
- `78 passed`

## Recommendation Among Next Tasks

### `transport_livepaper_smoke`

Recommended next because:

- the implemented transport is now runtime-smoked in memory, so the next sharp residual risk is whether that same transport surface stays coherent when exercised through the already-approved live-paper seams
- this lane removed uncertainty around handle lifecycle, failure normalization, and rollback semantics, which are exactly the prerequisites for a transport-shaped live-paper smoke
- observability should attach after the transport/livepaper seam is proven, not before

### `livepaper_observability_spec`

Not next because:

- the system still benefits more from one more bounded behavioral proof than from describing telemetry on an un-smoked livepaper transport seam
- handle ids, ack states, reconciliation outcomes, and rollback confirmations already exist and can be specified more sharply after transport livepaper smoke

### `executor_boundary_code_spec`

Not next because:

- the boundary was already fixed in earlier interface/spec lanes and did not reopen during runtime smoke
- this smoke found no new interface ambiguity that would justify another boundary-only spec pass

## Decision

- Outcome: `A`
- Key finding: `executor_transport_runtime_smoke_passed`
- Claim boundary: `transport_runtime_smoke_bounded`
- Decision: `transport_livepaper_smoke_ready`
- Recommended next step: `transport_livepaper_smoke`
