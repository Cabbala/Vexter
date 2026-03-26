import asyncio
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vexter.planner_router.models import FailureCode, PlanRequest, PlanStatus, Source, SourcePinRegistry
from vexter.planner_router.planner import plan_and_dispatch, plan_request
from vexter.planner_router.transport import (
    AckState,
    InMemoryPlanStore,
    ReconcilingStatusSink,
    SourceFaithfulTransportAdapter,
    TransportFailureMode,
    build_source_faithful_transport_registry,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "config" / "planner_router"
FROZEN_PINS = SourcePinRegistry(
    dexter="ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    mewx="dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
)
CREATED_AT = datetime(2026, 3, 26, 4, 12, tzinfo=timezone.utc)


def clone_config_dir(tmp_path: Path) -> Path:
    destination = tmp_path / "planner_router"
    shutil.copytree(CONFIG_ROOT, destination)
    return destination


def enable_mewx_sleeve(config_root: Path) -> None:
    sleeves_path = config_root / "sleeves.json"
    payload = json.loads(sleeves_path.read_text())
    payload[1]["enabled"] = True
    sleeves_path.write_text(json.dumps(payload, indent=2) + "\n")


def build_default_plan() -> tuple[InMemoryPlanStore, object]:
    store = InMemoryPlanStore()
    batch = plan_request(
        PlanRequest(plan_request_id="req-transport-default"),
        CONFIG_ROOT,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )
    return store, batch.plans[0]


def test_source_faithful_transport_prepare_returns_idempotent_handle_envelope() -> None:
    _, plan = build_default_plan()
    adapter = SourceFaithfulTransportAdapter(
        source=Source.DEXTER,
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
    )

    first_handle = adapter.prepare(plan)
    duplicate_handle = adapter.prepare(plan)

    assert first_handle.native_handle["transport_version"] == "v1"
    assert first_handle.native_handle["handle_id"] == duplicate_handle.native_handle["handle_id"]
    assert first_handle.native_handle["ack_state"] == AckState.ACCEPTED.value
    assert duplicate_handle.native_handle["ack_state"] == AckState.DUPLICATE.value
    assert first_handle.native_handle["entrypoint"] == "monitor_mint_session"
    assert first_handle.native_handle["status_delivery"] == "poll_first"
    assert first_handle.native_handle["pinned_commit"] == FROZEN_PINS.dexter
    assert first_handle.native_handle["plan_batch_id"] == plan.plan_batch_id
    assert first_handle.native_handle["objective_profile_id"] == plan.objective_profile_id
    assert first_handle.native_handle["monitor_profile_id"] == plan.monitor_binding.monitor_profile_id
    assert first_handle.native_handle["quarantine_scope"] == plan.monitor_binding.quarantine_scope


def test_source_faithful_transport_start_stop_are_idempotent_with_snapshot_confirmation() -> None:
    _, plan = build_default_plan()
    adapter = SourceFaithfulTransportAdapter(
        source=Source.DEXTER,
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
    )
    handle = adapter.prepare(plan)

    asyncio.run(adapter.start(handle))
    asyncio.run(adapter.start(handle))

    running_snapshot = asyncio.run(adapter.status(handle))

    asyncio.run(adapter.stop(handle, reason="manual_latched_stop_all"))
    asyncio.run(adapter.stop(handle, reason="manual_latched_stop_all"))

    stopping_snapshot = asyncio.run(adapter.status(handle))
    terminal_snapshot = asyncio.run(adapter.snapshot(handle))
    stopped_snapshot = asyncio.run(adapter.status(handle))

    assert running_snapshot.status is PlanStatus.RUNNING
    assert running_snapshot.detail["ack_state"] == AckState.DUPLICATE.value
    assert running_snapshot.detail["start_accepted_once"] is True
    assert running_snapshot.detail["start_duplicate_seen"] is True
    assert stopping_snapshot.status is PlanStatus.STOPPING
    assert stopping_snapshot.detail["ack_state"] == AckState.DUPLICATE.value
    assert stopping_snapshot.detail["stop_accepted_once"] is True
    assert stopping_snapshot.detail["stop_duplicate_seen"] is True
    assert terminal_snapshot["executor_status"] == PlanStatus.STOPPED.value
    assert terminal_snapshot["handle_id"] == handle.native_handle["handle_id"]
    assert terminal_snapshot["start_duplicate_seen"] is True
    assert terminal_snapshot["stop_duplicate_seen"] is True
    assert terminal_snapshot["plan_batch_id"] == plan.plan_batch_id
    assert stopped_snapshot.status is PlanStatus.STOPPED


def test_source_faithful_transport_prepare_preserves_pin_mismatch_failure_code() -> None:
    _, plan = build_default_plan()
    adapter = SourceFaithfulTransportAdapter(
        source=Source.DEXTER,
        executor_profile_id="dexter_main_pinned",
        pinned_commit="deadbeef",
    )

    with pytest.raises(Exception) as exc_info:
        adapter.prepare(plan)

    assert getattr(exc_info.value, "failure", None) is not None
    assert exc_info.value.failure.code is FailureCode.PIN_MISMATCH
    assert exc_info.value.failure.detail["rejection_class"] == "pin_mismatch"
    assert exc_info.value.failure.detail["execution_mode"] == "paper_live"
    assert exc_info.value.failure.detail["entrypoint"] == "monitor_mint_session"
    assert exc_info.value.failure.detail["plan_batch_id"] == plan.plan_batch_id
    assert exc_info.value.failure.detail["monitor_profile_id"] == plan.monitor_binding.monitor_profile_id


def test_transport_registry_and_sink_keep_plan_store_separate_while_poll_reconciliation_advances(
    tmp_path: Path,
) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    store = InMemoryPlanStore()
    sink = ReconcilingStatusSink()
    registry = build_source_faithful_transport_registry(FROZEN_PINS)

    dispatch_snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(plan_request_id="req-transport-overlay", objective_profile_id="dexter_with_mewx_overlay"),
            config_root,
            FROZEN_PINS,
            store,
            registry,
            sink,
            CREATED_AT,
        )
    )

    assert len(store.batches) == 1
    assert len(store.batches[0].plans) == 2
    assert [snapshot.status for snapshot in dispatch_snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
    ]
    assert set(sink.latest_by_plan_id) == {plan.plan_id for plan in store.batches[0].plans}


