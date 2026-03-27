import json
from pathlib import Path

import pytest

from vexter.planner_router.handoff_watchdog import (
    LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES,
    RUNTIME_CURRENT_POINTER_PATHS,
    RUNTIME_CURRENT_TASK_STATE,
    RUNTIME_FAILURE_DETAIL_POINTER,
    evaluate_livepaper_observability_shift_handoff_watchdog,
    RUNTIME_RECOMMENDED_NEXT_STEP,
    RUNTIME_TERMINAL_SNAPSHOT_POINTER,
)


pytestmark = [
    pytest.mark.livepaper_observability_shift_handoff_watchdog_runtime,
    pytest.mark.livepaper_observability_shift_handoff_watchdog_ci_gate,
]

REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-runtime"
    / "HANDOFF.md"
)
PROOF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json"
)
SUMMARY_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-watchdog-runtime-summary.md"
)
REPORT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-runtime-report.md"
)
STATUS_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-runtime-status.md"
)
PROMPT_CONTEXT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-runtime"
    / "CONTEXT.json"
)

EXPECTED_RUNTIME_TEST_FILES = [
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py",
]
EXPECTED_FIRST_DEEP_PROOF_PATH = (
    "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json"
)
EXPECTED_MONITORED_SURFACES = list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES)
SURFACE_MUTATIONS = {
    "current_status": lambda text: text.replace(
        "- task_state: livepaper_observability_shift_handoff_watchdog_runtime_passed",
        "- task_state: livepaper_observability_shift_handoff_watchdog_runtime_passed\n"
        "- task_state: same as before",
    ),
    "proof_and_report_pointers": lambda text: text.replace(
        "- current_report: artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime-report.md",
        "- current_report: artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime-report.md\n"
        "- current_report: artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime-status.md",
    ),
    "omission_drift_partial_visibility": lambda text: text.replace(
        "- omission_present: false",
        "- omission_present: maybe",
    ),
    "manual_stop_all": lambda text: text.replace(
        "- trigger_plan_id_or_none: req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
        "- trigger_plan_id_or_none: same as before",
    ),
    "quarantine": lambda text: text.replace(
        "- quarantine_reason_or_none: timeout_guard",
        "- quarantine_reason_or_none: same as before",
    ),
    "terminal_snapshot": lambda text: text.replace(
        "- terminal_snapshot_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py",
        "- terminal_snapshot_pointer_or_none: none",
    ),
    "normalized_failure_detail": lambda text: text.replace(
        "- failure_detail_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py",
        "- failure_detail_pointer_or_none: none",
    ),
    "open_questions": lambda text: text.replace(
        "- question_1_or_none: none",
        "- question_1_or_none: same as before",
    ),
    "next_shift_priority_checks": lambda text: text.replace(
        "- priority_check_1: confirm the current runtime handoff status, report, and proof JSON before changing task state",
        "- priority_check_1: none",
    ),
}
EXPECTED_SURFACE_TESTS = {
    surface: [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_runtime_flags_follow_up_face_regression[{surface}]"
    ]
    for surface in SURFACE_MUTATIONS
}


def load_runtime_proof() -> dict[str, object]:
    return json.loads(PROOF_PATH.read_text())


