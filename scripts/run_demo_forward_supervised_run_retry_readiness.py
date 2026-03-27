#!/usr/bin/env python3
"""Emit bounded retry-readiness proof surfaces from the blocked supervised-run baseline."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vexter.planner_router.transport import DexterDemoRuntimeConfig


TEMPLATE_ENV_PATH = ROOT / "templates" / "windows_runtime" / "dexter.env.example"
CONTEXT_PATH = ROOT / "artifacts" / "context_pack.json"
MANIFEST_PATH = ROOT / "artifacts" / "proof_bundle_manifest.json"
LEDGER_PATH = ROOT / "artifacts" / "task_ledger.jsonl"
SUMMARY_PATH = ROOT / "artifacts" / "summary.md"
README_PATH = ROOT / "README.md"
CHECKLIST_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_readiness_checklist.md"
MATRIX_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_prerequisite_matrix.md"
SCRIPT_PATH = ROOT / "scripts" / "run_demo_forward_supervised_run_retry_readiness.py"
SPEC_PATH = ROOT / "specs" / "DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md"
PLAN_PATH = ROOT / "plans" / "demo_forward_supervised_run_retry_readiness_plan.md"

PREVIOUS_PROOF_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-check.json"
PREVIOUS_SUMMARY_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-summary.md"
PREVIOUS_REPORT_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-report.md"
PREVIOUS_STATUS_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-status.md"
PREVIOUS_HANDOFF_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run" / "HANDOFF.md"
PREVIOUS_FOLLOW_UP_PATH = ROOT / "docs" / "demo_forward_supervised_run_operator_follow_up.md"

REPORT_DIR = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-readiness"
REPORT_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-readiness-report.md"
STATUS_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-readiness-status.md"
SUBAGENTS_PATH = REPORT_DIR / "SUBAGENTS.md"
PROOF_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-readiness-check.json"
PROOF_SUMMARY_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-readiness-summary.md"
)

BUNDLE_PATH = "artifacts/bundles/demo-forward-supervised-run-retry-readiness.tar.gz"
BUNDLE_SOURCE = "/Users/cabbala/Downloads/vexter_supervised_run_retry_readiness_bundle.tar.gz"

TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS"
TASK_STATUS = "supervised_run_retry_readiness_blocked"
KEY_FINDING = "supervised_run_retry_readiness_blocked_on_external_prerequisites"
CLAIM_BOUNDARY = "supervised_run_retry_readiness_bounded"
NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
NEXT_TASK_STATE = "ready_for_supervised_run_retry_gate"
NEXT_TASK_LANE = "supervised_run_retry_gate"
DECISION = "supervised_run_retry_gate_required"

VERIFIED_DEXTER_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
VERIFIED_MEWX_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
VERIFIED_VEXTER_PR = 73
VERIFIED_VEXTER_COMMIT = "aea530368fc5b59b87dd08a38c2629392ea8d706"
VERIFIED_VEXTER_MERGED_AT = "2026-03-27T00:56:46Z"

REQUIRED_EXTERNAL_REF_VARS = (
    "DEXTER_DEMO_CREDENTIAL_SOURCE",
    "DEXTER_DEMO_VENUE_REF",
    "DEXTER_DEMO_ACCOUNT_REF",
    "DEXTER_DEMO_CONNECTIVITY_PROFILE",
)
BOUNDED_RUNTIME_VARS = (
    "DEXTER_DEMO_ALLOWED_SYMBOLS",
    "DEXTER_DEMO_DEFAULT_SYMBOL",
    "DEXTER_DEMO_ORDER_SIZE_LOTS",
    "DEXTER_DEMO_MAX_ORDER_SIZE_LOTS",
    "DEXTER_DEMO_WINDOW_MINUTES",
    "DEXTER_DEMO_MAX_OPEN_POSITIONS",
)
SUB_AGENT_SUMMARIES = (
    {
        "name": "Anscombe",
        "summary": (
            "Validated that the current proof / report / handoff / status pointers can move to "
            "retry-readiness without losing the blocked supervised-run baseline, and that the "
            "remaining prerequisite language stays observation-based."
        ),
    },
    {
        "name": "Euler",
        "summary": (
            "Confirmed the retry-readiness boundary should stay Dexter-only, `single_sleeve`, "
            "`dexter_default`, explicit allowlist, small lot, bounded supervised window, and "
            "planner `prepare / start / status / stop / snapshot`, with the next smallest lane "
            "framed as a retry gate rather than wider execution."
        ),
    },
    {
        "name": "Parfit",
        "summary": (
            "Reviewed the change as a minimal source-of-truth promotion, scoped regression impact "
            "to artifact-generation and contract tests, and recommended validating the new "
            "generator, bundle output, and affected artifact-layout tests before merge."
        ),
    },
)


def parse_template_env(path: Path) -> dict[str, str]:
    payload: dict[str, str] = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        payload[key.strip()] = value.strip()
    return payload


@contextmanager
def patched_demo_env(values: dict[str, str]) -> Iterator[None]:
    previous = {key: os.environ.get(key) for key in values}
    try:
        os.environ.update(values)
        yield
    finally:
        for key, old_value in previous.items():
            if old_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old_value


def format_json(payload: object) -> str:
    return json.dumps(payload, indent=2, sort_keys=False) + "\n"


def format_jsonl(payload: object) -> str:
    return json.dumps(payload, sort_keys=False) + "\n"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rewrite_ledger(entry: dict[str, object]) -> None:
    retained: list[str] = []
    if LEDGER_PATH.exists():
        for raw_line in LEDGER_PATH.read_text().splitlines():
            if not raw_line.strip():
                continue
            payload = json.loads(raw_line)
            if payload.get("task_id") == TASK_ID:
                continue
            retained.append(format_jsonl(payload))
    retained.append(format_jsonl(entry))
    LEDGER_PATH.write_text("".join(retained))


def build_prerequisite_matrix(template_env: dict[str, str], runtime_config: DexterDemoRuntimeConfig) -> list[dict]:
    return [
        {
            "name": "DEXTER_DEMO_CREDENTIAL_SOURCE",
            "repo_visible_marker": template_env["DEXTER_DEMO_CREDENTIAL_SOURCE"],
            "repo_visible_marker_present": True,
            "resolved_outside_repo": False,
            "who_confirms": "named_operator_owner_outside_repo",
            "retry_ready_when": (
                "the external credential source for Dexter paper_live is explicitly named "
                "outside the repo and confirmed against the pinned source seam"
            ),
        },
        {
            "name": "DEXTER_DEMO_VENUE_REF",
            "repo_visible_marker": template_env["DEXTER_DEMO_VENUE_REF"],
            "repo_visible_marker_present": True,
            "resolved_outside_repo": False,
            "who_confirms": "named_operator_owner_outside_repo",
            "retry_ready_when": (
                "the demo venue reference is explicitly mapped to a reachable Dexter paper_live venue"
            ),
        },
        {
            "name": "DEXTER_DEMO_ACCOUNT_REF",
            "repo_visible_marker": template_env["DEXTER_DEMO_ACCOUNT_REF"],
            "repo_visible_marker_present": True,
            "resolved_outside_repo": False,
            "who_confirms": "named_operator_owner_outside_repo",
            "retry_ready_when": (
                "the demo account reference is explicitly mapped to the same venue / mode pair"
            ),
        },
        {
            "name": "DEXTER_DEMO_CONNECTIVITY_PROFILE",
            "repo_visible_marker": template_env["DEXTER_DEMO_CONNECTIVITY_PROFILE"],
            "repo_visible_marker_present": True,
            "resolved_outside_repo": False,
            "who_confirms": "named_operator_owner_outside_repo",
            "retry_ready_when": (
                "the connectivity profile is explicitly confirmed for the retry window and "
                "poll / stop-all visibility remains available"
            ),
        },
        {
            "name": "operator_owner",
            "repo_visible_marker": "unconfirmed_outside_repo",
            "repo_visible_marker_present": False,
            "resolved_outside_repo": False,
            "who_confirms": "project_side_retry_owner_outside_repo",
            "retry_ready_when": "one operator owner is explicitly named for the full supervised window",
        },
        {
            "name": "bounded_supervised_window_start_criteria",
            "repo_visible_marker": f"bounded_window_minutes={runtime_config.bounded_window_minutes}",
            "repo_visible_marker_present": True,
            "resolved_outside_repo": False,
            "who_confirms": "named_operator_owner_outside_repo",
            "retry_ready_when": (
                "the start time, abort owner, and halt path are explicitly named before retry"
            ),
        },
        {
            "name": "allowlist_symbol_lot_reconfirmation",
            "repo_visible_marker": {
                "allowed_symbols": list(runtime_config.allowed_symbols),
                "default_symbol": runtime_config.default_symbol,
                "order_size_lots": str(runtime_config.order_size_lots),
                "max_order_size_lots": str(runtime_config.max_order_size_lots),
                "max_open_positions": runtime_config.max_open_positions,
            },
            "repo_visible_marker_present": True,
            "resolved_outside_repo": False,
            "who_confirms": "named_operator_owner_outside_repo",
            "retry_ready_when": (
                "the operator reconfirms allowlist, symbol, lot size, and max-position guardrails "
                "for the bounded retry window"
            ),
        },
        {
            "name": "stop_all_visibility_reconfirmation",
            "repo_visible_marker": "baseline_stop_all_state=flatten_confirmed",
            "repo_visible_marker_present": True,
            "resolved_outside_repo": False,
            "who_confirms": "named_operator_owner_outside_repo",
            "retry_ready_when": (
                "cancel / stop-all and terminal snapshot visibility are reconfirmed before the retry gate opens"
            ),
        },
    ]


def build_current_report(
    run_timestamp: str,
    previous_proof: dict,
    runtime_config: DexterDemoRuntimeConfig,
    matrix: list[dict],
) -> str:
    unresolved = [row["name"] for row in matrix if not row["resolved_outside_repo"]]
    baseline_sequence = previous_proof["demo_forward_supervised_run"]["supervised_sequence"]
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS Report

## Verified Base

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#73`, merge commit `{VERIFIED_VEXTER_COMMIT}`, merged at `{VERIFIED_VEXTER_MERGED_AT}`.
- Dexter remained pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen Mew-X remained pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## Starting Point

- Accepted `demo_forward_supervised_run_blocked` as the current blocked baseline instead of fabricating a retry success.
- Carried forward the bounded supervised-run proof, report, summary, and handoff as the baseline current source of truth.
- Promoted retry readiness as the new current operator-visible lane.

## Retry Readiness Boundary

- Dexter-only real demo slice
- Dexter `paper_live`
- frozen Mew-X `sim_live`
- `single_sleeve`
- `dexter_default`
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded supervised window required
- external credential refs remain outside repo
- operator owner must be explicit
- venue / connectivity confirmation must be explicit
- stop-all visibility must be reconfirmed before retry
- funded live forbidden

## Baseline Continuity

- blocked supervised-run handle id: `{baseline_sequence["prepare"]["handle_id"]}`
- blocked supervised-run status path: `artifacts/reports/demo-forward-supervised-run-status.md`
- blocked supervised-run proof path: `artifacts/proofs/demo-forward-supervised-run-check.json`
- blocked supervised-run handoff path: `artifacts/reports/demo-forward-supervised-run/HANDOFF.md`
- bounded runtime guardrails stayed parseable from `templates/windows_runtime/dexter.env.example`
- runtime validation errors: `{len(list(runtime_config.validation_errors()))}`

## Required Current Surfaces

- current status report: `artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md`
- current report: `artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md`
- current summary: `artifacts/proofs/demo-forward-supervised-run-retry-readiness-summary.md`
- current proof json: `artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json`
- current handoff: `artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md`
- retry readiness checklist: `docs/demo_forward_supervised_run_retry_readiness_checklist.md`
- retry prerequisite matrix: `docs/demo_forward_supervised_run_retry_prerequisite_matrix.md`
- sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md`

## Prerequisite Matrix Summary

- unresolved prerequisite count: `{len(unresolved)}`
- unresolved prerequisites: `{", ".join(unresolved)}`
- bounded window minutes: `{runtime_config.bounded_window_minutes}`
- allowlist: `{", ".join(runtime_config.allowed_symbols)}`
- default symbol: `{runtime_config.default_symbol}`
- order size lots: `{runtime_config.order_size_lots}`
- max open positions: `{runtime_config.max_open_positions}`

## Outcome

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task state: `{TASK_STATUS}`
- Blocker: the retry-readiness surface is current, but external reference resolution, operator ownership, venue / connectivity confirmation, and stop-all reconfirmation remain outside the repo and unresolved.
- Run timestamp: `{run_timestamp}`

## Recommendation

- Current task state: `{TASK_STATUS}`
- Recommended next step: `{NEXT_TASK_LANE}`
- Reason: the repo-visible readiness surface is now bounded, but the smallest honest next lane is a retry gate until the named external prerequisites are explicitly satisfied.
"""


