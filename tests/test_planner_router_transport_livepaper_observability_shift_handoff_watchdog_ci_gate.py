import json
from pathlib import Path

import pytest

from vexter.planner_router.handoff_watchdog import (
    CI_GATE_CURRENT_POINTER_PATHS,
    CI_GATE_CURRENT_TASK_STATE,
    CI_GATE_FAILURE_DETAIL_POINTER,
    CI_GATE_FIRST_DEEP_PROOF_PATH,
    CI_GATE_RECOMMENDED_NEXT_STEP,
    CI_GATE_TERMINAL_SNAPSHOT_POINTER,
    DEFAULT_CURRENT_POINTER_PATHS,
    DEFAULT_CURRENT_TASK_STATE,
    DEFAULT_FAILURE_DETAIL_POINTER,
    DEFAULT_FIRST_DEEP_PROOF_PATH,
    DEFAULT_RECOMMENDED_NEXT_STEP,
    DEFAULT_TERMINAL_SNAPSHOT_POINTER,
    HANDOFF_CI_GATE_PATH,
    HANDOFF_PATH,
    LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES,
    RUNTIME_CURRENT_POINTER_PATHS,
    RUNTIME_CURRENT_TASK_STATE,
    RUNTIME_FAILURE_DETAIL_POINTER,
    RUNTIME_FIRST_DEEP_PROOF_PATH,
    RUNTIME_RECOMMENDED_NEXT_STEP,
    RUNTIME_TERMINAL_SNAPSHOT_POINTER,
    evaluate_livepaper_observability_shift_handoff_watchdog,
)


pytestmark = pytest.mark.livepaper_observability_shift_handoff_watchdog_ci_gate

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_HANDOFF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-runtime"
    / "HANDOFF.md"
)
REGRESSION_PACK_HANDOFF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-regression-pack"
    / "HANDOFF.md"
)
PROOF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json"
)
SUMMARY_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md"
)
REPORT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-report.md"
)
STATUS_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-status.md"
)
PROMPT_CONTEXT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-ci-gate"
    / "CONTEXT.json"
)

EXPECTED_GROUPED_TEST_FILES = [
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py",
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py",
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py",
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py",
]
EXPECTED_SUPPORTING_TEST_FILES = [
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py",
]
EXPECTED_GROUPED_SUITE_MARKERS = [
    "livepaper_observability_shift_handoff_watchdog",
    "livepaper_observability_shift_handoff_watchdog_runtime",
    "livepaper_observability_shift_handoff_watchdog_regression_pack",
]
EXPECTED_MONITORED_SURFACES = list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES)
REGRESSION_PACK_CURRENT_POINTER_PATHS = {
    "current_status_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md",
    "current_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md",
    "current_proof_summary": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md",
    "current_proof_json": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
}
REGRESSION_PACK_FIRST_DEEP_PROOF_PATH = (
    "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json"
)
EXPECTED_GATE_SURFACE_TESTS = {
    surface: [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_flags_face_regression[{surface}]",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_runtime_flags_follow_up_face_regression[{surface}]",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_regression_pack_flags_face_regression[{surface}]",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_regression_pack_flags_surface_omission[{surface}]",
    ]
    for surface in EXPECTED_MONITORED_SURFACES
}


def evaluate_case(
    markdown: str,
    *,
    expected_first_deep_proof_path: str,
    expected_task_state: str,
    expected_recommended_next_step: str,
    expected_current_pointer_paths: dict[str, str],
    expected_terminal_snapshot_pointer: str,
    expected_failure_detail_pointer: str,
):
    return evaluate_livepaper_observability_shift_handoff_watchdog(
        markdown,
        repo_root=REPO_ROOT,
        expected_first_deep_proof_path=expected_first_deep_proof_path,
        expected_task_state=expected_task_state,
        expected_recommended_next_step=expected_recommended_next_step,
        expected_current_pointer_paths=expected_current_pointer_paths,
        expected_terminal_snapshot_pointer=expected_terminal_snapshot_pointer,
        expected_failure_detail_pointer=expected_failure_detail_pointer,
    )


