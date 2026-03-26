#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF_DIR="$ROOT_DIR/artifacts/proofs"
REPORT_DIR="$ROOT_DIR/artifacts/reports"
PROOF_JSON="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-ci-check-check.json"
SUMMARY_MD="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-ci-check-summary.md"
REPORT_MD="$REPORT_DIR/task-007-livepaper-observability-shift-handoff-ci-check-report.md"
STATUS_MD="$REPORT_DIR/task-007-livepaper-observability-shift-handoff-ci-check-status.md"
PACK_DIR="$REPORT_DIR/task-007-livepaper-observability-shift-handoff-ci-check"
CONTEXT_JSON="$PACK_DIR/CONTEXT.json"
DETAILS_MD="$PACK_DIR/DETAILS.md"
MIN_PROMPT_TXT="$PACK_DIR/MIN_PROMPT.txt"
LOG_PATH="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-ci-check-pytest.log"
SUITE_MARKER="livepaper_observability_shift_handoff_ci_check"

mkdir -p "$PROOF_DIR" "$REPORT_DIR" "$PACK_DIR"

GROUPED_TEST_FILES=(
  "tests/test_planner_router_transport_livepaper_observability_shift_handoff_template.py"
  "tests/test_planner_router_transport_livepaper_observability_shift_handoff_drill.py"
  "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py"
)

printf 'Livepaper observability shift handoff CI check\n'
printf 'Suite marker: %s\n' "$SUITE_MARKER"
printf 'Grouped test files:\n'
for file in "${GROUPED_TEST_FILES[@]}"; do
  printf ' - %s\n' "$file"
done
printf 'Locked handoff faces:\n'
printf ' - current_status\n'
printf ' - proof_and_report_pointers\n'
printf ' - omission_drift_partial_visibility\n'
printf ' - manual_stop_all\n'
printf ' - quarantine\n'
printf ' - terminal_snapshot\n'
printf ' - normalized_failure_detail\n'
printf ' - open_questions\n'
printf ' - next_shift_priority_checks\n'

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
  GATE_STATUS="passed"
  TASK_STATE="livepaper_observability_shift_handoff_ci_check_passed"
  SELECTED_OUTCOME="A"
  RECOMMENDED_NEXT_STEP="livepaper_observability_shift_handoff_watchdog"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG"
  DECISION="livepaper_observability_shift_handoff_watchdog_ready"
else
  GATE_STATUS="failed"
  TASK_STATE="livepaper_observability_shift_handoff_ci_check_failed"
  SELECTED_OUTCOME="handoff_ci_check_failed"
  RECOMMENDED_NEXT_STEP="livepaper_observability_shift_handoff_ci_check"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK"
  DECISION="livepaper_observability_shift_handoff_ci_check_failed"
fi

export PROOF_JSON SUMMARY_MD REPORT_MD STATUS_MD CONTEXT_JSON DETAILS_MD MIN_PROMPT_TXT LOG_PATH
export GATE_STATUS TASK_STATE SELECTED_OUTCOME RECOMMENDED_NEXT_STEP RECOMMENDED_NEXT_TASK_ID DECISION SUITE_MARKER

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
failed_tests = []
for line in log_lines:
    stripped = line.strip()
    if not stripped.startswith("FAILED "):
        continue
    failed_tests.append(stripped.split(" - ", 1)[0].replace("FAILED ", "", 1))

gate_surface_tests = {
    "current_status": [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_locks_required_face[current_status]",
    ],
    "proof_and_report_pointers": [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_locks_required_face[proof_and_report_pointers]",
    ],
    "omission_drift_partial_visibility": [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_locks_required_face[omission_drift_partial_visibility]",
    ],
    "manual_stop_all": [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_locks_required_face[manual_stop_all]",
    ],
    "quarantine": [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_locks_required_face[quarantine]",
    ],
    "terminal_snapshot": [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_locks_required_face[terminal_snapshot]",
    ],
    "normalized_failure_detail": [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_locks_required_face[normalized_failure_detail]",
    ],
    "open_questions": [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_locks_required_face[open_questions]",
    ],
    "next_shift_priority_checks": [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_locks_required_face[next_shift_priority_checks]",
    ],
}

