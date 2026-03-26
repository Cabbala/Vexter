import asyncio
import json
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from vexter.planner_router.dispatch_state_machine import normalize_status_update, validate_transition
from vexter.planner_router.models import PlanRequest, PlanStatus, Source, SourcePinRegistry, StatusSnapshot
from vexter.planner_router.planner import plan_and_dispatch
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
CREATED_AT = datetime(2026, 3, 26, 22, 10, tzinfo=timezone.utc)
MANUAL_LATCHED_STOP_ALL = "manual_latched_stop_all"


class ObservabilityRegressionPlanStore:
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
    def __init__(self, store: ObservabilityRegressionPlanStore) -> None:
        super().__init__()
        self.store = store

    def record(self, snapshot: StatusSnapshot) -> None:
        super().record(snapshot)
        self.store.apply_snapshot(snapshot)


class ObservabilityRegressionTransportAdapter(SourceFaithfulTransportAdapter):
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
            detail=dict(handle.native_handle),
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
            detail={
                "start_request_count": session.start_request_count,
                "start_duplicate_seen": session.start_duplicate_seen,
                "start_terminal_seen": session.start_terminal_seen,
            },
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
            detail={
                "stop_request_count": session.stop_request_count,
                "stop_duplicate_seen": session.stop_duplicate_seen,
                "stop_terminal_seen": session.stop_terminal_seen,
            },
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
    dexter_adapter = ObservabilityRegressionTransportAdapter(
        observation_log=observation_log,
        source=Source.DEXTER,
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
        failure_mode=dexter_failure_mode,
    )
    mewx_adapter = ObservabilityRegressionTransportAdapter(
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
    store: ObservabilityRegressionPlanStore,
    sink: MirroringReconcilingStatusSink,
    snapshot: StatusSnapshot,
) -> None:
    validate_transition(store.current_status(plan.plan_id), snapshot.status)
    sink.record(snapshot)


async def propagate_manual_latched_stop_all(
    batch,
    store: ObservabilityRegressionPlanStore,
    sink: MirroringReconcilingStatusSink,
    registry: TransportExecutorRegistry,
    *,
    trigger_plan_id: str,
):
    stopping_snapshots: dict[str, StatusSnapshot] = {}
    stopped_snapshots: dict[str, StatusSnapshot] = {}
    terminal_snapshots: dict[str, dict[str, object]] = {}

    for plan in reversed(batch.plans):
        adapter = registry.adapter_for(plan)
        handle = adapter.handles_by_plan_id[plan.plan_id]
        await adapter.stop(handle, reason=MANUAL_LATCHED_STOP_ALL)
        await adapter.stop(handle, reason=MANUAL_LATCHED_STOP_ALL)
        adapter.queue_push_snapshot(
            handle,
            PlanStatus.STOPPING,
            source_reason=MANUAL_LATCHED_STOP_ALL,
            detail={
                "signal": "push_stop_confirmation",
                "halt_mode": MANUAL_LATCHED_STOP_ALL,
                "trigger_plan_id": trigger_plan_id,
                "status_sink_fan_in": "same_status_confirmed",
            },
        )
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
        stopping_snapshots[plan.plan_id] = stopping_snapshot
        stopped_snapshots[plan.plan_id] = final_snapshot
        terminal_snapshots[plan.plan_id] = terminal_snapshot

    return stopping_snapshots, stopped_snapshots, terminal_snapshots


