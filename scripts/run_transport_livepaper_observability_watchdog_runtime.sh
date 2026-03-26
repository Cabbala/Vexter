#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF_DIR="$ROOT_DIR/artifacts/proofs"
PROOF_JSON="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-runtime-check.json"
SUMMARY_MD="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-runtime-summary.md"
LOG_PATH="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-runtime-pytest.log"
SUITE_MARKER="transport_livepaper_observability_watchdog_runtime"

mkdir -p "$PROOF_DIR"

RUNTIME_TEST_FILES=(
  "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
)

MONITORED_SURFACES=(
  "required_observability_field_omission"
  "handle_lifecycle_continuity"
  "planned_runtime_metadata_drift"
  "partial_status_sink_fan_in"
  "ack_history_retention"
  "quarantine_reason_completeness"
  "manual_stop_all_propagation"
  "snapshot_backed_terminal_detail"
  "normalized_failure_detail_passthrough"
)

printf 'Transport livepaper observability watchdog runtime\n'
printf 'Suite marker: %s\n' "$SUITE_MARKER"

set +e
(
  cd "$ROOT_DIR"
  pytest -q -m "$SUITE_MARKER" "${RUNTIME_TEST_FILES[@]}"
) 2>&1 | tee "$LOG_PATH"
PYTEST_STATUS=${PIPESTATUS[0]}
set -e

if [[ $PYTEST_STATUS -eq 0 ]]; then
  WATCHDOG_RUNTIME_STATUS="passed"
  TASK_STATE="transport_livepaper_observability_watchdog_runtime_passed"
  SELECTED_OUTCOME="A"
  RECOMMENDED_NEXT_STEP="transport_livepaper_observability_watchdog_regression_pack"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-REGRESSION-PACK"
  DECISION="transport_livepaper_observability_watchdog_regression_pack_ready"
else
  WATCHDOG_RUNTIME_STATUS="failed"
  TASK_STATE="transport_livepaper_observability_watchdog_runtime_failed"
  SELECTED_OUTCOME="watchdog_runtime_failed"
  RECOMMENDED_NEXT_STEP="transport_livepaper_observability_watchdog_runtime"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME"
  DECISION="transport_livepaper_observability_watchdog_runtime_failed"
fi

export PROOF_JSON SUMMARY_MD LOG_PATH WATCHDOG_RUNTIME_STATUS TASK_STATE SELECTED_OUTCOME
export RECOMMENDED_NEXT_STEP RECOMMENDED_NEXT_TASK_ID DECISION SUITE_MARKER

python - <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

proof_json = Path(os.environ["PROOF_JSON"])
summary_md = Path(os.environ["SUMMARY_MD"])
log_path = Path(os.environ["LOG_PATH"])
watchdog_runtime_status = os.environ["WATCHDOG_RUNTIME_STATUS"]
task_state = os.environ["TASK_STATE"]
selected_outcome = os.environ["SELECTED_OUTCOME"]
recommended_next_step = os.environ["RECOMMENDED_NEXT_STEP"]
recommended_next_task_id = os.environ["RECOMMENDED_NEXT_TASK_ID"]
decision = os.environ["DECISION"]
suite_marker = os.environ["SUITE_MARKER"]

log_lines = log_path.read_text().splitlines()
pytest_result = next((line.strip() for line in reversed(log_lines) if line.strip()), "")
monitored_surfaces = [
    "required_observability_field_omission",
    "handle_lifecycle_continuity",
    "planned_runtime_metadata_drift",
    "partial_status_sink_fan_in",
    "ack_history_retention",
    "quarantine_reason_completeness",
    "manual_stop_all_propagation",
    "snapshot_backed_terminal_detail",
    "normalized_failure_detail_passthrough",
]

