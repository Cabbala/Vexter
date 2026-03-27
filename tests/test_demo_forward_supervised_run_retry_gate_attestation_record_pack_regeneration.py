import json
import os
import subprocess
import tarfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = (
    REPO_ROOT
    / "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json"
)
REPORT_PATH = (
    REPO_ROOT
    / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md"
)
STATUS_PATH = (
    REPO_ROOT
    / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md"
)
HANDOFF_PATH = (
    REPO_ROOT
    / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md"
)
SUBAGENTS_PATH = (
    REPO_ROOT
    / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md"
)
SPEC_PATH = (
    REPO_ROOT
    / "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md"
)
PLAN_PATH = (
    REPO_ROOT / "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md"
)
CHECKLIST_PATH = (
    REPO_ROOT
    / "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md"
)
DECISION_SURFACE_PATH = (
    REPO_ROOT
    / "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md"
)
PROMPT_CONTEXT_PATH = (
    REPO_ROOT
    / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/CONTEXT.json"
)
EXPORT_SCRIPT_PATH = (
    REPO_ROOT / "scripts/export_attestation_record_pack_regeneration_closeout_bundle.sh"
)
CONTRACT_SPEC_REL_PATH = "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_EXTERNAL_EVIDENCE_CONTRACT.md"
EVIDENCE_TEMPLATE_REL_PATH = (
    "manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json"
)
GAP_REPORT_REL_PATH = (
    "artifacts/reports/demo-forward-supervised-run-retry-gate-external-evidence-gap-report.md"
)
GAP_PROOF_REL_PATH = (
    "artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-check.json"
)
PREFLIGHT_REPORT_REL_PATH = (
    "artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md"
)
PREFLIGHT_PROOF_REL_PATH = (
    "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json"
)
PREFLIGHT_SUMMARY_REL_PATH = (
    "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-summary.md"
)


def load_last_ledger_entry() -> dict:
    lines = (REPO_ROOT / "artifacts/task_ledger.jsonl").read_text().strip().splitlines()
    return json.loads(lines[-1])


