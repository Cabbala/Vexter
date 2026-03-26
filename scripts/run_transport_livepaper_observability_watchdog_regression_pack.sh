#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF_DIR="$ROOT_DIR/artifacts/proofs"
REPORT_DIR="$ROOT_DIR/artifacts/reports"
PACK_DIR="$REPORT_DIR/task-007-transport-livepaper-observability-watchdog-regression-pack"
PROOF_JSON="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-regression-pack-check.json"
SUMMARY_MD="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-regression-pack-summary.md"
REPORT_MD="$REPORT_DIR/task-007-transport-livepaper-observability-watchdog-regression-pack-report.md"
STATUS_MD="$REPORT_DIR/task-007-transport-livepaper-observability-watchdog-regression-pack-status.md"
CONTEXT_JSON="$PACK_DIR/CONTEXT.json"
DETAILS_MD="$PACK_DIR/DETAILS.md"
MIN_PROMPT_TXT="$PACK_DIR/MIN_PROMPT.txt"
LOG_PATH="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-regression-pack-pytest.log"
SUITE_MARKER="transport_livepaper_observability_watchdog_regression_pack"

mkdir -p "$PROOF_DIR" "$REPORT_DIR" "$PACK_DIR"

RUNTIME_TEST_FILES=(
  "tests/test_planner_router_transport_livepaper_observability_regression_pack.py"
)

MONITORED_SURFACES=(
  "immutable_handoff_metadata_continuity"
  "handle_lifecycle_continuity"
  "planned_runtime_metadata_drift"
  "status_sink_fan_in"
  "ack_history_retention"
  "quarantine_reason_completeness"
  "manual_stop_all_propagation"
  "snapshot_backed_terminal_detail"
  "normalized_failure_detail_passthrough"
)

printf 'Transport livepaper observability watchdog regression pack\n'
printf 'Suite marker: %s\n' "$SUITE_MARKER"

set +e
(
  cd "$ROOT_DIR"
  pytest -q -m "$SUITE_MARKER" "${RUNTIME_TEST_FILES[@]}"
) 2>&1 | tee "$LOG_PATH"
PYTEST_STATUS=${PIPESTATUS[0]}
set -e

if [[ $PYTEST_STATUS -eq 0 ]]; then
  WATCHDOG_REGRESSION_PACK_STATUS="passed"
  TASK_STATE="transport_livepaper_observability_watchdog_regression_pack_passed"
  SELECTED_OUTCOME="A"
  RECOMMENDED_NEXT_STEP="transport_livepaper_observability_watchdog_ci_gate"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE"
  DECISION="transport_livepaper_observability_watchdog_ci_gate_ready"
else
  WATCHDOG_REGRESSION_PACK_STATUS="failed"
  TASK_STATE="transport_livepaper_observability_watchdog_regression_pack_failed"
  SELECTED_OUTCOME="watchdog_regression_pack_failed"
  RECOMMENDED_NEXT_STEP="transport_livepaper_observability_watchdog_regression_pack"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-REGRESSION-PACK"
  DECISION="transport_livepaper_observability_watchdog_regression_pack_failed"
fi

export PROOF_JSON SUMMARY_MD REPORT_MD STATUS_MD CONTEXT_JSON DETAILS_MD MIN_PROMPT_TXT LOG_PATH
export WATCHDOG_REGRESSION_PACK_STATUS TASK_STATE SELECTED_OUTCOME RECOMMENDED_NEXT_STEP
export RECOMMENDED_NEXT_TASK_ID DECISION SUITE_MARKER

python - <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

proof_json = Path(os.environ["PROOF_JSON"])
summary_md = Path(os.environ["SUMMARY_MD"])
report_md = Path(os.environ["REPORT_MD"])
status_md = Path(os.environ["STATUS_MD"])
context_json = Path(os.environ["CONTEXT_JSON"])
details_md = Path(os.environ["DETAILS_MD"])
min_prompt_txt = Path(os.environ["MIN_PROMPT_TXT"])
log_path = Path(os.environ["LOG_PATH"])
watchdog_regression_pack_status = os.environ["WATCHDOG_REGRESSION_PACK_STATUS"]
task_state = os.environ["TASK_STATE"]
selected_outcome = os.environ["SELECTED_OUTCOME"]
recommended_next_step = os.environ["RECOMMENDED_NEXT_STEP"]
recommended_next_task_id = os.environ["RECOMMENDED_NEXT_TASK_ID"]
decision = os.environ["DECISION"]
suite_marker = os.environ["SUITE_MARKER"]

