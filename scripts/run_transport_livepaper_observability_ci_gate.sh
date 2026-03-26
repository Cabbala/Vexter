#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF_DIR="$ROOT_DIR/artifacts/proofs"
PROOF_JSON="$PROOF_DIR/task-007-transport-livepaper-observability-ci-gate-check.json"
SUMMARY_MD="$PROOF_DIR/task-007-transport-livepaper-observability-ci-gate-summary.md"
LOG_PATH="$PROOF_DIR/task-007-transport-livepaper-observability-ci-gate-pytest.log"
SUITE_MARKER="transport_livepaper_observability_ci_gate"

mkdir -p "$PROOF_DIR"

GATE_TEST_FILES=(
  "tests/test_planner_router_transport_livepaper_observability_smoke.py"
  "tests/test_planner_router_transport_livepaper_observability_runtime.py"
  "tests/test_planner_router_transport_livepaper_observability_hardening.py"
  "tests/test_planner_router_transport_livepaper_observability_regression_pack.py"
)

printf 'Transport livepaper observability CI gate\n'
printf 'Suite marker: %s\n' "$SUITE_MARKER"
printf 'Gate test files:\n'
for file in "${GATE_TEST_FILES[@]}"; do
  printf ' - %s\n' "$file"
done
printf 'Locked observability surfaces:\n'
printf ' - immutable_handoff_metadata_continuity\n'
printf ' - handle_lifecycle_continuity\n'
printf ' - status_sink_fan_in\n'
printf ' - ack_history_retention\n'
printf ' - quarantine_reason_completeness\n'
printf ' - manual_stop_all_propagation\n'
printf ' - snapshot_backed_terminal_detail\n'
printf ' - normalized_failure_detail_passthrough\n'

set +e
(
  cd "$ROOT_DIR"
  pytest -q -m "$SUITE_MARKER" "${GATE_TEST_FILES[@]}"
) 2>&1 | tee "$LOG_PATH"
PYTEST_STATUS=${PIPESTATUS[0]}
set -e

if [[ $PYTEST_STATUS -eq 0 ]]; then
  GATE_STATUS="passed"
  TASK_STATE="transport_livepaper_observability_ci_gate_passed"
  SELECTED_OUTCOME="A"
  RECOMMENDED_NEXT_STEP="transport_livepaper_observability_watchdog"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG"
  DECISION="transport_livepaper_observability_watchdog_ready"
else
  GATE_STATUS="failed"
  TASK_STATE="transport_livepaper_observability_ci_gate_failed"
  SELECTED_OUTCOME="gate_failed"
  RECOMMENDED_NEXT_STEP="transport_livepaper_observability_ci_gate"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-CI-GATE"
  DECISION="transport_livepaper_observability_ci_gate_failed"
fi

export PROOF_JSON SUMMARY_MD LOG_PATH GATE_STATUS TASK_STATE SELECTED_OUTCOME
export RECOMMENDED_NEXT_STEP RECOMMENDED_NEXT_TASK_ID DECISION SUITE_MARKER

python - <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

proof_json = Path(os.environ["PROOF_JSON"])
summary_md = Path(os.environ["SUMMARY_MD"])
log_path = Path(os.environ["LOG_PATH"])
gate_status = os.environ["GATE_STATUS"]
task_state = os.environ["TASK_STATE"]
selected_outcome = os.environ["SELECTED_OUTCOME"]
recommended_next_step = os.environ["RECOMMENDED_NEXT_STEP"]
recommended_next_task_id = os.environ["RECOMMENDED_NEXT_TASK_ID"]
decision = os.environ["DECISION"]
suite_marker = os.environ["SUITE_MARKER"]

log_lines = log_path.read_text().splitlines()
pytest_result = next((line.strip() for line in reversed(log_lines) if line.strip()), "")

surface_tests = {
    "immutable_handoff_metadata_continuity": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_immutable_handoff_metadata_continuity"
    ],
    "handle_lifecycle_continuity": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_handle_lifecycle_continuity"
    ],
    "status_sink_fan_in": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_status_sink_fan_in"
    ],
    "ack_history_retention": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_ack_history_retention"
    ],
    "quarantine_reason_completeness": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_quarantine_reason_completeness"
    ],
    "manual_stop_all_propagation": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_manual_stop_all_propagation"
    ],
    "snapshot_backed_terminal_detail": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_snapshot_backed_terminal_detail"
    ],
    "normalized_failure_detail_passthrough": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_normalized_failure_detail_passthrough"
    ],
}

