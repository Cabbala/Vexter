import asyncio
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vexter.planner_router.models import DispatchHandle, PlanRequest, PlanStatus, Source, SourcePinRegistry, StatusSnapshot
from vexter.planner_router.planner import plan_and_dispatch
from vexter.planner_router.transport import (
    ReconcilingStatusSink,
    SourceFaithfulTransportAdapter,
    TransportExecutorRegistry,
    evaluate_livepaper_observability_watchdog,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "config" / "planner_router"
FROZEN_PINS = SourcePinRegistry(
    dexter="ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    mewx="dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
)
CREATED_AT = datetime(2026, 3, 26, 23, 0, tzinfo=timezone.utc)
MANUAL_LATCHED_STOP_ALL = "manual_latched_stop_all"

EXPECTED_WATCHDOG_TEST_FILES = [
    "tests/test_planner_router_transport_livepaper_observability_watchdog.py",
]
EXPECTED_WATCHDOG_SURFACES = [
    "required_observability_field_omission",
    "handle_lifecycle_continuity",
    "planned_runtime_metadata_drift",
    "partial_status_sink_fan_in",
    "ack_history_retention",
    "quarantine_reason_completeness",
    "manual_stop_all_propagation",
    "snapshot_backed_terminal_detail",
    "normalized_failure_detail_passthrough",
]


class WatchdogPlanStore:
    def __init__(self) -> None:
        self.batches = []

    def put_batch(self, batch) -> None:
        self.batches.append(batch)


class RecordingWatchdogTransportAdapter(SourceFaithfulTransportAdapter):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.handles_by_plan_id: dict[str, DispatchHandle] = {}

    def prepare(self, plan):
        handle = super().prepare(plan)
        self.handles_by_plan_id[plan.plan_id] = handle
        return handle


def clone_config_dir(tmp_path: Path) -> Path:
    destination = tmp_path / "planner_router"
    shutil.copytree(CONFIG_ROOT, destination)
    return destination


def enable_mewx_sleeve(config_root: Path) -> None:
    sleeves_path = config_root / "sleeves.json"
    payload = json.loads(sleeves_path.read_text())
    payload[1]["enabled"] = True
    sleeves_path.write_text(json.dumps(payload, indent=2) + "\n")


def build_watchdog_registry() -> tuple[TransportExecutorRegistry, RecordingWatchdogTransportAdapter, RecordingWatchdogTransportAdapter]:
    dexter_adapter = RecordingWatchdogTransportAdapter(
        source=Source.DEXTER,
        executor_profile_id="dexter_main_pinned",
        pinned_commit=FROZEN_PINS.dexter,
    )
    mewx_adapter = RecordingWatchdogTransportAdapter(
        source=Source.MEWX,
        executor_profile_id="mewx_frozen_pinned",
        pinned_commit=FROZEN_PINS.mewx,
    )
    registry = TransportExecutorRegistry(
        {
            "dexter_main_pinned": dexter_adapter,
            "mewx_frozen_pinned": mewx_adapter,
        }
    )
    return registry, dexter_adapter, mewx_adapter


async def build_watchdog_runtime(
    tmp_path: Path,
) -> tuple[WatchdogPlanStore, ReconcilingStatusSink, dict[str, DispatchHandle], dict[str, dict[str, object]]]:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    store = WatchdogPlanStore()
    sink = ReconcilingStatusSink()
    registry, dexter_adapter, mewx_adapter = build_watchdog_registry()
    await plan_and_dispatch(
        PlanRequest(
            plan_request_id="req-transport-livepaper-observability-watchdog",
            objective_profile_id="dexter_with_mewx_overlay",
        ),
        config_root,
        FROZEN_PINS,
        store,
        registry,
        sink,
        CREATED_AT,
    )

    batch = store.batches[0]
    terminal_snapshots: dict[str, dict[str, object]] = {}
    for plan in reversed(batch.plans):
        adapter = registry.adapter_for(plan)
        handle = adapter.handles_by_plan_id[plan.plan_id]
        await adapter.stop(handle, reason=MANUAL_LATCHED_STOP_ALL)
        sink.record(await adapter.status(handle))
        terminal_snapshots[plan.plan_id] = dict(await adapter.snapshot(handle))
        sink.record(await adapter.status(handle))

    handles_by_plan_id = {
        plan.plan_id: registry.adapter_for(plan).handles_by_plan_id[plan.plan_id]
        for plan in batch.plans
    }
    return store, sink, handles_by_plan_id, terminal_snapshots


def make_snapshot(
    snapshot: StatusSnapshot,
    *,
    status: PlanStatus | None = None,
    source_reason: str | None = None,
    detail_changes: dict[str, object] | None = None,
    remove_fields: tuple[str, ...] = (),
) -> StatusSnapshot:
    detail = dict(snapshot.detail)
    if detail_changes:
        detail.update(detail_changes)
    for field_name in remove_fields:
        detail.pop(field_name, None)
    return StatusSnapshot(
        plan_id=snapshot.plan_id,
        status=status or snapshot.status,
        source_reason=snapshot.source_reason if source_reason is None else source_reason,
        observed_at_utc=snapshot.observed_at_utc,
        detail=detail,
    )


@pytest.mark.transport_livepaper_observability_watchdog
def test_livepaper_observability_watchdog_passes_on_complete_runtime_visibility(tmp_path: Path) -> None:
    store, sink, handles_by_plan_id, terminal_snapshots = asyncio.run(build_watchdog_runtime(tmp_path))
    batch = store.batches[0]

    report = evaluate_livepaper_observability_watchdog(
        batch.plans,
        handles_by_plan_id,
        runtime_snapshots=tuple(sink.snapshots),
        sink_snapshots=tuple(sink.snapshots),
        terminal_snapshots=terminal_snapshots,
    )

    assert report.passed is True
    assert report.checked_plan_ids == tuple(plan.plan_id for plan in batch.plans)
    assert report.findings == ()
    assert report.surface_status == {surface: True for surface in EXPECTED_WATCHDOG_SURFACES}


@pytest.mark.transport_livepaper_observability_watchdog
def test_livepaper_observability_watchdog_flags_drift_and_partial_visibility(tmp_path: Path) -> None:
    store, sink, handles_by_plan_id, terminal_snapshots = asyncio.run(build_watchdog_runtime(tmp_path))
    batch = store.batches[0]
    runtime_snapshots = list(sink.snapshots)
    primary_plan = batch.plans[0]
    primary_index = next(
        index for index, snapshot in enumerate(runtime_snapshots) if snapshot.plan_id == primary_plan.plan_id
    )
    primary_runtime_snapshot = runtime_snapshots[primary_index]

    runtime_snapshots[primary_index] = make_snapshot(
        primary_runtime_snapshot,
        detail_changes={
            "handle_id": "mismatched-handle",
            "native_session_id": "paper_live:mismatched-session",
        },
        remove_fields=("monitor_profile_id",),
    )
    runtime_snapshots.append(
        make_snapshot(
            primary_runtime_snapshot,
            status=PlanStatus.QUARANTINED,
            source_reason="timeout_guard",
            detail_changes={
                "signal": "push_quarantine",
                "quarantine_reason": None,
                "stop_requested": False,
                "stop_confirmed": False,
            },
        )
    )
    runtime_snapshots.append(
        make_snapshot(
            primary_runtime_snapshot,
            detail_changes={
                "signal": "halt_latched",
                "stop_reason": None,
                "stop_requested": True,
                "stop_confirmed": True,
            },
        )
    )

    sink_snapshots = runtime_snapshots[:-1]
    tampered_terminal_snapshots = dict(terminal_snapshots)
    tampered_terminal_snapshots[primary_plan.plan_id] = {
        **tampered_terminal_snapshots[primary_plan.plan_id],
        "prepare_request_count": 0,
        "stop_reason": None,
    }
    tampered_failure_details = {
        primary_plan.plan_id: {
            "code": "status_timeout",
            "stage": "status",
            "plan_id": primary_plan.plan_id,
            "source": primary_plan.route.selected_source.value,
            "source_reason": "status timeout",
            "detail": {
                "rollback_confirmed": True,
                "rollback_confirmation_source": "snapshot",
                "plan_id": primary_plan.plan_id,
                "plan_batch_id": primary_plan.plan_batch_id,
                "rollback_snapshot": {
                    "execution_mode": "paper_live",
                },
            },
        }
    }
    tampered_handles = dict(handles_by_plan_id)
    tampered_handles[primary_plan.plan_id] = DispatchHandle(
        plan_id=handles_by_plan_id[primary_plan.plan_id].plan_id,
        source=handles_by_plan_id[primary_plan.plan_id].source,
        native_handle={
            **dict(handles_by_plan_id[primary_plan.plan_id].native_handle),
            "pinned_commit": "deadbeef",
        },
        plan=handles_by_plan_id[primary_plan.plan_id].plan,
    )

    report = evaluate_livepaper_observability_watchdog(
        batch.plans,
        tampered_handles,
        runtime_snapshots=tuple(runtime_snapshots),
        sink_snapshots=tuple(sink_snapshots),
        terminal_snapshots=tampered_terminal_snapshots,
        failure_details_by_plan_id=tampered_failure_details,
    )

    surfaces = {finding.surface for finding in report.findings}
    assert report.passed is False
    assert "required_observability_field_omission" in surfaces
    assert "handle_lifecycle_continuity" in surfaces
    assert "planned_runtime_metadata_drift" in surfaces
    assert "partial_status_sink_fan_in" in surfaces
    assert "ack_history_retention" in surfaces
    assert "quarantine_reason_completeness" in surfaces
    assert "manual_stop_all_propagation" in surfaces
    assert "snapshot_backed_terminal_detail" in surfaces
    assert "normalized_failure_detail_passthrough" in surfaces


def load_watchdog_proof() -> dict[str, object]:
    return json.loads(
        (
            REPO_ROOT
            / "artifacts"
            / "proofs"
            / "task-007-transport-livepaper-observability-watchdog-check.json"
        ).read_text()
    )


def test_transport_livepaper_observability_watchdog_proof_tracks_outputs_and_runtime_next_step() -> None:
    proof = load_watchdog_proof()

    assert proof["task_id"] == "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG"
    assert proof["verified_github"]["latest_vexter_pr"] == 53
    assert proof["watchdog_suite"]["suite_group"] == "transport_livepaper_observability_watchdog"
    assert proof["watchdog_suite"]["watchdog_test_files"] == EXPECTED_WATCHDOG_TEST_FILES
    assert proof["watchdog_suite"]["monitored_surfaces"] == EXPECTED_WATCHDOG_SURFACES
    assert proof["watchdog_suite"]["source_faithful_modes"] == {
        "dexter": "paper_live",
        "mewx": "sim_live",
    }
    assert proof["task_result"]["task_state"] in {
        "transport_livepaper_observability_watchdog_passed",
        "transport_livepaper_observability_watchdog_failed",
    }
    if proof["task_result"]["task_state"] == "transport_livepaper_observability_watchdog_passed":
        assert proof["task_result"]["recommended_next_step"] == "transport_livepaper_observability_watchdog_runtime"
    else:
        assert proof["task_result"]["recommended_next_step"] == "transport_livepaper_observability_watchdog"


def test_transport_livepaper_observability_watchdog_workflow_runs_after_ci_gate() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()

    gate_index = workflow.index("Run transport livepaper observability CI gate")
    watchdog_index = workflow.index("Run transport livepaper observability watchdog")
    build_bundle_index = workflow.index("Build proof bundle")
    remaining_tests_index = workflow.index("Run remaining tests")

    assert "./scripts/run_transport_livepaper_observability_watchdog.sh" in workflow
    assert "transport-livepaper-observability-watchdog-proof" in workflow
    assert "cat artifacts/proofs/task-007-transport-livepaper-observability-watchdog-summary.md" in workflow
    assert 'pytest -q -m "not transport_livepaper_observability_ci_gate and not transport_livepaper_observability_watchdog"' in workflow
    assert gate_index < watchdog_index < build_bundle_index < remaining_tests_index


def test_transport_livepaper_observability_watchdog_manifest_and_context_point_to_watchdog_bundle() -> None:
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())

    assert manifest["bundle_path"] == "artifacts/bundles/task-007-transport-livepaper-observability-watchdog.tar.gz"
    assert manifest["task_id"] == "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG"
    assert manifest["status"] == "transport_livepaper_observability_watchdog_passed"
    assert "scripts/run_transport_livepaper_observability_watchdog.sh" in manifest["scripts"]
    assert (
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-report.md"
        in manifest["reports"]
    )
    assert context["current_task"]["id"] == "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG"
    assert context["current_contract"]["watchdog_marker"] == "transport_livepaper_observability_watchdog"
    assert (
        "tests/test_planner_router_transport_livepaper_observability_watchdog.py"
        in context["current_task"]["deliverables"]
    )
    assert (
        "tests/test_planner_router_transport_livepaper_observability_watchdog.py"
        in context["evidence"]["transport_livepaper_observability_watchdog"]["watchdog_test_files"]
    )
    assert context["next_task"]["id"] == "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME"


def test_transport_livepaper_observability_watchdog_script_targets_current_suite() -> None:
    watchdog_script = (REPO_ROOT / "scripts" / "run_transport_livepaper_observability_watchdog.sh").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    for file_name in EXPECTED_WATCHDOG_TEST_FILES:
        assert file_name in watchdog_script
    assert "transport_livepaper_observability_watchdog" in watchdog_script
    assert "transport_livepaper_observability_watchdog" in pytest_ini