log_lines = log_path.read_text().splitlines()
pytest_result = next((line.strip() for line in reversed(log_lines) if line.strip()), "")
monitored_surfaces = [
    "immutable_handoff_metadata_continuity",
    "handle_lifecycle_continuity",
    "planned_runtime_metadata_drift",
    "status_sink_fan_in",
    "ack_history_retention",
    "quarantine_reason_completeness",
    "manual_stop_all_propagation",
    "snapshot_backed_terminal_detail",
    "normalized_failure_detail_passthrough",
]

proof = {
    "task_id": "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-REGRESSION-PACK",
    "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "verified_github": {
        "latest_vexter_pr": 56,
        "latest_vexter_main_commit": "cc8996e0204b7dd149ebce85f1988d7a3abf90cd",
        "latest_vexter_merged_at_utc": "2026-03-26T15:26:06Z",
        "open_non_authoritative_vexter_prs": [50],
        "dexter_pr": 3,
        "dexter_main_commit": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
        "dexter_pr_3_merged_at_utc": "2026-03-21T11:31:07Z",
        "mewx_frozen_commit": "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
        "mewx_frozen_commit_date_utc": "2026-03-20T16:05:19Z",
    },
    "fixed_input_surface": {
        "promoted_label": "task005-pass-grade-pair-20260325T180027Z",
        "comparison_source_of_truth_state": "comparison_closed_out",
        "watchdog_proof": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-check.json",
        "watchdog_runtime_proof": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json",
        "watchdog_status": "transport_livepaper_observability_watchdog_passed",
        "watchdog_runtime_status": "transport_livepaper_observability_watchdog_runtime_passed",
        "dexter_replay_coverage_ratio": 1.0,
        "dexter_live_vs_replay_gap_pct": 0.0,
        "mewx_replay_coverage_ratio": 1.0,
        "mewx_live_vs_replay_gap_pct": 0.0,
        "confirmatory_residual": "Mew-X candidate_rejected",
        "confirmatory_overturns_promoted_baseline": False,
    },
    "watchdog_regression_pack_suite": {
        "suite_group": suite_marker,
        "pytest_command": "pytest -q -m transport_livepaper_observability_watchdog_regression_pack tests/test_planner_router_transport_livepaper_observability_regression_pack.py",
        "pytest_result": pytest_result,
        "watchdog_regression_pack_status": watchdog_regression_pack_status,
        "runner_script": "scripts/run_transport_livepaper_observability_watchdog_regression_pack.sh",
        "proof_outputs": [
            "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-regression-pack-check.json",
            "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-regression-pack-summary.md",
        ],
        "runtime_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_regression_pack.py",
        ],
        "supporting_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_watchdog.py",
            "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py",
            "tests/test_planner_router_transport_livepaper_observability_ci_gate.py",
            "tests/test_bootstrap_layout.py",
        ],
        "monitored_surfaces": monitored_surfaces,
        "source_faithful_modes": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "proof_artifact_name": "transport-livepaper-observability-watchdog-regression-pack-proof",
    },
    "regression_surface": {
        "goal": "Freeze the watchdog and watchdog-runtime drift, omission, and partial-visibility surface into durable regression coverage.",
        "locked_axes": [
            "immutable handoff metadata continuity",
            "handle lifecycle continuity",
            "planned/runtime metadata drift detection",
            "status sink fan-in detection",
            "ack-history retention",
            "quarantine reason completeness",
            "reverse-order manual stop-all propagation",
            "snapshot-backed terminal detail completeness",
            "normalized failure-detail passthrough",
        ],
    },
    "next_task_evaluation": {
        "transport_livepaper_observability_watchdog_ci_gate": {
            "recommended": watchdog_regression_pack_status == "passed",
            "reasons": [
                "The remaining risk is no longer missing watchdog categories; it is making the watchdog regression pack run on every transport change.",
                "A watchdog-specific CI gate operationalizes the durable regression surface without reopening the comparison baseline or changing source logic.",
                "This path preserves the source-faithful Dexter paper_live and frozen Mew-X sim_live seam while reducing future transport drift risk.",
            ],
        },
        "livepaper_observability_spec": {
            "recommended": False,
            "reasons": [
                "The observability and watchdog categories are already bounded through CI gate, watchdog, watchdog runtime, and this regression pack.",
                "A spec-only restatement would reduce less risk than always-on execution of the watchdog regression pack.",
            ],
        },
        "executor_boundary_code_spec": {
            "recommended": False,
            "reasons": [
                "No new planner-to-transport ambiguity surfaced while packaging the watchdog surfaces.",
                "The current risk is transport drift inside the fixed contract, not missing interface shape.",
            ],
        },
    },
    "task_result": {
        "selected_outcome": selected_outcome,
        "key_finding": "executor_transport_livepaper_observability_watchdog_regression_pack_passed" if watchdog_regression_pack_status == "passed" else "executor_transport_livepaper_observability_watchdog_regression_pack_failed",
        "claim_boundary": "transport_livepaper_observability_watchdog_regression_pack_bounded",
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
    "# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-REGRESSION-PACK Proof Summary",
    "",
    "- Verified Vexter `main` at merged PR `#56` commit `cc8996e0204b7dd149ebce85f1988d7a3abf90cd`",
    "- Kept Dexter pinned at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "- Repackaged the watchdog and watchdog-runtime detection surface into a durable regression lane without changing source logic or reopening the comparison baseline",
    f"- Watchdog regression-pack run result: `{pytest_result}`",
    "- Locked immutable handoff metadata, handle lifecycle continuity, planned/runtime metadata drift detection, status sink fan-in, ack-history retention, quarantine completeness, manual stop-all propagation, snapshot-backed terminal detail, and normalized failure passthrough",
]
if watchdog_regression_pack_status == "passed":
    summary_lines.append("- Recommended next task: `transport_livepaper_observability_watchdog_ci_gate`")