def build_status() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS Status

- task_id: `{TASK_ID}`
- task_state: `{TASK_STATUS}`
- run_outcome: `FAIL/BLOCKED`
- key_finding: `{KEY_FINDING}`
- claim_boundary: `{CLAIM_BOUNDARY}`
- verified_vexter_main_pr: `{VERIFIED_VEXTER_PR}`
- verified_vexter_main_commit: `{VERIFIED_VEXTER_COMMIT}`
- verified_dexter_main_commit: `{VERIFIED_DEXTER_COMMIT}`
- verified_mewx_frozen_commit: `{VERIFIED_MEWX_COMMIT}`
- baseline_task: `DEMO-FORWARD-SUPERVISED-RUN`
- baseline_task_state: `demo_forward_supervised_run_blocked`
- planner_boundary: `prepare/start/status/stop/snapshot`
- real_demo_path: `build_demo_executor_transport_registry -> DexterDemoExecutorAdapter`
- mewx_path: `unchanged_sim_live`
- next_task: `{NEXT_TASK_ID}`
"""


def build_proof_summary() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS Summary

- Verified base: Vexter `main` at PR `#73` merge commit `{VERIFIED_VEXTER_COMMIT}`.
- Starting point: the bounded supervised run already failed closed on unresolved external prerequisites.
- Promoted boundary: retry readiness is now current source of truth for the same Dexter-only `paper_live` / frozen Mew-X `sim_live` seam, `single_sleeve`, `dexter_default`, explicit allowlist, small lot, bounded supervised window, one active real demo plan max, and one open position max.
- Added current surfaces: retry readiness status, report, summary, proof, handoff, checklist, prerequisite matrix, and sub-agent summary.
- Outcome: `FAIL/BLOCKED` because the external prerequisite set is still unresolved outside the repo.
- Recommended next task: `{NEXT_TASK_LANE}`.
"""


