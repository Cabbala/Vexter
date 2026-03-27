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
        "docs/livepaper_observability_operator_runbook.md",
        "docs/livepaper_observability_shift_checklist.md",
        "docs/livepaper_observability_shift_handoff_template.md",
        "docs/livepaper_observability_shift_handoff_drill.md",
        "docs/demo_forward_operator_checklist.md",
        "docs/demo_forward_abort_rollback_matrix.md",
        "docs/demo_forward_supervised_run_operator_follow_up.md",
        "docs/demo_forward_supervised_run_retry_readiness_checklist.md",
        "docs/demo_forward_supervised_run_retry_prerequisite_matrix.md",
        "docs/demo_forward_supervised_run_retry_gate_checklist.md",
        "docs/demo_forward_supervised_run_retry_gate_decision_surface.md",
        "docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md",
        "docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md",
        "docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md",
        "docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md",
        "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md",
        "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md",
        "docs/windows_runtime_recovery.md",
        "docs/dexter_source_assessment.md",
        "docs/dexter_event_mapping.md",
        "docs/dexter_paper_mode_design.md",
        "docs/mewx_source_assessment.md",
        "docs/mewx_event_mapping.md",
        "specs/FIXED_WORKFLOW.md",
        "specs/ANALYSIS_CONTRACT.md",
        "specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md",
        "specs/PATTERN_A_DEMO_EXECUTOR_CUTOVER.md",
        "specs/DEMO_FORWARD_ACCEPTANCE_PACK.md",
        "specs/DEMO_FORWARD_SUPERVISED_RUN.md",
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md",
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md",
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md",
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md",
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK.md",
        "ops/CODEX_MEMORY.md",
        "plans/IMPLEMENTATION_PLAN.md",
        "plans/TASK_000_BOOTSTRAP.md",
        "plans/SOURCE_ASSESSMENT_DEXTER.md",
        "plans/SOURCE_ASSESSMENT_MEWX.md",
        "plans/dexter_instrumentation_plan.md",
        "plans/mewx_instrumentation_plan.md",
        "plans/integration_readiness_plan.md",
        "plans/demo_executor_adapter_implementation_plan.md",
        "plans/demo_forward_acceptance_pack_plan.md",
        "plans/demo_forward_supervised_run_plan.md",
        "plans/demo_forward_supervised_run_retry_readiness_plan.md",
        "plans/demo_forward_supervised_run_retry_gate_plan.md",
        "plans/demo_forward_supervised_run_retry_gate_input_attestation_plan.md",
        "plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md",
        "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_plan.md",
        "manifests/reference_repos.json",
        "manifests/windows_runtime.json",
        "scripts/bootstrap_windows_workspace.sh",
        "scripts/recover_windows_runtime.sh",
        "scripts/sync_reference_repos.sh",
        "scripts/build_proof_bundle.sh",
        "scripts/run_demo_forward_supervised_run.py",
        "scripts/run_demo_forward_supervised_run_retry_readiness.py",
        "scripts/run_demo_forward_supervised_run_retry_gate.py",
        "scripts/run_demo_forward_supervised_run_retry_gate_input_attestation.py",
        "scripts/run_demo_forward_supervised_run_retry_gate_attestation_audit.py",
        "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
        "scripts/run_livepaper_observability_shift_handoff_ci_check.sh",
        "scripts/run_livepaper_observability_shift_handoff_watchdog.sh",
        "scripts/run_livepaper_observability_shift_handoff_watchdog_runtime.sh",
        "scripts/run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh",
        "scripts/run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh",
        "scripts/run_transport_livepaper_observability_ci_gate.sh",
        "scripts/run_transport_livepaper_observability_watchdog.sh",
        "scripts/run_transport_livepaper_observability_watchdog_runtime.sh",
        "scripts/run_transport_livepaper_observability_watchdog_regression_pack.sh",
        "scripts/run_transport_livepaper_observability_watchdog_ci_gate.sh",
        "scripts/comparison_analysis.py",
        "scripts/collect_comparison_package.ps1",
        "pytest.ini",
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
        "vexter/planner_router/handoff_watchdog.py",
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
        "tests/test_pattern_a_demo_executor_cutover.py",
        "tests/test_demo_forward_acceptance_pack.py",
        "tests/test_demo_forward_supervised_run.py",
        "tests/test_demo_forward_supervised_run_retry_readiness.py",
        "tests/test_demo_forward_supervised_run_retry_gate.py",
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
        "artifacts/reports/task-007-transport-livepaper-observability-runtime-report.md",
        "artifacts/reports/task-007-transport-livepaper-observability-runtime-status.md",
        "artifacts/reports/task-007-transport-livepaper-observability-runtime/DETAILS.md",
        "artifacts/reports/task-007-transport-livepaper-observability-runtime/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-livepaper-observability-runtime/CONTEXT.json",
        "artifacts/reports/task-007-transport-livepaper-observability-hardening-report.md",
        "artifacts/reports/task-007-transport-livepaper-observability-hardening-status.md",
        "artifacts/reports/task-007-transport-livepaper-observability-hardening/DETAILS.md",
        "artifacts/reports/task-007-transport-livepaper-observability-hardening/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-livepaper-observability-hardening/CONTEXT.json",
        "artifacts/reports/task-007-transport-livepaper-observability-regression-pack-report.md",
        "artifacts/reports/task-007-transport-livepaper-observability-regression-pack-status.md",
        "artifacts/reports/task-007-transport-livepaper-observability-regression-pack/DETAILS.md",
        "artifacts/reports/task-007-transport-livepaper-observability-regression-pack/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-livepaper-observability-regression-pack/CONTEXT.json",
        "artifacts/reports/task-007-transport-livepaper-observability-ci-gate-report.md",
        "artifacts/reports/task-007-transport-livepaper-observability-ci-gate-status.md",
        "artifacts/reports/task-007-transport-livepaper-observability-ci-gate/DETAILS.md",
        "artifacts/reports/task-007-transport-livepaper-observability-ci-gate/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-livepaper-observability-ci-gate/CONTEXT.json",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-report.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-status.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog/DETAILS.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog/CONTEXT.json",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime-report.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime-status.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime/DETAILS.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime/CONTEXT.json",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-regression-pack-report.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-regression-pack-status.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-regression-pack/DETAILS.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-regression-pack/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-regression-pack/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/HANDOFF.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/HANDOFF.md",
        "artifacts/reports/pattern-a-demo-executor-cutover-report.md",
        "artifacts/reports/pattern-a-demo-executor-cutover-status.md",
        "artifacts/reports/pattern-a-demo-executor-cutover/DETAILS.md",
        "artifacts/reports/pattern-a-demo-executor-cutover/MIN_PROMPT.txt",
        "artifacts/reports/pattern-a-demo-executor-cutover/CONTEXT.json",
        "artifacts/reports/pattern-a-demo-executor-cutover/HANDOFF.md",
        "artifacts/reports/demo-executor-adapter-implementation-report.md",
        "artifacts/reports/demo-executor-adapter-implementation-status.md",
        "artifacts/reports/demo-forward-acceptance-pack-report.md",
        "artifacts/reports/demo-forward-acceptance-pack-status.md",
        "artifacts/reports/demo-forward-acceptance-pack/DETAILS.md",
        "artifacts/reports/demo-forward-acceptance-pack/MIN_PROMPT.txt",
        "artifacts/reports/demo-forward-acceptance-pack/CONTEXT.json",
        "artifacts/reports/demo-forward-acceptance-pack/HANDOFF.md",
        "artifacts/reports/demo-forward-supervised-run-report.md",
        "artifacts/reports/demo-forward-supervised-run-status.md",
        "artifacts/reports/demo-forward-supervised-run/DETAILS.md",
        "artifacts/reports/demo-forward-supervised-run/MIN_PROMPT.txt",
        "artifacts/reports/demo-forward-supervised-run/CONTEXT.json",
        "artifacts/reports/demo-forward-supervised-run/HANDOFF.md",
        "artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md",
        "artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md",
        "artifacts/reports/demo-forward-supervised-run-retry-readiness/DETAILS.md",
        "artifacts/reports/demo-forward-supervised-run-retry-readiness/MIN_PROMPT.txt",
        "artifacts/reports/demo-forward-supervised-run-retry-readiness/CONTEXT.json",
        "artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md",
        "artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-report.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-status.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate/DETAILS.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate/MIN_PROMPT.txt",
        "artifacts/reports/demo-forward-supervised-run-retry-gate/CONTEXT.json",
        "artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate/subagent_summary.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/DETAILS.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/MIN_PROMPT.txt",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/CONTEXT.json",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/subagent_summary.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/DETAILS.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/MIN_PROMPT.txt",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/CONTEXT.json",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/subagent_summary.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/DETAILS.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/MIN_PROMPT.txt",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/CONTEXT.json",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/HANDOFF.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/SUBAGENTS.md",
        "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/subagent_summary.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate-report.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate-status.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate/DETAILS.md",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate/MIN_PROMPT.txt",
        "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-spec-report.md",
        "artifacts/reports/task-007-livepaper-observability-spec-status.md",
        "artifacts/reports/task-007-livepaper-observability-spec/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-spec/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-spec/CONTEXT.json",
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
        "artifacts/proofs/task-007-transport-livepaper-observability-runtime-check.json",
        "artifacts/proofs/task-007-transport-livepaper-observability-runtime-summary.md",
        "artifacts/proofs/task-007-transport-livepaper-observability-hardening-check.json",
        "artifacts/proofs/task-007-transport-livepaper-observability-hardening-summary.md",
        "artifacts/proofs/task-007-transport-livepaper-observability-regression-pack-check.json",
        "artifacts/proofs/task-007-transport-livepaper-observability-regression-pack-summary.md",
        "artifacts/proofs/task-007-transport-livepaper-observability-ci-gate-check.json",
        "artifacts/proofs/task-007-transport-livepaper-observability-ci-gate-summary.md",
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-check.json",
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-summary.md",
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json",
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-summary.md",
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-regression-pack-check.json",
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-regression-pack-summary.md",
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json",
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-summary.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md",
        "artifacts/proofs/pattern-a-demo-executor-cutover-check.json",
        "artifacts/proofs/pattern-a-demo-executor-cutover-summary.md",
        "artifacts/proofs/demo-executor-adapter-implementation-check.json",
        "artifacts/proofs/demo-executor-adapter-implementation-summary.md",
        "artifacts/proofs/demo-forward-acceptance-pack-check.json",
        "artifacts/proofs/demo-forward-acceptance-pack-summary.md",
        "artifacts/proofs/demo-forward-supervised-run-check.json",
        "artifacts/proofs/demo-forward-supervised-run-summary.md",
        "artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json",
        "artifacts/proofs/demo-forward-supervised-run-retry-readiness-summary.md",
        "artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json",
        "artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md",
        "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json",
        "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md",
        "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json",
        "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md",
        "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json",
        "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-summary.md",
        "artifacts/bundles/task-007-planner-router-code-implementation.tar.gz",
        "artifacts/bundles/task-007-planner-router-integration-smoke.tar.gz",
        "artifacts/bundles/task-007-monitor-killswitch-spec.tar.gz",
        "artifacts/bundles/task-007-planner-router-livepaper-smoke.tar.gz",
        "artifacts/bundles/task-007-planner-router-executor-transport-spec.tar.gz",
        "artifacts/bundles/task-007-planner-router-executor-transport-implementation.tar.gz",
        "artifacts/bundles/task-007-transport-runtime-smoke.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-smoke.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-observability-smoke.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-observability-runtime.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-observability-hardening.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-observability-regression-pack.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-observability-ci-gate.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-observability-watchdog.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-observability-watchdog-runtime.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-observability-watchdog-regression-pack.tar.gz",
        "artifacts/bundles/task-007-transport-livepaper-observability-watchdog-ci-gate.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz",
        "artifacts/bundles/pattern-a-demo-executor-cutover.tar.gz",
        "artifacts/bundles/demo-forward-acceptance-pack.tar.gz",
        "artifacts/bundles/demo-forward-supervised-run.tar.gz",
        "artifacts/bundles/demo-forward-supervised-run-retry-readiness.tar.gz",
        "artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz",
        "artifacts/bundles/demo-forward-supervised-run-retry-gate-input-attestation.tar.gz",
        "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz",
        "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack.tar.gz",
        "tests/test_demo_forward_supervised_run_retry_gate.py",
        "tests/test_demo_forward_supervised_run_retry_readiness.py",
        "tests/test_demo_forward_supervised_run_retry_gate_input_attestation.py",
        "tests/test_demo_forward_supervised_run_retry_gate_attestation_audit.py",
        "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
        "tests/test_planner_router_transport_livepaper_observability_smoke.py",
        "tests/test_planner_router_transport_livepaper_observability_runtime.py",
        "tests/test_planner_router_transport_livepaper_observability_hardening.py",
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py",
        "tests/test_planner_router_transport_livepaper_observability_ci_gate.py",
        "tests/test_planner_router_transport_livepaper_observability_watchdog.py",
        "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py",
        "tests/test_planner_router_transport_livepaper_observability_watchdog_ci_gate.py",
        "tests/test_planner_router_transport_livepaper_observability_spec_contract.py",
        "tests/test_planner_router_transport_livepaper_observability_operator_runbook.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_checklist.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_template.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_drill.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py",
        "artifacts/examples/task-004-sample-comparison/pack_manifest.json",
        "artifacts/reports/task-007-livepaper-observability-spec-report.md",
        "artifacts/reports/task-007-livepaper-observability-spec-status.md",
        "artifacts/reports/task-007-livepaper-observability-spec/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-spec/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-spec/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-operator-runbook-report.md",
        "artifacts/reports/task-007-livepaper-observability-operator-runbook-status.md",
        "artifacts/reports/task-007-livepaper-observability-operator-runbook/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-operator-runbook/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-operator-runbook/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-checklist-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-checklist-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-checklist/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-checklist/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-checklist/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-template-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-template-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-template/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-template/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-template/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/HANDOFF.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime/HANDOFF.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/HANDOFF.md",
        "artifacts/proofs/task-007-livepaper-observability-spec-check.json",
        "artifacts/proofs/task-007-livepaper-observability-spec-summary.md",
        "artifacts/proofs/task-007-livepaper-observability-operator-runbook-check.json",
        "artifacts/proofs/task-007-livepaper-observability-operator-runbook-summary.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-checklist-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-checklist-summary.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-template-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-template-summary.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-drill-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-drill-summary.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-summary.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-summary.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-summary.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md",
        "artifacts/bundles/task-007-livepaper-observability-spec.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-operator-runbook.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-checklist.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-template.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-drill.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-ci-check.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog.tar.gz",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-runtime.tar.gz",
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


