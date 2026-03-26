import json
from pathlib import Path

from vexter.planner_router.transport import (
    _LIVEPAPER_WATCHDOG_SURFACES,
    _WATCHDOG_ACK_COUNT_KEYS,
    _WATCHDOG_ACK_DUPLICATE_FLAGS,
    _WATCHDOG_ACK_RETENTION_KEYS,
    _WATCHDOG_ACK_STICKY_KEYS,
    _WATCHDOG_FAILED_SNAPSHOT_REQUIRED_KEYS,
    _WATCHDOG_FAILURE_DETAIL_REQUIRED_KEYS,
    _WATCHDOG_FAILURE_REQUIRED_KEYS,
    _WATCHDOG_HANDLE_REQUIRED_KEYS,
    _WATCHDOG_LIFECYCLE_KEYS,
    _WATCHDOG_ROLLBACK_REQUIRED_KEYS,
    _WATCHDOG_RUNTIME_REQUIRED_KEYS,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = REPO_ROOT / "artifacts" / "proofs" / "task-007-livepaper-observability-spec-check.json"
REPORT_PATH = REPO_ROOT / "artifacts" / "reports" / "task-007-livepaper-observability-spec-report.md"
STATUS_PATH = REPO_ROOT / "artifacts" / "reports" / "task-007-livepaper-observability-spec-status.md"
SPEC_PATH = REPO_ROOT / "specs" / "LIVEPAPER_OBSERVABILITY_CONTRACT.md"
PROMPT_CONTEXT_PATH = (
    REPO_ROOT / "artifacts" / "reports" / "task-007-livepaper-observability-spec" / "CONTEXT.json"
)


def load_proof() -> dict[str, object]:
    return json.loads(PROOF_PATH.read_text())


def test_livepaper_observability_spec_proof_tracks_latest_git_state_and_recommendation() -> None:
    proof = load_proof()

    assert proof["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SPEC"
    assert proof["verified_github"]["latest_vexter_pr"] == 58
    assert (
        proof["verified_github"]["latest_vexter_main_commit"]
        == "10e23faa2a2428abae8206df963889392840919c"
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
    assert proof["livepaper_observability_spec"]["source_faithful_modes"] == {
        "dexter": "paper_live",
        "mewx": "sim_live",
    }
    assert proof["task_result"]["task_state"] == "livepaper_observability_spec_ready"
    assert (
        proof["task_result"]["recommended_next_step"]
        == "livepaper_observability_operator_runbook"
    )
    assert (
        proof["task_result"]["recommended_next_task_id"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-OPERATOR-RUNBOOK"
    )


def test_livepaper_observability_spec_proof_matches_transport_watchdog_contract() -> None:
    proof = load_proof()
    contract = proof["livepaper_observability_spec"]

    assert contract["required_surfaces"] == list(_LIVEPAPER_WATCHDOG_SURFACES)
    assert contract["required_fields"]["handle_metadata"] == list(_WATCHDOG_HANDLE_REQUIRED_KEYS)
    assert contract["required_fields"]["runtime_snapshot"] == list(_WATCHDOG_RUNTIME_REQUIRED_KEYS)
    assert contract["required_fields"]["failed_runtime_snapshot"] == list(
        _WATCHDOG_FAILED_SNAPSHOT_REQUIRED_KEYS
    )
    assert contract["required_fields"]["failure_envelope"] == list(_WATCHDOG_FAILURE_REQUIRED_KEYS)
    assert contract["required_fields"]["failure_detail"] == list(
        _WATCHDOG_FAILURE_DETAIL_REQUIRED_KEYS
    )
    assert contract["required_fields"]["rollback_snapshot"] == list(
        _WATCHDOG_ROLLBACK_REQUIRED_KEYS
    )
    assert contract["required_fields"]["ack_retention"] == list(_WATCHDOG_ACK_RETENTION_KEYS)
    assert contract["required_fields"]["ack_monotonic_counts"] == list(_WATCHDOG_ACK_COUNT_KEYS)
    assert contract["required_fields"]["ack_sticky_flags"] == list(_WATCHDOG_ACK_STICKY_KEYS)
    assert contract["required_fields"]["ack_duplicate_visibility"] == {
        key: list(value) for key, value in _WATCHDOG_ACK_DUPLICATE_FLAGS.items()
    }
    assert contract["lifecycle_semantics"]["identity_continuity_fields"] == list(
        _WATCHDOG_LIFECYCLE_KEYS
    )


def test_livepaper_observability_spec_artifacts_and_context_are_wired() -> None:
    manifest = json.loads((REPO_ROOT / "artifacts" / "proof_bundle_manifest.json").read_text())
    context = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    prompt_context = json.loads(PROMPT_CONTEXT_PATH.read_text())

    assert manifest["task_id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SPEC"
    assert manifest["status"] == "livepaper_observability_spec_ready"
    assert manifest["bundle_path"] == "artifacts/bundles/task-007-livepaper-observability-spec.tar.gz"
    assert "artifacts/reports/task-007-livepaper-observability-spec-report.md" in manifest["reports"]
    assert "artifacts/proofs/task-007-livepaper-observability-spec-check.json" in manifest["proof_files"]
    assert context["current_task"]["id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-SPEC"
    assert (
        context["current_contract"]["livepaper_observability_spec_marker"]
        == "livepaper_observability_spec"
    )
    assert (
        context["evidence"]["livepaper_observability_spec"]["preferred_next_step"]
        == "livepaper_observability_operator_runbook"
    )
    assert (
        context["next_task"]["id"] == "TASK-007-LIVEPAPER-OBSERVABILITY-OPERATOR-RUNBOOK"
    )
    assert (
        prompt_context["recommended_next_task"]
        == "TASK-007-LIVEPAPER-OBSERVABILITY-OPERATOR-RUNBOOK"
    )


def test_livepaper_observability_contract_doc_and_reports_call_out_required_contract_edges() -> None:
    spec_text = SPEC_PATH.read_text()
    report_text = REPORT_PATH.read_text()
    status_text = STATUS_PATH.read_text()

    for needle in (
        "manual_latched_stop_all",
        "snapshot_backed_terminal_detail",
        "normalized_failure_detail_passthrough",
        "quarantine_reason_completeness",
        "ack_history_retention",
    ):
        assert needle in spec_text
        assert needle in report_text

    assert "livepaper_observability_operator_runbook" in report_text
    assert "livepaper_observability_spec_ready" in status_text
    assert "TASK-007-LIVEPAPER-OBSERVABILITY-SPEC" in status_text