def test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_artifacts_are_current_and_consistent() -> None:
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
    assert (
        manifest["task_id"]
        == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION"
    )
    assert (
        manifest["status"]
        == ledger["status"]
        == "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked"
    )
    assert (
        manifest["bundle_path"]
        == ledger["artifact_bundle"]
        == "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration.tar.gz"
    )
    assert (
        manifest["bundle_source"]
        == context["bundle_source"]
        == "/Users/cabbala/Downloads/vexter_attestation_record_pack_regeneration_bundle_latest.tar.gz"
    )
    assert manifest["next_task"]["id"] == context["next_task"]["id"] == ledger["next_task_id"]
    assert (
        manifest["next_task"]["id"]
        == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH"
    )
    assert manifest["next_task"]["state"] == context["next_task"]["state"] == ledger["next_task_state"]
    assert (
        manifest["next_task"]["state"]
        == "additional_attestation_refresh_required_for_record_pack_regeneration"
    )
    assert manifest["next_task"]["pass_successor"]["id"] == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
    assert manifest["next_task"]["pass_successor"]["lane"] == "supervised_run_retry_gate"

    assert (
        proof["task_id"]
        == "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION"
    )
    assert proof["verified_github"]["latest_vexter_pr"] == 93
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "1271c18b6a57bb0ff5e9eedae6a886ba90945960"
    )
    assert proof["verified_github"]["latest_vexter_merged_at"] == "2026-03-27T22:25:21Z"
    assert proof["task_result"]["outcome"] == "FAIL/BLOCKED"
    assert (
        proof["task_result"]["recommended_next_step"] == "supervised_run_retry_gate_attestation_refresh"
    )
    assert proof["task_result"]["gate_pass_successor"] == "supervised_run_retry_gate"
    assert (
        proof["task_result"]["decision"]
        == "retry_gate_review_blocked_pending_current_attestation_record_pack_regeneration"
    )

    canonical_external_evidence = proof[
        "supervised_run_retry_gate_attestation_record_pack_regeneration"
    ]["canonical_external_evidence"]
    assert canonical_external_evidence["contract_spec"] == CONTRACT_SPEC_REL_PATH
    assert canonical_external_evidence["manifest_path"] == EVIDENCE_TEMPLATE_REL_PATH
    assert canonical_external_evidence["preflight_report"] == PREFLIGHT_REPORT_REL_PATH
    assert canonical_external_evidence["preflight_proof"] == PREFLIGHT_PROOF_REL_PATH
    assert canonical_external_evidence["preflight_summary"] == PREFLIGHT_SUMMARY_REL_PATH
    assert canonical_external_evidence["preflight_status"] == "blocked"
    assert canonical_external_evidence["gap_report"] == GAP_REPORT_REL_PATH
    assert canonical_external_evidence["gap_proof"] == GAP_PROOF_REL_PATH
    assert canonical_external_evidence["manifest_status"] == "template_only"
    assert canonical_external_evidence["retry_gate_review_reopen_ready"] is False
    assert canonical_external_evidence["aggregated_blocked_reason_counts"]["template_only_manifest"] == 9
    assert "Manifest remains template_only" in canonical_external_evidence["template_only_false_path"]
    assert canonical_external_evidence["consistency_checks"]["blocked_reason_counts_match_face_rows"] is True
    assert (
        canonical_external_evidence["next_human_pass"]["faces"][0]["face"]
        == "external_credential_source_face"
    )

    regeneration_boundary = context["evidence"][
        "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration"
    ]["attestation_record_pack_regeneration_boundary"]
    assert context["evidence"]["github_latest"]["latest_recent_vexter_prs"] == [93, 92, 91, 90, 89]
    assert (
        context["evidence"]["github_latest"]["vexter_pr_93_merged_at"]
        == "2026-03-27T22:25:21Z"
    )
    regeneration_evidence = context["evidence"][
        "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration"
    ]
    assert regeneration_evidence["attestation_record_pack_regeneration_surface_current"] is True
    assert (
        context["evidence"]["demo_forward_supervised_run_retry_gate_attestation_refresh"][
            "attestation_refresh_surface_current"
        ]
        is False
    )
    assert regeneration_boundary["demo_source"] == "dexter"
    assert regeneration_boundary["execution_mode"] == "paper_live"
    assert regeneration_boundary["route_mode"] == "single_sleeve"
    assert regeneration_boundary["selected_sleeve_id"] == "dexter_default"
    assert regeneration_boundary["max_active_real_demo_plans"] == 1
    assert regeneration_boundary["max_open_positions"] == 1
    assert regeneration_boundary["allowlist_required"] is True
    assert regeneration_boundary["small_lot_required"] is True
    assert regeneration_boundary["bounded_supervised_window_required"] is True
    assert regeneration_boundary["external_credential_refs_outside_repo"] is True
    assert regeneration_boundary["operator_owner_explicit_required"] is True
    assert regeneration_boundary["venue_connectivity_confirmation_required"] is True
    assert regeneration_boundary["bounded_start_criteria_explicit_required"] is True
    assert regeneration_boundary["manual_latched_stop_all_visibility_reconfirmation_required"] is True
    assert regeneration_boundary["terminal_snapshot_readability_reconfirmation_required"] is True
    assert regeneration_boundary["mewx_unchanged"] is True
    assert regeneration_boundary["funded_live_forbidden"] is True

    assert regeneration_evidence["external_evidence_contract"] == CONTRACT_SPEC_REL_PATH
    assert regeneration_evidence["external_evidence_manifest"] == EVIDENCE_TEMPLATE_REL_PATH
    assert regeneration_evidence["external_evidence_preflight_report"] == PREFLIGHT_REPORT_REL_PATH
    assert regeneration_evidence["external_evidence_preflight_proof"] == PREFLIGHT_PROOF_REL_PATH
    assert regeneration_evidence["external_evidence_preflight_summary"] == PREFLIGHT_SUMMARY_REL_PATH
    assert regeneration_evidence["external_evidence_preflight_status"] == "blocked"
    assert regeneration_evidence["external_evidence_gap_report"] == GAP_REPORT_REL_PATH
    assert regeneration_evidence["external_evidence_gap_proof"] == GAP_PROOF_REL_PATH
    assert regeneration_evidence["external_evidence_manifest_status"] == "template_only"
    assert regeneration_evidence["retry_gate_review_reopen_ready_from_external_evidence"] is False
    assert regeneration_evidence["aggregated_blocked_reason_counts"]["template_only_manifest"] == 9
    assert "Manifest remains template_only" in regeneration_evidence["template_only_false_path"]
    assert regeneration_evidence["consistency_checks"]["blocked_face_names_match_face_rows"] is True
    assert regeneration_evidence["next_human_pass"]["faces"][0]["face"] == "external_credential_source_face"
    assert regeneration_evidence["per_face_manifest_field_maps_explicit"] is True
    assert regeneration_evidence["per_face_proof_path_maps_explicit"] is True
    assert regeneration_evidence["canonical_gap_blocked_faces_align_with_regeneration_lane"] is True

    regeneration_faces = proof[
        "supervised_run_retry_gate_attestation_record_pack_regeneration"
    ]["regeneration_faces"]
    assert regeneration_faces["record_pack_reviewable_now"] is False
    assert regeneration_faces["retry_gate_review_reopen_ready"] is False
    checklist = regeneration_faces["checklist_attestation_record_pack_regeneration"]
    assert checklist["runtime_guardrails_parse_cleanly"] is True
    assert checklist["all_required_faces_present"] is True
    assert checklist["all_regeneration_owners_explicit"] is True
    assert checklist["all_regeneration_triggers_explicit"] is True
    assert checklist["all_minimum_regenerated_locator_shapes_explicit"] is True
    assert checklist["all_freshness_inheritance_rules_explicit"] is True
    assert checklist["all_regenerated_reviewable_conditions_explicit"] is True
    assert checklist["all_manifest_field_maps_explicit"] is True
    assert checklist["all_proof_path_maps_explicit"] is True
    assert checklist["all_current_fresh_locator_inputs_present"] is False
    assert checklist["all_freshness_inherited_cleanly"] is False
    assert checklist["all_regenerated_faces_reviewable_now"] is False
    assert len(regeneration_faces["attestation_record_pack_regeneration_decision_surface"]) == 9
    assert "operator_owner_face" in regeneration_faces["blocked_regenerated_faces"]
    assert "terminal_snapshot_readability_reconfirmed" in regeneration_faces["blocked_regenerated_faces"]
    first_face = regeneration_faces["attestation_record_pack_regeneration_decision_surface"][0]
    assert first_face["regeneration_rule_complete"] is True
    assert first_face["current_fresh_locator_present"] is False
    assert first_face["freshness_inherited_cleanly"] is False
    assert first_face["regenerated_face_reviewable_now"] is False
    assert "minimum_regenerated_locator_shape" in first_face
    assert "freshness_inheritance_or_reset_rule" in first_face
    assert (
        first_face["regeneration_trigger"].count(
            "regenerate the current record-pack face again whenever"
        )
        == 1
    )
    assert (
        first_face["minimum_regenerated_locator_shape"].count(
            "plus regenerated face name, regeneration timestamp"
        )
        == 1
    )
    assert first_face["freshness_inheritance_or_reset_rule"].count(
        "inherit freshness only while"
    ) == 1
    assert (
        first_face["reviewable_enough_when"].count(
            "regenerated face points to the same bounded-window locator"
        )
        == 1
    )
    assert (
        "faces.external_credential_source_face.evidence_locator"
        in first_face["required_manifest_fields"]
    )
    assert GAP_PROOF_REL_PATH in first_face["proof_paths_to_recheck"]
    assert "template_only_manifest" in first_face["canonical_blocked_reasons"]
    assert "Provide one current non-secret locator" in first_face["operator_input_needed"]
    assert "template_only_manifest" in first_face["current_regeneration_observation"]
    assert "outside_repo_locator_not_supplied" in first_face["current_regeneration_observation"]
    assert "Operator input still needed:" in first_face["current_regeneration_observation"]

    assert (
        prompt_context["task_state"]
        == "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked"
    )
    assert prompt_context["recommended_next_step"] == "supervised_run_retry_gate_attestation_refresh"
    assert prompt_context["candidate_pass_next_step"] == "supervised_run_retry_gate"
    assert prompt_context["external_evidence_manifest_status"] == "template_only"
    assert prompt_context["external_evidence_preflight_status"] == "blocked"
    assert prompt_context["external_evidence_preflight_report"] == PREFLIGHT_REPORT_REL_PATH
    assert prompt_context["external_evidence_gap_report"] == GAP_REPORT_REL_PATH
    assert "Manifest remains template_only" in prompt_context["external_evidence_template_only_false_path"]
    assert "FAIL/BLOCKED" in report_text
    assert "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked" in status_text
    assert "manual_latched_stop_all" in handoff_text
    assert "baseline_attestation_refresh_task_state" in handoff_text
    assert PREFLIGHT_REPORT_REL_PATH in report_text
    assert PREFLIGHT_REPORT_REL_PATH in handoff_text
    assert GAP_REPORT_REL_PATH in report_text
    assert GAP_REPORT_REL_PATH in handoff_text
    assert "Canonical Evidence Intake Handoff" in handoff_text
    assert "Next Human Pass Checklist" in handoff_text
    assert "template_only_false_path" in handoff_text
    assert "evidence_preflight_consistency_checks" in handoff_text
    assert "bounded_window_fields_to_fill_once" in handoff_text
    assert "faces.external_credential_source_face.evidence_locator" in handoff_text
    assert "template_only_reopen_ready_consistency_holds: true" in handoff_text
    assert "## Next Human Pass" in report_text
    assert "supervised_run_retry_gate" in decision_surface_text
    for name in ("Anscombe", "Euler", "Parfit"):
        assert name in subagents_text


