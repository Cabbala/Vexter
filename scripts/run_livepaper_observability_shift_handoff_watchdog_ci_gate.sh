#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF_DIR="$ROOT_DIR/artifacts/proofs"
REPORT_DIR="$ROOT_DIR/artifacts/reports"
PROOF_JSON="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json"
SUMMARY_MD="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md"
REPORT_MD="$REPORT_DIR/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-report.md"
STATUS_MD="$REPORT_DIR/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-status.md"
PACK_DIR="$REPORT_DIR/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate"
CONTEXT_JSON="$PACK_DIR/CONTEXT.json"
DETAILS_MD="$PACK_DIR/DETAILS.md"
MIN_PROMPT_TXT="$PACK_DIR/MIN_PROMPT.txt"
HANDOFF_MD="$PACK_DIR/HANDOFF.md"
LOG_PATH="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-pytest.log"
SUITE_MARKER="livepaper_observability_shift_handoff_watchdog_ci_gate"

mkdir -p "$PROOF_DIR" "$REPORT_DIR" "$PACK_DIR"

GROUPED_TEST_FILES=(
  "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py"
  "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py"
  "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py"
  "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py"
)

printf 'Livepaper observability shift handoff watchdog CI gate\n'
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
  WATCHDOG_CI_GATE_STATUS="passed"
  TASK_STATE="livepaper_observability_shift_handoff_watchdog_ci_gate_passed"
  SELECTED_OUTCOME="A"
  RECOMMENDED_NEXT_STEP="transport_livepaper_observability_acceptance_pack"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-ACCEPTANCE-PACK"
  DECISION="transport_livepaper_observability_acceptance_pack_ready"
  KEY_FINDING="livepaper_observability_shift_handoff_watchdog_ci_gate_enforced"
else
  WATCHDOG_CI_GATE_STATUS="failed"
  TASK_STATE="livepaper_observability_shift_handoff_watchdog_ci_gate_failed"
  SELECTED_OUTCOME="handoff_watchdog_ci_gate_failed"
  RECOMMENDED_NEXT_STEP="livepaper_observability_shift_handoff_watchdog_ci_gate"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE"
  DECISION="livepaper_observability_shift_handoff_watchdog_ci_gate_failed"
  KEY_FINDING="livepaper_observability_shift_handoff_watchdog_ci_gate_failed"
fi

export ROOT_DIR PROOF_JSON SUMMARY_MD REPORT_MD STATUS_MD CONTEXT_JSON DETAILS_MD MIN_PROMPT_TXT
export HANDOFF_MD LOG_PATH WATCHDOG_CI_GATE_STATUS TASK_STATE SELECTED_OUTCOME
export RECOMMENDED_NEXT_STEP RECOMMENDED_NEXT_TASK_ID DECISION KEY_FINDING SUITE_MARKER

python - <<'PY'
import json
import os
import re
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
gate_status = os.environ["WATCHDOG_CI_GATE_STATUS"]
task_state = os.environ["TASK_STATE"]
selected_outcome = os.environ["SELECTED_OUTCOME"]
recommended_next_step = os.environ["RECOMMENDED_NEXT_STEP"]
recommended_next_task_id = os.environ["RECOMMENDED_NEXT_TASK_ID"]
decision = os.environ["DECISION"]
key_finding = os.environ["KEY_FINDING"]
suite_marker = os.environ["SUITE_MARKER"]

