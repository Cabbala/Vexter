import json
from pathlib import Path

import pytest

from vexter.planner_router.handoff_watchdog import (
    HANDOFF_PATH,
    LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES,
    evaluate_livepaper_observability_shift_handoff_watchdog,
)


pytestmark = [
    pytest.mark.livepaper_observability_shift_handoff_watchdog,
    pytest.mark.livepaper_observability_shift_handoff_watchdog_ci_gate,
]

REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-watchdog-check.json"
)
SUMMARY_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-watchdog-summary.md"
)
REPORT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-report.md"
)
STATUS_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-status.md"
)
PROMPT_CONTEXT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog"
    / "CONTEXT.json"
)
EXPECTED_WATCHDOG_TEST_FILES = [
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py",
]
EXPECTED_MONITORED_SURFACES = list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES)
SURFACE_MUTATIONS = {
    "current_status": lambda text: text.replace(
        "- status_delivery: poll_first",
        "- status_delivery: push_first",
    ),
    "proof_and_report_pointers": lambda text: text.replace(
        "- current_proof_json: artifacts/proofs/task-007-livepaper-observability-shift-handoff-drill-check.json",
        "- current_proof_json: artifacts/reports/task-007-livepaper-observability-shift-handoff-drill-status.md",
    ).replace(
        "- shortest_proof_trail: status -> report -> summary -> contract -> proof -> sample handoff",
        "- shortest_proof_trail: same as before",
    ),
    "omission_drift_partial_visibility": lambda text: text.replace(
        "- partial_visibility_present: false",
        "- partial_visibility_present: maybe",
    ),
    "manual_stop_all": lambda text: text.replace(
        "- stop_reason_or_none: manual_latched_stop_all",
        "- stop_reason_or_none: none",
    ),
    "quarantine": lambda text: text.replace(
        "- quarantine_reason_or_none: timeout_guard",
        "- quarantine_reason_or_none: none",
    ),
    "terminal_snapshot": lambda text: text.replace(
        "- terminal_snapshot_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_regression_pack.py",
        "- terminal_snapshot_pointer_or_none: none",
    ),
    "normalized_failure_detail": lambda text: text.replace(
        "- failure_detail_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_regression_pack.py",
        "- failure_detail_pointer_or_none: none",
    ),
    "open_questions": lambda text: text.replace(
        "- question_2_or_none: none",
        "- question_2_or_none: same as before",
    ),
    "next_shift_priority_checks": lambda text: text.replace(
        "- priority_check_1: confirm the current report, proof summary, and proof JSON before changing any task state",
        "- priority_check_1: none",
    ),
}
EXPECTED_SURFACE_TESTS = {
    surface: [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_flags_face_regression[{surface}]"
    ]
    for surface in SURFACE_MUTATIONS
}


def load_watchdog_proof() -> dict[str, object]:
    return json.loads(PROOF_PATH.read_text())


def load_last_ledger_entry() -> dict[str, object]:
    lines = (REPO_ROOT / "artifacts" / "task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


def test_livepaper_observability_shift_handoff_watchdog_passes_on_fixed_surface() -> None:
    report = evaluate_livepaper_observability_shift_handoff_watchdog(
        (REPO_ROOT / HANDOFF_PATH).read_text(),
        repo_root=REPO_ROOT,
    )

    assert report.passed is True
    assert report.findings == ()
    assert report.surface_status == {surface: True for surface in EXPECTED_MONITORED_SURFACES}


@pytest.mark.parametrize("surface_name", SURFACE_MUTATIONS, ids=SURFACE_MUTATIONS.keys())
def test_livepaper_observability_shift_handoff_watchdog_flags_face_regression(surface_name: str) -> None:
    mutated_handoff = SURFACE_MUTATIONS[surface_name]((REPO_ROOT / HANDOFF_PATH).read_text())

    report = evaluate_livepaper_observability_shift_handoff_watchdog(
        mutated_handoff,
        repo_root=REPO_ROOT,
    )

    assert report.passed is False
    surfaces = {finding.surface for finding in report.findings}
    assert surface_name in surfaces
    assert report.surface_status[surface_name] is False


def test_livepaper_observability_shift_handoff_watchdog_proof_tracks_monitored_surfaces_and_outputs() -> None:
    proof = load_watchdog_proof()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG"
    assert proof["verified_github"]["latest_vexter_pr"] == 65
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "51cfec8b85b5020ba5f6d0f72dceb5c47c339c06"
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog"]["suite_group"]
        == "livepaper_observability_shift_handoff_watchdog"
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog"]["grouped_test_files"]
        == EXPECTED_WATCHDOG_TEST_FILES
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog"]["grouped_suite_markers"]
        == ["livepaper_observability_shift_handoff_watchdog"]
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog"]["monitored_surfaces"]
        == EXPECTED_MONITORED_SURFACES
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog"]["watchdog_face_tests"]
        == EXPECTED_SURFACE_TESTS
    )
    assert proof["livepaper_observability_shift_handoff_watchdog"]["proof_outputs"] == [
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-summary.md",
    ]
    assert (
        proof["livepaper_observability_shift_handoff_watchdog"]["proof_artifact_name"]
        == "livepaper-observability-shift-handoff-watchdog-proof"
    )
    assert set(
        proof["livepaper_observability_shift_handoff_watchdog"]["watchdog_snapshot"]
    ) == {
        "checked_handoff",
        "findings",
        "monitored_surfaces",
        "passed",
        "surface_status",
    }
    assert set(
        proof["livepaper_observability_shift_handoff_watchdog"]["normalized_failure_detail"]
    ) == {
        "finding_surfaces_or_none",
        "finding_classes_or_none",
        "failed_tests_or_none",
        "non_surface_failures_or_none",
    }
    assert proof["task_result"]["task_state"] in {
        "livepaper_observability_shift_handoff_watchdog_passed",
        "livepaper_observability_shift_handoff_watchdog_failed",
    }


