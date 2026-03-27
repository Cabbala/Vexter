import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = REPO_ROOT / "artifacts/proofs/pattern-a-demo-executor-cutover-check.json"
SUMMARY_PATH = REPO_ROOT / "artifacts/proofs/pattern-a-demo-executor-cutover-summary.md"
REPORT_PATH = REPO_ROOT / "artifacts/reports/pattern-a-demo-executor-cutover-report.md"
STATUS_PATH = REPO_ROOT / "artifacts/reports/pattern-a-demo-executor-cutover-status.md"
HANDOFF_PATH = REPO_ROOT / "artifacts/reports/pattern-a-demo-executor-cutover/HANDOFF.md"
SPEC_PATH = REPO_ROOT / "specs/PATTERN_A_DEMO_EXECUTOR_CUTOVER.md"
PLAN_PATH = REPO_ROOT / "plans/demo_executor_adapter_implementation_plan.md"

def test_pattern_a_demo_executor_cutover_artifacts_are_consistent() -> None:
    proof = json.loads(PROOF_PATH.read_text())
    manifest = json.loads((REPO_ROOT / "artifacts/proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts/context_pack.json").read_text())
    summary_text = SUMMARY_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    status_text = STATUS_PATH.read_text()
    handoff_text = HANDOFF_PATH.read_text()

    assert "artifacts/proofs/pattern-a-demo-executor-cutover-check.json" in manifest["proof_files"]
    assert "artifacts/proofs/pattern-a-demo-executor-cutover-summary.md" in manifest["proof_files"]
    assert "artifacts/reports/pattern-a-demo-executor-cutover-report.md" in manifest["reports"]
    assert "artifacts/reports/pattern-a-demo-executor-cutover-status.md" in manifest["reports"]
    assert context["evidence"]["pattern_a_demo_executor_cutover"]["task_state"] == (
        "pattern_a_demo_executor_cutover_ready"
    )
    assert context["evidence"]["pattern_a_demo_executor_cutover"]["preferred_next_step"] == (
        "demo_executor_adapter_implementation"
    )
    assert context["evidence"]["demo_executor_adapter_implementation"]["task_state"] == (
        "demo_executor_adapter_implemented"
    )
    assert context["evidence"]["demo_executor_adapter_implementation"]["preferred_next_step"] == (
        "demo_forward_acceptance_pack"
    )

    assert proof["task_id"] == "PATTERN-A-DEMO-EXECUTOR-CUTOVER"
    assert proof["verified_github"]["latest_vexter_pr"] == 69
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "289eb1bc87a8db9a9801b9b0583a8dbc6b17a5b3"
    )
    assert proof["task_result"]["recommended_next_step"] == "demo_executor_adapter_implementation"
    assert proof["task_result"]["decision"] == "demo_executor_adapter_implementation_ready"

    first_target = context["evidence"]["pattern_a_demo_executor_cutover"]["first_demo_target"]
    assert first_target["source"] == "dexter"
    assert first_target["execution_mode"] == "paper_live"
    assert first_target["entrypoint"] == "monitor_mint_session"
    assert (
        context["evidence"]["pattern_a_demo_executor_cutover"]["real_vs_simulated"]["realized_now"]
        == ["dexter_paper_live_demo_adapter"]
    )
    assert (
        context["evidence"]["pattern_a_demo_executor_cutover"]["real_vs_simulated"]["still_simulated"]
        == ["mewx_sim_live", "funded_live_trading", "portfolio_split_real_execution"]
    )

    assert "PATTERN-A-DEMO-EXECUTOR-CUTOVER" in summary_text or "Pattern A" in summary_text
    assert "demo_executor_adapter_implementation" in summary_text
    assert "pattern_a_demo_executor_cutover_ready" in status_text
    assert "Dexter `paper_live`" in report_text
    assert "Mew-X `sim_live`" in report_text
    assert "manual_latched_stop_all" in handoff_text
    assert "poll_first" in handoff_text


def test_pattern_a_demo_executor_cutover_spec_and_plan_capture_boundary() -> None:
    spec_text = SPEC_PATH.read_text()
    plan_text = PLAN_PATH.read_text()

    for needle in (
        "Dexter stays `paper_live`",
        "Mew-X stays frozen `sim_live`",
        "`submit_order`",
        "`cancel_order`",
        "`order_status`",
        "`fill_state`",
        "`stop_all`",
        "`manual_latched_stop_all`",
        "`poll_first`",
        "single_sleeve",
        "small-lot",
        "allowlist",
    ):
        assert needle in spec_text or needle in plan_text

    assert "demo_executor_adapter_implementation" in spec_text
    assert "one active `dexter_default` sleeve" in plan_text
