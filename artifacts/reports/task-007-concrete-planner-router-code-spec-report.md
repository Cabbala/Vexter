# TASK-007-CONCRETE-PLANNER-ROUTER-CODE-SPEC

## Scope

This task starts from merged PR `#36` and the completed `TASK-007-CONCRETE-PLANNER-ROUTER-IMPLEMENTATION-SPEC` lane. It keeps the promoted comparison baseline frozen and asks one bounded implementation question:

- Given the fixed planner-side flow, what code-ready module, data-model, and function boundary can be fixed now without reopening comparison work or changing frozen source logic?

The task stays intentionally narrow:

- no new evidence collection
- no validator or source changes
- no baseline reopen
- no numeric monitor-threshold fix
- no executor-transport or process-model fix
- only minimal reaggregation of already committed planning outputs plus source-faithful mapping to the pinned Dexter and Mew-X entrypoints

## Verified GitHub State

- Latest merged Vexter `main`: PR `#36`, main commit `8713b9ba8de82accda48526fdff8732531d7b620`, merged at `2026-03-26T01:24:01Z`
- Supporting merged Vexter states: PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Concrete implementation source of truth: `artifacts/reports/task-007-concrete-planner-router-implementation-spec-report.md`
- Planner/router interface source of truth: `artifacts/reports/task-007-planner-router-interface-spec-report.md`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from closeout through the concrete implementation spec:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- config package order: `planner`, `objective_profiles`, `sleeves`, `budget_policies`, `monitor_profiles`, `executor_profiles`
- immutable plan contract: one emitted plan binds one sleeve, one source, one executor profile, and one source pin before start
- dispatch contract: `prepare` all plans before any `start`
- unsupported scope: mid-trade handoff, threshold transplant, trust-logic transplant, multi-source sleeves, fused-engine superiority claims

## Source-Faithful Anchors

The code-spec boundary is tied to the frozen source surfaces already assessed:

- Dexter config source: `sources/Dexter/settings.py`
- Dexter runtime and session hooks: `sources/Dexter/Dexter.py`
  - `_settings_snapshot`
  - `_reserve_buy_spend`
  - `_release_buy_spend`
  - `_finalize_buy_spend`
  - `set_trust_level`
  - `buy`
  - `sell`
  - `monitor_mint_session`
- Dexter normalized event surface: `sources/Dexter/DexLab/instrumentation.py`
- Mew-X config source: `sources/Mew-X/src/mew/config.rs`
- Mew-X runtime wiring: `sources/Mew-X/src/main.rs`
- Mew-X session and execution hooks: `sources/Mew-X/src/mew/snipe/handler.rs`
  - `start_session`
  - `sim_session`
  - `trade_session`
  - `buy`
  - `sell`
- Mew-X normalized event surface: `sources/Mew-X/src/mew/instrumentation.rs`

Source-faithful consequence fixed now:

- Vexter may bind to config snapshots, pinned commits, and normalized event/status surfaces.
- Vexter may not rewrite Dexter trust logic, exit ladder logic, or reserved-balance semantics.
- Vexter may not rewrite Mew-X CHP/TIZ, loss/take-profit, inactivity, route fanout, or transport knobs.
- Any planner failure model must keep source-native reasons as passthrough metadata rather than reclassifying source strategy semantics.

## Concrete Planner/Router Code Spec

### Proposed package layout

| Module path | Responsibility | Source-faithful anchor |
| --- | --- | --- |
| `vexter/planner_router/models.py` | Frozen dataclasses and enums for config, request, plan, batch, status, and failure payloads | Immutable plan contract from PR `#35` / PR `#36` |
| `vexter/planner_router/errors.py` | Exception hierarchy for load, validation, resolution, emission, and dispatch failures | Planner pre-emit vs post-emit boundary |
| `vexter/planner_router/interfaces.py` | `PlanStore`, `ExecutorAdapter`, `ExecutorRegistry`, and `StatusSink` protocols | Keeps executor transport deferred |
| `vexter/planner_router/config_loader.py` | Deterministic JSON load, duplicate-id checks, cross-reference checks, and pin validation | `settings.py` and `config.rs` stay external |
| `vexter/planner_router/objective_resolver.py` | Objective-profile lookup and route-mode validation | `mixed_default -> Dexter`, explicit containment-only Mew-X |
| `vexter/planner_router/sleeve_selector.py` | Explicit sleeve selection with source-match enforcement | Dexter single-anchor vs Mew-X selective sleeve |
| `vexter/planner_router/budget_binder.py` | Sleeve-scoped share and cap-reference binding | `_reserve_buy_spend` and `MAX_TOKENS_AT_ONCE` stay source-local |
| `vexter/planner_router/plan_emitter.py` | Immutable `execution_plan` creation and atomic `plan_batch` emission | Pre-run binding only, no runtime mutation |
| `vexter/planner_router/dispatch_state_machine.py` | Prepare/start/stop orchestration and normalized status transitions | `monitor_mint_session`, `start_session`, `trade_session`, `sim_session` stay source-local |
| `vexter/planner_router/planner.py` | Public orchestration entrypoints that sequence load -> resolve -> select -> bind -> emit -> dispatch | Single Vexter control-plane surface |