def test_livepaper_observability_shift_handoff_watchdog_workflow_runs_after_handoff_ci_check_before_bundle_build() -> None:
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

    assert "./scripts/run_livepaper_observability_shift_handoff_watchdog.sh" in workflow
    assert "livepaper-observability-shift-handoff-watchdog-proof" in workflow
    assert (
        "cat artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-summary.md"
        in workflow
    )
    assert "not livepaper_observability_shift_handoff_watchdog" in workflow
    assert (
        handoff_ci_check_index
        < handoff_watchdog_index
        < handoff_watchdog_runtime_index
        < handoff_watchdog_regression_pack_index
        < handoff_watchdog_ci_gate_index
        < build_bundle_index
        < remaining_tests_index
    )


def test_livepaper_observability_shift_handoff_watchdog_manifest_and_context_point_to_bundle() -> None:
    proof = load_watchdog_proof()
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    ledger = load_last_ledger_entry()
    summary_text = SUMMARY_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    bundle_script = (REPO_ROOT / "scripts" / "build_proof_bundle.sh").read_text()

    current_task_id = manifest["task_id"]

    assert manifest["task_id"] == context["current_task"]["id"] == ledger["task_id"]
    assert manifest["status"] == ledger["status"]
    assert (
        manifest["bundle_path"]
        == ledger["artifact_bundle"]
    )
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
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE":
        assert manifest["status"] == "supervised_run_retry_gate_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz"
        )
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK":
        assert manifest["status"] == "supervised_run_retry_gate_attestation_record_pack_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack.tar.gz"
        )
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT":
        assert manifest["status"] == "supervised_run_retry_gate_attestation_audit_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz"
        )
    else:
        assert current_task_id in {
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG",
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
        }
        assert manifest["status"] in {
            "livepaper_observability_shift_handoff_watchdog_passed",
            "livepaper_observability_shift_handoff_watchdog_runtime_passed",
            "livepaper_observability_shift_handoff_watchdog_regression_pack_passed",
            "livepaper_observability_shift_handoff_watchdog_ci_gate_passed",
            "livepaper_observability_shift_handoff_watchdog_ci_gate_failed",
        }
        assert manifest["bundle_path"] in {
            "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog.tar.gz",
            "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-runtime.tar.gz",
            "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz",
            "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz",
        }
    assert "scripts/run_livepaper_observability_shift_handoff_watchdog.sh" in manifest["scripts"]
    assert (
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-report.md"
        in manifest["reports"]
    )
    assert (
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json"
        in manifest["proof_files"]
    )
    assert (
        context["current_contract"]["livepaper_observability_shift_handoff_watchdog_marker"]
        == "livepaper_observability_shift_handoff_watchdog"
    )
    assert (
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py"
        in context["evidence"]["livepaper_observability_shift_handoff_watchdog"]["watchdog_test_files"]
    )
    assert (
        context["evidence"]["livepaper_observability_shift_handoff_watchdog"]["preferred_next_step"]
        == "livepaper_observability_shift_handoff_watchdog_runtime"
    )
    assert (
        prompt_context["recommended_next_task"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME"
    )
    assert "livepaper_observability_shift_handoff_watchdog_runtime" in summary_text
    assert "livepaper_observability_shift_handoff_watchdog_passed" in status_text
    assert "livepaper_observability_shift_handoff_watchdog_runtime" in report_text
    if current_task_id == "PATTERN-A-DEMO-EXECUTOR-CUTOVER":
        assert "pattern-a-demo-executor-cutover.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-ACCEPTANCE-PACK":
        assert "demo-forward-acceptance-pack.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN":
        assert "demo-forward-supervised-run.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS":
        assert "demo-forward-supervised-run-retry-readiness.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE":
        assert "demo-forward-supervised-run-retry-gate.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK":
        assert "demo-forward-supervised-run-retry-gate-attestation-record-pack.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT":
        assert "demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz" in bundle_script
    else:
        assert "task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz" in bundle_script


def test_livepaper_observability_shift_handoff_watchdog_script_targets_current_suite() -> None:
    gate_script = (REPO_ROOT / "scripts" / "run_livepaper_observability_shift_handoff_watchdog.sh").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    for file_name in EXPECTED_WATCHDOG_TEST_FILES:
        assert file_name in gate_script
    assert "livepaper_observability_shift_handoff_watchdog" in gate_script
    assert "livepaper_observability_shift_handoff_watchdog" in pytest_ini
