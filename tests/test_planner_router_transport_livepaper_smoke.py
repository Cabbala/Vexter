import asyncio
import json
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from vexter.planner_router.dispatch_state_machine import normalize_status_update, validate_transition
from vexter.planner_router.models import PlanRequest, PlanStatus, Source, SourcePinRegistry, StatusSnapshot
from vexter.planner_router.planner import plan_and_dispatch, plan_request
from vexter.planner_router.transport import (
    AckState,
    SourceFaithfulTransportAdapter,
    TransportExecutorRegistry,
    TransportFailureMode,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "config" / "planner_router"
FROZEN_PINS = SourcePinRegistry(
    dexter="ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    mewx="dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
)
CREATED_AT = datetime(2026, 3, 26, 12, 24, tzinfo=timezone.utc)
MANUAL_LATCHED_STOP_ALL = "manual_latched_stop_all"


class LivePaperTransportMirrorPlanStore:
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
    def __init__(self, store: LivePaperTransportMirrorPlanStore) -> None:
        self.store = store
        self.snapshots = []

    def record(self, snapshot: StatusSnapshot) -> None:
        self.snapshots.append(snapshot)
        self.store.apply_snapshot(snapshot)


class RecordingLivePaperTransportAdapter(SourceFaithfulTransportAdapter):
    def __init__(self, *, events: list[str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.events = events
        self.handles_by_plan_id: dict[str, object] = {}
        self.prepared_manifests: list[dict[str, object]] = []

    def prepare(self, plan):
        handle = super().prepare(plan)
        self.handles_by_plan_id.setdefault(plan.plan_id, handle)
        self.prepared_manifests.append(
            {
                "plan_id": plan.plan_id,
                "source": self.source.value,
                "handle_id": handle.handle_id,
                "execution_mode": handle.native_handle["execution_mode"],
                "entrypoint": handle.native_handle["entrypoint"],
                "monitor_profile_id": plan.monitor_binding.monitor_profile_id,
                "timeout_envelope_class": plan.monitor_binding.timeout_envelope_class,
                "pinned_commit": plan.executor_binding.pinned_commit,
                "ack_state": handle.native_handle["ack_state"],
            }
        )
        self.events.append(
            f"prepare:{self.source.value}:{plan.plan_id}:{handle.handle_id}:{handle.native_handle['ack_state']}"
        )
        return handle

    async def start(self, handle) -> None:
        await super().start(handle)
        session = self._session_for_handle(handle)
        self.events.append(f"start:{self.source.value}:{handle.plan_id}:{session.last_start_ack_state.value}")

    async def status(self, handle):
        try:
            snapshot = await super().status(handle)
        except Exception as exc:
            failure = getattr(exc, "failure", None)
            code = failure.code.value if failure is not None else type(exc).__name__
            self.events.append(f"status_error:{self.source.value}:{handle.plan_id}:{code}")
            raise
        self.events.append(
            f"status:{self.source.value}:{handle.plan_id}:{snapshot.status.value}:{snapshot.detail.get('reconciliation_decision', 'none')}"
        )
        return snapshot

    async def stop(self, handle, reason: str) -> None:
        await super().stop(handle, reason)
        session = self._session_for_handle(handle)
        self.events.append(
            f"stop:{self.source.value}:{handle.plan_id}:{session.last_stop_reason}:{session.last_stop_ack_state.value}"
        )

    async def snapshot(self, handle):
        snapshot = await super().snapshot(handle)
        self.events.append(f"snapshot:{self.source.value}:{handle.plan_id}:{snapshot['executor_status']}")
        return snapshot


def clone_config_dir(tmp_path: Path) -> Path:
    destination = tmp_path / "planner_router"
    shutil.copytree(CONFIG_ROOT, destination)
    return destination


def enable_mewx_sleeve(config_root: Path) -> None:
    sleeves_path = config_root / "sleeves.json"
    payload = json.loads(sleeves_path.read_text())
    payload[1]["enabled"] = True
    sleeves_path.write_text(json.dumps(payload, indent=2) + "\n")


def build_recording_registry(
    events: list[str],
    *,
    dexter_failure_mode: TransportFailureMode | None = None,
    mewx_failure_mode: TransportFailureMode | None = None,
):
    dexter_adapter = RecordingLivePaperTransportAdapter(
        events=events,
        source=Source.DEXTER,
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
        failure_mode=dexter_failure_mode,
    )
    mewx_adapter = RecordingLivePaperTransportAdapter(
        events=events,
        source=Source.MEWX,
        executor_profile_id="mewx_frozen_pinned",
        pinned_commit=FROZEN_PINS.mewx,
        failure_mode=mewx_failure_mode,
    )
    registry = TransportExecutorRegistry(
        {
            "dexter_main_pinned": dexter_adapter,
            "mewx_frozen_pinned": mewx_adapter,
        }
    )
    return registry, dexter_adapter, mewx_adapter


def record_snapshot(
    plan,
    store: LivePaperTransportMirrorPlanStore,
    sink: MirroringStatusSink,
    snapshot: StatusSnapshot,
) -> None:
    validate_transition(store.current_status(plan.plan_id), snapshot.status)
    sink.record(snapshot)


async def start_plan(
    plan,
    handle,
    adapter: RecordingLivePaperTransportAdapter,
    store: LivePaperTransportMirrorPlanStore,
    sink: MirroringStatusSink,
) -> StatusSnapshot:
    starting_snapshot = normalize_status_update(
        plan,
        PlanStatus.STARTING.value,
        detail={"stage": "start", "handle_id": handle.handle_id},
    )
    record_snapshot(plan, store, sink, starting_snapshot)
    await adapter.start(handle)
    await adapter.start(handle)
    running_snapshot = await adapter.status(handle)
    record_snapshot(plan, store, sink, running_snapshot)
    return running_snapshot


async def propagate_manual_latched_stop_all(
    batch,
    store: LivePaperTransportMirrorPlanStore,
    sink: MirroringStatusSink,
    registry: TransportExecutorRegistry,
    *,
    trigger_plan_id: str,
):
    stopping_snapshots: list[StatusSnapshot] = []
    stopped_snapshots: list[StatusSnapshot] = []
    terminal_snapshots: dict[str, dict[str, object]] = {}

    for plan in reversed(batch.plans):
        adapter = registry.adapter_for(plan)
        handle = adapter.handles_by_plan_id[plan.plan_id]
        await adapter.stop(handle, reason=MANUAL_LATCHED_STOP_ALL)
        await adapter.stop(handle, reason=MANUAL_LATCHED_STOP_ALL)
        stopping_snapshot = await adapter.status(handle)
        record_snapshot(plan, store, sink, stopping_snapshot)
        terminal_snapshot = await adapter.snapshot(handle)
        confirmed_snapshot = await adapter.status(handle)
        final_snapshot = normalize_status_update(
            plan,
            confirmed_snapshot.status.value,
            detail={
                **dict(confirmed_snapshot.detail),
                "signal": "halt_latched",
                "stop_reason": MANUAL_LATCHED_STOP_ALL,
                "halt_mode": MANUAL_LATCHED_STOP_ALL,
                "trigger_plan_id": trigger_plan_id,
                "adapter_snapshot": terminal_snapshot,
            },
        )
        record_snapshot(plan, store, sink, final_snapshot)
        stopping_snapshots.append(stopping_snapshot)
        stopped_snapshots.append(final_snapshot)
        terminal_snapshots[plan.plan_id] = terminal_snapshot

    return stopping_snapshots, stopped_snapshots, terminal_snapshots


def test_transport_livepaper_smoke_preserves_immutable_handoff_and_handle_lifecycle(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    events: list[str] = []
    store = LivePaperTransportMirrorPlanStore(events)
    sink = MirroringStatusSink(store)
    registry, dexter_adapter, mewx_adapter = build_recording_registry(events)

    batch = plan_request(
        PlanRequest(
            plan_request_id="req-transport-livepaper-overlay",
            objective_profile_id="dexter_with_mewx_overlay",
        ),
        config_root,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )

    first_handles = []
    duplicate_handles = []
    for plan in batch.plans:
        adapter = registry.adapter_for(plan)
        first_handles.append(adapter.prepare(plan))
        duplicate_handles.append(adapter.prepare(plan))

    dexter_plan, mewx_plan = batch.plans
    dexter_handle, mewx_handle = first_handles

    dexter_running = asyncio.run(start_plan(dexter_plan, dexter_handle, dexter_adapter, store, sink))
    mewx_running = asyncio.run(start_plan(mewx_plan, mewx_handle, mewx_adapter, store, sink))

    mewx_adapter.queue_push_snapshot(
        mewx_handle,
        PlanStatus.QUARANTINED,
        source_reason="mewx_timeout_guard",
        detail={
            "signal": "push_quarantine",
            "monitor_profile_id": "mewx_timeout_guard",
            "quarantine_scope": "sleeve",
        },
    )
    mewx_quarantined = asyncio.run(mewx_adapter.status(mewx_handle))
    record_snapshot(mewx_plan, store, sink, mewx_quarantined)

    stopping_snapshots, stopped_snapshots, terminal_snapshots = asyncio.run(
        propagate_manual_latched_stop_all(
            batch,
            store,
            sink,
            registry,
            trigger_plan_id=mewx_plan.plan_id,
        )
    )

    assert store.batches[0] is batch
    assert [plan.status for plan in store.batches[0].plans] == [PlanStatus.PLANNED, PlanStatus.PLANNED]
    assert [plan.route.selected_source for plan in batch.plans] == [Source.DEXTER, Source.MEWX]
    assert first_handles[0].handle_id == duplicate_handles[0].handle_id
    assert first_handles[1].handle_id == duplicate_handles[1].handle_id
    assert first_handles[0].native_handle["ack_state"] == AckState.ACCEPTED.value
    assert duplicate_handles[0].native_handle["ack_state"] == AckState.DUPLICATE.value
    assert first_handles[1].native_handle["ack_state"] == AckState.ACCEPTED.value
    assert duplicate_handles[1].native_handle["ack_state"] == AckState.DUPLICATE.value
    assert dexter_handle.native_handle["execution_mode"] == "paper_live"
    assert dexter_handle.native_handle["entrypoint"] == "monitor_mint_session"
    assert dexter_handle.native_handle["startup_method"] is None
    assert mewx_handle.native_handle["execution_mode"] == "sim_live"
    assert mewx_handle.native_handle["entrypoint"] == "sim_session"
    assert mewx_handle.native_handle["startup_method"] == "start_session"
    assert dexter_running.status is PlanStatus.RUNNING
    assert dexter_running.detail["ack_state"] == AckState.DUPLICATE.value
    assert mewx_running.status is PlanStatus.RUNNING
    assert mewx_running.detail["ack_state"] == AckState.DUPLICATE.value
    assert mewx_quarantined.status is PlanStatus.QUARANTINED
    assert mewx_quarantined.detail["reconciliation_mode"] == "poll_first"
    assert mewx_quarantined.detail["reconciliation_decision"] == "push_promoted"
    assert mewx_quarantined.detail["push_status"] == PlanStatus.QUARANTINED.value
    assert [snapshot.status for snapshot in stopping_snapshots] == [PlanStatus.STOPPING, PlanStatus.STOPPING]
    assert [snapshot.detail["ack_state"] for snapshot in stopping_snapshots] == [
        AckState.DUPLICATE.value,
        AckState.DUPLICATE.value,
    ]
    assert [snapshot.status for snapshot in stopped_snapshots] == [PlanStatus.STOPPED, PlanStatus.STOPPED]
    assert terminal_snapshots[mewx_plan.plan_id]["executor_status"] == PlanStatus.STOPPED.value
    assert terminal_snapshots[mewx_plan.plan_id]["stop_reason"] == MANUAL_LATCHED_STOP_ALL
    assert terminal_snapshots[dexter_plan.plan_id]["executor_status"] == PlanStatus.STOPPED.value
    assert terminal_snapshots[dexter_plan.plan_id]["stop_reason"] == MANUAL_LATCHED_STOP_ALL
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
    assert store.detail_sequences[dexter_plan.plan_id][-1]["adapter_snapshot"]["execution_mode"] == "paper_live"
    assert store.detail_sequences[mewx_plan.plan_id][-1]["adapter_snapshot"]["execution_mode"] == "sim_live"
    assert store.detail_sequences[dexter_plan.plan_id][-1]["halt_mode"] == MANUAL_LATCHED_STOP_ALL
    assert store.detail_sequences[mewx_plan.plan_id][-1]["halt_mode"] == MANUAL_LATCHED_STOP_ALL
    assert [event for event in events if event.startswith("stop:") and event.endswith(":accepted")] == [
        f"stop:mewx:{mewx_plan.plan_id}:{MANUAL_LATCHED_STOP_ALL}:accepted",
        f"stop:dexter:{dexter_plan.plan_id}:{MANUAL_LATCHED_STOP_ALL}:accepted",
    ]


def test_transport_livepaper_smoke_normalizes_status_timeout_and_rolls_back_active_handles(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    events: list[str] = []
    store = LivePaperTransportMirrorPlanStore(events)
    sink = MirroringStatusSink(store)
    registry, dexter_adapter, mewx_adapter = build_recording_registry(
        events,
        mewx_failure_mode=TransportFailureMode(status_timeout=True),
    )

    snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(
                plan_request_id="req-transport-livepaper-timeout",
                objective_profile_id="dexter_with_mewx_overlay",
            ),
            config_root,
            FROZEN_PINS,
            store,
            registry,
            sink,
            CREATED_AT,
        )
    )

    dexter_plan, mewx_plan = store.batches[0].plans
    mewx_failure = next(
        snapshot
        for snapshot in snapshots
        if snapshot.plan_id == mewx_plan.plan_id and snapshot.status is PlanStatus.FAILED
    )
    dexter_failure = next(
        snapshot
        for snapshot in snapshots
        if snapshot.plan_id == dexter_plan.plan_id and snapshot.status is PlanStatus.FAILED
    )

    assert [snapshot.status for snapshot in snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.FAILED,
        PlanStatus.FAILED,
    ]
    assert dexter_adapter.handles_by_plan_id[dexter_plan.plan_id].native_handle["execution_mode"] == "paper_live"
    assert mewx_adapter.handles_by_plan_id[mewx_plan.plan_id].native_handle["execution_mode"] == "sim_live"
    assert mewx_failure.source_reason == "status timeout"
    assert mewx_failure.detail["failure_code"] == "status_timeout"
    assert mewx_failure.detail["stage"] == "status"
    assert mewx_failure.detail["rollback_confirmed"] is True
    assert mewx_failure.detail["rollback_confirmation_source"] == "snapshot"
    assert dexter_failure.detail["rollback_confirmed"] is True
    assert dexter_failure.detail["rollback_confirmation_source"] == "snapshot"
    assert [event for event in events if event.startswith("stop:") and event.endswith(":accepted")] == [
        f"stop:mewx:{mewx_plan.plan_id}:status_timeout:accepted",
        f"stop:dexter:{dexter_plan.plan_id}:status_timeout:accepted",
    ]
    assert f"status_error:mewx:{mewx_plan.plan_id}:status_timeout" in events
    assert sink.snapshots == snapshots


def test_transport_livepaper_smoke_proof_tracks_transport_livepaper_observability_as_next_step() -> None:
    proof = json.loads(
        (REPO_ROOT / "artifacts" / "proofs" / "task-007-transport-livepaper-smoke-check.json").read_text()
    )

    assert proof["task_id"] == "TASK-007-TRANSPORT-LIVEPAPER-SMOKE"
    assert proof["verified_github"]["latest_vexter_pr"] == 45
    assert proof["transport_livepaper_smoke"]["immutable_plan_handoff"]["stable_handle_identity"] is True
    assert proof["transport_livepaper_smoke"]["livepaper_quarantine_and_stop_all"]["manual_latched_stop_all"] is True
    assert proof["task_result"]["task_state"] == "transport_livepaper_smoke_passed"
    assert proof["task_result"]["recommended_next_step"] == "transport_livepaper_observability_smoke"
