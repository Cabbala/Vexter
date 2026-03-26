import asyncio
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from vexter.planner_router.models import PlanRequest, PlanStatus, Source, SourcePinRegistry
from vexter.planner_router.planner import plan_and_dispatch, plan_request
from vexter.planner_router.transport import (
    AckState,
    InMemoryPlanStore,
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
CREATED_AT = datetime(2026, 3, 26, 11, 39, tzinfo=timezone.utc)


def clone_config_dir(tmp_path: Path) -> Path:
    destination = tmp_path / "planner_router"
    shutil.copytree(CONFIG_ROOT, destination)
    return destination


def enable_mewx_sleeve(config_root: Path) -> None:
    sleeves_path = config_root / "sleeves.json"
    payload = json.loads(sleeves_path.read_text())
    payload[1]["enabled"] = True
    sleeves_path.write_text(json.dumps(payload, indent=2) + "\n")


def build_default_plan():
    store = InMemoryPlanStore()
    batch = plan_request(
        PlanRequest(plan_request_id="req-transport-runtime-default"),
        CONFIG_ROOT,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )
    return store, batch.plans[0]


class RecordingTransportAdapter(SourceFaithfulTransportAdapter):
    def __init__(self, *, events: list[str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.events = events

    def prepare(self, plan):
        handle = super().prepare(plan)
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


def build_recording_registry(
    events: list[str],
    *,
    dexter_failure_mode: TransportFailureMode | None = None,
    mewx_failure_mode: TransportFailureMode | None = None,
) -> TransportExecutorRegistry:
    return TransportExecutorRegistry(
        {
            "dexter_main_pinned": RecordingTransportAdapter(
                events=events,
                source=Source.DEXTER,
                executor_profile_id="dexter_main_pinned",
                pinned_commit=FROZEN_PINS.dexter,
                failure_mode=dexter_failure_mode,
            ),
            "mewx_frozen_pinned": RecordingTransportAdapter(
                events=events,
                source=Source.MEWX,
                executor_profile_id="mewx_frozen_pinned",
                pinned_commit=FROZEN_PINS.mewx,
                failure_mode=mewx_failure_mode,
            ),
        }
    )


def test_transport_runtime_smoke_progresses_handle_commands_with_source_faithful_seams(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    store = InMemoryPlanStore()
    batch = plan_request(
        PlanRequest(
            plan_request_id="req-transport-runtime-path",
            objective_profile_id="dexter_with_mewx_overlay",
        ),
        config_root,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )
    registry = build_recording_registry(events=[])
    handles_by_source = {}

    assert [plan.status for plan in batch.plans] == [PlanStatus.PLANNED, PlanStatus.PLANNED]

    for plan in batch.plans:
        adapter = registry.adapter_for(plan)
        first_handle = adapter.prepare(plan)
        duplicate_handle = adapter.prepare(plan)
        handles_by_source[plan.route.selected_source] = first_handle

        asyncio.run(adapter.start(first_handle))
        asyncio.run(adapter.start(first_handle))
        running_snapshot = asyncio.run(adapter.status(first_handle))

        asyncio.run(adapter.stop(first_handle, reason="manual_latched_stop_all"))
        asyncio.run(adapter.stop(first_handle, reason="manual_latched_stop_all"))
        stopping_snapshot = asyncio.run(adapter.status(first_handle))
        terminal_snapshot = asyncio.run(adapter.snapshot(first_handle))
        stopped_snapshot = asyncio.run(adapter.status(first_handle))

        assert first_handle.handle_id == duplicate_handle.handle_id
        assert first_handle.native_handle["ack_state"] == AckState.ACCEPTED.value
        assert duplicate_handle.native_handle["ack_state"] == AckState.DUPLICATE.value
        assert running_snapshot.status is PlanStatus.RUNNING
        assert running_snapshot.detail["ack_state"] == AckState.DUPLICATE.value
        assert stopping_snapshot.status is PlanStatus.STOPPING
        assert stopping_snapshot.detail["ack_state"] == AckState.DUPLICATE.value
        assert terminal_snapshot["executor_status"] == PlanStatus.STOPPED.value
        assert terminal_snapshot["handle_id"] == first_handle.handle_id
        assert terminal_snapshot["stop_reason"] == "manual_latched_stop_all"
        assert stopped_snapshot.status is PlanStatus.STOPPED

    dexter_handle = handles_by_source[Source.DEXTER]
    mewx_handle = handles_by_source[Source.MEWX]

    assert dexter_handle.handle_id.startswith("dexter_main_pinned:")
    assert dexter_handle.native_handle["entrypoint"] == "monitor_mint_session"
    assert dexter_handle.native_handle["execution_mode"] == "paper_live"
    assert dexter_handle.native_handle["startup_method"] is None
    assert mewx_handle.handle_id.startswith("mewx_frozen_pinned:")
    assert mewx_handle.native_handle["entrypoint"] == "sim_session"
    assert mewx_handle.native_handle["execution_mode"] == "sim_live"
    assert mewx_handle.native_handle["startup_method"] == "start_session"


def test_transport_runtime_smoke_prefers_push_then_confirms_stop_with_snapshot_fallback() -> None:
    _, plan = build_default_plan()
    adapter = SourceFaithfulTransportAdapter(
        source=Source.DEXTER,
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
    )
    handle = adapter.prepare(plan)

    asyncio.run(adapter.start(handle))
    initial_snapshot = asyncio.run(adapter.status(handle))
    adapter.queue_push_snapshot(
        handle,
        PlanStatus.QUARANTINED,
        source_reason="monitor_guard",
        detail={"signal": "push_quarantine", "quarantine_scope": "sleeve"},
    )

    reconciled_snapshot = asyncio.run(adapter.status(handle))
    asyncio.run(adapter.stop(handle, reason="manual_latched_stop_all"))
    stopping_snapshot = asyncio.run(adapter.status(handle))
    terminal_snapshot = asyncio.run(adapter.snapshot(handle))

    assert initial_snapshot.status is PlanStatus.RUNNING
    assert reconciled_snapshot.status is PlanStatus.QUARANTINED
    assert reconciled_snapshot.detail["reconciliation_mode"] == "poll_first"
    assert reconciled_snapshot.detail["reconciliation_decision"] == "push_promoted"
    assert reconciled_snapshot.detail["poll_status"] == PlanStatus.RUNNING.value
    assert reconciled_snapshot.detail["push_status"] == PlanStatus.QUARANTINED.value
    assert stopping_snapshot.status is PlanStatus.STOPPING
    assert stopping_snapshot.detail["reconciliation_decision"] == "poll_only"
    assert stopping_snapshot.detail["ack_state"] == AckState.ACCEPTED.value
    assert terminal_snapshot["executor_status"] == PlanStatus.STOPPED.value
    assert terminal_snapshot["stop_reason"] == "manual_latched_stop_all"


def test_transport_runtime_smoke_normalizes_status_timeout_and_rolls_back_in_reverse_order(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    events: list[str] = []
    store = InMemoryPlanStore()
    sink = ReconcilingStatusSink()
    registry = build_recording_registry(
        events,
        mewx_failure_mode=TransportFailureMode(status_timeout=True),
    )

    snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(
                plan_request_id="req-transport-runtime-timeout",
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
    stop_events = [event for event in events if event.startswith("stop:")]

    assert [snapshot.status for snapshot in snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.FAILED,
        PlanStatus.FAILED,
    ]
    assert mewx_failure.status is PlanStatus.FAILED
    assert mewx_failure.source_reason == "status timeout"
    assert mewx_failure.detail["failure_code"] == "status_timeout"
    assert mewx_failure.detail["stage"] == "status"
    assert mewx_failure.detail["rollback_confirmed"] is True
    assert mewx_failure.detail["rollback_confirmation_source"] == "snapshot"
    assert f"status_error:mewx:{mewx_plan.plan_id}:status_timeout" in events
    assert stop_events == [
        f"stop:mewx:{mewx_plan.plan_id}:status_timeout:accepted",
        f"stop:dexter:{dexter_plan.plan_id}:status_timeout:accepted",
    ]
    assert sink.snapshots == snapshots


def test_transport_runtime_smoke_proof_tracks_transport_livepaper_smoke_as_next_step() -> None:
    proof = json.loads(
        (REPO_ROOT / "artifacts" / "proofs" / "task-007-transport-runtime-smoke-check.json").read_text()
    )

    assert proof["task_id"] == "TASK-007-TRANSPORT-RUNTIME-SMOKE"
    assert proof["verified_github"]["latest_vexter_pr"] == 44
    assert proof["transport_runtime_smoke"]["handle_runtime_progression"]["source_faithful_modes"]["dexter"] == "paper_live"
    assert proof["transport_runtime_smoke"]["rollback_runtime_smoke"]["reverse_order_stop_all"] is True
    assert proof["task_result"]["task_state"] == "transport_runtime_smoke_passed"
    assert proof["task_result"]["recommended_next_step"] == "transport_livepaper_smoke"