Implementation-stage test files fixed now:

- `tests/test_planner_router_config_loader.py`
- `tests/test_planner_router_objective_resolver.py`
- `tests/test_planner_router_plan_emitter.py`
- `tests/test_planner_router_dispatch_state_machine.py`

### Typed object boundary

Shared objects should be `@dataclass(frozen=True, slots=True)` unless they are explicit runtime snapshots.

Config models:

- `PlannerConfig`
  - `default_execution_anchor`
  - `allowed_route_modes`
  - `global_halt_policy`
  - `config_package_order`
- `ObjectiveProfileConfig`
  - `objective_profile_id`
  - `preferred_source`
  - `route_mode`
  - `primary_sleeve_id`
  - `overlay_sleeve_ids`
  - `budget_policy_id`
  - `monitor_profile_id`
  - `executor_profile_id`
- `SleeveConfig`
  - `sleeve_id`
  - `source`
  - `enabled`
  - `budget_mode`
  - `executor_profile_id`
- `BudgetPolicyConfig`
  - `budget_policy_id`
  - `sleeve_shares`
  - `explicit_cap_required`
  - `cap_reference_by_sleeve`
- `MonitorProfileConfig`
  - `monitor_profile_id`
  - `admission_gate_class`
  - `timeout_envelope_class`
  - `quarantine_scope`
  - `global_halt_participation`
- `ExecutorProfileConfig`
  - `executor_profile_id`
  - `source`
  - `pinned_commit`
  - `methods`
  - `normalized_statuses`
- `SourcePinRegistry`
  - `dexter`
  - `mewx`

Planning and resolved models:

- `PlanRequest`
  - `plan_request_id`
  - `objective_profile_id`
  - `portfolio_budget_id`
- `PlannerRouterPackage`
  - `planner`
  - `objective_profiles`
  - `sleeves`
  - `budget_policies`
  - `monitor_profiles`
  - `executor_profiles`
  - `source_pins`
- `ResolvedObjectiveProfile`
  - `objective_profile_id`
  - `preferred_source`
  - `route_mode`
  - `primary_sleeve_id`
  - `overlay_sleeve_ids`
  - `budget_policy`
  - `monitor_profile`
  - `executor_profile`
- `SelectedSleeve`
  - `sleeve_id`
  - `source`
  - `executor_profile`
  - `declaration_order`
- `BudgetBinding`
  - `portfolio_budget_id`
  - `policy_id`
  - `sleeve_id`
  - `sleeve_share`
  - `explicit_cap_required`
  - `cap_reference`
- `ResolvedPlanningContext`
  - `request`
  - `package`
  - `resolved_objective`
  - `selected_sleeves`
  - `budget_bindings`

Plan and dispatch models:

- `PlanStatus`
  - `planned`
  - `starting`
  - `running`
  - `quarantined`
  - `stopping`
  - `stopped`
  - `failed`
- `ExecutionPlan`
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
  - `status`
- `PlanBatch`
  - `plan_batch_id`
  - `plans`
  - `request_id`
  - `portfolio_budget_id`
- `DispatchHandle`
  - `plan_id`
  - `source`
  - `native_handle`
- `StatusSnapshot`
  - `plan_id`
  - `status`
  - `source_reason`
  - `observed_at_utc`
  - `detail`
- `FailureDetail`
  - `code`
  - `stage`
  - `plan_id`
  - `source`
  - `source_reason`
  - `detail`

### Function boundaries by module

`config_loader.py`

```python
def load_planner_router_package(
    config_root: Path,
    frozen_pins: SourcePinRegistry,
) -> PlannerRouterPackage: ...

def load_planner_config(path: Path) -> PlannerConfig: ...
def load_objective_profiles(path: Path) -> dict[str, ObjectiveProfileConfig]: ...
def load_sleeves(path: Path) -> dict[str, SleeveConfig]: ...
def load_budget_policies(path: Path) -> dict[str, BudgetPolicyConfig]: ...
def load_monitor_profiles(path: Path) -> dict[str, MonitorProfileConfig]: ...
def load_executor_profiles(path: Path) -> dict[str, ExecutorProfileConfig]: ...
def validate_package_references(
    package: PlannerRouterPackage,
    frozen_pins: SourcePinRegistry,
) -> None: ...
```

Boundary fixed now:

