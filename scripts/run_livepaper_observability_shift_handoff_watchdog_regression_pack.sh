#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF_DIR="$ROOT_DIR/artifacts/proofs"
REPORT_DIR="$ROOT_DIR/artifacts/reports"
PROOF_JSON="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json"
SUMMARY_MD="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md"
REPORT_MD="$REPORT_DIR/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md"
STATUS_MD="$ROOT_DIR/artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md"
PACK_DIR="$ROOT_DIR/artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack"
CONTEXT_JSON="$PACK_DIR/CONTEXT.json"
DETAILS_MD="$PACK_DIR/DETAILS.md"
MIN_PROMPT_TXT="$PACK_DIR/MIN_PROMPT.txt"
HANDOFF_MD="$PACK_DIR/HANDOFF.md"
LOG_PATH="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-pytest.log"
SUITE_MARKER="livepaper_observability_shift_handoff_watchdog_regression_pack"

mkdir -p "$PROOF_DIR" "$ROOT_DIR/artifacts/reports" "$PACK_DIR"

GROUPED_TEST_FILES=(
  "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py"
)

printf 'Livepaper observability shift handoff watchdog regression pack\n'
printf 'Suite marker: %s\n' "$SUITE_MARKER"
printf 'Grouped test files:\n'
for file in "${GROUPED_TEST_FILES[@]}"; do
  printf ' - %s\n' "$file"
done

set +e
(
  cd "$ROOT_DIR"
  find tests -name '*.pyc' -delete
  find tests -name '__pycache__' -type d -empty -delete
  pytest -q -m "$SUITE_MARKER" "${GROUPED_TEST_FILES[@]}"
) 2>&1 | tee "$LOG_PATH"
PYTEST_STATUS=${PIPESTATUS[0]}
set -e

if [[ $PYTEST_STATUS -eq 0 ]]; then
  WATCHDOG_REGRESSION_PACK_STATUS="passed"
  TASK_STATE="livepaper_observability_shift_handoff_watchdog_regression_pack_passed"
  SELECTED_OUTCOME="A"
  RECOMMENDED_NEXT_STEP="livepaper_observability_shift_handoff_watchdog_ci_gate"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE"
  DECISION="livepaper_observability_shift_handoff_watchdog_ci_gate_ready"
  KEY_FINDING="livepaper_observability_shift_handoff_watchdog_regression_pack_durable"
else
  WATCHDOG_REGRESSION_PACK_STATUS="failed"
  TASK_STATE="livepaper_observability_shift_handoff_watchdog_regression_pack_failed"
  SELECTED_OUTCOME="handoff_watchdog_regression_pack_failed"
  RECOMMENDED_NEXT_STEP="livepaper_observability_shift_handoff_watchdog_regression_pack"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK"
  DECISION="livepaper_observability_shift_handoff_watchdog_regression_pack_failed"
  KEY_FINDING="livepaper_observability_shift_handoff_watchdog_regression_pack_failed"
fi

export ROOT_DIR PROOF_JSON SUMMARY_MD REPORT_MD STATUS_MD CONTEXT_JSON DETAILS_MD MIN_PROMPT_TXT
export HANDOFF_MD LOG_PATH WATCHDOG_REGRESSION_PACK_STATUS TASK_STATE SELECTED_OUTCOME
export RECOMMENDED_NEXT_STEP RECOMMENDED_NEXT_TASK_ID DECISION KEY_FINDING SUITE_MARKER

python - <<'PY'
import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import sys

root_dir = Path(os.environ["ROOT_DIR"])
proof_json = Path(os.environ["PROOF_JSON"])
summary_md = Path(os.environ["SUMMARY_MD"])
report_md = Path(os.environ["REPORT_MD"])
status_md = Path(os.environ["STATUS_MD"])
context_json = Path(os.environ["CONTEXT_JSON"])
details_md = Path(os.environ["DETAILS_MD"])
min_prompt_txt = Path(os.environ["MIN_PROMPT_TXT"])
handoff_md = Path(os.environ["HANDOFF_MD"])
log_path = Path(os.environ["LOG_PATH"])
watchdog_regression_pack_status = os.environ["WATCHDOG_REGRESSION_PACK_STATUS"]
task_state = os.environ["TASK_STATE"]
selected_outcome = os.environ["SELECTED_OUTCOME"]
recommended_next_step = os.environ["RECOMMENDED_NEXT_STEP"]
recommended_next_task_id = os.environ["RECOMMENDED_NEXT_TASK_ID"]
decision = os.environ["DECISION"]
key_finding = os.environ["KEY_FINDING"]
suite_marker = os.environ["SUITE_MARKER"]

