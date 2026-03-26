import asyncio
import json
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vexter.planner_router.dispatch_state_machine import normalize_status_update, validate_transition
from vexter.planner_router.errors import ConfigValidationError
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
CREATED_AT = datetime(2026, 3, 26, 3, 24, tzinfo=timezone.utc)
MANUAL_LATCHED_STOP_ALL = "manual_latched_stop_all"


class LivePaperMirrorPlanStore:
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
                    "monitor_profile_id": plan.monitor_binding.monitor_profile_id,
                    "timeout_envelope_class": plan.monitor_binding.timeout_envelope_class,
                    "executor_profile_id": plan.executor_binding.executor_profile_id,
                    "pinned_commit": plan.executor_binding.pinned_commit,
                }
            )

    def apply_snapshot(self, snapshot: StatusSnapshot) -> None:
        self.current_statuses[snapshot.plan_id] = snapshot.status
        self.status_sequences[snapshot.plan_id].append(snapshot.status)
        self.detail_sequences[snapshot.plan_id].append(dict(snapshot.detail))

    def current_status(self, plan_id: str) -> PlanStatus:
        return self.current_statuses[plan_id]


class MirroringStatusSink:
    def __init__(self, store: LivePaperMirrorPlanStore) -> None:
        self.store = store
        self.snapshots = []

    def record(self, snapshot: StatusSnapshot) -> None:
        self.snapshots.append(snapshot)
        self.store.apply_snapshot(snapshot)


def _paper_execution_mode(source: Source) -> str:
    return "paper_live" if source is Source.DEXTER else "sim_live"


def _paper_entrypoint(plan) -> str:
    if plan.route.selected_source is Source.DEXTER:
        return "monitor_mint_session"
    return "sim_session"


class LivePaperScriptedAdapter:
    def __init__(self, source: Source, events: list[str]) -> None:
        self.source = source
        self.events = events
        self.handles: dict[str, DispatchHandle] = {}
        self.prepared_sessions: list[dict[str, object]] = []
        self.started = []
        self.stopped = []

    def prepare(self, plan) -> DispatchHandle:
        execution_mode = _paper_execution_mode(self.source)
        entrypoint = _paper_entrypoint(plan)
        session_manifest = {
            "plan_id": plan.plan_id,
            "source": self.source.value,
            "execution_mode": execution_mode,
            "entrypoint": entrypoint,
            "monitor_profile_id": plan.monitor_binding.monitor_profile_id,
            "timeout_envelope_class": plan.monitor_binding.timeout_envelope_class,
            "quarantine_scope": plan.monitor_binding.quarantine_scope,
            "global_halt_participation": plan.monitor_binding.global_halt_participation,
            "pinned_commit": plan.executor_binding.pinned_commit,
        }
        handle = DispatchHandle(
            plan_id=plan.plan_id,
            source=plan.route.selected_source,
            native_handle={
                "paper_session_id": f"{execution_mode}:{plan.plan_id}",
                **session_manifest,
            },
            plan=plan,
        )
        self.events.append(f"prepare:{self.source.value}:{plan.plan_id}")
        self.handles[plan.plan_id] = handle
        self.prepared_sessions.append(session_manifest)
        return handle

    async def start(self, handle: DispatchHandle) -> None:
        self.events.append(f"start:{self.source.value}:{handle.plan_id}")
        self.started.append(handle.plan_id)

    async def status(self, handle: DispatchHandle) -> StatusSnapshot:
        self.events.append(f"status:{self.source.value}:{handle.plan_id}")
        return StatusSnapshot(
            plan_id=handle.plan_id,
            status=PlanStatus.RUNNING,
            source_reason=None,
            observed_at_utc=datetime.now(timezone.utc),
            detail={
                "signal": "status_poll",
                "source": self.source.value,
                "execution_mode": handle.native_handle["execution_mode"],
                "entrypoint": handle.native_handle["entrypoint"],
                "pinned_commit": handle.native_handle["pinned_commit"],
            },
        )

    async def stop(self, handle: DispatchHandle, reason: str) -> None:
        self.events.append(f"stop:{self.source.value}:{handle.plan_id}:{reason}")
        self.stopped.append((handle.plan_id, reason))

    async def snapshot(self, handle: DispatchHandle):
        self.events.append(f"snapshot:{self.source.value}:{handle.plan_id}")
        return {
            "paper_session_id": handle.native_handle["paper_session_id"],
            "execution_mode": handle.native_handle["execution_mode"],
            "entrypoint": handle.native_handle["entrypoint"],
            "pinned_commit": handle.native_handle["pinned_commit"],
        }


