import asyncio
import json
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from vexter.planner_router.dispatch_state_machine import normalize_status_update, validate_transition
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
CREATED_AT = datetime(2026, 3, 26, 2, 41, tzinfo=timezone.utc)


class RuntimeMirrorPlanStore:
    def __init__(self, events: list[str] | None = None) -> None:
        self.events = events if events is not None else []
        self.batches = []
        self.current_statuses: dict[str, PlanStatus] = {}
        self.status_sequences: defaultdict[str, list[PlanStatus]] = defaultdict(list)
        self.detail_sequences: defaultdict[str, list[dict[str, object]]] = defaultdict(list)

    def put_batch(self, batch) -> None:
        self.events.append(f"store:{batch.plan_batch_id}")
        self.batches.append(batch)
        for plan in batch.plans:
            self.current_statuses[plan.plan_id] = plan.status
            self.status_sequences[plan.plan_id].append(plan.status)
            self.detail_sequences[plan.plan_id].append(
                {
                    "origin": "plan_store",
                    "status": plan.status.value,
                    "source": plan.route.selected_source.value,
                }
            )

    def apply_snapshot(self, snapshot: StatusSnapshot) -> None:
        self.current_statuses[snapshot.plan_id] = snapshot.status
        self.status_sequences[snapshot.plan_id].append(snapshot.status)
        self.detail_sequences[snapshot.plan_id].append(dict(snapshot.detail))

    def current_status(self, plan_id: str) -> PlanStatus:
        return self.current_statuses[plan_id]


class MirroringStatusSink:
    def __init__(self, store: RuntimeMirrorPlanStore) -> None:
        self.store = store
        self.snapshots = []

    def record(self, snapshot: StatusSnapshot) -> None:
        self.snapshots.append(snapshot)
        self.store.apply_snapshot(snapshot)


class RuntimeScriptedAdapter:
    def __init__(
        self,
        source: Source,
        events: list[str],
        *,
        fail_stop: bool = False,
        status: PlanStatus = PlanStatus.RUNNING,
    ) -> None:
        self.source = source
        self.events = events
        self.fail_stop = fail_stop
        self.status_value = status
        self.handles: dict[str, DispatchHandle] = {}
        self.prepared = []
        self.started = []
        self.stopped = []

    def prepare(self, plan) -> DispatchHandle:
        self.events.append(f"prepare:{self.source.value}:{plan.plan_id}")
        handle = DispatchHandle(
            plan_id=plan.plan_id,
            source=plan.route.selected_source,
            native_handle={"source": self.source.value},
            plan=plan,
        )
        self.handles[plan.plan_id] = handle
        self.prepared.append(plan.plan_id)
        return handle

    async def start(self, handle: DispatchHandle) -> None:
        self.events.append(f"start:{self.source.value}:{handle.plan_id}")
        self.started.append(handle.plan_id)

    async def status(self, handle: DispatchHandle) -> StatusSnapshot:
        self.events.append(f"status:{self.source.value}:{handle.plan_id}")
        return StatusSnapshot(
            plan_id=handle.plan_id,
            status=self.status_value,
            source_reason=None,
            observed_at_utc=datetime.now(timezone.utc),
            detail={"signal": "status_poll", "source": self.source.value},
        )

    async def stop(self, handle: DispatchHandle, reason: str) -> None:
        self.events.append(f"stop:{self.source.value}:{handle.plan_id}:{reason}")
        self.stopped.append((handle.plan_id, reason))
        if self.fail_stop:
            raise RuntimeError(f"shutdown unconfirmed for {handle.plan_id}")

    async def snapshot(self, handle: DispatchHandle):
        self.events.append(f"snapshot:{self.source.value}:{handle.plan_id}")
        return {"plan_id": handle.plan_id, "source": self.source.value, "stopped": True}


class ExecutorRegistry:
    def __init__(self, dexter_adapter: RuntimeScriptedAdapter, mewx_adapter: RuntimeScriptedAdapter) -> None:
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


def build_registry(
    events: list[str],
    *,
    fail_stop_for_mewx: bool = False,
    dexter_status: PlanStatus = PlanStatus.RUNNING,
    mewx_status: PlanStatus = PlanStatus.RUNNING,
) -> tuple[ExecutorRegistry, RuntimeScriptedAdapter, RuntimeScriptedAdapter]:
    dexter_adapter = RuntimeScriptedAdapter(Source.DEXTER, events, status=dexter_status)
    mewx_adapter = RuntimeScriptedAdapter(
        Source.MEWX,
        events,
        fail_stop=fail_stop_for_mewx,
        status=mewx_status,
    )
    return ExecutorRegistry(dexter_adapter, mewx_adapter), dexter_adapter, mewx_adapter