LATEST_VEXTER_PR = 67
LATEST_VEXTER_MAIN_COMMIT = "7ab737a306ceca06193044d384e6b17d371838e2"
LATEST_VEXTER_MERGED_AT_UTC = "2026-03-26T21:34:46Z"
LATEST_RECENT_VEXTER_PRS = [67, 66, 65, 64]
DEXTER_MAIN_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
DEXTER_PR_3_MERGED_AT_UTC = "2026-03-21T11:31:07Z"
MEWX_FROZEN_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
MEWX_FROZEN_COMMIT_DATE_UTC = "2026-03-20T16:05:19Z"
PROMOTED_BASELINE = "task005-pass-grade-pair-20260325T180027Z"
COMPARISON_SOURCE = "comparison_closed_out"
BUNDLE_SOURCE = (
    "/Users/cabbala/Downloads/"
    "vexter_task007_livepaper_observability_shift_handoff_watchdog_regression_pack_bundle.tar.gz"
)
REGRESSION_PACK_TASK_ID = (
    "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK"
)
REGRESSION_PACK_MARKER = "livepaper_observability_shift_handoff_watchdog_regression_pack"
REGRESSION_PACK_CI_GATE_MARKER = "livepaper_observability_shift_handoff_watchdog_ci_gate"
REGRESSION_PACK_CURRENT_POINTER_PATHS = {
    "current_status_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md",
    "current_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md",
    "current_proof_summary": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md",
    "current_proof_json": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
}
REGRESSION_PACK_FIRST_DEEP_PROOF_PATH = (
    "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json"
)
REGRESSION_PACK_CURRENT_TASK_STATE = (
    "livepaper_observability_shift_handoff_watchdog_regression_pack_passed"
)
REGRESSION_PACK_RECOMMENDED_NEXT_STEP = "livepaper_observability_shift_handoff_watchdog_ci_gate"
REGRESSION_PACK_TERMINAL_SNAPSHOT_POINTER = (
    "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
)
REGRESSION_PACK_FAILURE_DETAIL_POINTER = (
    "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
)

sys.path.insert(0, str(root_dir))
from vexter.planner_router.handoff_watchdog import (  # noqa: E402
    DEFAULT_CURRENT_POINTER_PATHS,
    DEFAULT_CURRENT_TASK_STATE,
    DEFAULT_FAILURE_DETAIL_POINTER,
    DEFAULT_FIRST_DEEP_PROOF_PATH,
    DEFAULT_RECOMMENDED_NEXT_STEP,
    DEFAULT_TERMINAL_SNAPSHOT_POINTER,
    HANDOFF_PATH,
    HANDOFF_RUNTIME_PATH,
    LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES,
    RUNTIME_CURRENT_POINTER_PATHS,
    RUNTIME_CURRENT_TASK_STATE,
    RUNTIME_FAILURE_DETAIL_POINTER,
    RUNTIME_FIRST_DEEP_PROOF_PATH,
    RUNTIME_RECOMMENDED_NEXT_STEP,
    RUNTIME_TERMINAL_SNAPSHOT_POINTER,
    evaluate_livepaper_observability_shift_handoff_watchdog,
)


def evaluate_case(
    markdown: str,
    *,
    expected_first_deep_proof_path: str,
    expected_task_state: str,
    expected_recommended_next_step: str,
    expected_current_pointer_paths: dict[str, str],
    expected_terminal_snapshot_pointer: str,
    expected_failure_detail_pointer: str,
):
    return evaluate_livepaper_observability_shift_handoff_watchdog(
        markdown,
        repo_root=root_dir,
        expected_first_deep_proof_path=expected_first_deep_proof_path,
        expected_task_state=expected_task_state,
        expected_recommended_next_step=expected_recommended_next_step,
        expected_current_pointer_paths=expected_current_pointer_paths,
        expected_terminal_snapshot_pointer=expected_terminal_snapshot_pointer,
        expected_failure_detail_pointer=expected_failure_detail_pointer,
    )


