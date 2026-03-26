import asyncio
import json
import shutil
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vexter.planner_router.errors import ConfigValidationError, UnknownObjectiveProfileError
from vexter.planner_router.models import (
    DispatchHandle,
    FailureCode,
    PlanRequest,
    PlanStatus,
    Source,
    SourcePinRegistry,
    StatusSnapshot,
)
from vexter.planner_router.planner import plan_and_dispatch, plan_request


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "config" / "planner_router"
FROZEN_PINS = SourcePinRegistry(
    dexter="ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    mewx="dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
)
CREATED_AT = datetime(2026, 3, 26, 2, 18, tzinfo=timezone.utc)


class MemoryPlanStore:
    def __init__(self, events: list[str] | None = None) -> None:
        self.events = events if events is not None else []
        self.batches = []

    def put_batch(self, batch) -> None:
        self.events.append(f"store:{batch.plan_batch_id}")
        self.batches.append(batch)


class MemoryStatusSink:
    def __init__(self) -> None:
        self.snapshots = []

    def record(self, snapshot) -> None:
        self.snapshots.append(snapshot)


class ScriptedAdapter:
    def __init__(
        self,
        source: Source,
        events: list[str],
        *,
        fail_prepare: bool = False,
        fail_start: bool = False,
    ) -> None:
        self.source = source
        self.events = events
        self.fail_prepare = fail_prepare
        self.fail_start = fail_start
        self.prepared = []
        self.started = []
        self.stopped = []

    def prepare(self, plan) -> DispatchHandle:
        self.events.append(f"prepare:{self.source.value}:{plan.plan_id}")
        if self.fail_prepare:
            raise RuntimeError(f"prepare failed for {plan.plan_id}")
        self.prepared.append(plan.plan_id)
        return DispatchHandle(plan_id=plan.plan_id, source=plan.route.selected_source, native_handle={}, plan=plan)

    async def start(self, handle: DispatchHandle) -> None:
        self.events.append(f"start:{self.source.value}:{handle.plan_id}")
        if self.fail_start:
            raise RuntimeError(f"start failed for {handle.plan_id}")
        self.started.append(handle.plan_id)

    async def status(self, handle: DispatchHandle) -> StatusSnapshot:
        self.events.append(f"status:{self.source.value}:{handle.plan_id}")
        return StatusSnapshot(
            plan_id=handle.plan_id,
            status=PlanStatus.RUNNING,
            source_reason=None,
            observed_at_utc=datetime.now(timezone.utc),
            detail={},
        )

    async def stop(self, handle: DispatchHandle, reason: str) -> None:
        self.events.append(f"stop:{self.source.value}:{handle.plan_id}:{reason}")
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


def mutate_invalid_profile(config_root: Path) -> None:
    objective_profiles_path = config_root / "objective_profiles.json"
    payload = json.loads(objective_profiles_path.read_text())
    payload[0]["route_mode"] = "portfolio_split"
    payload[0]["overlay_sleeve_ids"] = []
    objective_profiles_path.write_text(json.dumps(payload, indent=2) + "\n")


def mutate_pin_mismatch(config_root: Path) -> None:
    executor_profiles_path = config_root / "executor_profiles.json"
    payload = json.loads(executor_profiles_path.read_text())
    payload[0]["pinned_commit"] = "deadbeef"
    executor_profiles_path.write_text(json.dumps(payload, indent=2) + "\n")


def mutate_missing_cross_reference(config_root: Path) -> None:
    objective_profiles_path = config_root / "objective_profiles.json"
    payload = json.loads(objective_profiles_path.read_text())
    payload[0]["monitor_profile_id"] = "missing_monitor"
    objective_profiles_path.write_text(json.dumps(payload, indent=2) + "\n")


def build_registry(
    events: list[str],
    *,
    fail_prepare_for_mewx: bool = False,
    fail_start_for_mewx: bool = False,
) -> tuple[ExecutorRegistry, ScriptedAdapter, ScriptedAdapter]:
    dexter_adapter = ScriptedAdapter(Source.DEXTER, events)
    mewx_adapter = ScriptedAdapter(
        Source.MEWX,
        events,
        fail_prepare=fail_prepare_for_mewx,
        fail_start=fail_start_for_mewx,
    )
    return ExecutorRegistry(dexter_adapter, mewx_adapter), dexter_adapter, mewx_adapter


def test_plan_request_smoke_emits_immutable_default_batch() -> None:
    store = MemoryPlanStore()

    batch = plan_request(
        PlanRequest(plan_request_id="req-smoke-default"),
        CONFIG_ROOT,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )

    assert store.batches == [batch]
    assert batch.plan_batch_id == "req-smoke-default:batch"
    assert batch.request_id == "req-smoke-default"
    assert batch.portfolio_budget_id == "main"
    assert len(batch.plans) == 1

    plan = batch.plans[0]
    assert plan.objective_profile_id == "mixed_default"
    assert plan.route.selected_source is Source.DEXTER
    assert plan.sleeve_binding.sleeve_id == "dexter_default"
    assert plan.budget_binding.policy_id == "single_anchor_default"
    assert plan.budget_binding.sleeve_share == 100
    assert plan.executor_binding.pinned_commit == FROZEN_PINS.dexter
    assert plan.source_pin == FROZEN_PINS
    assert plan.status is PlanStatus.PLANNED
    assert "source_pin_embedded_before_start" in plan.invariants

    with pytest.raises(FrozenInstanceError):
        plan.status = PlanStatus.RUNNING


