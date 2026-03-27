import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = REPO_ROOT / "artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json"
REPORT_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md"
STATUS_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md"
HANDOFF_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md"
SUBAGENTS_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md"
SPEC_PATH = REPO_ROOT / "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md"
PLAN_PATH = REPO_ROOT / "plans/demo_forward_supervised_run_retry_readiness_plan.md"
CHECKLIST_PATH = REPO_ROOT / "docs/demo_forward_supervised_run_retry_readiness_checklist.md"
MATRIX_PATH = REPO_ROOT / "docs/demo_forward_supervised_run_retry_prerequisite_matrix.md"
PROMPT_CONTEXT_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-readiness/CONTEXT.json"


def test_demo_forward_supervised_run_retry_readiness_artifacts_are_current_and_consistent() -> None:
    proof = json.loads(PROOF_PATH.read_text())
    manifest = json.loads((REPO_ROOT / "artifacts/proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts/context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    report_text = REPORT_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    handoff_text = HANDOFF_PATH.read_text()
    subagents_text = SUBAGENTS_PATH.read_text()

    assert manifest["task_id"] in {
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION",
    }
    assert "artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json" in manifest[
        "proof_files"
    ]
    assert "artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md" in manifest[
        "reports"
    ]
    assert "artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md" in manifest[
        "reports"
    ]

    assert proof["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS"
    assert proof["verified_github"]["latest_vexter_pr"] == 73
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "aea530368fc5b59b87dd08a38c2629392ea8d706"
    )
    assert proof["task_result"]["outcome"] == "FAIL/BLOCKED"
    assert proof["task_result"]["recommended_next_step"] == "supervised_run_retry_gate"
    assert proof["task_result"]["decision"] == "supervised_run_retry_gate_required"

    retry_boundary = context["evidence"]["demo_forward_supervised_run_retry_readiness"][
        "retry_boundary"
    ]
    assert context["evidence"]["demo_forward_supervised_run_retry_readiness"]["task_state"] == (
        "supervised_run_retry_readiness_blocked"
    )
    assert context["evidence"]["demo_forward_supervised_run_retry_readiness"]["preferred_next_step"] == (
        "supervised_run_retry_gate"
    )
    assert context["evidence"]["demo_forward_supervised_run_retry_gate"]["task_state"] == (
        "supervised_run_retry_gate_blocked"
    )
    assert context["evidence"]["demo_forward_supervised_run_retry_gate_input_attestation"][
        "task_state"
    ] == "supervised_run_retry_gate_input_attestation_blocked"
    assert context["evidence"]["demo_forward_supervised_run_retry_gate_attestation_audit"][
        "task_state"
    ] == "supervised_run_retry_gate_attestation_audit_blocked"
    assert context["evidence"]["demo_forward_supervised_run_retry_gate_attestation_record_pack"][
        "task_state"
    ] == "supervised_run_retry_gate_attestation_record_pack_blocked"
    assert context["evidence"]["demo_forward_supervised_run_retry_gate_attestation_refresh"][
        "task_state"
    ] == "supervised_run_retry_gate_attestation_refresh_blocked"
    assert context["evidence"]["demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration"][
        "task_state"
    ] == "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked"
    assert retry_boundary["demo_source"] == "dexter"
    assert retry_boundary["execution_mode"] == "paper_live"
    assert retry_boundary["route_mode"] == "single_sleeve"
    assert retry_boundary["selected_sleeve_id"] == "dexter_default"
    assert retry_boundary["max_active_real_demo_plans"] == 1
    assert retry_boundary["max_open_positions"] == 1
    assert retry_boundary["allowlist_required"] is True
    assert retry_boundary["small_lot_required"] is True
    assert retry_boundary["bounded_supervised_window_required"] is True
    assert retry_boundary["external_credential_refs_outside_repo"] is True
    assert retry_boundary["operator_owner_explicit_required"] is True
    assert retry_boundary["venue_connectivity_confirmation_required"] is True
    assert retry_boundary["stop_all_visibility_reconfirmation_required"] is True
    assert retry_boundary["mewx_unchanged"] is True
    assert retry_boundary["funded_live_forbidden"] is True

    prereqs = proof["supervised_run_retry_readiness"]["external_prerequisites"]
    assert prereqs["runtime_validation_errors"] == []
    assert prereqs["checklist_gate"]["external_reference_markers_present_in_repo"] is True
    assert prereqs["checklist_gate"]["runtime_guardrails_parse_cleanly"] is True
    assert prereqs["checklist_gate"]["real_demo_retry_execution_allowed"] is False
    assert len(prereqs["retry_prerequisite_matrix"]) == 8
    assert "operator_owner" in prereqs["unresolved_prerequisites"]
    assert "stop_all_visibility_reconfirmation" in prereqs["unresolved_prerequisites"]

    assert prompt_context["task_state"] == "supervised_run_retry_readiness_blocked"
    assert prompt_context["recommended_next_task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
    assert "FAIL/BLOCKED" in report_text
    assert "supervised_run_retry_readiness_blocked" in status_text
    assert "manual_latched_stop_all" in handoff_text
    assert "stop_all_visibility_reconfirmation" in handoff_text
    for name in ("Anscombe", "Euler", "Parfit"):
        assert name in subagents_text


def test_demo_forward_supervised_run_retry_readiness_spec_plan_and_docs_capture_required_boundary() -> None:
    spec_text = SPEC_PATH.read_text()
    plan_text = PLAN_PATH.read_text()
    checklist_text = CHECKLIST_PATH.read_text()
    matrix_text = MATRIX_PATH.read_text()
    subagents_text = SUBAGENTS_PATH.read_text()

    for needle in (
        "Dexter-only real demo slice",
        "`single_sleeve`",
        "`dexter_default`",
        "max active real demo plans",
        "max open positions",
        "explicit allowlist required",
        "small lot required",
        "bounded supervised window required",
        "external credential refs remain outside repo",
        "operator owner must be explicit",
        "venue / connectivity confirmation must be explicit",
        "stop-all visibility must be reconfirmed before retry",
        "Mew-X unchanged",
        "funded live forbidden",
        "`prepare`",
        "`start`",
        "`status`",
        "`stop`",
        "`snapshot`",
        "FAIL/BLOCKED",
    ):
        assert needle in spec_text or needle in plan_text

    for needle in (
        "DEXTER_DEMO_CREDENTIAL_SOURCE",
        "DEXTER_DEMO_VENUE_REF",
        "DEXTER_DEMO_ACCOUNT_REF",
        "DEXTER_DEMO_CONNECTIVITY_PROFILE",
        "DEXTER_DEMO_ALLOWED_SYMBOLS",
        "DEXTER_DEMO_DEFAULT_SYMBOL",
        "DEXTER_DEMO_ORDER_SIZE_LOTS",
        "DEXTER_DEMO_MAX_ORDER_SIZE_LOTS",
        "DEXTER_DEMO_MAX_OPEN_POSITIONS=1",
        "DEXTER_DEMO_WINDOW_MINUTES=15",
        "manual_latched_stop_all",
        "funded live forbidden",
    ):
        assert needle in checklist_text or needle in matrix_text

    for needle in ("Anscombe", "Euler", "Parfit"):
        assert needle in subagents_text