def test_transport_livepaper_observability_ci_gate_is_wired_into_validation() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    script = (REPO_ROOT / "scripts" / "run_transport_livepaper_observability_ci_gate.sh").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    assert "./scripts/run_transport_livepaper_observability_ci_gate.sh" in workflow
    assert "transport-livepaper-observability-ci-gate-proof" in workflow
    assert "-m \"$SUITE_MARKER\"" in script
    assert "tests/test_planner_router_transport_livepaper_observability_regression_pack.py" in script
    assert "tests/test_planner_router_transport_livepaper_observability_ci_gate.py" in script
    assert "transport_livepaper_observability_ci_gate" in pytest_ini


def test_livepaper_observability_shift_handoff_ci_check_is_wired_into_validation() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    script = (REPO_ROOT / "scripts" / "run_livepaper_observability_shift_handoff_ci_check.sh").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    assert "./scripts/run_livepaper_observability_shift_handoff_ci_check.sh" in workflow
    assert "livepaper-observability-shift-handoff-ci-check-proof" in workflow
    assert "not livepaper_observability_shift_handoff_ci_check" in workflow
    assert "-m \"$SUITE_MARKER\"" in script
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_template.py" in script
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_drill.py" in script
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py" in script
    assert "livepaper_observability_shift_handoff_ci_check" in pytest_ini


