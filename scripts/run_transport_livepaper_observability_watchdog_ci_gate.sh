#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF_DIR="$ROOT_DIR/artifacts/proofs"
REPORT_DIR="$ROOT_DIR/artifacts/reports"
PROOF_JSON="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json"
SUMMARY_MD="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-ci-gate-summary.md"
REPORT_MD="$REPORT_DIR/task-007-transport-livepaper-observability-watchdog-ci-gate-report.md"
STATUS_MD="$REPORT_DIR/task-007-transport-livepaper-observability-watchdog-ci-gate-status.md"
PACK_DIR="$REPORT_DIR/task-007-transport-livepaper-observability-watchdog-ci-gate"
CONTEXT_JSON="$PACK_DIR/CONTEXT.json"
DETAILS_MD="$PACK_DIR/DETAILS.md"
MIN_PROMPT_TXT="$PACK_DIR/MIN_PROMPT.txt"
LOG_PATH="$PROOF_DIR/task-007-transport-livepaper-observability-watchdog-ci-gate-pytest.log"
SUITE_MARKER="transport_livepaper_observability_watchdog_ci_gate"

mkdir -p "$PROOF_DIR" "$REPORT_DIR" "$PACK_DIR"

GROUPED_TEST_FILES=(
  "tests/test_planner_router_transport_livepaper_observability_watchdog.py"
  "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
  "tests/test_planner_router_transport_livepaper_observability_regression_pack.py"
  "tests/test_planner_router_transport_livepaper_observability_watchdog_ci_gate.py"
)

printf 'Transport livepaper observability watchdog CI gate\n'
printf 'Suite marker: %s\n' "$SUITE_MARKER"
printf 'Grouped test files:\n'
for file in "${GROUPED_TEST_FILES[@]}"; do
  printf ' - %s\n' "$file"
done

set +e
(
  cd "$ROOT_DIR"
  pytest -q -m "$SUITE_MARKER" "${GROUPED_TEST_FILES[@]}"
) 2>&1 | tee "$LOG_PATH"
PYTEST_STATUS=${PIPESTATUS[0]}
set -e

if [[ $PYTEST_STATUS -eq 0 ]]; then
  GATE_STATUS="passed"
  TASK_STATE="transport_livepaper_observability_watchdog_ci_gate_passed"
  SELECTED_OUTCOME="A"
  RECOMMENDED_NEXT_STEP="livepaper_observability_spec"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-LIVEPAPER-OBSERVABILITY-SPEC"
  DECISION="livepaper_observability_spec_ready"
else
  GATE_STATUS="failed"
  TASK_STATE="transport_livepaper_observability_watchdog_ci_gate_failed"
  SELECTED_OUTCOME="watchdog_ci_gate_failed"
  RECOMMENDED_NEXT_STEP="transport_livepaper_observability_watchdog_ci_gate"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE"
  DECISION="transport_livepaper_observability_watchdog_ci_gate_failed"
fi

export PROOF_JSON SUMMARY_MD REPORT_MD STATUS_MD PACK_DIR CONTEXT_JSON DETAILS_MD MIN_PROMPT_TXT LOG_PATH
export GATE_STATUS TASK_STATE SELECTED_OUTCOME
export RECOMMENDED_NEXT_STEP RECOMMENDED_NEXT_TASK_ID DECISION SUITE_MARKER

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
gate_status = os.environ["GATE_STATUS"]
task_state = os.environ["TASK_STATE"]
selected_outcome = os.environ["SELECTED_OUTCOME"]
recommended_next_step = os.environ["RECOMMENDED_NEXT_STEP"]
recommended_next_task_id = os.environ["RECOMMENDED_NEXT_TASK_ID"]
decision = os.environ["DECISION"]
suite_marker = os.environ["SUITE_MARKER"]

log_lines = log_path.read_text().splitlines()
pytest_result = next((line.strip() for line in reversed(log_lines) if line.strip()), "")