async def drive_quarantine_stop_all(
    batch,
    store: RuntimeMirrorPlanStore,
    sink: MirroringStatusSink,
    registry: ExecutorRegistry,
    *,
    quarantine_plan_id: str,
    stop_reason: str,
) -> list[StatusSnapshot]:
    snapshots: list[StatusSnapshot] = []
    plans_by_id = {plan.plan_id: plan for plan in batch.plans}
    trigger_plan = plans_by_id[quarantine_plan_id]

    quarantine_snapshot = normalize_status_update(
        trigger_plan,
        PlanStatus.QUARANTINED.value,
        source_reason="runtime_guard_triggered",
        detail={
            "signal": "quarantine",
            "quarantine_scope": trigger_plan.monitor_binding.quarantine_scope,
            "trigger_plan_id": quarantine_plan_id,
        },
    )
    validate_transition(store.current_status(quarantine_plan_id), quarantine_snapshot.status)
    sink.record(quarantine_snapshot)
    snapshots.append(quarantine_snapshot)

    for plan in reversed(batch.plans):
        stopping_snapshot = normalize_status_update(
            plan,
            PlanStatus.STOPPING.value,
            source_reason="stop_all",
            detail={
                "signal": "stop",
                "stop_reason": stop_reason,
                "trigger_plan_id": quarantine_plan_id,
            },
        )
        validate_transition(store.current_status(plan.plan_id), stopping_snapshot.status)
        sink.record(stopping_snapshot)
        snapshots.append(stopping_snapshot)

        adapter = registry.adapter_for(plan)
        handle = adapter.handles[plan.plan_id]
        try:
            await adapter.stop(handle, reason=stop_reason)
            final_snapshot = normalize_status_update(
                plan,
                PlanStatus.STOPPED.value,
                source_reason=None,
                detail={
                    "signal": "rollback_complete",
                    "stop_reason": stop_reason,
                    "trigger_plan_id": quarantine_plan_id,
                    "adapter_snapshot": await adapter.snapshot(handle),
                },
            )
        except Exception as exc:
            final_snapshot = normalize_status_update(
                plan,
                PlanStatus.FAILED.value,
                source_reason=str(exc),
                detail={
                    "signal": "rollback_failed",
                    "stop_reason": stop_reason,
                    "trigger_plan_id": quarantine_plan_id,
                    "failure_code": FailureCode.SHUTDOWN_UNCONFIRMED.value,
                    "error": str(exc),
                },
            )

        validate_transition(store.current_status(plan.plan_id), final_snapshot.status)
        sink.record(final_snapshot)
        snapshots.append(final_snapshot)

    return snapshots


def test_plan_request_runtime_smoke_seeds_planned_store_state(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    events: list[str] = []
    store = RuntimeMirrorPlanStore(events)

    batch = plan_request(
        PlanRequest(plan_request_id="req-runtime-plan", objective_profile_id="dexter_with_mewx_overlay"),
        config_root,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )

    plan_ids = [plan.plan_id for plan in batch.plans]
    assert [store.current_status(plan_id) for plan_id in plan_ids] == [PlanStatus.PLANNED, PlanStatus.PLANNED]
    assert [status.value for status in store.status_sequences[plan_ids[0]]] == ["planned"]
    assert [status.value for status in store.status_sequences[plan_ids[1]]] == ["planned"]
    assert events == ["store:req-runtime-plan:batch"]


def test_plan_and_dispatch_runtime_smoke_progresses_single_sleeve_path_to_stopped() -> None:
    events: list[str] = []
    store = RuntimeMirrorPlanStore(events)
    sink = MirroringStatusSink(store)
    registry, dexter_adapter, _ = build_registry(events)

    dispatch_snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(plan_request_id="req-runtime-single"),
            CONFIG_ROOT,
            FROZEN_PINS,
            store,
            registry,
            sink,
            CREATED_AT,
        )
    )

    batch = store.batches[0]
    plan_id = batch.plans[0].plan_id
    runtime_snapshots = asyncio.run(
        drive_quarantine_stop_all(
            batch,
            store,
            sink,
            registry,
            quarantine_plan_id=plan_id,
            stop_reason="monitor_quarantine",
        )
    )

    assert [snapshot.status for snapshot in dispatch_snapshots] == [PlanStatus.STARTING, PlanStatus.RUNNING]
    assert [snapshot.status for snapshot in runtime_snapshots] == [
        PlanStatus.QUARANTINED,
        PlanStatus.STOPPING,
        PlanStatus.STOPPED,
    ]
    assert [status.value for status in store.status_sequences[plan_id]] == [
        "planned",
        "starting",
        "running",
        "quarantined",
        "stopping",
        "stopped",
    ]
    assert store.detail_sequences[plan_id][3]["signal"] == "quarantine"
    assert store.detail_sequences[plan_id][4]["signal"] == "stop"
    assert store.detail_sequences[plan_id][5]["signal"] == "rollback_complete"
    assert sink.snapshots == dispatch_snapshots + runtime_snapshots
    assert dexter_adapter.stopped == [(plan_id, "monitor_quarantine")]
    assert events == [
        "store:req-runtime-single:batch",
        f"prepare:dexter:{plan_id}",
        f"start:dexter:{plan_id}",
        f"status:dexter:{plan_id}",
        f"stop:dexter:{plan_id}:monitor_quarantine",
        f"snapshot:dexter:{plan_id}",
    ]