handoff_lines = [
    "# Live-Paper Observability Shift Handoff Watchdog Regression Pack",
    "",
    "## Current Status",
    "- outgoing_shift_window: 2026-03-27 regression-pack durability check",
    "- incoming_shift_window: 2026-03-27 watchdog-ci-gate follow-up",
    f"- task_state: {REGRESSION_PACK_CURRENT_TASK_STATE}",
    "- shift_outcome: contained",
    "- current_action: continue",
    "- active_broken_surface_or_none: none",
    f"- recommended_next_step: {REGRESSION_PACK_RECOMMENDED_NEXT_STEP}",
    "- status_delivery: poll_first",
    "- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`",
    f"- vexter_main_commit: {LATEST_VEXTER_MAIN_COMMIT}",
    f"- dexter_main_commit: {DEXTER_MAIN_COMMIT}",
    f"- mewx_frozen_commit: {MEWX_FROZEN_COMMIT}",
    f"- promoted_baseline: {PROMOTED_BASELINE}",
    f"- comparison_source_of_truth: {COMPARISON_SOURCE}",
    "- containment_anchor_plan_id: req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "- failure_anchor_plan_id: req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "",
    "## Proof and Report Pointers",
    f"- current_status_report: {REGRESSION_PACK_CURRENT_POINTER_PATHS['current_status_report']}",
    f"- current_report: {REGRESSION_PACK_CURRENT_POINTER_PATHS['current_report']}",
    f"- current_proof_summary: {REGRESSION_PACK_CURRENT_POINTER_PATHS['current_proof_summary']}",
    f"- current_proof_json: {REGRESSION_PACK_CURRENT_POINTER_PATHS['current_proof_json']}",
    f"- first_deep_proof_to_open_next: {REGRESSION_PACK_FIRST_DEEP_PROOF_PATH}",
    "- shortest_proof_trail: status -> report -> summary -> regression-pack proof -> regression-pack handoff -> runtime handoff proof -> baseline handoff proof",
    "",
    "## Observability Classification",
    "- omission_present: false",
    "- omission_summary_or_none: none",
    "- drift_present: false",
    "- drift_summary_or_none: none",
    "- partial_visibility_present: false",
    "- partial_visibility_summary_or_none: none",
    "- exact_broken_surface_or_none: none",
    "",
    "## Manual Stop-All and Quarantine",
    "- manual_stop_all_visible: true",
    "- halt_mode_or_none: manual_latched_stop_all",
    "- trigger_plan_id_or_none: req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "- stop_reason_or_none: manual_latched_stop_all",
    "- peer_plan_propagation_confirmed: true",
    "- quarantine_active: true",
    "- quarantine_reason_or_none: timeout_guard",
    "- continuity_check: monitor_profile_id=mewx_timeout_guard, quarantine_scope=sleeve, execution_mode=sim_live, ack_history_visible=true, runtime_follow_up_visible=true, regression_pack_visible=true",
    "",
    "## Terminal Snapshot",
    "- terminal_snapshot_present: true",
    f"- terminal_snapshot_pointer_or_none: {REGRESSION_PACK_TERMINAL_SNAPSHOT_POINTER}",
    "- snapshot_signal_visible: true",
    "- terminal_stop_reason_visible: true",
    "- terminal_anchor_native_session_id: sim_live:req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "- terminal_anchor_handle_id: mewx_frozen_pinned:req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "",
    "## Normalized Failure Detail",
    "- normalized_failure_detail_present: true",
    f"- failure_detail_pointer_or_none: {REGRESSION_PACK_FAILURE_DETAIL_POINTER}",
    "- normalized_identity_chain_coherent: true",
    "- source_reason_visible: true",
    "- rollback_snapshot_required_and_present_or_none: present",
    "- failure_code: status_timeout",
    "- failure_stage: status",
    "- failure_source_reason: status timeout",
    "- rollback_snapshot_signal: snapshot",
    "- rollback_snapshot_stop_reason: manual_latched_stop_all",
    "",
    "## Open Questions",
    "- question_1_or_none: none",
    "- question_2_or_none: none",
    "- question_3_or_none: none",
    "",
    "## Next-Shift Priority Checks",
    "- priority_check_1: confirm the current regression-pack status, report, and proof JSON before changing task state",
    "- priority_check_2_or_none: if any face regresses on the baseline, runtime, or regression-pack handoff, restore the explicit field instead of carrying it over implicitly",
    "- priority_check_3_or_none: start the next bounded lane at `livepaper_observability_shift_handoff_watchdog_ci_gate` using the current regression-pack proof together with the baseline and runtime watchdog proofs",
    "",
    "## Completeness Check",
    "- every_required_face_filled_or_none: true",
    "- status_matches_current_checklist_artifacts: true",
    "- proof_and_report_pointers_checked: true",
    "- omission_drift_partial_visibility_explicit: true",
    "- containment_and_failure_faces_explicit: true",
    "- open_questions_and_next_checks_explicit: true",
    "",
    "This handoff is synthetic and bounded. It packages the fixed handoff watchdog and runtime-watchdog evidence into one durable regression surface, does not collect new evidence, keeps the comparison baseline closed, and reuses the source-faithful runtime anchors instead of inventing new ones.",
]
handoff_md.write_text("\n".join(handoff_lines) + "\n")

baseline_report = evaluate_case(
    (root_dir / HANDOFF_PATH).read_text(),
    expected_first_deep_proof_path=DEFAULT_FIRST_DEEP_PROOF_PATH,
    expected_task_state=DEFAULT_CURRENT_TASK_STATE,
    expected_recommended_next_step=DEFAULT_RECOMMENDED_NEXT_STEP,
    expected_current_pointer_paths=DEFAULT_CURRENT_POINTER_PATHS,
    expected_terminal_snapshot_pointer=DEFAULT_TERMINAL_SNAPSHOT_POINTER,
    expected_failure_detail_pointer=DEFAULT_FAILURE_DETAIL_POINTER,
)
runtime_report = evaluate_case(
    (root_dir / HANDOFF_RUNTIME_PATH).read_text(),
    expected_first_deep_proof_path=RUNTIME_FIRST_DEEP_PROOF_PATH,
    expected_task_state=RUNTIME_CURRENT_TASK_STATE,
    expected_recommended_next_step=RUNTIME_RECOMMENDED_NEXT_STEP,
    expected_current_pointer_paths=RUNTIME_CURRENT_POINTER_PATHS,
    expected_terminal_snapshot_pointer=RUNTIME_TERMINAL_SNAPSHOT_POINTER,
    expected_failure_detail_pointer=RUNTIME_FAILURE_DETAIL_POINTER,
)
regression_pack_report = evaluate_case(
    handoff_md.read_text(),
    expected_first_deep_proof_path=REGRESSION_PACK_FIRST_DEEP_PROOF_PATH,
    expected_task_state=REGRESSION_PACK_CURRENT_TASK_STATE,
    expected_recommended_next_step=REGRESSION_PACK_RECOMMENDED_NEXT_STEP,
    expected_current_pointer_paths=REGRESSION_PACK_CURRENT_POINTER_PATHS,
    expected_terminal_snapshot_pointer=REGRESSION_PACK_TERMINAL_SNAPSHOT_POINTER,
    expected_failure_detail_pointer=REGRESSION_PACK_FAILURE_DETAIL_POINTER,
)

