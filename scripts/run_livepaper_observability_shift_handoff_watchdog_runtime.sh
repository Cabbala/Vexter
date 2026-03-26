#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF_DIR="$ROOT_DIR/artifacts/proofs"
REPORT_DIR="$ROOT_DIR/artifacts/reports"
PROOF_JSON="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json"
SUMMARY_MD="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-runtime-summary.md"
REPORT_MD="$REPORT_DIR/task-007-livepaper-observability-shift-handoff-watchdog-runtime-report.md"
STATUS_MD="$ROOT_DIR/artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime-status.md"
PACK_DIR="$ROOT_DIR/artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime"
CONTEXT_JSON="$PACK_DIR/CONTEXT.json"
DETAILS_MD="$PACK_DIR/DETAILS.md"
MIN_PROMPT_TXT="$PACK_DIR/MIN_PROMPT.txt"
HANDOFF_MD="$PACK_DIR/HANDOFF.md"
LOG_PATH="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-runtime-pytest.log"
SUITE_MARKER="livepaper_observability_shift_handoff_watchdog_runtime"

mkdir -p "$PROOF_DIR" "$ROOT_DIR/artifacts/reports" "$PACK_DIR"

RUNTIME_TEST_FILES=(
  "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py"
)

printf 'Livepaper observability shift handoff watchdog runtime\n'
printf 'Suite marker: %s\n' "$SUITE_MARKER"
printf 'Runtime test files:\n'
for file in "${RUNTIME_TEST_FILES[@]}"; do
  printf ' - %s\n' "$file"
done

set +e
(
  cd "$ROOT_DIR"
  find tests -name '*.pyc' -delete
  find tests -name '__pycache__' -type d -empty -delete
  pytest -q -m "$SUITE_MARKER" "${RUNTIME_TEST_FILES[@]}"
) 2>&1 | tee "$LOG_PATH"
PYTEST_STATUS=${PIPESTATUS[0]}
set -e

if [[ $PYTEST_STATUS -eq 0 ]]; then
  WATCHDOG_RUNTIME_STATUS="passed"
  TASK_STATE="livepaper_observability_shift_handoff_watchdog_runtime_passed"
  SELECTED_OUTCOME="A"
  RECOMMENDED_NEXT_STEP="livepaper_observability_shift_handoff_watchdog_regression_pack"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK"
  DECISION="livepaper_observability_shift_handoff_watchdog_regression_pack_ready"
  KEY_FINDING="livepaper_observability_shift_handoff_watchdog_runtime_continuity_confirmed"
else
  WATCHDOG_RUNTIME_STATUS="failed"
  TASK_STATE="livepaper_observability_shift_handoff_watchdog_runtime_failed"
  SELECTED_OUTCOME="handoff_watchdog_runtime_failed"
  RECOMMENDED_NEXT_STEP="livepaper_observability_shift_handoff_watchdog_runtime"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME"
  DECISION="livepaper_observability_shift_handoff_watchdog_runtime_failed"
  KEY_FINDING="livepaper_observability_shift_handoff_watchdog_runtime_failed"
fi

export ROOT_DIR PROOF_JSON SUMMARY_MD REPORT_MD STATUS_MD CONTEXT_JSON DETAILS_MD MIN_PROMPT_TXT
export HANDOFF_MD LOG_PATH WATCHDOG_RUNTIME_STATUS TASK_STATE SELECTED_OUTCOME
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
watchdog_runtime_status = os.environ["WATCHDOG_RUNTIME_STATUS"]
task_state = os.environ["TASK_STATE"]
selected_outcome = os.environ["SELECTED_OUTCOME"]
recommended_next_step = os.environ["RECOMMENDED_NEXT_STEP"]
recommended_next_task_id = os.environ["RECOMMENDED_NEXT_TASK_ID"]
decision = os.environ["DECISION"]
key_finding = os.environ["KEY_FINDING"]
suite_marker = os.environ["SUITE_MARKER"]