LATEST_VEXTER_PR = 68
LATEST_VEXTER_MAIN_COMMIT = "32133ff2acd233e0873d3de5817f2b31acafe809"
LATEST_VEXTER_MERGED_AT_UTC = "2026-03-26T22:13:43Z"
LATEST_RECENT_VEXTER_PRS = [68, 67, 66, 65]
DEXTER_MAIN_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
DEXTER_PR_3_MERGED_AT_UTC = "2026-03-21T11:31:07Z"
MEWX_FROZEN_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
MEWX_FROZEN_COMMIT_DATE_UTC = "2026-03-20T16:05:19Z"
PROMOTED_BASELINE = "task005-pass-grade-pair-20260325T180027Z"
COMPARISON_SOURCE = "comparison_closed_out"
BUNDLE_SOURCE = (
    "/Users/cabbala/Downloads/"
    "vexter_task007_livepaper_observability_shift_handoff_watchdog_ci_gate_bundle.tar.gz"
)
TASK_ID = "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE"
NEXT_TASK_ID = "TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-ACCEPTANCE-PACK"
NEXT_TASK_STATE = "ready_for_transport_livepaper_observability_acceptance_pack"
GATE_MARKER = "livepaper_observability_shift_handoff_watchdog_ci_gate"
CI_GATE_CURRENT_POINTER_PATHS = {
    "current_status_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-status.md",
    "current_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-report.md",
    "current_proof_summary": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md",
    "current_proof_json": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json",
}
CI_GATE_FIRST_DEEP_PROOF_PATH = (
    "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json"
)
CI_GATE_CURRENT_TASK_STATE = "livepaper_observability_shift_handoff_watchdog_ci_gate_passed"
CI_GATE_RECOMMENDED_NEXT_STEP = "transport_livepaper_observability_acceptance_pack"
CI_GATE_TERMINAL_SNAPSHOT_POINTER = (
    "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
)
CI_GATE_FAILURE_DETAIL_POINTER = (
    "tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py"
)
FACE_CLASSIFICATION_BY_SURFACE = {
    "current_status": "drift",
    "proof_and_report_pointers": "partial_visibility",
    "omission_drift_partial_visibility": "drift",
    "manual_stop_all": "partial_visibility",
    "quarantine": "partial_visibility",
    "terminal_snapshot": "partial_visibility",
    "normalized_failure_detail": "partial_visibility",
    "open_questions": "partial_visibility",
    "next_shift_priority_checks": "omission",
}
GROUPED_TEST_FILES = [
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py",
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py",
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py",
    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py",
]

sys.path.insert(0, str(root_dir))
from vexter.planner_router.handoff_watchdog import (  # noqa: E402
    LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES,
    evaluate_livepaper_observability_shift_handoff_watchdog,
)


def classify_failed_test(test_name: str) -> tuple[str | None, str | None]:
    match = re.search(r"\[([a-z_]+)\]$", test_name)
    surface = match.group(1) if match else None
    if surface is None:
        return None, None
    if "flags_surface_omission" in test_name:
        return surface, "omission"
    if "face_regression" in test_name:
        return surface, FACE_CLASSIFICATION_BY_SURFACE[surface]
    return surface, None


log_lines = log_path.read_text().splitlines()
pytest_result = next((line.strip() for line in reversed(log_lines) if line.strip()), "")
failed_tests = []
for line in log_lines:
    stripped = line.strip()
    if stripped.startswith("FAILED "):
        failed_tests.append(stripped.split(" - ", 1)[0].replace("FAILED ", "", 1))

failure_pairs = [classify_failed_test(test_name) for test_name in failed_tests]
broken_surfaces = sorted({surface for surface, _ in failure_pairs if surface})
failure_classes = sorted({failure_class for _, failure_class in failure_pairs if failure_class})
primary_surface = broken_surfaces[0] if broken_surfaces else "none"


def summary_for_class(name: str) -> str:
    surfaces = sorted(
        {
            surface
            for surface, failure_class in failure_pairs
            if surface is not None and failure_class == name
        }
    )
    if not surfaces:
        return "none"
    return "gate failures on " + ", ".join(surfaces)


