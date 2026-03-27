import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = REPO_ROOT / "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json"
REPORT_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md"
STATUS_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md"
HANDOFF_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md"
SUBAGENTS_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md"
SPEC_PATH = REPO_ROOT / "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md"
PLAN_PATH = REPO_ROOT / "plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md"
CHECKLIST_PATH = REPO_ROOT / "docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md"
DECISION_SURFACE_PATH = REPO_ROOT / "docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md"
PROMPT_CONTEXT_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/CONTEXT.json"


def load_last_ledger_entry() -> dict:
    lines = (REPO_ROOT / "artifacts/task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


def test_demo_forward_supervised_run_retry_gate_attestation_audit_artifacts_are_current_and_consistent() -> None:
    proof = json.loads(PROOF_PATH.read_text())
    manifest = json.loads((REPO_ROOT / "artifacts/proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts/context_pack.json").read_text())
    ledger = load_last_ledger_entry()
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    report_text = REPORT_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    handoff_text = HANDOFF_PATH.read_text()
    subagents_text = SUBAGENTS_PATH.read_text()
    decision_surface_text = DECISION_SURFACE_PATH.read_text()

    assert manifest["task_id"] == context["current_task"]["id"] == ledger["task_id"]
    assert manifest["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH"
    assert manifest["status"] == ledger["status"] == "supervised_run_retry_gate_attestation_refresh_blocked"
    assert (
        manifest["bundle_path"]
        == ledger["artifact_bundle"]
        == "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-refresh.tar.gz"
    )
    assert manifest["next_task"]["id"] == context["next_task"]["id"] == ledger["next_task_id"]
    assert (
        manifest["next_task"]["id"]
        == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION"
    )
    assert manifest["next_task"]["state"] == context["next_task"]["state"] == ledger["next_task_state"]
    assert manifest["next_task"]["state"] == "ready_for_attestation_record_pack_regeneration"
    assert manifest["next_task"]["pass_successor"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
    assert manifest["next_task"]["pass_successor"]["lane"] == "supervised_run_retry_gate"

    assert proof["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT"
    assert proof["verified_github"]["latest_vexter_pr"] == 76
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "56dedfe86bf9f6252d1099775fa9506d7259e0da"
    )
    assert proof["task_result"]["outcome"] == "FAIL/BLOCKED"
    assert proof["task_result"]["recommended_next_step"] == "supervised_run_retry_gate_attestation_audit"
    assert proof["task_result"]["gate_pass_successor"] == "supervised_run_retry_gate"
    assert (
        proof["task_result"]["decision"]
        == "retry_gate_review_blocked_pending_auditable_attestation_records"
    )

    audit_boundary = context["evidence"]["demo_forward_supervised_run_retry_gate_attestation_audit"][
        "attestation_audit_boundary"
    ]
    assert audit_boundary["demo_source"] == "dexter"
    assert audit_boundary["execution_mode"] == "paper_live"
    assert audit_boundary["route_mode"] == "single_sleeve"
    assert audit_boundary["selected_sleeve_id"] == "dexter_default"
    assert audit_boundary["max_active_real_demo_plans"] == 1
    assert audit_boundary["max_open_positions"] == 1
    assert audit_boundary["allowlist_required"] is True
    assert audit_boundary["small_lot_required"] is True
    assert audit_boundary["bounded_supervised_window_required"] is True
    assert audit_boundary["external_credential_refs_outside_repo"] is True
    assert audit_boundary["operator_owner_explicit_required"] is True
    assert audit_boundary["venue_connectivity_confirmation_required"] is True
    assert audit_boundary["bounded_start_criteria_explicit_required"] is True
    assert audit_boundary["manual_latched_stop_all_visibility_reconfirmation_required"] is True
    assert audit_boundary["terminal_snapshot_readability_reconfirmation_required"] is True
    assert audit_boundary["mewx_unchanged"] is True
    assert audit_boundary["funded_live_forbidden"] is True

    audit_faces = proof["supervised_run_retry_gate_attestation_audit"]["audit_faces"]
    assert audit_faces["retry_gate_review_reopen_ready"] is False
    assert audit_faces["checklist_attestation"]["runtime_guardrails_parse_cleanly"] is True
    assert audit_faces["checklist_attestation"]["all_required_faces_present"] is True
    assert audit_faces["checklist_attestation"]["all_definition_fields_explicit"] is True
    assert audit_faces["checklist_attestation"]["all_stale_conditions_explicit"] is True
    assert audit_faces["checklist_attestation"]["all_auditable_enough_conditions_explicit"] is True
    assert audit_faces["checklist_attestation"]["all_current_attestation_refs_present"] is False
    assert audit_faces["checklist_attestation"]["all_faces_non_stale_now"] is False
    assert audit_faces["checklist_attestation"]["all_faces_auditable_now"] is False
    assert len(audit_faces["attestation_audit_decision_surface"]) == 9
    assert "operator_owner_face" in audit_faces["blocked_audit_faces"]
    assert "terminal_snapshot_readability_reconfirmed" in audit_faces["blocked_audit_faces"]
    first_face = audit_faces["attestation_audit_decision_surface"][0]
    assert first_face["definition_complete"] is True
    assert first_face["current_attestation_ref_present"] is False
    assert first_face["auditable_now"] is False
    assert "auditable_enough_when" in first_face
    assert "minimal_evidence_shape" in first_face

    assert prompt_context["task_state"] == "supervised_run_retry_gate_attestation_audit_blocked"
    assert prompt_context["recommended_next_step"] == "supervised_run_retry_gate_attestation_audit"
    assert prompt_context["candidate_pass_next_step"] == "supervised_run_retry_gate"
    assert "FAIL/BLOCKED" in report_text
    assert "supervised_run_retry_gate_attestation_audit_blocked" in status_text
    assert "manual_latched_stop_all" in handoff_text
    assert "baseline_retry_gate_input_attestation_task_state" in handoff_text
    assert "supervised_run_retry_gate" in decision_surface_text
    for name in ("Anscombe", "Euler", "Parfit"):
        assert name in subagents_text


def test_demo_forward_supervised_run_retry_gate_attestation_audit_spec_plan_and_docs_capture_required_boundary() -> None:
    spec_text = SPEC_PATH.read_text()
    plan_text = PLAN_PATH.read_text()
    checklist_text = CHECKLIST_PATH.read_text()
    decision_surface_text = DECISION_SURFACE_PATH.read_text()
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
        "operator owner explicit",
        "venue / connectivity confirmation explicit",
        "bounded start criteria explicit",
        "`manual_latched_stop_all` visibility reconfirmation explicit",
        "terminal snapshot readability reconfirmation explicit",
        "who attests",
        "what is being attested",
        "minimal evidence shape",
        "what makes the face auditable enough",
        "Mew-X unchanged",
        "funded live forbidden",
        "`prepare`",
        "`start`",
        "`status`",
        "`stop`",
        "`snapshot`",
        "FAIL/BLOCKED",
    ):
        assert needle in spec_text or needle in plan_text or needle in decision_surface_text

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
        "terminal snapshot readability",
        "Who attests",
        "Minimal evidence shape",
        "auditable enough",
        "funded live forbidden",
    ):
        assert needle in checklist_text or needle in decision_surface_text

    for name in ("Anscombe", "Euler", "Parfit"):
        assert name in subagents_text