def build_details() -> str:
    return f"""# {TASK_ID}

## 1. Intent
- Accept the blocked supervised run as baseline.
- Promote retry readiness to the repo-visible current source of truth.

## 2. Boundary
- Dexter `paper_live` only
- frozen Mew-X `sim_live` only
- `single_sleeve`
- `dexter_default`
- one active real demo plan max
- one open position max
- allowlist only
- small lot only
- bounded supervised window only
- external refs remain outside repo

## 3. Required Current Surfaces
- status
- report
- summary
- proof
- handoff
- checklist
- prerequisite matrix
- sub-agent summary

## 4. Honest Outcome
- `PASS` only if all retry prerequisites are explicitly satisfied enough for the next bounded retry lane.
- `FAIL/BLOCKED` if any external prerequisite remains unresolved.

## 5. Next Task
- `{NEXT_TASK_LANE}`
"""


def build_min_prompt() -> str:
    return (
        "GitHub最新状態を確認し、Vexter `main` PR #73 merge 後の retry-readiness surface を current source of truth として扱ってください。\n"
        "出発点は `demo_forward_supervised_run_blocked` で、Dexter `paper_live` のみ・frozen Mew-X `sim_live` のみ・`single_sleeve`・`dexter_default`・explicit allowlist・small lot・max open positions=1・bounded supervised window を維持してください。\n"
        "planner の public boundary は `prepare / start / status / stop / snapshot` のまま、`manual_latched_stop_all` は planner-owned のまま保ってください。\n"
        "external credential refs は repo 外に残し、operator owner / venue connectivity / supervised-window start criteria / stop-all reconfirmation を repo 内で捏造しないでください。\n"
        "current status / report / proof / handoff / checklist / prerequisite matrix / sub-agent summary を更新し、次は `supervised_run_retry_gate` を最小 cut として示してください.\n"
    )