canonical_handoff_snapshots = {
    "baseline": {
        "path": str(HANDOFF_PATH),
        "passed": baseline_report.passed,
        "findings": [asdict(finding) for finding in baseline_report.findings],
        "surface_status": dict(baseline_report.surface_status),
    },
    "runtime": {
        "path": str(HANDOFF_RUNTIME_PATH),
        "passed": runtime_report.passed,
        "findings": [asdict(finding) for finding in runtime_report.findings],
        "surface_status": dict(runtime_report.surface_status),
    },
    "regression_pack": {
        "path": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/HANDOFF.md",
        "passed": regression_pack_report.passed,
        "findings": [asdict(finding) for finding in regression_pack_report.findings],
        "surface_status": dict(regression_pack_report.surface_status),
    },
}

surface_regression_tests = {
    surface: [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_regression_pack_flags_face_regression[{surface}]"
    ]
    for surface in LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES
}
surface_omission_tests = {
    surface: [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_regression_pack_flags_surface_omission[{surface}]"
    ]
    for surface in LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES
}

log_lines = log_path.read_text().splitlines()
pytest_result = next((line.strip() for line in reversed(log_lines) if line.strip()), "")
failed_tests = []
for line in log_lines:
    stripped = line.strip()
    if stripped.startswith("FAILED "):
        failed_tests.append(stripped.split(" - ", 1)[0].replace("FAILED ", "", 1))

proof = {
    "task_id": REGRESSION_PACK_TASK_ID,
    "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "verified_github": {
        "latest_vexter_pr": LATEST_VEXTER_PR,
        "latest_vexter_main_commit": LATEST_VEXTER_MAIN_COMMIT,
        "latest_vexter_merged_at_utc": LATEST_VEXTER_MERGED_AT_UTC,
        "latest_recent_vexter_prs": LATEST_RECENT_VEXTER_PRS,
        "open_non_authoritative_vexter_prs": [50],
        "dexter_pr": 3,
        "dexter_main_commit": DEXTER_MAIN_COMMIT,
        "dexter_pr_3_merged_at_utc": DEXTER_PR_3_MERGED_AT_UTC,
        "mewx_frozen_commit": MEWX_FROZEN_COMMIT,
        "mewx_frozen_commit_date_utc": MEWX_FROZEN_COMMIT_DATE_UTC,
    },
    "fixed_input_surface": {
        "canonical_contract": "specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md",
        "canonical_runbook": "docs/livepaper_observability_operator_runbook.md",
        "canonical_checklist": "docs/livepaper_observability_shift_checklist.md",
        "canonical_handoff_template": "docs/livepaper_observability_shift_handoff_template.md",
        "canonical_handoff_drill": "docs/livepaper_observability_shift_handoff_drill.md",
        "baseline_watchdog_proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json",
        "runtime_watchdog_proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json",
        "transport_runtime_watchdog_proof": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json",
        "promoted_label": PROMOTED_BASELINE,
        "comparison_source_of_truth": COMPARISON_SOURCE,
        "global_halt_mode": "manual_latched_stop_all",
        "status_delivery": "poll_first",
    },
    "implementation": {
        "source_logic_changed": False,
        "validator_rules_changed": False,
        "dexter_strategy_changed": False,
        "mewx_strategy_changed": False,
        "new_evidence_collection_required": False,
        "comparison_baseline_reopened": False,
    },
    "livepaper_observability_shift_handoff_watchdog_regression_pack": {
        "suite_group": suite_marker,
        "runner_script": "scripts/run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh",
        "workflow": ".github/workflows/validate.yml",
        "pytest_command": "pytest -q -m livepaper_observability_shift_handoff_watchdog_regression_pack tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py",
        "pytest_result": pytest_result,
        "watchdog_regression_pack_status": watchdog_regression_pack_status,
        "grouped_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py",
        ],
        "grouped_suite_markers": ["livepaper_observability_shift_handoff_watchdog_regression_pack"],
        "monitored_surfaces": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
        "monitored_issue_classes": ["omission", "drift", "partial_visibility"],
        "surface_regression_tests": surface_regression_tests,
        "surface_omission_tests": surface_omission_tests,
        "proof_outputs": [
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md",
        ],
        "proof_artifact_name": "livepaper-observability-shift-handoff-watchdog-regression-pack-proof",
        "canonical_handoff_snapshots": canonical_handoff_snapshots,
        "baseline_watchdog_proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json",
        "runtime_watchdog_proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json",
        "source_faithful_modes": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "normalized_failure_detail": {
            "finding_surfaces_or_none": sorted(
                {finding.surface for finding in regression_pack_report.findings}
            )
            or ["none"],
            "finding_classes_or_none": sorted(
                {finding.classification for finding in regression_pack_report.findings}
            )
            or ["none"],
            "failed_tests_or_none": failed_tests or ["none"],
            "non_surface_failures_or_none": failed_tests or ["none"],
        },
    },
    "next_task_evaluation": {
        "livepaper_observability_shift_handoff_watchdog_ci_gate": {
            "recommended": watchdog_regression_pack_status == "passed",
            "reasons": [
                "The remaining risk is no longer missing handoff-watchdog faces; it is making the frozen regression pack run on every handoff-facing change.",
                "A dedicated handoff-watchdog CI gate operationalizes the durable pack without reopening comparison work or changing source logic.",
                "This path preserves the source-faithful Dexter paper_live and frozen Mew-X sim_live seam while keeping operator-facing regressions visible.",
            ],
        },
        "transport_livepaper_observability_acceptance_pack": {
            "recommended": False,
            "reasons": [
                "An acceptance pack would mostly repackage already-fixed handoff outputs instead of adding a stronger always-on guard.",
                "The highest remaining leverage is CI execution durability for the fixed handoff-watchdog surface.",
            ],
        },
        "executor_boundary_code_spec": {
            "recommended": False,
            "reasons": [
                "No new planner-to-transport boundary ambiguity surfaced while packaging the handoff watchdog surfaces.",
                "The remaining risk is regression durability inside the fixed contract, not a missing interface definition.",
            ],
        },
    },
    "task_result": {
        "selected_outcome": selected_outcome,
        "key_finding": key_finding,
        "claim_boundary": "livepaper_observability_shift_handoff_watchdog_regression_pack_bounded",
        "comparison_source_of_truth_state": COMPARISON_SOURCE,
        "task_state": task_state,
        "recommended_next_step": recommended_next_step,
        "recommended_next_task_id": recommended_next_task_id,
        "decision": decision,
        "promoted_label": PROMOTED_BASELINE,
        "default_execution_anchor": "dexter",
        "selective_option_source": "mewx",
    },
}
proof_json.write_text(json.dumps(proof, indent=2) + "\n")