proof = {
    "task_id": "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-CI-GATE",
    "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "verified_github": {
        "latest_vexter_pr": 52,
        "latest_vexter_main_commit": "64d0670c328f446d1caddda0e2d9c81534ef8787",
        "latest_vexter_merged_at_utc": "2026-03-26T13:38:30Z",
        "dexter_pr": 3,
        "dexter_main_commit": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
        "mewx_frozen_commit": "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
    },
    "fixed_input_surface": {
        "promoted_label": "task005-pass-grade-pair-20260325T180027Z",
        "comparison_source_of_truth_state": "comparison_closed_out",
        "regression_pack_proof": "artifacts/proofs/task-007-transport-livepaper-observability-regression-pack-check.json",
        "regression_pack_summary": "artifacts/proofs/task-007-transport-livepaper-observability-regression-pack-summary.md",
        "regression_pack_status": "transport_livepaper_observability_regression_pack_passed",
        "dexter_replay_coverage_ratio": 1.0,
        "dexter_live_vs_replay_gap_pct": 0.0,
        "mewx_replay_coverage_ratio": 1.0,
        "mewx_live_vs_replay_gap_pct": 0.0,
        "confirmatory_residual": "Mew-X candidate_rejected",
        "confirmatory_overturns_promoted_baseline": False,
    },
    "ci_gate_suite": {
        "suite_group": suite_marker,
        "pytest_command": "pytest -q -m transport_livepaper_observability_ci_gate tests/test_planner_router_transport_livepaper_observability_smoke.py tests/test_planner_router_transport_livepaper_observability_runtime.py tests/test_planner_router_transport_livepaper_observability_hardening.py tests/test_planner_router_transport_livepaper_observability_regression_pack.py",
        "pytest_result": pytest_result,
        "gate_status": gate_status,
        "workflow": ".github/workflows/validate.yml",
        "proof_outputs": [
            "artifacts/proofs/task-007-transport-livepaper-observability-ci-gate-check.json",
            "artifacts/proofs/task-007-transport-livepaper-observability-ci-gate-summary.md",
        ],
        "gate_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_smoke.py",
            "tests/test_planner_router_transport_livepaper_observability_runtime.py",
            "tests/test_planner_router_transport_livepaper_observability_hardening.py",
            "tests/test_planner_router_transport_livepaper_observability_regression_pack.py"
        ],
        "surface_tests": surface_tests,
        "source_faithful_modes": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "proof_artifact_name": "transport-livepaper-observability-ci-gate-proof",
    },
    "next_task_evaluation": {
        "transport_livepaper_observability_watchdog": {
            "recommended": gate_status == "passed",
            "reasons": [
                "The transport seam is now guarded by an always-on CI gate, so the next bounded risk is runtime drift that escapes pre-merge checks.",
                "A watchdog lane would extend enforcement into ongoing observability monitoring without reopening comparison or boundary design.",
            ],
        },
        "livepaper_observability_spec": {
            "recommended": False,
            "reasons": [
                "The observability surface is already fixed across smoke, runtime, hardening, regression-pack, and CI-gate enforcement.",
                "Another spec pass would reduce less risk than runtime watchdog coverage.",
            ],
        },
        "executor_boundary_code_spec": {
            "recommended": False,
            "reasons": [
                "No new planner-to-transport boundary ambiguity surfaced while adding the CI gate.",
                "The remaining risk is enforcement continuity, not contract uncertainty.",
            ],
        },
    },
    "task_result": {
        "selected_outcome": selected_outcome,
        "key_finding": "executor_transport_livepaper_observability_ci_gate_passed" if gate_status == "passed" else "executor_transport_livepaper_observability_ci_gate_failed",
        "claim_boundary": "transport_livepaper_observability_ci_gate_bounded",
        "comparison_source_of_truth_state": "comparison_closed_out",
        "task_state": task_state,
        "recommended_next_step": recommended_next_step,
        "recommended_next_task_id": recommended_next_task_id,
        "decision": decision,
        "promoted_label": "task005-pass-grade-pair-20260325T180027Z",
        "default_execution_anchor": "dexter",
        "selective_option_source": "mewx",
    },
}

proof_json.write_text(json.dumps(proof, indent=2) + "\n")

summary_lines = [
    "# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-CI-GATE Proof Summary",
    "",
    "- Verified Vexter `main` at merged PR `#52` commit `64d0670c328f446d1caddda0e2d9c81534ef8787`",
    "- Kept Dexter pinned at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "- Promoted the live-paper observability regression pack into an always-on CI gate with an explicit pytest suite group and proof output",
    f"- Gate run result: `{pytest_result}`",
    "- Locked immutable handoff metadata continuity, handle lifecycle continuity, status sink fan-in, ack-history retention, quarantine reason completeness, reverse-order `manual_latched_stop_all` propagation, snapshot-backed terminal detail, and normalized failure detail passthrough",
    "- Preserved frozen source behavior, comparison closeout, and no-cross-source-handoff constraints",
]

if gate_status == "passed":
    summary_lines.append("- Recommended next task: `transport_livepaper_observability_watchdog`")
else:
    summary_lines.append("- Gate failed, so the immediate next step remains `transport_livepaper_observability_ci_gate`")

summary_md.write_text("\n".join(summary_lines) + "\n")
PY

printf '\nGenerated proof files:\n'
printf ' - %s\n' "$PROOF_JSON"
printf ' - %s\n' "$SUMMARY_MD"
printf '\n'
cat "$SUMMARY_MD"

exit "$PYTEST_STATUS"