def test_plan_and_dispatch_smoke_runs_overlay_path_end_to_end(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    events: list[str] = []
    store = MemoryPlanStore(events)
    sink = MemoryStatusSink()
    registry, dexter_adapter, mewx_adapter = build_registry(events)

    snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(plan_request_id="req-smoke-overlay", objective_profile_id="dexter_with_mewx_overlay"),
            config_root,
            FROZEN_PINS,
            store,
            registry,
            sink,
            CREATED_AT,
        )
    )

    assert [plan.route.selected_source for plan in store.batches[0].plans] == [Source.DEXTER, Source.MEWX]
    assert [plan.budget_binding.sleeve_share for plan in store.batches[0].plans] == [80, 20]
    assert store.batches[0].plans[1].budget_binding.cap_reference == "mewx_overlay_minor_cap"
    assert [snapshot.status for snapshot in snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
    ]
    assert sink.snapshots == snapshots
    assert dexter_adapter.stopped == []
    assert mewx_adapter.stopped == []

    plan_ids = [plan.plan_id for plan in store.batches[0].plans]
    assert events == [
        "store:req-smoke-overlay:batch",
        f"prepare:dexter:{plan_ids[0]}",
        f"prepare:mewx:{plan_ids[1]}",
        f"start:dexter:{plan_ids[0]}",
        f"status:dexter:{plan_ids[0]}",
        f"start:mewx:{plan_ids[1]}",
        f"status:mewx:{plan_ids[1]}",
    ]


@pytest.mark.parametrize(
    ("config_mutator", "plan_request_input", "expected_exception", "expected_code"),
    [
        (
            None,
            PlanRequest(plan_request_id="req-invalid-objective", objective_profile_id="unknown_profile"),
            UnknownObjectiveProfileError,
            FailureCode.UNKNOWN_OBJECTIVE_PROFILE,
        ),
        (
            mutate_invalid_profile,
            PlanRequest(plan_request_id="req-invalid-profile"),
            ConfigValidationError,
            FailureCode.ROUTE_MODE_INVALID,
        ),
        (
            mutate_pin_mismatch,
            PlanRequest(plan_request_id="req-pin-mismatch"),
            ConfigValidationError,
            FailureCode.PIN_MISMATCH,
        ),
        (
            mutate_missing_cross_reference,
            PlanRequest(plan_request_id="req-cross-reference"),
            ConfigValidationError,
            FailureCode.CONFIG_MISSING,
        ),
    ],
)
def test_plan_request_fail_closed_rejects_invalid_inputs_without_partial_batch(
    tmp_path: Path,
    config_mutator,
    plan_request_input: PlanRequest,
    expected_exception,
    expected_code: FailureCode,
) -> None:
    config_root = clone_config_dir(tmp_path)
    if config_mutator is not None:
        config_mutator(config_root)
    store = MemoryPlanStore()

    with pytest.raises(expected_exception) as exc_info:
        plan_request(plan_request_input, config_root, FROZEN_PINS, store, CREATED_AT)

    assert exc_info.value.failure is not None
    assert exc_info.value.failure.code is expected_code
    assert store.batches == []


@pytest.mark.parametrize(
    ("fail_prepare_for_mewx", "fail_start_for_mewx", "expected_stop_reason", "expected_statuses"),
    [
        (
            True,
            False,
            "prepare_failed",
            [PlanStatus.FAILED, PlanStatus.FAILED],
        ),
        (
            False,
            True,
            "start_failed",
            [
                PlanStatus.STARTING,
                PlanStatus.RUNNING,
                PlanStatus.STARTING,
                PlanStatus.FAILED,
                PlanStatus.FAILED,
            ],
        ),
    ],
)
def test_plan_and_dispatch_smoke_rolls_back_overlay_batch_on_partial_failure(
    tmp_path: Path,
    fail_prepare_for_mewx: bool,
    fail_start_for_mewx: bool,
    expected_stop_reason: str,
    expected_statuses: list[PlanStatus],
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    events: list[str] = []
    store = MemoryPlanStore(events)
    sink = MemoryStatusSink()
    registry, dexter_adapter, mewx_adapter = build_registry(
        events,
        fail_prepare_for_mewx=fail_prepare_for_mewx,
        fail_start_for_mewx=fail_start_for_mewx,
    )

    snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(plan_request_id="req-rollback", objective_profile_id="dexter_with_mewx_overlay"),
            config_root,
            FROZEN_PINS,
            store,
            registry,
            sink,
            CREATED_AT,
        )
    )

    plan_ids = [plan.plan_id for plan in store.batches[0].plans]

    assert [snapshot.status for snapshot in snapshots] == expected_statuses
    assert sink.snapshots == snapshots
    assert dexter_adapter.stopped == [(plan_ids[0], expected_stop_reason)]

    if fail_prepare_for_mewx:
        assert mewx_adapter.stopped == []
        assert events == [
            "store:req-rollback:batch",
            f"prepare:dexter:{plan_ids[0]}",
            f"prepare:mewx:{plan_ids[1]}",
            f"stop:dexter:{plan_ids[0]}:{expected_stop_reason}",
        ]
    else:
        assert mewx_adapter.stopped == [(plan_ids[1], expected_stop_reason)]
        assert events == [
            "store:req-rollback:batch",
            f"prepare:dexter:{plan_ids[0]}",
            f"prepare:mewx:{plan_ids[1]}",
            f"start:dexter:{plan_ids[0]}",
            f"status:dexter:{plan_ids[0]}",
            f"start:mewx:{plan_ids[1]}",
            f"stop:mewx:{plan_ids[1]}:{expected_stop_reason}",
            f"stop:dexter:{plan_ids[0]}:{expected_stop_reason}",
        ]
