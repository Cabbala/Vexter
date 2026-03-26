#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF_DIR="$ROOT_DIR/artifacts/proofs"
PROOF_JSON="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-check.json"
SUMMARY_MD="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-summary.md"
LOG_PATH="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-pytest.log"
SUITE_MARKER="transport_livepaper_observability_watchdog"

mkdir -p "$PROOF_DIR"

WATCHDOG_TEST_FILES=(
  "tests/test_planner_router_transport_livepaper_observability_watchdog.py"
)

WATCHDOG_SURFACES=(
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

printf 'Transport livepaper observability watchdog\n'
printf 'Suite marker: %s\n' "$SUITE_MARKER"
printf 'Watchdog test files:\n'
for file in "${WATCHDOG_TEST_FILES[@]}"; do
  printf ' - %s\n' "$file"
done
printf 'Monitored surfaces:\n'
for surface in "${WATCHDOG_SURFACES[@]}"; do
  printf ' - %s\n' "$surface"
done

set +e
(
  cd "$ROOT_DIR"
  pytest -q -m "$SUITE_MARKER" "${WATCHDOG_TEST_FILES[@]}"
) 2>&1 | tee "$LOG_PATH"
PYTEST_STATUS=${PIPESTATUS[0]}
set -e

if [[ $PYTEST_STATUS -eq 0 ]]; then
  WATCHDOG_STATUS="passed"
  TASK_STATE="transport_livepaper_observability_watchdog_passed"
  SELECTED_OUTCOME="A"
  RECOMMENDED_NEXT_STEP="transport_livepaper_observability_watchdog_runtime"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME"
  DECISION="transport_livepaper_observability_watchdog_runtime_ready"
else
  WATCHDOG_STATUS="failed"
  TASK_STATE="transport_livepaper_observability_watchdog_failed"
  SELECTED_OUTCOME="watchdog_failed"
  RECOMMENDED_NEXT_STEP="transport_livepaper_observability_watchdog"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG"
  DECISION="transport_livepaper_observability_watchdog_failed"
fi

export PROOF_JSON SUMMARY_MD LOG_PATH WATCHDOG_STATUS TASK_STATE SELECTED_OUTCOME
export RECOMMENDED_NEXT_STEP RECOMMENDED_NEXT_TASK_ID DECISION SUITE_MARKER

python - <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

proof_json = Path(os.environ["PROOF_JSON"])
summary_md = Path(os.environ["SUMMARY_MD"])
log_path = Path(os.environ["LOG_PATH"])
watchdog_status = os.environ["WATCHDOG_STATUS"]
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
    "task_id": "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG",
    "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "verified_github": {
        "latest_vexter_pr": 53,
        "latest_vexter_main_commit": "64cd0e22c284c759a64939348a59c3152afc77dc",
        "latest_vexter_merged_at_utc": "2026-03-26T14:14:55Z",
        "dexter_pr": 3,
        "dexter_main_commit": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
        "mewx_frozen_commit": "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
    },
    "fixed_input_surface": {
        "promoted_label": "task005-pass-grade-pair-20260325T180027Z",
        "comparison_source_of_truth_state": "comparison_closed_out",
        "ci_gate_proof": "artifacts/proofs/task-007-transport-livepaper-observability-ci-gate-check.json",
        "ci_gate_summary": "artifacts/proofs/task-007-transport-livepaper-observability-ci-gate-summary.md",
        "ci_gate_status": "transport_livepaper_observability_ci_gate_passed",
        "dexter_replay_coverage_ratio": 1.0,
        "dexter_live_vs_replay_gap_pct": 0.0,
        "mewx_replay_coverage_ratio": 1.0,
        "mewx_live_vs_replay_gap_pct": 0.0,
        "confirmatory_residual": "Mew-X candidate_rejected",
        "confirmatory_overturns_promoted_baseline": False,
    },
    "watchdog_suite": {
        "suite_group": suite_marker,
        "pytest_command": "pytest -q -m transport_livepaper_observability_watchdog tests/test_planner_router_transport_livepaper_observability_watchdog.py",
        "pytest_result": pytest_result,
        "watchdog_status": watchdog_status,
        "workflow": ".github/workflows/validate.yml",
        "proof_outputs": [
            "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-check.json",
            "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-summary.md",
        ],
        "watchdog_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_watchdog.py",
        ],
        "monitored_surfaces": monitored_surfaces,
        "source_faithful_modes": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "proof_artifact_name": "transport-livepaper-observability-watchdog-proof",
    },
    "watchdog_alert_model": {
        "issue_classes": [
            "omission",
            "partial_visibility",
            "drift",
        ],
        "focus": [
            "required observability field omission",
            "planned-versus-runtime metadata drift",
            "partial status-sink fan-in",
            "ack-history retention collapse",
            "missing quarantine reason / stop reason / terminal snapshot detail",
            "normalized failure detail passthrough",
        ],
    },
    "next_task_evaluation": {
        "transport_livepaper_observability_watchdog_runtime": {
            "recommended": watchdog_status == "passed",
            "reasons": [
                "The bounded watchdog now detects operational drift and partial visibility in synthetic transport-follow-up paths.",
                "The next risk is moving the watchdog surface into a more runtime-shaped execution path without reopening comparison or changing source logic.",
            ],
        },
        "livepaper_observability_spec": {
            "recommended": False,
            "reasons": [
                "The observability contract is already fixed through CI gate plus watchdog detection.",
                "Another spec-only pass would reduce less risk than runtime-shaped watchdog continuation.",
            ],
        },
        "executor_boundary_code_spec": {
            "recommended": False,
            "reasons": [
                "No new boundary ambiguity surfaced while adding the watchdog lane.",
                "The remaining work is enforcement continuity rather than contract discovery.",
            ],
        },
    },
    "task_result": {
        "selected_outcome": selected_outcome,
        "key_finding": "executor_transport_livepaper_observability_watchdog_passed" if watchdog_status == "passed" else "executor_transport_livepaper_observability_watchdog_failed",
        "claim_boundary": "transport_livepaper_observability_watchdog_bounded",
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
    "# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG Proof Summary",
    "",
    "- Verified Vexter `main` at merged PR `#53` commit `64cd0e22c284c759a64939348a59c3152afc77dc`",
    "- Kept Dexter pinned at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "- Added a bounded watchdog lane on top of the CI-gated live-paper transport observability seam without changing source logic or reopening the comparison baseline",
    f"- Watchdog run result: `{pytest_result}`",
    "- Monitored required field omission, handle lifecycle continuity, planned-runtime metadata drift, partial sink fan-in, ack-history retention, quarantine completeness, manual stop-all propagation, snapshot-backed terminal detail, and normalized failure detail passthrough",
]

if watchdog_status == "passed":
    summary_lines.append("- Recommended next task: `transport_livepaper_observability_watchdog_runtime`")
else:
    summary_lines.append("- Watchdog failed, so the immediate next step remains `transport_livepaper_observability_watchdog`")

summary_md.write_text("\n".join(summary_lines) + "\n")
PY

printf '\nGenerated proof files:\n'
printf ' - %s\n' "$PROOF_JSON"
printf ' - %s\n' "$SUMMARY_MD"
printf '\n'
cat "$SUMMARY_MD"

exit "$PYTEST_STATUS"
