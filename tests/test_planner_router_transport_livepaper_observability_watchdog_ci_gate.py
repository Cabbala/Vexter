import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.transport_livepaper_observability_watchdog_ci_gate

REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_GROUPED_TEST_FILES = [
    "tests/test_planner_router_transport_livepaper_observability_watchdog.py",
    "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py",
    "tests/test_planner_router_transport_livepaper_observability_regression_pack.py",
    "tests/test_planner_router_transport_livepaper_observability_watchdog_ci_gate.py",
]

EXPECTED_GATE_SURFACE_TESTS = {
    "immutable_handoff_metadata_continuity": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_immutable_handoff_metadata_continuity"
    ],
    "handle_lifecycle_continuity": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_handle_lifecycle_continuity"
    ],
    "planned_runtime_metadata_drift": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_watchdog_regression_pack_locks_planned_runtime_metadata_drift"
    ],
    "status_sink_fan_in": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_status_sink_fan_in"
    ],
    "ack_history_retention": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_ack_history_retention"
    ],
    "quarantine_reason_completeness": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_quarantine_reason_completeness"
    ],
    "manual_stop_all_propagation": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_manual_stop_all_propagation"
    ],
    "snapshot_backed_terminal_detail": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_snapshot_backed_terminal_detail"
    ],
    "normalized_failure_detail_passthrough": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_normalized_failure_detail_passthrough"
    ],
}


def load_watchdog_ci_gate_proof() -> dict[str, object]:
    return json.loads(
        (
            REPO_ROOT
            / "artifacts"
            / "proofs"
            / "task-007-transport-livepaper-observability-watchdog-ci-gate-check.json"
        ).read_text()
    )


@pytest.mark.parametrize("surface_name", EXPECTED_GATE_SURFACE_TESTS, ids=EXPECTED_GATE_SURFACE_TESTS.keys())
def test_transport_livepaper_observability_watchdog_ci_gate_proof_locks_each_surface(
    surface_name: str,
) -> None:
    proof = load_watchdog_ci_gate_proof()

    assert proof["watchdog_ci_gate_suite"]["gate_surface_tests"][surface_name] == EXPECTED_GATE_SURFACE_TESTS[
        surface_name
    ]


def test_transport_livepaper_observability_watchdog_ci_gate_proof_tracks_grouped_suites_and_outputs() -> None:
    proof = load_watchdog_ci_gate_proof()

    assert proof["task_id"] == "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE"
    assert proof["verified_github"]["latest_vexter_pr"] == 57
    assert (
        proof["watchdog_ci_gate_suite"]["suite_group"]
        == "transport_livepaper_observability_watchdog_ci_gate"
    )
    assert proof["watchdog_ci_gate_suite"]["grouped_test_files"] == EXPECTED_GROUPED_TEST_FILES
    assert proof["watchdog_ci_gate_suite"]["grouped_suite_markers"] == [
        "transport_livepaper_observability_watchdog",
        "transport_livepaper_observability_watchdog_runtime",
        "transport_livepaper_observability_watchdog_regression_pack",
    ]
    assert proof["watchdog_ci_gate_suite"]["supporting_test_files"] == [
        "tests/test_planner_router_transport_livepaper_observability_watchdog_ci_gate.py",
    ]
    assert proof["watchdog_ci_gate_suite"]["proof_outputs"] == [
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json",
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-summary.md",
    ]
    assert (
        proof["watchdog_ci_gate_suite"]["proof_artifact_name"]
        == "transport-livepaper-observability-watchdog-ci-gate-proof"
    )
    assert proof["watchdog_ci_gate_suite"]["source_faithful_modes"] == {
        "dexter": "paper_live",
        "mewx": "sim_live",
    }
    assert proof["task_result"]["task_state"] in {
        "transport_livepaper_observability_watchdog_ci_gate_passed",
        "transport_livepaper_observability_watchdog_ci_gate_failed",
    }
    if proof["task_result"]["task_state"] == "transport_livepaper_observability_watchdog_ci_gate_passed":
        assert proof["task_result"]["recommended_next_step"] == "livepaper_observability_spec"
    else:
        assert (
            proof["task_result"]["recommended_next_step"]
            == "transport_livepaper_observability_watchdog_ci_gate"
        )


def test_transport_livepaper_observability_watchdog_ci_gate_workflow_runs_before_component_lanes() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()

    gate_index = workflow.index("- name: Run transport livepaper observability CI gate")
    watchdog_index = workflow.index("- name: Run transport livepaper observability watchdog")
    watchdog_runtime_index = workflow.index("- name: Run transport livepaper observability watchdog runtime")
    watchdog_regression_pack_index = workflow.index(
        "- name: Run transport livepaper observability watchdog regression pack"
    )
    watchdog_ci_gate_index = workflow.index("- name: Run transport livepaper observability watchdog CI gate")
    build_bundle_index = workflow.index("- name: Build proof bundle")
    remaining_tests_index = workflow.index("- name: Run remaining tests")

    assert "./scripts/run_transport_livepaper_observability_watchdog_ci_gate.sh" in workflow
    assert "transport-livepaper-observability-watchdog-ci-gate-proof" in workflow
    assert "cat artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-summary.md" in workflow
    assert (
        'pytest -q -m "not transport_livepaper_observability_watchdog_ci_gate and not '
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
        < build_bundle_index
        < remaining_tests_index
    )


def test_transport_livepaper_observability_watchdog_ci_gate_manifest_and_context_point_to_bundle() -> None:
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())

    assert "scripts/run_transport_livepaper_observability_watchdog_ci_gate.sh" in manifest["scripts"]
    assert (
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate-report.md"
        in manifest["reports"]
    )
    assert (
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json"
        in manifest["proof_files"]
    )
    assert (
        context["current_contract"]["watchdog_ci_gate_marker"]
        == "transport_livepaper_observability_watchdog_ci_gate"
    )
    assert (
        "tests/test_planner_router_transport_livepaper_observability_watchdog_ci_gate.py"
        in context["evidence"]["transport_livepaper_observability_watchdog_ci_gate"]["gate_test_files"]
    )
    assert (
        context["evidence"]["transport_livepaper_observability_watchdog_ci_gate"]["preferred_next_step"]
        == "livepaper_observability_spec"
    )


def test_transport_livepaper_observability_watchdog_ci_gate_script_targets_current_suite() -> None:
    gate_script = (
        REPO_ROOT / "scripts" / "run_transport_livepaper_observability_watchdog_ci_gate.sh"
    ).read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    for file_name in EXPECTED_GROUPED_TEST_FILES:
        assert file_name in gate_script
    assert "transport_livepaper_observability_watchdog_ci_gate" in gate_script
    assert "transport_livepaper_observability_watchdog_ci_gate" in pytest_ini
