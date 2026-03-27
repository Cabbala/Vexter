import json
from pathlib import Path

import pytest

from vexter.planner_router.handoff_watchdog import (
    DEFAULT_CURRENT_POINTER_PATHS,
    DEFAULT_CURRENT_TASK_STATE,
    DEFAULT_FAILURE_DETAIL_POINTER,
    DEFAULT_FIRST_DEEP_PROOF_PATH,
    DEFAULT_RECOMMENDED_NEXT_STEP,
    DEFAULT_TERMINAL_SNAPSHOT_POINTER,
    LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES,
    RUNTIME_CURRENT_POINTER_PATHS,
    RUNTIME_CURRENT_TASK_STATE,
    RUNTIME_FAILURE_DETAIL_POINTER,
    RUNTIME_FIRST_DEEP_PROOF_PATH,
    RUNTIME_RECOMMENDED_NEXT_STEP,
    RUNTIME_TERMINAL_SNAPSHOT_POINTER,
    evaluate_livepaper_observability_shift_handoff_watchdog,
)


pytestmark = [
    pytest.mark.livepaper_observability_shift_handoff_watchdog_regression_pack,
    pytest.mark.livepaper_observability_shift_handoff_watchdog_ci_gate,
]

REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_HANDOFF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-drill"
    / "HANDOFF.md"
)
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
    / "task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json"
)
SUMMARY_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md"
)
REPORT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md"
)
STATUS_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md"
)
PROMPT_CONTEXT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-watchdog-regression-pack"
    / "CONTEXT.json"
)

EXPECTED_TEST_FILES = [
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py",
]
EXPECTED_MONITORED_SURFACES = list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES)
REGRESSION_PACK_CURRENT_POINTER_PATHS = {
    "current_status_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md",
    "current_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md",
    "current_proof_summary": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md",
    "current_proof_json": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
}
REGRESSION_PACK_CURRENT_TASK_STATE = (
    "livepaper_observability_shift_handoff_watchdog_regression_pack_passed"
)
REGRESSION_PACK_RECOMMENDED_NEXT_STEP = (
    "livepaper_observability_shift_handoff_watchdog_ci_gate"
)
REGRESSION_PACK_FIRST_DEEP_PROOF_PATH = (
    "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json"
)
REGRESSION_PACK_TERMINAL_SNAPSHOT_POINTER = RUNTIME_TERMINAL_SNAPSHOT_POINTER
REGRESSION_PACK_FAILURE_DETAIL_POINTER = RUNTIME_FAILURE_DETAIL_POINTER


def _evaluate_baseline_handoff(markdown: str):
    return evaluate_livepaper_observability_shift_handoff_watchdog(
        markdown,
        repo_root=REPO_ROOT,
        expected_first_deep_proof_path=DEFAULT_FIRST_DEEP_PROOF_PATH,
        expected_task_state=DEFAULT_CURRENT_TASK_STATE,
        expected_recommended_next_step=DEFAULT_RECOMMENDED_NEXT_STEP,
        expected_current_pointer_paths=DEFAULT_CURRENT_POINTER_PATHS,
        expected_terminal_snapshot_pointer=DEFAULT_TERMINAL_SNAPSHOT_POINTER,
        expected_failure_detail_pointer=DEFAULT_FAILURE_DETAIL_POINTER,
    )


def _evaluate_runtime_handoff(markdown: str):
    return evaluate_livepaper_observability_shift_handoff_watchdog(
        markdown,
        repo_root=REPO_ROOT,
        expected_first_deep_proof_path=RUNTIME_FIRST_DEEP_PROOF_PATH,
        expected_task_state=RUNTIME_CURRENT_TASK_STATE,
        expected_recommended_next_step=RUNTIME_RECOMMENDED_NEXT_STEP,
        expected_current_pointer_paths=RUNTIME_CURRENT_POINTER_PATHS,
        expected_terminal_snapshot_pointer=RUNTIME_TERMINAL_SNAPSHOT_POINTER,
        expected_failure_detail_pointer=RUNTIME_FAILURE_DETAIL_POINTER,
    )


def _evaluate_regression_pack_handoff(markdown: str):
    return evaluate_livepaper_observability_shift_handoff_watchdog(
        markdown,
        repo_root=REPO_ROOT,
        expected_first_deep_proof_path=REGRESSION_PACK_FIRST_DEEP_PROOF_PATH,
        expected_task_state=REGRESSION_PACK_CURRENT_TASK_STATE,
        expected_recommended_next_step=REGRESSION_PACK_RECOMMENDED_NEXT_STEP,
        expected_current_pointer_paths=REGRESSION_PACK_CURRENT_POINTER_PATHS,
        expected_terminal_snapshot_pointer=REGRESSION_PACK_TERMINAL_SNAPSHOT_POINTER,
        expected_failure_detail_pointer=REGRESSION_PACK_FAILURE_DETAIL_POINTER,
    )


