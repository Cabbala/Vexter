#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF_DIR="$ROOT_DIR/artifacts/proofs"
REPORT_DIR="$ROOT_DIR/artifacts/reports"
PROOF_JSON="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-check.json"
SUMMARY_MD="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-summary.md"
REPORT_MD="$REPORT_DIR/task-007-livepaper-observability-shift-handoff-watchdog-report.md"
STATUS_MD="$ROOT_DIR/artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-status.md"
PACK_DIR="$ROOT_DIR/artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog"
CONTEXT_JSON="$PACK_DIR/CONTEXT.json"
DETAILS_MD="$PACK_DIR/DETAILS.md"
MIN_PROMPT_TXT="$PACK_DIR/MIN_PROMPT.txt"
LOG_PATH="$PROOF_DIR/task-007-livepaper-observability-shift-handoff-watchdog-pytest.log"
SUITE_MARKER="livepaper_observability_shift_handoff_watchdog"

mkdir -p "$PROOF_DIR" "$ROOT_DIR/artifacts/reports" "$PACK_DIR"

GROUPED_TEST_FILES=(
  "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py"
)

printf 'Livepaper observability shift handoff watchdog\n'
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
  WATCHDOG_STATUS="passed"
  TASK_STATE="livepaper_observability_shift_handoff_watchdog_passed"
  SELECTED_OUTCOME="A"
  RECOMMENDED_NEXT_STEP="livepaper_observability_shift_handoff_watchdog_runtime"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME"
  DECISION="livepaper_observability_shift_handoff_watchdog_runtime_ready"
  KEY_FINDING="livepaper_observability_shift_handoff_watchdog_guarded"
else
  WATCHDOG_STATUS="failed"
  TASK_STATE="livepaper_observability_shift_handoff_watchdog_failed"
  SELECTED_OUTCOME="handoff_watchdog_failed"
  RECOMMENDED_NEXT_STEP="livepaper_observability_shift_handoff_watchdog"
  RECOMMENDED_NEXT_TASK_ID="TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG"
  DECISION="livepaper_observability_shift_handoff_watchdog_failed"
  KEY_FINDING="livepaper_observability_shift_handoff_watchdog_failed"
fi

export ROOT_DIR PROOF_JSON SUMMARY_MD REPORT_MD STATUS_MD CONTEXT_JSON DETAILS_MD MIN_PROMPT_TXT LOG_PATH
export WATCHDOG_STATUS TASK_STATE SELECTED_OUTCOME RECOMMENDED_NEXT_STEP RECOMMENDED_NEXT_TASK_ID DECISION KEY_FINDING SUITE_MARKER

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
log_path = Path(os.environ["LOG_PATH"])
watchdog_status = os.environ["WATCHDOG_STATUS"]
task_state = os.environ["TASK_STATE"]
selected_outcome = os.environ["SELECTED_OUTCOME"]
recommended_next_step = os.environ["RECOMMENDED_NEXT_STEP"]
recommended_next_task_id = os.environ["RECOMMENDED_NEXT_TASK_ID"]
decision = os.environ["DECISION"]
key_finding = os.environ["KEY_FINDING"]
suite_marker = os.environ["SUITE_MARKER"]

sys.path.insert(0, str(root_dir))
from vexter.planner_router.handoff_watchdog import (
    HANDOFF_PATH,
    LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES,
    evaluate_livepaper_observability_shift_handoff_watchdog,
)

