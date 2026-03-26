"""Immutable execution-plan emission."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime

from .errors import PlanEmissionError
from .interfaces import PlanStore
from .models import (
    BudgetBinding,
    ExecutionPlan,
    ExecutorBinding,
    FailureCode,
    MonitorBinding,
    MonitorProfileConfig,
    PlanBatch,
    PlanRequest,
    PlanStatus,
    ResolvedPlanningContext,
    RouteBinding,
    SelectedSleeve,
    SleeveBinding,
    Source,
    ensure_utc,
)


PLAN_INVARIANTS = (
    "route_is_pre_run_and_single_source",
    "bindings_are_fully_resolved_before_start",
    "source_pin_embedded_before_start",
    "no_mid_trade_handoff",
)


def _failure(code: FailureCode, *, detail: dict[str, object]) -> object:
    from .models import FailureDetail

    return FailureDetail(code=code, stage="emit", plan_id=None, source=None, source_reason=None, detail=detail)


def _monitor_profile_for_sleeve(
    context: ResolvedPlanningContext,
    selected_sleeve: SelectedSleeve,
) -> MonitorProfileConfig:
    if selected_sleeve.source is context.resolved_objective.preferred_source:
        return context.resolved_objective.monitor_profile
    if selected_sleeve.source is Source.DEXTER:
        return context.package.monitor_profiles["dexter_default"]
    return context.package.monitor_profiles["mewx_timeout_guard"]


def _budget_binding_by_sleeve(bindings: Sequence[BudgetBinding]) -> Mapping[str, BudgetBinding]:
    return {binding.sleeve_id: binding for binding in bindings}


def build_execution_plans(
    context: ResolvedPlanningContext,
    created_at_utc: datetime,
) -> tuple[ExecutionPlan, ...]:
    if not context.selected_sleeves:
        raise PlanEmissionError(
            "cannot emit plans without selected sleeves",
            failure=_failure(FailureCode.CONFIG_MISSING, detail={"reason": "selected_sleeves_empty"}),
        )

    created_at_utc = ensure_utc(created_at_utc)
    budget_binding_by_sleeve = _budget_binding_by_sleeve(context.budget_bindings)
    plan_batch_id = f"{context.request.plan_request_id}:batch"

    plans: list[ExecutionPlan] = []
    for selected_sleeve in context.selected_sleeves:
        budget_binding = budget_binding_by_sleeve.get(selected_sleeve.sleeve_id)
        if budget_binding is None:
            raise PlanEmissionError(
                f"missing budget binding for sleeve {selected_sleeve.sleeve_id!r}",
                failure=_failure(
                    FailureCode.UNKNOWN_BUDGET_POLICY,
                    detail={"sleeve_id": selected_sleeve.sleeve_id},
                ),
            )
        sleeve_config = context.package.sleeves[selected_sleeve.sleeve_id]
        monitor_profile = _monitor_profile_for_sleeve(context, selected_sleeve)
        plan_id = f"{plan_batch_id}:{selected_sleeve.declaration_order}:{selected_sleeve.sleeve_id}"
        plans.append(
            ExecutionPlan(
                plan_id=plan_id,
                plan_batch_id=plan_batch_id,
                created_at_utc=created_at_utc,
                objective_profile_id=context.resolved_objective.objective_profile_id,
                route=RouteBinding(
                    mode=context.resolved_objective.route_mode,
                    selected_sleeve_id=selected_sleeve.sleeve_id,
                    selected_source=selected_sleeve.source,
                ),
                sleeve_binding=SleeveBinding(
                    sleeve_id=selected_sleeve.sleeve_id,
                    source=selected_sleeve.source,
                    budget_mode=sleeve_config.budget_mode,
                ),
                budget_binding=budget_binding,
                monitor_binding=MonitorBinding(
                    monitor_profile_id=monitor_profile.monitor_profile_id,
                    admission_gate_class=monitor_profile.admission_gate_class,
                    timeout_envelope_class=monitor_profile.timeout_envelope_class,
                    quarantine_scope=monitor_profile.quarantine_scope,
                    global_halt_participation=monitor_profile.global_halt_participation,
                ),
                executor_binding=ExecutorBinding(
                    executor_profile_id=selected_sleeve.executor_profile.executor_profile_id,
                    source=selected_sleeve.executor_profile.source,
                    pinned_commit=selected_sleeve.executor_profile.pinned_commit,
                    methods=selected_sleeve.executor_profile.methods,
                    normalized_statuses=selected_sleeve.executor_profile.normalized_statuses,
                ),
                source_pin=context.package.source_pins,
                invariants=PLAN_INVARIANTS,
                status=PlanStatus.PLANNED,
            )
        )
    return tuple(plans)


def emit_plan_batch(
    plans: Sequence[ExecutionPlan],
    request: PlanRequest,
    plan_store: PlanStore,
) -> PlanBatch:
    if not plans:
        raise PlanEmissionError(
            "cannot emit an empty plan batch",
            failure=_failure(FailureCode.CONFIG_MISSING, detail={"reason": "plans_empty"}),
        )

    plan_batch_id = plans[0].plan_batch_id
    if any(plan.plan_batch_id != plan_batch_id for plan in plans):
        raise PlanEmissionError(
            "all plans must share a plan_batch_id",
            failure=_failure(FailureCode.CONFIG_MISSING, detail={"reason": "mixed_plan_batch_ids"}),
        )

    batch = PlanBatch(
        plan_batch_id=plan_batch_id,
        plans=tuple(plans),
        request_id=request.plan_request_id,
        portfolio_budget_id=request.portfolio_budget_id or plans[0].budget_binding.portfolio_budget_id,
    )
    try:
        plan_store.put_batch(batch)
    except Exception as exc:
        raise PlanEmissionError(
            f"failed to store batch {batch.plan_batch_id!r}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                detail={"plan_batch_id": batch.plan_batch_id, "error": str(exc)},
            ),
        ) from exc
    return batch
