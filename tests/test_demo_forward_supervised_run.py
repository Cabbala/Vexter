import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = REPO_ROOT / "artifacts/proofs/demo-forward-supervised-run-check.json"
SUMMARY_PATH = REPO_ROOT / "artifacts/proofs/demo-forward-supervised-run-summary.md"
REPORT_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-report.md"
STATUS_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run-status.md"
HANDOFF_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run/HANDOFF.md"
SPEC_PATH = REPO_ROOT / "specs/DEMO_FORWARD_SUPERVISED_RUN.md"
PLAN_PATH = REPO_ROOT / "plans/demo_forward_supervised_run_plan.md"
FOLLOW_UP_PATH = REPO_ROOT / "docs/demo_forward_supervised_run_operator_follow_up.md"
PROMPT_CONTEXT_PATH = REPO_ROOT / "artifacts/reports/demo-forward-supervised-run/CONTEXT.json"


def test_demo_forward_supervised_run_artifacts_remain_consistent() -> None:
    proof = json.loads(PROOF_PATH.read_text())
    manifest = json.loads((REPO_ROOT / "artifacts/proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts/context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    summary_text = SUMMARY_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    handoff_text = HANDOFF_PATH.read_text()
    follow_up_text = FOLLOW_UP_PATH.read_text()

    assert "artifacts/proofs/demo-forward-supervised-run-check.json" in manifest["proof_files"]
    assert "artifacts/proofs/demo-forward-supervised-run-summary.md" in manifest["proof_files"]
    assert "artifacts/reports/demo-forward-supervised-run-report.md" in manifest["reports"]
    assert "artifacts/reports/demo-forward-supervised-run-status.md" in manifest["reports"]
    assert "docs/demo_forward_supervised_run_operator_follow_up.md" in manifest["docs"]
    assert "scripts/run_demo_forward_supervised_run.py" in manifest["scripts"]
    assert context["evidence"]["demo_forward_supervised_run"]["task_state"] == (
        "demo_forward_supervised_run_blocked"
    )
    assert context["evidence"]["demo_forward_supervised_run"]["preferred_next_step"] == (
        "supervised_run_retry_readiness"
    )
    assert context["evidence"]["demo_forward_supervised_run_retry_readiness"]["task_state"] == (
        "supervised_run_retry_readiness_blocked"
    )

    assert proof["task_id"] == "DEMO-FORWARD-SUPERVISED-RUN"
    assert proof["verified_github"]["latest_vexter_pr"] == 72
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "a6ca623b01dbed4191c4be10c2bfe51534025cac"
    )
    assert proof["task_result"]["outcome"] == "FAIL/BLOCKED"
    assert proof["task_result"]["recommended_next_step"] == "supervised_run_retry_readiness"
    assert proof["task_result"]["decision"] == "supervised_run_retry_readiness_required"

    supervised_boundary = context["evidence"]["demo_forward_supervised_run"]["supervised_boundary"]
    assert supervised_boundary["demo_source"] == "dexter"
    assert supervised_boundary["execution_mode"] == "paper_live"
    assert supervised_boundary["route_mode"] == "single_sleeve"
    assert supervised_boundary["selected_sleeve_id"] == "dexter_default"
    assert supervised_boundary["max_active_real_demo_plans"] == 1
    assert supervised_boundary["max_open_positions"] == 1
    assert supervised_boundary["allowlist_required"] is True
    assert supervised_boundary["small_lot_required"] is True
    assert supervised_boundary["operator_supervised_window_required"] is True
    assert supervised_boundary["mewx_overlay_enabled"] is False
    assert supervised_boundary["funded_live_forbidden"] is True

    supervised_sequence = proof["demo_forward_supervised_run"]["supervised_sequence"]
    assert supervised_sequence["prepare"]["status_delivery"] == "poll_first"
    assert supervised_sequence["status"]["native_order_status"] == "filled"
    assert supervised_sequence["status"]["fill_count"] == 1
    assert supervised_sequence["stop"]["stop_all_state"] == "flatten_requested"
    assert supervised_sequence["snapshot"]["stop_all_state"] == "flatten_confirmed"
    assert supervised_sequence["snapshot"]["fill_count"] == 2

    prereqs = proof["demo_forward_supervised_run"]["external_prerequisites"]
    assert prereqs["operator_attestation_available"] is False
    assert prereqs["venue_connectivity_confirmed"] is False
    assert prereqs["real_demo_completion_claim_allowed"] is False
    assert (
        proof["demo_forward_supervised_run"]["normalized_failure_detail"]["failure_code"]
        == "external_prerequisites_unresolved"
    )

    assert prompt_context["task_state"] == "demo_forward_supervised_run_blocked"
    assert prompt_context["recommended_next_task_id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS"
    assert "supervised_run_retry_readiness" in summary_text
    assert "FAIL/BLOCKED" in report_text
    assert "demo_forward_supervised_run_blocked" in status_text
    assert "manual_latched_stop_all" in handoff_text
    assert "real_demo_completion_claim_allowed: false" in handoff_text
    assert "Do not claim a real-demo completion." in follow_up_text


def test_demo_forward_supervised_run_spec_plan_and_follow_up_capture_required_boundary() -> None:
    spec_text = SPEC_PATH.read_text()
    plan_text = PLAN_PATH.read_text()
    follow_up_text = FOLLOW_UP_PATH.read_text()

    for needle in (
        "Dexter-only real demo slice",
        "`single_sleeve`",
        "`dexter_default`",
        "max active real demo plans",
        "max open positions",
        "explicit allowlist required",
        "small lot required",
        "bounded operator-supervised window required",
        "Mew-X overlay disabled / unchanged",
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
        "manual_latched_stop_all",
        "funded live forbidden",
    ):
        assert needle in follow_up_text
