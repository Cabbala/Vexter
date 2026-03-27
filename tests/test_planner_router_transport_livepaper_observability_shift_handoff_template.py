import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "livepaper_observability_shift_handoff_template.md"
PROOF_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-template-check.json"
)
REPORT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-template-report.md"
)
STATUS_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-template-status.md"
)
SUMMARY_PATH = (
    REPO_ROOT
    / "artifacts"
    / "proofs"
    / "task-007-livepaper-observability-shift-handoff-template-summary.md"
)
PROMPT_CONTEXT_PATH = (
    REPO_ROOT
    / "artifacts"
    / "reports"
    / "task-007-livepaper-observability-shift-handoff-template"
    / "CONTEXT.json"
)

pytestmark = pytest.mark.livepaper_observability_shift_handoff_ci_check


def load_proof() -> dict[str, object]:
    return json.loads(PROOF_PATH.read_text())


def load_last_ledger_entry() -> dict[str, object]:
    lines = (REPO_ROOT / "artifacts" / "task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


def test_livepaper_observability_shift_handoff_template_proof_tracks_latest_git_state() -> None:
    proof = load_proof()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-TEMPLATE"
    assert proof["verified_github"]["latest_vexter_pr"] == 62
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "3b595faacf316aca89655b6e1ffcf7568478763e"
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
    assert proof["livepaper_observability_shift_handoff_template"]["source_faithful_modes"] == {
        "dexter": "paper_live",
        "mewx": "sim_live",
    }
    assert proof["task_result"]["task_state"] == "livepaper_observability_shift_handoff_template_ready"
    assert (
        proof["task_result"]["recommended_next_step"]
        == "livepaper_observability_shift_handoff_drill"
    )
    assert (
        proof["task_result"]["recommended_next_task_id"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-DRILL"
    )


def test_livepaper_observability_shift_handoff_template_current_artifacts_are_consistent() -> None:
    proof = load_proof()
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    ledger = load_last_ledger_entry()
    summary_text = SUMMARY_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    report_text = REPORT_PATH.read_text()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-TEMPLATE"
    current_task_id = manifest["task_id"]

    assert manifest["task_id"] == context["current_task"]["id"] == ledger["task_id"]
    assert manifest["status"] == ledger["status"]
    assert proof["task_result"]["task_state"] == "livepaper_observability_shift_handoff_template_ready"
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
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE":
        assert manifest["status"] == "supervised_run_retry_gate_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz"
        )
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION":
        assert manifest["status"] == "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration.tar.gz"
        )
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH":
        assert manifest["status"] == "supervised_run_retry_gate_attestation_refresh_blocked"
        assert (
            manifest["bundle_path"]
            == "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-refresh.tar.gz"
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
    assert (
        proof["task_result"]["key_finding"]
        == context["evidence"]["livepaper_observability_shift_handoff_template"]["key_finding"]
        == "livepaper_observability_shift_handoff_template_fixed"
    )
    assert (
        proof["task_result"]["claim_boundary"]
        == context["evidence"]["livepaper_observability_shift_handoff_template"]["claim_boundary"]
        == "livepaper_observability_shift_handoff_template_bounded"
    )
    assert (
        proof["task_result"]["recommended_next_step"]
        == context["evidence"]["livepaper_observability_shift_handoff_template"]["preferred_next_step"]
        == prompt_context["current_state"]["recommended_next_step"]
        == "livepaper_observability_shift_handoff_drill"
    )
    assert manifest["next_task"]["id"] == context["next_task"]["id"] == ledger["next_task_id"]
    assert manifest["next_task"]["state"] == context["next_task"]["state"] == ledger["next_task_state"]
    assert (
        prompt_context["recommended_next_task"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-DRILL"
    )
    assert "livepaper_observability_shift_handoff_drill" in summary_text
    assert "livepaper_observability_shift_handoff_template_ready" in status_text
    assert "livepaper_observability_shift_handoff_drill" in report_text
    if current_task_id == "PATTERN-A-DEMO-EXECUTOR-CUTOVER":
        assert manifest["next_task"]["id"] == "DEMO-EXECUTOR-ADAPTER-IMPLEMENTATION"
        assert (
            manifest["next_task"]["state"]
            == "ready_for_demo_executor_adapter_implementation"
        )
    elif current_task_id == "DEMO-FORWARD-ACCEPTANCE-PACK":
        assert manifest["next_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN"
        assert manifest["next_task"]["state"] == "ready_for_demo_forward_supervised_run"
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN":
        assert manifest["next_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS"
        assert manifest["next_task"]["state"] == "ready_for_supervised_run_retry_readiness"
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS":
        assert manifest["next_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
        assert manifest["next_task"]["state"] == "ready_for_supervised_run_retry_gate"
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE":
        assert manifest["next_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
        assert manifest["next_task"]["state"] == "retry_gate_inputs_pending"
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION":
        assert (
            manifest["next_task"]["id"]
            == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH"
        )
        assert (
            manifest["next_task"]["state"]
            == "additional_attestation_refresh_required_for_record_pack_regeneration"
        )
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH":
        assert (
            manifest["next_task"]["id"]
            == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK"
        )
        assert manifest["next_task"]["state"] == "ready_for_attestation_record_pack_regeneration"
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK":
        assert (
            manifest["next_task"]["id"]
            == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH"
        )
        assert manifest["next_task"]["state"] == "current_attestation_records_refresh_required"
    elif current_task_id == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT":
        assert (
            manifest["next_task"]["id"]
            == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT"
        )
        assert manifest["next_task"]["state"] == "retry_gate_attestation_audits_pending"
    else:
        assert manifest["next_task"]["id"] in {
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
            "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
            "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-ACCEPTANCE-PACK",
        }
        assert manifest["next_task"]["state"] in {
            "ready_for_livepaper_observability_shift_handoff_watchdog_runtime",
            "ready_for_livepaper_observability_shift_handoff_watchdog_regression_pack",
            "ready_for_livepaper_observability_shift_handoff_watchdog_ci_gate",
            "ready_for_transport_livepaper_observability_acceptance_pack",
        }


def test_livepaper_observability_shift_handoff_template_doc_and_report_capture_required_faces() -> None:
    proof = load_proof()
    doc_text = DOC_PATH.read_text()
    report_text = REPORT_PATH.read_text()

    for needle in (
        "Current status",
        "Proof and report pointers",
        "omission",
        "drift",
        "partial_visibility",
        "manual_latched_stop_all",
        "poll_first",
        "Terminal snapshot state",
        "Normalized failure detail state",
        "Open questions",
        "Next-shift priority checks",
        "Bounded completeness criteria",
    ):
        assert needle in doc_text
        assert needle in report_text or needle in {
            "Current status",
            "Proof and report pointers",
            "Terminal snapshot state",
            "Normalized failure detail state",
            "Open questions",
            "Next-shift priority checks",
            "Bounded completeness criteria",
        }

    assert proof["livepaper_observability_shift_handoff_template"]["artifact_entry_order"] == [
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-template-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-template-report.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-template-summary.md",
        "docs/livepaper_observability_shift_handoff_template.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-template-check.json",
    ]
    assert proof["livepaper_observability_shift_handoff_template"]["first_deep_proof"] == (
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json"
    )
    assert (
        proof["livepaper_observability_shift_handoff_template"]["required_handoff_faces"][0]
        == "current_status"
    )
    assert (
        proof["livepaper_observability_shift_handoff_template"]["completeness_criteria"][0]
        == "Every required handoff face is filled or explicitly marked none."
    )
    assert (REPO_ROOT / "artifacts" / "bundles" / "task-007-livepaper-observability-shift-handoff-template.tar.gz").exists()