class ExecutorRegistry:
    def __init__(self, dexter_adapter: LivePaperScriptedAdapter, mewx_adapter: LivePaperScriptedAdapter) -> None:
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


def activate_global_halt(config_root: Path) -> None:
    planner_path = config_root / "planner.json"
    payload = json.loads(planner_path.read_text())
    payload["global_halt_policy"]["active"] = True
    planner_path.write_text(json.dumps(payload, indent=2) + "\n")


def build_registry(
    events: list[str],
) -> tuple[ExecutorRegistry, LivePaperScriptedAdapter, LivePaperScriptedAdapter]:
    dexter_adapter = LivePaperScriptedAdapter(Source.DEXTER, events)
    mewx_adapter = LivePaperScriptedAdapter(Source.MEWX, events)
    return ExecutorRegistry(dexter_adapter, mewx_adapter), dexter_adapter, mewx_adapter


async def trigger_profile_bound_quarantine(
    batch,
    store: LivePaperMirrorPlanStore,
    sink: MirroringStatusSink,
    *,
    quarantine_plan_id: str,
    trigger_reason: str,
) -> list[StatusSnapshot]:
    plans_by_id = {plan.plan_id: plan for plan in batch.plans}
    trigger_plan = plans_by_id[quarantine_plan_id]
    quarantine_snapshot = normalize_status_update(
        trigger_plan,
        PlanStatus.QUARANTINED.value,
        source_reason=trigger_reason,
        detail={
            "signal": "quarantine",
            "trigger_reason": trigger_reason,
            "trigger_plan_id": quarantine_plan_id,
            "monitor_profile_id": trigger_plan.monitor_binding.monitor_profile_id,
            "timeout_envelope_class": trigger_plan.monitor_binding.timeout_envelope_class,
            "quarantine_scope": trigger_plan.monitor_binding.quarantine_scope,
        },
    )
    validate_transition(store.current_status(quarantine_plan_id), quarantine_snapshot.status)
    sink.record(quarantine_snapshot)
    return [quarantine_snapshot]


async def propagate_manual_latched_stop_all(
    batch,
    store: LivePaperMirrorPlanStore,
    sink: MirroringStatusSink,
    registry: ExecutorRegistry,
    *,
    trigger_plan_id: str,
) -> list[StatusSnapshot]:
    snapshots: list[StatusSnapshot] = []
    for plan in reversed(batch.plans):
        stopping_snapshot = normalize_status_update(
            plan,
            PlanStatus.STOPPING.value,
            source_reason=MANUAL_LATCHED_STOP_ALL,
            detail={
                "signal": "stop",
                "stop_reason": MANUAL_LATCHED_STOP_ALL,
                "halt_mode": MANUAL_LATCHED_STOP_ALL,
                "trigger_plan_id": trigger_plan_id,
            },
        )
        validate_transition(store.current_status(plan.plan_id), stopping_snapshot.status)
        sink.record(stopping_snapshot)
        snapshots.append(stopping_snapshot)

        adapter = registry.adapter_for(plan)
        handle = adapter.handles[plan.plan_id]
        await adapter.stop(handle, reason=MANUAL_LATCHED_STOP_ALL)
        final_snapshot = normalize_status_update(
            plan,
            PlanStatus.STOPPED.value,
            source_reason=None,
            detail={
                "signal": "halt_latched",
                "stop_reason": MANUAL_LATCHED_STOP_ALL,
                "halt_mode": MANUAL_LATCHED_STOP_ALL,
                "trigger_plan_id": trigger_plan_id,
                "adapter_snapshot": await adapter.snapshot(handle),
            },
        )
        validate_transition(store.current_status(plan.plan_id), final_snapshot.status)
        sink.record(final_snapshot)
        snapshots.append(final_snapshot)

    return snapshots