CANONICAL_HANDOFF_CASES = {
    "baseline": (
        REPO_ROOT / HANDOFF_PATH,
        dict(
            expected_first_deep_proof_path=DEFAULT_FIRST_DEEP_PROOF_PATH,
            expected_task_state=DEFAULT_CURRENT_TASK_STATE,
            expected_recommended_next_step=DEFAULT_RECOMMENDED_NEXT_STEP,
            expected_current_pointer_paths=DEFAULT_CURRENT_POINTER_PATHS,
            expected_terminal_snapshot_pointer=DEFAULT_TERMINAL_SNAPSHOT_POINTER,
            expected_failure_detail_pointer=DEFAULT_FAILURE_DETAIL_POINTER,
        ),
    ),
    "runtime": (
        RUNTIME_HANDOFF_PATH,
        dict(
            expected_first_deep_proof_path=RUNTIME_FIRST_DEEP_PROOF_PATH,
            expected_task_state=RUNTIME_CURRENT_TASK_STATE,
            expected_recommended_next_step=RUNTIME_RECOMMENDED_NEXT_STEP,
            expected_current_pointer_paths=RUNTIME_CURRENT_POINTER_PATHS,
            expected_terminal_snapshot_pointer=RUNTIME_TERMINAL_SNAPSHOT_POINTER,
            expected_failure_detail_pointer=RUNTIME_FAILURE_DETAIL_POINTER,
        ),
    ),
    "regression_pack": (
        REGRESSION_PACK_HANDOFF_PATH,
        dict(
            expected_first_deep_proof_path=REGRESSION_PACK_FIRST_DEEP_PROOF_PATH,
            expected_task_state="livepaper_observability_shift_handoff_watchdog_regression_pack_passed",
            expected_recommended_next_step="livepaper_observability_shift_handoff_watchdog_ci_gate",
            expected_current_pointer_paths=REGRESSION_PACK_CURRENT_POINTER_PATHS,
            expected_terminal_snapshot_pointer=RUNTIME_TERMINAL_SNAPSHOT_POINTER,
            expected_failure_detail_pointer=RUNTIME_FAILURE_DETAIL_POINTER,
        ),
    ),
    "ci_gate": (
        REPO_ROOT / HANDOFF_CI_GATE_PATH,
        dict(
            expected_first_deep_proof_path=CI_GATE_FIRST_DEEP_PROOF_PATH,
            expected_task_state=CI_GATE_CURRENT_TASK_STATE,
            expected_recommended_next_step=CI_GATE_RECOMMENDED_NEXT_STEP,
            expected_current_pointer_paths=CI_GATE_CURRENT_POINTER_PATHS,
            expected_terminal_snapshot_pointer=CI_GATE_TERMINAL_SNAPSHOT_POINTER,
            expected_failure_detail_pointer=CI_GATE_FAILURE_DETAIL_POINTER,
        ),
    ),
}


def load_proof() -> dict[str, object]:
    return json.loads(PROOF_PATH.read_text())