def test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_spec_plan_and_docs_capture_required_boundary() -> None:
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
        "regeneration owner",
        "regeneration trigger",
        "minimum regenerated locator shape",
        "freshness inheritance or reset rule",
        "reviewable enough",
        "canonical external evidence",
        "gap report",
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
        "Regeneration owner",
        "Regeneration trigger",
        "Freshness inheritance or reset rule",
        "funded live forbidden",
        "evidence-preflight-report",
    ):
        assert needle in checklist_text or needle in decision_surface_text

    for name in ("Anscombe", "Euler", "Parfit"):
        assert name in subagents_text


def test_export_attestation_record_pack_regeneration_closeout_bundle(tmp_path: Path) -> None:
    output_path = tmp_path / "closeout.tar.gz"
    expected_proof_bundle_name = Path(
        json.loads((REPO_ROOT / "artifacts/proof_bundle_manifest.json").read_text())["bundle_path"]
    ).name
    env = {
        "RESULT_BRANCH": "codex/attestation-record-pack-regeneration-after-pr90",
        "RESULT_COMMIT_SHA": "abc123def456",
        "RESULT_PR_URL": "https://github.com/Cabbala/Vexter/pull/999",
        "RESULT_MERGE_COMMIT_SHA": "fedcba654321",
        "RESULT_MERGED_AT": "2026-03-28T04:45:03Z",
        "RESULT_TEST_RESULT": "284 passed",
        "ANSCOMBE_SUMMARY": "Current pointers move atomically from refresh to regeneration off merged PR #90 through the shared external-evidence contract.",
        "EULER_SUMMARY": "Planner boundary and fail-closed runtime guardrails stayed unchanged.",
        "PARFIT_SUMMARY": "Closeout bundle now carries the regeneration result, handoff, report, status, baseline refresh handoff, proof tarball, and canonical external-evidence artifacts.",
    }
    subprocess.run(
        [str(EXPORT_SCRIPT_PATH), str(output_path)],
        check=True,
        cwd=REPO_ROOT,
        env={**os.environ, **env},
    )

    assert output_path.exists()
    with tarfile.open(output_path, "r:gz") as tar:
        names = tar.getnames()
        assert any(name.endswith("/RESULT.md") for name in names)
        assert any(name.endswith("/HANDOFF.md") for name in names)
        assert any(name.endswith("/subagent_summary.md") for name in names)
        assert any(
            name.endswith("/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md")
            for name in names
        )
        assert any(
            name.endswith("/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md")
            for name in names
        )
        assert any(name.endswith("/baseline-attestation-refresh-HANDOFF.md") for name in names)
        assert any(name.endswith(f"/{expected_proof_bundle_name}") for name in names)
        assert any(name.endswith("/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_EXTERNAL_EVIDENCE_CONTRACT.md") for name in names)
        assert any(name.endswith("/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json") for name in names)
        assert any(name.endswith("/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md") for name in names)
        assert any(name.endswith("/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json") for name in names)
        assert any(name.endswith("/demo-forward-supervised-run-retry-gate-evidence-preflight-summary.md") for name in names)
        assert any(name.endswith("/demo-forward-supervised-run-retry-gate-external-evidence-gap-report.md") for name in names)
        assert any(name.endswith("/demo-forward-supervised-run-retry-gate-external-evidence-gap-check.json") for name in names)
        result_member = next(name for name in names if name.endswith("/RESULT.md"))
        subagent_member = next(name for name in names if name.endswith("/subagent_summary.md"))
        result_text = tar.extractfile(result_member).read().decode("utf-8")
        subagent_text = tar.extractfile(subagent_member).read().decode("utf-8")

    assert "284 passed" in result_text
    assert "https://github.com/Cabbala/Vexter/pull/999" in result_text
    assert "abc123def456" in result_text
    assert "fedcba654321" in result_text
    for name in ("Anscombe", "Euler", "Parfit"):
        assert name in subagent_text