def test_livepaper_observability_shift_handoff_watchdog_is_wired_into_validation() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    script = (REPO_ROOT / "scripts" / "run_livepaper_observability_shift_handoff_watchdog.sh").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    assert "./scripts/run_livepaper_observability_shift_handoff_watchdog.sh" in workflow
    assert "livepaper-observability-shift-handoff-watchdog-proof" in workflow
    assert "not livepaper_observability_shift_handoff_watchdog" in workflow
    assert "-m \"$SUITE_MARKER\"" in script
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py" in script
    assert "livepaper_observability_shift_handoff_watchdog" in pytest_ini


def test_livepaper_observability_shift_handoff_watchdog_runtime_is_wired_into_validation() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    script = (
        REPO_ROOT / "scripts" / "run_livepaper_observability_shift_handoff_watchdog_runtime.sh"
    ).read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    assert "./scripts/run_livepaper_observability_shift_handoff_watchdog_runtime.sh" in workflow
    assert "livepaper-observability-shift-handoff-watchdog-runtime-proof" in workflow
    assert "not livepaper_observability_shift_handoff_watchdog_runtime" in workflow
    assert "-m \"$SUITE_MARKER\"" in script
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py" in script
    assert "livepaper_observability_shift_handoff_watchdog_runtime" in pytest_ini