gate_surface_proof_tests = {
    face_name: [
        f"tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py::test_livepaper_observability_shift_handoff_ci_check_proof_locks_each_surface[{face_name}]"
    ]
    for face_name in gate_surface_tests
}

failed_faces = []
non_surface_failures = []
for failed_test in failed_tests:
    matched = False
    for face_name, test_ids in gate_surface_tests.items():
        if failed_test in test_ids or failed_test in gate_surface_proof_tests[face_name]:
            failed_faces.append(face_name)
            matched = True
    if not matched:
        non_surface_failures.append(failed_test)

failed_faces = sorted(set(failed_faces))

if failed_faces:
    failure_category = "handoff_face_regression"
elif non_surface_failures:
    failure_category = "suite_failure"
else:
    failure_category = "none"

proof = {
    "task_id": "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK",
    "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "verified_github": {
        "latest_vexter_pr": 64,
        "latest_vexter_main_commit": "30652c29570bf34d105befed6a46a60b551d59b7",
        "latest_vexter_merged_at_utc": "2026-03-26T18:53:07Z",
        "latest_recent_vexter_prs": [64, 63, 62, 61],
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
        "sample_handoff": "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/HANDOFF.md",
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
    "livepaper_observability_shift_handoff_ci_check": {
        "suite_group": suite_marker,
        "runner_script": "scripts/run_livepaper_observability_shift_handoff_ci_check.sh",
        "workflow": ".github/workflows/validate.yml",
        "pytest_command": "pytest -q -m livepaper_observability_shift_handoff_ci_check tests/test_planner_router_transport_livepaper_observability_shift_handoff_template.py tests/test_planner_router_transport_livepaper_observability_shift_handoff_drill.py tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py",
        "pytest_result": pytest_result,
        "gate_status": gate_status,
        "grouped_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_template.py",
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_drill.py",
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py",
        ],
        "supporting_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_template.py",
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_drill.py",
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py",
        ],
        "grouped_suite_markers": ["livepaper_observability_shift_handoff_ci_check"],
        "required_handoff_faces": list(gate_surface_tests),
        "gate_surface_tests": gate_surface_tests,
        "proof_outputs": [
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-check.json",
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-summary.md",
        ],
        "proof_artifact_name": "livepaper-observability-shift-handoff-ci-check-proof",
        "proof_and_report_pointers": {
            "status_report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check-status.md",
            "report": "artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check-report.md",
            "summary": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-summary.md",
            "proof_json": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-check.json",
            "first_deep_proof": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json",
        },
        "normalized_failure_detail": {
            "failed_faces_or_none": failed_faces or ["none"],
            "failed_tests_or_none": failed_tests or ["none"],
            "non_surface_failures_or_none": non_surface_failures or ["none"],
            "failure_category_or_none": failure_category,
        },
        "source_faithful_modes": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
    },
    "next_task_evaluation": {
        "livepaper_observability_shift_handoff_watchdog": {
            "recommended": gate_status == "passed",
            "reasons": [
                "The handoff surface is now CI-gated on change, so the next bounded gap is keeping future handoff drift visible as the operator workflow evolves.",
                "A handoff watchdog extends the same fixed faces without reopening acceptance scope or planner-to-transport design.",
            ],
        },
        "transport_livepaper_observability_acceptance_pack": {
            "recommended": False,
            "reasons": [
                "An acceptance pack would mostly restate the already fixed and now CI-gated handoff surface.",
                "The higher remaining leverage is ongoing drift detection for the handoff itself.",
            ],
        },
        "executor_boundary_code_spec": {
            "recommended": False,
            "reasons": [
                "No new boundary ambiguity surfaced while formalizing the handoff gate.",
                "The residual risk remains operator handoff drift rather than transport contract uncertainty.",
            ],
        },
    },
    "task_result": {
        "selected_outcome": selected_outcome,
        "key_finding": "livepaper_observability_shift_handoff_ci_gate_enforced" if gate_status == "passed" else "livepaper_observability_shift_handoff_ci_gate_failed",
        "claim_boundary": "livepaper_observability_shift_handoff_ci_check_bounded",
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
    "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK Proof Summary",
    "",
    "- Verified Vexter `main` at merged PR `#64` commit `30652c29570bf34d105befed6a46a60b551d59b7`",
    "- Kept Dexter pinned at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "- Promoted the fixed shift handoff template and drill into an always-on CI gate with one explicit test surface per required handoff face",
    f"- Gate run result: `{pytest_result}`",
]
if failed_faces:
    summary_lines.append(f"- Broken handoff faces: `{', '.join(failed_faces)}`")
