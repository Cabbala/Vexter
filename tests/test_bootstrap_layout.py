import json
import tarfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_required_paths_exist() -> None:
    required_paths = [
        "README.md",
        "docs/ROLE_DEFINITION.md",
        "docs/evaluation_contract.md",
        "docs/normalized_event_schema.md",
        "docs/metrics_catalog.md",
        "docs/comparison_matrix_template.md",
        "docs/comparison_collection_runbook.md",
        "docs/windows_runtime_recovery.md",
        "docs/dexter_source_assessment.md",
        "docs/dexter_event_mapping.md",
        "docs/dexter_paper_mode_design.md",
        "docs/mewx_source_assessment.md",
        "docs/mewx_event_mapping.md",
        "specs/FIXED_WORKFLOW.md",
        "specs/ANALYSIS_CONTRACT.md",
        "ops/CODEX_MEMORY.md",
        "plans/IMPLEMENTATION_PLAN.md",
        "plans/TASK_000_BOOTSTRAP.md",
        "plans/SOURCE_ASSESSMENT_DEXTER.md",
        "plans/SOURCE_ASSESSMENT_MEWX.md",
        "plans/dexter_instrumentation_plan.md",
        "plans/mewx_instrumentation_plan.md",
        "plans/integration_readiness_plan.md",
        "manifests/reference_repos.json",
        "manifests/windows_runtime.json",
        "scripts/bootstrap_windows_workspace.sh",
        "scripts/recover_windows_runtime.sh",
        "scripts/sync_reference_repos.sh",
        "scripts/build_proof_bundle.sh",
        "scripts/comparison_analysis.py",
        "scripts/collect_comparison_package.ps1",
        "templates/windows_runtime/dexter.env.example",
        "templates/windows_runtime/mewx.env.example",
        "vexter/__init__.py",
        "vexter/comparison/__init__.py",
        "vexter/comparison/constants.py",
        "vexter/comparison/packages.py",
        "vexter/comparison/validator.py",
        "vexter/comparison/metrics.py",
        "vexter/comparison/pack.py",
        "tests/conftest.py",
        "artifacts/context_pack.json",
        "artifacts/summary.md",
        "artifacts/proof_bundle_manifest.json",
        "artifacts/task_ledger.jsonl",
        "artifacts/reports/task-005-live-collection-blocker.md",
        "artifacts/reports/task-005-windows-runtime-recovery.md",
        "artifacts/reports/dexter-paper-design-handoff/DETAILS.md",
        "artifacts/reports/dexter-paper-design-handoff/MIN_PROMPT.txt",
        "artifacts/reports/task-005-paper-validation-handoff/DETAILS.md",
        "artifacts/reports/task-005-paper-validation-handoff/MIN_PROMPT.txt",
        "artifacts/reports/task-005-pass-grade-pair-readiness.md",
        "artifacts/reports/task-005-pass-grade-pair-handoff/DETAILS.md",
        "artifacts/reports/task-005-pass-grade-pair-handoff/MIN_PROMPT.txt",
        "artifacts/proofs/task-005-live-collection-check.json",
        "artifacts/proofs/task-005-pass-grade-pair-check.json",
        "artifacts/proofs/task-005-windows-runtime-recovery.json",
        "artifacts/examples/task-004-sample-comparison/pack_manifest.json",
        ".github/workflows/validate.yml",
    ]

    for relative_path in required_paths:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_json_manifests_are_valid() -> None:
    json_paths = [
        REPO_ROOT / "manifests/reference_repos.json",
        REPO_ROOT / "manifests/windows_runtime.json",
        REPO_ROOT / "artifacts/context_pack.json",
        REPO_ROOT / "artifacts/proof_bundle_manifest.json",
    ]

    for path in json_paths:
        with path.open() as handle:
            payload = json.load(handle)
        assert payload


def test_reference_repo_manifest_has_expected_repos() -> None:
    with (REPO_ROOT / "manifests/reference_repos.json").open() as handle:
        manifest = json.load(handle)

    repo_names = {repo["name"] for repo in manifest["repos"]}
    assert repo_names == {"Dexter", "Mew-X"}