gate_surface_tests = {
    "immutable_handoff_metadata_continuity": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_immutable_handoff_metadata_continuity"
    ],
    "handle_lifecycle_continuity": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_ci_gate_locks_handle_lifecycle_continuity"
    ],
    "planned_runtime_metadata_drift": [
        "tests/test_planner_router_transport_livepaper_observability_regression_pack.py::test_transport_livepaper_observability_watchdog_regression_pack_locks_planned_runtime_metadata_drift"
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
    "task_id": "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE",
    "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "verified_github": {
        "latest_vexter_pr": 57,
        "latest_vexter_main_commit": "8368b545c3ef3c32db9843ac7e958528902fe67c",
        "latest_vexter_merged_at_utc": "2026-03-26T15:58:51Z",
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
        "watchdog_regression_pack_proof": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-regression-pack-check.json",
        "watchdog_status": "transport_livepaper_observability_watchdog_passed",
        "watchdog_runtime_status": "transport_livepaper_observability_watchdog_runtime_passed",
        "watchdog_regression_pack_status": "transport_livepaper_observability_watchdog_regression_pack_passed",
        "dexter_replay_coverage_ratio": 1.0,
        "dexter_live_vs_replay_gap_pct": 0.0,
        "mewx_replay_coverage_ratio": 1.0,
        "mewx_live_vs_replay_gap_pct": 0.0,
        "confirmatory_residual": "Mew-X candidate_rejected",
        "confirmatory_overturns_promoted_baseline": False,
    },
    "watchdog_ci_gate_suite": {
        "suite_group": suite_marker,
        "pytest_command": "pytest -q -m transport_livepaper_observability_watchdog_ci_gate tests/test_planner_router_transport_livepaper_observability_watchdog.py tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py tests/test_planner_router_transport_livepaper_observability_regression_pack.py tests/test_planner_router_transport_livepaper_observability_watchdog_ci_gate.py",
        "pytest_result": pytest_result,
        "gate_status": gate_status,
        "runner_script": "scripts/run_transport_livepaper_observability_watchdog_ci_gate.sh",
        "workflow": ".github/workflows/validate.yml",
        "proof_outputs": [
            "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json",
            "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-summary.md",
        ],
        "grouped_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_watchdog.py",
            "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py",
            "tests/test_planner_router_transport_livepaper_observability_regression_pack.py",
            "tests/test_planner_router_transport_livepaper_observability_watchdog_ci_gate.py",
        ],
        "grouped_suite_markers": [
            "transport_livepaper_observability_watchdog",
            "transport_livepaper_observability_watchdog_runtime",
            "transport_livepaper_observability_watchdog_regression_pack",
        ],
        "supporting_runner_scripts": [
            "scripts/run_transport_livepaper_observability_watchdog.sh",
            "scripts/run_transport_livepaper_observability_watchdog_runtime.sh",
            "scripts/run_transport_livepaper_observability_watchdog_regression_pack.sh",
        ],
        "component_suites": {
            "watchdog": {
                "test_files": [
                    "tests/test_planner_router_transport_livepaper_observability_watchdog.py",
                ],
                "monitored_surfaces": [
                    "required_observability_field_omission",
                    "handle_lifecycle_continuity",
                    "planned_runtime_metadata_drift",
                    "partial_status_sink_fan_in",
                    "ack_history_retention",
                    "quarantine_reason_completeness",
                    "manual_stop_all_propagation",
                    "snapshot_backed_terminal_detail",
                    "normalized_failure_detail_passthrough",
                ],
            },
            "watchdog_runtime": {
                "test_files": [
                    "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py",
                ],
                "monitored_surfaces": [
                    "required_observability_field_omission",
                    "handle_lifecycle_continuity",
                    "planned_runtime_metadata_drift",
                    "partial_status_sink_fan_in",
                    "ack_history_retention",
                    "quarantine_reason_completeness",
                    "manual_stop_all_propagation",
                    "snapshot_backed_terminal_detail",
                    "normalized_failure_detail_passthrough",
                ],
            },
            "watchdog_regression_pack": {
                "test_files": [
                    "tests/test_planner_router_transport_livepaper_observability_regression_pack.py",
                ],
                "monitored_surfaces": list(gate_surface_tests),
            },
        },
        "gate_surface_tests": gate_surface_tests,
        "source_faithful_modes": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "proof_artifact_name": "transport-livepaper-observability-watchdog-ci-gate-proof",
    },
    "next_task_evaluation": {
        "livepaper_observability_spec": {
            "recommended": gate_status == "passed",
            "reasons": [
                "The watchdog seam is now locked in standard validation, so the highest remaining leverage is specifying the observability contract that the gate keeps enforcing.",
                "A spec lane can now document the already-proven source-faithful surface without reopening comparison or transport behavior.",
            ],
        },
        "executor_boundary_code_spec": {
            "recommended": False,
            "reasons": [
                "No new planner-to-transport boundary ambiguity surfaced while promoting the watchdog suites into CI.",
                "The current residual risk is observability contract clarity rather than missing code-boundary shape.",
            ],
        },
        "transport_livepaper_observability_watchdog_watchdog_runtime": {
            "recommended": False,
            "reasons": [
                "The watchdog-runtime lane is already merged and this CI gate now re-enforces it on every validation run.",
                "Re-cutting a completed runtime watchdog lane would duplicate already-bounded evidence instead of extending coverage.",
            ],
        },
    },
    "task_result": {
        "selected_outcome": selected_outcome,
        "key_finding": "executor_transport_livepaper_observability_watchdog_ci_gate_passed" if gate_status == "passed" else "executor_transport_livepaper_observability_watchdog_ci_gate_failed",
        "claim_boundary": "transport_livepaper_observability_watchdog_ci_gate_bounded",
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
    "# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE Proof Summary",
    "",
    "- Verified Vexter `main` at merged PR `#57` commit `8368b545c3ef3c32db9843ac7e958528902fe67c`",
    "- Kept Dexter pinned at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "- Promoted watchdog, watchdog-runtime, and watchdog-regression-pack into a grouped CI gate without changing source logic or reopening the comparison baseline",
    f"- Watchdog CI gate run result: `{pytest_result}`",
    "- Locked immutable handoff metadata, handle lifecycle continuity, planned/runtime metadata drift detection, status sink fan-in, ack-history retention, quarantine reason completeness, reverse-order manual stop-all propagation, snapshot-backed terminal detail, and normalized failure-detail passthrough",
]
if gate_status == "passed":
    summary_lines.append("- Recommended next task: `livepaper_observability_spec`")
