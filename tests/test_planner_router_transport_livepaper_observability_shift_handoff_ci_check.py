import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.livepaper_observability_shift_handoff_ci_check

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DOC_PATH = REPO_ROOT / "docs" / "livepaper_observability_shift_handoff_template.md"
DRILL_DOC_PATH = REPO_ROOT / "docs" / "livepaper_observability_shift_handoff_drill.md"
HANDOFF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-drill"
    / "HANDOFF.md"
)
PROOF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-ci-check-check.json"
)
SUMMARY_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-ci-check-summary.md"
)
REPORT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-ci-check-report.md"
)
STATUS_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-ci-check-status.md"
)
PROMPT_CONTEXT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-ci-check"
    / "CONTEXT.json"
)

EXPECTED_GROUPED_TEST_FILES = [
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_template.py",
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_drill.py",
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py",
]

FACE_ASSERTIONS = {
    "current_status": [
        (TEMPLATE_DOC_PATH, "## 1. Current status"),
        (TEMPLATE_DOC_PATH, "current task status"),
        (DRILL_DOC_PATH, "current status"),
        (HANDOFF_PATH, "## Current Status"),
        (HANDOFF_PATH, "- task_state: livepaper_observability_shift_handoff_drill_passed"),
        (HANDOFF_PATH, "- current_action: continue"),
    ],
    "proof_and_report_pointers": [
        (TEMPLATE_DOC_PATH, "## 2. Proof and report pointers"),
        (TEMPLATE_DOC_PATH, "first deep proof to open next"),
        (DRILL_DOC_PATH, "proof and report pointers"),
        (HANDOFF_PATH, "## Proof and Report Pointers"),
        (HANDOFF_PATH, "- current_status_report:"),
        (HANDOFF_PATH, "- current_proof_json:"),
    ],
    "omission_drift_partial_visibility": [
        (TEMPLATE_DOC_PATH, "## 3. `omission` / `drift` / `partial_visibility`"),
        (DRILL_DOC_PATH, "`omission`, `drift`, and `partial_visibility`"),
        (HANDOFF_PATH, "- omission_present: false"),
        (HANDOFF_PATH, "- drift_present: false"),
        (HANDOFF_PATH, "- partial_visibility_present: false"),
        (HANDOFF_PATH, "- exact_broken_surface_or_none: none"),
    ],
    "manual_stop_all": [
        (TEMPLATE_DOC_PATH, "whether `manual_latched_stop_all` is visible"),
        (TEMPLATE_DOC_PATH, "`halt_mode`, `trigger_plan_id`, and `stop_reason`, or `none`"),
        (DRILL_DOC_PATH, "manual stop-all and quarantine state"),
        (HANDOFF_PATH, "- manual_stop_all_visible: true"),
        (HANDOFF_PATH, "- halt_mode_or_none: manual_latched_stop_all"),
        (HANDOFF_PATH, "- stop_reason_or_none: manual_latched_stop_all"),
    ],
    "quarantine": [
        (TEMPLATE_DOC_PATH, "whether quarantine is active"),
        (TEMPLATE_DOC_PATH, "`quarantine_reason`, or `none`"),
        (DRILL_DOC_PATH, "manual stop-all and quarantine state"),
        (HANDOFF_PATH, "- quarantine_active: true"),
        (HANDOFF_PATH, "- quarantine_reason_or_none: timeout_guard"),
        (HANDOFF_PATH, "- continuity_check:"),
    ],
    "terminal_snapshot": [
        (TEMPLATE_DOC_PATH, "## 5. Terminal snapshot state"),
        (DRILL_DOC_PATH, "terminal snapshot state"),
        (HANDOFF_PATH, "## Terminal Snapshot"),
        (HANDOFF_PATH, "- terminal_snapshot_present: true"),
        (HANDOFF_PATH, "- snapshot_signal_visible: true"),
    ],
    "normalized_failure_detail": [
        (TEMPLATE_DOC_PATH, "## 6. Normalized failure detail state"),
        (DRILL_DOC_PATH, "normalized failure detail state"),
        (HANDOFF_PATH, "## Normalized Failure Detail"),
        (HANDOFF_PATH, "- normalized_failure_detail_present: true"),
        (HANDOFF_PATH, "- failure_code: status_timeout"),
        (HANDOFF_PATH, "- failure_stage: status"),
    ],
    "open_questions": [
        (TEMPLATE_DOC_PATH, "## 7. Open questions"),
        (DRILL_DOC_PATH, "open questions"),
        (HANDOFF_PATH, "## Open Questions"),
        (HANDOFF_PATH, "- question_1_or_none: none"),
        (HANDOFF_PATH, "- question_2_or_none: none"),
    ],
    "next_shift_priority_checks": [
        (TEMPLATE_DOC_PATH, "## 8. Next-shift priority checks"),
        (DRILL_DOC_PATH, "next-shift priority checks"),
        (HANDOFF_PATH, "## Next-Shift Priority Checks"),
        (HANDOFF_PATH, "- priority_check_1:"),
        (HANDOFF_PATH, "- priority_check_2_or_none:"),
    ],
}

