# TASK-007-PLANNER-ROUTER-INTERFACE-SPEC

## Scope

This task starts from merged PR `#34` and the completed `TASK-007-IMPLEMENTATION-PLANNING` lane. It keeps the promoted comparison baseline frozen and asks one bounded implementation question:

- Given the fixed implementation-planning surface, what planner/router interface contract can be fixed now without reopening comparison work or changing frozen source logic?

The task stays intentionally narrow:

- no new evidence collection
- no validator or source changes
- no baseline reopen
- no threshold transplant
- only minimal reaggregation of already committed comparison, strategy, execution, and implementation-planning outputs visible on GitHub

## Verified GitHub State

- Latest merged Vexter `main`: PR `#34`, merge commit `981f0977788cffd10de4bf78f14e5b430fbce4c1`, merged at `2026-03-26T00:39:22Z`
- Supporting merged Vexter states: PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Implementation-planning source of truth: `artifacts/reports/task-007-implementation-planning-report.md`
- Execution-planning source of truth: `artifacts/reports/task-007-execution-planning-report.md`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from closeout through implementation planning:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- route unit: `objective_profile_bound_sleeve_selected_pre_run`
- supported routing scope: `objective_conditioned_route_selection_or_portfolio_split`
- unsupported routing scope: `mid_trade_handoff`, threshold transplant, trust-logic transplant, fused-engine superiority claims
- replay parity remains bounded to close-summary / `position_closed` realized-return fidelity

## Planner/Router Interface Contract

### Immutable plan object

The first implementation contract should be one immutable `execution_plan` record emitted before any executor starts.

Required top-level fields:

- `plan_id`
- `created_at_utc`
- `objective_profile_id`
- `route`
- `sleeve_binding`
- `budget_binding`
- `monitor_binding`
- `executor_binding`
- `source_pin`
- `invariants`

Minimum shape:

```json
{
  "plan_id": "uuid-or-monotonic-id",
  "created_at_utc": "RFC3339 timestamp",
  "objective_profile_id": "mixed_default",
  "route": {
    "mode": "single_sleeve",
    "selected_sleeve_id": "dexter_default",
    "selected_source": "dexter"
  },
  "sleeve_binding": {
    "sleeve_id": "dexter_default",
    "source": "dexter",
    "budget_mode": "single_anchor_default"
  },
  "budget_binding": {
    "portfolio_budget_id": "main",
    "policy": "single_anchor_default",
    "sleeve_share": "100%",
    "explicit_cap_required": false
  },
  "monitor_binding": {
    "monitor_profile_id": "dexter_default",
    "quarantine_scope": "sleeve",
    "global_halt_participation": true
  },
  "executor_binding": {
    "executor_profile_id": "dexter_main_pinned",
    "source": "dexter",
    "pinned_commit": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
  },
  "source_pin": {
    "dexter": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    "mewx": "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
  },
  "invariants": [
    "route_is_pre_run_and_single_source",
    "bindings_are_fully_resolved_before_start",
    "no_mid_trade_handoff"
  ]
}
```

Plan invariants fixed now:

- exactly one selected sleeve and one selected source per plan
- `route.selected_source == sleeve_binding.source == executor_binding.source`
- budget, monitor, and executor bindings must be fully resolved before execution leaves `planned`
- pinned commit must match the selected executor profile and frozen source reference
- once emitted, a plan cannot mutate route, sleeve, budget, monitor, or executor binding in place

### Objective profile contract

Every objective profile must resolve routing and bindings before planning emits an immutable plan.

Required objective-profile fields:

- `objective_profile_id`
- `preferred_source`
- `allowed_sleeves`
- `budget_policy`
- `monitor_profile_id`
- `executor_profile_id`

Resolution rules fixed now:

- every profile resolves to exactly one preferred source
- mixed or unspecified objectives resolve to Dexter
- `mixed_default` resolves to `dexter_default`
- `containment_first` resolves to `mewx_containment`
- any Mew-X profile must explicitly accept timeout-shaped lifecycle behavior
- objective profiles may not authorize multi-source sleeves or in-run source fusion

### Sleeve binding contract

The route unit remains a sleeve selected before execution starts.

Required sleeve-binding fields:

- `sleeve_id`
- `source`
- `enabled`
- `budget_mode`
- `executor_profile_id`

Supported sleeves fixed now:

- `dexter_default`: default execution anchor for mixed, capture-first, low-slippage, realized-exit, and stale-risk-sensitive objectives
- `mewx_containment`: explicit containment-first sleeve for drawdown containment, fast post-attempt fill, and local-peak retention where timeout-shaped lifecycle behavior is acceptable

Sleeve-binding invariants:

- one plan may bind exactly one sleeve
- a sleeve may bind to exactly one source
- no plan may rebind from `dexter_default` to `mewx_containment` after start
- Mew-X sleeve enablement is always explicit and never implied by mixed objectives