CANONICAL_HANDOFF_CASES = {
    "baseline": (BASELINE_HANDOFF_PATH, _evaluate_baseline_handoff),
    "runtime": (RUNTIME_HANDOFF_PATH, _evaluate_runtime_handoff),
    "regression_pack": (REGRESSION_PACK_HANDOFF_PATH, _evaluate_regression_pack_handoff),
}

SURFACE_MUTATIONS = {
    "current_status": lambda text: text.replace(
        "- status_delivery: poll_first",
        "- status_delivery: push_first",
    ),
    "proof_and_report_pointers": lambda text: text.replace(
        "- current_proof_json: artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
        "- current_proof_json: artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md",
    ).replace(
        "- shortest_proof_trail: status -> report -> summary -> regression-pack proof -> regression-pack handoff -> runtime handoff proof -> baseline handoff proof",
        "- shortest_proof_trail: same as before",
    ),
    "omission_drift_partial_visibility": lambda text: text.replace(
        "- drift_present: false",
        "- drift_present: maybe",
    ),
    "manual_stop_all": lambda text: text.replace(
        "- stop_reason_or_none: manual_latched_stop_all",
        "- stop_reason_or_none: same as before",
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
        "- priority_check_1: confirm the current regression-pack status, report, and proof JSON before changing task state",
        "- priority_check_1: none",
    ),
}
SURFACE_EXPECTED_CLASSIFICATIONS = {
    "current_status": "drift",
    "proof_and_report_pointers": "partial_visibility",
    "omission_drift_partial_visibility": "drift",
    "manual_stop_all": "partial_visibility",
    "quarantine": "partial_visibility",
    "terminal_snapshot": "partial_visibility",
    "normalized_failure_detail": "partial_visibility",
    "open_questions": "partial_visibility",
    "next_shift_priority_checks": "omission",
}
OMISSION_MUTATIONS = {
    "current_status": lambda text: text.replace(
        "- task_state: livepaper_observability_shift_handoff_watchdog_regression_pack_passed\n",
        "",
    ),
    "proof_and_report_pointers": lambda text: text.replace(
        "- current_proof_json: artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json\n",
        "",
    ),
    "omission_drift_partial_visibility": lambda text: text.replace(
        "- exact_broken_surface_or_none: none\n",
        "",
    ),
    "manual_stop_all": lambda text: text.replace(
        "- stop_reason_or_none: manual_latched_stop_all\n",
        "",
    ),
    "quarantine": lambda text: text.replace(
        "- continuity_check: monitor_profile_id=mewx_timeout_guard, quarantine_scope=sleeve, execution_mode=sim_live, ack_history_visible=true, runtime_follow_up_visible=true, regression_pack_visible=true\n",
        "",
    ),
    "terminal_snapshot": lambda text: text.replace(
        "- terminal_snapshot_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py\n",
        "",
    ),
    "normalized_failure_detail": lambda text: text.replace(
        "- failure_detail_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py\n",
        "",
    ),
    "open_questions": lambda text: text.replace(
        "- question_2_or_none: none\n",
        "",
    ),
    "next_shift_priority_checks": lambda text: text.replace(
        "- priority_check_1: confirm the current regression-pack status, report, and proof JSON before changing task state\n",
        "",
    ),
}
EXPECTED_SURFACE_TESTS = {
    surface: [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_regression_pack_flags_face_regression[{surface}]"
    ]
    for surface in SURFACE_MUTATIONS
}
EXPECTED_OMISSION_TESTS = {
    surface: [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_regression_pack_flags_surface_omission[{surface}]"
    ]
    for surface in OMISSION_MUTATIONS
}


def load_regression_pack_proof() -> dict[str, object]:
    return json.loads(PROOF_PATH.read_text())