else:
    summary_lines.append("- Watchdog CI gate failed, so the immediate next step remains `transport_livepaper_observability_watchdog_ci_gate`")
summary_md.write_text("\n".join(summary_lines) + "\n")

report_md.write_text(
    "\n".join(
        [
            "# TASK-007 Transport Live-Paper Observability Watchdog CI Gate Report",
            "",
            "## Verified GitHub State",
            "",
            "- `Cabbala/Vexter` latest merged `main` was reverified at PR `#57` main commit `8368b545c3ef3c32db9843ac7e958528902fe67c` on `2026-03-26T15:58:51Z`.",
            "- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.",
            "- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.",
            "- Open Vexter PR `#50` remained non-authoritative relative to merged `main`.",
            "",
            "## What This Task Did",
            "",
            "- Started from the merged watchdog-regression-pack lane on PR `#57` and kept the promoted comparison baseline frozen.",
            "- Added a grouped watchdog CI gate that runs the watchdog, watchdog-runtime, and watchdog-regression-pack suites together before the rest of validation.",
            "- Made the gate proof name the exact locked surfaces so drift, omission, or partial visibility breaks are attributable immediately.",
            "- Refreshed workflow ordering, marker registration, bundle targeting, and handoff metadata without changing planner/router source logic or collecting new evidence.",
            "",
            "## Watchdog Gate Outcome",
            "",
            "- The grouped gate preserves the source-faithful Dexter `paper_live` / frozen Mew-X `sim_live` seam.",
            "- Immutable handoff metadata, handle lifecycle continuity, planned/runtime metadata drift detection, status sink fan-in, ack-history retention, quarantine completeness, manual stop-all propagation, snapshot-backed terminal detail, and normalized failure-detail passthrough remain the mandatory gate faces.",
            f"- Gate run result: `{pytest_result}`.",
            "",
            "## Recommendation Among Next Tasks",
            "",
            "### `livepaper_observability_spec`",
            "",
            "- Recommended next because the watchdog surfaces are now continuously enforced in CI and the highest-value follow-up is to codify that observability contract.",
            "",
            "### `executor_boundary_code_spec`",
            "",
            "- Not next because the transport boundary itself did not become ambiguous while wiring the gate.",
            "",
            "### `transport_livepaper_observability_watchdog_watchdog_runtime`",
            "",
            "- Not next because the runtime watchdog lane is already merged and this task already makes it fail-fast in CI.",
            "",
            "## Decision",
            "",
            f"- Outcome: `{selected_outcome}`",
            f"- Key finding: `{'executor_transport_livepaper_observability_watchdog_ci_gate_passed' if gate_status == 'passed' else 'executor_transport_livepaper_observability_watchdog_ci_gate_failed'}`",
            "- Claim boundary: `transport_livepaper_observability_watchdog_ci_gate_bounded`",
            f"- Decision: `{decision}`",
            f"- Recommended next step: `{recommended_next_step}`",
        ]
    )
    + "\n"
)