- `config_loader.py` owns all file IO and all duplicate-id / cross-reference / pin checks.
- No downstream module re-opens JSON files or revalidates pins.
- Runtime overrides may not mutate preferred source, sleeve enablement, monitor profile, budget policy, or pinned commit after this module succeeds.

`objective_resolver.py`

```python
def resolve_objective_profile(
    request: PlanRequest,
    package: PlannerRouterPackage,
) -> ResolvedObjectiveProfile: ...
```

Boundary fixed now:

- Omitted `objective_profile_id` becomes `mixed_default`.
- Unknown explicit ids raise `UnknownObjectiveProfileError`.
- `portfolio_split` is legal only for Dexter-primary separate-sleeve templates.
- Mew-X-preferred profiles must be explicit containment-first profiles.

`sleeve_selector.py`

```python
def select_sleeves(
    objective: ResolvedObjectiveProfile,
    sleeves: Mapping[str, SleeveConfig],
) -> tuple[SelectedSleeve, ...]: ...
```

Boundary fixed now:

- `single_sleeve` returns one ordered sleeve.
- `portfolio_split` returns one Dexter primary sleeve plus explicitly declared overlay sleeves in declaration order.
- If any explicitly required sleeve is disabled or source-mismatched, the full request fails before emission.

`budget_binder.py`

```python
def bind_budgets(
    request: PlanRequest,
    objective: ResolvedObjectiveProfile,
    selected_sleeves: Sequence[SelectedSleeve],
    budget_policies: Mapping[str, BudgetPolicyConfig],
) -> tuple[BudgetBinding, ...]: ...
```

Boundary fixed now:

- Every selected sleeve gets exactly one immutable `BudgetBinding`.
- Nonzero Mew-X share requires `explicit_cap_required == True` and a non-empty cap reference.
- Aggregate batch share above `100%` raises `BudgetShareOverflowError`.

`plan_emitter.py`

```python
def build_execution_plans(
    context: ResolvedPlanningContext,
    created_at_utc: datetime,
) -> tuple[ExecutionPlan, ...]: ...

def emit_plan_batch(
    plans: Sequence[ExecutionPlan],
    request: PlanRequest,
    plan_store: PlanStore,
) -> PlanBatch: ...
```

Boundary fixed now:

- `build_execution_plans()` is pure and deterministic.
- `emit_plan_batch()` is the only module allowed to persist or publish plan artifacts.
- Emission is atomic at the batch boundary: either the full `PlanBatch` is stored or none is stored.

`interfaces.py`

```python
class PlanStore(Protocol):
    def put_batch(self, batch: PlanBatch) -> None: ...

class ExecutorAdapter(Protocol):
    def prepare(self, plan: ExecutionPlan) -> DispatchHandle: ...
    async def start(self, handle: DispatchHandle) -> None: ...
    async def status(self, handle: DispatchHandle) -> StatusSnapshot: ...
    async def stop(self, handle: DispatchHandle, reason: str) -> None: ...
    async def snapshot(self, handle: DispatchHandle) -> Mapping[str, Any]: ...

class ExecutorRegistry(Protocol):
    def adapter_for(self, plan: ExecutionPlan) -> ExecutorAdapter: ...

class StatusSink(Protocol):
    def record(self, snapshot: StatusSnapshot) -> None: ...
```

Source-faithful adapter ownership fixed now:

- Dexter adapter wraps `_settings_snapshot`, `set_trust_level`, `buy`, `sell`, `monitor_mint_session`, and the reserved-spend helpers as source-local behavior.
- Mew-X adapter wraps `config()`, `get_snipe_config()`, `get_strats_config()`, `get_tx_settings()`, `start_session`, `sim_session`, `trade_session`, `buy`, and `sell`.
- Transport family, subprocess/service execution, and handle serialization remain out of scope.

`dispatch_state_machine.py`

```python
async def dispatch_plan_batch(
    batch: PlanBatch,
    executor_registry: ExecutorRegistry,
    status_sink: StatusSink,
) -> list[StatusSnapshot]: ...

async def prepare_batch(
    batch: PlanBatch,
    executor_registry: ExecutorRegistry,
) -> tuple[DispatchHandle, ...]: ...

async def rollback_prepared_batch(
    handles: Sequence[DispatchHandle],
    executor_registry: ExecutorRegistry,
    failure: FailureDetail,
    status_sink: StatusSink,
) -> None: ...

def normalize_status_update(
    plan: ExecutionPlan,
    raw_status: str,
    *,
    source_reason: str | None = None,
    detail: Mapping[str, Any] | None = None,
) -> StatusSnapshot: ...

def validate_transition(previous: PlanStatus, next_status: PlanStatus) -> None: ...
```

`planner.py`

