# TASK-007-PLANNER-ROUTER-INTEGRATION-SMOKE

## Scope

This task starts from merged PR `#38` and the completed `TASK-007-PLANNER-ROUTER-CODE-IMPLEMENTATION` lane. It keeps the promoted comparison baseline frozen and asks one bounded question:

- Given the already-implemented planner/router control plane, do the public `plan_request()` and `plan_and_dispatch()` paths stay wired end to end, fail closed on invalid inputs, and roll back safely on partial dispatch failure?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source-logic changes
- no validator-rule changes
- no comparison-baseline reopen
- no numeric monitor-threshold finalization
- no executor-transport or process-model redesign
- only integration smoke tests, task artifacts, and the refreshed handoff bundle required to prove the control-plane path is live

## Verified GitHub State

- Latest merged Vexter `main`: PR `#38`, main commit `b1ceac48af931db0571a25ea197b1e4e5df52543`, merged at `2026-03-26T02:10:03Z`
- Supporting merged Vexter states: PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior implementation source of truth: `artifacts/reports/task-007-planner-router-code-implementation-report.md`
- Prior implementation proof: `artifacts/proofs/task-007-planner-router-code-implementation-check.json`
- Current inherited implementation conclusion: `planner_router_code_implemented`
- Current inherited claim boundary: `implementation_bounded`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from comparison closeout through implementation:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- no mid-trade handoff, threshold transplant, or fused-engine claim

## What Landed

### Integration smoke coverage

Committed integration smoke now lives at `tests/test_planner_router_integration_smoke.py` and exercises the public planner/router entrypoints rather than the lower-level helper functions in isolation.

The new smoke covers:

- `plan_request()` from committed repo config through config load, objective resolution, sleeve selection, budget binding, immutable plan emission, and atomic plan-store write on the default Dexter path
- `plan_and_dispatch()` on the explicit overlay path with committed config plus smoke-only enablement of `mewx_containment`, proving store -> prepare -> start -> status sequencing across Dexter primary plus Mew-X overlay
- fail-closed rejection for invalid objective id, invalid objective-profile contract, pin mismatch, and missing cross-reference, all without leaving a partial batch in the plan store
- rollback behavior for both partial prepare failure and partial start failure, including reverse-order stop-all rollback across the prepared handles

### Behavior now evidenced

- Config loading is wired to the public planner entrypoint and still fails closed on pin mismatch or broken cross-reference before any `PlanBatch` is stored.
- Objective resolution remains explicit: omitted intent resolves to `mixed_default`, while invalid objective or invalid profile contract is rejected before emission.
- Sleeve selection and budget binding are visible at the entrypoint boundary, including the explicit Mew-X overlay `20%` cap-bound slice via `mewx_overlay_minor_cap`.
- Immutable `ExecutionPlan` records are emitted before dispatch and remain frozen once returned from `plan_request()`.
- `plan_and_dispatch()` stores the batch first, then prepares all plans, then starts them in declaration order, and stop-all rollback still triggers on partial prepare or start failure.

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

Validation run on this branch:

- `pytest -q`
- `49 passed`

## Recommendation Among Next Tasks

### `planner_router_runtime_smoke`

Recommended next because:

- the control-plane path is now proven at the public entrypoint boundary rather than only in lower-level unit seams
- the next remaining unknown is the bounded runtime seam around the abstract executor adapters, status normalization, and source-faithful dry execution harness
- runtime smoke advances the code path without reopening comparison or prematurely hard-freezing monitor numerics

### `monitor_killswitch_spec`

Not next because:

- immutable plan emission already carries monitor bindings end to end
- integration smoke shows those bindings survive entrypoint orchestration, so the remaining work is numeric and escalation-policy detail rather than a wiring blocker

### `executor_boundary_spec`

Not next because:

- the adapter and registry seams remain intact and source-faithful
- integration smoke reduces the highest current uncertainty to runtime behavior at those seams, making a bounded runtime smoke more informative than another contract-only pass

## Decision

- Outcome: `A`
- Key finding: `planner_router_integration_smoke_passed`
- Claim boundary: `integration_smoke_bounded`
- Decision: `runtime_smoke_ready`
- Recommended next step: `planner_router_runtime_smoke`