EXPECTED_GATE_SURFACE_TESTS = {
    face: [
        f"tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_locks_required_face[{face}]"
    ]
    for face in FACE_ASSERTIONS
}


def load_ci_gate_proof() -> dict[str, object]:
    return json.loads(PROOF_PATH.read_text())


def load_last_ledger_entry() -> dict[str, object]:
    lines = (REPO_ROOT / "artifacts" / "task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


@pytest.mark.parametrize("surface_name", FACE_ASSERTIONS, ids=FACE_ASSERTIONS.keys())
def test_livepaper_observability_shift_handoff_ci_check_locks_required_face(surface_name: str) -> None:
    for path, needle in FACE_ASSERTIONS[surface_name]:
        assert needle.lower() in path.read_text().lower(), f"{surface_name} missing `{needle}` in {path}"


def test_livepaper_observability_shift_handoff_ci_check_completeness_rules_remain_explicit() -> None:
    template_doc = TEMPLATE_DOC_PATH.read_text().lower()
    drill_doc = DRILL_DOC_PATH.read_text().lower()
    handoff = HANDOFF_PATH.read_text().lower()

    for needle in (
        "every required face is filled or explicitly marked `none`",
        "manual stop-all, quarantine, terminal snapshot, and normalized failure detail are each recorded explicitly",
        "every required handoff face is present",
        "no face relies on \"same as before\"",
        "- every_required_face_filled_or_none: true",
        "- proof_and_report_pointers_checked: true",
        "- containment_and_failure_faces_explicit: true",
    ):
        assert needle in template_doc or needle in drill_doc or needle in handoff


def test_livepaper_observability_shift_handoff_ci_check_proof_tracks_grouped_suite_and_outputs() -> None:
    proof = load_ci_gate_proof()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK"
    assert proof["verified_github"]["latest_vexter_pr"] == 65
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "51cfec8b85b5020ba5f6d0f72dceb5c47c339c06"
    )
    assert (
        proof["livepaper_observability_shift_handoff_ci_check"]["suite_group"]
        == "livepaper_observability_shift_handoff_ci_check"
    )
    assert (
        proof["livepaper_observability_shift_handoff_ci_check"]["grouped_test_files"]
        == EXPECTED_GROUPED_TEST_FILES
    )
    assert (
        proof["livepaper_observability_shift_handoff_ci_check"]["grouped_suite_markers"]
        == ["livepaper_observability_shift_handoff_ci_check"]
    )
    assert (
        proof["livepaper_observability_shift_handoff_ci_check"]["required_handoff_faces"]
        == list(FACE_ASSERTIONS)
    )
    assert proof["livepaper_observability_shift_handoff_ci_check"]["proof_outputs"] == [
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-summary.md",
    ]
    assert (
        proof["livepaper_observability_shift_handoff_ci_check"]["proof_artifact_name"]
        == "livepaper-observability-shift-handoff-ci-check-proof"
    )
    assert set(
        proof["livepaper_observability_shift_handoff_ci_check"]["normalized_failure_detail"]
    ) == {
        "failed_faces_or_none",
        "failed_tests_or_none",
        "non_surface_failures_or_none",
        "failure_category_or_none",
    }
    assert proof["task_result"]["task_state"] in {
        "livepaper_observability_shift_handoff_ci_check_passed",
        "livepaper_observability_shift_handoff_ci_check_failed",
    }


@pytest.mark.parametrize("surface_name", EXPECTED_GATE_SURFACE_TESTS, ids=EXPECTED_GATE_SURFACE_TESTS.keys())
def test_livepaper_observability_shift_handoff_ci_check_proof_locks_each_surface(surface_name: str) -> None:
    proof = load_ci_gate_proof()

    assert (
        proof["livepaper_observability_shift_handoff_ci_check"]["gate_surface_tests"][surface_name]
        == EXPECTED_GATE_SURFACE_TESTS[surface_name]
    )


