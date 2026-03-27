import asyncio
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vexter.planner_router.models import FailureCode, PlanRequest, PlanStatus, SourcePinRegistry
from vexter.planner_router.planner import plan_and_dispatch, plan_request
from vexter.planner_router.transport import (
    AckState,
    DexterDemoExecutorAdapter,
    InMemoryPlanStore,
    ReconcilingStatusSink,
    TransportFailureMode,
    TransportRejectionClass,
    build_demo_executor_transport_registry,
    build_source_faithful_transport_registry,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "config" / "planner_router"
FROZEN_PINS = SourcePinRegistry(
    dexter="ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    mewx="dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
)
CREATED_AT = datetime(2026, 3, 26, 5, 12, tzinfo=timezone.utc)


def clone_config_dir(tmp_path: Path) -> Path:
    destination = tmp_path / "planner_router"
    shutil.copytree(CONFIG_ROOT, destination)
    return destination


def enable_mewx_sleeve(config_root: Path) -> None:
    sleeves_path = config_root / "sleeves.json"
    payload = json.loads(sleeves_path.read_text())
    payload[1]["enabled"] = True
    sleeves_path.write_text(json.dumps(payload, indent=2) + "\n")


def test_source_faithful_transport_adapter_is_idempotent_and_handle_based() -> None:
    store = InMemoryPlanStore()
    batch = plan_request(
        PlanRequest(plan_request_id="req-transport-idempotent"),
        CONFIG_ROOT,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )
    plan = batch.plans[0]
    registry = build_source_faithful_transport_registry(FROZEN_PINS)
    adapter = registry.adapter_for(plan)

    first_handle = adapter.prepare(plan)
    duplicate_handle = adapter.prepare(plan)

    assert first_handle.handle_id == duplicate_handle.handle_id
    assert first_handle.native_handle["ack_state"] == AckState.ACCEPTED.value
    assert duplicate_handle.native_handle["ack_state"] == AckState.DUPLICATE.value
    assert first_handle.native_handle["entrypoint"] == "monitor_mint_session"
    assert first_handle.native_handle["status_delivery"] == "poll_first"

    asyncio.run(adapter.start(first_handle))
    asyncio.run(adapter.start(first_handle))
    running_snapshot = asyncio.run(adapter.status(first_handle))

    assert running_snapshot.status is PlanStatus.RUNNING
    assert running_snapshot.detail["handle_id"] == first_handle.handle_id
    assert running_snapshot.detail["signal"] == "status_poll"
    assert running_snapshot.detail["entrypoint"] == "monitor_mint_session"
    assert running_snapshot.detail["ack_state"] == AckState.DUPLICATE.value

    asyncio.run(adapter.stop(first_handle, reason="manual_latched_stop_all"))
    asyncio.run(adapter.stop(first_handle, reason="manual_latched_stop_all"))
    stopping_snapshot = asyncio.run(adapter.status(first_handle))
    confirmed_snapshot = asyncio.run(adapter.snapshot(first_handle))

    assert stopping_snapshot.status is PlanStatus.STOPPING
    assert confirmed_snapshot["executor_status"] == PlanStatus.STOPPED.value
    assert confirmed_snapshot["handle_id"] == first_handle.handle_id
    assert confirmed_snapshot["entrypoint"] == "monitor_mint_session"


def test_transport_status_reconciliation_promotes_valid_push_over_poll() -> None:
    store = InMemoryPlanStore()
    batch = plan_request(
        PlanRequest(plan_request_id="req-transport-push"),
        CONFIG_ROOT,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )
    plan = batch.plans[0]
    registry = build_source_faithful_transport_registry(FROZEN_PINS)
    adapter = registry.adapter_for(plan)
    handle = adapter.prepare(plan)

    asyncio.run(adapter.start(handle))
    initial_snapshot = asyncio.run(adapter.status(handle))
    assert initial_snapshot.status is PlanStatus.RUNNING
    adapter.queue_push_snapshot(
        handle,
        PlanStatus.QUARANTINED,
        source_reason="monitor_guard",
        detail={"signal": "push_quarantine"},
    )
    snapshot = asyncio.run(adapter.status(handle))

    assert snapshot.status is PlanStatus.QUARANTINED
    assert snapshot.detail["reconciliation_decision"] == "push_promoted"
    assert snapshot.detail["poll_status"] == PlanStatus.RUNNING.value
    assert snapshot.detail["push_status"] == PlanStatus.QUARANTINED.value
    assert snapshot.detail["entrypoint"] == "monitor_mint_session"


def test_dexter_demo_adapter_maps_submit_fill_and_stop_all_runtime() -> None:
    store = InMemoryPlanStore()
    batch = plan_request(
        PlanRequest(plan_request_id="req-demo-adapter-runtime"),
        CONFIG_ROOT,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )
    plan = batch.plans[0]
    registry = build_demo_executor_transport_registry(FROZEN_PINS)
    adapter = registry.adapter_for(plan)

    assert isinstance(adapter, DexterDemoExecutorAdapter)

    handle = adapter.prepare(plan)
    assert handle.native_handle["demo_runtime"] == "dexter_paper_live_demo"
    assert handle.native_handle["symbol_allowlist"] == ["BONK/USDC"]
    assert handle.native_handle["demo_symbol"] == "BONK/USDC"

    asyncio.run(adapter.start(handle))
    running_snapshot = asyncio.run(adapter.status(handle))

    assert running_snapshot.detail["native_order_status"] == "filled"
    assert running_snapshot.detail["fill_count"] == 1
    assert running_snapshot.detail["orders"][0]["purpose"] == "entry"
    assert running_snapshot.detail["orders"][0]["state"] == "filled"
    assert running_snapshot.detail["fills"][0]["side"] == "buy"
    assert running_snapshot.detail["open_position_lots"] == "0.05"

    asyncio.run(adapter.stop(handle, reason="manual_latched_stop_all"))
    stopping_snapshot = asyncio.run(adapter.status(handle))
    confirmed_snapshot = asyncio.run(adapter.snapshot(handle))

    assert stopping_snapshot.detail["stop_all_state"] == "flatten_requested"
    assert confirmed_snapshot["stop_all_state"] == "flatten_confirmed"
    assert confirmed_snapshot["fill_count"] == 2
    assert confirmed_snapshot["orders"][1]["purpose"] == "flatten"
    assert confirmed_snapshot["orders"][1]["state"] == "filled"
    assert confirmed_snapshot["open_position_lots"] == "0"


def test_dexter_demo_adapter_cancels_unfilled_entry_before_terminal_snapshot() -> None:
    store = InMemoryPlanStore()
    batch = plan_request(
        PlanRequest(plan_request_id="req-demo-adapter-cancel"),
        CONFIG_ROOT,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )
    plan = batch.plans[0]
    adapter = DexterDemoExecutorAdapter(
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
    )

    handle = adapter.prepare(plan)
    asyncio.run(adapter.start(handle))
    asyncio.run(adapter.stop(handle, reason="manual_latched_stop_all"))
    snapshot = asyncio.run(adapter.snapshot(handle))

    assert snapshot["stop_all_state"] == "cancel_confirmed"
    assert snapshot["fill_count"] == 0
    assert snapshot["orders"][0]["purpose"] == "entry"
    assert snapshot["orders"][0]["state"] == "canceled"
    assert snapshot["orders"][0]["cancel_reason"] == "manual_latched_stop_all"


def test_dexter_demo_adapter_rejects_portfolio_split_route_for_first_demo_slice(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    store = InMemoryPlanStore()
    batch = plan_request(
        PlanRequest(
            plan_request_id="req-demo-adapter-route-guardrail",
            objective_profile_id="dexter_with_mewx_overlay",
        ),
        config_root,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )
    dexter_plan = batch.plans[0]
    adapter = DexterDemoExecutorAdapter(
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
    )

    with pytest.raises(Exception) as exc_info:
        adapter.prepare(dexter_plan)

    assert exc_info.value.failure.code is FailureCode.PREPARE_FAILED
    assert exc_info.value.failure.source_reason == "single_sleeve_only"
    assert exc_info.value.failure.detail["route_mode"] == "portfolio_split"


def test_dexter_demo_adapter_surfaces_fill_reconciliation_gap_abort() -> None:
    store = InMemoryPlanStore()
    batch = plan_request(
        PlanRequest(plan_request_id="req-demo-adapter-reconciliation-gap"),
        CONFIG_ROOT,
        FROZEN_PINS,
        store,
        CREATED_AT,
    )
    plan = batch.plans[0]
    adapter = DexterDemoExecutorAdapter(
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
        failure_mode=TransportFailureMode(fill_reconciliation_gap=True),
    )

    handle = adapter.prepare(plan)
    asyncio.run(adapter.start(handle))

    with pytest.raises(Exception) as exc_info:
        asyncio.run(adapter.status(handle))

    assert exc_info.value.failure.code is FailureCode.RECONCILIATION_GAP
    assert exc_info.value.failure.detail["abort_condition"] == "status_or_fill_reconciliation_gap"
    assert exc_info.value.failure.detail["demo_runtime"] == "dexter_paper_live_demo"


def test_dispatch_failure_propagates_transport_failure_and_confirms_reverse_stop(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    store = InMemoryPlanStore()
    sink = ReconcilingStatusSink()
    registry = build_source_faithful_transport_registry(
        FROZEN_PINS,
        mewx_failure_mode=TransportFailureMode(
            start_rejection=TransportRejectionClass.NATIVE_START_REJECTED,
        ),
    )

    snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(
                plan_request_id="req-transport-start-fail",
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

    assert [snapshot.status for snapshot in snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.FAILED,
        PlanStatus.FAILED,
    ]
    assert snapshots[-2].detail["failure_code"] == "start_failed"
    assert snapshots[-1].detail["failure_code"] == "start_failed"
    assert snapshots[-2].detail["rollback_confirmed"] is True
    assert snapshots[-1].detail["rollback_confirmed"] is True
    assert snapshots[-2].detail["rollback_for"] == "start_failed"
    assert snapshots[-1].detail["rollback_for"] == "start_failed"
    assert snapshots[-1].detail["rollback_confirmation_source"] in {"status", "snapshot"}

    dexter_adapter = registry.adapter_for(dexter_plan)
    mewx_adapter = registry.adapter_for(mewx_plan)
    dexter_handle = dexter_adapter.prepare(dexter_plan)
    mewx_handle = mewx_adapter.prepare(mewx_plan)

    assert dexter_handle.handle_id != mewx_handle.handle_id


def test_plan_and_dispatch_with_transport_registry_emits_handle_based_running_details(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    store = InMemoryPlanStore()
    sink = ReconcilingStatusSink()
    registry = build_source_faithful_transport_registry(FROZEN_PINS)

    snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(
                plan_request_id="req-transport-overlay",
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

    running_snapshots = [snapshot for snapshot in snapshots if snapshot.status is PlanStatus.RUNNING]

    assert [snapshot.status for snapshot in snapshots] == [
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
        PlanStatus.STARTING,
        PlanStatus.RUNNING,
    ]
    assert len(running_snapshots) == 2
    assert running_snapshots[0].detail["handle_id"].startswith("dexter_main_pinned:")
    assert running_snapshots[0].detail["entrypoint"] == "monitor_mint_session"
    assert running_snapshots[0].detail["pinned_commit"] == FROZEN_PINS.dexter
    assert running_snapshots[1].detail["handle_id"].startswith("mewx_frozen_pinned:")
    assert running_snapshots[1].detail["entrypoint"] == "sim_session"
    assert running_snapshots[1].detail["pinned_commit"] == FROZEN_PINS.mewx
    assert sink.snapshots == snapshots