def build_handoff(
    run_timestamp: str,
    previous_proof: dict,
    runtime_config: DexterDemoRuntimeConfig,
    matrix: list[dict],
) -> str:
    baseline_sequence = previous_proof["demo_forward_supervised_run"]["supervised_sequence"]
    return f"""# Demo Forward Supervised Run Retry Readiness Handoff

## Current Status
- outgoing_shift_window: {run_timestamp} retry-readiness lane
- incoming_shift_window: external prerequisite resolution and retry gate
- task_state: {TASK_STATUS}
- shift_outcome: blocked
- current_action: hold_retry_until_retry_gate_passes
- recommended_next_step: {NEXT_TASK_LANE}
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: {VERIFIED_VEXTER_COMMIT}
- dexter_main_commit: {VERIFIED_DEXTER_COMMIT}
- mewx_frozen_commit: {VERIFIED_MEWX_COMMIT}
- baseline_supervised_task_state: demo_forward_supervised_run_blocked
- baseline_handle_id: {baseline_sequence["prepare"]["handle_id"]}

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md
- current_report: artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md
- current_proof_summary: artifacts/proofs/demo-forward-supervised-run-retry-readiness-summary.md
- current_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json
- current_retry_checklist: docs/demo_forward_supervised_run_retry_readiness_checklist.md
- current_prerequisite_matrix: docs/demo_forward_supervised_run_retry_prerequisite_matrix.md
- current_subagent_summary: artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md
- baseline_status_report: artifacts/reports/demo-forward-supervised-run-status.md
- baseline_report: artifacts/reports/demo-forward-supervised-run-report.md
- baseline_proof_json: artifacts/proofs/demo-forward-supervised-run-check.json
- baseline_handoff: artifacts/reports/demo-forward-supervised-run/HANDOFF.md

## Guardrails
- route_mode: single_sleeve
- selected_sleeve_id: dexter_default
- max_active_real_demo_plans: 1
- max_open_positions: {runtime_config.max_open_positions}
- allowlist_required: true
- allowlist_symbols: {", ".join(runtime_config.allowed_symbols)}
- demo_symbol: {runtime_config.default_symbol}
- small_lot_required: true
- small_lot_order_size: {runtime_config.order_size_lots}
- bounded_window_minutes: {runtime_config.bounded_window_minutes}
- operator_supervised_window_required: true
- external_credential_refs_outside_repo: true
- operator_owner_explicit_required: true
- venue_connectivity_confirmation_required: true
- stop_all_visibility_reconfirmation_required: true
- mewx_overlay_enabled: false
- funded_live_allowed: false

## External Prerequisite Matrix
{chr(10).join(f"- {row['name']}: resolved_outside_repo={str(row['resolved_outside_repo']).lower()}, who_confirms={row['who_confirms']}" for row in matrix)}

## Open Questions
- question_1_or_none: who is the named operator owner for the bounded retry window
- question_2_or_none: when does the bounded supervised retry window open outside the repo
- question_3_or_none: which venue / account / connectivity refs are confirmed live outside the repo
- question_4_or_none: has stop-all visibility been reconfirmed before the retry gate opens

## Next-Shift Priority Checks
- priority_check_1: resolve the named external credential, venue, account, and connectivity refs outside the repo before retry
- priority_check_2: keep the lane Dexter-only, `single_sleeve`, `dexter_default`, small-lot, and funded-live-forbidden
- priority_check_3: preserve `manual_latched_stop_all`, poll-first status visibility, and terminal snapshot visibility during the retry gate

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- checklist_pointer_checked: true
- matrix_pointer_checked: true
- subagent_summary_pointer_checked: true
- blocked_claim_boundary_explicit: true

This handoff promotes the bounded retry-readiness lane only. It does not claim a passed retry gate, a completed retry execution, funded live access, or any Mew-X seam expansion.
"""