def test_livepaper_observability_shift_handoff_ci_check_workflow_runs_before_bundle_build() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()

    watchdog_ci_gate_index = workflow.index("- name: Run transport livepaper observability watchdog CI gate")
    handoff_ci_gate_index = workflow.index("- name: Run livepaper observability shift handoff CI check")
    handoff_watchdog_index = workflow.index("- name: Run livepaper observability shift handoff watchdog")
    build_bundle_index = workflow.index("- name: Build proof bundle")
    remaining_tests_index = workflow.index("- name: Run remaining tests")

    assert "./scripts/run_livepaper_observability_shift_handoff_ci_check.sh" in workflow
    assert "livepaper-observability-shift-handoff-ci-check-proof" in workflow
    assert "cat artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-summary.md" in workflow
    assert "not livepaper_observability_shift_handoff_ci_check" in workflow
    assert (
        watchdog_ci_gate_index
        < handoff_ci_gate_index
        < handoff_watchdog_index
        < build_bundle_index
        < remaining_tests_index
    )


def test_livepaper_observability_shift_handoff_ci_check_manifest_and_context_point_to_bundle() -> None:
    proof = load_ci_gate_proof()
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    ledger = load_last_ledger_entry()
    summary_text = SUMMARY_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    bundle_script = (REPO_ROOT / "scripts" / "build_proof_bundle.sh").read_text()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK"
    assert manifest["task_id"] == context["current_task"]["id"] == ledger["task_id"]
    assert manifest["task_id"] in {
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
    }
    assert manifest["status"] == ledger["status"]
    assert manifest["status"] in {
        "livepaper_observability_shift_handoff_watchdog_passed",
        "livepaper_observability_shift_handoff_watchdog_runtime_passed",
        "livepaper_observability_shift_handoff_watchdog_regression_pack_passed",
        "livepaper_observability_shift_handoff_watchdog_ci_gate_passed",
        "livepaper_observability_shift_handoff_watchdog_ci_gate_failed",
    }
    assert manifest["bundle_path"] == ledger["artifact_bundle"]
    assert manifest["bundle_path"] in {
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-runtime.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz",
    }
    assert "scripts/run_livepaper_observability_shift_handoff_ci_check.sh" in manifest["scripts"]
    assert (
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check-report.md"
        in manifest["reports"]
    )
    assert (
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-check.json"
        in manifest["proof_files"]
    )
    assert (
        context["current_contract"]["livepaper_observability_shift_handoff_ci_check_marker"]
        == "livepaper_observability_shift_handoff_ci_check"
    )
    assert (
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py"
        in context["evidence"]["livepaper_observability_shift_handoff_ci_check"]["gate_test_files"]
    )
    assert (
        context["evidence"]["livepaper_observability_shift_handoff_ci_check"]["preferred_next_step"]
        == "livepaper_observability_shift_handoff_watchdog"
    )
    assert prompt_context["recommended_next_task"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG"
    assert (
        "livepaper_observability_shift_handoff_watchdog" in summary_text
        or "livepaper_observability_shift_handoff_ci_check" in summary_text
    )
    assert "livepaper_observability_shift_handoff_ci_check_passed" in status_text
    assert "livepaper_observability_shift_handoff_watchdog" in report_text
    assert "task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz" in bundle_script


def test_livepaper_observability_shift_handoff_ci_check_script_targets_current_suite() -> None:
    gate_script = (REPO_ROOT / "scripts" / "run_livepaper_observability_shift_handoff_ci_check.sh").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()
    template_test = (
        REPO_ROOT / "tests" / "test_planner_router_transport_livepaper_observability_shift_handoff_template.py"
    ).read_text()
    drill_test = (
        REPO_ROOT / "tests" / "test_planner_router_transport_livepaper_observability_shift_handoff_drill.py"
    ).read_text()

    for file_name in EXPECTED_GROUPED_TEST_FILES:
        assert file_name in gate_script
    assert "livepaper_observability_shift_handoff_ci_check" in gate_script
    assert "livepaper_observability_shift_handoff_ci_check" in pytest_ini
    assert "pytestmark = pytest.mark.livepaper_observability_shift_handoff_ci_check" in template_test
    assert "pytestmark = pytest.mark.livepaper_observability_shift_handoff_ci_check" in drill_test
