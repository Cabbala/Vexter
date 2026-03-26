import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "livepaper_observability_operator_runbook.md"
PROOF_PATH = (
    REPO_ROOT / "artifacts" / "proofs" / "task-007-livepaper-observability-operator-runbook-check.json"
)
REPORT_PATH = (
    REPO_ROOT / "artifacts" / "reports" / "task-007-livepaper-observability-operator-runbook-report.md"
)
STATUS_PATH = (
    REPO_ROOT / "artifacts" / "reports" / "task-007-livepaper-observability-operator-runbook-status.md"
)
SUMMARY_PATH = (
    REPO_ROOT / "artifacts" / "proofs" / "task-007-livepaper-observability-operator-runbook-summary.md"
)
PROMPT_CONTEXT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-operator-runbook"
    / "CONTEXT.json"
)


def load_proof() -> dict[str, object]:
    return json.loads(PROOF_PATH.read_text())


def load_last_ledger_entry() -> dict[str, object]:
    lines = (REPO_ROOT / "artifacts" / "task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


def test_livepaper_observability_operator_runbook_proof_tracks_latest_git_state() -> None:
    proof = load_proof()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-OPERATOR-RUNBOOK"
    assert proof["verified_github"]["latest_vexter_pr"] == 59
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "4be21e4e52fbe686e585dea6b573efea759e0933"
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
    assert proof["livepaper_observability_operator_runbook"]["source_faithful_modes"] == {
        "dexter": "paper_live",
        "mewx": "sim_live",
    }
    assert proof["task_result"]["task_state"] == "livepaper_observability_operator_runbook_ready"
    assert (
        proof["task_result"]["recommended_next_step"]
        == "livepaper_observability_shift_checklist"
    )
    assert (
        proof["task_result"]["recommended_next_task_id"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-CHECKLIST"
    )


def test_livepaper_observability_operator_runbook_current_artifacts_are_consistent() -> None:
    proof = load_proof()
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    ledger = load_last_ledger_entry()
    summary_text = SUMMARY_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    report_text = REPORT_PATH.read_text()

    assert manifest["task_id"] == proof["task_id"] == context["current_task"]["id"] == ledger["task_id"]
    assert (
        manifest["status"]
        == proof["task_result"]["task_state"]
        == ledger["status"]
        == "livepaper_observability_operator_runbook_ready"
    )
    assert (
        manifest["bundle_path"]
        == ledger["artifact_bundle"]
        == "artifacts/bundles/task-007-livepaper-observability-operator-runbook.tar.gz"
    )
    assert (
        manifest["task_result"]["key_finding"]
        == proof["task_result"]["key_finding"]
        == context["evidence"]["livepaper_observability_operator_runbook"]["key_finding"]
        == ledger["key_finding"]
        == "livepaper_observability_operator_runbook_fixed"
    )
    assert (
        manifest["task_result"]["claim_boundary"]
        == proof["task_result"]["claim_boundary"]
        == context["evidence"]["livepaper_observability_operator_runbook"]["claim_boundary"]
        == ledger["claim_boundary"]
        == "livepaper_observability_operator_runbook_bounded"
    )
    assert (
        manifest["task_result"]["recommended_next_step"]
        == proof["task_result"]["recommended_next_step"]
        == context["evidence"]["livepaper_observability_operator_runbook"]["preferred_next_step"]
        == prompt_context["current_state"]["recommended_next_step"]
        == "livepaper_observability_shift_checklist"
    )
    assert manifest["next_task"]["id"] == context["next_task"]["id"] == ledger["next_task_id"] == (
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-CHECKLIST"
    )
    assert (
        manifest["next_task"]["state"]
        == context["next_task"]["state"]
        == ledger["next_task_state"]
        == "ready_for_livepaper_observability_shift_checklist"
    )
    assert prompt_context["recommended_next_task"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-CHECKLIST"
    assert "livepaper_observability_shift_checklist" in summary_text
    assert "livepaper_observability_operator_runbook_ready" in status_text
    assert "livepaper_observability_shift_checklist" in report_text


def test_livepaper_observability_operator_runbook_doc_and_report_capture_lookup_and_triage() -> None:
    proof = load_proof()
    doc_text = DOC_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    bundle_script = (REPO_ROOT / "scripts" / "build_proof_bundle.sh").read_text()

    for needle in (
        "manual_latched_stop_all",
        "quarantine_reason_completeness",
        "snapshot_backed_terminal_detail",
        "normalized_failure_detail_passthrough",
        "omission",
        "drift",
        "partial_visibility",
    ):
        assert needle in doc_text
        assert needle in report_text

    assert proof["livepaper_observability_operator_runbook"]["first_check_order"] == [
        "artifacts/reports/task-007-livepaper-observability-operator-runbook-status.md",
        "artifacts/reports/task-007-livepaper-observability-operator-runbook-report.md",
        "artifacts/proofs/task-007-livepaper-observability-operator-runbook-summary.md",
        "specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md",
        "artifacts/proofs/task-007-livepaper-observability-operator-runbook-check.json",
    ]
    assert proof["livepaper_observability_operator_runbook"]["first_deep_proof"] == (
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json"
    )
    assert (
        proof["livepaper_observability_operator_runbook"]["failure_surface_priority"][0]["surface"]
        == "manual_stop_all_propagation"
    )
    assert (
        proof["livepaper_observability_operator_runbook"]["operator_meanings"]["drift"]
        == "A required field is present but no longer matches the planned source-faithful envelope."
    )
    assert (
        "task-007-livepaper-observability-operator-runbook.tar.gz" in bundle_script
    )