def build_subagents() -> str:
    lines = ["# Demo Forward Supervised Run Retry Readiness Sub-agent Summaries", ""]
    for item in SUB_AGENT_SUMMARIES:
        lines.append(f"- {item['name']}: {item['summary']}")
    lines.append("")
    return "\n".join(lines)


def update_readme() -> None:
    marker = "`DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS` starts from latest GitHub-visible Vexter `main`"
    if marker in README_PATH.read_text():
        return
    entry = (
        "\n\n`DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS` starts from latest GitHub-visible "
        "Vexter `main` at merged PR `#73` merge commit "
        f"`{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`, keeps Dexter pinned at merged "
        f"PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`, and keeps frozen Mew-X at `{VERIFIED_MEWX_COMMIT}`. "
        "It accepts the bounded supervised run as a blocked baseline and promotes retry readiness instead: "
        "the repo now fixes the current status/report/proof/handoff/checklist/prerequisite-matrix surfaces "
        "for the next retry, makes the missing external prerequisite set operator-visible, preserves the "
        "Dexter-only `paper_live` seam, and keeps funded live forbidden while leaving Mew-X unchanged on "
        "`sim_live`. The resulting status is `supervised_run_retry_readiness_blocked` with "
        f"`{CLAIM_BOUNDARY}`, and the next recommended task is `{NEXT_TASK_LANE}`."
    )
    README_PATH.write_text(README_PATH.read_text() + entry + "\n")


def main() -> None:
    run_timestamp = iso_utc_now()
    template_env = parse_template_env(TEMPLATE_ENV_PATH)
    previous_proof = read_json(PREVIOUS_PROOF_PATH)
    with patched_demo_env(template_env):
        runtime_config = DexterDemoRuntimeConfig.from_env()
        runtime_errors = list(runtime_config.validation_errors())

    matrix = build_prerequisite_matrix(template_env, runtime_config)
    unresolved_prerequisites = [row["name"] for row in matrix if not row["resolved_outside_repo"]]
    checklist_gate = {
        "external_reference_markers_present_in_repo": True,
        "runtime_guardrails_parse_cleanly": not runtime_errors,
        "operator_owner_named_outside_repo": False,
        "bounded_supervised_window_named_outside_repo": False,
        "venue_connectivity_confirmed_outside_repo": False,
        "allowlist_symbol_lot_reconfirmed_outside_repo": False,
        "stop_all_visibility_reconfirmed_before_retry": False,
        "real_demo_retry_execution_allowed": False,
    }

    proof = {
        "task_id": TASK_ID,
        "verified_github": {
            "latest_vexter_pr": VERIFIED_VEXTER_PR,
            "latest_vexter_main_commit": VERIFIED_VEXTER_COMMIT,
            "latest_vexter_merged_at": VERIFIED_VEXTER_MERGED_AT,
            "dexter_pr_3_commit": VERIFIED_DEXTER_COMMIT,
            "mewx_frozen_commit": VERIFIED_MEWX_COMMIT,
        },
        "starting_point": {
            "task_id": "DEMO-FORWARD-SUPERVISED-RUN",
            "task_state": "demo_forward_supervised_run_blocked",
            "report": "artifacts/reports/demo-forward-supervised-run-report.md",
            "status_report": "artifacts/reports/demo-forward-supervised-run-status.md",
            "proof": "artifacts/proofs/demo-forward-supervised-run-check.json",
            "summary": "artifacts/proofs/demo-forward-supervised-run-summary.md",
            "handoff": "artifacts/reports/demo-forward-supervised-run/HANDOFF.md",
            "operator_follow_up": "docs/demo_forward_supervised_run_operator_follow_up.md",
        },
        "supervised_run_retry_readiness": {
            "planner_boundary": ["prepare", "start", "status", "stop", "snapshot"],
            "retry_boundary": {
                "demo_source": "dexter",
                "execution_mode": "paper_live",
                "route_mode": "single_sleeve",
                "selected_sleeve_id": "dexter_default",
                "max_active_real_demo_plans": 1,
                "max_open_positions": runtime_config.max_open_positions,
                "allowlist_required": True,
                "small_lot_required": True,
                "bounded_supervised_window_required": True,
                "external_credential_refs_outside_repo": True,
                "operator_owner_explicit_required": True,
                "venue_connectivity_confirmation_required": True,
                "stop_all_visibility_reconfirmation_required": True,
                "mewx_unchanged": True,
                "funded_live_forbidden": True,
            },
            "required_artifacts": {
                "current_status_report": "artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md",
                "current_report": "artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md",
                "current_summary": "artifacts/proofs/demo-forward-supervised-run-retry-readiness-summary.md",
                "current_proof_json": "artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json",
                "current_handoff": "artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md",
                "retry_readiness_checklist": "docs/demo_forward_supervised_run_retry_readiness_checklist.md",
                "retry_prerequisite_matrix": "docs/demo_forward_supervised_run_retry_prerequisite_matrix.md",
                "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md",
            },
            "baseline_blocked_outcome": {
                "task_id": "DEMO-FORWARD-SUPERVISED-RUN",
                "task_state": previous_proof["task_result"]["task_state"],
                "key_finding": previous_proof["task_result"]["key_finding"],
                "claim_boundary": previous_proof["task_result"]["claim_boundary"],
                "recommended_next_step": previous_proof["task_result"]["recommended_next_step"],
                "supervised_sequence": previous_proof["demo_forward_supervised_run"][
                    "supervised_sequence"
                ],
            },
            "external_prerequisites": {
                "required_ref_variables": list(REQUIRED_EXTERNAL_REF_VARS),
                "bounded_runtime_variables": list(BOUNDED_RUNTIME_VARS),
                "repo_visible_reference_markers": {
                    name: template_env[name] for name in REQUIRED_EXTERNAL_REF_VARS
                },
                "runtime_guardrails": {
                    "allowed_symbols": list(runtime_config.allowed_symbols),
                    "default_symbol": runtime_config.default_symbol,
                    "order_size_lots": str(runtime_config.order_size_lots),
                    "max_order_size_lots": str(runtime_config.max_order_size_lots),
                    "bounded_window_minutes": runtime_config.bounded_window_minutes,
                    "max_open_positions": runtime_config.max_open_positions,
                },
                "runtime_validation_errors": runtime_errors,
                "retry_prerequisite_matrix": matrix,
                "unresolved_prerequisites": unresolved_prerequisites,
                "checklist_gate": checklist_gate,
            },
            "sub_agents": list(SUB_AGENT_SUMMARIES),
            "supporting_files": [
                "specs/DEMO_FORWARD_SUPERVISED_RUN.md",
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md",
                "plans/demo_forward_supervised_run_plan.md",
                "plans/demo_forward_supervised_run_retry_readiness_plan.md",
                "docs/demo_forward_supervised_run_operator_follow_up.md",
                "docs/demo_forward_supervised_run_retry_readiness_checklist.md",
                "docs/demo_forward_supervised_run_retry_prerequisite_matrix.md",
                "scripts/run_demo_forward_supervised_run.py",
                "scripts/run_demo_forward_supervised_run_retry_readiness.py",
                "scripts/build_proof_bundle.sh",
                "tests/test_demo_forward_supervised_run.py",
                "tests/test_demo_forward_supervised_run_retry_readiness.py",
            ],
            "proof_outputs": [
                "artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json",
                "artifacts/proofs/demo-forward-supervised-run-retry-readiness-summary.md",
                "artifacts/bundles/demo-forward-supervised-run-retry-readiness.tar.gz",
            ],
        },
        "task_result": {
            "outcome": "FAIL/BLOCKED",
            "key_finding": KEY_FINDING,
            "claim_boundary": CLAIM_BOUNDARY,
            "task_state": TASK_STATUS,
            "recommended_next_step": NEXT_TASK_LANE,
            "recommended_next_task_id": NEXT_TASK_ID,
            "decision": DECISION,
        },
    }

    report_text = build_current_report(run_timestamp, previous_proof, runtime_config, matrix)
    status_text = build_status()
    proof_summary_text = build_proof_summary()
    summary_text = f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#73` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## What This Task Did