### Budget binding and portfolio split contract

Budget policy is part of the immutable plan rather than a later runtime guess.

Required budget-binding fields:

- `portfolio_budget_id`
- `policy`
- `sleeve_share`
- `explicit_cap_required`

Supported policies fixed now:

- `single_anchor_default`: Dexter `100%`, Mew-X `0%`
- `selective_overlay`: Dexter primary share plus an explicitly capped Mew-X minority sleeve
- `dedicated_containment_template`: Mew-X `100%` in a fully separate containment-first template

Budget invariants:

- all budget declarations are sleeve-scoped
- any Mew-X share is explicit, never implicit
- mixed or unspecified objectives cannot emit a nonzero Mew-X budget by default
- no budget policy may imply dynamic cross-sleeve rebalance inside one immutable plan

Not fixed now:

- exact numeric Mew-X overlay caps
- leverage and drawdown numbers inside each sleeve allocator
- adaptive rebalance after start

### Monitor profile binding contract

Monitor profiles are bound by reference inside the immutable plan. This task fixes the binding surface, not the numeric thresholds.

Required monitor-binding fields:

- `monitor_profile_id`
- `admission_gate_class`
- `timeout_envelope_class`
- `quarantine_scope`
- `global_halt_participation`

Binding rules fixed now:

- every plan binds exactly one monitor profile
- `dexter_default` binds lifecycle-control monitoring
- `mewx_timeout_guard` binds timeout-aware monitoring for the containment sleeve
- admission gates can block planning on config invalidity, pin mismatch, disabled sleeve, budget overflow, or active global halt
- quarantine remains sleeve-scoped
- global halt freezes new planning and dispatches source-native stop requests only

Mew-X timeout boundary fixed now:

- a normal `inactivity_timeout` close reason is source-native and not an automatic incident
- quarantine triggers only when the session outlives the configured timeout envelope or fails to emit normalized close or shutdown confirmation
- Mew-X quarantine must not transfer the position to Dexter

Not fixed now:

- heartbeat numbers
- retry counts
- timeout durations

### Executor profile binding and handoff boundary

Executor binding is fixed at the interface level even though transport remains open.

Required executor-binding fields:

- `executor_profile_id`
- `source`
- `pinned_commit`
- `methods`
- `normalized_statuses`

Expected executor methods:

- `prepare`
- `start`
- `status`
- `stop`
- `snapshot`

Normalized statuses:

- `planned`
- `starting`
- `running`
- `quarantined`
- `stopping`
- `stopped`
- `failed`

Ownership split fixed now:

- planner/router owns route choice, sleeve selection, budget binding, monitor binding, executor binding, and kill-switch dispatch
- executors own source-native startup, lifecycle, threshold use, trust logic, and stop semantics

Not fixed now:

- subprocess versus service transport
- process supervisor shape
- runtime IPC details

### Planner/router responsibilities

Planner/router must:

- validate objective profile, sleeve config, source pins, and budget policy before start
- resolve one source and one sleeve before execution starts
- emit one immutable `execution_plan` per selected sleeve
- launch exactly one source-matched executor per plan
- interpret normalized statuses into sleeve quarantine or global halt actions

Planner/router must not:

- rewrite source thresholds or trust logic
- compare live source internals inside one position lifecycle
- hand open positions between Dexter and Mew-X
- claim that a fused engine is already validated

### Unsupported patterns

Unsupported now:

- mid-trade handoff from Dexter to Mew-X or the reverse
- multi-source sleeves
- threshold transplant
- trust-logic transplant
- implicit Mew-X budget for mixed objectives
- fused-engine superiority claims
- widening replay fidelity into full path equivalence

## Recommended Next Spec

### `concrete_planner_router_implementation_spec`

Recommended first because:

- the immutable plan schema, route invariants, and binding references are now fixed strongly enough to implement planner-side validation and plan emission directly
- executor boundary is already fixed at the contract level, so implementation can focus on config loading, route resolution, immutable plan construction, and dispatch orchestration
- monitor thresholds can attach to the shared plan and status surface afterward without creating a parallel contract

### `monitor_kill_switch_spec`

Not first because:

- numeric timeout and quarantine thresholds are still implementation defaults rather than evidence decisions
- the monitoring spec should attach to the concrete planner lifecycle and plan registry rather than define that lifecycle indirectly

### `executor_boundary_spec`

Not first because:

- the source-faithful boundary is already fixed here through methods, statuses, source pins, and ownership split
- what remains open is transport and process model, which is implementation-local rather than the next evidence-bound spec cut

## Decision

- Outcome: `A`
- Key finding: `planner_router_spec_ready`
- Claim boundary: `planner_router_spec_bounded`
- Current task status: `planner_router_spec_ready`
- Recommended next step: `concrete_planner_router_implementation_spec`
- Decision: `next_spec_ready`