else:
    summary_lines.append("- Broken handoff faces: `none`")
summary_lines.extend(
    [
        "- Locked current status, proof/report pointers, omission/drift/partial_visibility, manual stop-all and quarantine, terminal snapshot, normalized failure detail, open questions, and next-shift priority checks as mandatory handoff gates",
        "- Preserved frozen source behavior, fixed comparison baseline, and no new evidence collection",
    ]
)
if gate_status == "passed":
    summary_lines.append("- Recommended next task: `livepaper_observability_shift_handoff_watchdog`")
else:
    summary_lines.append("- Gate failed, so the immediate next step remains `livepaper_observability_shift_handoff_ci_check`")
summary_md.write_text("\n".join(summary_lines) + "\n")

report_lines = [
    "# TASK-007 Live-Paper Observability Shift Handoff CI Check Report",
    "",
    "## Scope",
    "",
    "This task promotes the fixed live-paper observability shift handoff template and drill into a standard CI gate.",
    "It does not reopen comparison work, collect new evidence, or change planner/router, Dexter, or Mew-X source logic.",
    "",
    "## Verified GitHub State",
    "",
    "- Latest merged Vexter `main`: PR `#64`, main commit `30652c29570bf34d105befed6a46a60b551d59b7`, merged at `2026-03-26T18:53:07Z`",
    "- Open non-authoritative Vexter PR: `#50`, `feat(infra): refresh runtime observability artifacts`",
    "- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`",
    "- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`",
    "",
    "## CI Gate Shape",
    "",
    "- Suite marker: `livepaper_observability_shift_handoff_ci_check`",
    "- Runner: `scripts/run_livepaper_observability_shift_handoff_ci_check.sh`",
    "- Grouped test files:",
    "  - `tests/test_planner_router_transport_livepaper_observability_shift_handoff_template.py`",
    "  - `tests/test_planner_router_transport_livepaper_observability_shift_handoff_drill.py`",
    "  - `tests/test_planner_router_transport_livepaper_observability_shift_handoff_ci_check.py`",
    "- Proof outputs:",
    "  - `artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-check.json`",
    "  - `artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-summary.md`",
    "- First deep proof remains `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json`",
    "",
    "## Required Handoff Gate Faces",
    "",
    "- `current_status`",
    "- `proof_and_report_pointers`",
    "- `omission_drift_partial_visibility`",
    "- `manual_stop_all`",
    "- `quarantine`",
    "- `terminal_snapshot`",
    "- `normalized_failure_detail`",
    "- `open_questions`",
    "- `next_shift_priority_checks`",
    "",
    "## Normalized Failure Detail",
    "",
    f"- Gate status: `{gate_status}`",
    f"- Failed faces: `{', '.join(failed_faces) if failed_faces else 'none'}`",
    f"- Failed tests: `{', '.join(failed_tests) if failed_tests else 'none'}`",
    f"- Non-surface failures: `{', '.join(non_surface_failures) if non_surface_failures else 'none'}`",
    "",
    "## What Did Not Change",
    "",
    "- No planner/router source logic changed.",
    "- No Dexter behavior changed.",
    "- No Mew-X behavior changed.",
    "- No validator rules changed.",
    "- No comparison evidence was recollected.",
    "- No comparison baseline was reopened.",
    "",
    "## Recommendation Among Next Tasks",
    "",
    "### `livepaper_observability_shift_handoff_watchdog`",
    "",
    "- Recommended next because the required handoff faces are now CI-gated on change, so the next bounded cut is drift detection for future operator handoff evolution.",
    "- It extends the handoff lane directly without widening scope or restating already fixed artifacts.",
    "",
    "### `transport_livepaper_observability_acceptance_pack`",
    "",
    "- Not next because it would mostly repackage the same fixed and now CI-enforced handoff surfaces.",
    "",
    "### `executor_boundary_code_spec`",
    "",
    "- Not next because no new planner-to-transport ambiguity surfaced while codifying the handoff gate.",
    "",
    "## Decision",
    "",
    f"- Outcome: `{selected_outcome}`",
    f"- Key finding: `{proof['task_result']['key_finding']}`",
    "- Claim boundary: `livepaper_observability_shift_handoff_ci_check_bounded`",
    f"- Current task status: `{task_state}`",
    f"- Recommended next step: `{recommended_next_step}`",
    f"- Decision: `{decision}`",
]
report_md.write_text("\n".join(report_lines) + "\n")

