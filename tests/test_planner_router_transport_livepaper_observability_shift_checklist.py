import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "livepaper_observability_shift_checklist.md"
PROOF_PATH = (
    REPO_ROOT / "artifacts" / "proofs" / "task-007-livepaper-observability-shift-checklist-check.json"
)
REPORT_PATH = (
    REPO_ROOT / "artifacts" / "reports" / "task-007-livepaper-observability-shift-checklist-report.md"
)
STATUS_PATH = (
    REPO_ROOT / "artifacts" / "reports" / "task-007-livepaper-observability-shift-checklist-status.md"
)
SUMMARY_PATH = (
    REPO_ROOT / "artifacts" / "proofs" / "task-007-livepaper-observability-shift-checklist-summary.md"
)
PROMPT_CONTEXT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-checklist"
    / "CONTEXT.json"
)


def load_proof() -> dict[str, object]:
    return json.loads(PROOF_PATH.read_text())


def load_last_ledger_entry() -> dict[str, object]:
    lines = (REPO_ROOT / "artifacts" / "task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


def test_livepaper_observability_shift_checklist_proof_tracks_latest_git_state() -> None:
    proof = load_proof()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-CHECKLIST"
    assert proof["verified_github"]["latest_vexter_pr"] == 60
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "ec46f051b41c3e140db09e808ef54e4d6e3d33ac"
    )
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
    assert proof["livepaper_observability_shift_checklist"]["source_faithful_modes"] == {
        "dexter": "paper_live",
        "mewx": "sim_live",
    }
    assert proof["task_result"]["task_state"] == "livepaper_observability_shift_checklist_ready"
    assert (
        proof["task_result"]["recommended_next_step"]
        == "livepaper_observability_shift_handoff_template"
    )
    assert (
        proof["task_result"]["recommended_next_task_id"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-TEMPLATE"
    )


def test_livepaper_observability_shift_checklist_artifacts_remain_wired_after_handoff_template_lane() -> None:
    proof = load_proof()
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    summary_text = SUMMARY_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    report_text = REPORT_PATH.read_text()

    assert "artifacts/reports/task-007-livepaper-observability-shift-checklist-report.md" in manifest["reports"]
    assert "artifacts/proofs/task-007-livepaper-observability-shift-checklist-check.json" in manifest[
        "proof_files"
    ]
    assert (
        context["evidence"]["livepaper_observability_shift_checklist"]["key_finding"]
        == proof["task_result"]["key_finding"]
        == "livepaper_observability_shift_checklist_fixed"
    )
    assert (
        context["evidence"]["livepaper_observability_shift_checklist"]["claim_boundary"]
        == proof["task_result"]["claim_boundary"]
        == "livepaper_observability_shift_checklist_bounded"
    )
    assert (
        context["evidence"]["livepaper_observability_shift_checklist"]["preferred_next_step"]
        == "livepaper_observability_shift_handoff_template"
    )
    assert (
        context["evidence"]["livepaper_observability_shift_checklist"]["task_state"]
        == proof["task_result"]["task_state"]
        == "livepaper_observability_shift_checklist_ready"
    )
    assert (
        prompt_context["recommended_next_task"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-TEMPLATE"
    )
    assert "livepaper_observability_shift_handoff_template" in summary_text
    assert "livepaper_observability_shift_checklist_ready" in status_text
    assert "livepaper_observability_shift_handoff_template" in report_text


def test_livepaper_observability_shift_checklist_doc_and_report_capture_timed_flow() -> None:
    proof = load_proof()
    doc_text = DOC_PATH.read_text()
    report_text = REPORT_PATH.read_text()

    for needle in (
        "Pre-Shift Checklist",
        "During-Shift Periodic Checks",
        "End-of-Shift Checklist",
        "manual_latched_stop_all",
        "omission",
        "drift",
        "partial_visibility",
        "halt",
        "quarantine",
        "continue",
    ):
        assert needle in doc_text
        assert needle in report_text or needle in {"Pre-Shift Checklist", "During-Shift Periodic Checks", "End-of-Shift Checklist"}

    assert proof["livepaper_observability_shift_checklist"]["artifact_entry_order"] == [
        "artifacts/reports/task-007-livepaper-observability-shift-checklist-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-checklist-report.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-checklist-summary.md",
        "specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-checklist-check.json",
    ]
    assert proof["livepaper_observability_shift_checklist"]["first_deep_proof"] == (
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json"
    )
    assert proof["livepaper_observability_shift_checklist"]["decision_mapping"]["halt"][0] == (
        "containment surfaces fail"
    )
    assert "artifacts/bundles/task-007-livepaper-observability-shift-checklist.tar.gz" in proof[
        "livepaper_observability_shift_checklist"
    ]["proof_outputs"]