def test_windows_runtime_manifest_has_expected_shape() -> None:
    with (REPO_ROOT / "manifests/windows_runtime.json").open() as handle:
        manifest = json.load(handle)

    assert manifest["host_alias"] == "win-lan"
    assert manifest["selected_root"].endswith("Vexter")
    assert len(manifest["directories"]) >= 8
    assert manifest["analysis_layout"]["dexter"]["raw_events"].endswith("data\\raw\\dexter")
    assert manifest["analysis_layout"]["mewx"]["raw_events"].endswith("data\\raw\\mewx")
    assert manifest["runtime_prerequisites"]["cargo"]["present"] is True
    assert manifest["runtime_prerequisites"]["postgres"]["listener"] == "127.0.0.1:5432"
    assert manifest["env_injection_points"]["mewx"]["path"].endswith("sources\\Mew-X\\.env")


def test_windows_env_examples_use_parser_safe_assignments() -> None:
    mewx_example = (REPO_ROOT / "templates/windows_runtime/mewx.env.example").read_text()
    dexter_example = (REPO_ROOT / "templates/windows_runtime/dexter.env.example").read_text()

    assert 'PRIVATE_KEY="' not in mewx_example
    assert 'RPC_URL="' not in mewx_example
    assert 'WS_URL="' not in mewx_example
    assert 'DB_URL="' not in mewx_example
    assert "REGIONS=Germany,Netherlands,UnitedKingdom" in mewx_example
    assert "DB_URL=postgres://postgres:admin123@127.0.0.1:5432" in mewx_example

    assert 'PRIVATE_KEY="' not in dexter_example
    assert 'HTTP_URL="' not in dexter_example
    assert 'WS_URL="' not in dexter_example


def test_task_ledger_is_valid_jsonl() -> None:
    ledger_path = REPO_ROOT / "artifacts/task_ledger.jsonl"
    lines = ledger_path.read_text().strip().splitlines()

    assert len(lines) >= 3
    payload = json.loads(lines[-1])
    assert payload["task_id"] in {
        "TASK-005-live-comparison-evidence",
        "DEXTER-PAPER-DESIGN",
        "TASK-005-PAPER-VALIDATION",
        "TASK-005-PAPER-REVALIDATE",
        "TASK-005-PASS-GRADE-PAIR",
        "TASK-005-GAP-AUDIT",
        "TASK-005-VALIDATOR-CONTRACT-AUDIT",
        "TASK-005-VALIDATOR-RULE-REVIEW",
        "TASK-005-VALIDATOR-RULE-IMPLEMENT",
    }
    assert payload["status"] in {
        "partial_live_comparison_blocker",
        "subsecond_overlap_partial_blocker",
        "retry_collection_blocker",
        "dexter_startup_rate_limit_blocker",
        "design_complete_recommend_implement",
        "design_complete_keep_retrying",
        "paper_live_coverage_ceiling_blocker",
        "paper_live_improved_but_partial_validation",
        "pass_grade_pair_collected_but_partial_validation",
        "structural_gap_confirmed",
        "rule_review_needed_helper_fix_insufficient",
        "rule_review_memo_ready_for_approval",
        "rule_implementation_applied",
    }
    assert payload["branch"] in {
        "codex/task-005-live-comparison-evidence",
        "codex/task-005-resume-matched-window",
        "codex/task-005-pass-grade-pair",
        "codex/task-005-resume-after-pr7",
        "codex/task-005-resume-after-pr8",
        "codex/task-005-resume-after-pr9",
        "codex/dexter-paper-design",
        "codex/task-005-paper-validation",
        "codex/task-005-paper-revalidate",
        "codex/task-005-pass-grade-pair-20260326",
        "codex/task-005-gap-audit",
        "codex/task-005-validator-contract-audit",
        "codex/task-005-validator-rule-review",
        "codex/task-005-validator-rule-implement",
    }
    assert payload["next_task_id"] in {
        "TASK-005-RESUME",
        "BLOCKED",
        "DEXTER-PAPER-IMPLEMENT",
        "TASK-005-PASS-GRADE-PAIR",
        "TASK-005-VALIDATOR-RULE-IMPLEMENTATION",
        "TASK-006",
    }
    assert payload["next_task_state"] in {
        "awaiting_matched_live_window_with_full_event_coverage",
        "awaiting_nontrivial_matched_live_window_and_fuller_coverage",
        "awaiting_pass_grade_matched_live_pair",
        "awaiting_helius_recovery_and_eventful_sim_window",
        "awaiting_dexter_startup_without_helius_429",
        "ready_for_paper_implementation",
        "awaiting_dexter_paper_live_session_coverage",
        "collect_fresh_pass_grade_matched_pair",
        "awaiting_pass_grade_matched_live_pair",
        "awaiting_validator_contract_audit_or_rule_exception_review",
        "awaiting_validator_rule_review_approval",
        "awaiting_explicit_approval_to_modify_validator_rules",
        "ready_for_replay_validation",
    }


