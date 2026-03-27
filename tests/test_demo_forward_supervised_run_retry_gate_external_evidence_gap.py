import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = (
    REPO_ROOT / "artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-check.json"
)
REPORT_PATH = (
    REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-gate-external-evidence-gap-report.md"
)
SUMMARY_PATH = (
    REPO_ROOT / "artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-summary.md"
)
SCRIPT_PATH = REPO_ROOT / "scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py"
MANIFEST_PATH = (
    REPO_ROOT / "manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json"
)


def test_demo_forward_supervised_run_retry_gate_external_evidence_gap_surfaces_are_current_and_fail_closed() -> None:
    proof = json.loads(PROOF_PATH.read_text())
    manifest = json.loads(MANIFEST_PATH.read_text())
    report_text = REPORT_PATH.read_text()
    summary_text = SUMMARY_PATH.read_text()

    assert manifest["manifest_role"] == "template"
    assert proof["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-EXTERNAL-EVIDENCE-GAP"
    assert proof["manifest"]["path"] == (
        "manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json"
    )
    assert proof["manifest"]["contract_spec"] == (
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_EXTERNAL_EVIDENCE_CONTRACT.md"
    )
    assert proof["manifest"]["status"] == "template_only"
    assert proof["summary"]["required_face_count"] == 9
    assert proof["summary"]["present_face_count"] == 0
    assert proof["summary"]["current_face_count"] == 0
    assert proof["summary"]["reviewable_face_count"] == 0
    assert proof["summary"]["blocked_face_count"] == 9
    assert len(proof["summary"]["operator_inputs_remaining"]) == 9
    assert proof["summary"]["retry_gate_review_reopen_ready"] is False
    assert "operator_owner_face" in proof["summary"]["blocked_faces"]
    assert "terminal_snapshot_readability_reconfirmed" in proof["summary"]["blocked_faces"]

    first_face = proof["faces"][0]
    assert first_face["declared"] is True
    assert first_face["present"] is False
    assert first_face["current"] is False
    assert first_face["fresh_enough"] is False
    assert first_face["reviewable"] is False
    assert first_face["blocked"] is True
    assert "template_only_manifest" in first_face["blocked_reasons"]
    assert "outside_repo_locator_not_supplied" in first_face["blocked_reasons"]
    assert "Operator input still needed:" in first_face["current_observation"]

    assert "Manifest status: `template_only`" in report_text
    assert "demo_forward_supervised_run_retry_gate_external_evidence_manifest.json" in report_text
    assert "Blocked faces:" in summary_text
    assert "Retry-gate review reopen ready: `no`" in summary_text


def test_demo_forward_supervised_run_retry_gate_external_evidence_gap_script_reports_template_only_status() -> None:
    completed = subprocess.run(
        ["python3.12", str(SCRIPT_PATH)],
        check=True,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["manifest_status"] == "template_only"
    assert len(payload["blocked_faces"]) == 9
    assert "external_credential_source_face" in payload["blocked_faces"]
    assert "terminal_snapshot_readability_reconfirmed" in payload["blocked_faces"]
    assert payload["retry_gate_review_reopen_ready"] is False