```python
def plan_request(
    request: PlanRequest,
    config_root: Path,
    frozen_pins: SourcePinRegistry,
    plan_store: PlanStore,
    created_at_utc: datetime,
) -> PlanBatch: ...

async def plan_and_dispatch(
    request: PlanRequest,
    config_root: Path,
    frozen_pins: SourcePinRegistry,
    plan_store: PlanStore,
    executor_registry: ExecutorRegistry,
    status_sink: StatusSink,
    created_at_utc: datetime,
) -> list[StatusSnapshot]: ...
```

Public-entry boundary fixed now:

- `planner.py` is the only module that sequences load -> resolve -> select -> bind -> emit -> dispatch.
- The implementation PR should keep all other modules importable and unit-testable without network or source process startup.

### Dispatch state machine and rollback semantics

Internal planner phases may exist, but the first externally visible state remains `planned`.

Allowed transitions:

- `planned -> starting`
- `planned -> failed`
- `starting -> running`
- `starting -> failed`
- `running -> quarantined`
- `running -> stopping`
- `running -> stopped`
- `running -> failed`
- `quarantined -> stopping`
- `quarantined -> failed`
- `stopping -> stopped`
- `stopping -> failed`

Rollback rules fixed now:

1. `prepare_batch()` runs in emitted plan order.
2. If any `prepare()` fails:
   - no `start()` call is issued
   - every previously prepared handle receives `stop(..., reason="prepare_failed")`
   - all plans in the batch end as `failed`
3. If all `prepare()` calls succeed:
   - all plans transition to `starting`
   - `start()` runs in emitted order
4. If a `start()` call fails:
   - already started handles receive `stop(..., reason="start_failed")`
   - prepared but not yet started handles also receive `stop`
   - the batch fails without reroute, rebinding, or cross-source handoff
5. Runtime failures after `running` stay source-local:
   - planner may quarantine the sleeve or request source-native stop
   - planner may not move the position to the other source
6. A normal Mew-X `inactivity_timeout` close stays source-native and does not by itself imply `quarantined`

### Error classes and failure surfaces

Exception hierarchy fixed now:

- `PlannerRouterError`
- `ConfigLoadError`
- `ConfigValidationError`
- `UnknownObjectiveProfileError`
- `SleeveSelectionError`
- `BudgetBindingError`
- `PlanEmissionError`
- `DispatchError`
- `InvalidStatusTransitionError`

Planner-owned failure codes fixed now:

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
- `prepare_failed`
- `start_failed`
- `status_timeout`
- `shutdown_unconfirmed`
- `invalid_status_transition`
- `source_stop_failed`

Source-native reasons remain passthrough metadata on `FailureDetail.source_reason`.

Dexter passthrough examples:

- `blacklist`
- `single_lock`
- `leaderboard_update`
- `insufficient_balance`
- `price_too_high`
- `zero_quote`
- `creator_vault_unavailable`
- `buy_confirmation_failed`
- `buy_confirmation_invalid`
- `stagnant`
- `drop-time`
- `malicious`

Mew-X passthrough examples:

- `region_inactive`
- `concurrency_cap_reached`
- `session_already_active`
- `transport_send_failed`
- `max_loss`
- `take_profit`
- `recent_profit_collapse`
- `creator_sold`
- `inactivity_timeout`

### What remains deferred

`monitor_killswitch_spec`

- numeric timeout-envelope values
- heartbeat cadence
- retry counts
- escalation thresholds from sleeve quarantine to global halt

`executor_boundary_spec`

- subprocess versus service model
- RPC versus gRPC versus SWQOS transport ownership
- native handle serialization
- transport telemetry retention format

These stay deferred because the code-spec cut already isolates them behind `MonitorProfileConfig`, `ExecutorAdapter`, `ExecutorRegistry`, and `StatusSink`.

## Recommendation Among Next Tasks

### `planner_router_code_implementation`

Recommended next because:

- the file layout, typed objects, public APIs, and test seams are now fixed strongly enough to implement without reopening evidence work
- config loading, resolution, selection, binding, emission, and dispatch can land behind abstract executor adapters before transport details are finalized
- the implementation can preserve frozen Dexter and Mew-X behavior by treating source-native reasons as adapter outputs rather than planner logic

### `monitor_killswitch_spec`

Not next because:

- it now attaches cleanly to already fixed `PlanStatus` transitions and `FailureDetail`
- numeric thresholds can be added after the first implementation skeleton exists

### `executor_boundary_spec`

Not next because:

- the current code spec already isolates executor transport behind protocols
- transport/process decisions no longer block the planner/router module implementation

## Decision

- Outcome: `A`
- Key finding: `planner_router_code_spec_ready`
- Claim boundary: `code_spec_bounded`
- Decision: `implementation_ready`
- Recommended next step: `planner_router_code_implementation`