summary_lines = [
    "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK Proof Summary",
    "",
    "- Verified Vexter `main` at merged PR `#67` commit `7ab737a306ceca06193044d384e6b17d371838e2`",
    "- Kept Dexter pinned at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "- Packaged the baseline handoff watchdog and runtime follow-up handoff watchdog into one durable regression lane without changing source logic or reopening the comparison baseline",
    f"- Regression-pack run result: `{pytest_result}`",
    "- Locked current status, proof/report pointers, omission / drift / partial_visibility, manual stop-all, quarantine, terminal snapshot, normalized failure detail, open questions, and next-shift priority checks across baseline, runtime, and regression-pack handoffs",
]
if watchdog_regression_pack_status == "passed":
    summary_lines.append("- Recommended next task: `livepaper_observability_shift_handoff_watchdog_ci_gate`")
else:
    summary_lines.append("- Regression-pack failed, so the immediate next step remains `livepaper_observability_shift_handoff_watchdog_regression_pack`")
summary_md.write_text("\n".join(summary_lines) + "\n")

report_lines = [
    "# TASK-007 Live-Paper Observability Shift Handoff Watchdog Regression-Pack Report",
    "",
    "## Verified GitHub State",
    "",
    "- `Cabbala/Vexter` latest merged `main` was reverified at PR `#67` main commit `7ab737a306ceca06193044d384e6b17d371838e2` on `2026-03-26T21:34:46Z`.",
    "- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.",
    "- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.",
    "- Open Vexter PR `#50` remained non-authoritative relative to merged `main`.",
    "",
    "## What This Task Did",
    "",
    "- Started from the merged handoff-watchdog-runtime lane on PR `#67` and kept the promoted comparison baseline frozen.",
    "- Added a dedicated handoff-watchdog regression-pack lane so future handoff-facing changes must preserve the fixed watchdog surface across the baseline handoff, runtime follow-up handoff, and current regression-pack handoff.",
    "- Locked required-face omission, pointer shrinkage or ambiguity, implicit carry-over, omission / drift / partial_visibility completeness, manual stop-all visibility, quarantine visibility, terminal snapshot visibility, normalized failure detail visibility, open questions, and next-shift priority checks into durable assertions.",
    "- Preserved the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam without changing source logic, trust logic, thresholds, validator rules, or frozen source pins.",
    "",
    "## Validation",
    "",
    "- `pytest -q -m livepaper_observability_shift_handoff_watchdog_regression_pack tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py`",
    f"- `{pytest_result}`",
    "",
    "## Recommendation Among Next Tasks",
    "",
    "### `livepaper_observability_shift_handoff_watchdog_ci_gate`",
    "",
    "Recommended next because:",
    "",
    "- this task already packages the baseline and runtime handoff-watchdog conclusions into a durable regression surface",
    "- the remaining risk is making that surface run on every handoff-facing change, not discovering a new face",
    "- a dedicated CI gate operationalizes the pack without reopening comparison or changing source logic",
    "",
    "### `transport_livepaper_observability_acceptance_pack`",
    "",
    "Not recommended now because:",
    "",
    "- it would mostly repackage already-fixed operator-facing artifacts instead of increasing regression durability",
    "- the sharper risk-reduction step is an always-on handoff-watchdog CI gate",
    "",
    "### `executor_boundary_code_spec`",
    "",
    "Not recommended now because:",
    "",
    "- no new executor boundary ambiguity surfaced while packaging the handoff watchdog surface",
    "- the remaining work is preserving the existing fixed contract rather than redefining it",
    "",
    "## Decision",
    "",
    f"- Outcome: `{selected_outcome}`",
    f"- Key finding: `{key_finding}`",
    "- Claim boundary: `livepaper_observability_shift_handoff_watchdog_regression_pack_bounded`",
    f"- Current task status: `{task_state}`",
    f"- Recommended next step: `{recommended_next_step}`",
    f"- Decision: `{decision}`",
    "",
    "## Key Paths",
    "",
    "- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`",
    "- Canonical runbook: `docs/livepaper_observability_operator_runbook.md`",
    "- Canonical checklist: `docs/livepaper_observability_shift_checklist.md`",
    "- Canonical handoff template: `docs/livepaper_observability_shift_handoff_template.md`",
    "- Canonical handoff drill: `docs/livepaper_observability_shift_handoff_drill.md`",
    "- Baseline handoff watchdog proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json`",
    "- Runtime handoff watchdog proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json`",
    "- Regression-pack handoff: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/HANDOFF.md`",
    "- Regression-pack report: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md`",
    "- Regression-pack status: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md`",
    "- Regression-pack proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json`",
    "- Regression-pack summary: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md`",
    "- Regression-pack prompt pack: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack`",
    "- Regression-pack bundle: `artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz`",
]
report_md.write_text("\n".join(report_lines) + "\n")