def test_livepaper_observability_shift_handoff_watchdog_regression_pack_is_wired_into_validation() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    script = (
        REPO_ROOT / "scripts" / "run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh"
    ).read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    assert "./scripts/run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh" in workflow
    assert "livepaper-observability-shift-handoff-watchdog-regression-pack-proof" in workflow
    assert "not livepaper_observability_shift_handoff_watchdog_regression_pack" in workflow
    assert "-m \"$SUITE_MARKER\"" in script
    assert (
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py"
        in script
    )
    assert "livepaper_observability_shift_handoff_watchdog_regression_pack" in pytest_ini


def test_livepaper_observability_shift_handoff_watchdog_ci_gate_is_wired_into_validation() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    script = (
        REPO_ROOT / "scripts" / "run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh"
    ).read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    assert "./scripts/run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh" in workflow
    assert "livepaper-observability-shift-handoff-watchdog-ci-gate-proof" in workflow
    assert "not livepaper_observability_shift_handoff_watchdog_ci_gate" in workflow
    assert "-m \"$SUITE_MARKER\"" in script
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py" in script
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py" in script
    assert (
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py"
        in script
    )
    assert (
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py"
        in script
    )
    assert "livepaper_observability_shift_handoff_watchdog_ci_gate" in pytest_ini


def test_transport_livepaper_observability_watchdog_is_wired_into_validation() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    script = (REPO_ROOT / "scripts" / "run_transport_livepaper_observability_watchdog.sh").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    assert "./scripts/run_transport_livepaper_observability_watchdog.sh" in workflow
    assert "transport-livepaper-observability-watchdog-proof" in workflow
    assert "not transport_livepaper_observability_watchdog" in workflow
    assert "-m \"$SUITE_MARKER\"" in script
    assert "tests/test_planner_router_transport_livepaper_observability_watchdog.py" in script
    assert "transport_livepaper_observability_watchdog" in pytest_ini


def test_transport_livepaper_observability_watchdog_ci_gate_is_wired_into_validation() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    script = (REPO_ROOT / "scripts" / "run_transport_livepaper_observability_watchdog_ci_gate.sh").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    assert "./scripts/run_transport_livepaper_observability_watchdog_ci_gate.sh" in workflow
    assert "transport-livepaper-observability-watchdog-ci-gate-proof" in workflow
    assert "not transport_livepaper_observability_watchdog_ci_gate" in workflow
    assert "-m \"$SUITE_MARKER\"" in script
    assert "tests/test_planner_router_transport_livepaper_observability_watchdog.py" in script
    assert "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py" in script
    assert "tests/test_planner_router_transport_livepaper_observability_regression_pack.py" in script
    assert "transport_livepaper_observability_watchdog_ci_gate" in pytest_ini