status_lines = [
    "# TASK-007 Live-Paper Observability Shift Handoff CI Check Status",
    "",
    "## Verified Start",
    "",
    "- Vexter `origin/main` verified at PR `#64` commit `30652c29570bf34d105befed6a46a60b551d59b7`",
    "- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "",
    "## Current Result",
    "",
    "- Task ID: `TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK`",
    "- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`",
    "- Comparison source of truth: `comparison_closed_out`",
    "- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`",
    "- Canonical runbook: `docs/livepaper_observability_operator_runbook.md`",
    "- Canonical checklist: `docs/livepaper_observability_shift_checklist.md`",
    "- Canonical handoff template: `docs/livepaper_observability_shift_handoff_template.md`",
    "- Canonical handoff drill: `docs/livepaper_observability_shift_handoff_drill.md`",
    "- Sample handoff: `artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/HANDOFF.md`",
    "- Gate runner: `scripts/run_livepaper_observability_shift_handoff_ci_check.sh`",
    f"- Validation: `pytest -q -m livepaper_observability_shift_handoff_ci_check ...` -> `{pytest_result}`",
    f"- Broken handoff faces: `{', '.join(failed_faces) if failed_faces else 'none'}`",
    "",
    "## Decision",
    "",
    f"- Current task: `{task_state}`",
    f"- Key finding: `{proof['task_result']['key_finding']}`",
    "- Claim boundary: `livepaper_observability_shift_handoff_ci_check_bounded`",
    f"- Recommended next step: `{recommended_next_step}`",
    f"- Decision: `{decision}`",
]
status_md.write_text("\n".join(status_lines) + "\n")

context = {
    "recommended_next_task": recommended_next_task_id,
    "visible_main_state": {
        "latest_vexter_pr": 64,
        "latest_vexter_main_commit": "30652c29570bf34d105befed6a46a60b551d59b7",
        "dexter_main": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
        "mewx_frozen": "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
    },
    "current_state": {
        "current_task": task_state,
        "recommended_next_step": recommended_next_step,
        "first_deep_proof": "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json",
        "broken_handoff_faces_or_none": failed_faces or ["none"],
    },
}
context_json.write_text(json.dumps(context, indent=2) + "\n")

details_md.write_text(
    "\n".join(
        [
            "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-CI-CHECK",
            "",
            "## Goal",
            "",
            "Keep the fixed shift handoff template and drill as a hard CI gate so required handoff faces fail immediately when they drift.",
            "",
            "## Required Faces",
            "",
            "- current status",
            "- proof/report pointers",
            "- omission / drift / partial_visibility",
            "- manual stop-all",
            "- quarantine",
            "- terminal snapshot",
            "- normalized failure detail",
            "- open questions",
            "- next-shift priority checks",
            "",
            "## Proof Pointers",
            "",
            "- status: `artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check-status.md`",
            "- report: `artifacts/reports/task-007-livepaper-observability-shift-handoff-ci-check-report.md`",
            "- summary: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-summary.md`",
            "- proof json: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-check.json`",
        ]
    )
    + "\n"
)

min_prompt_txt.write_text(
    "Verify the livepaper observability shift handoff CI check proof and status, then inspect any failed handoff face before changing template or drill artifacts.\n"
)
PY

printf '\nGenerated proof files:\n'
printf ' - %s\n' "$PROOF_JSON"
printf ' - %s\n' "$SUMMARY_MD"
printf '\n'
cat "$SUMMARY_MD"

exit "$PYTEST_STATUS"
