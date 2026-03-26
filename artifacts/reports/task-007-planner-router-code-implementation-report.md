# TASK-007-PLANNER-ROUTER-CODE-IMPLEMENTATION

## Scope

This task starts from merged PR `#37` and the completed `TASK-007-CONCRETE-PLANNER-ROUTER-CODE-SPEC` lane. It keeps the promoted comparison baseline frozen and asks one bounded implementation question:

- Given the fixed planner/router code spec, what first working source-faithful planner/router implementation can land now without reopening comparison work or changing frozen source logic?

The task stays intentionally narrow:

- no new evidence collection
- no validator or source changes
- no baseline reopen
- no numeric monitor-threshold fix
- no executor-transport or process-model fix
- only the planner-side code, config package, tests, and handoff artifacts required to make the code-spec executable

## Verified GitHub State

- Latest merged Vexter `main`: PR `#37`, main commit `786221a664637925f790e89af0448fa04832426e`, merged at `2026-03-26T01:43:05Z`
- Supporting merged Vexter states: PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Planner/router code-spec source of truth: `artifacts/reports/task-007-concrete-planner-router-code-spec-report.md`
- Concrete implementation source of truth: `artifacts/reports/task-007-concrete-planner-router-implementation-spec-report.md`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from closeout through the code spec:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- no mid-trade handoff, threshold transplant, or fused-engine claim

## What Landed

### Config package

Committed deterministic planner/router config now lives at `config/planner_router/`:

- `planner.json`
- `objective_profiles.json`
- `sleeves.json`
- `budget_policies.json`
- `monitor_profiles.json`
- `executor_profiles.json`

The default config keeps `mixed_default` on Dexter, carries explicit `containment_first` and `dexter_with_mewx_overlay` profiles, and preserves the source-faithful stance that Mew-X routing is explicit and bounded. The committed package leaves `mewx_containment` disabled by default, so explicit containment or overlay planning still requires config-level opt-in instead of silent fallback.

### Source implementation

The planner/router implementation now exists under `vexter/planner_router/`:

- `models.py`: frozen typed records for config, requests, resolved context, immutable plans, status snapshots, and failure payloads
- `errors.py`: exception hierarchy for load, validation, resolution, emission, and dispatch failures
- `interfaces.py`: `PlanStore`, `ExecutorAdapter`, `ExecutorRegistry`, and `StatusSink` protocols
- `config_loader.py`: deterministic JSON load, duplicate-id checks, cross-reference checks, and pin validation
- `objective_resolver.py`: omitted-objective defaulting, route-mode validation, and containment-only Mew-X resolution
- `sleeve_selector.py`: explicit sleeve selection with enablement and source-match enforcement
- `budget_binder.py`: sleeve-scoped share binding plus explicit-cap enforcement for nonzero Mew-X allocation
- `plan_emitter.py`: deterministic immutable `ExecutionPlan` creation and atomic `PlanBatch` emission
- `dispatch_state_machine.py`: `prepare`-then-`start` orchestration, normalized status validation, and stop-all rollback
- `planner.py`: public `plan_request()` and `plan_and_dispatch()` orchestration entrypoints

### Behavior fixed now

- Config loading fails closed on missing files, duplicate ids, cross-reference mismatches, and pin mismatches against Dexter `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` and Mew-X `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Omitted objective intent resolves to `mixed_default`, while explicit unknown objective ids are rejected.
- `portfolio_split` remains Dexter-primary only and keeps overlay sleeves explicit and separate.
- Any nonzero Mew-X allocation requires both explicit policy opt-in and a symbolic cap reference.
- Immutable plan emission binds route, sleeve, budget, monitor, executor, and source pins before the first executor start.
- Dispatch prepares every plan before any start, and partial prepare or start failure triggers stop-all rollback without reroute or cross-source handoff.

### Tests

Planner/router unit coverage now includes:

- `tests/test_planner_router_config_loader.py`
- `tests/test_planner_router_objective_resolver.py`
- `tests/test_planner_router_plan_emitter.py`
- `tests/test_planner_router_dispatch_state_machine.py`

The tests cover deterministic load/validation, objective defaulting and explicit rejection, immutable plan emission for single-sleeve and overlay batches, and rollback behavior on partial prepare or partial start failure.

Validation run on this branch:

- `pytest -q`
- `41 passed`

## Recommendation Among Next Tasks

### `planner_router_integration_smoke`

Recommended next because:

- the code-spec surface is now implemented, not just specified
- planner, config, and dispatch seams are already unit-tested and ready for one higher-level orchestration smoke across `plan_request()` / `plan_and_dispatch()`
- integration smoke can prove the control-plane wiring before monitor numbers or executor transport ownership are finalized

### `monitor_killswitch_spec`

Not next because:

- the implementation already isolates monitor bindings behind `MonitorProfileConfig` and `PlanStatus`
- the remaining work is primarily numeric and escalation-policy detail, not a blocker for confirming the code path exists end to end

### `executor_boundary_spec`

Not next because:

- executor transport is already isolated behind `ExecutorAdapter` and `ExecutorRegistry`
- a smoke-level control-plane check is the shorter path to confirm that transport remains safely deferred

## Decision

- Outcome: `A`
- Key finding: `planner_router_code_implemented`
- Claim boundary: `implementation_bounded`
- Decision: `integration_smoke_ready`
- Recommended next step: `planner_router_integration_smoke`