def load_last_ledger_entry() -> dict[str, object]:
    lines = (REPO_ROOT / "artifacts" / "task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


@pytest.mark.parametrize("case_name", CANONICAL_HANDOFF_CASES, ids=CANONICAL_HANDOFF_CASES.keys())
def test_livepaper_observability_shift_handoff_watchdog_regression_pack_passes_on_canonical_handoffs(
    case_name: str,
) -> None:
    handoff_path, evaluator = CANONICAL_HANDOFF_CASES[case_name]
    report = evaluator(handoff_path.read_text())

    assert report.passed is True
    assert report.findings == ()
    assert report.surface_status == {surface: True for surface in EXPECTED_MONITORED_SURFACES}


@pytest.mark.parametrize("surface_name", SURFACE_MUTATIONS, ids=SURFACE_MUTATIONS.keys())
def test_livepaper_observability_shift_handoff_watchdog_regression_pack_flags_face_regression(
    surface_name: str,
) -> None:
    mutated_handoff = SURFACE_MUTATIONS[surface_name](REGRESSION_PACK_HANDOFF_PATH.read_text())
    report = _evaluate_regression_pack_handoff(mutated_handoff)

    assert report.passed is False
    matching_findings = [finding for finding in report.findings if finding.surface == surface_name]
    assert matching_findings
    assert (
        SURFACE_EXPECTED_CLASSIFICATIONS[surface_name]
        in {finding.classification for finding in matching_findings}
    )
    assert report.surface_status[surface_name] is False


@pytest.mark.parametrize("surface_name", OMISSION_MUTATIONS, ids=OMISSION_MUTATIONS.keys())
def test_livepaper_observability_shift_handoff_watchdog_regression_pack_flags_surface_omission(
    surface_name: str,
) -> None:
    omitted_handoff = OMISSION_MUTATIONS[surface_name](REGRESSION_PACK_HANDOFF_PATH.read_text())
    report = _evaluate_regression_pack_handoff(omitted_handoff)

    assert report.passed is False
    matching_findings = [finding for finding in report.findings if finding.surface == surface_name]
    assert matching_findings
    assert "omission" in {finding.classification for finding in matching_findings}
    assert report.surface_status[surface_name] is False


def test_livepaper_observability_shift_handoff_watchdog_regression_pack_proof_tracks_outputs() -> None:
    proof = load_regression_pack_proof()

    assert (
        proof["task_id"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK"
    )
    assert proof["verified_github"]["latest_vexter_pr"] == 67
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "7ab737a306ceca06193044d384e6b17d371838e2"
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"]["suite_group"]
        == "livepaper_observability_shift_handoff_watchdog_regression_pack"
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"]["grouped_test_files"]
        == EXPECTED_TEST_FILES
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"]["grouped_suite_markers"]
        == ["livepaper_observability_shift_handoff_watchdog_regression_pack"]
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"]["monitored_surfaces"]
        == EXPECTED_MONITORED_SURFACES
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"]["surface_regression_tests"]
        == EXPECTED_SURFACE_TESTS
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"]["surface_omission_tests"]
        == EXPECTED_OMISSION_TESTS
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"]["proof_outputs"]
        == [
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md",
        ]
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"]["proof_artifact_name"]
        == "livepaper-observability-shift-handoff-watchdog-regression-pack-proof"
    )
    assert set(
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"][
            "canonical_handoff_snapshots"
        ]
    ) == {"baseline", "runtime", "regression_pack"}
    assert set(
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"][
            "normalized_failure_detail"
        ]
    ) == {
        "finding_surfaces_or_none",
        "finding_classes_or_none",
        "failed_tests_or_none",
        "non_surface_failures_or_none",
    }
    if proof["task_result"]["task_state"] == "livepaper_observability_shift_handoff_watchdog_regression_pack_passed":
        assert (
            proof["next_task_evaluation"]["livepaper_observability_shift_handoff_watchdog_ci_gate"][
                "recommended"
            ]
            is True
        )
    else:
        assert (
            proof["next_task_evaluation"]["livepaper_observability_shift_handoff_watchdog_ci_gate"][
                "recommended"
            ]
            is False
        )
    assert proof["task_result"]["task_state"] in {
        "livepaper_observability_shift_handoff_watchdog_regression_pack_passed",
        "livepaper_observability_shift_handoff_watchdog_regression_pack_failed",
    }