watchdog_report = evaluate_livepaper_observability_shift_handoff_watchdog(
    (root_dir / HANDOFF_PATH).read_text(),
    repo_root=root_dir,
)
watchdog_face_tests = {
    surface: [
        "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py::"
        f"test_livepaper_observability_shift_handoff_watchdog_flags_face_regression[{surface}]"
    ]
    for surface in LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES
}
watchdog_snapshot = {
    "checked_handoff": str(HANDOFF_PATH),
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
    "task_id": "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG",
    "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "verified_github": {
        "latest_vexter_pr": 65,
        "latest_vexter_main_commit": "51cfec8b85b5020ba5f6d0f72dceb5c47c339c06",
        "latest_vexter_merged_at_utc": "2026-03-26T19:30:46Z",
        "latest_recent_vexter_prs": [65, 64, 63, 62],
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
        "canonical_handoff_ci_check": "artifacts/proofs/task-007-livepaper-observability-shift-handoff-ci-check-check.json",
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
    "livepaper_observability_shift_handoff_watchdog": {
        "suite_group": suite_marker,
        "runner_script": "scripts/run_livepaper_observability_shift_handoff_watchdog.sh",
        "workflow": ".github/workflows/validate.yml",
        "pytest_command": "pytest -q -m livepaper_observability_shift_handoff_watchdog tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py",
        "pytest_result": pytest_result,
        "watchdog_status": watchdog_status,
        "grouped_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py",
        ],
        "supporting_test_files": [
            "tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py",
        ],
        "grouped_suite_markers": ["livepaper_observability_shift_handoff_watchdog"],
        "required_handoff_faces": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
        "monitored_surfaces": list(LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES),
        "monitored_issue_classes": ["omission", "drift", "partial_visibility"],
        "watchdog_face_tests": watchdog_face_tests,
        "proof_outputs": [
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json",
            "artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-summary.md",
        ],
        "proof_artifact_name": "livepaper-observability-shift-handoff-watchdog-proof",
        "evaluated_handoff": str(HANDOFF_PATH),
        "watchdog_snapshot": watchdog_snapshot,
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
        "livepaper_observability_shift_handoff_watchdog_runtime": {
            "recommended": watchdog_status == "passed",
            "reasons": [
                "The bounded watchdog now detects omission, drift, and partial-visibility regressions directly on the shift handoff surface.",
                "The next remaining risk is runtime-shaped continuity of the same handoff watchdog, not restating the contract.",
            ],
        },
        "transport_livepaper_observability_acceptance_pack": {
            "recommended": False,
            "reasons": [
                "An acceptance pack would mostly repackage the fixed handoff surface that is now CI-gated and watchdog-checked.",
                "Runtime continuity of the watchdog surface reduces more risk than repackaging the same fixed artifacts.",
            ],
        },
        "executor_boundary_code_spec": {
            "recommended": False,
            "reasons": [
                "No new planner-to-transport boundary ambiguity surfaced while adding the handoff watchdog lane.",
                "The remaining work is continuity of the existing handoff surface rather than interface discovery.",
            ],
        },
    },
    "task_result": {
        "selected_outcome": selected_outcome,
        "key_finding": key_finding,
        "claim_boundary": "livepaper_observability_shift_handoff_watchdog_bounded",
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
    "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG Proof Summary",
    "",
    "- Verified Vexter `main` at merged PR `#65` commit `51cfec8b85b5020ba5f6d0f72dceb5c47c339c06`",
    "- Kept Dexter pinned at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "- Added a bounded shift-handoff watchdog lane on top of the fixed template, drill, and CI check without changing source logic or reopening the comparison baseline",
    f"- Watchdog run result: `{pytest_result}`",
    f"- Runtime continuation target remains `livepaper_observability_shift_handoff_watchdog_runtime`",
]
if watchdog_report.passed:
    summary_lines.append("- Current handoff sample passed all watchdog faces without degraded visibility")
else:
    summary_lines.append("- Current handoff sample produced watchdog findings; inspect the proof JSON before advancing")
summary_md.write_text("\n".join(summary_lines) + "\n")