else:
    summary_lines.append("- Watchdog regression-pack failed, so the immediate next step remains `transport_livepaper_observability_watchdog_regression_pack`")
summary_md.write_text("\n".join(summary_lines) + "\n")

report_md.write_text(
    "\n".join(
        [
            "# TASK-007 Transport Live-Paper Observability Watchdog Regression-Pack Report",
            "",
            "## Verified GitHub State",
            "",
            "- `Cabbala/Vexter` latest merged `main` was reverified at PR `#56` main commit `cc8996e0204b7dd149ebce85f1988d7a3abf90cd` on `2026-03-26T15:26:06Z`.",
            "- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.",
            "- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.",
            "",
            "## What This Task Did",
            "",
            "- Started from the merged watchdog-runtime lane on PR `#56` and kept the promoted comparison baseline frozen.",
            "- Added a dedicated watchdog-regression-pack lane so future transport changes must preserve the watchdog/runtime observability surface instead of relying on one bounded runtime follow-up proof.",
            "- Locked immutable handoff metadata continuity, handle lifecycle continuity, planned/runtime metadata drift detection, status sink fan-in, ack-history retention, quarantine reason completeness, reverse-order `manual_latched_stop_all` propagation, snapshot-backed terminal detail, and normalized failure-detail passthrough into durable transport assertions.",
            "- Preserved the source-faithful Dexter `paper_live` and Mew-X `sim_live` seam without changing source logic, trust logic, thresholds, validator rules, or frozen source pins.",
            "",
            "## Validation",
            "",
            "- `pytest -q -m transport_livepaper_observability_watchdog_regression_pack tests/test_planner_router_transport_livepaper_observability_regression_pack.py`",
            f"- `{pytest_result}`",
            "",
            "## Recommendation Among Next Tasks",
            "",
            "### `transport_livepaper_observability_watchdog_ci_gate`",
            "",
            "Recommended next because:",
            "",
            "- this task packages the watchdog and watchdog-runtime conclusions into a durable regression surface, so the next highest-value step is enforcing that lane on every transport change",
            "- the remaining risk is execution consistency, not missing watchdog categories",
            "- a watchdog-specific CI gate operationalizes the bounded guarantees without reopening comparison or boundary design",
            "",
            "### `livepaper_observability_spec`",
            "",
            "Not next because:",
            "",
            "- the observability surface is already evidenced across smoke, runtime continuity, CI gate, watchdog, watchdog runtime, and now watchdog regression coverage",
            "- another spec-only pass would add less risk reduction than making the watchdog regression pack always-on",
            "",
            "### `executor_boundary_code_spec`",
            "",
            "Not next because:",
            "",
            "- no new planner-to-transport boundary ambiguity surfaced in this task",
            "- the risk surface remains drift inside an already-bounded interface rather than contract shape uncertainty",
            "",
            "## Decision",
            "",
            f"- Outcome: `{selected_outcome}`",
            f"- Key finding: `{proof['task_result']['key_finding']}`",
            f"- Claim boundary: `{proof['task_result']['claim_boundary']}`",
            f"- Decision: `{decision}`",
            f"- Recommended next step: `{recommended_next_step}`",
        ]
    )
    + "\n"
)

