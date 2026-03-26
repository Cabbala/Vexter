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
        "config/planner_router/planner.json",
        "config/planner_router/objective_profiles.json",
        "config/planner_router/sleeves.json",
        "config/planner_router/budget_policies.json",
        "config/planner_router/monitor_profiles.json",
        "config/planner_router/executor_profiles.json",
        "vexter/__init__.py",
        "vexter/comparison/__init__.py",
        "vexter/comparison/constants.py",
        "vexter/comparison/packages.py",
        "vexter/comparison/validator.py",
        "vexter/comparison/metrics.py",
        "vexter/comparison/pack.py",
        "vexter/comparison/replay_deepening.py",
        "vexter/comparison/replay_surface_fix.py",
        "vexter/planner_router/__init__.py",
        "vexter/planner_router/models.py",
        "vexter/planner_router/errors.py",
        "vexter/planner_router/interfaces.py",
        "vexter/planner_router/config_loader.py",
        "vexter/planner_router/objective_resolver.py",
        "vexter/planner_router/sleeve_selector.py",
        "vexter/planner_router/budget_binder.py",
        "vexter/planner_router/plan_emitter.py",
        "vexter/planner_router/dispatch_state_machine.py",
        "vexter/planner_router/planner.py",
        "vexter/planner_router/transport.py",
        "tests/conftest.py",
        "tests/test_planner_router_config_loader.py",
        "tests/test_planner_router_objective_resolver.py",
        "tests/test_planner_router_plan_emitter.py",
        "tests/test_planner_router_dispatch_state_machine.py",
        "tests/test_monitor_killswitch_spec_contract.py",
        "tests/test_planner_router_livepaper_smoke.py",
        "tests/test_planner_router_executor_transport_spec_contract.py",
        "tests/test_planner_router_executor_transport_implementation.py",
        "tests/test_planner_router_transport.py",
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
        "artifacts/reports/task-006-replay-validation.md",
        "artifacts/reports/task-006-replay-validation-status.md",
        "artifacts/reports/task-006-replay-validation-handoff/DETAILS.md",
        "artifacts/reports/task-006-replay-validation-handoff/MIN_PROMPT.txt",
        "artifacts/reports/task-006-replay-deepening.md",
        "artifacts/reports/task-006-replay-deepening-handoff/DETAILS.md",
        "artifacts/reports/task-006-replay-deepening-handoff/MIN_PROMPT.txt",
        "artifacts/reports/task-006-replay-analysis.md",
        "artifacts/reports/task-006-replay-analysis-handoff/DETAILS.md",
        "artifacts/reports/task-006-replay-analysis-handoff/MIN_PROMPT.txt",
        "artifacts/reports/task-006-replay-surface-fix.md",
        "artifacts/reports/task-006-replay-surface-fix-handoff/DETAILS.md",
        "artifacts/reports/task-006-replay-surface-fix-handoff/MIN_PROMPT.txt",
        "artifacts/reports/task-006-downstream-comparative-analysis.md",
        "artifacts/reports/task-006-downstream-comparative-analysis-handoff/DETAILS.md",
        "artifacts/reports/task-006-downstream-comparative-analysis-handoff/MIN_PROMPT.txt",
        "artifacts/reports/task-006-comparison-closeout.md",
        "artifacts/reports/task-006-comparison-closeout-handoff/DETAILS.md",
        "artifacts/reports/task-006-comparison-closeout-handoff/MIN_PROMPT.txt",
        "artifacts/reports/task-006-research-handoff-report.md",
        "artifacts/reports/task-006-research-handoff-status.md",
        "artifacts/reports/task-006-research-handoff/DETAILS.md",
        "artifacts/reports/task-006-research-handoff/MIN_PROMPT.txt",
        "artifacts/reports/task-007-candidate-generation-vs-quality-report.md",
        "artifacts/reports/task-007-candidate-generation-vs-quality-status.md",
        "artifacts/reports/task-007-candidate-generation-vs-quality/DETAILS.md",
        "artifacts/reports/task-007-candidate-generation-vs-quality/MIN_PROMPT.txt",
        "artifacts/reports/task-007-execution-timing-vs-retention-report.md",
        "artifacts/reports/task-007-execution-timing-vs-retention-status.md",
        "artifacts/reports/task-007-execution-timing-vs-retention/DETAILS.md",
        "artifacts/reports/task-007-execution-timing-vs-retention/MIN_PROMPT.txt",
        "artifacts/reports/task-007-risk-containment-vs-exit-capture-report.md",
        "artifacts/reports/task-007-risk-containment-vs-exit-capture-status.md",
        "artifacts/reports/task-007-risk-containment-vs-exit-capture/DETAILS.md",
        "artifacts/reports/task-007-risk-containment-vs-exit-capture/MIN_PROMPT.txt",
        "artifacts/reports/task-007-strategy-planning-report.md",
        "artifacts/reports/task-007-strategy-planning-status.md",
        "artifacts/reports/task-007-strategy-planning/DETAILS.md",
        "artifacts/reports/task-007-strategy-planning/MIN_PROMPT.txt",
        "artifacts/reports/task-007-execution-planning-report.md",
        "artifacts/reports/task-007-execution-planning-status.md",
        "artifacts/reports/task-007-execution-planning/DETAILS.md",
        "artifacts/reports/task-007-execution-planning/MIN_PROMPT.txt",
        "artifacts/reports/task-007-implementation-planning-report.md",
        "artifacts/reports/task-007-implementation-planning-status.md",
        "artifacts/reports/task-007-implementation-planning/DETAILS.md",
        "artifacts/reports/task-007-implementation-planning/MIN_PROMPT.txt",
        "artifacts/reports/task-007-planner-router-interface-spec-report.md",
        "artifacts/reports/task-007-planner-router-interface-spec-status.md",
        "artifacts/reports/task-007-planner-router-interface-spec/DETAILS.md",
        "artifacts/reports/task-007-planner-router-interface-spec/MIN_PROMPT.txt",
        "artifacts/reports/task-007-concrete-planner-router-implementation-spec-report.md",
        "artifacts/reports/task-007-concrete-planner-router-implementation-spec-status.md",
        "artifacts/reports/task-007-concrete-planner-router-implementation-spec/DETAILS.md",
        "artifacts/reports/task-007-concrete-planner-router-implementation-spec/MIN_PROMPT.txt",
        "artifacts/reports/task-007-planner-router-code-implementation-report.md",
        "artifacts/reports/task-007-planner-router-code-implementation-status.md",
        "artifacts/reports/task-007-planner-router-code-implementation/DETAILS.md",
        "artifacts/reports/task-007-planner-router-code-implementation/MIN_PROMPT.txt",
        "artifacts/reports/task-007-planner-router-integration-smoke-report.md",
        "artifacts/reports/task-007-planner-router-integration-smoke-status.md",
        "artifacts/reports/task-007-planner-router-integration-smoke/DETAILS.md",
        "artifacts/reports/task-007-planner-router-integration-smoke/MIN_PROMPT.txt",
        "artifacts/reports/task-007-monitor-killswitch-spec-report.md",
        "artifacts/reports/task-007-monitor-killswitch-spec-status.md",
        "artifacts/reports/task-007-monitor-killswitch-spec/DETAILS.md",
        "artifacts/reports/task-007-monitor-killswitch-spec/MIN_PROMPT.txt",
        "artifacts/reports/task-007-monitor-killswitch-spec/CONTEXT.json",
        "artifacts/reports/task-007-planner-router-livepaper-smoke-report.md",
        "artifacts/reports/task-007-planner-router-livepaper-smoke-status.md",
        "artifacts/reports/task-007-planner-router-livepaper-smoke/DETAILS.md",
        "artifacts/reports/task-007-planner-router-livepaper-smoke/MIN_PROMPT.txt",
        "artifacts/reports/task-007-planner-router-livepaper-smoke/CONTEXT.json",
        "artifacts/reports/task-007-planner-router-executor-transport-spec-report.md",
        "artifacts/reports/task-007-planner-router-executor-transport-spec-status.md",
        "artifacts/reports/task-007-planner-router-executor-transport-spec/DETAILS.md",
        "artifacts/reports/task-007-planner-router-executor-transport-spec/MIN_PROMPT.txt",
        "artifacts/reports/task-007-planner-router-executor-transport-spec/CONTEXT.json",
        "artifacts/reports/task-007-planner-router-executor-transport-implementation-report.md",
        "artifacts/reports/task-007-planner-router-executor-transport-implementation-status.md",
        "artifacts/reports/task-007-planner-router-executor-transport-implementation/DETAILS.md",
        "artifacts/reports/task-007-planner-router-executor-transport-implementation/MIN_PROMPT.txt",
        "artifacts/reports/task-007-planner-router-executor-transport-implementation/CONTEXT.json",
        "artifacts/reports/task-007-transport-runtime-smoke-report.md",
        "artifacts/reports/task-007-transport-runtime-smoke-status.md",
        "artifacts/reports/task-007-transport-runtime-smoke/DETAILS.md",
        "artifacts/reports/task-007-transport-runtime-smoke/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-runtime-smoke/CONTEXT.json",
        "artifacts/reports/task-007-transport-livepaper-smoke-report.md",
        "artifacts/reports/task-007-transport-livepaper-smoke-status.md",
        "artifacts/reports/task-007-transport-livepaper-smoke/DETAILS.md",
        "artifacts/reports/task-007-transport-livepaper-smoke/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-livepaper-smoke/CONTEXT.json",
        "artifacts/reports/task-007-transport-livepaper-observability-smoke-report.md",
        "artifacts/reports/task-007-transport-livepaper-observability-smoke-status.md",
        "artifacts/reports/task-007-transport-livepaper-observability-smoke/DETAILS.md",
        "artifacts/reports/task-007-transport-livepaper-observability-smoke/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-livepaper-observability-smoke/CONTEXT.json",
        "artifacts/proofs/task-005-live-collection-check.json",
        "artifacts/proofs/task-005-pass-grade-pair-check.json",
        "artifacts/proofs/task-005-windows-runtime-recovery.json",
        "artifacts/proofs/task-006-replay-validation-check.json",
        "artifacts/proofs/task-006-replay-deepening-check.json",
        "artifacts/proofs/task-006-replay-deepening-summary.md",
        "artifacts/proofs/task-006-replay-analysis-check.json",
        "artifacts/proofs/task-006-replay-analysis-summary.md",
        "artifacts/proofs/task-006-replay-surface-fix-check.json",
        "artifacts/proofs/task-006-replay-surface-fix-summary.md",
        "artifacts/proofs/task-006-downstream-comparative-analysis-check.json",
        "artifacts/proofs/task-006-downstream-comparative-analysis-summary.md",
        "artifacts/proofs/task-006-comparison-closeout-check.json",
        "artifacts/proofs/task-006-comparison-closeout-summary.md",
        "artifacts/proofs/task-006-research-handoff-check.json",
        "artifacts/proofs/task-006-research-handoff-summary.md",
        "artifacts/proofs/task-007-candidate-generation-vs-quality-check.json",
        "artifacts/proofs/task-007-candidate-generation-vs-quality-summary.md",
        "artifacts/proofs/task-007-execution-timing-vs-retention-check.json",
        "artifacts/proofs/task-007-execution-timing-vs-retention-summary.md",
        "artifacts/proofs/task-007-risk-containment-vs-exit-capture-check.json",
        "artifacts/proofs/task-007-risk-containment-vs-exit-capture-summary.md",
        "artifacts/proofs/task-007-strategy-planning-check.json",
        "artifacts/proofs/task-007-strategy-planning-summary.md",
        "artifacts/proofs/task-007-execution-planning-check.json",
        "artifacts/proofs/task-007-execution-planning-summary.md",
        "artifacts/proofs/task-007-implementation-planning-check.json",
        "artifacts/proofs/task-007-implementation-planning-summary.md",
        "artifacts/proofs/task-007-planner-router-interface-spec-check.json",
        "artifacts/proofs/task-007-planner-router-interface-spec-summary.md",
        "artifacts/proofs/task-007-concrete-planner-router-implementation-spec-check.json",
        "artifacts/proofs/task-007-concrete-planner-router-implementation-spec-summary.md",
        "artifacts/proofs/task-007-planner-router-code-implementation-check.json",
        "artifacts/proofs/task-007-planner-router-code-implementation-summary.md",
        "artifacts/proofs/task-007-planner-router-integration-smoke-check.json",
        "artifacts/proofs/task-007-planner-router-integration-smoke-summary.md",
        "artifacts/proofs/task-007-monitor-killswitch-spec-check.json",
        "artifacts/proofs/task-007-monitor-killswitch-spec-summary.md",
        "artifacts/proofs/task-007-planner-router-livepaper-smoke-check.json",
        "artifacts/proofs/task-007-planner-router-livepaper-smoke-summary.md",
        "artifacts/proofs/task-007-planner-router-executor-transport-spec-check.json",
        "artifacts/proofs/task-007-planner-router-executor-transport-spec-summary.md",
        "artifacts/proofs/task-007-planner-router-executor-transport-implementation-check.json",
        "artifacts/proofs/task-007-planner-router-executor-transport-implementation-summary.md",
        "artifacts/proofs/task-007-transport-runtime-smoke-check.json",
        "artifacts/proofs/task-007-transport-runtime-smoke-summary.md",
        "artifacts/proofs/task-007-transport-livepaper-smoke-check.json",
        "artifacts/proofs/task-007-transport-livepaper-smoke-summary.md",
        "artifacts/proofs/task-007-transport-livepaper-observability-smoke-check.json",
        "artifacts/proofs/task-007-transport-livepaper-observability-smoke-summary.md",
        "artifacts/bundles/task-007-planner-router-code-implementation.tar.gz",
        "artifacts/bundles/task-007-planner-router-integration-smoke.tar.gz",
        "artifacts/bundles/task-007-monitor-killswitch-spec.tar.gz",
        "artifacts/bundles/task-007-planner-router-livepaper-smoke.tar.gz",
        "artifacts/bundles/task-007-planner-router-executor-transport-spec.tar.gz",
        "artifacts/bundles/task-007-planner-router-executor-transport-implementation.tar.gz",
        "artifacts/bundles/task-007-transport-runtime-smoke.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-smoke.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-observability-smoke.tar.gz",
        "tests/test_planner_router_transport_livepaper_observability_smoke.py",
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
        "TASK-006-REPLAY-VALIDATION",
        "TASK-006-REPLAY-DEEPENING",
        "TASK-006-REPLAY-ANALYSIS",
        "TASK-006-REPLAY-SURFACE-FIX",
        "TASK-006-DOWNSTREAM-COMPARATIVE-ANALYSIS",
        "TASK-006-COMPARISON-CLOSEOUT",
        "TASK-006-RESEARCH-HANDOFF",
        "TASK-007-DOWNSTREAM-RESEARCH-INTAKE",
        "TASK-007-CANDIDATE-GENERATION-VS-QUALITY",
        "TASK-007-EXECUTION-TIMING-VS-RETENTION",
        "TASK-007-RISK-CONTAINMENT-VS-EXIT-CAPTURE",
        "TASK-007-STRATEGY-PLANNING",
        "TASK-007-EXECUTION-PLANNING",
        "TASK-007-IMPLEMENTATION-PLANNING",
        "TASK-007-PLANNER-ROUTER-INTERFACE-SPEC",
        "TASK-007-CONCRETE-PLANNER-ROUTER-IMPLEMENTATION-SPEC",
        "TASK-007-CONCRETE-PLANNER-ROUTER-CODE-SPEC",
        "TASK-007-PLANNER-ROUTER-CODE-IMPLEMENTATION",
        "TASK-007-PLANNER-ROUTER-INTEGRATION-SMOKE",
        "TASK-007-PLANNER-ROUTER-RUNTIME-SMOKE",
        "TASK-007-MONITOR-KILLSWITCH-SPEC",
        "TASK-007-PLANNER-ROUTER-LIVEPAPER-SMOKE",
        "TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-SPEC",
        "TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-IMPLEMENTATION",
        "TASK-007-TRANSPORT-RUNTIME-SMOKE",
        "TASK-007-TRANSPORT-LIVEPAPER-SMOKE",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-SMOKE",
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
        "replay_validation_in_progress",
        "replay_gap_measured",
        "needs_replay_surface_fix",
        "surface_fix_applied",
        "comparison_closeout_ready",
        "comparison_closed_out",
        "research_handoff_completed",
        "research_intake_ready",
        "candidate_edge_supported",
        "timing_retention_tradeoff_supported",
        "risk_exit_tradeoff_supported",
        "strategy_plan_ready",
        "execution_plan_ready",
        "implementation_plan_ready",
        "planner_router_spec_ready",
        "concrete_planner_router_spec_ready",
        "planner_router_code_spec_ready",
        "planner_router_code_implemented",
        "planner_router_integration_smoke_passed",
        "planner_router_runtime_smoke_passed",
        "monitor_killswitch_spec_ready",
        "planner_router_livepaper_smoke_passed",
        "planner_router_executor_transport_spec_ready",
        "planner_router_executor_transport_implemented",
        "transport_runtime_smoke_passed",
        "transport_livepaper_smoke_passed",
        "transport_livepaper_observability_smoke_passed",
        "handoff_blocked",
        "intake_blocked",
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
        "codex/task-006-replay-validation",
        "codex/task-006-replay-deepening",
        "codex/task-006-replay-analysis",
        "codex/task-006-replay-surface-fix",
        "codex/task-006-downstream-comparative-analysis",
        "codex/task-006-comparison-closeout",
        "codex/task-006-research-handoff",
        "codex/task-007-downstream-research-intake",
        "codex/task-007-candidate-generation-vs-quality",
        "codex/task-007-execution-timing-vs-retention",
        "codex/task-007-risk-containment-vs-exit-capture",
        "codex/task-007-strategy-planning",
        "codex/task-007-execution-planning",
        "codex/task-007-implementation-planning",
        "codex/task-007-planner-router-interface-spec",
        "codex/task-007-concrete-planner-router-implementation-spec",
        "codex/task-007-concrete-planner-router-code-spec",
        "codex/task-007-planner-router-code-implementation",
        "codex/task-007-planner-router-integration-smoke",
        "codex/task-007-planner-router-runtime-smoke",
        "codex/task-007-monitor-killswitch-spec",
        "codex/task-007-planner-router-livepaper-smoke",
        "codex/task-007-planner-router-executor-transport-spec",
        "codex/task-007-planner-router-executor-transport-implementation",
        "codex/task-007-transport-runtime-smoke",
        "codex/task-007-transport-livepaper-smoke",
        "codex/task-007-transport-livepaper-observability-smoke",
    }
    assert payload["next_task_id"] in {
        "TASK-005-RESUME",
        "BLOCKED",
        "DEXTER-PAPER-IMPLEMENT",
        "TASK-005-PASS-GRADE-PAIR",
        "TASK-005-VALIDATOR-RULE-IMPLEMENTATION",
        "TASK-006",
        "RESEARCH-HANDOFF",
        "DOWNSTREAM-RESEARCH",
        "HYPOTHESIS-RESEARCH",
        "STRATEGY-PLANNING",
        "EXECUTION-PLANNING",
        "IMPLEMENTATION-PLANNING",
        "PLANNER-ROUTER-INTERFACE-SPEC",
        "CONCRETE-PLANNER-ROUTER-IMPLEMENTATION-SPEC",
        "CONCRETE-PLANNER-ROUTER-CODE-SPEC",
        "TASK-007-PLANNER-ROUTER-CODE-IMPLEMENTATION",
        "TASK-007-PLANNER-ROUTER-INTEGRATION-SMOKE",
        "TASK-007-PLANNER-ROUTER-RUNTIME-SMOKE",
        "TASK-007-MONITOR-KILLSWITCH-SPEC",
        "TASK-007-PLANNER-ROUTER-LIVEPAPER-SMOKE",
        "TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-SPEC",
        "TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-IMPLEMENTATION",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SPEC",
        "TASK-007-EXECUTOR-BOUNDARY-CODE-SPEC",
        "TASK-007-TRANSPORT-RUNTIME-SMOKE",
        "TASK-007-TRANSPORT-LIVEPAPER-SMOKE",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-SMOKE",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-RUNTIME",
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
        "replay_validation_in_progress",
        "ready_for_next_replay_analysis_step",
        "needs_replay_surface_fix",
        "ready_for_downstream_comparative_analysis",
        "comparison_closeout_ready",
        "research_handoff_ready",
        "ready_to_start_from_handoff",
        "ready_for_hypothesis_specific_research",
        "ready_for_objective_weighted_strategy_planning",
        "ready_for_execution_planning",
        "ready_for_implementation_planning",
        "ready_for_planner_router_interface_spec",
        "ready_for_concrete_planner_router_implementation_spec",
        "ready_for_concrete_planner_router_code_spec",
        "ready_for_planner_router_code_implementation",
        "ready_for_planner_router_integration_smoke",
        "ready_for_planner_router_runtime_smoke",
        "ready_for_monitor_killswitch_spec",
        "ready_for_planner_router_livepaper_smoke",
        "ready_for_planner_router_executor_transport_spec",
        "ready_for_planner_router_executor_transport_implementation",
        "ready_for_livepaper_observability_spec",
        "ready_for_executor_boundary_code_spec",
        "ready_for_transport_runtime_smoke",
        "ready_for_transport_livepaper_smoke",
        "ready_for_transport_livepaper_observability_smoke",
        "ready_for_transport_livepaper_observability_runtime",
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
        "replay_validation_in_progress",
        "replay_gap_measured",
        "needs_replay_surface_fix",
        "surface_fix_applied",
        "comparison_closeout_ready",
        "comparison_closed_out",
        "research_handoff_completed",
        "research_intake_ready",
        "candidate_edge_supported",
        "timing_retention_tradeoff_supported",
        "risk_exit_tradeoff_supported",
        "strategy_plan_ready",
        "execution_plan_ready",
        "implementation_plan_ready",
        "planner_router_spec_ready",
        "concrete_planner_router_spec_ready",
        "planner_router_code_spec_ready",
        "planner_router_code_implemented",
        "planner_router_integration_smoke_passed",
        "planner_router_runtime_smoke_passed",
        "monitor_killswitch_spec_ready",
        "planner_router_livepaper_smoke_passed",
        "planner_router_executor_transport_spec_ready",
        "planner_router_executor_transport_implemented",
        "transport_runtime_smoke_passed",
        "transport_livepaper_smoke_passed",
        "transport_livepaper_observability_smoke_passed",
        "handoff_blocked",
        "intake_blocked",
    }
    assert manifest["next_task"]["id"] in {
        "TASK-005-RESUME",
        "BLOCKED",
        "DEXTER-PAPER-IMPLEMENT",
        "TASK-005-PASS-GRADE-PAIR",
        "TASK-005-VALIDATOR-RULE-IMPLEMENTATION",
        "TASK-006",
        "RESEARCH-HANDOFF",
        "DOWNSTREAM-RESEARCH",
        "HYPOTHESIS-RESEARCH",
        "STRATEGY-PLANNING",
        "EXECUTION-PLANNING",
        "IMPLEMENTATION-PLANNING",
        "PLANNER-ROUTER-INTERFACE-SPEC",
        "CONCRETE-PLANNER-ROUTER-IMPLEMENTATION-SPEC",
        "CONCRETE-PLANNER-ROUTER-CODE-SPEC",
        "TASK-007-PLANNER-ROUTER-CODE-IMPLEMENTATION",
        "TASK-007-PLANNER-ROUTER-INTEGRATION-SMOKE",
        "TASK-007-PLANNER-ROUTER-RUNTIME-SMOKE",
        "TASK-007-MONITOR-KILLSWITCH-SPEC",
        "TASK-007-PLANNER-ROUTER-LIVEPAPER-SMOKE",
        "TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-SPEC",
        "TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-IMPLEMENTATION",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SPEC",
        "TASK-007-EXECUTOR-BOUNDARY-CODE-SPEC",
        "TASK-007-TRANSPORT-RUNTIME-SMOKE",
        "TASK-007-TRANSPORT-LIVEPAPER-SMOKE",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-SMOKE",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-RUNTIME",
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
        "replay_validation_in_progress",
        "ready_for_next_replay_analysis_step",
        "needs_replay_surface_fix",
        "ready_for_downstream_comparative_analysis",
        "comparison_closeout_ready",
        "research_handoff_ready",
        "ready_to_start_from_handoff",
        "ready_for_hypothesis_specific_research",
        "ready_for_objective_weighted_strategy_planning",
        "ready_for_execution_planning",
        "ready_for_implementation_planning",
        "ready_for_planner_router_interface_spec",
        "ready_for_concrete_planner_router_implementation_spec",
        "ready_for_concrete_planner_router_code_spec",
        "ready_for_planner_router_code_implementation",
        "ready_for_planner_router_integration_smoke",
        "ready_for_planner_router_runtime_smoke",
        "ready_for_monitor_killswitch_spec",
        "ready_for_planner_router_livepaper_smoke",
        "ready_for_planner_router_executor_transport_spec",
        "ready_for_planner_router_executor_transport_implementation",
        "ready_for_livepaper_observability_spec",
        "ready_for_executor_boundary_code_spec",
        "ready_for_transport_runtime_smoke",
        "ready_for_transport_livepaper_smoke",
        "ready_for_transport_livepaper_observability_smoke",
        "ready_for_transport_livepaper_observability_runtime",
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
    assert "vexter/comparison/replay_deepening.py" in names
    assert "vexter/comparison/replay_surface_fix.py" in names
    assert "vexter/planner_router/planner.py" in names
    assert "config/planner_router/planner.json" in names
    assert "artifacts/examples/task-004-sample-comparison/summary.md" in names
    assert "artifacts/reports/task-005-live-collection-blocker.md" in names
    assert "artifacts/reports/task-005-windows-runtime-recovery.md" in names
    assert "artifacts/reports/dexter-paper-design-handoff/DETAILS.md" in names
    assert "artifacts/reports/dexter-paper-design-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-005-paper-validation-handoff/DETAILS.md" in names
    assert "artifacts/reports/task-005-paper-validation-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-006-replay-validation.md" in names
    assert "artifacts/reports/task-006-replay-validation-status.md" in names
    assert "artifacts/reports/task-006-replay-validation-handoff/DETAILS.md" in names
    assert "artifacts/reports/task-006-replay-validation-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-006-replay-deepening.md" in names
    assert "artifacts/reports/task-006-replay-deepening-handoff/DETAILS.md" in names
    assert "artifacts/reports/task-006-replay-deepening-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-006-replay-analysis.md" in names
    assert "artifacts/reports/task-006-replay-analysis-handoff/DETAILS.md" in names
    assert "artifacts/reports/task-006-replay-analysis-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-006-replay-surface-fix.md" in names
    assert "artifacts/reports/task-006-replay-surface-fix-handoff/DETAILS.md" in names
    assert "artifacts/reports/task-006-replay-surface-fix-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-006-downstream-comparative-analysis.md" in names
    assert "artifacts/reports/task-006-downstream-comparative-analysis-handoff/DETAILS.md" in names
    assert "artifacts/reports/task-006-downstream-comparative-analysis-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-006-comparison-closeout.md" in names
    assert "artifacts/reports/task-006-comparison-closeout-handoff/DETAILS.md" in names
    assert "artifacts/reports/task-006-comparison-closeout-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-006-research-handoff-report.md" in names
    assert "artifacts/reports/task-006-research-handoff-status.md" in names
    assert "artifacts/reports/task-006-research-handoff/DETAILS.md" in names
    assert "artifacts/reports/task-006-research-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-downstream-research-intake-report.md" in names
    assert "artifacts/reports/task-007-downstream-research-intake-status.md" in names
    assert "artifacts/reports/task-007-downstream-research-intake/DETAILS.md" in names
    assert "artifacts/reports/task-007-downstream-research-intake/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-candidate-generation-vs-quality-report.md" in names
    assert "artifacts/reports/task-007-candidate-generation-vs-quality-status.md" in names
    assert "artifacts/reports/task-007-candidate-generation-vs-quality/DETAILS.md" in names
    assert "artifacts/reports/task-007-candidate-generation-vs-quality/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-execution-timing-vs-retention-report.md" in names
    assert "artifacts/reports/task-007-execution-timing-vs-retention-status.md" in names
    assert "artifacts/reports/task-007-execution-timing-vs-retention/DETAILS.md" in names
    assert "artifacts/reports/task-007-execution-timing-vs-retention/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-risk-containment-vs-exit-capture-report.md" in names
    assert "artifacts/reports/task-007-risk-containment-vs-exit-capture-status.md" in names
    assert "artifacts/reports/task-007-risk-containment-vs-exit-capture/DETAILS.md" in names
    assert "artifacts/reports/task-007-risk-containment-vs-exit-capture/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-strategy-planning-report.md" in names
    assert "artifacts/reports/task-007-strategy-planning-status.md" in names
    assert "artifacts/reports/task-007-strategy-planning/DETAILS.md" in names
    assert "artifacts/reports/task-007-strategy-planning/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-execution-planning-report.md" in names
    assert "artifacts/reports/task-007-execution-planning-status.md" in names
    assert "artifacts/reports/task-007-execution-planning/DETAILS.md" in names
    assert "artifacts/reports/task-007-execution-planning/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-implementation-planning-report.md" in names
    assert "artifacts/reports/task-007-implementation-planning-status.md" in names
    assert "artifacts/reports/task-007-implementation-planning/DETAILS.md" in names
    assert "artifacts/reports/task-007-implementation-planning/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-planner-router-interface-spec-report.md" in names
    assert "artifacts/reports/task-007-planner-router-interface-spec-status.md" in names
    assert "artifacts/reports/task-007-planner-router-interface-spec/DETAILS.md" in names
    assert "artifacts/reports/task-007-planner-router-interface-spec/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-concrete-planner-router-implementation-spec-report.md" in names
    assert "artifacts/reports/task-007-concrete-planner-router-implementation-spec-status.md" in names
    assert "artifacts/reports/task-007-concrete-planner-router-implementation-spec/DETAILS.md" in names
    assert "artifacts/reports/task-007-concrete-planner-router-implementation-spec/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-planner-router-code-implementation-report.md" in names
    assert "artifacts/reports/task-007-planner-router-code-implementation-status.md" in names
    assert "artifacts/reports/task-007-planner-router-code-implementation/DETAILS.md" in names
    assert "artifacts/reports/task-007-planner-router-code-implementation/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-planner-router-integration-smoke-report.md" in names
    assert "artifacts/reports/task-007-planner-router-integration-smoke-status.md" in names
    assert "artifacts/reports/task-007-planner-router-integration-smoke/DETAILS.md" in names
    assert "artifacts/reports/task-007-planner-router-integration-smoke/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-monitor-killswitch-spec-report.md" in names
    assert "artifacts/reports/task-007-monitor-killswitch-spec-status.md" in names
    assert "artifacts/reports/task-007-monitor-killswitch-spec/DETAILS.md" in names
    assert "artifacts/reports/task-007-monitor-killswitch-spec/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-monitor-killswitch-spec/CONTEXT.json" in names
    assert "artifacts/reports/task-007-planner-router-livepaper-smoke-report.md" in names
    assert "artifacts/reports/task-007-planner-router-livepaper-smoke-status.md" in names
    assert "artifacts/reports/task-007-planner-router-livepaper-smoke/DETAILS.md" in names
    assert "artifacts/reports/task-007-planner-router-livepaper-smoke/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-planner-router-livepaper-smoke/CONTEXT.json" in names
    assert "artifacts/reports/task-007-planner-router-executor-transport-spec-report.md" in names
    assert "artifacts/reports/task-007-planner-router-executor-transport-spec-status.md" in names
    assert "artifacts/reports/task-007-planner-router-executor-transport-spec/DETAILS.md" in names
    assert "artifacts/reports/task-007-planner-router-executor-transport-spec/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-planner-router-executor-transport-spec/CONTEXT.json" in names
    assert "artifacts/reports/task-007-planner-router-executor-transport-implementation-report.md" in names
    assert "artifacts/reports/task-007-planner-router-executor-transport-implementation-status.md" in names
    assert "artifacts/reports/task-007-planner-router-executor-transport-implementation/DETAILS.md" in names
    assert "artifacts/reports/task-007-planner-router-executor-transport-implementation/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-planner-router-executor-transport-implementation/CONTEXT.json" in names
    assert "artifacts/reports/task-007-transport-runtime-smoke-report.md" in names
    assert "artifacts/reports/task-007-transport-runtime-smoke-status.md" in names
    assert "artifacts/reports/task-007-transport-runtime-smoke/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-runtime-smoke/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-runtime-smoke/CONTEXT.json" in names
    assert "artifacts/reports/task-007-transport-livepaper-smoke-report.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-smoke-status.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-smoke/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-smoke/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-livepaper-smoke/CONTEXT.json" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-smoke-report.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-smoke-status.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-smoke/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-smoke/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-smoke/CONTEXT.json" in names
    assert "artifacts/proofs/task-005-live-collection-check.json" in names
    assert "artifacts/proofs/task-005-windows-runtime-recovery.json" in names
    assert "artifacts/proofs/task-006-replay-validation-check.json" in names
    assert "artifacts/proofs/task-006-replay-deepening-check.json" in names
    assert "artifacts/proofs/task-006-replay-deepening-summary.md" in names
    assert "artifacts/proofs/task-006-replay-analysis-check.json" in names
    assert "artifacts/proofs/task-006-replay-analysis-summary.md" in names
    assert "artifacts/proofs/task-006-replay-surface-fix-check.json" in names
    assert "artifacts/proofs/task-006-replay-surface-fix-summary.md" in names
    assert "artifacts/proofs/task-006-downstream-comparative-analysis-check.json" in names
    assert "artifacts/proofs/task-006-downstream-comparative-analysis-summary.md" in names
    assert "artifacts/proofs/task-006-comparison-closeout-check.json" in names
    assert "artifacts/proofs/task-006-comparison-closeout-summary.md" in names
    assert "artifacts/proofs/task-006-research-handoff-check.json" in names
    assert "artifacts/proofs/task-006-research-handoff-summary.md" in names
    assert "artifacts/proofs/task-007-downstream-research-intake-check.json" in names
    assert "artifacts/proofs/task-007-downstream-research-intake-summary.md" in names
    assert "artifacts/proofs/task-007-candidate-generation-vs-quality-check.json" in names
    assert "artifacts/proofs/task-007-candidate-generation-vs-quality-summary.md" in names
    assert "artifacts/proofs/task-007-execution-timing-vs-retention-check.json" in names
    assert "artifacts/proofs/task-007-execution-timing-vs-retention-summary.md" in names
    assert "artifacts/proofs/task-007-risk-containment-vs-exit-capture-check.json" in names
    assert "artifacts/proofs/task-007-risk-containment-vs-exit-capture-summary.md" in names
    assert "artifacts/proofs/task-007-strategy-planning-check.json" in names
    assert "artifacts/proofs/task-007-strategy-planning-summary.md" in names
    assert "artifacts/proofs/task-007-execution-planning-check.json" in names
    assert "artifacts/proofs/task-007-execution-planning-summary.md" in names
    assert "artifacts/proofs/task-007-implementation-planning-check.json" in names
    assert "artifacts/proofs/task-007-implementation-planning-summary.md" in names
    assert "artifacts/proofs/task-007-planner-router-interface-spec-check.json" in names
    assert "artifacts/proofs/task-007-planner-router-interface-spec-summary.md" in names
    assert "artifacts/proofs/task-007-concrete-planner-router-implementation-spec-check.json" in names
    assert "artifacts/proofs/task-007-concrete-planner-router-implementation-spec-summary.md" in names
    assert "artifacts/proofs/task-007-planner-router-code-implementation-check.json" in names
    assert "artifacts/proofs/task-007-planner-router-code-implementation-summary.md" in names
    assert "artifacts/proofs/task-007-planner-router-integration-smoke-check.json" in names
    assert "artifacts/proofs/task-007-planner-router-integration-smoke-summary.md" in names
    assert "artifacts/proofs/task-007-monitor-killswitch-spec-check.json" in names
    assert "artifacts/proofs/task-007-monitor-killswitch-spec-summary.md" in names
    assert "artifacts/proofs/task-007-planner-router-livepaper-smoke-check.json" in names
    assert "artifacts/proofs/task-007-planner-router-livepaper-smoke-summary.md" in names
    assert "artifacts/proofs/task-007-planner-router-executor-transport-spec-check.json" in names
    assert "artifacts/proofs/task-007-planner-router-executor-transport-spec-summary.md" in names
    assert "artifacts/proofs/task-007-planner-router-executor-transport-implementation-check.json" in names
    assert "artifacts/proofs/task-007-planner-router-executor-transport-implementation-summary.md" in names
    assert "artifacts/proofs/task-007-transport-runtime-smoke-check.json" in names
    assert "artifacts/proofs/task-007-transport-runtime-smoke-summary.md" in names
    assert "artifacts/proofs/task-007-transport-livepaper-smoke-check.json" in names
    assert "artifacts/proofs/task-007-transport-livepaper-smoke-summary.md" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-smoke-check.json" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-smoke-summary.md" in names
    assert "tests/test_planner_router_transport_livepaper_observability_smoke.py" in names
    assert "tests/test_planner_router_transport_livepaper_smoke.py" in names
    assert "artifacts/context_pack.json" in names
    assert "artifacts/proof_bundle_manifest.json" in names
    assert "tests/__pycache__/" not in names
