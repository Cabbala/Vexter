import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = (
    REPO_ROOT / "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json"
)
REPORT_PATH = (
    REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md"
)
SUMMARY_PATH = (
    REPO_ROOT / "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-summary.md"
)
SCRIPT_PATH = REPO_ROOT / "scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py"
MANIFEST_PATH = (
    REPO_ROOT / "manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json"
)


def test_demo_forward_supervised_run_retry_gate_evidence_preflight_surfaces_are_current_and_fail_closed() -> None:
    proof = json.loads(PROOF_PATH.read_text())
    manifest = json.loads(MANIFEST_PATH.read_text())
    report_text = REPORT_PATH.read_text()
    summary_text = SUMMARY_PATH.read_text()

    assert manifest["manifest_role"] == "template"
    assert proof["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-EVIDENCE-PREFLIGHT"
    assert proof["manifest"]["path"] == (
        "manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json"
    )
    assert proof["manifest"]["preflight_proof"] == (
        "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json"
    )
    assert proof["manifest"]["preflight_report"] == (
        "artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md"
    )
    assert proof["manifest"]["preflight_summary"] == (
        "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-summary.md"
    )

    readiness = proof["reopen_readiness"]
    assert readiness["status"] == "blocked"
    assert readiness["decision"] == "retry_gate_review_reopen_blocked"
    assert readiness["manifest_status"] == "template_only"
    assert readiness["retry_gate_review_reopen_ready"] is False
    assert readiness["blocked_face_count"] == 9
    assert "operator_owner_face" in readiness["blocked_faces"]
    assert "terminal_snapshot_readability_reconfirmed" in readiness["blocked_faces"]
    assert readiness["blocked_reason_counts"]["template_only_manifest"] == 9
    assert readiness["blocked_reason_group_counts"]["state"] == 9
    assert "python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py" in (
        readiness["canonical_command"]
    )
    assert "Manifest remains template_only" in readiness["template_only_false_path"]
    assert readiness["consistency_checks"]["blocked_reason_counts_match_face_rows"] is True
    assert readiness["next_human_pass"]["bounded_window_fields_once"] == [
        "bounded_supervised_window.label",
        "bounded_supervised_window.starts_at",
        "bounded_supervised_window.ends_at",
    ]
    assert readiness["next_human_pass"]["faces"][0]["face"] == "external_credential_source_face"

    first_face = proof["faces"][0]
    assert first_face["reopen_ready_now"] is False
    assert first_face["reopen_status"] == "FAIL/BLOCKED"
    assert "template_only_manifest" in first_face["reopen_blockers"]["state"]
    assert "outside_repo_locator_not_supplied" in first_face["reopen_blockers"]["missing"]

    assert "## Unified Reopen-Readiness" in report_text
    assert "Aggregated blocked reasons" in report_text
    assert "Face-To-Manifest And Proof Map" in report_text
    assert "## Consistency Checks" in report_text
    assert "## Next Human Pass Checklist" in report_text
    assert "Preflight status: `blocked`" in summary_text
    assert "Canonical preflight command" in summary_text


def test_demo_forward_supervised_run_retry_gate_evidence_preflight_script_reports_blocked_status() -> None:
    completed = subprocess.run(
        ["python3.12", str(SCRIPT_PATH)],
        check=True,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["preflight_status"] == "blocked"
    assert payload["manifest_status"] == "template_only"
    assert len(payload["blocked_faces"]) == 9
    assert payload["blocked_reason_counts"]["template_only_manifest"] == 9
    assert payload["retry_gate_review_reopen_ready"] is False
    assert (
        payload["canonical_command"]
        == "python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py"
    )
    assert "Manifest remains template_only" in payload["template_only_false_path"]
    assert payload["consistency_checks"]["template_only_false_path_holds"] is True
    assert payload["next_human_pass"]["faces"][0]["face"] == "external_credential_source_face"
