import asyncio
import json
from dataclasses import dataclass
from pathlib import Path

import pytest

from vexter.planner_router.models import DispatchHandle, PlanRequest, PlanStatus, StatusSnapshot
from vexter.planner_router.planner import plan_and_dispatch
from vexter.planner_router.transport import evaluate_livepaper_observability_watchdog

from tests.test_planner_router_transport_livepaper_observability_regression_pack import (
    CREATED_AT,
    FROZEN_PINS,
    MANUAL_LATCHED_STOP_ALL,
    MirroringReconcilingStatusSink,
    ObservabilityRegressionPlanStore,
    build_observability_registry,
    clone_config_dir,
    enable_mewx_sleeve,
    propagate_manual_latched_stop_all,
    record_snapshot,
)


pytestmark = [
    pytest.mark.transport_livepaper_observability_watchdog_runtime,
    pytest.mark.transport_livepaper_observability_watchdog_ci_gate,
]

REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_WATCHDOG_RUNTIME_TEST_FILES = [
    "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py",
]
EXPECTED_WATCHDOG_RUNTIME_SURFACES = [
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


@dataclass(frozen=True)
class WatchdogRuntimeSurface:
    store: ObservabilityRegressionPlanStore
    sink: MirroringReconcilingStatusSink
    batch: object
    dexter_plan: object
    mewx_plan: object
    dexter_handle: object
    mewx_handle: object
    terminal_snapshots: dict[str, dict[str, object]]
    dexter_follow_up: StatusSnapshot
    mewx_follow_up: StatusSnapshot
    mewx_quarantined: StatusSnapshot
    mewx_terminal_ack: StatusSnapshot


def _handle_map(surface: WatchdogRuntimeSurface) -> dict[str, object]:
    return {
        surface.dexter_plan.plan_id: surface.dexter_handle,
        surface.mewx_plan.plan_id: surface.mewx_handle,
    }


def _watchdog_terminal_snapshots(surface: WatchdogRuntimeSurface) -> dict[str, dict[str, object]]:
    mewx_terminal_snapshot = {
        **dict(surface.terminal_snapshots[surface.mewx_plan.plan_id]),
        "ack_state": surface.mewx_terminal_ack.detail["ack_state"],
        "stop_terminal_seen": surface.mewx_terminal_ack.detail["stop_terminal_seen"],
        "stop_duplicate_seen": surface.mewx_terminal_ack.detail["stop_duplicate_seen"],
        "stop_request_count": surface.mewx_terminal_ack.detail["stop_request_count"],
    }
    return {
        **surface.terminal_snapshots,
        surface.mewx_plan.plan_id: mewx_terminal_snapshot,
    }


def _make_snapshot(
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


def _build_valid_failure_detail(plan, handle, terminal_snapshot: dict[str, object]) -> dict[str, object]:
    handle_detail = dict(handle.native_handle)
    return {
        "code": "status_timeout",
        "stage": "status",
        "plan_id": plan.plan_id,
        "source": plan.route.selected_source.value,
        "source_reason": "status timeout",
        "detail": {
            "rollback_confirmed": True,
            "rollback_confirmation_source": "snapshot",
            "plan_id": plan.plan_id,
            "plan_batch_id": plan.plan_batch_id,
            "objective_profile_id": plan.objective_profile_id,
            "source": plan.route.selected_source.value,
            "selected_sleeve_id": plan.route.selected_sleeve_id,
            "monitor_profile_id": plan.monitor_binding.monitor_profile_id,
            "timeout_envelope_class": plan.monitor_binding.timeout_envelope_class,
            "quarantine_scope": plan.monitor_binding.quarantine_scope,
            "global_halt_participation": plan.monitor_binding.global_halt_participation,
            "executor_profile_id": plan.executor_binding.executor_profile_id,
            "pinned_commit": plan.executor_binding.pinned_commit,
            "entrypoint": handle_detail["entrypoint"],
            "execution_mode": handle_detail["execution_mode"],
            "startup_method": handle_detail["startup_method"],
            "handle_id": handle_detail["handle_id"],
            "transport_version": handle_detail["transport_version"],
            "rollback_snapshot": {
                **dict(terminal_snapshot),
                "executor_profile_id": plan.executor_binding.executor_profile_id,
                "pinned_commit": plan.executor_binding.pinned_commit,
            },
        },
    }


@pytest.fixture(scope="module")
def watchdog_runtime_surface(tmp_path_factory: pytest.TempPathFactory) -> WatchdogRuntimeSurface:
    tmp_path = tmp_path_factory.mktemp("transport_livepaper_observability_watchdog_runtime")
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    observation_log: list[dict[str, object]] = []
    store = ObservabilityRegressionPlanStore(observation_log)
    sink = MirroringReconcilingStatusSink(store)
    registry, dexter_adapter, mewx_adapter = build_observability_registry(observation_log)

    dispatch_snapshots = asyncio.run(
        plan_and_dispatch(
            PlanRequest(
                plan_request_id="req-transport-livepaper-observability-watchdog-runtime-overlay",
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

    dexter_adapter.prepare(dexter_plan)
    mewx_adapter.prepare(mewx_plan)

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

    _, _, terminal_snapshots = asyncio.run(
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

    assert dispatch_snapshots

    return WatchdogRuntimeSurface(
        store=store,
        sink=sink,
        batch=batch,
        dexter_plan=dexter_plan,
        mewx_plan=mewx_plan,
        dexter_handle=dexter_handle,
        mewx_handle=mewx_handle,
        terminal_snapshots=terminal_snapshots,
        dexter_follow_up=dexter_follow_up,
        mewx_follow_up=mewx_follow_up,
        mewx_quarantined=mewx_quarantined,
        mewx_terminal_ack=mewx_terminal_ack,
    )


def test_transport_livepaper_observability_watchdog_runtime_passes_on_runtime_follow_up_surface(
    watchdog_runtime_surface: WatchdogRuntimeSurface,
) -> None:
    valid_failure_details = {
        watchdog_runtime_surface.mewx_plan.plan_id: _build_valid_failure_detail(
            watchdog_runtime_surface.mewx_plan,
            watchdog_runtime_surface.mewx_handle,
            watchdog_runtime_surface.terminal_snapshots[watchdog_runtime_surface.mewx_plan.plan_id],
        )
    }

    report = evaluate_livepaper_observability_watchdog(
        watchdog_runtime_surface.batch.plans,
        _handle_map(watchdog_runtime_surface),
        runtime_snapshots=tuple(watchdog_runtime_surface.sink.snapshots),
        sink_snapshots=tuple(watchdog_runtime_surface.sink.snapshots),
        terminal_snapshots=_watchdog_terminal_snapshots(watchdog_runtime_surface),
        failure_details_by_plan_id=valid_failure_details,
    )

    assert report.passed is True
    assert report.findings == ()
    assert report.checked_plan_ids == tuple(plan.plan_id for plan in watchdog_runtime_surface.batch.plans)
    assert report.surface_status == {surface: True for surface in EXPECTED_WATCHDOG_RUNTIME_SURFACES}
    assert watchdog_runtime_surface.mewx_follow_up.detail["prepare_duplicate_seen"] is True
    assert watchdog_runtime_surface.mewx_quarantined.detail["quarantine_reason"] == "timeout_guard"
    assert watchdog_runtime_surface.mewx_terminal_ack.detail["stop_terminal_seen"] is True


def test_transport_livepaper_observability_watchdog_runtime_flags_drift_and_partial_visibility(
    watchdog_runtime_surface: WatchdogRuntimeSurface,
) -> None:
    runtime_snapshots = list(watchdog_runtime_surface.sink.snapshots)
    primary_plan = watchdog_runtime_surface.mewx_plan
    running_index = next(
        index
        for index, snapshot in enumerate(runtime_snapshots)
        if snapshot.plan_id == primary_plan.plan_id
        and snapshot.status is PlanStatus.RUNNING
        and dict(snapshot.detail).get("prepare_request_count") == 2
    )
    quarantine_index = next(
        index
        for index, snapshot in enumerate(runtime_snapshots)
        if snapshot.plan_id == primary_plan.plan_id and snapshot.status is PlanStatus.QUARANTINED
    )
    halt_index = next(
        index
        for index, snapshot in enumerate(runtime_snapshots)
        if snapshot.plan_id == primary_plan.plan_id and dict(snapshot.detail).get("signal") == "halt_latched"
    )

    runtime_snapshots[running_index] = _make_snapshot(
        runtime_snapshots[running_index],
        detail_changes={
            "handle_id": "runtime-follow-up-drift",
            "native_session_id": "sim_live:runtime-follow-up-drift",
        },
        remove_fields=("monitor_profile_id",),
    )
    runtime_snapshots[quarantine_index] = _make_snapshot(
        runtime_snapshots[quarantine_index],
        detail_changes={
            "quarantine_reason": None,
            "push_detail": {
                "signal": "push_quarantine",
                "monitor_profile_id": primary_plan.monitor_binding.monitor_profile_id,
                "quarantine_scope": primary_plan.monitor_binding.quarantine_scope,
            },
        },
    )
    runtime_snapshots[halt_index] = _make_snapshot(
        runtime_snapshots[halt_index],
        detail_changes={
            "halt_mode": "runtime_watchdog_drift",
            "stop_reason": None,
            "trigger_plan_id": None,
        },
    )

    tampered_terminal_snapshots = _watchdog_terminal_snapshots(watchdog_runtime_surface)
    tampered_terminal_snapshots[primary_plan.plan_id] = {
        **tampered_terminal_snapshots[primary_plan.plan_id],
        "signal": "status_poll",
        "prepare_request_count": 0,
        "stop_duplicate_seen": False,
        "stop_terminal_seen": False,
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
                    "execution_mode": "sim_live",
                },
            },
        }
    }
    tampered_handles = _handle_map(watchdog_runtime_surface)
    tampered_handles[primary_plan.plan_id] = DispatchHandle(
        plan_id=watchdog_runtime_surface.mewx_handle.plan_id,
        source=watchdog_runtime_surface.mewx_handle.source,
        native_handle={
            **dict(watchdog_runtime_surface.mewx_handle.native_handle),
            "pinned_commit": "runtime-follow-up-drift",
        },
        plan=watchdog_runtime_surface.mewx_handle.plan,
    )

    report = evaluate_livepaper_observability_watchdog(
        watchdog_runtime_surface.batch.plans,
        tampered_handles,
        runtime_snapshots=tuple(runtime_snapshots),
        sink_snapshots=tuple(runtime_snapshots[:-1]),
        terminal_snapshots=tampered_terminal_snapshots,
        failure_details_by_plan_id=tampered_failure_details,
    )

    assert report.passed is False
    assert {finding.surface for finding in report.findings} == set(EXPECTED_WATCHDOG_RUNTIME_SURFACES)


def test_transport_livepaper_observability_watchdog_runtime_script_targets_current_suite() -> None:
    watchdog_script = (
        REPO_ROOT / "scripts" / "run_transport_livepaper_observability_watchdog_runtime.sh"
    ).read_text()
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    for file_name in EXPECTED_WATCHDOG_RUNTIME_TEST_FILES:
        assert file_name in watchdog_script
    assert "transport_livepaper_observability_watchdog_runtime" in watchdog_script
    assert "transport-livepaper-observability-watchdog-runtime-proof" in workflow
    assert "./scripts/run_transport_livepaper_observability_watchdog_runtime.sh" in workflow
    assert "transport_livepaper_observability_watchdog_runtime" in pytest_ini


def test_transport_livepaper_observability_watchdog_runtime_workflow_runs_after_watchdog() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()

    gate_index = workflow.index("- name: Run transport livepaper observability CI gate")
    watchdog_index = workflow.index("- name: Run transport livepaper observability watchdog")
    watchdog_runtime_index = workflow.index("- name: Run transport livepaper observability watchdog runtime")
    watchdog_regression_pack_index = workflow.index(
        "- name: Run transport livepaper observability watchdog regression pack"
    )
    watchdog_ci_gate_index = workflow.index("- name: Run transport livepaper observability watchdog CI gate")
    handoff_watchdog_regression_pack_index = workflow.index(
        "- name: Run livepaper observability shift handoff watchdog regression pack"
    )
    build_bundle_index = workflow.index("- name: Build proof bundle")
    remaining_tests_index = workflow.index("- name: Run remaining tests")

    assert "cat artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-summary.md" in workflow
    assert (
        'pytest -q -m "not livepaper_observability_shift_handoff_ci_check and not '
        'livepaper_observability_shift_handoff_watchdog and not '
        'livepaper_observability_shift_handoff_watchdog_runtime and not '
        'livepaper_observability_shift_handoff_watchdog_regression_pack and not '
        'livepaper_observability_shift_handoff_watchdog_ci_gate and not '
        'transport_livepaper_observability_watchdog_ci_gate and not '
        'transport_livepaper_observability_ci_gate and not '
        'transport_livepaper_observability_watchdog and not '
        'transport_livepaper_observability_watchdog_runtime and not '
        'transport_livepaper_observability_watchdog_regression_pack"'
    ) in workflow
    assert (
        gate_index
        < watchdog_index
        < watchdog_runtime_index
        < watchdog_regression_pack_index
        < watchdog_ci_gate_index
        < handoff_watchdog_regression_pack_index
        < build_bundle_index
        < remaining_tests_index
    )


def test_transport_livepaper_observability_watchdog_runtime_manifest_and_context_point_to_bundle() -> None:
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())

    assert "scripts/run_transport_livepaper_observability_watchdog_runtime.sh" in manifest["scripts"]
    assert (
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime-report.md"
        in manifest["reports"]
    )
    assert (
        context["current_contract"]["watchdog_runtime_marker"]
        == "transport_livepaper_observability_watchdog_runtime"
    )
    assert (
        "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
        in context["evidence"]["transport_livepaper_observability_watchdog_runtime"]["runtime_test_files"]
    )
    assert (
        context["evidence"]["transport_livepaper_observability_watchdog_runtime"]["preferred_next_step"]
        == "transport_livepaper_observability_watchdog_regression_pack"
    )
    assert context["current_task"]["id"] in {
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SPEC",
        "TASK-007-LIVEPAPER-OBSERVABILITY-OPERATOR-RUNBOOK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-CHECKLIST",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-TEMPLATE",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-DRILL",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
        "PATTERN-A-DEMO-EXECUTOR-CUTOVER",
        "DEMO-FORWARD-ACCEPTANCE-PACK",
        "DEMO-FORWARD-SUPERVISED-RUN",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION",
    }


def test_transport_livepaper_observability_watchdog_runtime_proof_tracks_regression_pack_as_next_step() -> None:
    proof = json.loads(
        (
            REPO_ROOT
            / "artifacts"
            / "proofs"
            / "task-007-transport-livepaper-observability-watchdog-runtime-check.json"
        ).read_text()
    )

    assert proof["task_id"] == "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME"
    assert proof["verified_github"]["latest_vexter_pr"] == 55
    assert proof["watchdog_runtime_suite"]["suite_group"] == "transport_livepaper_observability_watchdog_runtime"
    assert proof["watchdog_runtime_suite"]["runtime_test_files"] == EXPECTED_WATCHDOG_RUNTIME_TEST_FILES
    assert proof["watchdog_runtime_suite"]["monitored_surfaces"] == EXPECTED_WATCHDOG_RUNTIME_SURFACES
    assert proof["watchdog_runtime_suite"]["proof_artifact_name"] == "transport-livepaper-observability-watchdog-runtime-proof"
    assert proof["task_result"]["task_state"] in {
        "transport_livepaper_observability_watchdog_runtime_passed",
        "transport_livepaper_observability_watchdog_runtime_failed",
    }
    if proof["task_result"]["task_state"] == "transport_livepaper_observability_watchdog_runtime_passed":
        assert proof["task_result"]["recommended_next_step"] == "transport_livepaper_observability_watchdog_regression_pack"
    else:
        assert proof["task_result"]["recommended_next_step"] == "transport_livepaper_observability_watchdog_runtime"