def test_transport_status_reconciliation_prefers_latest_valid_monotonic_update() -> None:
    _, plan = build_default_plan()
    adapter = SourceFaithfulTransportAdapter(
        source=Source.DEXTER,
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
        failure_mode=TransportFailureMode(),
    )
    handle = adapter.prepare(plan)
    asyncio.run(adapter.start(handle))
    adapter.queue_push_snapshot(
        handle,
        PlanStatus.STOPPING,
        detail={"signal": "push_event", "push_reason": "quarantine_escalation"},
    )

    reconciled = asyncio.run(adapter.status(handle))

    assert reconciled.status is PlanStatus.STOPPING
    assert reconciled.detail["reconciliation_mode"] == "poll_first"
    assert reconciled.detail["reconciliation_decision"] == "push_promoted"
    assert reconciled.detail["push_status"] == PlanStatus.STOPPING.value
    assert reconciled.detail["poll_status"] == PlanStatus.RUNNING.value
    assert reconciled.detail["poll_detail"]["execution_mode"] == "paper_live"
    assert reconciled.detail["execution_mode"] == "paper_live"
    assert reconciled.detail["plan_batch_id"] == plan.plan_batch_id
    assert reconciled.detail["objective_profile_id"] == plan.objective_profile_id
    assert reconciled.detail["start_accepted_once"] is True
    assert reconciled.detail["stop_accepted_once"] is False


def test_transport_implementation_proof_tracks_runtime_smoke_as_next_step() -> None:
    proof = json.loads(
        (
            REPO_ROOT
            / "artifacts"
            / "proofs"
            / "task-007-planner-router-executor-transport-implementation-check.json"
        ).read_text()
    )

    assert proof["task_id"] == "TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-IMPLEMENTATION"
    assert proof["verified_github"]["latest_vexter_pr"] == 43
    assert proof["transport_implementation"]["adapter"] == "SourceFaithfulTransportAdapter"
    assert proof["dispatch_state_machine_updates"]["stop_confirmation_implemented"] is True
    assert proof["task_result"]["task_state"] == "planner_router_executor_transport_implemented"
    assert proof["task_result"]["recommended_next_step"] == "transport_runtime_smoke"