def load_last_ledger_entry() -> dict[str, object]:
    lines = (REPO_ROOT / "artifacts" / "task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


@pytest.mark.parametrize("case_name", CANONICAL_HANDOFF_CASES, ids=CANONICAL_HANDOFF_CASES.keys())
def test_livepaper_observability_shift_handoff_watchdog_ci_gate_passes_on_canonical_handoffs(
    case_name: str,
) -> None:
    handoff_path, kwargs = CANONICAL_HANDOFF_CASES[case_name]
    report = evaluate_case(handoff_path.read_text(), **kwargs)

    if case_name != "ci_gate":
        assert report.passed is True
        assert report.findings == ()
        assert report.surface_status == {surface: True for surface in EXPECTED_MONITORED_SURFACES}
        return

    proof = load_proof()
    current_snapshot = proof["livepaper_observability_shift_handoff_watchdog_ci_gate"][
        "current_handoff_watchdog_snapshot"
    ]

    assert report.passed is current_snapshot["passed"]
    assert dict(report.surface_status) == current_snapshot["surface_status"]


@pytest.mark.parametrize("surface_name", EXPECTED_GATE_SURFACE_TESTS, ids=EXPECTED_GATE_SURFACE_TESTS.keys())
def test_livepaper_observability_shift_handoff_watchdog_ci_gate_proof_locks_each_surface(
    surface_name: str,
) -> None:
    proof = load_proof()

    assert (
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["gate_surface_tests"][
            surface_name
        ]
        == EXPECTED_GATE_SURFACE_TESTS[surface_name]
    )


def test_livepaper_observability_shift_handoff_watchdog_ci_gate_proof_tracks_outputs() -> None:
    proof = load_proof()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE"
    assert proof["verified_github"]["latest_vexter_pr"] == 68
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "32133ff2acd233e0873d3de5817f2b31acafe809"
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["suite_group"]
        == "livepaper_observability_shift_handoff_watchdog_ci_gate"
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["grouped_test_files"]
        == EXPECTED_GROUPED_TEST_FILES
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["supporting_test_files"]
        == EXPECTED_SUPPORTING_TEST_FILES
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["grouped_suite_markers"]
        == EXPECTED_GROUPED_SUITE_MARKERS
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["monitored_surfaces"]
        == EXPECTED_MONITORED_SURFACES
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["gate_surface_tests"]
        == EXPECTED_GATE_SURFACE_TESTS
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["proof_outputs"]
        == [
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json",
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md",
        ]
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["proof_artifact_name"]
        == "livepaper-observability-shift-handoff-watchdog-ci-gate-proof"
    )
    assert set(
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"][
            "current_handoff_watchdog_snapshot"
        ]
    ) == {"checked_handoff", "findings", "monitored_surfaces", "passed", "surface_status"}
    assert set(
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["component_suites"].keys()
    ) == {"watchdog", "watchdog_runtime", "watchdog_regression_pack"}
    assert set(
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"]["normalized_failure_detail"]
    ) == {
        "broken_handoff_watchdog_surfaces_or_none",
        "failure_classes_or_none",
        "failed_tests_or_none",
        "non_surface_failures_or_none",
    }
    assert proof["task_result"]["task_state"] in {
        "livepaper_observability_shift_handoff_watchdog_ci_gate_passed",
        "livepaper_observability_shift_handoff_watchdog_ci_gate_failed",
    }
    if proof["task_result"]["task_state"] == "livepaper_observability_shift_handoff_watchdog_ci_gate_passed":
        assert (
            proof["next_task_evaluation"]["transport_livepaper_observability_acceptance_pack"][
                "recommended"
            ]
            is True
        )
        assert (
            proof["task_result"]["recommended_next_step"]
            == "transport_livepaper_observability_acceptance_pack"
        )
    else:
        assert (
            proof["next_task_evaluation"]["transport_livepaper_observability_acceptance_pack"][
                "recommended"
            ]
            is False
        )
        assert (
            proof["task_result"]["recommended_next_step"]
            == "livepaper_observability_shift_handoff_watchdog_ci_gate"
        )


def test_livepaper_observability_shift_handoff_watchdog_ci_gate_workflow_runs_after_regression_pack() -> None:
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

    assert "./scripts/run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh" in workflow
    assert "livepaper-observability-shift-handoff-watchdog-ci-gate-proof" in workflow
    assert (
        "cat artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md"
        in workflow
    )
    assert "not livepaper_observability_shift_handoff_watchdog_ci_gate" in workflow
    assert (
        handoff_ci_check_index
        < handoff_watchdog_index
        < handoff_watchdog_runtime_index
        < handoff_watchdog_regression_pack_index
        < handoff_watchdog_ci_gate_index
        < build_bundle_index
        < remaining_tests_index
    )


