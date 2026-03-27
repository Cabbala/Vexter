import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = REPO_ROOT / "artifacts/proofs/demo-forward-acceptance-pack-check.json"
SUMMARY_PATH = REPO_ROOT / "artifacts/summary.md"
REPORT_PATH = REPO_ROOT / "artifacts/reports/demo-forward-acceptance-pack-report.md"
STATUS_PATH = REPO_ROOT / "artifacts/reports/demo-forward-acceptance-pack-status.md"
HANDOFF_PATH = REPO_ROOT / "artifacts/reports/demo-forward-acceptance-pack/HANDOFF.md"
SPEC_PATH = REPO_ROOT / "specs/DEMO_FORWARD_ACCEPTANCE_PACK.md"
PLAN_PATH = REPO_ROOT / "plans/demo_forward_acceptance_pack_plan.md"
CHECKLIST_PATH = REPO_ROOT / "docs/demo_forward_operator_checklist.md"
ABORT_MATRIX_PATH = REPO_ROOT / "docs/demo_forward_abort_rollback_matrix.md"
PROMPT_CONTEXT_PATH = REPO_ROOT / "artifacts/reports/demo-forward-acceptance-pack/CONTEXT.json"


def load_last_ledger_entry() -> dict:
    lines = (REPO_ROOT / "artifacts/task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


def test_demo_forward_acceptance_pack_artifacts_are_current_and_consistent() -> None:
    proof = json.loads(PROOF_PATH.read_text())
    manifest = json.loads((REPO_ROOT / "artifacts/proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts/context_pack.json").read_text())
    ledger = load_last_ledger_entry()
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())
    summary_text = SUMMARY_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    handoff_text = HANDOFF_PATH.read_text()

    assert manifest["task_id"] == context["current_task"]["id"] == ledger["task_id"]
    assert manifest["task_id"] == "DEMO-FORWARD-ACCEPTANCE-PACK"
    assert manifest["status"] == ledger["status"] == "demo_forward_acceptance_pack_ready"
    assert (
        manifest["bundle_path"]
        == ledger["artifact_bundle"]
        == "artifacts/bundles/demo-forward-acceptance-pack.tar.gz"
    )
    assert manifest["next_task"]["id"] == context["next_task"]["id"] == ledger["next_task_id"]
    assert manifest["next_task"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN"
    assert manifest["next_task"]["state"] == context["next_task"]["state"] == ledger["next_task_state"]
    assert manifest["next_task"]["state"] == "ready_for_demo_forward_supervised_run"

    assert proof["task_id"] == "DEMO-FORWARD-ACCEPTANCE-PACK"
    assert proof["verified_github"]["latest_vexter_pr"] == 71
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "5c1feb2561da7b16a17c5d03b71ff2bf895e20e4"
    )
    assert proof["task_result"]["recommended_next_step"] == "demo_forward_supervised_run"
    assert proof["task_result"]["decision"] == "demo_forward_supervised_run_ready"

    acceptance_boundary = context["evidence"]["demo_forward_acceptance_pack"]["acceptance_boundary"]
    assert acceptance_boundary["demo_source"] == "dexter"
    assert acceptance_boundary["execution_mode"] == "paper_live"
    assert acceptance_boundary["route_mode"] == "single_sleeve"
    assert acceptance_boundary["selected_sleeve_id"] == "dexter_default"
    assert acceptance_boundary["max_active_real_demo_plans"] == 1
    assert acceptance_boundary["max_open_positions"] == 1
    assert acceptance_boundary["allowlist_required"] is True
    assert acceptance_boundary["small_lot_required"] is True
    assert acceptance_boundary["operator_supervised_window_required"] is True
    assert acceptance_boundary["mewx_overlay_enabled"] is False
    assert acceptance_boundary["funded_live_forbidden"] is True

    assert prompt_context["task_state"] == "demo_forward_acceptance_pack_ready"
    assert prompt_context["recommended_next_task_id"] == "DEMO-FORWARD-SUPERVISED-RUN"
    assert "demo_forward_supervised_run" in summary_text
    assert "demo_forward_acceptance_pack_ready" in status_text
    assert "Dexter-only real demo slice" in report_text
    assert "manual_latched_stop_all" in handoff_text
    assert "terminal_snapshot_visibility_lost" in handoff_text


def test_demo_forward_acceptance_pack_spec_plan_and_docs_capture_required_boundary() -> None:
    spec_text = SPEC_PATH.read_text()
    plan_text = PLAN_PATH.read_text()
    checklist_text = CHECKLIST_PATH.read_text()
    abort_matrix_text = ABORT_MATRIX_PATH.read_text()

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
    ):
        assert needle in spec_text or needle in plan_text

    for needle in (
        "DEXTER_DEMO_ALLOWED_SYMBOLS",
        "DEXTER_DEMO_DEFAULT_SYMBOL",
        "DEXTER_DEMO_ORDER_SIZE_LOTS",
        "DEXTER_DEMO_MAX_OPEN_POSITIONS=1",
        "manual_latched_stop_all",
        "terminal snapshot",
    ):
        assert needle in checklist_text

    for needle in (
        "pin_mismatch",
        "mode_mismatch",
        "status_or_fill_reconciliation_gap",
        "duplicate_or_ambiguous_handle",
        "unexpected_funded_live_path",
        "cancel_or_stop_all_unconfirmed",
        "quarantine_or_manual_halt_triggered",
        "terminal_snapshot_visibility_lost",
    ):
        assert needle in abort_matrix_text