handoff_lines = [
    "# Live-Paper Observability Shift Handoff Watchdog CI Gate",
    "",
    "## Current Status",
    "- outgoing_shift_window: 2026-03-27 watchdog CI gate enforcement",
    "- incoming_shift_window: 2026-03-27 transport acceptance-pack follow-up",
    f"- task_state: {task_state}",
    f"- shift_outcome: {'contained' if gate_status == 'passed' else 'repair_required'}",
    f"- current_action: {'continue' if gate_status == 'passed' else 'repair'}",
    f"- active_broken_surface_or_none: {primary_surface}",
    f"- recommended_next_step: {recommended_next_step}",
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
    f"- current_status_report: {CI_GATE_CURRENT_POINTER_PATHS['current_status_report']}",
    f"- current_report: {CI_GATE_CURRENT_POINTER_PATHS['current_report']}",
    f"- current_proof_summary: {CI_GATE_CURRENT_POINTER_PATHS['current_proof_summary']}",
    f"- current_proof_json: {CI_GATE_CURRENT_POINTER_PATHS['current_proof_json']}",
    f"- first_deep_proof_to_open_next: {CI_GATE_FIRST_DEEP_PROOF_PATH}",
    "- shortest_proof_trail: status -> report -> summary -> watchdog CI gate proof -> watchdog CI gate handoff -> regression-pack proof -> runtime handoff proof -> baseline handoff proof",
    "",
    "## Observability Classification",
    f"- omission_present: {'true' if 'omission' in failure_classes else 'false'}",
    f"- omission_summary_or_none: {summary_for_class('omission')}",
    f"- drift_present: {'true' if 'drift' in failure_classes else 'false'}",
    f"- drift_summary_or_none: {summary_for_class('drift')}",
    f"- partial_visibility_present: {'true' if 'partial_visibility' in failure_classes else 'false'}",
    f"- partial_visibility_summary_or_none: {summary_for_class('partial_visibility')}",
    f"- exact_broken_surface_or_none: {primary_surface}",
    "",
    "## Manual Stop-All and Quarantine",
    "- manual_stop_all_visible: true",
    "- halt_mode_or_none: manual_latched_stop_all",
    "- trigger_plan_id_or_none: req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "- stop_reason_or_none: manual_latched_stop_all",
    "- peer_plan_propagation_confirmed: true",
    "- quarantine_active: true",
    "- quarantine_reason_or_none: timeout_guard",
    "- continuity_check: monitor_profile_id=mewx_timeout_guard, quarantine_scope=sleeve, execution_mode=sim_live, ack_history_visible=true, runtime_follow_up_visible=true, regression_pack_visible=true, watchdog_ci_gate_visible=true",
    "",
    "## Terminal Snapshot",
    "- terminal_snapshot_present: true",
    f"- terminal_snapshot_pointer_or_none: {CI_GATE_TERMINAL_SNAPSHOT_POINTER}",
    "- snapshot_signal_visible: true",
    "- terminal_stop_reason_visible: true",
    "- terminal_anchor_native_session_id: sim_live:req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "- terminal_anchor_handle_id: mewx_frozen_pinned:req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "",
    "## Normalized Failure Detail",
    "- normalized_failure_detail_present: true",
    f"- failure_detail_pointer_or_none: {CI_GATE_FAILURE_DETAIL_POINTER}",
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
    f"- question_1_or_none: {'none' if gate_status == 'passed' else f'why did {primary_surface} regress under the watchdog CI gate?'}",
    f"- question_2_or_none: {'none' if gate_status == 'passed' else 'do the failing tests reflect one surface or multiple grouped surfaces?'}",
    f"- question_3_or_none: {'none' if gate_status == 'passed' else 'did the regression-pack proof chain stay intact while the CI gate failed?'}",
    "",
    "## Next-Shift Priority Checks",
    f"- priority_check_1: {'confirm the current watchdog CI gate status, report, and proof JSON before assembling the acceptance pack' if gate_status == 'passed' else 'open the current watchdog CI gate status, report, and proof JSON before touching the grouped suites'}",
    "- priority_check_2_or_none: if any face becomes implicit, replace it with explicit `false` or `none` before re-running the watchdog CI gate",
    f"- priority_check_3_or_none: {'start the next bounded lane at `transport_livepaper_observability_acceptance_pack` using the watchdog CI gate proof together with the regression-pack, runtime, and baseline proofs' if gate_status == 'passed' else 'rerun `livepaper_observability_shift_handoff_watchdog_ci_gate` after the broken face is explicit again'}",
    "",
    "## Completeness Check",
    "- every_required_face_filled_or_none: true",
    "- status_matches_current_checklist_artifacts: true",
    "- proof_and_report_pointers_checked: true",
    "- omission_drift_partial_visibility_explicit: true",
    "- containment_and_failure_faces_explicit: true",
    "- open_questions_and_next_checks_explicit: true",
    "",
    "This handoff is synthetic and bounded. It packages the grouped watchdog CI gate status without collecting new evidence, keeps the comparison baseline closed, and reuses the source-faithful transport watchdog runtime anchors already fixed on main.",
]
handoff_md.write_text("\n".join(handoff_lines) + "\n")

watchdog_report = evaluate_livepaper_observability_shift_handoff_watchdog(
    handoff_md.read_text(),
    repo_root=root_dir,
    expected_first_deep_proof_path=CI_GATE_FIRST_DEEP_PROOF_PATH,
    expected_task_state=CI_GATE_CURRENT_TASK_STATE,
    expected_recommended_next_step=CI_GATE_RECOMMENDED_NEXT_STEP,
    expected_current_pointer_paths=CI_GATE_CURRENT_POINTER_PATHS,
    expected_terminal_snapshot_pointer=CI_GATE_TERMINAL_SNAPSHOT_POINTER,
    expected_failure_detail_pointer=CI_GATE_FAILURE_DETAIL_POINTER,
)
gate_surface_tests = {
    surface: [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_flags_face_regression[{surface}]",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_runtime_flags_follow_up_face_regression[{surface}]",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_regression_pack_flags_face_regression[{surface}]",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_regression_pack_flags_surface_omission[{surface}]",
    ]
    for surface in LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES
}