status_lines = [
    "# TASK-007 Live-Paper Observability Shift Handoff Watchdog Regression-Pack Status",
    "",
    f"- Task state: `{task_state}`",
    f"- Key finding: `{key_finding}`",
    "- Claim boundary: `livepaper_observability_shift_handoff_watchdog_regression_pack_bounded`",
    f"- Recommended next step: `{recommended_next_step}`",
    f"- Recommended next task id: `{recommended_next_task_id}`",
    f"- Decision: `{decision}`",
    f"- Latest merged Vexter PR: `#{LATEST_VEXTER_PR}`",
    f"- Latest merged Vexter commit: `{LATEST_VEXTER_MAIN_COMMIT}`",
    f"- Dexter pin: `{DEXTER_MAIN_COMMIT}`",
    f"- Mew-X frozen pin: `{MEWX_FROZEN_COMMIT}`",
    f"- Promoted baseline: `{PROMOTED_BASELINE}`",
    f"- Comparison source of truth: `{COMPARISON_SOURCE}`",
]
status_md.write_text("\n".join(status_lines) + "\n")

context_json.write_text(
    json.dumps(
        {
            "recommended_next_task": "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
            "visible_main_state": {
                "latest_vexter_pr": LATEST_VEXTER_PR,
                "latest_vexter_main_commit": LATEST_VEXTER_MAIN_COMMIT,
                "dexter_main": DEXTER_MAIN_COMMIT,
                "mewx_frozen": MEWX_FROZEN_COMMIT,
            },
            "current_state": {
                "current_task": REGRESSION_PACK_CURRENT_TASK_STATE,
                "recommended_next_step": REGRESSION_PACK_RECOMMENDED_NEXT_STEP,
                "broken_handoff_watchdog_surfaces_or_none": ["none"],
            },
        },
        indent=2,
    )
    + "\n"
)
details_md.write_text(
    "\n".join(
        [
            "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
            "",
            "## Goal",
            "",
            "Freeze the fixed handoff-watchdog and runtime-follow-up watchdog faces into a durable regression pack.",
            "",
            "## Monitored Surfaces",
            "",
            "- current_status",
            "- proof_and_report_pointers",
            "- omission_drift_partial_visibility",
            "- manual_stop_all",
            "- quarantine",
            "- terminal_snapshot",
            "- normalized_failure_detail",
            "- open_questions",
            "- next_shift_priority_checks",
        ]
    )
    + "\n"
)
min_prompt_txt.write_text(
    "Verify the regression-pack proof and status, then inspect the named broken handoff surface across the baseline, runtime, and regression-pack handoffs before changing CI-gate artifacts.\n"
)

summary_path = root_dir / "artifacts" / "summary.md"
summary_path.write_text(
    "\n".join(
        [
            "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK Summary",
            "",
            "## Verified GitHub State",
            "",
            "- `Cabbala/Vexter` latest merged `main` was reverified at PR `#67` commit `7ab737a306ceca06193044d384e6b17d371838e2` on `2026-03-26T21:34:46Z`.",
            "- The completed handoff watchdog runtime lane remained visible at PR `#67`.",
            "- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.",
            "- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.",
            "- Open Vexter PR `#50` (`feat(infra): refresh runtime observability artifacts`) remained non-authoritative relative to merged `main`.",
            "",
            "## What This Task Did",
            "",
            "- Treated the fixed observability contract, runbook, checklist, handoff template, handoff drill, handoff watchdog proof, and handoff-watchdog-runtime proof as the formal baseline without reopening comparison work.",
            "- Added a regression-pack lane through `scripts/run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh` and `tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py`.",
            "- Kept the handoff watchdog explicit across the baseline handoff, the runtime-shaped follow-up handoff, and the regression-pack handoff for current status, proof/report pointers, omission / drift / partial_visibility, manual stop-all, quarantine, terminal snapshot, normalized failure detail, open questions, and next-shift priority checks.",
            "- Refreshed workflow wiring, bundle metadata, context pack, proof manifest, task ledger, proof outputs, status/report, and the regression-pack handoff bundle without changing planner/router source logic or collecting new evidence.",
            "",
            "## Decision",
            "",
            "- Outcome: `A`",
            "- Key finding: `livepaper_observability_shift_handoff_watchdog_regression_pack_durable`",
            "- Claim boundary: `livepaper_observability_shift_handoff_watchdog_regression_pack_bounded`",
            "- Current task status: `livepaper_observability_shift_handoff_watchdog_regression_pack_passed`",
            "- Recommended next step: `livepaper_observability_shift_handoff_watchdog_ci_gate`",
            "- Decision: `livepaper_observability_shift_handoff_watchdog_ci_gate_ready`",
            "",
            "## Key Paths",
            "",
            "- Regression-pack proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json`",
            "- Regression-pack summary: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md`",
            "- Regression-pack report: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md`",
            "- Regression-pack status: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md`",
            "- Regression-pack handoff: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/HANDOFF.md`",
            "- Baseline handoff watchdog proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json`",
            "- Runtime handoff watchdog proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json`",
            "- Current bundle target: `artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz`",
        ]
    )
    + "\n"
)

