"""Planner/router orchestration entrypoints."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .budget_binder import bind_budgets
from .config_loader import load_planner_router_package
from .dispatch_state_machine import dispatch_plan_batch
from .interfaces import ExecutorRegistry, PlanStore, StatusSink
from .models import PlanBatch, PlanRequest, ResolvedPlanningContext, SourcePinRegistry
from .objective_resolver import resolve_objective_profile
from .plan_emitter import build_execution_plans, emit_plan_batch
from .sleeve_selector import select_sleeves


def plan_request(
    request: PlanRequest,
    config_root: Path,
    frozen_pins: SourcePinRegistry,
    plan_store: PlanStore,
    created_at_utc: datetime,
) -> PlanBatch:
    package = load_planner_router_package(config_root, frozen_pins)
    resolved_objective = resolve_objective_profile(request, package)
    selected_sleeves = select_sleeves(resolved_objective, package.sleeves)
    budget_bindings = bind_budgets(request, resolved_objective, selected_sleeves, package.budget_policies)
    context = ResolvedPlanningContext(
        request=request,
        package=package,
        resolved_objective=resolved_objective,
        selected_sleeves=selected_sleeves,
        budget_bindings=budget_bindings,
    )
    plans = build_execution_plans(context, created_at_utc)
    return emit_plan_batch(plans, request, plan_store)


async def plan_and_dispatch(
    request: PlanRequest,
    config_root: Path,
    frozen_pins: SourcePinRegistry,
    plan_store: PlanStore,
    executor_registry: ExecutorRegistry,
    status_sink: StatusSink,
    created_at_utc: datetime,
) -> list:
    batch = plan_request(request, config_root, frozen_pins, plan_store, created_at_utc)
    return await dispatch_plan_batch(batch, executor_registry, status_sink)