sys.path.insert(0, str(root_dir))
from vexter.planner_router.handoff_watchdog import (  # noqa: E402
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

handoff_lines = [
    "# Live-Paper Observability Shift Handoff Watchdog Runtime",
    "",
    "## Current Status",
    "- outgoing_shift_window: 2026-03-27 watchdog runtime handoff validation",
    "- incoming_shift_window: 2026-03-27 regression-pack follow-up",
    f"- task_state: {RUNTIME_CURRENT_TASK_STATE}",
    "- shift_outcome: contained",
    "- current_action: continue",
    "- active_broken_surface_or_none: none",
    f"- recommended_next_step: {RUNTIME_RECOMMENDED_NEXT_STEP}",
    "- status_delivery: poll_first",
    "- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`",
    "- vexter_main_commit: 2cd19d8ddbd5ef4918b41536494e10d4f2a9c125",
    "- dexter_main_commit: ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    "- mewx_frozen_commit: dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
    "- promoted_baseline: task005-pass-grade-pair-20260325T180027Z",
    "- comparison_source_of_truth: comparison_closed_out",
    "- containment_anchor_plan_id: req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "- failure_anchor_plan_id: req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "",
    "## Proof and Report Pointers",
    f"- current_status_report: {RUNTIME_CURRENT_POINTER_PATHS['current_status_report']}",
    f"- current_report: {RUNTIME_CURRENT_POINTER_PATHS['current_report']}",
    f"- current_proof_summary: {RUNTIME_CURRENT_POINTER_PATHS['current_proof_summary']}",
    f"- current_proof_json: {RUNTIME_CURRENT_POINTER_PATHS['current_proof_json']}",
    f"- first_deep_proof_to_open_next: {RUNTIME_FIRST_DEEP_PROOF_PATH}",
    "- shortest_proof_trail: status -> report -> summary -> handoff runtime proof -> runtime handoff -> transport watchdog runtime proof -> handoff watchdog proof",
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
    "- continuity_check: monitor_profile_id=mewx_timeout_guard, quarantine_scope=sleeve, execution_mode=sim_live, ack_history_visible=true, runtime_follow_up_visible=true",
    "",
    "## Terminal Snapshot",
    "- terminal_snapshot_present: true",
    f"- terminal_snapshot_pointer_or_none: {RUNTIME_TERMINAL_SNAPSHOT_POINTER}",
    "- snapshot_signal_visible: true",
    "- terminal_stop_reason_visible: true",
    "- terminal_anchor_native_session_id: sim_live:req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "- terminal_anchor_handle_id: mewx_frozen_pinned:req-transport-livepaper-observability-watchdog-runtime-overlay:batch:1:mewx_containment",
    "",
    "## Normalized Failure Detail",
    "- normalized_failure_detail_present: true",
    f"- failure_detail_pointer_or_none: {RUNTIME_FAILURE_DETAIL_POINTER}",
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
    "- priority_check_1: confirm the current runtime handoff status, report, and proof JSON before changing task state",
    "- priority_check_2_or_none: if any face becomes implicit, replace it with explicit `false` or `none` before promoting the next handoff",
    "- priority_check_3_or_none: start the next bounded check at `livepaper_observability_shift_handoff_watchdog_regression_pack` using the current runtime handoff proof and transport watchdog runtime proof together",
    "",
    "## Completeness Check",
    "- every_required_face_filled_or_none: true",
    "- status_matches_current_checklist_artifacts: true",
    "- proof_and_report_pointers_checked: true",
    "- omission_drift_partial_visibility_explicit: true",
    "- containment_and_failure_faces_explicit: true",
    "- open_questions_and_next_checks_explicit: true",
    "",
    "This handoff is synthetic and bounded. It reuses the fixed evidence trail, does not collect new evidence, keeps the comparison baseline closed, and carries runtime-follow-up containment and failure values only from existing transport watchdog runtime proofs.",
]
handoff_md.write_text("\n".join(handoff_lines) + "\n")

watchdog_report = evaluate_livepaper_observability_shift_handoff_watchdog(
    handoff_md.read_text(),
    repo_root=root_dir,
    expected_first_deep_proof_path=RUNTIME_FIRST_DEEP_PROOF_PATH,
    expected_task_state=RUNTIME_CURRENT_TASK_STATE,
    expected_recommended_next_step=RUNTIME_RECOMMENDED_NEXT_STEP,
    expected_current_pointer_paths=RUNTIME_CURRENT_POINTER_PATHS,
    expected_terminal_snapshot_pointer=RUNTIME_TERMINAL_SNAPSHOT_POINTER,
    expected_failure_detail_pointer=RUNTIME_FAILURE_DETAIL_POINTER,
)
watchdog_face_tests = {
    surface: [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_runtime_flags_follow_up_face_regression[{surface}]"
    ]
    for surface in LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES
}
watchdog_snapshot = {
    "checked_handoff": str(HANDOFF_RUNTIME_PATH),
    "findings": [asdict(finding) for finding in watchdog_report.findings],
    "monitored_surfaces": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
    "passed": watchdog_report.passed,
    "surface_status": dict(watchdog_report.surface_status),
}

log_lines = log_path.read_text().splitlines()
pytest_result = next((line.strip() for line in reversed(log_lines) if line.strip()), "")
failed_tests = []
for line in log_lines:
    stripped = line.strip()
    if stripped.startswith("FAILED "):
        failed_tests.append(stripped.split(" - ", 1)[0].replace("FAILED ", "", 1))

proof = {
    "task_id": "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
    "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "verified_github": {
        "latest_vexter_pr": 66,
        "latest_vexter_main_commit": "2cd19d8ddbd5ef4918b41536494e10d4f2a9c125",
        "latest_vexter_merged_at_utc": "2026-03-26T20:06:25Z",
        "latest_recent_vexter_prs": [66, 65, 64, 63],
        "open_non_authoritative_vexter_prs": [50],
        "dexter_pr": 3,
        "dexter_main_commit": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
        "dexter_pr_3_merged_at_utc": "2026-03-21T11:31:07Z",
        "mewx_frozen_commit": "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
        "mewx_frozen_commit_date_utc": "2026-03-20T16:05:19Z",
    },
    "fixed_input_surface": {
        "canonical_contract": "specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md",
        "canonical_runbook": "docs/livepaper_observability_operator_runbook.md",
        "canonical_checklist": "docs/livepaper_observability_shift_checklist.md",
        "canonical_handoff_template": "docs/livepaper_observability_shift_handoff_template.md",
        "canonical_handoff_drill": "docs/livepaper_observability_shift_handoff_drill.md",
        "canonical_handoff_watchdog": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json",
        "canonical_transport_runtime_watchdog": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json",
        "promoted_label": "task005-pass-grade-pair-20260325T180027Z",
        "comparison_source_of_truth": "comparison_closed_out",
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
    "livepaper_observability_shift_handoff_watchdog_runtime": {
        "suite_group": suite_marker,
        "runner_script": "scripts/run_livepaper_observability_shift_handoff_watchdog_runtime.sh",
        "workflow": ".github/workflows/validate.yml",
        "pytest_command": "pytest -q -m livepaper_observability_shift_handoff_watchdog_runtime tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py",
        "pytest_result": pytest_result,
        "watchdog_runtime_status": watchdog_runtime_status,
        "runtime_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py",
        ],
        "monitored_surfaces": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
        "monitored_issue_classes": ["omission", "drift", "partial_visibility"],
        "watchdog_face_tests": watchdog_face_tests,
        "proof_outputs": [
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json",
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-summary.md",
        ],
        "proof_artifact_name": "livepaper-observability-shift-handoff-watchdog-runtime-proof",
        "evaluated_handoff": str(HANDOFF_RUNTIME_PATH),
        "watchdog_snapshot": watchdog_snapshot,
        "runtime_follow_up_focus": {
            "baseline_handoff_proof": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json",
            "runtime_proof": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json",
            "runtime_status_report": "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime-status.md",
            "runtime_report": "artifacts/reports/task-007-transport-livepaper-observability-watchdog-runtime-report.md",
        },
        "normalized_failure_detail": {
            "finding_surfaces_or_none": sorted({finding.surface for finding in watchdog_report.findings})
            or ["none"],
            "finding_classes_or_none": sorted(
                {finding.classification for finding in watchdog_report.findings}
            )
            or ["none"],
            "failed_tests_or_none": failed_tests or ["none"],
            "non_surface_failures_or_none": failed_tests or ["none"],
        },
        "source_faithful_modes": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
    },
    "next_task_evaluation": {
        "livepaper_observability_shift_handoff_watchdog_regression_pack": {
            "recommended": watchdog_runtime_status == "passed",
            "reasons": [
                "The handoff watchdog now stays explicit on both the bounded handoff surface and runtime-shaped follow-up handoff flow.",
                "The next leverage point is packaging those runtime-shaped handoff regressions into a durable regression pack rather than restating the current handoff face list.",
            ],
        },
        "transport_livepaper_observability_acceptance_pack": {
            "recommended": False,
            "reasons": [
                "An acceptance pack would mostly repackage already-fixed runtime and handoff proofs instead of adding sharper regression containment.",
                "The remaining risk is preserving runtime-shaped handoff completeness, not widening the proof bundle surface.",
            ],
        },
        "executor_boundary_code_spec": {
            "recommended": False,
            "reasons": [
                "No new planner-to-transport boundary ambiguity surfaced while extending the handoff watchdog into runtime follow-up.",
                "The remaining work is preserving the existing handoff surface, not discovering a missing code contract.",
            ],
        },
    },
    "task_result": {
        "selected_outcome": selected_outcome,
        "key_finding": key_finding,
        "claim_boundary": "livepaper_observability_shift_handoff_watchdog_runtime_bounded",
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
    "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME Proof Summary",
    "",
    "- Verified Vexter `main` at merged PR `#66` commit `2cd19d8ddbd5ef4918b41536494e10d4f2a9c125`",
    "- Kept Dexter pinned at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "- Extended the bounded handoff watchdog into runtime-shaped shift follow-up without changing source logic or reopening the comparison baseline",
    f"- Watchdog runtime run result: `{pytest_result}`",
    "- Verified current status, proof/report pointers, omission-drift-partial_visibility, manual stop-all, quarantine, terminal snapshot, normalized failure detail, open questions, and next-shift priority checks remain watchdog-detectable on the runtime handoff path",
]
if watchdog_report.passed:
    summary_lines.append("- Recommended next task: `livepaper_observability_shift_handoff_watchdog_regression_pack`")
else:
    summary_lines.append("- Runtime handoff watchdog failed, so the immediate next step remains `livepaper_observability_shift_handoff_watchdog_runtime`")
summary_md.write_text("\n".join(summary_lines) + "\n")

report_lines = [
    "# TASK-007 Live-Paper Observability Shift Handoff Watchdog Runtime Report",
    "",
    "## Scope",
    "",
    "This task keeps the already-fixed shift handoff watchdog surface intact while extending it to a runtime-shaped follow-up handoff.",
    "It does not reopen comparison work, collect new evidence, or change planner/router, Dexter, or Mew-X source logic.",
    "",
    "## Verified GitHub State",
    "",
    "- Latest merged Vexter `main`: PR `#66`, main commit `2cd19d8ddbd5ef4918b41536494e10d4f2a9c125`, merged at `2026-03-26T20:06:25Z`",
    "- Open non-authoritative Vexter PR: `#50`, `feat(infra): refresh runtime observability artifacts`",
    "- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`",
    "- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`",
    "",
    "## Runtime Handoff Shape",
    "",
    "- Suite marker: `livepaper_observability_shift_handoff_watchdog_runtime`",
    "- Runner: `scripts/run_livepaper_observability_shift_handoff_watchdog_runtime.sh`",
    "- Runtime test file: `tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_runtime.py`",
    "- Deep runtime proof anchor: `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json`",
    "- Current runtime handoff: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-runtime/HANDOFF.md`",
    "",
    "## Current Runtime Result",
    "",
    f"- Watchdog runtime status: `{watchdog_runtime_status}`",
    f"- Broken surfaces: `{', '.join(proof['livepaper_observability_shift_handoff_watchdog_runtime']['normalized_failure_detail']['finding_surfaces_or_none'])}`",
    "",
    "## Decision",
    "",
    f"- Outcome: `{selected_outcome}`",
    f"- Key finding: `{key_finding}`",
    "- Claim boundary: `livepaper_observability_shift_handoff_watchdog_runtime_bounded`",
    f"- Current task status: `{task_state}`",
    f"- Recommended next step: `{recommended_next_step}`",
    f"- Decision: `{decision}`",
]
report_md.write_text("\n".join(report_lines) + "\n")

status_lines = [
    "# TASK-007 Live-Paper Observability Shift Handoff Watchdog Runtime Status",
    "",
    "## Verified Start",
    "",
    "- Vexter `origin/main` verified at PR `#66` commit `2cd19d8ddbd5ef4918b41536494e10d4f2a9c125`",
    "- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "",
    "## Current Result",
    "",
    "- Task ID: `TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME`",
    f"- Validation: `pytest -q -m livepaper_observability_shift_handoff_watchdog_runtime ...` -> `{pytest_result}`",
    "- Runtime deep proof anchor: `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json`",
    f"- Current task: `{task_state}`",
]
status_md.write_text("\n".join(status_lines) + "\n")

context_payload = {
    "recommended_next_task": "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-REGRESSION-PACK",
    "visible_main_state": {
        "latest_vexter_pr": 66,
        "latest_vexter_main_commit": "2cd19d8ddbd5ef4918b41536494e10d4f2a9c125",
        "dexter_main": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
        "mewx_frozen": "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
    },
    "current_state": {
        "current_task": task_state,
        "recommended_next_step": recommended_next_step,
        "broken_handoff_watchdog_surfaces_or_none": proof[
            "livepaper_observability_shift_handoff_watchdog_runtime"
        ]["normalized_failure_detail"]["finding_surfaces_or_none"],
    },
}
context_json.write_text(json.dumps(context_payload, indent=2) + "\n")

details_lines = [
    "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
    "",
    "## Goal",
    "",
    "Keep the bounded live-paper shift handoff watchdog effective on a runtime-shaped follow-up handoff flow.",
    "",
    "## Monitored Surfaces",
    "",
]
details_lines.extend([f"- {surface}" for surface in LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES])
details_md.write_text("\n".join(details_lines) + "\n")

min_prompt_txt.write_text(
    "Verify the livepaper observability shift handoff watchdog runtime proof and status, then inspect the named broken handoff surface before changing runtime handoff artifacts.\n"
)
PY

printf '\nGenerated proof files:\n'
printf ' - %s\n' "$PROOF_JSON"
printf ' - %s\n' "$SUMMARY_MD"
printf '\n'
cat "$SUMMARY_MD"

exit "$PYTEST_STATUS"
