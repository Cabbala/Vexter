import asyncio
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from vexter.planner_router.budget_binder import bind_budgets
from vexter.planner_router.config_loader import load_planner_router_package
from vexter.planner_router.dispatch_state_machine import dispatch_plan_batch
from vexter.planner_router.models import (
    DispatchHandle,
    PlanRequest,
    PlanStatus,
    ResolvedPlanningContext,
    Source,
    SourcePinRegistry,
    StatusSnapshot,
)
from vexter.planner_router.objective_resolver import resolve_objective_profile
from vexter.planner_router.plan_emitter import build_execution_plans, emit_plan_batch
from vexter.planner_router.sleeve_selector import select_sleeves


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "config" / "planner_router"
FROZEN_PINS = SourcePinRegistry(
    dexter="ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    mewx="dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
)


class MemoryPlanStore:
    def __init__(self) -> None:
        self.batches = []

    def put_batch(self, batch) -> None:
        self.batches.append(batch)


class MemoryStatusSink:
    def __init__(self) -> None:
        self.snapshots = []

    def record(self, snapshot) -> None:
        self.snapshots.append(snapshot)


class ScriptedAdapter:
    def __init__(
        self,
        *,
        fail_prepare_for: set[str] | None = None,
        fail_start_for: set[str] | None = None,
    ) -> None:
        self.fail_prepare_for = fail_prepare_for or set()
        self.fail_start_for = fail_start_for or set()
        self.prepared = []
        self.started = []
        self.stopped = []

    def prepare(self, plan) -> DispatchHandle:
        if plan.plan_id in self.fail_prepare_for:
            raise RuntimeError(f"prepare failed for {plan.plan_id}")
        self.prepared.append(plan.plan_id)
        return DispatchHandle(plan_id=plan.plan_id, source=plan.route.selected_source, native_handle={}, plan=plan)

    async def start(self, handle: DispatchHandle) -> None:
        if handle.plan_id in self.fail_start_for:
            raise RuntimeError(f"start failed for {handle.plan_id}")
        self.started.append(handle.plan_id)

    async def status(self, handle: DispatchHandle) -> StatusSnapshot:
        return StatusSnapshot(
            plan_id=handle.plan_id,
            status=PlanStatus.RUNNING,
            source_reason=None,
            observed_at_utc=datetime.now(timezone.utc),
            detail={},
        )

    async def stop(self, handle: DispatchHandle, reason: str) -> None:
        self.stopped.append((handle.plan_id, reason))

    async def snapshot(self, handle: DispatchHandle):
        return {"plan_id": handle.plan_id}


class ExecutorRegistry:
    def __init__(self, dexter_adapter: ScriptedAdapter, mewx_adapter: ScriptedAdapter) -> None:
        self.dexter_adapter = dexter_adapter
        self.mewx_adapter = mewx_adapter

    def adapter_for(self, plan):
        if plan.route.selected_source is Source.DEXTER:
            return self.dexter_adapter
        return self.mewx_adapter


def clone_config_dir(tmp_path: Path) -> Path:
    destination = tmp_path / "planner_router"
    shutil.copytree(CONFIG_ROOT, destination)
    return destination


def enable_mewx_sleeve(config_root: Path) -> None:
    sleeves_path = config_root / "sleeves.json"
    payload = json.loads(sleeves_path.read_text())
    payload[1]["enabled"] = True
    sleeves_path.write_text(json.dumps(payload, indent=2) + "\n")


def build_batch(config_root: Path, request: PlanRequest):
    package = load_planner_router_package(config_root, FROZEN_PINS)
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
    plans = build_execution_plans(context, datetime(2026, 3, 26, 2, 15, tzinfo=timezone.utc))
    return emit_plan_batch(plans, request, MemoryPlanStore())


def test_dispatch_plan_batch_runs_prepare_then_start_for_single_plan() -> None:
    batch = build_batch(CONFIG_ROOT, PlanRequest(plan_request_id="req-6"))
    dexter_adapter = ScriptedAdapter()
    mewx_adapter = ScriptedAdapter()
    sink = MemoryStatusSink()

    snapshots = asyncio.run(dispatch_plan_batch(batch, ExecutorRegistry(dexter_adapter, mewx_adapter), sink))

    assert [snapshot.status for snapshot in snapshots] == [PlanStatus.STARTING, PlanStatus.RUNNING]
    assert dexter_adapter.prepared == [batch.plans[0].plan_id]
    assert dexter_adapter.started == [batch.plans[0].plan_id]
    assert dexter_adapter.stopped == []


def test_dispatch_plan_batch_rolls_back_on_prepare_failure(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    batch = build_batch(
        config_root,
        PlanRequest(plan_request_id="req-7", objective_profile_id="dexter_with_mewx_overlay"),
    )
    dexter_adapter = ScriptedAdapter()
    mewx_adapter = ScriptedAdapter(fail_prepare_for={batch.plans[1].plan_id})
    sink = MemoryStatusSink()

    snapshots = asyncio.run(dispatch_plan_batch(batch, ExecutorRegistry(dexter_adapter, mewx_adapter), sink))

    assert all(snapshot.status is PlanStatus.FAILED for snapshot in snapshots)
    assert dexter_adapter.stopped == [(batch.plans[0].plan_id, "prepare_failed")]
    assert mewx_adapter.stopped == []


def test_dispatch_plan_batch_rolls_back_on_start_failure(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    batch = build_batch(
        config_root,
        PlanRequest(plan_request_id="req-8", objective_profile_id="dexter_with_mewx_overlay"),
    )
    dexter_adapter = ScriptedAdapter()
    mewx_adapter = ScriptedAdapter(fail_start_for={batch.plans[1].plan_id})
    sink = MemoryStatusSink()

    snapshots = asyncio.run(dispatch_plan_batch(batch, ExecutorRegistry(dexter_adapter, mewx_adapter), sink))

    assert snapshots[0].status is PlanStatus.STARTING
    assert snapshots[1].status is PlanStatus.RUNNING
    assert all(snapshot.status is PlanStatus.FAILED for snapshot in snapshots[-2:])
    assert dexter_adapter.stopped == [(batch.plans[0].plan_id, "start_failed")]
    assert mewx_adapter.stopped == [(batch.plans[1].plan_id, "start_failed")]