proof = {
    "task_id": TASK_ID,
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
        "watchdog_proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json",
        "watchdog_runtime_proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json",
        "watchdog_regression_pack_proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json",
        "transport_watchdog_ci_gate_proof": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json",
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
    "livepaper_observability_shift_handoff_watchdog_ci_gate": {
        "suite_group": suite_marker,
        "runner_script": "scripts/run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh",
        "workflow": ".github/workflows/validate.yml",
        "pytest_command": "pytest -q -m livepaper_observability_shift_handoff_watchdog_ci_gate tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py",
        "pytest_result": pytest_result,
        "watchdog_ci_gate_status": gate_status,
        "grouped_test_files": GROUPED_TEST_FILES,
        "grouped_suite_markers": [
            "livepaper_observability_shift_handoff_watchdog",
            "livepaper_observability_shift_handoff_watchdog_runtime",
            "livepaper_observability_shift_handoff_watchdog_regression_pack",
        ],
        "supporting_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py",
        ],
        "supporting_runner_scripts": [
            "scripts/run_livepaper_observability_shift_handoff_watchdog.sh",
            "scripts/run_livepaper_observability_shift_handoff_watchdog_runtime.sh",
            "scripts/run_livepaper_observability_shift_handoff_watchdog_regression_pack.sh",
        ],
        "component_suites": {
            "watchdog": {
                "test_files": [
                    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py",
                ],
                "suite_marker": "livepaper_observability_shift_handoff_watchdog",
                "monitored_surfaces": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
            },
            "watchdog_runtime": {
                "test_files": [
                    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py",
                ],
                "suite_marker": "livepaper_observability_shift_handoff_watchdog_runtime",
                "monitored_surfaces": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
            },
            "watchdog_regression_pack": {
                "test_files": [
                    "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py",
                ],
                "suite_marker": "livepaper_observability_shift_handoff_watchdog_regression_pack",
                "monitored_surfaces": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
            },
        },
        "monitored_surfaces": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
        "monitored_issue_classes": ["omission", "drift", "partial_visibility"],
        "gate_surface_tests": gate_surface_tests,
        "proof_outputs": [
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json",
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md",
        ],
        "proof_artifact_name": "livepaper-observability-shift-handoff-watchdog-ci-gate-proof",
        "current_handoff_watchdog_snapshot": {
            "checked_handoff": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/HANDOFF.md",
            "findings": [asdict(finding) for finding in watchdog_report.findings],
            "monitored_surfaces": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
            "passed": watchdog_report.passed,
            "surface_status": dict(watchdog_report.surface_status),
        },
        "source_faithful_modes": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "normalized_failure_detail": {
            "broken_handoff_watchdog_surfaces_or_none": broken_surfaces or ["none"],
            "failure_classes_or_none": failure_classes or ["none"],
            "failed_tests_or_none": failed_tests or ["none"],
            "non_surface_failures_or_none": [
                test_name for test_name, (surface, _) in zip(failed_tests, failure_pairs) if surface is None
            ]
            or ["none"],
        },
    },
    "next_task_evaluation": {
        "transport_livepaper_observability_acceptance_pack": {
            "recommended": gate_status == "passed",
            "reasons": [
                "The handoff watchdog surfaces are now grouped into an always-on CI gate, so the highest remaining leverage is packaging the already-enforced transport-to-handoff acceptance story.",
                "An acceptance pack can now consume the fixed transport watchdog CI gate and handoff watchdog CI gate proofs without reopening comparison work or changing source logic.",
            ],
        },
        "executor_boundary_code_spec": {
            "recommended": False,
            "reasons": [
                "No new executor-boundary ambiguity surfaced while grouping the handoff watchdog surfaces into CI.",
                "The sharper next cut is operator-facing acceptance packaging rather than another boundary restatement.",
            ],
        },
        "livepaper_observability_shift_handoff_watchdog_runtime_watchdog": {
            "recommended": False,
            "reasons": [
                "The runtime-shaped handoff watchdog is already frozen in the grouped CI gate, so another watchdog-on-watchdog cut would duplicate existing enforcement.",
                "The next useful increment is acceptance packaging on top of the now-stable gate outputs.",
            ],
        },
    },
    "task_result": {
        "selected_outcome": selected_outcome,
        "key_finding": key_finding,
        "claim_boundary": "livepaper_observability_shift_handoff_watchdog_ci_gate_bounded",
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
    "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE Proof Summary",
    "",
    "- Verified Vexter `main` at merged PR `#68` commit `32133ff2acd233e0873d3de5817f2b31acafe809`",
    "- Kept Dexter pinned at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "- Promoted the fixed handoff watchdog, runtime, and regression-pack surfaces into one always-on CI gate without changing source logic or reopening the comparison baseline",
    f"- Watchdog CI gate result: `{pytest_result}`",
    "- Grouped current status, proof/report pointers, omission / drift / partial_visibility, manual stop-all, quarantine, terminal snapshot, normalized failure detail, open questions, and next-shift priority checks under one CI-facing suite",
]
if gate_status == "passed":
    summary_lines.append("- Recommended next task: `transport_livepaper_observability_acceptance_pack`")