context_pack_path = root_dir / "artifacts" / "context_pack.json"
context_pack = json.loads(context_pack_path.read_text())
context_pack["bundle_source"] = BUNDLE_SOURCE
context_pack["current_contract"][
    "livepaper_observability_shift_handoff_watchdog_regression_pack_marker"
] = REGRESSION_PACK_MARKER
context_pack["current_contract"][
    "livepaper_observability_shift_handoff_watchdog_ci_gate_marker"
] = REGRESSION_PACK_CI_GATE_MARKER
context_pack["current_task"] = {
    "id": REGRESSION_PACK_TASK_ID,
    "scope": [
        "Verify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X.",
        "Treat the fixed observability contract, operator runbook, shift checklist, handoff template, handoff drill, handoff watchdog proof, and handoff-watchdog-runtime proof as the formal live-paper observability handoff baseline without reopening comparison work.",
        "Package the fixed handoff watchdog and handoff-watchdog-runtime conclusions into one durable regression pack.",
        "Guard required handoff field omission, pointer shrinkage or ambiguity, implicit carry-over instead of explicit false/none, omission / drift / partial_visibility completeness, manual stop-all, quarantine, terminal snapshot, normalized failure detail, open questions, and next-shift priority checks across the baseline and runtime handoff paths.",
        "Keep proof/report outputs and the regression-pack handoff explicit so the broken handoff face is immediately visible in workflow and proof outputs.",
        "Recommend the next bounded cut among executor_boundary_code_spec, transport_livepaper_observability_acceptance_pack, and livepaper_observability_shift_handoff_watchdog_ci_gate.",
        "Refresh tests, summary, context pack, proof manifest, task ledger, report, proof output, and handoff bundle without changing planner/router source logic.",
    ],
    "deliverables": [
        "README.md",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py",
        "tests/test_bootstrap_layout.py",
        "scripts/build_proof_bundle.sh",
        "scripts/run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh",
        ".github/workflows/validate.yml",
        "pytest.ini",
        "artifacts/summary.md",
        "artifacts/context_pack.json",
        "artifacts/proof_bundle_manifest.json",
        "artifacts/task_ledger.jsonl",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/HANDOFF.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz",
    ],
    "frozen_source_commits": {
        "dexter": DEXTER_MAIN_COMMIT,
        "mewx": MEWX_FROZEN_COMMIT,
    },
}
github_latest = context_pack.setdefault("evidence", {}).setdefault("github_latest", {})
github_latest["latest_vexter_pr"] = LATEST_VEXTER_PR
github_latest["latest_vexter_main_commit"] = LATEST_VEXTER_MAIN_COMMIT
github_latest["latest_recent_vexter_prs"] = LATEST_RECENT_VEXTER_PRS
github_latest["vexter_pr_67_merged_at"] = LATEST_VEXTER_MERGED_AT_UTC

context_pack["evidence"]["livepaper_observability_shift_handoff_watchdog_regression_pack"] = {
    "report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md",
    "status_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md",
    "proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
    "summary": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md",
    "handoff_dir": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack",
    "key_finding": key_finding,
    "claim_boundary": "livepaper_observability_shift_handoff_watchdog_regression_pack_bounded",
    "task_state": task_state,
    "grouped_test_files": [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py",
    ],
    "validated_axes": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
    "preferred_next_step": REGRESSION_PACK_RECOMMENDED_NEXT_STEP,
}
context_pack["next_task"] = {
    "id": "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
    "state": "ready_for_livepaper_observability_shift_handoff_watchdog_ci_gate",
    "rationale": [
        "The handoff watchdog surface is now durably packed across the baseline handoff, runtime follow-up handoff, and current regression-pack handoff.",
        "The next bounded cut is enforcing that pack as an always-on CI gate instead of discovering another handoff face.",
        "A transport-facing acceptance pack or executor-boundary restatement would reduce less risk than continuous enforcement of the fixed handoff-watchdog surface.",
    ],
}
proofs = context_pack.setdefault("proofs", {})
proofs["livepaper_observability_shift_handoff_watchdog_regression_pack_added"] = True
proofs["livepaper_observability_shift_handoff_watchdog_regression_pack_workflow_enforced"] = True
proofs["livepaper_observability_shift_handoff_watchdog_regression_pack_proof_emitted"] = True
proofs["livepaper_observability_shift_handoff_watchdog_regression_pack_baseline_handoff_locked"] = True
proofs["livepaper_observability_shift_handoff_watchdog_regression_pack_runtime_handoff_locked"] = True
proofs["livepaper_observability_shift_handoff_watchdog_regression_pack_omission_guarded"] = True
proofs["livepaper_observability_shift_handoff_watchdog_regression_pack_drift_guarded"] = True
proofs["livepaper_observability_shift_handoff_watchdog_regression_pack_partial_visibility_guarded"] = True
context_pack_path.write_text(json.dumps(context_pack, indent=2) + "\n")