def test_plan_and_dispatch_runtime_smoke_rolls_back_overlay_batch_on_quarantine_failure(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    events: list[str] = []
    store = RuntimeMirrorPlanStore(events)
    sink = MirroringStatusSink(store)
    registry, dexter_adapter, mewx_adapter = build_registry(events, fail_stop_for_mewx=True)

    dispatch_snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(plan_request_id="req-runtime-overlay", objective_profile_id="dexter_with_mewx_overlay"),
            config_root,
            FROZEN_PINS,
            store,
            registry,
            sink,
            CREATED_AT,
        )
    )

    batch = store.batches[0]
    dexter_plan, mewx_plan = batch.plans
    runtime_snapshots = asyncio.run(
        drive_quarantine_stop_all(
            batch,
            store,
            sink,
            registry,
            quarantine_plan_id=mewx_plan.plan_id,
            stop_reason="monitor_quarantine",
        )
    )

    assert [snapshot.status for snapshot in dispatch_snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
    ]
    assert [snapshot.status for snapshot in runtime_snapshots] == [
        PlanStatus.QUARANTINED,
        PlanStatus.STOPPING,
        PlanStatus.FAILED,
        PlanStatus.STOPPING,
        PlanStatus.STOPPED,
    ]
    assert [status.value for status in store.status_sequences[mewx_plan.plan_id]] == [
        "planned",
        "starting",
        "running",
        "quarantined",
        "stopping",
        "failed",
    ]
    assert [status.value for status in store.status_sequences[dexter_plan.plan_id]] == [
        "planned",
        "starting",
        "running",
        "stopping",
        "stopped",
    ]
    assert store.detail_sequences[mewx_plan.plan_id][-1]["failure_code"] == FailureCode.SHUTDOWN_UNCONFIRMED.value
    assert store.detail_sequences[dexter_plan.plan_id][-1]["signal"] == "rollback_complete"
    assert mewx_adapter.stopped == [(mewx_plan.plan_id, "monitor_quarantine")]
    assert dexter_adapter.stopped == [(dexter_plan.plan_id, "monitor_quarantine")]
    assert events == [
        "store:req-runtime-overlay:batch",
        f"prepare:dexter:{dexter_plan.plan_id}",
        f"prepare:mewx:{mewx_plan.plan_id}",
        f"start:dexter:{dexter_plan.plan_id}",
        f"status:dexter:{dexter_plan.plan_id}",
        f"start:mewx:{mewx_plan.plan_id}",
        f"status:mewx:{mewx_plan.plan_id}",
        f"stop:mewx:{mewx_plan.plan_id}:monitor_quarantine",
        f"stop:dexter:{dexter_plan.plan_id}:monitor_quarantine",
        f"snapshot:dexter:{dexter_plan.plan_id}",
    ]


def test_plan_and_dispatch_runtime_smoke_fails_closed_on_invalid_runtime_transition(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    events: list[str] = []
    store = RuntimeMirrorPlanStore(events)
    sink = MirroringStatusSink(store)
    registry, dexter_adapter, mewx_adapter = build_registry(events, mewx_status=PlanStatus.STOPPED)

    dispatch_snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(plan_request_id="req-runtime-invalid", objective_profile_id="dexter_with_mewx_overlay"),
            config_root,
            FROZEN_PINS,
            store,
            registry,
            sink,
            CREATED_AT,
        )
    )

    batch = store.batches[0]
    dexter_plan, mewx_plan = batch.plans

    assert [snapshot.status for snapshot in dispatch_snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.FAILED,
        PlanStatus.FAILED,
    ]
    assert dispatch_snapshots[-2].detail["failure_code"] == FailureCode.INVALID_STATUS_TRANSITION.value
    assert dispatch_snapshots[-1].detail["failure_code"] == FailureCode.INVALID_STATUS_TRANSITION.value
    assert dexter_adapter.stopped == [(dexter_plan.plan_id, FailureCode.INVALID_STATUS_TRANSITION.value)]
    assert mewx_adapter.stopped == [(mewx_plan.plan_id, FailureCode.INVALID_STATUS_TRANSITION.value)]
    assert dispatch_snapshots[-1].detail["rollback_attempted"] is True
    assert events == [
        "store:req-runtime-invalid:batch",
        f"prepare:dexter:{dexter_plan.plan_id}",
        f"prepare:mewx:{mewx_plan.plan_id}",
        f"start:dexter:{dexter_plan.plan_id}",
        f"status:dexter:{dexter_plan.plan_id}",
        f"start:mewx:{mewx_plan.plan_id}",
        f"status:mewx:{mewx_plan.plan_id}",
        f"stop:mewx:{mewx_plan.plan_id}:{FailureCode.INVALID_STATUS_TRANSITION.value}",
        f"status:mewx:{mewx_plan.plan_id}",
        f"stop:dexter:{dexter_plan.plan_id}:{FailureCode.INVALID_STATUS_TRANSITION.value}",
        f"status:dexter:{dexter_plan.plan_id}",
        f"snapshot:dexter:{dexter_plan.plan_id}",
    ]
