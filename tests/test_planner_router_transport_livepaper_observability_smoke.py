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
    ReconcilingStatusSink,
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
CREATED_AT = datetime(2026, 3, 26, 13, 18, tzinfo=timezone.utc)
MANUAL_LATCHED_STOP_ALL = "manual_latched_stop_all"


class ObservabilityMirrorPlanStore:
    def __init__(self, observation_log: list[dict[str, object]] | None = None) -> None:
        self.batches = []
        self.current_statuses: dict[str, PlanStatus] = {}
        self.status_sequences: defaultdict[str, list[PlanStatus]] = defaultdict(list)
        self.detail_sequences: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
        self.observation_log = observation_log if observation_log is not None else []

    def put_batch(self, batch) -> None:
        self.batches.append(batch)
        self.observation_log.append(
            {
                "stage": "plan_store",
                "plan_batch_id": batch.plan_batch_id,
                "request_id": batch.request_id,
                "plan_count": len(batch.plans),
            }
        )
        for plan in batch.plans:
            self.current_statuses[plan.plan_id] = plan.status
            self.status_sequences[plan.plan_id].append(plan.status)
            self.detail_sequences[plan.plan_id].append(
                {
                    "origin": "plan_store",
                    "plan_id": plan.plan_id,
                    "plan_batch_id": plan.plan_batch_id,
                    "objective_profile_id": plan.objective_profile_id,
                    "status": plan.status.value,
                    "source": plan.route.selected_source.value,
                    "selected_sleeve_id": plan.route.selected_sleeve_id,
                    "monitor_profile_id": plan.monitor_binding.monitor_profile_id,
                    "timeout_envelope_class": plan.monitor_binding.timeout_envelope_class,
                    "quarantine_scope": plan.monitor_binding.quarantine_scope,
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


class MirroringReconcilingStatusSink(ReconcilingStatusSink):
    def __init__(self, store: ObservabilityMirrorPlanStore) -> None:
        super().__init__()
        self.store = store

    def record(self, snapshot: StatusSnapshot) -> None:
        super().record(snapshot)
        self.store.apply_snapshot(snapshot)


class ObservabilityLivePaperTransportAdapter(SourceFaithfulTransportAdapter):
    def __init__(self, *, observation_log: list[dict[str, object]], **kwargs) -> None:
        super().__init__(**kwargs)
        self.observation_log = observation_log
        self.handles_by_plan_id: dict[str, object] = {}

    def _record(self, stage: str, **fields: object) -> None:
        self.observation_log.append({"stage": stage, "source": self.source.value, **fields})

    def prepare(self, plan):
        handle = super().prepare(plan)
        self.handles_by_plan_id.setdefault(plan.plan_id, handle)
        self._record(
            "prepare",
            plan_id=plan.plan_id,
            plan_batch_id=plan.plan_batch_id,
            handle_id=handle.handle_id,
            ack_state=handle.native_handle["ack_state"],
            transport_version=handle.native_handle["transport_version"],
            status_delivery=handle.native_handle["status_delivery"],
            execution_mode=handle.native_handle["execution_mode"],
            entrypoint=handle.native_handle["entrypoint"],
            startup_method=handle.native_handle["startup_method"],
            monitor_profile_id=plan.monitor_binding.monitor_profile_id,
            timeout_envelope_class=plan.monitor_binding.timeout_envelope_class,
            quarantine_scope=plan.monitor_binding.quarantine_scope,
            executor_profile_id=plan.executor_binding.executor_profile_id,
            pinned_commit=plan.executor_binding.pinned_commit,
        )
        return handle

    async def start(self, handle) -> None:
        await super().start(handle)
        session = self._session_for_handle(handle)
        self._record(
            "start",
            plan_id=handle.plan_id,
            handle_id=session.handle_id,
            ack_state=session.last_start_ack_state.value,
        )

    async def status(self, handle):
        try:
            snapshot = await super().status(handle)
        except Exception as exc:
            failure = getattr(exc, "failure", None)
            self._record(
                "status_error",
                plan_id=handle.plan_id,
                handle_id=handle.handle_id,
                failure_code=failure.code.value if failure is not None else type(exc).__name__,
                failure_stage=failure.stage if failure is not None else "status",
                source_reason=failure.source_reason if failure is not None else str(exc),
                detail=dict(failure.detail) if failure is not None else {"error": str(exc)},
            )
            raise
        self._record(
            "status",
            plan_id=handle.plan_id,
            handle_id=handle.handle_id,
            status=snapshot.status.value,
            source_reason=snapshot.source_reason,
            detail=dict(snapshot.detail),
        )
        return snapshot

    async def stop(self, handle, reason: str) -> None:
        await super().stop(handle, reason)
        session = self._session_for_handle(handle)
        self._record(
            "stop",
            plan_id=handle.plan_id,
            handle_id=session.handle_id,
            stop_reason=session.last_stop_reason,
            ack_state=session.last_stop_ack_state.value,
        )

    async def snapshot(self, handle):
        snapshot = await super().snapshot(handle)
        self._record(
            "snapshot",
            plan_id=handle.plan_id,
            handle_id=handle.handle_id,
            detail=dict(snapshot),
        )
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


def build_observability_registry(
    observation_log: list[dict[str, object]],
    *,
    dexter_failure_mode: TransportFailureMode | None = None,
    mewx_failure_mode: TransportFailureMode | None = None,
):
    dexter_adapter = ObservabilityLivePaperTransportAdapter(
        observation_log=observation_log,
        source=Source.DEXTER,
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
        failure_mode=dexter_failure_mode,
    )
    mewx_adapter = ObservabilityLivePaperTransportAdapter(
        observation_log=observation_log,
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
    store: ObservabilityMirrorPlanStore,
    sink: MirroringReconcilingStatusSink,
    snapshot: StatusSnapshot,
) -> None:
    validate_transition(store.current_status(plan.plan_id), snapshot.status)
    sink.record(snapshot)


async def start_plan(
    plan,
    handle,
    adapter: ObservabilityLivePaperTransportAdapter,
    store: ObservabilityMirrorPlanStore,
    sink: MirroringReconcilingStatusSink,
) -> StatusSnapshot:
    starting_snapshot = normalize_status_update(
        plan,
        PlanStatus.STARTING.value,
        detail={"stage": "start", "signal": "start_requested", "handle_id": handle.handle_id},
    )
    record_snapshot(plan, store, sink, starting_snapshot)
    await adapter.start(handle)
    await adapter.start(handle)
    running_snapshot = await adapter.status(handle)
    record_snapshot(plan, store, sink, running_snapshot)
    return running_snapshot


async def propagate_manual_latched_stop_all(
    batch,
    store: ObservabilityMirrorPlanStore,
    sink: MirroringReconcilingStatusSink,
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


def test_transport_livepaper_observability_smoke_traces_handoff_lifecycle_and_fan_in(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    observation_log: list[dict[str, object]] = []
    store = ObservabilityMirrorPlanStore(observation_log)
    sink = MirroringReconcilingStatusSink(store)
    registry, dexter_adapter, mewx_adapter = build_observability_registry(observation_log)

    batch = plan_request(
        PlanRequest(
            plan_request_id="req-transport-livepaper-observability-overlay",
            objective_profile_id="dexter_with_mewx_overlay",
        ),
        config_root,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )

    first_handles = {}
    duplicate_handles = {}
    for plan in batch.plans:
        adapter = registry.adapter_for(plan)
        first_handles[plan.plan_id] = adapter.prepare(plan)
        duplicate_handles[plan.plan_id] = adapter.prepare(plan)

    dexter_plan, mewx_plan = batch.plans
    dexter_handle = first_handles[dexter_plan.plan_id]
    mewx_handle = first_handles[mewx_plan.plan_id]

    dexter_running = asyncio.run(start_plan(dexter_plan, dexter_handle, dexter_adapter, store, sink))
    mewx_running = asyncio.run(start_plan(mewx_plan, mewx_handle, mewx_adapter, store, sink))

    mewx_adapter.queue_push_snapshot(
        mewx_handle,
        PlanStatus.QUARANTINED,
        source_reason="mewx_timeout_guard",
        detail={
            "signal": "push_quarantine",
            "monitor_profile_id": mewx_plan.monitor_binding.monitor_profile_id,
            "quarantine_scope": mewx_plan.monitor_binding.quarantine_scope,
            "quarantine_reason": "timeout_guard",
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

    dexter_prepare = [
        entry
        for entry in observation_log
        if entry["stage"] == "prepare" and entry["plan_id"] == dexter_plan.plan_id
    ]
    mewx_prepare = [
        entry
        for entry in observation_log
        if entry["stage"] == "prepare" and entry["plan_id"] == mewx_plan.plan_id
    ]
    dexter_start = [
        entry
        for entry in observation_log
        if entry["stage"] == "start" and entry["plan_id"] == dexter_plan.plan_id
    ]
    mewx_start = [
        entry
        for entry in observation_log
        if entry["stage"] == "start" and entry["plan_id"] == mewx_plan.plan_id
    ]
    accepted_stops = [
        entry
        for entry in observation_log
        if entry["stage"] == "stop" and entry["ack_state"] == AckState.ACCEPTED.value
    ]
    duplicate_stops = [
        entry
        for entry in observation_log
        if entry["stage"] == "stop" and entry["ack_state"] == AckState.DUPLICATE.value
    ]

    assert store.batches[0] is batch
    assert set(sink.latest_by_plan_id) == {dexter_plan.plan_id, mewx_plan.plan_id}
    assert first_handles[dexter_plan.plan_id].handle_id == duplicate_handles[dexter_plan.plan_id].handle_id
    assert first_handles[mewx_plan.plan_id].handle_id == duplicate_handles[mewx_plan.plan_id].handle_id
    assert [entry["ack_state"] for entry in dexter_prepare] == [
        AckState.ACCEPTED.value,
        AckState.DUPLICATE.value,
    ]
    assert [entry["ack_state"] for entry in mewx_prepare] == [
        AckState.ACCEPTED.value,
        AckState.DUPLICATE.value,
    ]
    assert [entry["ack_state"] for entry in dexter_start] == [
        AckState.ACCEPTED.value,
        AckState.DUPLICATE.value,
    ]
    assert [entry["ack_state"] for entry in mewx_start] == [
        AckState.ACCEPTED.value,
        AckState.DUPLICATE.value,
    ]
    assert dexter_prepare[0]["execution_mode"] == "paper_live"
    assert dexter_prepare[0]["entrypoint"] == "monitor_mint_session"
    assert mewx_prepare[0]["execution_mode"] == "sim_live"
    assert mewx_prepare[0]["entrypoint"] == "sim_session"
    assert store.detail_sequences[dexter_plan.plan_id][0] == {
        "origin": "plan_store",
        "plan_id": dexter_plan.plan_id,
        "plan_batch_id": dexter_plan.plan_batch_id,
        "objective_profile_id": dexter_plan.objective_profile_id,
        "status": PlanStatus.PLANNED.value,
        "source": Source.DEXTER.value,
        "selected_sleeve_id": dexter_plan.route.selected_sleeve_id,
        "monitor_profile_id": dexter_plan.monitor_binding.monitor_profile_id,
        "timeout_envelope_class": dexter_plan.monitor_binding.timeout_envelope_class,
        "quarantine_scope": dexter_plan.monitor_binding.quarantine_scope,
        "executor_profile_id": dexter_plan.executor_binding.executor_profile_id,
        "pinned_commit": dexter_plan.executor_binding.pinned_commit,
    }
    assert store.detail_sequences[mewx_plan.plan_id][0]["monitor_profile_id"] == mewx_plan.monitor_binding.monitor_profile_id
    assert store.detail_sequences[mewx_plan.plan_id][0]["pinned_commit"] == FROZEN_PINS.mewx
    assert dexter_running.status is PlanStatus.RUNNING
    assert dexter_running.detail["handle_id"] == dexter_handle.handle_id
    assert dexter_running.detail["ack_state"] == AckState.DUPLICATE.value
    assert dexter_running.detail["execution_mode"] == "paper_live"
    assert mewx_running.status is PlanStatus.RUNNING
    assert mewx_running.detail["handle_id"] == mewx_handle.handle_id
    assert mewx_running.detail["ack_state"] == AckState.DUPLICATE.value
    assert mewx_running.detail["execution_mode"] == "sim_live"
    assert mewx_quarantined.status is PlanStatus.QUARANTINED
    assert mewx_quarantined.source_reason == "mewx_timeout_guard"
    assert mewx_quarantined.detail["quarantine_reason"] == "timeout_guard"
    assert mewx_quarantined.detail["monitor_profile_id"] == mewx_plan.monitor_binding.monitor_profile_id
    assert mewx_quarantined.detail["quarantine_scope"] == mewx_plan.monitor_binding.quarantine_scope
    assert mewx_quarantined.detail["reconciliation_decision"] == "push_promoted"
    assert mewx_quarantined.detail["push_status"] == PlanStatus.QUARANTINED.value
    assert [snapshot.status for snapshot in stopping_snapshots] == [PlanStatus.STOPPING, PlanStatus.STOPPING]
    assert [snapshot.status for snapshot in stopped_snapshots] == [PlanStatus.STOPPED, PlanStatus.STOPPED]
    assert [entry["source"] for entry in accepted_stops] == [Source.MEWX.value, Source.DEXTER.value]
    assert [entry["source"] for entry in duplicate_stops] == [Source.MEWX.value, Source.DEXTER.value]
    assert [status.value for status in store.status_sequences[dexter_plan.plan_id]] == [
        PlanStatus.PLANNED.value,
        PlanStatus.STARTING.value,
        PlanStatus.RUNNING.value,
        PlanStatus.STOPPING.value,
        PlanStatus.STOPPED.value,
    ]
    assert [status.value for status in store.status_sequences[mewx_plan.plan_id]] == [
        PlanStatus.PLANNED.value,
        PlanStatus.STARTING.value,
        PlanStatus.RUNNING.value,
        PlanStatus.QUARANTINED.value,
        PlanStatus.STOPPING.value,
        PlanStatus.STOPPED.value,
    ]
    assert store.detail_sequences[dexter_plan.plan_id][-1]["handle_id"] == dexter_handle.handle_id
    assert store.detail_sequences[mewx_plan.plan_id][-1]["handle_id"] == mewx_handle.handle_id
    assert store.detail_sequences[dexter_plan.plan_id][-1]["halt_mode"] == MANUAL_LATCHED_STOP_ALL
    assert store.detail_sequences[mewx_plan.plan_id][-1]["halt_mode"] == MANUAL_LATCHED_STOP_ALL
    assert store.detail_sequences[dexter_plan.plan_id][-1]["stop_reason"] == MANUAL_LATCHED_STOP_ALL
    assert store.detail_sequences[mewx_plan.plan_id][-1]["stop_reason"] == MANUAL_LATCHED_STOP_ALL
    assert store.detail_sequences[dexter_plan.plan_id][-1]["adapter_snapshot"]["execution_mode"] == "paper_live"
    assert store.detail_sequences[mewx_plan.plan_id][-1]["adapter_snapshot"]["execution_mode"] == "sim_live"
    assert terminal_snapshots[dexter_plan.plan_id]["stop_reason"] == MANUAL_LATCHED_STOP_ALL
    assert terminal_snapshots[mewx_plan.plan_id]["stop_reason"] == MANUAL_LATCHED_STOP_ALL
    assert sink.latest_by_plan_id[dexter_plan.plan_id].status is PlanStatus.STOPPED
    assert sink.latest_by_plan_id[mewx_plan.plan_id].status is PlanStatus.STOPPED


def test_transport_livepaper_observability_smoke_surfaces_normalized_failure_detail(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    observation_log: list[dict[str, object]] = []
    store = ObservabilityMirrorPlanStore(observation_log)
    sink = MirroringReconcilingStatusSink(store)
    registry, dexter_adapter, mewx_adapter = build_observability_registry(
        observation_log,
        mewx_failure_mode=TransportFailureMode(status_timeout=True),
    )

    snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(
                plan_request_id="req-transport-livepaper-observability-timeout",
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
    accepted_stops = [
        entry
        for entry in observation_log
        if entry["stage"] == "stop" and entry["ack_state"] == AckState.ACCEPTED.value
    ]

    assert [snapshot.status for snapshot in snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.FAILED,
        PlanStatus.FAILED,
    ]
    assert mewx_failure.source_reason == "status timeout"
    assert mewx_failure.detail["failure_code"] == "status_timeout"
    assert mewx_failure.detail["stage"] == "status"
    assert mewx_failure.detail["rollback_confirmed"] is True
    assert mewx_failure.detail["rollback_confirmation_source"] == "snapshot"
    assert mewx_failure.detail["handle_id"] == mewx_adapter.handles_by_plan_id[mewx_plan.plan_id].handle_id
    assert mewx_failure.detail["signal"] == "status_poll"
    assert mewx_failure.detail["poll_counter"] == 1
    assert mewx_failure.detail["rollback_snapshot"]["execution_mode"] == "sim_live"
    assert mewx_failure.detail["rollback_snapshot"]["stop_reason"] == "status_timeout"
    assert dexter_failure.detail["rollback_confirmed"] is True
    assert dexter_failure.detail["rollback_confirmation_source"] == "snapshot"
    assert dexter_failure.detail["rollback_snapshot"]["execution_mode"] == "paper_live"
    assert dexter_failure.detail["rollback_snapshot"]["stop_reason"] == "status_timeout"
    assert sink.latest_by_plan_id[mewx_plan.plan_id].detail["rollback_snapshot"]["stop_reason"] == "status_timeout"
    assert sink.latest_by_plan_id[dexter_plan.plan_id].detail["rollback_snapshot"]["stop_reason"] == "status_timeout"
    assert [entry["source"] for entry in accepted_stops] == [Source.MEWX.value, Source.DEXTER.value]
    assert dexter_adapter.handles_by_plan_id[dexter_plan.plan_id].native_handle["execution_mode"] == "paper_live"
    assert mewx_adapter.handles_by_plan_id[mewx_plan.plan_id].native_handle["execution_mode"] == "sim_live"


def test_transport_livepaper_observability_smoke_proof_tracks_runtime_as_next_step() -> None:
    proof = json.loads(
        (
            REPO_ROOT
            / "artifacts"
            / "proofs"
            / "task-007-transport-livepaper-observability-smoke-check.json"
        ).read_text()
    )

    assert proof["task_id"] == "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-SMOKE"
    assert proof["verified_github"]["latest_vexter_pr"] == 46
    assert proof["transport_livepaper_observability_smoke"]["status_sink_fan_in"]["both_sources_visible"] is True
    assert proof["transport_livepaper_observability_smoke"]["ack_metadata"]["accepted_and_duplicate_visible"] is True
    assert proof["transport_livepaper_observability_smoke"]["failure_detail"]["source_reason_passthrough"] is True
    assert proof["task_result"]["task_state"] == "transport_livepaper_observability_smoke_passed"
    assert proof["task_result"]["recommended_next_step"] == "transport_livepaper_observability_runtime"