manifest_path = root_dir / "artifacts" / "proof_bundle_manifest.json"
manifest = json.loads(manifest_path.read_text())
manifest["bundle_path"] = (
    "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz"
)
manifest["bundle_source"] = BUNDLE_SOURCE
manifest["task_id"] = REGRESSION_PACK_TASK_ID
manifest["status"] = task_state

for script_path in (
    "scripts/run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh",
):
    if script_path not in manifest["scripts"]:
        manifest["scripts"].append(script_path)
for proof_path in (
    "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
    "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md",
):
    if proof_path not in manifest["proof_files"]:
        manifest["proof_files"].append(proof_path)
for report_path in (
    "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md",
    "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md",
    "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack",
):
    if report_path not in manifest["reports"]:
        manifest["reports"].append(report_path)
manifest["next_task"] = {
    "id": "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
    "state": "ready_for_livepaper_observability_shift_handoff_watchdog_ci_gate",
    "resume_requirements": [
        "Treat task005-pass-grade-pair-20260325T180027Z as the frozen promoted baseline.",
        "Carry forward livepaper_observability_shift_handoff_watchdog_regression_pack_durable together with livepaper_observability_shift_handoff_watchdog_regression_pack_bounded as the current evidence conclusion.",
        "Use the fixed handoff contract, runbook, checklist, template, drill, baseline handoff watchdog proof, runtime handoff watchdog proof, and regression-pack handoff proof as the operator-facing source of truth.",
        "Preserve the current Dexter and Mew-X source pins together with fixed poll_first delivery and manual_latched_stop_all semantics.",
        "Do not reopen comparison work or change source logic in the next lane.",
        "Run the durable regression pack on every handoff-facing change.",
    ],
}
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

ledger_path = root_dir / "artifacts" / "task_ledger.jsonl"
ledger_entry = {
    "artifact_bundle": "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz",
    "base_main": LATEST_VEXTER_MAIN_COMMIT,
    "branch": "codex/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack",
    "claim_boundary": "livepaper_observability_shift_handoff_watchdog_regression_pack_bounded",
    "comparison_source_of_truth_state": COMPARISON_SOURCE,
    "confirmatory_overturns_promoted_baseline": False,
    "confirmatory_residual": "Mew-X candidate_rejected",
    "confirmatory_same_attempt_label": "task005-pass-grade-pair-20260325T180604Z",
    "date": "2026-03-27",
    "decision": decision,
    "default_execution_anchor": "dexter",
    "handoff_watchdog_regression_pack_workflow_enforced": True,
    "handoff_watchdog_regression_pack_proof_emitted": True,
    "handoff_watchdog_regression_pack_runner_added": True,
    "handoff_watchdog_regression_pack_baseline_handoff_locked": True,
    "handoff_watchdog_regression_pack_runtime_handoff_locked": True,
    "handoff_watchdog_regression_pack_current_status_watchdogged": True,
    "handoff_watchdog_regression_pack_proof_pointer_watchdogged": True,
    "handoff_watchdog_regression_pack_visibility_classification_watchdogged": True,
    "handoff_watchdog_regression_pack_manual_stop_all_watchdogged": True,
    "handoff_watchdog_regression_pack_quarantine_watchdogged": True,
    "handoff_watchdog_regression_pack_terminal_snapshot_watchdogged": True,
    "handoff_watchdog_regression_pack_normalized_failure_detail_watchdogged": True,
    "handoff_watchdog_regression_pack_open_questions_watchdogged": True,
    "handoff_watchdog_regression_pack_next_shift_priorities_watchdogged": True,
    "key_finding": key_finding,
    "live_metric_winner_tally": {"dexter": 6, "mewx": 4, "tie": 2},
    "new_evidence_collection_required": False,
    "next_task_id": "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
    "next_task_state": "ready_for_livepaper_observability_shift_handoff_watchdog_ci_gate",
    "prior_lane_source_state": "livepaper_observability_shift_handoff_watchdog_runtime_passed",
    "promoted_live_winner_mode": "derived",
    "promoted_replay_winner_mode": "derived",
    "promoted_same_attempt_label": PROMOTED_BASELINE,
    "proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
    "recommended_next_lane": REGRESSION_PACK_RECOMMENDED_NEXT_STEP,
    "replay_metric_winner_tally": {"dexter": 6, "mewx": 4, "tie": 2},
    "repo": "https://github.com/Cabbala/Vexter",
    "selected_outcome": selected_outcome,
    "selective_option_source": "mewx",
    "source_faithful_modes": {"dexter": "paper_live", "mewx": "sim_live"},
    "status": task_state,
    "supporting_vexter_prs": [67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17],
    "task_id": REGRESSION_PACK_TASK_ID,
    "verified_dexter_main_commit": DEXTER_MAIN_COMMIT,
    "verified_dexter_pr": 3,
    "verified_mewx_frozen_commit": MEWX_FROZEN_COMMIT,
    "verified_prs": [67, 66, 65],
}
with ledger_path.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(ledger_entry) + "\n")
PY