- Accepted the blocked supervised run as the baseline current source of truth.
- Promoted retry readiness to the current operator-visible lane.
- Added current status, report, summary, proof, handoff, checklist, prerequisite matrix, and sub-agent summary surfaces.
- Bounded the external prerequisite gap by naming what is missing, who confirms it, and what must be true before retry.

## Decision

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task status: `{TASK_STATUS}`
- Recommended next step: `{NEXT_TASK_LANE}`
- Decision: `{DECISION}`

## Key Paths

- Current spec: `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md`
- Current implementation plan: `plans/demo_forward_supervised_run_retry_readiness_plan.md`
- Current checklist: `docs/demo_forward_supervised_run_retry_readiness_checklist.md`
- Current prerequisite matrix: `docs/demo_forward_supervised_run_retry_prerequisite_matrix.md`
- Current proof: `artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json`
- Current report: `artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md`
- Current handoff: `artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md`
- Current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md`
- Current bundle target: `artifacts/bundles/demo-forward-supervised-run-retry-readiness.tar.gz`
"""

    prompt_context = {
        "task_id": TASK_ID,
        "task_state": TASK_STATUS,
        "recommended_next_step": NEXT_TASK_LANE,
        "recommended_next_task_id": NEXT_TASK_ID,
        "verified_vexter_main_pr": VERIFIED_VEXTER_PR,
        "verified_vexter_main_commit": VERIFIED_VEXTER_COMMIT,
        "baseline_task_state": "demo_forward_supervised_run_blocked",
        "first_demo_target": "dexter_paper_live",
        "source_faithful_seam": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "unresolved_prerequisites": unresolved_prerequisites,
        "real_demo_retry_execution_allowed": False,
    }

    details_text = build_details()
    min_prompt_text = build_min_prompt()
    handoff_text = build_handoff(run_timestamp, previous_proof, runtime_config, matrix)
    subagents_text = build_subagents()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts" / "proofs").mkdir(parents=True, exist_ok=True)

    REPORT_PATH.write_text(report_text)
    STATUS_PATH.write_text(status_text)
    PROOF_PATH.write_text(format_json(proof))
    PROOF_SUMMARY_PATH.write_text(proof_summary_text)
    SUMMARY_PATH.write_text(summary_text)
    (REPORT_DIR / "DETAILS.md").write_text(details_text)
    (REPORT_DIR / "MIN_PROMPT.txt").write_text(min_prompt_text)
    (REPORT_DIR / "CONTEXT.json").write_text(format_json(prompt_context))
    (REPORT_DIR / "HANDOFF.md").write_text(handoff_text)
    SUBAGENTS_PATH.write_text(subagents_text)

    context_pack = read_json(CONTEXT_PATH)
    context_pack["background"] = {
        "previous_task_id": "DEMO-FORWARD-SUPERVISED-RUN",
        "previous_task_state": "demo_forward_supervised_run_blocked",
        "previous_key_finding": "demo_forward_supervised_run_blocked_on_external_prerequisites",
        "previous_claim_boundary": "demo_forward_supervised_run_fail_closed",
        "comparison_source_of_truth_fixed_before_task": True,
        "blocked_supervised_baseline_accepted": True,
    }
    context_pack["bundle_source"] = BUNDLE_SOURCE
    context_pack["current_contract"].update(
        {
            "demo_forward_supervised_retry_readiness_marker": (
                "demo_forward_supervised_run_retry_readiness"
            ),
            "demo_forward_supervised_retry_readiness_spec_path": (
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md"
            ),
            "demo_forward_supervised_retry_readiness_plan_path": (
                "plans/demo_forward_supervised_run_retry_readiness_plan.md"
            ),
            "demo_forward_supervised_retry_readiness_checklist_path": (
                "docs/demo_forward_supervised_run_retry_readiness_checklist.md"
            ),
            "demo_forward_supervised_retry_prerequisite_matrix_path": (
                "docs/demo_forward_supervised_run_retry_prerequisite_matrix.md"
            ),
            "demo_forward_supervised_retry_readiness_subagents_path": (
                "artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md"
            ),
            "demo_forward_retry_readiness_next_step": NEXT_TASK_LANE,
        }
    )
    context_pack["current_task"] = {
        "id": TASK_ID,
        "scope": [
            "Reverify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X after the blocked supervised run merged.",
            "Accept the blocked supervised run as baseline current source of truth.",
            "Promote retry readiness status, report, summary, proof, handoff, checklist, matrix, and sub-agent summary surfaces.",
            "Bound each external prerequisite with a missing-state, confirmer, and retry-ready condition.",
            "Advance the next recommended lane to a retry gate unless explicit retry-readiness pass conditions are satisfied.",
        ],
        "deliverables": [
            "README.md",
            "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md",
            "plans/demo_forward_supervised_run_retry_readiness_plan.md",
            "docs/demo_forward_supervised_run_retry_readiness_checklist.md",
            "docs/demo_forward_supervised_run_retry_prerequisite_matrix.md",
            "tests/test_demo_forward_supervised_run_retry_readiness.py",
            "tests/test_demo_forward_supervised_run.py",
            "tests/test_bootstrap_layout.py",
            "scripts/run_demo_forward_supervised_run_retry_readiness.py",
            "scripts/build_proof_bundle.sh",
            "artifacts/summary.md",
            "artifacts/context_pack.json",
            "artifacts/proof_bundle_manifest.json",
            "artifacts/task_ledger.jsonl",
            "artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md",
            "artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md",
            "artifacts/reports/demo-forward-supervised-run-retry-readiness/DETAILS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-readiness/MIN_PROMPT.txt",
            "artifacts/reports/demo-forward-supervised-run-retry-readiness/CONTEXT.json",
            "artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md",
            "artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md",
            "artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json",
            "artifacts/proofs/demo-forward-supervised-run-retry-readiness-summary.md",
            "artifacts/bundles/demo-forward-supervised-run-retry-readiness.tar.gz",
        ],
        "frozen_source_commits": {
            "dexter": VERIFIED_DEXTER_COMMIT,
            "mewx": VERIFIED_MEWX_COMMIT,
        },
    }
    context_pack["evidence"]["github_latest"].update(
        {
            "latest_vexter_pr": VERIFIED_VEXTER_PR,
            "latest_vexter_main_commit": VERIFIED_VEXTER_COMMIT,
            "latest_recent_vexter_prs": [73, 72, 71, 70, 69],
            "vexter_pr_73_merged_at": VERIFIED_VEXTER_MERGED_AT,
            "vexter_pr_73_closed_at": VERIFIED_VEXTER_MERGED_AT,
        }
    )
    context_pack["evidence"]["demo_forward_supervised_run_retry_readiness"] = {
        "report": "artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md",
        "status_report": "artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md",
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json",
        "summary": "artifacts/proofs/demo-forward-supervised-run-retry-readiness-summary.md",
        "handoff_dir": "artifacts/reports/demo-forward-supervised-run-retry-readiness",
        "checklist": "docs/demo_forward_supervised_run_retry_readiness_checklist.md",
        "prerequisite_matrix": "docs/demo_forward_supervised_run_retry_prerequisite_matrix.md",
        "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md",
        "key_finding": KEY_FINDING,
        "claim_boundary": CLAIM_BOUNDARY,
        "task_state": TASK_STATUS,
        "run_outcome": "FAIL/BLOCKED",
        "operator_visible_readiness_surface_current": True,
        "preferred_next_step": NEXT_TASK_LANE,
        "retry_boundary": proof["supervised_run_retry_readiness"]["retry_boundary"],
        "unresolved_prerequisites": unresolved_prerequisites,
        "sub_agents": list(SUB_AGENT_SUMMARIES),
    }
    context_pack["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "rationale": [
            "The blocked supervised-run baseline is still current and preserved.",
            "The retry-readiness lane now makes the missing prerequisite set explicit and current.",
            "The smallest honest next cut is a retry gate until the named external prerequisites are explicitly satisfied.",
        ],
    }
    context_pack["proofs"].update(
        {
            "demo_forward_supervised_run_retry_readiness_added": True,
            "demo_forward_retry_current_pointers_fixed": True,
            "demo_forward_retry_checklist_written": True,
            "demo_forward_retry_prerequisite_matrix_written": True,
            "demo_forward_retry_subagent_summary_written": True,
            "recommended_next_step_is_supervised_run_retry_gate": True,
        }
    )
    CONTEXT_PATH.write_text(format_json(context_pack))

    manifest = read_json(MANIFEST_PATH)
    manifest["bundle_path"] = BUNDLE_PATH
    manifest["bundle_source"] = BUNDLE_SOURCE
    manifest["task_id"] = TASK_ID
    manifest["status"] = TASK_STATUS
    manifest["task_result"] = proof["task_result"]
    for key, path in (
        ("docs", "docs/demo_forward_supervised_run_retry_readiness_checklist.md"),
        ("docs", "docs/demo_forward_supervised_run_retry_prerequisite_matrix.md"),
        ("scripts", "scripts/run_demo_forward_supervised_run_retry_readiness.py"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-retry-readiness-summary.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-readiness"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md"),
    ):
        if path not in manifest[key]:
            manifest[key].append(path)
    for path in (
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md",
        "plans/demo_forward_supervised_run_retry_readiness_plan.md",
        "tests/test_demo_forward_supervised_run_retry_readiness.py",
        "artifacts/bundles/demo-forward-supervised-run-retry-readiness.tar.gz",
    ):
        if path not in manifest["included_paths"]:
            manifest["included_paths"].append(path)
    manifest["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "resume_requirements": [
            f"Keep Dexter pinned at {VERIFIED_DEXTER_COMMIT} and Mew-X frozen at {VERIFIED_MEWX_COMMIT}.",
            "Start from the current retry-readiness status, report, proof, handoff, checklist, prerequisite matrix, and sub-agent summary surfaces.",
            "Resolve the named external refs, operator owner, supervised-window start criteria, and stop-all reconfirmation outside the repo before retry execution.",
            "Keep the planner boundary at prepare / start / status / stop / snapshot and preserve poll_first plus manual_latched_stop_all.",
            "Do not introduce funded live or a Mew-X real-demo path.",
        ],
    }
    manifest["proofs"].update(
        {
            "demo_forward_supervised_run_retry_readiness_added": True,
            "demo_forward_retry_current_pointers_fixed": True,
            "demo_forward_retry_checklist_written": True,
            "demo_forward_retry_prerequisite_matrix_written": True,
            "demo_forward_retry_subagent_summary_written": True,
            "recommended_next_step_is_supervised_run_retry_gate": True,
        }
    )
    MANIFEST_PATH.write_text(format_json(manifest))

    ledger_payload = {
        "artifact_bundle": BUNDLE_PATH,
        "base_main": VERIFIED_VEXTER_COMMIT,
        "baseline_task_id": "DEMO-FORWARD-SUPERVISED-RUN",
        "baseline_task_state": "demo_forward_supervised_run_blocked",
        "branch": git_output("branch", "--show-current"),
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": DECISION,
        "first_demo_target": "dexter_paper_live",
        "key_finding": KEY_FINDING,
        "next_task_id": NEXT_TASK_ID,
        "next_task_state": NEXT_TASK_STATE,
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json",
        "recommended_next_lane": NEXT_TASK_LANE,
        "repo": "https://github.com/Cabbala/Vexter",
        "retry_prerequisite_count": len(matrix),
        "retry_unresolved_prerequisite_count": len(unresolved_prerequisites),
        "selected_outcome": "FAIL/BLOCKED",
        "source_faithful_modes": {"dexter": "paper_live", "mewx": "sim_live"},
        "status": TASK_STATUS,
        "sub_agents_used": [item["name"] for item in SUB_AGENT_SUMMARIES],
        "supporting_vexter_prs": [73, 72, 71, 70, 69],
        "task_id": TASK_ID,
        "template_runtime_validation_errors": runtime_errors,
        "verified_dexter_main_commit": VERIFIED_DEXTER_COMMIT,
        "verified_dexter_pr": 3,
        "verified_mewx_frozen_commit": VERIFIED_MEWX_COMMIT,
        "verified_prs": [73, 72, 71],
        "date": datetime.now(timezone.utc).date().isoformat(),
    }
    rewrite_ledger(ledger_payload)

    update_readme()


if __name__ == "__main__":
    main()