def test_transport_livepaper_observability_watchdog_runtime_is_wired_into_validation() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    script = (REPO_ROOT / "scripts" / "run_transport_livepaper_observability_watchdog_runtime.sh").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    assert "./scripts/run_transport_livepaper_observability_watchdog_runtime.sh" in workflow
    assert "transport-livepaper-observability-watchdog-runtime-proof" in workflow
    assert "not transport_livepaper_observability_watchdog_runtime" in workflow
    assert "-m \"$SUITE_MARKER\"" in script
    assert "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py" in script
    assert "transport_livepaper_observability_watchdog_runtime" in pytest_ini


def test_transport_livepaper_observability_watchdog_regression_pack_runner_is_present() -> None:
    script = (REPO_ROOT / "scripts" / "run_transport_livepaper_observability_watchdog_regression_pack.sh").read_text()
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text()

    assert "-m \"$SUITE_MARKER\"" in script
    assert "tests/test_planner_router_transport_livepaper_observability_regression_pack.py" in script
    assert "./scripts/run_transport_livepaper_observability_watchdog_regression_pack.sh" in workflow
    assert "transport-livepaper-observability-watchdog-regression-pack-proof" in workflow
    assert "transport_livepaper_observability_watchdog_regression_pack" in pytest_ini


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
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-RUNTIME",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-HARDENING",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-REGRESSION-PACK",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-CI-GATE",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-REGRESSION-PACK",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SPEC",
        "TASK-007-LIVEPAPER-OBSERVABILITY-OPERATOR-RUNBOOK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-CHECKLIST",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-TEMPLATE",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-DRILL",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
        "PATTERN-A-DEMO-EXECUTOR-CUTOVER",
        "DEMO-FORWARD-ACCEPTANCE-PACK",
        "DEMO-FORWARD-SUPERVISED-RUN",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK",
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
        "transport_livepaper_observability_runtime_passed",
        "transport_livepaper_observability_hardening_passed",
        "transport_livepaper_observability_regression_pack_passed",
        "transport_livepaper_observability_ci_gate_passed",
        "transport_livepaper_observability_watchdog_passed",
        "transport_livepaper_observability_watchdog_runtime_passed",
        "transport_livepaper_observability_watchdog_regression_pack_passed",
        "transport_livepaper_observability_watchdog_ci_gate_passed",
        "livepaper_observability_spec_ready",
        "livepaper_observability_operator_runbook_ready",
        "livepaper_observability_shift_checklist_ready",
        "livepaper_observability_shift_handoff_template_ready",
        "livepaper_observability_shift_handoff_drill_passed",
        "livepaper_observability_shift_handoff_ci_check_passed",
        "livepaper_observability_shift_handoff_watchdog_passed",
        "livepaper_observability_shift_handoff_watchdog_runtime_passed",
        "livepaper_observability_shift_handoff_watchdog_regression_pack_passed",
        "livepaper_observability_shift_handoff_watchdog_ci_gate_passed",
        "livepaper_observability_shift_handoff_watchdog_ci_gate_failed",
        "pattern_a_demo_executor_cutover_ready",
        "demo_forward_acceptance_pack_ready",
        "demo_forward_supervised_run_blocked",
        "supervised_run_retry_readiness_blocked",
        "supervised_run_retry_gate_blocked",
        "supervised_run_retry_gate_input_attestation_blocked",
        "supervised_run_retry_gate_attestation_audit_blocked",
        "supervised_run_retry_gate_attestation_record_pack_blocked",
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
        "codex/task-007-transport-livepaper-observability-runtime",
        "codex/task-007-transport-livepaper-observability-hardening",
        "codex/task-007-transport-livepaper-observability-regression-pack",
        "codex/task-007-transport-livepaper-observability-ci-gate",
        "codex/task-007-transport-livepaper-observability-watchdog",
        "codex/task-007-transport-livepaper-observability-watchdog-runtime",
        "codex/task-007-transport-livepaper-observability-watchdog-regression-pack",
        "codex/task-007-transport-livepaper-observability-watchdog-ci-gate",
        "codex/task-007-livepaper-observability-spec",
        "codex/task-007-livepaper-observability-operator-runbook",
        "codex/task-007-livepaper-observability-shift-checklist",
        "codex/task-007-livepaper-observability-shift-handoff-template",
        "codex/task-007-livepaper-observability-shift-handoff-drill",
        "codex/task-007-livepaper-observability-shift-handoff-ci-check",
        "codex/task-007-livepaper-observability-shift-handoff-watchdog",
        "codex/task-007-livepaper-observability-shift-handoff-watchdog-runtime",
        "codex/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack",
        "codex/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate",
        "codex/pattern-a-demo-executor-cutover",
        "feat/demo-forward-acceptance-pack",
            "feat/demo-forward-supervised-run",
            "feat/supervised-run-retry-readiness",
        "feat/supervised-run-retry-gate",
        "feat/supervised-run-retry-gate-input-attestation",
        "feat/retry-gate-attestation-audit",
        "feat/attestation-record-pack",
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
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-HARDENING",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-REGRESSION-PACK",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-CI-GATE",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-REGRESSION-PACK",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-ACCEPTANCE-PACK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-OPERATOR-RUNBOOK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-CHECKLIST",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-TEMPLATE",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-DRILL",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
        "DEMO-EXECUTOR-ADAPTER-IMPLEMENTATION",
        "DEMO-FORWARD-SUPERVISED-RUN",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH",
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
        "ready_for_transport_livepaper_observability_hardening",
        "ready_for_transport_livepaper_observability_regression_pack",
        "ready_for_transport_livepaper_observability_ci_gate",
        "ready_for_transport_livepaper_observability_watchdog",
        "ready_for_transport_livepaper_observability_watchdog_runtime",
        "ready_for_transport_livepaper_observability_watchdog_regression_pack",
        "ready_for_transport_livepaper_observability_watchdog_ci_gate",
        "ready_for_transport_livepaper_observability_acceptance_pack",
        "ready_for_livepaper_observability_operator_runbook",
        "ready_for_livepaper_observability_shift_checklist",
        "ready_for_livepaper_observability_shift_handoff_template",
        "ready_for_livepaper_observability_shift_handoff_drill",
        "ready_for_livepaper_observability_shift_handoff_ci_check",
        "ready_for_livepaper_observability_shift_handoff_watchdog",
        "ready_for_livepaper_observability_shift_handoff_watchdog_runtime",
        "ready_for_livepaper_observability_shift_handoff_watchdog_regression_pack",
        "ready_for_livepaper_observability_shift_handoff_watchdog_ci_gate",
        "ready_for_demo_executor_adapter_implementation",
        "ready_for_demo_forward_supervised_run",
        "ready_for_supervised_run_retry_readiness",
        "ready_for_supervised_run_retry_gate",
        "retry_gate_inputs_pending",
        "retry_gate_input_attestations_pending",
        "retry_gate_attestation_audits_pending",
        "current_attestation_records_refresh_required",
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
        "transport_livepaper_observability_runtime_passed",
        "transport_livepaper_observability_hardening_passed",
        "transport_livepaper_observability_regression_pack_passed",
        "transport_livepaper_observability_ci_gate_passed",
        "transport_livepaper_observability_watchdog_passed",
        "transport_livepaper_observability_watchdog_runtime_passed",
        "transport_livepaper_observability_watchdog_regression_pack_passed",
        "transport_livepaper_observability_watchdog_ci_gate_passed",
        "livepaper_observability_spec_ready",
        "livepaper_observability_operator_runbook_ready",
        "livepaper_observability_shift_checklist_ready",
        "livepaper_observability_shift_handoff_template_ready",
        "livepaper_observability_shift_handoff_drill_passed",
        "livepaper_observability_shift_handoff_ci_check_passed",
        "livepaper_observability_shift_handoff_watchdog_passed",
        "livepaper_observability_shift_handoff_watchdog_runtime_passed",
        "livepaper_observability_shift_handoff_watchdog_regression_pack_passed",
        "livepaper_observability_shift_handoff_watchdog_ci_gate_passed",
        "livepaper_observability_shift_handoff_watchdog_ci_gate_failed",
        "pattern_a_demo_executor_cutover_ready",
        "demo_forward_acceptance_pack_ready",
        "demo_forward_supervised_run_blocked",
        "supervised_run_retry_readiness_blocked",
        "supervised_run_retry_gate_blocked",
        "supervised_run_retry_gate_input_attestation_blocked",
        "supervised_run_retry_gate_attestation_audit_blocked",
        "supervised_run_retry_gate_attestation_record_pack_blocked",
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
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-HARDENING",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-REGRESSION-PACK",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-CI-GATE",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-REGRESSION-PACK",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE",
        "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-ACCEPTANCE-PACK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-OPERATOR-RUNBOOK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-CHECKLIST",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-TEMPLATE",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-DRILL",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
        "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
            "DEMO-EXECUTOR-ADAPTER-IMPLEMENTATION",
            "DEMO-FORWARD-SUPERVISED-RUN",
            "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT",
        "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH",
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
        "ready_for_transport_livepaper_observability_hardening",
        "ready_for_transport_livepaper_observability_regression_pack",
        "ready_for_transport_livepaper_observability_ci_gate",
        "ready_for_transport_livepaper_observability_watchdog",
        "ready_for_transport_livepaper_observability_watchdog_runtime",
        "ready_for_transport_livepaper_observability_watchdog_regression_pack",
        "ready_for_transport_livepaper_observability_watchdog_ci_gate",
        "ready_for_transport_livepaper_observability_acceptance_pack",
        "ready_for_livepaper_observability_operator_runbook",
        "ready_for_livepaper_observability_shift_checklist",
        "ready_for_livepaper_observability_shift_handoff_template",
        "ready_for_livepaper_observability_shift_handoff_drill",
        "ready_for_livepaper_observability_shift_handoff_ci_check",
        "ready_for_livepaper_observability_shift_handoff_watchdog",
        "ready_for_livepaper_observability_shift_handoff_watchdog_runtime",
        "ready_for_livepaper_observability_shift_handoff_watchdog_regression_pack",
        "ready_for_livepaper_observability_shift_handoff_watchdog_ci_gate",
        "ready_for_demo_executor_adapter_implementation",
        "ready_for_demo_forward_supervised_run",
        "ready_for_supervised_run_retry_readiness",
        "ready_for_supervised_run_retry_gate",
        "retry_gate_inputs_pending",
        "retry_gate_input_attestations_pending",
        "retry_gate_attestation_audits_pending",
        "current_attestation_records_refresh_required",
    }

    bundle_path = REPO_ROOT / manifest["bundle_path"]
    assert bundle_path.exists()

    with tarfile.open(bundle_path, "r:gz") as bundle:
        names = set(bundle.getnames())

    assert "README.md" in names
    assert "docs/evaluation_contract.md" in names
    assert "docs/normalized_event_schema.md" in names
    assert "docs/comparison_collection_runbook.md" in names
    assert "docs/livepaper_observability_operator_runbook.md" in names
    assert "docs/livepaper_observability_shift_checklist.md" in names
    assert "docs/livepaper_observability_shift_handoff_template.md" in names
    assert "docs/livepaper_observability_shift_handoff_drill.md" in names
    assert "docs/demo_forward_operator_checklist.md" in names
    assert "docs/demo_forward_abort_rollback_matrix.md" in names
    assert "docs/demo_forward_supervised_run_operator_follow_up.md" in names
    assert "docs/demo_forward_supervised_run_retry_readiness_checklist.md" in names
    assert "docs/demo_forward_supervised_run_retry_prerequisite_matrix.md" in names
    assert "docs/demo_forward_supervised_run_retry_gate_checklist.md" in names
    assert "docs/demo_forward_supervised_run_retry_gate_decision_surface.md" in names
    assert "docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md" in names
    assert "docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md" in names
    assert "docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md" in names
    assert "docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md" in names
    assert "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md" in names
    assert "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md" in names
    assert "docs/windows_runtime_recovery.md" in names
    assert "docs/dexter_event_mapping.md" in names
    assert "docs/dexter_paper_mode_design.md" in names
    assert "docs/mewx_event_mapping.md" in names
    assert "specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md" in names
    assert "specs/DEMO_FORWARD_ACCEPTANCE_PACK.md" in names
    assert "specs/DEMO_FORWARD_SUPERVISED_RUN.md" in names
    assert "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md" in names
    assert "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md" in names
    assert "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md" in names
    assert "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md" in names
    assert "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK.md" in names
    assert "plans/demo_forward_acceptance_pack_plan.md" in names
    assert "plans/demo_forward_supervised_run_plan.md" in names
    assert "plans/demo_forward_supervised_run_retry_readiness_plan.md" in names
    assert "plans/demo_forward_supervised_run_retry_gate_plan.md" in names
    assert "plans/demo_forward_supervised_run_retry_gate_input_attestation_plan.md" in names
    assert "plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md" in names
    assert "tests/test_demo_forward_acceptance_pack.py" in names
    assert "tests/test_demo_forward_supervised_run.py" in names
    assert "tests/test_demo_forward_supervised_run_retry_readiness.py" in names
    assert "tests/test_demo_forward_supervised_run_retry_gate.py" in names
    assert "tests/test_demo_forward_supervised_run_retry_gate_input_attestation.py" in names
    assert "tests/test_demo_forward_supervised_run_retry_gate_attestation_audit.py" in names
    assert "scripts/run_demo_forward_supervised_run.py" in names
    assert "scripts/run_demo_forward_supervised_run_retry_readiness.py" in names
    assert "scripts/run_demo_forward_supervised_run_retry_gate.py" in names
    assert "scripts/run_demo_forward_supervised_run_retry_gate_input_attestation.py" in names
    assert "scripts/run_demo_forward_supervised_run_retry_gate_attestation_audit.py" in names
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
    assert "artifacts/reports/demo-forward-supervised-run-report.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-status.md" in names
    assert "artifacts/reports/demo-forward-supervised-run/DETAILS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run/MIN_PROMPT.txt" in names
    assert "artifacts/reports/demo-forward-supervised-run/CONTEXT.json" in names
    assert "artifacts/reports/demo-forward-supervised-run/HANDOFF.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-readiness/DETAILS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-readiness/MIN_PROMPT.txt" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-readiness/CONTEXT.json" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-report.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-status.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate/DETAILS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate/MIN_PROMPT.txt" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate/CONTEXT.json" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate/subagent_summary.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/DETAILS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/MIN_PROMPT.txt" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/CONTEXT.json" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/subagent_summary.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/DETAILS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/MIN_PROMPT.txt" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/CONTEXT.json" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/subagent_summary.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/DETAILS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/MIN_PROMPT.txt" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/CONTEXT.json" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/HANDOFF.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/SUBAGENTS.md" in names
    assert "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/subagent_summary.md" in names
    assert "artifacts/reports/dexter-paper-design-handoff/DETAILS.md" in names
    assert "artifacts/reports/dexter-paper-design-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-005-paper-validation-handoff/DETAILS.md" in names
    assert "artifacts/reports/task-005-paper-validation-handoff/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-006-replay-validation.md" in names
    assert "artifacts/reports/task-006-replay-validation-status.md" in names
    assert "artifacts/proofs/demo-forward-supervised-run-check.json" in names
    assert "artifacts/proofs/demo-forward-supervised-run-summary.md" in names
    assert "artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json" in names
    assert "artifacts/proofs/demo-forward-supervised-run-retry-readiness-summary.md" in names
    assert "artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json" in names
    assert "artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md" in names
    assert "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json" in names
    assert "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md" in names
    assert "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json" in names
    assert "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md" in names
    assert "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json" in names
    assert "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-summary.md" in names
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
    assert "artifacts/reports/task-007-transport-livepaper-observability-runtime-report.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-runtime-status.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-runtime/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-runtime/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-runtime/CONTEXT.json" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-hardening-report.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-hardening-status.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-hardening/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-hardening/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-hardening/CONTEXT.json" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-regression-pack-report.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-regression-pack-status.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-regression-pack/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-regression-pack/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-regression-pack/CONTEXT.json" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-ci-gate-report.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-ci-gate-status.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-ci-gate/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-report.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-status.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog/CONTEXT.json" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime-report.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime-status.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime/CONTEXT.json" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-regression-pack-report.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-regression-pack-status.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-regression-pack/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-regression-pack/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-regression-pack/CONTEXT.json" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate-report.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate-status.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate/DETAILS.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate/CONTEXT.json" in names
    assert "artifacts/reports/task-007-livepaper-observability-spec-report.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-spec-status.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-spec/DETAILS.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-spec/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-livepaper-observability-spec/CONTEXT.json" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-checklist-report.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-checklist-status.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-checklist/DETAILS.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-checklist/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-checklist/CONTEXT.json" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-template-report.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-template-status.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-template/DETAILS.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-template/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-template/CONTEXT.json" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill-report.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill-status.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/DETAILS.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/CONTEXT.json" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/HANDOFF.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check-report.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check-status.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check/DETAILS.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check/CONTEXT.json" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-report.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-status.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog/DETAILS.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog/CONTEXT.json" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime-report.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime-status.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime/DETAILS.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime/CONTEXT.json" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime/HANDOFF.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/DETAILS.md" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/CONTEXT.json" in names
    assert "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/HANDOFF.md" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-ci-gate/MIN_PROMPT.txt" in names
    assert "artifacts/reports/task-007-transport-livepaper-observability-ci-gate/CONTEXT.json" in names
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
    assert "artifacts/proofs/task-007-transport-livepaper-observability-runtime-check.json" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-runtime-summary.md" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-hardening-check.json" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-hardening-summary.md" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-regression-pack-check.json" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-regression-pack-summary.md" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-ci-gate-check.json" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-ci-gate-summary.md" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-check.json" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-summary.md" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-summary.md" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-regression-pack-check.json" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-regression-pack-summary.md" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json" in names
    assert "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-summary.md" in names
    assert "artifacts/proofs/task-007-livepaper-observability-spec-check.json" in names
    assert "artifacts/proofs/task-007-livepaper-observability-spec-summary.md" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-checklist-check.json" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-checklist-summary.md" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-template-check.json" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-template-summary.md" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-drill-check.json" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-drill-summary.md" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-check.json" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-summary.md" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-summary.md" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-summary.md" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json" in names
    assert "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md" in names
    assert "tests/test_planner_router_transport_livepaper_observability_smoke.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_runtime.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_hardening.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_regression_pack.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_ci_gate.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_watchdog.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_watchdog_ci_gate.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_shift_checklist.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_template.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_drill.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py" in names
    assert "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py" in names
    assert "tests/test_planner_router_transport_livepaper_smoke.py" in names
    assert "pytest.ini" in names
    assert "scripts/run_livepaper_observability_shift_handoff_ci_check.sh" in names
    assert "scripts/run_livepaper_observability_shift_handoff_watchdog.sh" in names
    assert "scripts/run_livepaper_observability_shift_handoff_watchdog_runtime.sh" in names
    assert "scripts/run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh" in names
    assert "scripts/run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh" in names
    assert "scripts/run_transport_livepaper_observability_ci_gate.sh" in names
    assert "scripts/run_transport_livepaper_observability_watchdog.sh" in names
    assert "scripts/run_transport_livepaper_observability_watchdog_runtime.sh" in names
    assert "scripts/run_transport_livepaper_observability_watchdog_regression_pack.sh" in names
    assert "scripts/run_transport_livepaper_observability_watchdog_ci_gate.sh" in names
    assert "artifacts/context_pack.json" in names
    assert "artifacts/proof_bundle_manifest.json" in names
    assert "tests/__pycache__/" not in names