def load_last_ledger_entry() -> dict[str, object]:
    lines = (REPO_ROOT / "artifacts" / "task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


def evaluate_runtime_handoff(markdown: str):
    return evaluate_livepaper_observability_shift_handoff_watchdog(
        markdown,
        repo_root=REPO_ROOT,
        expected_first_deep_proof_path=EXPECTED_FIRST_DEEP_PROOF_PATH,
        expected_task_state=RUNTIME_CURRENT_TASK_STATE,
        expected_recommended_next_step=RUNTIME_RECOMMENDED_NEXT_STEP,
        expected_current_pointer_paths=RUNTIME_CURRENT_POINTER_PATHS,
        expected_terminal_snapshot_pointer=RUNTIME_TERMINAL_SNAPSHOT_POINTER,
        expected_failure_detail_pointer=RUNTIME_FAILURE_DETAIL_POINTER,
    )


def test_livepaper_observability_shift_handoff_watchdog_runtime_passes_on_runtime_follow_up_handoff() -> None:
    report = evaluate_runtime_handoff(HANDOFF_PATH.read_text())

    assert report.passed is True
    assert report.findings == ()
    assert report.surface_status == {surface: True for surface in EXPECTED_MONITORED_SURFACES}


@pytest.mark.parametrize("surface_name", SURFACE_MUTATIONS, ids=SURFACE_MUTATIONS.keys())
def test_livepaper_observability_shift_handoff_watchdog_runtime_flags_follow_up_face_regression(
    surface_name: str,
) -> None:
    mutated_handoff = SURFACE_MUTATIONS[surface_name](HANDOFF_PATH.read_text())

    report = evaluate_runtime_handoff(mutated_handoff)

    assert report.passed is False
    surfaces = {finding.surface for finding in report.findings}
    assert surface_name in surfaces
    assert report.surface_status[surface_name] is False


def test_livepaper_observability_shift_handoff_watchdog_runtime_flags_whole_section_omission() -> None:
    original = HANDOFF_PATH.read_text()
    omitted = original.replace(
        "## Terminal Snapshot\n"
        "- terminal_snapshot_present: true\n"
        "- terminal_snapshot_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py\n"
        "- snapshot_signal_visible: true\n"
        "- terminal_stop_reason_visible: true\n"
        "- terminal_anchor_native_session_id: sim_live:req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment\n"
        "- terminal_anchor_handle_id: mewx_frozen_pinned:req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment\n\n",
        "",
    )

    report = evaluate_runtime_handoff(omitted)

    assert report.passed is False
    assert {finding.surface for finding in report.findings} == {"terminal_snapshot"}
    assert report.surface_status["terminal_snapshot"] is False


def test_livepaper_observability_shift_handoff_watchdog_runtime_script_targets_current_suite() -> None:
    runtime_script = (
        REPO_ROOT / "scripts" / "run_livepaper_observability_shift_handoff_watchdog_runtime.sh"
    ).read_text()
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    for file_name in EXPECTED_RUNTIME_TEST_FILES:
        assert file_name in runtime_script
    assert "livepaper_observability_shift_handoff_watchdog_runtime" in runtime_script
    assert "livepaper-observability-shift-handoff-watchdog-runtime-proof" in workflow
    assert "./scripts/run_livepaper_observability_shift_handoff_watchdog_runtime.sh" in workflow
    assert "livepaper_observability_shift_handoff_watchdog_runtime" in pytest_ini


def test_livepaper_observability_shift_handoff_watchdog_runtime_workflow_runs_after_handoff_watchdog() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()

    handoff_ci_check_index = workflow.index("- name: Run livepaper observability shift handoff CI check")
    handoff_watchdog_index = workflow.index("- name: Run livepaper observability shift handoff watchdog")
    handoff_watchdog_runtime_index = workflow.index(
        "- name: Run livepaper observability shift handoff watchdog runtime"
    )
    handoff_watchdog_regression_pack_index = workflow.index(
        "- name: Run livepaper observability shift handoff watchdog regression pack"
    )
    handoff_watchdog_ci_gate_index = workflow.index(
        "- name: Run livepaper observability shift handoff watchdog CI gate"
    )
    build_bundle_index = workflow.index("- name: Build proof bundle")
    remaining_tests_index = workflow.index("- name: Run remaining tests")

    assert (
        "cat artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-summary.md"
        in workflow
    )
    assert (
        "cat artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md"
        in workflow
    )
    assert "not livepaper_observability_shift_handoff_watchdog_runtime" in workflow
    assert "not livepaper_observability_shift_handoff_watchdog_regression_pack" in workflow
    assert (
        handoff_ci_check_index
        < handoff_watchdog_index
        < handoff_watchdog_runtime_index
        < handoff_watchdog_regression_pack_index
        < handoff_watchdog_ci_gate_index
        < build_bundle_index
        < remaining_tests_index
    )


def test_livepaper_observability_shift_handoff_watchdog_runtime_manifest_and_context_point_to_bundle() -> None:
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    ledger = load_last_ledger_entry()
    summary_text = SUMMARY_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    report_text = REPORT_PATH.read_text()

    current_task_id = manifest["task_id"]

    assert manifest["task_id"] == context["current_task"]["id"] == ledger["task_id"]
    assert manifest["status"] == ledger["status"]
    assert manifest["bundle_path"] == ledger["artifact_bundle"]
    if current_task_id == "PATTERN-A-DEMO-EXECUTOR-CUTOVER":
        assert manifest["status"] == "pattern_a_demo_executor_cutover_ready"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/pattern-a-demo-executor-cutover.tar.gz"
        )
    elif current_task_id == "DEMO-FORWARD-ACCEPTANCE-PACK":
        assert manifest["status"] == "demo_forward_acceptance_pack_ready"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-acceptance-pack.tar.gz"
        )
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN":
        assert manifest["status"] == "demo_forward_supervised_run_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run.tar.gz"
        )
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS":
        assert manifest["status"] == "supervised_run_retry_readiness_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-readiness.tar.gz"
        )
    else:
        assert manifest["task_id"] in {
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
        }
        assert manifest["status"] in {
            "livepaper_observability_shift_handoff_watchdog_runtime_passed",
            "livepaper_observability_shift_handoff_watchdog_regression_pack_passed",
            "livepaper_observability_shift_handoff_watchdog_ci_gate_passed",
            "livepaper_observability_shift_handoff_watchdog_ci_gate_failed",
        }
        assert manifest["bundle_path"] in {
            "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-runtime.tar.gz",
            "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz",
            "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz",
        }
    assert "scripts/run_livepaper_observability_shift_handoff_watchdog_runtime.sh" in manifest["scripts"]
    assert (
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime-report.md"
        in manifest["reports"]
    )
    assert (
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json"
        in manifest["proof_files"]
    )
    assert (
        context["current_contract"]["livepaper_observability_shift_handoff_watchdog_runtime_marker"]
        == "livepaper_observability_shift_handoff_watchdog_runtime"
    )
    assert (
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py"
        in context["evidence"]["livepaper_observability_shift_handoff_watchdog_runtime"][
            "runtime_test_files"
        ]
    )
    assert (
        context["evidence"]["livepaper_observability_shift_handoff_watchdog_runtime"][
            "preferred_next_step"
        ]
        == "livepaper_observability_shift_handoff_watchdog_regression_pack"
    )
    assert (
        prompt_context["recommended_next_task"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK"
    )
    assert "livepaper_observability_shift_handoff_watchdog_regression_pack" in summary_text
    assert "livepaper_observability_shift_handoff_watchdog_runtime_passed" in status_text
    assert "livepaper_observability_shift_handoff_watchdog_regression_pack" in report_text


def test_livepaper_observability_shift_handoff_watchdog_runtime_proof_tracks_regression_pack_as_next_step() -> None:
    proof = load_runtime_proof()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME"
    assert proof["verified_github"]["latest_vexter_pr"] == 66
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "2cd19d8ddbd5ef4918b41536494e10d4f2a9c125"
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_runtime"]["suite_group"]
        == "livepaper_observability_shift_handoff_watchdog_runtime"
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_runtime"]["runtime_test_files"]
        == EXPECTED_RUNTIME_TEST_FILES
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_runtime"]["monitored_surfaces"]
        == EXPECTED_MONITORED_SURFACES
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_runtime"]["watchdog_face_tests"]
        == EXPECTED_SURFACE_TESTS
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_runtime"]["proof_artifact_name"]
        == "livepaper-observability-shift-handoff-watchdog-runtime-proof"
    )
    assert set(
        proof["livepaper_observability_shift_handoff_watchdog_runtime"]["watchdog_snapshot"]
    ) == {
        "checked_handoff",
        "findings",
        "monitored_surfaces",
        "passed",
        "surface_status",
    }
    assert set(
        proof["livepaper_observability_shift_handoff_watchdog_runtime"]["runtime_follow_up_focus"]
    ) == {
        "baseline_handoff_proof",
        "runtime_proof",
        "runtime_status_report",
        "runtime_report",
    }
    assert proof["task_result"]["task_state"] in {
        "livepaper_observability_shift_handoff_watchdog_runtime_passed",
        "livepaper_observability_shift_handoff_watchdog_runtime_failed",
    }
    if proof["task_result"]["task_state"] == "livepaper_observability_shift_handoff_watchdog_runtime_passed":
        assert (
            proof["task_result"]["recommended_next_step"]
            == "livepaper_observability_shift_handoff_watchdog_regression_pack"
        )
    else:
        assert (
            proof["task_result"]["recommended_next_step"]
            == "livepaper_observability_shift_handoff_watchdog_runtime"
        )
