# TASK-007-CONCRETE-PLANNER-ROUTER-IMPLEMENTATION-SPEC

## Scope

This task starts from merged PR `#35` and the completed `TASK-007-PLANNER-ROUTER-INTERFACE-SPEC` lane. It keeps the promoted comparison baseline frozen and asks one bounded implementation question:

- Given the fixed planner/router contract, what concrete planner-side implementation flow can be fixed now without reopening comparison work or changing frozen source logic?

The task stays intentionally narrow:

- no new evidence collection
- no validator or source changes
- no baseline reopen
- no threshold transplant
- only minimal reaggregation of already committed comparison, planning, and interface outputs visible on GitHub

## Verified GitHub State

- Latest merged Vexter `main`: PR `#35`, merge commit `2bec1badde788ef1c75251af2df17609643720fb`, merged at `2026-03-26T01:03:31Z`
- Supporting merged Vexter states: PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Planner/router interface source of truth: `artifacts/reports/task-007-planner-router-interface-spec-report.md`
- Implementation-planning source of truth: `artifacts/reports/task-007-implementation-planning-report.md`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from closeout through interface spec:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- supported routing scope: `objective_conditioned_route_selection_or_portfolio_split_using_separate_sleeves`
- unsupported routing scope: `mid_trade_handoff`, threshold transplant, trust-logic transplant, multi-source sleeves, fused-engine superiority claims
- immutable plan contract: one emitted plan binds route, sleeve, budget, monitor, executor, and source pin before start
- replay parity remains bounded to close-summary / `position_closed` realized-return fidelity rather than full path equivalence

## Concrete Planner/Router Implementation Spec

### Config package and loading sequence

The concrete planner/router config surface should be one deterministic package rooted at `config/planner_router/` with these files:

- `planner.json`
- `objective_profiles.json`
- `sleeves.json`
- `budget_policies.json`
- `monitor_profiles.json`
- `executor_profiles.json`

Required file responsibilities:

- `planner.json`: default objective profile, default execution anchor, allowed route modes, global halt policy
- `objective_profiles.json`: named routing intents that bind route mode, preferred source, primary sleeve, optional overlay sleeves, and budget policy
- `sleeves.json`: source-specific sleeve enable flags, sleeve ids, and executor-profile references
- `budget_policies.json`: per-policy sleeve shares, cap references, and explicit-cap requirements
- `monitor_profiles.json`: admission-gate class, timeout-envelope class, quarantine scope, and global-halt participation
- `executor_profiles.json`: source, pinned commit, method surface, and normalized status surface

Deterministic loading sequence:

1. Load `planner.json`.
2. Load registries in fixed order: `objective_profiles.json`, `sleeves.json`, `budget_policies.json`, `monitor_profiles.json`, `executor_profiles.json`.
3. Materialize the frozen source-pin registry from Dexter `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` and Mew-X `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
4. Apply run-request inputs: `plan_request_id`, optional `objective_profile_id`, and `portfolio_budget_id`.
5. Cross-validate references and emit one immutable `resolved_planning_context`.

Load-time invariants fixed now:

- missing config files fail closed
- duplicate ids fail closed
- no runtime override may mutate preferred source, allowed sleeves, pinned commit, budget policy, or monitor profile after load
- executor-profile pins must match the frozen source-pin registry before planning may continue

### Objective profile resolution algorithm

The planner resolves objective intent before any sleeve or budget binding.

Algorithm:

1. If `objective_profile_id` is absent, substitute `mixed_default`.
2. Look up the objective profile by id; reject on miss.
3. Validate that exactly one `preferred_source` is declared.
4. Validate `route_mode` as either `single_sleeve` or `portfolio_split`.
5. If `route_mode == single_sleeve`, require exactly one `primary_sleeve_id`.
6. If `route_mode == portfolio_split`, require Dexter as the preferred source, `dexter_default` as the primary sleeve, and only explicitly declared overlay sleeves.
7. If the profile selects Mew-X as the preferred source, require the profile to be explicitly containment-first and timeout-tolerant.
8. Resolve referenced budget, monitor, and executor registries into a `resolved_objective_profile`.

Resolution rules fixed now:

- omitted or unspecified objectives become `mixed_default`
- explicit but unknown objective ids are rejected, not silently downgraded
- mixed default resolves to Dexter
- explicit Mew-X routing is allowed only for containment-first objectives
- portfolio split may exist only as a declared separate-sleeve template, never as multi-source fusion inside one sleeve

### Sleeve selection algorithm

Sleeve selection consumes the resolved objective profile and returns one or more immutable single-source sleeve intents.

Algorithm:

1. Derive ordered candidate sleeves from the resolved objective profile.
2. For `single_sleeve`, candidate set is `[primary_sleeve_id]`.
3. For `portfolio_split`, candidate set is `[primary_sleeve_id] + overlay_sleeve_ids` in declaration order.
4. For each candidate sleeve:
   - load the sleeve record
   - require `enabled == true`
   - require `sleeve.source` to match the profile's allowed routing semantics
   - require the sleeve's executor profile source to match the sleeve source
5. Emit one ordered `selected_sleeve` record per validated candidate.

Selection rules fixed now:

- `mixed_default` selects `dexter_default` only
- explicit containment-first profiles select `mewx_containment` only
- portfolio split templates keep `dexter_default` as primary and may add `mewx_containment` only as an explicit overlay sleeve
- no silent fallback is allowed from explicit Mew-X selection to Dexter
- if any explicitly required sleeve is disabled, the request is rejected before plan emission

### Budget binding algorithm

Budget binding remains sleeve-scoped and explicit.

Algorithm:

1. Resolve the profile's `budget_policy_id`.
2. Resolve `portfolio_budget_id`, defaulting to `main`.
3. For each selected sleeve, derive one `budget_binding` record from the policy.
4. Require any nonzero Mew-X allocation to carry `explicit_cap_required == true` and a non-empty cap reference.
5. Verify that aggregate sleeve shares in the batch do not exceed `100%`.
6. Emit one immutable budget binding per plan.

Supported policy shapes fixed now:

- `single_anchor_default`: `dexter_default` gets `100%`, Mew-X gets `0%`
- `selective_overlay`: Dexter remains primary and Mew-X gets an explicit minority cap reference
- `dedicated_containment_template`: one Mew-X sleeve gets `100%` inside its own explicit containment template

Budget invariants fixed now:

- all budget declarations are sleeve-scoped
- any Mew-X share is explicit, never implicit
- mixed or unspecified objectives cannot emit nonzero Mew-X budget by default
- budget binding uses symbolic cap references; exact numeric caps remain outside this task
- no budget policy implies adaptive cross-sleeve rebalance after start

### Immutable plan emission flow

The planner emits immutable single-sleeve plans, optionally grouped into one batch when an explicit split template is selected.

Emission algorithm:

1. Build `selected_sleeves` and `budget_bindings` from the validated planning context.
2. Allocate one `plan_batch_id`.
3. For each selected sleeve, derive one immutable `execution_plan`.
4. Populate `execution_plan` with:
   - `plan_id`
   - `plan_batch_id`
   - `created_at_utc`
   - `objective_profile_id`
   - `route`
   - `sleeve_binding`
   - `budget_binding`
   - `monitor_binding`
   - `executor_binding`
   - `source_pin`
   - `invariants`
5. Set initial normalized status to `planned`.
6. Persist or publish the full batch atomically: either every plan is emitted or none are emitted.

Immutable invariants fixed now:

- one emitted plan binds exactly one sleeve and one source
- `route.selected_source == sleeve_binding.source == executor_binding.source`
- monitor and executor bindings are resolved before `planned`
- source pins are copied into the plan, not looked up dynamically after start
- after emission, only plan status may change; route and bindings never mutate in place

### Executor dispatch flow

Dispatch occurs only after immutable plan emission succeeds for the full batch.

Dispatch algorithm:

1. Take the emitted plan batch in declared order.
2. Call `prepare(plan)` for each plan before starting any executor.
3. If any `prepare` call fails:
   - issue `stop` for every prepared handle
   - mark the affected plans `failed`
   - abort the batch before `start`
4. If all `prepare` calls succeed, transition plans from `planned` to `starting`.
5. Call `start(handle)` in batch order.
6. Wait for normalized `running` or terminal failure per plan.
7. Accept only normalized status and snapshot updates from executors.

Dispatch invariants fixed now:

- prepare is the all-or-nothing boundary for a split batch
- start order is deterministic and follows emitted plan order
- planners never rewrite source thresholds or trust logic during dispatch
- quarantine or failure in one sleeve does not rebind another sleeve to a different source
- no open position may be handed from Mew-X to Dexter or from Dexter to Mew-X

### Normalized plan status lifecycle

Planner-internal resolution stages are not exposed as mutable plan states. The first externally visible plan state is `planned`.

Normalized lifecycle:

- `planned`: immutable plan emitted, not yet started
- `starting`: executor prepare/start accepted
- `running`: executor reports live source-native execution
- `quarantined`: planner/monitor disables new work for the sleeve because the lifecycle left the allowed envelope
- `stopping`: planner has issued source-native stop
- `stopped`: normalized close and shutdown confirmation received
- `failed`: terminal failure after emission

Lifecycle rules fixed now:

- planning-time validation failures reject the request before any plan reaches `planned`
- `failed` never triggers automatic reroute to the other source
- `quarantined` is sleeve-scoped unless the configured global halt policy escalates
- Mew-X `inactivity_timeout` is source-native behavior, not an automatic incident by itself

### Planner/router validation and failure semantics

Failure handling is split between pre-emission rejection and post-emission lifecycle failure.

Pre-emission rejection reasons:

- `config_missing`
- `duplicate_config_id`
- `unknown_objective_profile`
- `route_mode_invalid`
- `sleeve_disabled`
- `executor_source_mismatch`
- `pin_mismatch`
- `unknown_budget_policy`
- `mewx_cap_required`
- `budget_share_overflow`
- `global_halt_active`

Post-emission failure reasons:

- `prepare_failed`
- `start_failed`
- `status_timeout`
- `shutdown_unconfirmed`
- `invalid_status_transition`
- `source_stop_failed`

Failure semantics fixed now:

- no partial plan batch is emitted if any pre-emission validation fails
- no silent downgrade from explicit Mew-X intent to Dexter default
- no partial batch start is allowed after a failed `prepare`
- once a plan is emitted, terminal failure is represented as `failed` rather than mutable route rebinding

## Deferred Boundaries

Deferred intentionally to `monitor_killswitch_spec`:

- numeric timeout durations
- heartbeat cadence
- retry counts
- incident escalation thresholds

Deferred intentionally to `executor_boundary_spec`:

- subprocess versus service transport
- IPC payload framing
- process supervisor model
- runtime auth or secret injection mechanics

Deferred intentionally to `concrete_planner_router_code_spec`:

- module layout
- data-model names
- function and method signatures
- storage adapter boundaries
- unit/integration test matrix

## Recommended Next Spec

### `concrete_planner_router_code_spec`

Recommended first because:

- config loading, validation, route resolution, budget binding, plan emission, and dispatch order are now fixed strongly enough to map directly into modules and functions
- monitor thresholds can attach to the fixed plan registry and normalized lifecycle without blocking code-structure design
- executor transport remains bounded behind the already fixed `prepare/start/status/stop/snapshot` surface

### `monitor_killswitch_spec`

Not first because:

- numeric thresholds and retry values are still intentionally deferred
- the monitoring spec now has a stable plan registry and status lifecycle to target, so it no longer needs to lead

### `executor_boundary_spec`

Not first because:

- source ownership, pins, method surface, and normalized statuses are already fixed
- what remains open is transport and process model, which is implementation-local rather than the next blocking design surface

## Decision

- Outcome: `A`
- Key finding: `concrete_planner_router_spec_ready`
- Claim boundary: `concrete_spec_bounded`
- Current task status: `concrete_planner_router_spec_ready`
- Recommended next step: `concrete_planner_router_code_spec`
- Decision: `next_spec_ready`