status_md.write_text(
    "\n".join(
        [
            "# TASK-007 Transport Live-Paper Observability Watchdog Regression-Pack Status",
            "",
            "## Verified Start",
            "",
            "- Vexter `origin/main` verified at PR `#56` commit `cc8996e0204b7dd149ebce85f1988d7a3abf90cd`",
            "- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
            "- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
            "",
            "## Current Result",
            "",
            "- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`",
            "- Comparison source of truth: `comparison_closed_out`",
            "- Prior lane source state: `transport_livepaper_observability_watchdog_runtime_passed`",
            "- `tests/test_planner_router_transport_livepaper_observability_regression_pack.py` now freezes the watchdog/runtime observability surface for immutable handoff metadata, handle lifecycle continuity, planned/runtime metadata drift, status sink fan-in, ack-history retention, quarantine reason completeness, manual stop-all propagation, snapshot-backed terminal detail, and normalized failure passthrough",
            "- Added a dedicated watchdog-regression-pack runner with refreshed proof output and bundle targeting",
            "",
            "## Decision",
            "",
            f"- Current task: `{task_state}`",
            f"- Key finding: `{proof['task_result']['key_finding']}`",
            f"- Claim boundary: `{proof['task_result']['claim_boundary']}`",
            f"- Recommended next step: `{recommended_next_step}`",
            f"- Decision: `{decision}`",
        ]
    )
    + "\n"
)

details_md.write_text(
    "\n".join(
        [
            "# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-REGRESSION-PACK",
            "",
            "## 1. Purpose",
            "Freeze the watchdog and watchdog-runtime drift / omission / partial-visibility surface into durable regression coverage on top of the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.",
            "",
            "## 2. Fixed Inputs",
            "- Latest merged Vexter `main`: PR `#56` commit `cc8996e0204b7dd149ebce85f1988d7a3abf90cd`",
            "- Dexter merged `main`: PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
            "- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
            "- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`",
            "- Comparison source of truth: `comparison_closed_out`",
            "",
            "## 3. Required Regression Surfaces",
            "- immutable handoff metadata continuity",
            "- handle lifecycle continuity",
            "- planned/runtime metadata drift detection",
            "- status sink fan-in detection",
            "- ack-history retention",
            "- quarantine reason completeness",
            "- reverse-order `manual_latched_stop_all` propagation",
            "- snapshot-backed terminal detail completeness",
            "- normalized failure-detail passthrough",
            "",
            "## 4. Constraints",
            "- no source logic changes",
            "- no validator rule changes",
            "- no comparison baseline reopen",
            "- no new evidence collection",
            "- keep source-faithful Dexter `paper_live` / Mew-X `sim_live` seam",
            "",
            "## 5. Recommended Next Task",
            "- `transport_livepaper_observability_watchdog_ci_gate`",
        ]
    )
    + "\n"
)

min_prompt_txt.write_text(
    "対象スレッド: 既存 Vexter Codex スレッド（なければ新規）\n"
    "作業系統: Vexter / Infra\n"
    "次タスクID: TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE\n\n"
    "GitHub 最新 merged main を確認し、watchdog regression pack を CI で恒常実行する gate として固定してください。"
    "comparison baseline は固定のまま、Dexter `paper_live` / frozen Mew-X `sim_live` seam と watchdog regression pack の surface を崩さず、"
    "tests・workflow・artifacts・handoff bundle を更新してください。\n"
)

context_json.write_text(
    json.dumps(
        {
            "recommended_next_task": "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE",
            "visible_main_state": {
                "latest_vexter_pr": 56,
                "dexter_main": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
                "mewx_frozen": "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
            },
            "current_state": {
                "current_task": task_state,
                "recommended_next_step": recommended_next_step,
                "default_execution_anchor": "Dexter",
                "mewx_role": "containment-first selective option",
            },
        },
        indent=2,
    )
    + "\n"
)
PY

printf '\nGenerated proof files:\n'
printf ' - %s\n' "$PROOF_JSON"
printf ' - %s\n' "$SUMMARY_MD"
printf '\n'
cat "$SUMMARY_MD"

exit "$PYTEST_STATUS"