def test_transport_livepaper_observability_regression_pack_locks_runtime_metadata_surface(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    observation_log: list[dict[str, object]] = []
    store = ObservabilityRegressionPlanStore(observation_log)
    sink = MirroringReconcilingStatusSink(store)
    registry, dexter_adapter, mewx_adapter = build_observability_registry(observation_log)

    dispatch_snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(
                plan_request_id="req-transport-livepaper-observability-regression-pack-overlay",
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

    batch = store.batches[0]
    dexter_plan, mewx_plan = batch.plans
    dexter_handle = dexter_adapter.handles_by_plan_id[dexter_plan.plan_id]
    mewx_handle = mewx_adapter.handles_by_plan_id[mewx_plan.plan_id]

    dexter_duplicate_handle = dexter_adapter.prepare(dexter_plan)
    mewx_duplicate_handle = mewx_adapter.prepare(mewx_plan)

    asyncio.run(dexter_adapter.start(dexter_handle))
    dexter_follow_up = asyncio.run(dexter_adapter.status(dexter_handle))
    record_snapshot(dexter_plan, store, sink, dexter_follow_up)

    asyncio.run(mewx_adapter.start(mewx_handle))
    mewx_follow_up = asyncio.run(mewx_adapter.status(mewx_handle))
    record_snapshot(mewx_plan, store, sink, mewx_follow_up)

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

    asyncio.run(mewx_adapter.stop(mewx_handle, reason=MANUAL_LATCHED_STOP_ALL))
    mewx_terminal_ack = asyncio.run(mewx_adapter.status(mewx_handle))
    record_snapshot(mewx_plan, store, sink, mewx_terminal_ack)

    dexter_starting = dispatch_snapshots[0]
    mewx_starting = dispatch_snapshots[2]
    mewx_stopping = stopping_snapshots[mewx_plan.plan_id]

    assert [snapshot.status for snapshot in dispatch_snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
    ]
    assert dexter_handle.handle_id == dexter_duplicate_handle.handle_id
    assert mewx_handle.handle_id == mewx_duplicate_handle.handle_id
    assert dexter_starting.detail["handle_id"] == dexter_handle.handle_id
    assert dexter_starting.detail["transport_version"] == "v1"
    assert dexter_starting.detail["plan_batch_id"] == dexter_plan.plan_batch_id
    assert dexter_starting.detail["objective_profile_id"] == dexter_plan.objective_profile_id
    assert dexter_starting.detail["monitor_profile_id"] == dexter_plan.monitor_binding.monitor_profile_id
    assert dexter_starting.detail["execution_mode"] == "paper_live"
    assert dexter_starting.detail["prepare_ack_state"] == AckState.ACCEPTED.value
    assert dexter_starting.detail["prepare_request_count"] == 1
    assert dexter_starting.detail["start_request_count"] == 0
    assert mewx_starting.detail["handle_id"] == mewx_handle.handle_id
    assert mewx_starting.detail["execution_mode"] == "sim_live"
    assert mewx_starting.detail["startup_method"] == "start_session"
    assert mewx_starting.detail["prepare_ack_state"] == AckState.ACCEPTED.value
    assert mewx_follow_up.detail["prepare_request_count"] == 2
    assert mewx_follow_up.detail["start_request_count"] == 2
    assert mewx_follow_up.detail["prepare_duplicate_seen"] is True
    assert mewx_follow_up.detail["start_duplicate_seen"] is True
    assert mewx_follow_up.detail["execution_mode"] == "sim_live"
    assert dexter_follow_up.detail["prepare_request_count"] == 2
    assert dexter_follow_up.detail["start_request_count"] == 2
    assert dexter_follow_up.detail["prepare_duplicate_seen"] is True
    assert dexter_follow_up.detail["start_duplicate_seen"] is True
    assert store.detail_sequences[dexter_plan.plan_id][0]["plan_batch_id"] == dexter_plan.plan_batch_id
    assert store.detail_sequences[mewx_plan.plan_id][0]["monitor_profile_id"] == mewx_plan.monitor_binding.monitor_profile_id
    assert store.status_sequences[dexter_plan.plan_id][0] is PlanStatus.PLANNED
    assert store.status_sequences[dexter_plan.plan_id][-1] is PlanStatus.STOPPED
    assert store.status_sequences[mewx_plan.plan_id][0] is PlanStatus.PLANNED
    assert store.status_sequences[mewx_plan.plan_id][-1] is PlanStatus.STOPPED
    assert mewx_quarantined.status is PlanStatus.QUARANTINED
    assert mewx_quarantined.detail["reconciliation_decision"] == "push_promoted"
    assert mewx_quarantined.detail["monitor_profile_id"] == mewx_plan.monitor_binding.monitor_profile_id
    assert mewx_quarantined.detail["quarantine_reason"] == "timeout_guard"
    assert mewx_quarantined.detail["quarantine_scope"] == mewx_plan.monitor_binding.quarantine_scope
    assert mewx_quarantined.detail["execution_mode"] == "sim_live"
    assert mewx_quarantined.detail["prepare_request_count"] == 2
    assert mewx_quarantined.detail["start_request_count"] == 2
    assert mewx_stopping.status is PlanStatus.STOPPING
    assert mewx_stopping.source_reason == MANUAL_LATCHED_STOP_ALL
    assert mewx_stopping.detail["reconciliation_decision"] == "poll_confirmed_by_push"
    assert mewx_stopping.detail["push_source_reason"] == MANUAL_LATCHED_STOP_ALL
    assert mewx_stopping.detail["trigger_plan_id"] == mewx_plan.plan_id
    assert mewx_stopping.detail["halt_mode"] == MANUAL_LATCHED_STOP_ALL
    assert mewx_stopping.detail["stop_reason"] == MANUAL_LATCHED_STOP_ALL
    assert mewx_stopping.detail["execution_mode"] == "sim_live"
    assert mewx_stopping.detail["prepare_request_count"] == 2
    assert mewx_stopping.detail["start_request_count"] == 2
    assert mewx_stopping.detail["stop_request_count"] == 2
    assert terminal_snapshots[dexter_plan.plan_id]["prepare_request_count"] == 2
    assert terminal_snapshots[dexter_plan.plan_id]["start_request_count"] == 2
    assert terminal_snapshots[dexter_plan.plan_id]["stop_request_count"] == 2
    assert terminal_snapshots[dexter_plan.plan_id]["execution_mode"] == "paper_live"
    assert terminal_snapshots[mewx_plan.plan_id]["prepare_request_count"] == 2
    assert terminal_snapshots[mewx_plan.plan_id]["start_request_count"] == 2
    assert terminal_snapshots[mewx_plan.plan_id]["stop_request_count"] == 2
    assert terminal_snapshots[mewx_plan.plan_id]["monitor_profile_id"] == mewx_plan.monitor_binding.monitor_profile_id
    assert terminal_snapshots[mewx_plan.plan_id]["execution_mode"] == "sim_live"
    assert stopped_snapshots[mewx_plan.plan_id].detail["trigger_plan_id"] == mewx_plan.plan_id
    assert stopped_snapshots[mewx_plan.plan_id].detail["adapter_snapshot"]["stop_reason"] == MANUAL_LATCHED_STOP_ALL
    assert stopped_snapshots[dexter_plan.plan_id].detail["adapter_snapshot"]["execution_mode"] == "paper_live"
    assert mewx_terminal_ack.status is PlanStatus.STOPPED
    assert mewx_terminal_ack.detail["ack_state"] == AckState.TERMINAL.value
    assert mewx_terminal_ack.detail["stop_terminal_seen"] is True
    assert mewx_terminal_ack.detail["stop_duplicate_seen"] is True
    assert mewx_terminal_ack.detail["stop_request_count"] == 3
    assert mewx_terminal_ack.detail["monitor_profile_id"] == mewx_plan.monitor_binding.monitor_profile_id
    assert sink.latest_by_plan_id[mewx_plan.plan_id].detail["stop_terminal_seen"] is True
    stop_order = [
        entry["plan_id"]
        for entry in observation_log
        if entry["stage"] == "stop"
    ]
    assert stop_order[:4] == [
        mewx_plan.plan_id,
        mewx_plan.plan_id,
        dexter_plan.plan_id,
        dexter_plan.plan_id,
    ]


def test_transport_livepaper_observability_regression_pack_locks_failure_metadata_surface(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    observation_log: list[dict[str, object]] = []
    store = ObservabilityRegressionPlanStore(observation_log)
    sink = MirroringReconcilingStatusSink(store)
    registry, _, mewx_adapter = build_observability_registry(
        observation_log,
        mewx_failure_mode=TransportFailureMode(status_timeout=True),
    )

    snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(
                plan_request_id="req-transport-livepaper-observability-regression-pack-timeout",
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
    mewx_handle = mewx_adapter.handles_by_plan_id[mewx_plan.plan_id]
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
    status_errors = [entry for entry in observation_log if entry["stage"] == "status_error"]

    assert [snapshot.status for snapshot in snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.FAILED,
        PlanStatus.FAILED,
    ]
    assert mewx_failure.source_reason == "status timeout"
    assert mewx_failure.detail["failure_code"] == "status_timeout"
    assert mewx_failure.detail["plan_batch_id"] == mewx_plan.plan_batch_id
    assert mewx_failure.detail["monitor_profile_id"] == mewx_plan.monitor_binding.monitor_profile_id
    assert mewx_failure.detail["execution_mode"] == "sim_live"
    assert mewx_failure.detail["prepare_request_count"] == 1
    assert mewx_failure.detail["start_request_count"] == 1
    assert mewx_failure.detail["stop_request_count"] == 0
    assert mewx_failure.detail["prepare_ack_state"] == AckState.ACCEPTED.value
    assert mewx_failure.detail["start_ack_state"] == AckState.ACCEPTED.value
    assert mewx_failure.detail["stop_ack_state"] is None
    assert mewx_failure.detail["executor_profile_id"] == mewx_plan.executor_binding.executor_profile_id
    assert mewx_failure.detail["pinned_commit"] == mewx_plan.executor_binding.pinned_commit
    assert mewx_failure.detail["rollback_snapshot"]["execution_mode"] == "sim_live"
    assert mewx_failure.detail["rollback_snapshot"]["monitor_profile_id"] == mewx_plan.monitor_binding.monitor_profile_id
    assert mewx_failure.detail["rollback_snapshot"]["prepare_request_count"] == 1
    assert mewx_failure.detail["rollback_snapshot"]["start_request_count"] == 1
    assert mewx_failure.detail["rollback_snapshot"]["stop_request_count"] == 1
    assert mewx_failure.detail["rollback_snapshot"]["stop_accepted_once"] is True
    assert mewx_failure.detail["rollback_snapshot"]["quarantine_scope"] == mewx_plan.monitor_binding.quarantine_scope
    assert dexter_failure.detail["rollback_snapshot"]["execution_mode"] == "paper_live"
    assert dexter_failure.detail["rollback_snapshot"]["stop_request_count"] == 1
    assert status_errors == [
        {
            "stage": "status_error",
            "source": Source.MEWX.value,
            "plan_id": mewx_plan.plan_id,
            "handle_id": mewx_handle.handle_id,
            "failure_code": "status_timeout",
            "failure_stage": "status",
            "source_reason": "status timeout",
            "detail": {
                "handle_id": mewx_handle.handle_id,
                "native_session_id": f"sim_live:{mewx_plan.plan_id}",
                "transport_version": "v1",
                "signal": "status_poll",
                "sequence": 0,
                "poll_counter": 1,
                "snapshot_counter": 0,
                "prepared_at_utc": mewx_failure.detail["prepared_at_utc"],
                "entrypoint": "sim_session",
                "execution_mode": "sim_live",
                "startup_method": "start_session",
                "status_delivery": "poll_first",
                "executor_status": "starting",
                "stop_reason": None,
                "started": True,
                "stop_requested": False,
                "stop_confirmed": False,
                "ack_state": "accepted",
                "duplicate": False,
                "plan_batch_id": mewx_plan.plan_batch_id,
                "objective_profile_id": mewx_plan.objective_profile_id,
                "source": Source.MEWX.value,
                "selected_sleeve_id": mewx_plan.route.selected_sleeve_id,
                "monitor_profile_id": mewx_plan.monitor_binding.monitor_profile_id,
                "timeout_envelope_class": mewx_plan.monitor_binding.timeout_envelope_class,
                "quarantine_scope": mewx_plan.monitor_binding.quarantine_scope,
                "global_halt_participation": mewx_plan.monitor_binding.global_halt_participation,
                "executor_profile_id": mewx_plan.executor_binding.executor_profile_id,
                "pinned_commit": mewx_plan.executor_binding.pinned_commit,
                "prepare_ack_state": "accepted",
                "prepare_accepted_once": True,
                "prepare_duplicate_seen": False,
                "prepare_request_count": 1,
                "start_ack_state": "accepted",
                "start_accepted_once": True,
                "start_duplicate_seen": False,
                "start_terminal_seen": False,
                "start_request_count": 1,
                "stop_ack_state": None,
                "stop_accepted_once": False,
                "stop_duplicate_seen": False,
                "stop_terminal_seen": False,
                "stop_request_count": 0,
                "last_reported_status": "planned",
            },
        }
    ]
    assert sink.latest_by_plan_id[mewx_plan.plan_id].detail["rollback_snapshot"]["stop_request_count"] == 1


def test_transport_livepaper_observability_regression_pack_proof_tracks_ci_gate_as_next_step() -> None:
    proof = json.loads(
        (
            REPO_ROOT
            / "artifacts"
            / "proofs"
            / "task-007-transport-livepaper-observability-regression-pack-check.json"
        ).read_text()
    )

    assert proof["task_id"] == "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-REGRESSION-PACK"
    assert proof["verified_github"]["latest_vexter_pr"] == 51
    assert proof["transport_livepaper_observability_regression_pack"]["regression_axes"][
        "status_sink_fan_in_completeness"
    ] is True
    assert proof["transport_livepaper_observability_regression_pack"]["locked_surface"][
        "prepared_handles_preserve_handoff_metadata"
    ] is True
    assert proof["task_result"]["task_state"] == "transport_livepaper_observability_regression_pack_passed"
    assert proof["task_result"]["recommended_next_step"] == "transport_livepaper_observability_ci_gate"
