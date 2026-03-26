# TASK-007-PLANNER-ROUTER-RUNTIME-SMOKE

## Scope

This task starts from merged PR `#39` and the completed `TASK-007-PLANNER-ROUTER-INTEGRATION-SMOKE` lane. It keeps the promoted comparison baseline frozen and asks one bounded question:

- Given the already-implemented planner/router control plane, do the public `plan_request()` and `plan_and_dispatch()` paths stay source-faithful when the runtime seam is exercised through bounded status progression, typed quarantine/stop signaling, and rollback completion?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source-logic changes
- no validator-rule changes
- no comparison-baseline reopen
- no monitor numeric-threshold finalization
- no executor-transport or process-model redesign
- only runtime smoke tests, task artifacts, and the refreshed handoff bundle required to prove the runtime-side seam is live

## Verified GitHub State

- Latest merged Vexter `main`: PR `#39`, main commit `a293d6e9260bd092297140bc82469802d6fce115`, merged at `2026-03-26T02:28:37Z`
- Supporting merged Vexter states: PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`; PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior implementation source of truth: `artifacts/reports/task-007-planner-router-integration-smoke-report.md`
- Prior implementation proof: `artifacts/proofs/task-007-planner-router-integration-smoke-check.json`
- Current inherited implementation conclusion: `planner_router_integration_smoke_passed`
- Current inherited claim boundary: `integration_smoke_bounded`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from comparison closeout through integration smoke:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- no mid-trade handoff, threshold transplant, or fused-engine claim

## What Landed

### Runtime smoke coverage

Committed runtime smoke now lives at `tests/test_planner_router_runtime_smoke.py` and stays on the public planner/router entrypoints plus the already-coded status-normalization helpers.

The new smoke covers:

- `plan_request()` from committed repo config through atomic batch store and into a runtime-like single-plan path that proves `planned -> starting -> running -> quarantined -> stopping -> stopped`
- typed runtime follow-up payloads that keep quarantine and stop semantics expressed as adapter-facing signal detail rather than planner-owned transport logic
- `plan_and_dispatch()` on the explicit Dexter-plus-Mew-X overlay path with an invalid runtime transition (`starting -> stopped`) on the Mew-X leg, proving typed failure snapshots plus reverse-order stop-all rollback completion
- store ordering that remains bounded to pre-runtime batch emission, with runtime-side progress and rollback expressed through `StatusSnapshot` detail and adapter stop reasons

### Behavior now evidenced

- `plan_request()` still emits and stores immutable `ExecutionPlan` records before any runtime interaction; the stored batch remains `planned` even while runtime-side signals progress through normalized snapshots.
- The shortest bounded runtime path is now evidenced as `planned -> starting -> running -> quarantined -> stopping -> stopped` without inserting monitor numerics or transport ownership into planner code.
- Quarantine and stop remain typed seam outputs: the smoke keeps `signal_type`, scope/mode, and completion fields in runtime detail instead of reopening source logic.
- `plan_and_dispatch()` still fails closed when a source reports an illegal normalized transition, emitting `invalid_status_transition` failures and completing reverse-order stop-all rollback.

### What did not change

- No Dexter source behavior changed.
- No Mew-X source behavior changed.
- No validator rules changed.
- No comparison evidence was recollected.
- No monitor numeric policy or executor transport ownership was finalized.

### Tests

Planner/router coverage now includes:

- `tests/test_planner_router_config_loader.py`
- `tests/test_planner_router_objective_resolver.py`
- `tests/test_planner_router_plan_emitter.py`
- `tests/test_planner_router_dispatch_state_machine.py`
- `tests/test_planner_router_integration_smoke.py`
- `tests/test_planner_router_runtime_smoke.py`

Validation run on this branch:

- `pytest -q`
- `51 passed`

## Recommendation Among Next Tasks

### `monitor_killswitch_spec`

Recommended next because:

- runtime smoke now proves the bounded lifecycle and rollback path, so the next unresolved question is how monitor-driven quarantine should escalate or halt
- killswitch policy can now be specified against a fixed runtime seam instead of speculative control-plane behavior
- live-paper smoke should inherit those monitor rules rather than guess them

### `executor_boundary_spec`

Not next because:

- the abstract adapter and registry seams remained source-faithful through both integration and runtime smoke
- another boundary-only pass would restate a contract that is now already runtime-smoked

### `planner_router_livepaper_smoke`

Not next because:

- runtime smoke cleared the wiring question, but live-paper still depends on explicit monitor/killswitch policy and escalation boundaries
- moving directly to live-paper would force policy assumptions that are still intentionally deferred

## Decision

- Outcome: `A`
- Key finding: `planner_router_runtime_smoke_passed`
- Claim boundary: `runtime_smoke_bounded`
- Decision: `monitor_killswitch_spec_ready`
- Recommended next step: `monitor_killswitch_spec`