def test_proof_bundle_exists_and_contains_required_files() -> None:
    with (REPO_ROOT / "artifacts/proof_bundle_manifest.json").open() as handle:
        manifest = json.load(handle)

    assert manifest["status"] in {
        "partial_live_comparison_blocker",
        "subsecond_overlap_partial_blocker",
        "retry_collection_blocker",
        "dexter_startup_rate_limit_blocker",
        "design_complete_recommend_implement",
        "design_complete_keep_retrying",
        "paper_live_coverage_ceiling_blocker",
        "paper_live_improved_but_partial_validation",
        "pass_grade_pair_collected_but_partial_validation",
        "structural_gap_confirmed",
        "rule_review_needed",
        "rule_memo_ready",
        "rule_implementation_applied",
    }
    assert manifest["next_task"]["id"] in {
        "TASK-005-RESUME",
        "BLOCKED",
        "DEXTER-PAPER-IMPLEMENT",
        "TASK-005-PASS-GRADE-PAIR",
        "TASK-005-VALIDATOR-RULE-IMPLEMENTATION",
        "TASK-006",
    }
    assert manifest["next_task"]["state"] in {
        "awaiting_matched_live_window_with_full_event_coverage",
        "awaiting_nontrivial_matched_live_window_and_fuller_coverage",
        "awaiting_pass_grade_matched_live_pair",
        "awaiting_helius_recovery_and_eventful_sim_window",
        "awaiting_dexter_startup_without_helius_429",
        "ready_for_paper_implementation",
        "awaiting_dexter_paper_live_session_coverage",
        "collect_fresh_pass_grade_matched_pair",
        "awaiting_validator_contract_audit_or_rule_exception_review",
        "awaiting_validator_rule_review_approval",
        "awaiting_explicit_approval_to_modify_validator_rules",
        "ready_for_replay_validation",
    }

    bundle_path = REPO_ROOT / manifest["bundle_path"]
    assert bundle_path.exists()

    with tarfile.open(bundle_path, "r:gz") as bundle:
        names = set(bundle.getnames())

    assert "README.md" in names
    assert "docs/evaluation_contract.md" in names
    assert "docs/normalized_event_schema.md" in names
    assert "docs/comparison_collection_runbook.md" in names
    assert "docs/windows_runtime_recovery.md" in names
    assert "docs/dexter_event_mapping.md" in names
    assert "docs/dexter_paper_mode_design.md" in names
    assert "docs/mewx_event_mapping.md" in names
    assert "scripts/comparison_analysis.py" in names
    assert "scripts/collect_comparison_package.ps1" in names
    assert "scripts/recover_windows_runtime.sh" in names
    assert "templates/windows_runtime/dexter.env.example" in names
    assert "templates/windows_runtime/mewx.env.example" in names
    assert "vexter/comparison/validator.py" in names
    assert "artifacts/examples/task-004-sample-comparison/summary.md" in names
    assert "artifacts/reports/task-005-live-collection-blocker.md" in names
    assert "artifacts/reports/task-005-windows-runtime-recovery.md" in names
    assert "artifacts/reports/dexter-paper-design-handoff/DETAILS.md" in names
    assert "artifacts/reports/dexter-paper-design-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-005-paper-validation-handoff/DETAILS.md" in names
    assert "artifacts/reports/task-005-paper-validation-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/proofs/task-005-live-collection-check.json" in names
    assert "artifacts/proofs/task-005-windows-runtime-recovery.json" in names
    assert "artifacts/context_pack.json" in names
    assert "artifacts/proof_bundle_manifest.json" in names
    assert "tests/__pycache__/" not in names