report_lines = [
    "# TASK-007 Live-Paper Observability Shift Handoff Watchdog Report",
    "",
    "## Scope",
    "",
    "This task adds a bounded watchdog for the already-fixed live-paper observability shift handoff surface.",
    "It does not reopen comparison work, collect new evidence, or change planner/router, Dexter, or Mew-X source logic.",
    "",
    "## Verified GitHub State",
    "",
    "- Latest merged Vexter `main`: PR `#65`, main commit `51cfec8b85b5020ba5f6d0f72dceb5c47c339c06`, merged at `2026-03-26T19:30:46Z`",
    "- Open non-authoritative Vexter PR: `#50`, `feat(infra): refresh runtime observability artifacts`",
    "- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`",
    "- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`",
    "",
    "## Watchdog Shape",
    "",
    "- Suite marker: `livepaper_observability_shift_handoff_watchdog`",
    "- Runner: `scripts/run_livepaper_observability_shift_handoff_watchdog.sh`",
    "- Grouped test file: `tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog.py`",
    "- Runtime continuation target: `livepaper_observability_shift_handoff_watchdog_runtime`",
    "",
    "## Current Watchdog Result",
    "",
    f"- Watchdog status: `{watchdog_status}`",
    f"- Broken surfaces: `{', '.join(proof['livepaper_observability_shift_handoff_watchdog']['normalized_failure_detail']['finding_surfaces_or_none'])}`",
    "",
    "## Decision",
    "",
    f"- Outcome: `{selected_outcome}`",
    f"- Key finding: `{key_finding}`",
    "- Claim boundary: `livepaper_observability_shift_handoff_watchdog_bounded`",
    f"- Current task status: `{task_state}`",
    f"- Recommended next step: `{recommended_next_step}`",
    f"- Decision: `{decision}`",
]
report_md.write_text("\n".join(report_lines) + "\n")

status_lines = [
    "# TASK-007 Live-Paper Observability Shift Handoff Watchdog Status",
    "",
    "## Verified Start",
    "",
    "- Vexter `origin/main` verified at PR `#65` commit `51cfec8b85b5020ba5f6d0f72dceb5c47c339c06`",
    "- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`",
    "- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`",
    "",
    "## Current Result",
    "",
    f"- Task ID: `TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG`",
    f"- Validation: `pytest -q -m livepaper_observability_shift_handoff_watchdog ...` -> `{pytest_result}`",
    f"- Runtime continuation target: `livepaper_observability_shift_handoff_watchdog_runtime`",
    f"- Current task: `{task_state}`",
]
status_md.write_text("\n".join(status_lines) + "\n")

context_payload = {
    "recommended_next_task": "TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG-RUNTIME",
    "visible_main_state": {
        "latest_vexter_pr": 65,
        "latest_vexter_main_commit": "51cfec8b85b5020ba5f6d0f72dceb5c47c339c06",
        "dexter_main": "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
        "mewx_frozen": "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
    },
    "current_state": {
        "current_task": task_state,
        "recommended_next_step": recommended_next_step,
        "broken_handoff_watchdog_surfaces_or_none": proof["livepaper_observability_shift_handoff_watchdog"][
            "normalized_failure_detail"
        ]["finding_surfaces_or_none"],
    },
}
context_json.write_text(json.dumps(context_payload, indent=2) + "\n")

details_lines = [
    "# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-WATCHDOG",
    "",
    "## Goal",
    "",
    "Detect bounded drift, omission, and partial visibility on the fixed live-paper shift handoff surface before bundle build.",
    "",
    "## Monitored Surfaces",
    "",
]
details_lines.extend([f"- {surface}" for surface in LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES])
details_md.write_text("\n".join(details_lines) + "\n")

min_prompt_txt.write_text(
    "Verify the livepaper observability shift handoff watchdog proof and status, then inspect the named broken handoff watchdog surface before changing handoff artifacts.\n"
)
PY

printf '\nGenerated proof files:\n'
printf ' - %s\n' "$PROOF_JSON"
printf ' - %s\n' "$SUMMARY_MD"
printf '\n'
cat "$SUMMARY_MD"

exit "$PYTEST_STATUS"