def test_plan_request_livepaper_smoke_emits_overlay_batch_for_source_faithful_paper_seams(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    events: list[str] = []
    store = LivePaperMirrorPlanStore(events)
    registry, dexter_adapter, mewx_adapter = build_registry(events)

    batch = plan_request(
        PlanRequest(plan_request_id="req-livepaper-plan", objective_profile_id="dexter_with_mewx_overlay"),
        config_root,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )

    handles = [registry.adapter_for(plan).prepare(plan) for plan in batch.plans]
    dexter_plan, mewx_plan = batch.plans

    assert [plan.route.selected_source for plan in batch.plans] == [Source.DEXTER, Source.MEWX]
    assert [plan.monitor_binding.monitor_profile_id for plan in batch.plans] == [
        "dexter_default",
        "mewx_timeout_guard",
    ]
    assert [plan.executor_binding.pinned_commit for plan in batch.plans] == [
        FROZEN_PINS.dexter,
        FROZEN_PINS.mewx,
    ]
    assert [store.current_status(plan.plan_id) for plan in batch.plans] == [
        PlanStatus.PLANNED,
        PlanStatus.PLANNED,
    ]
    assert store.detail_sequences[dexter_plan.plan_id][0]["monitor_profile_id"] == "dexter_default"
    assert store.detail_sequences[mewx_plan.plan_id][0]["monitor_profile_id"] == "mewx_timeout_guard"
    assert handles[0].native_handle["execution_mode"] == "paper_live"
    assert handles[0].native_handle["entrypoint"] == "monitor_mint_session"
    assert handles[1].native_handle["execution_mode"] == "sim_live"
    assert handles[1].native_handle["entrypoint"] == "sim_session"
    assert dexter_adapter.prepared_sessions == [
        {
            "plan_id": dexter_plan.plan_id,
            "source": "dexter",
            "execution_mode": "paper_live",
            "entrypoint": "monitor_mint_session",
            "monitor_profile_id": "dexter_default",
            "timeout_envelope_class": "dexter_lifecycle_control",
            "quarantine_scope": "sleeve",
            "global_halt_participation": True,
            "pinned_commit": FROZEN_PINS.dexter,
        }
    ]
    assert mewx_adapter.prepared_sessions == [
        {
            "plan_id": mewx_plan.plan_id,
            "source": "mewx",
            "execution_mode": "sim_live",
            "entrypoint": "sim_session",
            "monitor_profile_id": "mewx_timeout_guard",
            "timeout_envelope_class": "mewx_timeout_tolerant",
            "quarantine_scope": "sleeve",
            "global_halt_participation": True,
            "pinned_commit": FROZEN_PINS.mewx,
        }
    ]
    assert events == [
        "store:req-livepaper-plan:batch",
        f"prepare:dexter:{dexter_plan.plan_id}",
        f"prepare:mewx:{mewx_plan.plan_id}",
    ]


def test_plan_request_livepaper_smoke_rejects_active_global_halt_without_partial_batch(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    activate_global_halt(config_root)
    store = LivePaperMirrorPlanStore()

    with pytest.raises(ConfigValidationError) as exc_info:
        plan_request(
            PlanRequest(plan_request_id="req-livepaper-halt", objective_profile_id="dexter_with_mewx_overlay"),
            config_root,
            FROZEN_PINS,
            store,
            CREATED_AT,
        )

    assert exc_info.value.failure is not None
    assert exc_info.value.failure.code is FailureCode.GLOBAL_HALT_ACTIVE
    assert store.batches == []


def test_plan_and_dispatch_livepaper_smoke_progresses_overlay_batch_through_quarantine_and_manual_halt(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    events: list[str] = []
    store = LivePaperMirrorPlanStore(events)
    sink = MirroringStatusSink(store)
    registry, dexter_adapter, mewx_adapter = build_registry(events)

    dispatch_snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(plan_request_id="req-livepaper-overlay", objective_profile_id="dexter_with_mewx_overlay"),
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
    quarantine_snapshots = asyncio.run(
        trigger_profile_bound_quarantine(
            batch,
            store,
            sink,
            quarantine_plan_id=mewx_plan.plan_id,
            trigger_reason="shutdown_confirmation_missing",
        )
    )
    halt_snapshots = asyncio.run(
        propagate_manual_latched_stop_all(
            batch,
            store,
            sink,
            registry,
            trigger_plan_id=mewx_plan.plan_id,
        )
    )

    assert [snapshot.status for snapshot in dispatch_snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
    ]
    assert [snapshot.status for snapshot in quarantine_snapshots] == [PlanStatus.QUARANTINED]
    assert [snapshot.status for snapshot in halt_snapshots] == [
        PlanStatus.STOPPING,
        PlanStatus.STOPPED,
        PlanStatus.STOPPING,
        PlanStatus.STOPPED,
    ]
    assert [status.value for status in store.status_sequences[dexter_plan.plan_id]] == [
        "planned",
        "starting",
        "running",
        "stopping",
        "stopped",
    ]
    assert [status.value for status in store.status_sequences[mewx_plan.plan_id]] == [
        "planned",
        "starting",
        "running",
        "quarantined",
        "stopping",
        "stopped",
    ]
    assert store.detail_sequences[mewx_plan.plan_id][3] == {
        "signal": "quarantine",
        "trigger_reason": "shutdown_confirmation_missing",
        "trigger_plan_id": mewx_plan.plan_id,
        "monitor_profile_id": "mewx_timeout_guard",
        "timeout_envelope_class": "mewx_timeout_tolerant",
        "quarantine_scope": "sleeve",
    }
    assert store.detail_sequences[mewx_plan.plan_id][-1]["halt_mode"] == MANUAL_LATCHED_STOP_ALL
    assert store.detail_sequences[dexter_plan.plan_id][-1]["halt_mode"] == MANUAL_LATCHED_STOP_ALL
    assert store.detail_sequences[dexter_plan.plan_id][-1]["adapter_snapshot"]["execution_mode"] == "paper_live"
    assert store.detail_sequences[mewx_plan.plan_id][-1]["adapter_snapshot"]["execution_mode"] == "sim_live"
    assert sink.snapshots == dispatch_snapshots + quarantine_snapshots + halt_snapshots
    assert dexter_adapter.started == [dexter_plan.plan_id]
    assert mewx_adapter.started == [mewx_plan.plan_id]
    assert dexter_adapter.stopped == [(dexter_plan.plan_id, MANUAL_LATCHED_STOP_ALL)]
    assert mewx_adapter.stopped == [(mewx_plan.plan_id, MANUAL_LATCHED_STOP_ALL)]
    assert events == [
        "store:req-livepaper-overlay:batch",
        f"prepare:dexter:{dexter_plan.plan_id}",
        f"prepare:mewx:{mewx_plan.plan_id}",
        f"start:dexter:{dexter_plan.plan_id}",
        f"status:dexter:{dexter_plan.plan_id}",
        f"start:mewx:{mewx_plan.plan_id}",
        f"status:mewx:{mewx_plan.plan_id}",
        f"stop:mewx:{mewx_plan.plan_id}:{MANUAL_LATCHED_STOP_ALL}",
        f"snapshot:mewx:{mewx_plan.plan_id}",
        f"stop:dexter:{dexter_plan.plan_id}:{MANUAL_LATCHED_STOP_ALL}",
        f"snapshot:dexter:{dexter_plan.plan_id}",
    ]
