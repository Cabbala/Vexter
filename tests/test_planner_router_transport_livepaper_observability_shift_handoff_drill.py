import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "livepaper_observability_shift_handoff_drill.md"
PROOF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-drill-check.json"
)
REPORT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-drill-report.md"
)
STATUS_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-drill-status.md"
)
SUMMARY_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-drill-summary.md"
)
PROMPT_CONTEXT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-drill"
    / "CONTEXT.json"
)
HANDOFF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-drill"
    / "HANDOFF.md"
)


def load_proof() -> dict[str, object]:
    return json.loads(PROOF_PATH.read_text())


def load_last_ledger_entry() -> dict[str, object]:
    lines = (REPO_ROOT / "artifacts" / "task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


def test_livepaper_observability_shift_handoff_drill_proof_tracks_latest_git_state() -> None:
    proof = load_proof()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-DRILL"
    assert proof["verified_github"]["latest_vexter_pr"] == 63
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "9c00b7917f80bfbc4c7a0334625dddc09d903aca"
    )
    assert proof["verified_github"]["checklist_lane_pr"] == 61
    assert proof["verified_github"]["dexter_pr"] == 3
    assert (
        proof["verified_github"]["dexter_main_commit"]
        == "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
    )
    assert (
        proof["verified_github"]["mewx_frozen_commit"]
        == "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
    )
    assert proof["fixed_input_surface"]["promoted_label"] == "task005-pass-grade-pair-20260325T180027Z"
    assert proof["implementation"]["source_logic_changed"] is False
    assert proof["implementation"]["validator_rules_changed"] is False
    assert proof["implementation"]["new_evidence_collection_required"] is False
    assert proof["livepaper_observability_shift_handoff_drill"]["source_faithful_modes"] == {
        "dexter": "paper_live",
        "mewx": "sim_live",
    }
    assert proof["task_result"]["task_state"] == "livepaper_observability_shift_handoff_drill_passed"
    assert (
        proof["task_result"]["recommended_next_step"]
        == "livepaper_observability_shift_handoff_ci_check"
    )
    assert (
        proof["task_result"]["recommended_next_task_id"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK"
    )


def test_livepaper_observability_shift_handoff_drill_artifacts_are_wired_for_incoming_readers() -> None:
    proof = load_proof()
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    ledger = load_last_ledger_entry()
    summary_text = SUMMARY_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    bundle_script = (REPO_ROOT / "scripts" / "build_proof_bundle.sh").read_text()

    assert prompt_context["visible_main_state"]["latest_vexter_pr"] == 63
    assert (
        prompt_context["visible_main_state"]["latest_vexter_main_commit"]
        == "9c00b7917f80bfbc4c7a0334625dddc09d903aca"
    )
    assert (
        prompt_context["visible_main_state"]["latest_checklist_lane_pr"]
        == proof["verified_github"]["checklist_lane_pr"]
    )
    assert (
        prompt_context["recommended_next_task"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK"
    )
    assert manifest["task_id"] == proof["task_id"] == context["current_task"]["id"] == ledger["task_id"]
    assert (
        manifest["status"]
        == proof["task_result"]["task_state"]
        == ledger["status"]
        == "livepaper_observability_shift_handoff_drill_passed"
    )
    assert (
        manifest["bundle_path"]
        == ledger["artifact_bundle"]
        == "artifacts/bundles/task-007-livepaper-observability-shift-handoff-drill.tar.gz"
    )
    assert (
        manifest["task_result"]["key_finding"]
        == proof["task_result"]["key_finding"]
        == context["evidence"]["livepaper_observability_shift_handoff_drill"]["key_finding"]
        == ledger["key_finding"]
        == "livepaper_observability_shift_handoff_drill_validated"
    )
    assert (
        manifest["task_result"]["claim_boundary"]
        == proof["task_result"]["claim_boundary"]
        == context["evidence"]["livepaper_observability_shift_handoff_drill"]["claim_boundary"]
        == ledger["claim_boundary"]
        == "livepaper_observability_shift_handoff_drill_bounded"
    )
    assert (
        manifest["task_result"]["recommended_next_step"]
        == proof["task_result"]["recommended_next_step"]
        == context["evidence"]["livepaper_observability_shift_handoff_drill"]["preferred_next_step"]
        == prompt_context["current_state"]["recommended_next_step"]
        == "livepaper_observability_shift_handoff_ci_check"
    )
    assert (
        manifest["next_task"]["id"]
        == context["next_task"]["id"]
        == ledger["next_task_id"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK"
    )
    assert (
        manifest["next_task"]["state"]
        == context["next_task"]["state"]
        == ledger["next_task_state"]
        == "ready_for_livepaper_observability_shift_handoff_ci_check"
    )
    assert "livepaper_observability_shift_handoff_ci_check" in summary_text
    assert "livepaper_observability_shift_handoff_drill_passed" in status_text
    assert "livepaper_observability_shift_handoff_ci_check" in report_text
    assert "task-007-livepaper-observability-shift-handoff-drill.tar.gz" in bundle_script


def test_livepaper_observability_shift_handoff_drill_doc_and_sample_handoff_capture_required_faces() -> None:
    proof = load_proof()
    doc_text = DOC_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    handoff_text = HANDOFF_PATH.read_text()

    for needle in (
        "current status",
        "proof and report pointers",
        "omission",
        "drift",
        "partial_visibility",
        "manual stop-all",
        "quarantine",
        "terminal snapshot",
        "normalized failure detail",
        "open questions",
        "next-shift priority checks",
        "bounded completeness criteria",
        "false",
        "none",
    ):
        assert needle in doc_text.lower() or needle in report_text.lower() or needle in handoff_text.lower()

    assert proof["livepaper_observability_shift_handoff_drill"]["artifact_entry_order"] == [
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill-report.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-drill-summary.md",
        "docs/livepaper_observability_shift_handoff_drill.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-drill-check.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/HANDOFF.md",
    ]
    assert proof["livepaper_observability_shift_handoff_drill"]["first_deep_proof"] == (
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json"
    )
    assert (
        proof["livepaper_observability_shift_handoff_drill"]["required_handoff_faces"][0]
        == "current_status"
    )
    assert (
        proof["livepaper_observability_shift_handoff_drill"]["completeness_criteria"][0]
        == "Every required handoff face is filled or explicitly marked none."
    )
    assert proof["livepaper_observability_shift_handoff_drill"]["sample_handoff"] == {
        "task_state": "livepaper_observability_shift_handoff_drill_passed",
        "shift_outcome": "contained",
        "current_action": "continue",
        "active_broken_surface_or_none": "none",
        "omission_present": False,
        "drift_present": False,
        "partial_visibility_present": False,
        "manual_stop_all_visible": True,
        "quarantine_active": True,
        "terminal_snapshot_present": True,
        "normalized_failure_detail_present": True,
        "containment_anchor_plan_id": "req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
        "failure_anchor_plan_id": "req-transport-livepaper-observability-regression-pack-timeout:batch:1:mewx_containment",
        "halt_mode": "manual_latched_stop_all",
        "trigger_plan_id": "req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
        "stop_reason": "manual_latched_stop_all",
        "quarantine_reason": "timeout_guard",
        "terminal_signal": "snapshot",
        "normalized_failure_code": "status_timeout",
        "normalized_failure_stage": "status",
        "normalized_failure_source_reason": "status timeout",
        "rollback_snapshot_present": True,
        "open_questions": ["none"],
        "next_shift_priority_checks": [
            "confirm the current report, proof summary, and proof JSON before changing any task state",
            "if any face is blank, record `none` explicitly and stop the handoff",
            "start the next bounded check at the watchdog CI gate if a visibility break appears",
        ],
        "every_required_face_filled_or_none": True,
    }
    assert "current_action: continue" in handoff_text
    assert "omission_present: false" in handoff_text
    assert "drift_present: false" in handoff_text
    assert "partial_visibility_present: false" in handoff_text
    assert "manual_stop_all_visible: true" in handoff_text
    assert "quarantine_active: true" in handoff_text
    assert "quarantine_reason_or_none: timeout_guard" in handoff_text
    assert "halt_mode_or_none: manual_latched_stop_all" in handoff_text
    assert "terminal_snapshot_present: true" in handoff_text
    assert "snapshot_signal_visible: true" in handoff_text
    assert "normalized_failure_detail_present: true" in handoff_text
    assert "failure_code: status_timeout" in handoff_text
    assert "rollback_snapshot_required_and_present_or_none: present" in handoff_text
    assert "question_1_or_none: none" in handoff_text
    assert "priority_check_1:" in handoff_text