def test_livepaper_observability_shift_handoff_watchdog_regression_pack_freezes_prior_proofs() -> None:
    proof = load_regression_pack_proof()
    watchdog_proof = json.loads(
        (
            REPO_ROOT
            / "artifacts"
            / "proofs"
            / "task-007-livepaper-observability-shift-handoff-watchdog-check.json"
        ).read_text()
    )
    runtime_proof = json.loads(
        (
            REPO_ROOT
            / "artifacts"
            / "proofs"
            / "task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json"
        ).read_text()
    )

    assert (
        watchdog_proof["livepaper_observability_shift_handoff_watchdog"]["monitored_surfaces"]
        == EXPECTED_MONITORED_SURFACES
    )
    assert (
        runtime_proof["livepaper_observability_shift_handoff_watchdog_runtime"]["monitored_surfaces"]
        == EXPECTED_MONITORED_SURFACES
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"][
            "baseline_watchdog_proof"
        ]
        == "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json"
    )
    assert (
        proof["livepaper_observability_shift_handoff_watchdog_regression_pack"][
            "runtime_watchdog_proof"
        ]
        == "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json"
    )


def test_livepaper_observability_shift_handoff_watchdog_regression_pack_workflow_runs_after_runtime() -> None:
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

    assert "./scripts/run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh" in workflow
    assert "livepaper-observability-shift-handoff-watchdog-regression-pack-proof" in workflow
    assert (
        "cat artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md"
        in workflow
    )
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


def test_livepaper_observability_shift_handoff_watchdog_regression_pack_manifest_and_context() -> None:
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    ledger = load_last_ledger_entry()
    summary_text = SUMMARY_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    bundle_script = (REPO_ROOT / "scripts" / "build_proof_bundle.sh").read_text()
    handoff_text = REGRESSION_PACK_HANDOFF_PATH.read_text()

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
    if current_task_id == "PATTERN-A-DEMO-EXECUTOR-CUTOVER":
        assert context["current_task"]["id"] == "PATTERN-A-DEMO-EXECUTOR-CUTOVER"
        assert ledger["task_id"] == "PATTERN-A-DEMO-EXECUTOR-CUTOVER"
        assert manifest["status"] == "pattern_a_demo_executor_cutover_ready"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/pattern-a-demo-executor-cutover.tar.gz"
        )
    elif current_task_id == "DEMO-FORWARD-ACCEPTANCE-PACK":
        assert context["current_task"]["id"] == "DEMO-FORWARD-ACCEPTANCE-PACK"
        assert ledger["task_id"] == "DEMO-FORWARD-ACCEPTANCE-PACK"
        assert manifest["status"] == "demo_forward_acceptance_pack_ready"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-acceptance-pack.tar.gz"
        )
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN":
        assert context["current_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN"
        assert ledger["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN"
        assert manifest["status"] == "demo_forward_supervised_run_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run.tar.gz"
        )
    else:
        assert manifest["task_id"] in {
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
        }
        assert context["current_task"]["id"] in {
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
        }
        assert ledger["task_id"] in {
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
        }
        assert manifest["status"] in {
            "livepaper_observability_shift_handoff_watchdog_regression_pack_passed",
            "livepaper_observability_shift_handoff_watchdog_regression_pack_failed",
            "livepaper_observability_shift_handoff_watchdog_ci_gate_passed",
            "livepaper_observability_shift_handoff_watchdog_ci_gate_failed",
        }
        assert manifest["bundle_path"] in {
            "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz",
            "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz",
        }
    assert (
        context["current_contract"][
            "livepaper_observability_shift_handoff_watchdog_regression_pack_marker"
        ]
        == "livepaper_observability_shift_handoff_watchdog_regression_pack"
    )
    assert (
        context["evidence"]["livepaper_observability_shift_handoff_watchdog_regression_pack"][
            "grouped_test_files"
        ]
        == EXPECTED_TEST_FILES
    )
    assert (
        context["evidence"]["livepaper_observability_shift_handoff_watchdog_regression_pack"][
            "preferred_next_step"
        ]
        == "livepaper_observability_shift_handoff_watchdog_ci_gate"
    )
    assert (
        prompt_context["recommended_next_task"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE"
    )
    assert "scripts/run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh" in manifest[
        "scripts"
    ]
    assert (
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md"
        in manifest["reports"]
    )
    assert (
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json"
        in manifest["proof_files"]
    )
    assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in summary_text
    assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in report_text
    assert "livepaper_observability_shift_handoff_watchdog_regression_pack" in status_text
    if current_task_id == "PATTERN-A-DEMO-EXECUTOR-CUTOVER":
        assert "pattern-a-demo-executor-cutover.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-ACCEPTANCE-PACK":
        assert "demo-forward-acceptance-pack.tar.gz" in bundle_script
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN":
        assert "demo-forward-supervised-run.tar.gz" in bundle_script
    else:
        assert "task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz" in bundle_script
    assert (
        "- terminal_snapshot_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
        in handoff_text
    )
    assert (
        "- failure_detail_pointer_or_none: tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
        in handoff_text
    )