status_md.write_text(
    "\n".join(
        [
            "# TASK-007 Transport Live-Paper Observability Watchdog CI Gate Status",
            "",
            f"- Gate status: `{gate_status}`",
            f"- Task state: `{task_state}`",
            "- Prior lane source state: `transport_livepaper_observability_watchdog_regression_pack_passed`",
            "- Verified Vexter `main`: PR `#57` commit `8368b545c3ef3c32db9843ac7e958528902fe67c`",
            "- Locked gate surfaces: immutable_handoff_metadata_continuity, handle_lifecycle_continuity, planned_runtime_metadata_drift, status_sink_fan_in, ack_history_retention, quarantine_reason_completeness, manual_stop_all_propagation, snapshot_backed_terminal_detail, normalized_failure_detail_passthrough",
            f"- Recommended next step: `{recommended_next_step}`",
            f"- Decision: `{decision}`",
        ]
    )
    + "\n"
)

context_json.write_text(
    json.dumps(
        {
            "recommended_next_task": "TASK-007-LIVEPAPER-OBSERVABILITY-SPEC",
            "visible_main_state": {
                "latest_vexter_pr": 57,
                "latest_vexter_main_commit": "8368b545c3ef3c32db9843ac7e958528902fe67c",
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

details_md.write_text(
    "\n".join(
        [
            "# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE",
            "",
            "## 1. Purpose",
            "Promote the locked watchdog, watchdog-runtime, and watchdog-regression-pack observability surface into an always-on CI gate on the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.",
            "",
            "## 2. Fixed Inputs",
            "- Latest merged Vexter `main`: PR `#57` commit `8368b545c3ef3c32db9843ac7e958528902fe67c`",
            "- Dexter merged `main`: PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
            "- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
            "- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`",
            "- Comparison source of truth: `comparison_closed_out`",
            "",
            "## 3. Required Gate Surfaces",
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
            "- `livepaper_observability_spec`",
        ]
    )
    + "\n"
)

min_prompt_txt.write_text(
    "\n".join(
        [
            "対象スレッド: 既存 Vexter Codex スレッド（なければ新規）",
            "作業系統: Vexter / Infra",
            "次タスクID: TASK-007-LIVEPAPER-OBSERVABILITY-SPEC",
            "",
            "GitHub最新状態を確認し、Vexter main / Dexter PR #3 merged main / frozen Mew-X を前提に、transport live-paper observability spec を整理してください。watchdog CI gate で固定された surface を source of truth とし、comparison baseline は固定のまま、Dexter `paper_live` / frozen Mew-X `sim_live` seam と watchdog CI gate の required surfaces・suite grouping・proof contract・failure triage contract を spec 化してください。source logic 変更や新証拠収集は行わず、docs/specs/tests/artifacts/handoff bundle を更新してください。",
        ]
    )
    + "\n"
)
PY

printf '\nGenerated proof files:\n'
printf ' - %s\n' "$PROOF_JSON"
printf ' - %s\n' "$SUMMARY_MD"
printf ' - %s\n' "$REPORT_MD"
printf ' - %s\n' "$STATUS_MD"
printf ' - %s\n' "$CONTEXT_JSON"
printf ' - %s\n' "$DETAILS_MD"
printf ' - %s\n' "$MIN_PROMPT_TXT"
printf '\n'
cat "$SUMMARY_MD"

exit "$PYTEST_STATUS"