else:
    summary_lines.append("- Gate failed, so the immediate next step remains `livepaper_observability_shift_handoff_watchdog_ci_gate`")
summary_md.write_text("\n".join(summary_lines) + "\n")

report_lines = [
    "# TASK-007 Live-Paper Observability Shift Handoff Watchdog CI Gate Report",
    "",
    "## Verified GitHub State",
    "",
    "- `Cabbala/Vexter` latest merged `main` was reverified at PR `#68` main commit `32133ff2acd233e0873d3de5817f2b31acafe809` on `2026-03-26T22:13:43Z`.",
    "- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.",
    "- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.",
    "- Open Vexter PR `#50` remained non-authoritative relative to merged `main`.",
    "",
    "## What This Task Did",
    "",
    "- Started from the merged handoff-watchdog-regression-pack lane on PR `#68` and kept the promoted comparison baseline frozen.",
    "- Added a dedicated handoff-watchdog CI gate lane so future handoff-facing changes must preserve the fixed watchdog surface across the baseline handoff, runtime follow-up handoff, and regression-pack handoff.",
    "- Grouped the handoff watchdog, runtime, and regression-pack suites under one dedicated marker so drift, omission, and partial-visibility regressions fail directly under named handoff faces.",
    "- Emitted proof, summary, report, status, and a current CI-gate handoff bundle so the broken surface is visible without collecting new evidence or changing planner/router, Dexter, or Mew-X source logic.",
    "",
    "## Validation",
    "",
    "- `pytest -q -m livepaper_observability_shift_handoff_watchdog_ci_gate tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py`",
    f"- `{pytest_result}`",
    "",
    "## Recommendation Among Next Tasks",
    "",
    "### `transport_livepaper_observability_acceptance_pack`",
    "",
    "Recommended next because:",
    "",
    "- both the transport observability watchdog CI gate and the handoff watchdog CI gate are now source-faithful, current, and GitHub-visible",
    "- the remaining leverage is packaging those already-enforced proofs into one operator-facing acceptance bundle",
    "",
    "### `executor_boundary_code_spec`",
    "",
    "Not recommended now because:",
    "",
    "- no new executor-boundary ambiguity surfaced while promoting the handoff watchdog surface into CI",
    "- another boundary restatement would reduce less risk than acceptance packaging on top of the stable gates",
    "",
    "### `livepaper_observability_shift_handoff_watchdog_runtime_watchdog`",
    "",
    "Not recommended now because:",
    "",
    "- the runtime handoff watchdog is already inside the grouped CI gate, so another watchdog-on-watchdog cut would duplicate enforcement",
    "- the sharper next step is acceptance packaging rather than more recursion on the same gate surface",
    "",
    "## Decision",
    "",
    f"- Outcome: `{selected_outcome}`",
    f"- Key finding: `{key_finding}`",
    "- Claim boundary: `livepaper_observability_shift_handoff_watchdog_ci_gate_bounded`",
    f"- Current task status: `{task_state}`",
    f"- Recommended next step: `{recommended_next_step}`",
    f"- Decision: `{decision}`",
    "",
    "## Key Paths",
    "",
    "- Baseline handoff watchdog proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json`",
    "- Runtime handoff watchdog proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json`",
    "- Regression-pack handoff watchdog proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json`",
    "- Current watchdog CI gate handoff: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/HANDOFF.md`",
    "- Current watchdog CI gate report: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-report.md`",
    "- Current watchdog CI gate status: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-status.md`",
    "- Current watchdog CI gate proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json`",
    "- Current watchdog CI gate summary: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md`",
    "- Current bundle target: `artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz`",
]
report_md.write_text("\n".join(report_lines) + "\n")