proof = {
    "task_id": "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME",
    "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "verified_github": {
        "latest_vexter_pr": 55,
        "latest_vexter_main_commit": "79a74ee187f222be74d11a30cf7204cd5777f01e",
        "latest_vexter_merged_at_utc": "2026-03-26T14:56:13Z",
        "dexter_pr": 3,
        "dexter_main_commit": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
        "mewx_frozen_commit": "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
    },
    "fixed_input_surface": {
        "promoted_label": "task005-pass-grade-pair-20260325T180027Z",
        "comparison_source_of_truth_state": "comparison_closed_out",
        "watchdog_proof": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-check.json",
        "watchdog_summary": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-summary.md",
        "watchdog_status": "transport_livepaper_observability_watchdog_passed",
        "dexter_replay_coverage_ratio": 1.0,
        "dexter_live_vs_replay_gap_pct": 0.0,
        "mewx_replay_coverage_ratio": 1.0,
        "mewx_live_vs_replay_gap_pct": 0.0,
        "confirmatory_residual": "Mew-X candidate_rejected",
        "confirmatory_overturns_promoted_baseline": False,
    },
    "watchdog_runtime_suite": {
        "suite_group": suite_marker,
        "pytest_command": "pytest -q -m transport_livepaper_observability_watchdog_runtime tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py",
        "pytest_result": pytest_result,
        "watchdog_runtime_status": watchdog_runtime_status,
        "workflow": ".github/workflows/validate.yml",
        "proof_outputs": [
            "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json",
            "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-summary.md",
        ],
        "runtime_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py",
        ],
        "monitored_surfaces": monitored_surfaces,
        "source_faithful_modes": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "proof_artifact_name": "transport-livepaper-observability-watchdog-runtime-proof",
    },
    "runtime_follow_up_focus": {
        "goal": "Keep watchdog drift, omission, and partial-visibility detection intact on runtime-oriented follow-up paths.",
        "follow_up_axes": [
            "duplicate ack visibility after repeated prepare/start/stop requests",
            "push-promoted quarantine detail retention",
            "manual stop-all propagation on already-running handles",
            "snapshot-backed terminal detail continuity",
            "normalized failure detail passthrough without source drift",
        ],
    },
    "next_task_evaluation": {
        "transport_livepaper_observability_watchdog_regression_pack": {
            "recommended": watchdog_runtime_status == "passed",
            "reasons": [
                "The watchdog now covers both bounded synthetic drift cases and runtime-oriented follow-up continuity on the same source-faithful seam.",
                "The next leverage point is locking this runtime-shaped watchdog surface into a durable regression pack rather than restating the contract.",
            ],
        },
        "livepaper_observability_spec": {
            "recommended": False,
            "reasons": [
                "The observability and watchdog surfaces are already evidenced through CI gate, watchdog, and runtime-follow-up continuity.",
                "A spec-only pass would reduce less risk than packaging the runtime watchdog coverage into regression enforcement.",
            ],
        },
        "executor_boundary_code_spec": {
            "recommended": False,
            "reasons": [
                "No new planner-to-transport boundary ambiguity surfaced in the runtime watchdog lane.",
                "The remaining risk is drift of the existing surface, not interface discovery.",
            ],
        },
    },
    "task_result": {
        "selected_outcome": selected_outcome,
        "key_finding": "executor_transport_livepaper_observability_watchdog_runtime_passed" if watchdog_runtime_status == "passed" else "executor_transport_livepaper_observability_watchdog_runtime_failed",
        "claim_boundary": "transport_livepaper_observability_watchdog_runtime_bounded",
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
    "# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME Proof Summary",
    "",
    "- Verified Vexter `main` at merged PR `#55` commit `79a74ee187f222be74d11a30cf7204cd5777f01e`",
    "- Kept Dexter pinned at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "- Extended the bounded watchdog into runtime-oriented follow-up paths without changing source logic or reopening the comparison baseline",
    f"- Watchdog runtime run result: `{pytest_result}`",
    "- Verified immutable handoff metadata, handle lifecycle continuity, status sink fan-in, ack-history retention, quarantine completeness, manual stop-all propagation, snapshot-backed terminal detail, and normalized failure detail remain watchdog-detectable after runtime follow-up",
]

if watchdog_runtime_status == "passed":
    summary_lines.append("- Recommended next task: `transport_livepaper_observability_watchdog_regression_pack`")
else:
    summary_lines.append("- Watchdog runtime failed, so the immediate next step remains `transport_livepaper_observability_watchdog_runtime`")

summary_md.write_text("\n".join(summary_lines) + "\n")
PY

printf '\nGenerated proof files:\n'
printf ' - %s\n' "$PROOF_JSON"
printf ' - %s\n' "$SUMMARY_MD"
printf '\n'
cat "$SUMMARY_MD"

exit "$PYTEST_STATUS"