def test_livepaper_observability_shift_handoff_watchdog_ci_gate_manifest_and_context() -> None:
    proof = load_proof()
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    ledger = load_last_ledger_entry()
    summary_text = SUMMARY_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    bundle_script = (REPO_ROOT / "scripts" / "build_proof_bundle.sh").read_text()
    handoff_text = (REPO_ROOT / HANDOFF_CI_GATE_PATH).read_text()

    current_task_id = manifest["task_id"]

    assert (
        manifest["task_id"]
        == context["current_task"]["id"]
        == ledger["task_id"]
    )
    assert manifest["status"] == ledger["status"]
    assert (
        manifest["bundle_path"]
        == ledger["artifact_bundle"]
    )
    assert (
        context["current_contract"]["livepaper_observability_shift_handoff_watchdog_ci_gate_marker"]
        == "livepaper_observability_shift_handoff_watchdog_ci_gate"
    )
    assert (
        context["evidence"]["livepaper_observability_shift_handoff_watchdog_ci_gate"][
            "gate_test_files"
        ]
        == EXPECTED_GROUPED_TEST_FILES
    )
    if current_task_id == "PATTERN-A-DEMO-EXECUTOR-CUTOVER":
        assert context["current_task"]["id"] == "PATTERN-A-DEMO-EXECUTOR-CUTOVER"
        assert ledger["task_id"] == "PATTERN-A-DEMO-EXECUTOR-CUTOVER"
        assert manifest["status"] == "pattern_a_demo_executor_cutover_ready"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/pattern-a-demo-executor-cutover.tar.gz"
        )
        assert (
            "transport_livepaper_observability_acceptance_pack" in summary_text
            or "transport_livepaper_observability_acceptance_pack" in report_text
        )
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
        assert "pattern-a-demo-executor-cutover.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-ACCEPTANCE-PACK":
        assert context["current_task"]["id"] == "DEMO-FORWARD-ACCEPTANCE-PACK"
        assert ledger["task_id"] == "DEMO-FORWARD-ACCEPTANCE-PACK"
        assert manifest["status"] == "demo_forward_acceptance_pack_ready"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-acceptance-pack.tar.gz"
        )
        assert (
            "transport_livepaper_observability_acceptance_pack" in summary_text
            or "transport_livepaper_observability_acceptance_pack" in report_text
        )
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
        assert "demo-forward-acceptance-pack.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN":
        assert context["current_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN"
        assert ledger["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN"
        assert manifest["status"] == "demo_forward_supervised_run_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run.tar.gz"
        )
        assert (
            "transport_livepaper_observability_acceptance_pack" in summary_text
            or "transport_livepaper_observability_acceptance_pack" in report_text
        )
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
        assert "demo-forward-supervised-run.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS":
        assert context["current_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS"
        assert ledger["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS"
        assert manifest["status"] == "supervised_run_retry_readiness_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-readiness.tar.gz"
        )
        assert (
            "transport_livepaper_observability_acceptance_pack" in summary_text
            or "transport_livepaper_observability_acceptance_pack" in report_text
        )
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
        assert "demo-forward-supervised-run-retry-readiness.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE":
        assert context["current_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
        assert ledger["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
        assert manifest["status"] == "supervised_run_retry_gate_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz"
        )
        assert (
            "transport_livepaper_observability_acceptance_pack" in summary_text
            or "transport_livepaper_observability_acceptance_pack" in report_text
        )
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
        assert "demo-forward-supervised-run-retry-gate.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION":
        assert (
            context["current_task"]["id"]
            == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION"
        )
        assert (
            ledger["task_id"]
            == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION"
        )
        assert manifest["status"] == "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration.tar.gz"
        )
        assert (
            "transport_livepaper_observability_acceptance_pack" in summary_text
            or "transport_livepaper_observability_acceptance_pack" in report_text
        )
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
        assert "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH":
        assert context["current_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH"
        assert ledger["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH"
        assert manifest["status"] == "supervised_run_retry_gate_attestation_refresh_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-refresh.tar.gz"
        )
        assert (
            "transport_livepaper_observability_acceptance_pack" in summary_text
            or "transport_livepaper_observability_acceptance_pack" in report_text
        )
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
        assert "demo-forward-supervised-run-retry-gate-attestation-refresh.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK":
        assert context["current_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK"
        assert ledger["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK"
        assert manifest["status"] == "supervised_run_retry_gate_attestation_record_pack_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack.tar.gz"
        )
        assert (
            "transport_livepaper_observability_acceptance_pack" in summary_text
            or "transport_livepaper_observability_acceptance_pack" in report_text
        )
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
        assert "demo-forward-supervised-run-retry-gate-attestation-record-pack.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT":
        assert context["current_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT"
        assert ledger["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT"
        assert manifest["status"] == "supervised_run_retry_gate_attestation_audit_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz"
        )
        assert (
            "transport_livepaper_observability_acceptance_pack" in summary_text
            or "transport_livepaper_observability_acceptance_pack" in report_text
        )
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
        assert "demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz" in bundle_script
    else:
        assert manifest["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE"
        assert context["current_task"]["id"] in {
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
        }
        assert ledger["task_id"] in {
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
        }
        assert manifest["status"] in {
            "livepaper_observability_shift_handoff_watchdog_ci_gate_passed",
            "livepaper_observability_shift_handoff_watchdog_ci_gate_failed",
        }
        if manifest["status"] == "livepaper_observability_shift_handoff_watchdog_ci_gate_passed":
            assert (
                context["evidence"]["livepaper_observability_shift_handoff_watchdog_ci_gate"][
                    "preferred_next_step"
                ]
                == "transport_livepaper_observability_acceptance_pack"
            )
            assert (
                prompt_context["recommended_next_task"]
                == "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-ACCEPTANCE-PACK"
            )
            assert "transport_livepaper_observability_acceptance_pack" in summary_text
            assert "transport_livepaper_observability_acceptance_pack" in report_text
        else:
            assert (
                context["evidence"]["livepaper_observability_shift_handoff_watchdog_ci_gate"][
                    "preferred_next_step"
                ]
                == "transport_livepaper_observability_acceptance_pack"
            )
            assert (
                prompt_context["recommended_next_task"]
                == "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-ACCEPTANCE-PACK"
            )
            assert "transport_livepaper_observability_acceptance_pack" in report_text
        assert "task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz" in bundle_script
    assert "scripts/run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh" in manifest["scripts"]
    assert (
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-report.md"
        in manifest["reports"]
    )
    assert (
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json"
        in manifest["proof_files"]
    )
    if current_task_id == "PATTERN-A-DEMO-EXECUTOR-CUTOVER":
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
    elif current_task_id == "DEMO-FORWARD-ACCEPTANCE-PACK":
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN":
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS":
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE":
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION":
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH":
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK":
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT":
        assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in status_text
    else:
        assert manifest["status"] in status_text
    assert (
        "- terminal_snapshot_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
        in handoff_text
    )
    assert (
        "- failure_detail_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
        in handoff_text
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_ci_gate"][
            "current_handoff_watchdog_snapshot"
        ]["checked_handoff"]
        == "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/HANDOFF.md"
    )


def test_livepaper_observability_shift_handoff_watchdog_ci_gate_script_targets_current_suite() -> None:
    gate_script = (
        REPO_ROOT / "scripts" / "run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh"
    ).read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    for file_name in EXPECTED_GROUPED_TEST_FILES:
        assert file_name in gate_script
    assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in gate_script
    assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in pytest_ini