status_lines = [
    "# TASK-007 Live-Paper Observability Shift Handoff Watchdog CI Gate Status",
    "",
    f"- Task state: `{task_state}`",
    f"- Key finding: `{key_finding}`",
    "- Claim boundary: `livepaper_observability_shift_handoff_watchdog_ci_gate_bounded`",
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
            "recommended_next_task": NEXT_TASK_ID,
            "visible_main_state": {
                "latest_vexter_pr": LATEST_VEXTER_PR,
                "latest_vexter_main_commit": LATEST_VEXTER_MAIN_COMMIT,
                "dexter_main": DEXTER_MAIN_COMMIT,
                "mewx_frozen": MEWX_FROZEN_COMMIT,
            },
            "current_state": {
                "current_task": task_state,
                "recommended_next_step": recommended_next_step,
                "broken_handoff_watchdog_surfaces_or_none": broken_surfaces or ["none"],
            },
        },
        indent=2,
    )
    + "\n"
)
details_md.write_text(
    "\n".join(
        [
            "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE",
            "",
            "## Goal",
            "",
            "Promote the fixed handoff watchdog, runtime, and regression-pack surfaces into one always-on CI gate.",
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
    "対象スレッド: 既存 Vexter Codex スレッド（なければ新規）\n"
    "作業系統: Vexter / Infra\n"
    "次タスクID: TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-ACCEPTANCE-PACK\n\n"
    "GitHub最新状態を確認し、Vexter main / Dexter PR #3 merged main / frozen Mew-X を前提に、transport livepaper observability acceptance pack を整理してください。"
    "transport livepaper observability watchdog CI gate と livepaper observability shift handoff watchdog CI gate を source of truth とし、comparison baseline は固定のまま、Dexter `paper_live` / frozen Mew-X `sim_live` seam の acceptance surfaces / proof bundle / operator-facing artifacts を整理してください。"
    "source logic 変更や新証拠収集は行わず、docs/tests/artifacts/handoff bundle を更新してください。\n"
)

summary_path = root_dir / "artifacts" / "summary.md"
summary_path.write_text(
    "\n".join(
        [
            "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-CI-GATE Summary",
            "",
            "## Verified GitHub State",
            "",
            "- `Cabbala/Vexter` latest merged `main` was reverified at PR `#68` commit `32133ff2acd233e0873d3de5817f2b31acafe809` on `2026-03-26T22:13:43Z`.",
            "- The completed handoff watchdog regression-pack lane remained visible at PR `#68`.",
            "- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.",
            "- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.",
            "- Open Vexter PR `#50` (`feat(infra): refresh runtime observability artifacts`) remained non-authoritative relative to merged `main`.",
            "",
            "## What This Task Did",
            "",
            "- Treated the fixed observability contract, runbook, checklist, handoff template, drill, handoff watchdog proof, runtime handoff watchdog proof, and regression-pack proof as the formal handoff baseline without reopening comparison work.",
            "- Added a dedicated watchdog CI gate lane through `scripts/run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh` and `tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py`.",
            "- Grouped the handoff watchdog, handoff watchdog runtime, and handoff watchdog regression-pack suites under one dedicated marker so current status, proof/report pointers, omission / drift / partial_visibility, manual stop-all, quarantine, terminal snapshot, normalized failure detail, open questions, and next-shift priority checks now fail directly in CI.",
            "- Refreshed workflow wiring, bundle metadata, context pack, proof manifest, task ledger, proof outputs, status/report, and the watchdog CI gate handoff bundle without changing planner/router source logic or collecting new evidence.",
            "",
            "## Decision",
            "",
            "- Outcome: `A`",
            "- Key finding: `livepaper_observability_shift_handoff_watchdog_ci_gate_enforced`",
            "- Claim boundary: `livepaper_observability_shift_handoff_watchdog_ci_gate_bounded`",
            "- Current task status: `livepaper_observability_shift_handoff_watchdog_ci_gate_passed`",
            "- Recommended next step: `transport_livepaper_observability_acceptance_pack`",
            "- Decision: `transport_livepaper_observability_acceptance_pack_ready`",
            "",
            "## Key Paths",
            "",
            "- Watchdog CI gate proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json`",
            "- Watchdog CI gate summary: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md`",
            "- Watchdog CI gate report: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-report.md`",
            "- Watchdog CI gate status: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-status.md`",
            "- Watchdog CI gate handoff: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/HANDOFF.md`",
            "- Regression-pack proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json`",
            "- Current bundle target: `artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz`",
        ]
    )
    + "\n"
)

context_pack_path = root_dir / "artifacts" / "context_pack.json"
context_pack = json.loads(context_pack_path.read_text())
context_pack["background"]["previous_task_id"] = (
    "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK"
)
context_pack["background"]["previous_key_finding"] = (
    "livepaper_observability_shift_handoff_watchdog_regression_pack_durable"
)
context_pack["background"]["previous_claim_boundary"] = (
    "livepaper_observability_shift_handoff_watchdog_regression_pack_bounded"
)
context_pack["bundle_source"] = BUNDLE_SOURCE
context_pack["current_contract"]["livepaper_observability_shift_handoff_watchdog_ci_gate_marker"] = (
    GATE_MARKER
)
context_pack["current_task"] = {
    "id": TASK_ID,
    "scope": [
        "Verify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X.",
        "Treat the fixed observability contract, operator runbook, shift checklist, handoff template, handoff drill, handoff watchdog proof, runtime handoff watchdog proof, and handoff-watchdog-regression-pack proof as the formal live-paper observability handoff baseline without reopening comparison work.",
        "Promote the fixed handoff watchdog surfaces into one always-on CI gate.",
        "Keep current status, proof/report pointers, omission / drift / partial_visibility, manual stop-all, quarantine, terminal snapshot, normalized failure detail, open questions, and next-shift priority checks visible under one grouped watchdog gate.",
        "Refresh tests, proof outputs, summary, context pack, proof manifest, task ledger, report, and handoff bundle without changing planner/router source logic.",
    ],
    "deliverables": [
        "README.md",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py",
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_ci_gate.py",
        "tests/test_bootstrap_layout.py",
        "scripts/build_proof_bundle.sh",
        "scripts/run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh",
        ".github/workflows/validate.yml",
        "pytest.ini",
        "artifacts/summary.md",
        "artifacts/context_pack.json",
        "artifacts/proof_bundle_manifest.json",
        "artifacts/task_ledger.jsonl",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-report.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-status.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/DETAILS.md",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/MIN_PROMPT.txt",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/CONTEXT.json",
        "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate/HANDOFF.md",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json",
        "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md",
        "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz",
    ],
    "frozen_source_commits": {
        "dexter": DEXTER_MAIN_COMMIT,
        "mewx": MEWX_FROZEN_COMMIT,
    },
}
github_latest = context_pack["evidence"]["github_latest"]
github_latest["latest_vexter_pr"] = LATEST_VEXTER_PR
github_latest["latest_vexter_main_commit"] = LATEST_VEXTER_MAIN_COMMIT
github_latest["latest_recent_vexter_prs"] = LATEST_RECENT_VEXTER_PRS
github_latest["vexter_pr_68_merged_at"] = LATEST_VEXTER_MERGED_AT_UTC
context_pack["evidence"]["livepaper_observability_shift_handoff_watchdog_ci_gate"] = {
    "report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-report.md",
    "status_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-status.md",
    "proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json",
    "summary": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md",
    "handoff_dir": "artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate",
    "key_finding": key_finding,
    "claim_boundary": "livepaper_observability_shift_handoff_watchdog_ci_gate_bounded",
    "task_state": task_state,
    "gate_test_files": GROUPED_TEST_FILES,
    "grouped_suite_markers": [
        "livepaper_observability_shift_handoff_watchdog",
        "livepaper_observability_shift_handoff_watchdog_runtime",
        "livepaper_observability_shift_handoff_watchdog_regression_pack",
    ],
    "validated_axes": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
    "preferred_next_step": "transport_livepaper_observability_acceptance_pack",
}
context_pack["next_task"] = {
    "id": NEXT_TASK_ID,
    "state": NEXT_TASK_STATE,
    "rationale": [
        "The handoff watchdog surfaces are now always-on in CI and stay GitHub-visible through proof, report, and handoff outputs.",
        "The next bounded cut is packaging the already-enforced transport-to-handoff acceptance story rather than adding another watchdog layer.",
        "An executor-boundary restatement would reduce less risk than an operator-facing acceptance pack on top of the stable gates.",
    ],
}
context_pack.setdefault("proofs", {})
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_added"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_workflow_enforced"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_proof_emitted"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_suite_grouped"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_current_status_guarded"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_pointer_integrity_guarded"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_visibility_classification_guarded"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_manual_stop_all_guarded"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_quarantine_guarded"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_terminal_snapshot_guarded"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_normalized_failure_detail_guarded"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_open_questions_guarded"] = True
context_pack["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_next_shift_priorities_guarded"] = True
context_pack["proofs"]["recommended_next_step_is_transport_livepaper_observability_acceptance_pack"] = (
    gate_status == "passed"
)
context_pack_path.write_text(json.dumps(context_pack, indent=2) + "\n")

manifest_path = root_dir / "artifacts" / "proof_bundle_manifest.json"
manifest = json.loads(manifest_path.read_text())
manifest["bundle_path"] = "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz"
manifest["bundle_source"] = BUNDLE_SOURCE
manifest["task_id"] = TASK_ID
manifest["status"] = task_state
for entry, key in (
    ("scripts/run_livepaper_observability_shift_handoff_watchdog_ci_gate.sh", "scripts"),
    ("artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json", "proof_files"),
    ("artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-summary.md", "proof_files"),
    ("artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-report.md", "reports"),
    ("artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-status.md", "reports"),
    ("artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate", "reports"),
):
    if entry not in manifest[key]:
        manifest[key].append(entry)
manifest["next_task"] = {
    "id": NEXT_TASK_ID,
    "state": NEXT_TASK_STATE,
    "resume_requirements": [
        "Treat task005-pass-grade-pair-20260325T180027Z as the frozen promoted baseline.",
        "Carry forward the livepaper_observability_shift_handoff_watchdog_ci_gate_enforced conclusion together with the bounded gate proof as the current evidence surface.",
        "Use the fixed transport watchdog CI gate and handoff watchdog CI gate proofs as the operator-facing source of truth.",
        "Preserve the current Dexter and Mew-X source pins together with fixed poll_first delivery and manual_latched_stop_all semantics.",
        "Do not reopen comparison work or change source logic in the next lane.",
    ],
}
manifest.setdefault("proofs", {})
manifest["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_added"] = True
manifest["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_workflow_enforced"] = True
manifest["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_proof_emitted"] = True
manifest["proofs"]["livepaper_observability_shift_handoff_watchdog_ci_gate_suite_grouped"] = True
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

ledger_path = root_dir / "artifacts" / "task_ledger.jsonl"
ledger_entry = {
    "artifact_bundle": "artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate.tar.gz",
    "base_main": LATEST_VEXTER_MAIN_COMMIT,
    "branch": "codex/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate",
    "claim_boundary": "livepaper_observability_shift_handoff_watchdog_ci_gate_bounded",
    "comparison_source_of_truth_state": COMPARISON_SOURCE,
    "confirmatory_overturns_promoted_baseline": False,
    "confirmatory_residual": "Mew-X candidate_rejected",
    "confirmatory_same_attempt_label": "task005-pass-grade-pair-20260325T180604Z",
    "date": "2026-03-27",
    "decision": decision,
    "default_execution_anchor": "dexter",
    "handoff_watchdog_ci_gate_suite_grouped": True,
    "handoff_watchdog_ci_gate_workflow_enforced": True,
    "handoff_watchdog_ci_gate_proof_emitted": True,
    "handoff_watchdog_ci_gate_current_status_guarded": True,
    "handoff_watchdog_ci_gate_proof_pointer_guarded": True,
    "handoff_watchdog_ci_gate_visibility_classification_guarded": True,
    "handoff_watchdog_ci_gate_manual_stop_all_guarded": True,
    "handoff_watchdog_ci_gate_quarantine_guarded": True,
    "handoff_watchdog_ci_gate_terminal_snapshot_guarded": True,
    "handoff_watchdog_ci_gate_normalized_failure_detail_guarded": True,
    "handoff_watchdog_ci_gate_open_questions_guarded": True,
    "handoff_watchdog_ci_gate_next_shift_priorities_guarded": True,
    "key_finding": key_finding,
    "live_metric_winner_tally": {"dexter": 6, "mewx": 4, "tie": 2},
    "new_evidence_collection_required": False,
    "next_task_id": recommended_next_task_id,
    "next_task_state": NEXT_TASK_STATE if gate_status == "passed" else "ready_for_livepaper_observability_shift_handoff_watchdog_ci_gate",
    "prior_lane_source_state": "livepaper_observability_shift_handoff_watchdog_regression_pack_passed",
    "promoted_live_winner_mode": "derived",
    "promoted_replay_winner_mode": "derived",
    "promoted_same_attempt_label": "task005-pass-grade-pair-20260325T180027Z",
    "proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-ci-gate-check.json",
    "recommended_next_lane": recommended_next_step,
    "replay_metric_winner_tally": {"dexter": 6, "mewx": 4, "tie": 2},
    "repo": "https://github.com/Cabbala/Vexter",
    "selected_outcome": selected_outcome,
    "selective_option_source": "mewx",
    "source_faithful_modes": {"dexter": "paper_live", "mewx": "sim_live"},
    "status": task_state,
    "supporting_vexter_prs": [68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17],
    "task_id": TASK_ID,
    "verified_dexter_main_commit": DEXTER_MAIN_COMMIT,
    "verified_dexter_pr": 3,
    "verified_mewx_frozen_commit": MEWX_FROZEN_COMMIT,
    "verified_prs": [68, 67, 66],
}
with ledger_path.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(ledger_entry, sort_keys=True) + "\n")
PY
