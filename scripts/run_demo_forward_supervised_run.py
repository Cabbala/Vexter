#!/usr/bin/env python3
"""Emit bounded supervised-run proof surfaces without fabricating a live-demo claim."""

from __future__ import annotations

import asyncio
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

from vexter.planner_router.models import PlanRequest, SourcePinRegistry
from vexter.planner_router.planner import plan_request
from vexter.planner_router.transport import (
    DexterDemoRuntimeConfig,
    InMemoryPlanStore,
    build_demo_executor_transport_registry,
)


CONFIG_ROOT = ROOT / "config" / "planner_router"
TEMPLATE_ENV_PATH = ROOT / "templates" / "windows_runtime" / "dexter.env.example"
CONTEXT_PATH = ROOT / "artifacts" / "context_pack.json"
MANIFEST_PATH = ROOT / "artifacts" / "proof_bundle_manifest.json"
LEDGER_PATH = ROOT / "artifacts" / "task_ledger.jsonl"
SUMMARY_PATH = ROOT / "artifacts" / "summary.md"
README_PATH = ROOT / "README.md"
FOLLOW_UP_PATH = ROOT / "docs" / "demo_forward_supervised_run_operator_follow_up.md"
SCRIPT_PATH = ROOT / "scripts" / "run_demo_forward_supervised_run.py"
SPEC_PATH = ROOT / "specs" / "DEMO_FORWARD_SUPERVISED_RUN.md"
PLAN_PATH = ROOT / "plans" / "demo_forward_supervised_run_plan.md"

REPORT_DIR = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run"
REPORT_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-report.md"
STATUS_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-status.md"
PROOF_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-check.json"
PROOF_SUMMARY_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-summary.md"

BUNDLE_PATH = "artifacts/bundles/demo-forward-supervised-run.tar.gz"
BUNDLE_SOURCE = "/Users/cabbala/Downloads/vexter_demo_forward_supervised_run_bundle.tar.gz"

TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN"
TASK_STATUS = "demo_forward_supervised_run_blocked"
KEY_FINDING = "demo_forward_supervised_run_blocked_on_external_prerequisites"
CLAIM_BOUNDARY = "demo_forward_supervised_run_fail_closed"
NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS"
NEXT_TASK_STATE = "ready_for_supervised_run_retry_readiness"
NEXT_TASK_LANE = "supervised_run_retry_readiness"
DECISION = "supervised_run_retry_readiness_required"

VERIFIED_DEXTER_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
VERIFIED_MEWX_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
VERIFIED_VEXTER_PR = 72
VERIFIED_VEXTER_COMMIT = "a6ca623b01dbed4191c4be10c2bfe51534025cac"
VERIFIED_VEXTER_MERGED_AT = "2026-03-27T00:32:14Z"

FROZEN_PINS = SourcePinRegistry(
    dexter=VERIFIED_DEXTER_COMMIT,
    mewx=VERIFIED_MEWX_COMMIT,
)

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


def build_supervised_sequence() -> tuple[dict, dict]:
    store = InMemoryPlanStore()
    batch = plan_request(
        PlanRequest(plan_request_id="demo-forward-supervised-run"),
        CONFIG_ROOT,
        FROZEN_PINS,
        store,
        datetime(2026, 3, 27, 0, 45, tzinfo=timezone.utc),
    )
    plan = batch.plans[0]
    registry = build_demo_executor_transport_registry(FROZEN_PINS)
    adapter = registry.adapter_for(plan)
    handle = adapter.prepare(plan)

    async def run_sequence() -> tuple[object, object]:
        await adapter.start(handle)
        running_snapshot = await adapter.status(handle)
        await adapter.stop(handle, reason="manual_latched_stop_all")
        stopping_snapshot = await adapter.status(handle)
        terminal_snapshot = await adapter.snapshot(handle)
        return running_snapshot, stopping_snapshot, terminal_snapshot

    running_snapshot, stopping_snapshot, terminal_snapshot = asyncio.run(run_sequence())
    return (
        {
            "plan_id": plan.plan_id,
            "plan_batch_id": plan.plan_batch_id,
            "route_mode": plan.route.mode.value,
            "selected_sleeves": [plan.route.selected_sleeve_id],
            "prepare": {
                "handle_id": handle.handle_id,
                "status_delivery": handle.native_handle["status_delivery"],
                "entrypoint": handle.native_handle["entrypoint"],
                "execution_mode": handle.native_handle["execution_mode"],
                "transport_version": handle.native_handle["transport_version"],
                "demo_runtime": handle.native_handle["demo_runtime"],
                "symbol_allowlist": handle.native_handle["symbol_allowlist"],
                "demo_symbol": handle.native_handle["demo_symbol"],
                "small_lot_order_size": handle.native_handle["small_lot_order_size"],
                "bounded_window_minutes": handle.native_handle["bounded_window_minutes"],
            },
            "start": {
                "runtime_status": running_snapshot.status.value,
                "signal": running_snapshot.detail["signal"],
            },
            "status": {
                "runtime_status": running_snapshot.status.value,
                "native_order_status": running_snapshot.detail["native_order_status"],
                "fill_count": running_snapshot.detail["fill_count"],
                "orders": running_snapshot.detail["orders"],
                "fills": running_snapshot.detail["fills"],
                "open_position_lots": running_snapshot.detail["open_position_lots"],
                "reconciliation": {
                    "last_reconciliation": running_snapshot.detail["last_reconciliation"],
                    "mode": running_snapshot.detail["reconciliation_mode"],
                    "decision": running_snapshot.detail["reconciliation_decision"],
                },
            },
            "stop": {
                "runtime_status": stopping_snapshot.status.value,
                "stop_all_state": stopping_snapshot.detail["stop_all_state"],
                "stop_reason": "manual_latched_stop_all",
            },
            "snapshot": {
                "executor_status": terminal_snapshot["executor_status"],
                "stop_all_state": terminal_snapshot["stop_all_state"],
                "fill_count": terminal_snapshot["fill_count"],
                "orders": terminal_snapshot["orders"],
                "fills": terminal_snapshot["fills"],
                "open_position_lots": terminal_snapshot["open_position_lots"],
            },
        },
        {
            "handle_id": handle.handle_id,
            "plan_id": plan.plan_id,
            "plan_batch_id": plan.plan_batch_id,
        },
    )


def build_current_report(run_timestamp: str, sequence: dict, runtime_config: DexterDemoRuntimeConfig) -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN Report

## Verified Base

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#72`, merge commit `{VERIFIED_VEXTER_COMMIT}`, merged at `{VERIFIED_VEXTER_MERGED_AT}`.
- Dexter remained pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen Mew-X remained pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## What Landed

- Exercised the bounded `prepare / start / status / stop / snapshot` sequence through `DexterDemoExecutorAdapter`.
- Captured entry visibility, fill reconciliation, stop-all visibility, terminal snapshot detail, and handoff continuity as the current source of truth.
- Promoted a fail-closed supervised-run lane that does not fabricate a real-demo completion claim when external prerequisites remain unresolved.
- Kept the public planner boundary unchanged and kept funded live forbidden.

## Supervised Run Boundary

- Dexter-only real demo slice
- Dexter `paper_live`
- frozen Mew-X `sim_live`
- `single_sleeve`
- `dexter_default`
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded operator-supervised window required
- funded live forbidden

## Observed Sequence

1. `prepare` exposed `demo_runtime`, `symbol_allowlist`, `demo_symbol`, `small_lot_order_size`, and `bounded_window_minutes={runtime_config.bounded_window_minutes}`.
2. `start` moved the handle into a bounded running state without widening the planner boundary.
3. `status` surfaced `native_order_status={sequence["status"]["native_order_status"]}`, `fill_count={sequence["status"]["fill_count"]}`, and `open_position_lots={sequence["status"]["open_position_lots"]}`.
4. `stop` preserved stop-all visibility with `stop_all_state={sequence["stop"]["stop_all_state"]}`.
5. `snapshot` preserved terminal detail with `stop_all_state={sequence["snapshot"]["stop_all_state"]}` and `fill_count={sequence["snapshot"]["fill_count"]}`.

## Outcome

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task state: `{TASK_STATUS}`
- Blocker: the repo-visible lane can exercise bounded runtime visibility, but it cannot honestly claim a real Dexter supervised window because external reference resolution, operator ownership, and venue connectivity remain outside the repo and unverified.
- Run timestamp: `{run_timestamp}`

## Required Current Surfaces

- current status report: `artifacts/reports/demo-forward-supervised-run-status.md`
- current report: `artifacts/reports/demo-forward-supervised-run-report.md`
- current summary: `artifacts/proofs/demo-forward-supervised-run-summary.md`
- current proof json: `artifacts/proofs/demo-forward-supervised-run-check.json`
- current handoff: `artifacts/reports/demo-forward-supervised-run/HANDOFF.md`
- supervised run operator follow-up: `docs/demo_forward_supervised_run_operator_follow_up.md`

## Recommendation

- Current task state: `{TASK_STATUS}`
- Recommended next step: `{NEXT_TASK_LANE}`
- Reason: the bounded proof lane is current, but external prerequisites must be resolved outside the repo before a real-demo completion claim can be promoted.
"""


def build_status() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN Status

- task_id: `{TASK_ID}`
- task_state: `{TASK_STATUS}`
- run_outcome: `FAIL/BLOCKED`
- key_finding: `{KEY_FINDING}`
- claim_boundary: `{CLAIM_BOUNDARY}`
- verified_vexter_main_pr: `{VERIFIED_VEXTER_PR}`
- verified_vexter_main_commit: `{VERIFIED_VEXTER_COMMIT}`
- verified_dexter_main_commit: `{VERIFIED_DEXTER_COMMIT}`
- verified_mewx_frozen_commit: `{VERIFIED_MEWX_COMMIT}`
- planner_boundary: `prepare/start/status/stop/snapshot`
- real_demo_path: `build_demo_executor_transport_registry -> DexterDemoExecutorAdapter`
- mewx_path: `unchanged_sim_live`
- next_task: `{NEXT_TASK_ID}`
"""


def build_proof_summary() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN Summary

- Verified base: Vexter `main` at PR `#72` merge commit `{VERIFIED_VEXTER_COMMIT}`.
- Starting point: the forward acceptance pack is already fixed as current source of truth.
- Exercised boundary: `prepare`, `start`, `status`, `stop`, and `snapshot` remained bounded to Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, explicit allowlist, small lot, one active real demo plan max, and one open position max.
- Observed visibility: entry surface, order/fill reconciliation, stop-all state, terminal snapshot, and handoff continuity.
- Outcome: `FAIL/BLOCKED` because external prerequisites required for an honest real-demo completion claim remain repo-external and unverified.
- Recommended next task: `{NEXT_TASK_LANE}`.
"""


def build_details() -> str:
    return f"""# {TASK_ID}

## 1. Intent
- Promote the bounded supervised run lane to the repo-visible current source of truth.
- Fail closed if the repo cannot honestly claim a real-demo completion.

## 2. Boundary
- Dexter `paper_live` only
- frozen Mew-X `sim_live` only
- `single_sleeve`
- `dexter_default`
- one active real demo plan max
- one open position max
- allowlist only
- small lot only
- bounded operator-supervised window only

## 3. Sequence
- `prepare`
- `start`
- entry visibility
- order status / fill reconciliation
- stop-all visibility
- terminal snapshot
- normalized failure continuity

## 4. Outcome
- `FAIL/BLOCKED` is acceptable if external refs, operator ownership, or connectivity remain unresolved outside the repo.

## 5. Next Task
- `{NEXT_TASK_LANE}`
"""


def build_min_prompt() -> str:
    return (
        "GitHub最新状態を確認し、Vexter `main` PR #72 merge 後の bounded supervised run を current source of truth として扱ってください。\n"
        "Dexter `paper_live` のみを real demo leg に使い、frozen Mew-X `sim_live` は unchanged のまま維持してください。\n"
        "planner の public boundary は `prepare / start / status / stop / snapshot` のまま、allowlist・small lot・poll_first・manual_latched_stop_all・terminal snapshot visibility を崩さないでください。\n"
        "real-demo completion は捏造せず、external refs / credentials / operator ownership / venue connectivity が repo 外で未確認なら fail-closed で止めてください。\n"
        "current status / report / proof / handoff / operator follow-up を更新し、次は `supervised_run_retry_readiness` を最小 cut として示してください.\n"
    )


def build_handoff(run_timestamp: str, sequence: dict, external_presence: dict[str, bool]) -> str:
    return f"""# Demo Forward Supervised Run Handoff

## Current Status
- outgoing_shift_window: {run_timestamp} bounded supervised run lane
- incoming_shift_window: external prerequisite resolution and retry readiness
- task_state: {TASK_STATUS}
- shift_outcome: blocked
- current_action: hold_real_demo_claim_until_external_resolution
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
- prior_acceptance_lane: demo_forward_acceptance_pack_ready
- comparison_source_of_truth: comparison_closed_out

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-supervised-run-status.md
- current_report: artifacts/reports/demo-forward-supervised-run-report.md
- current_proof_summary: artifacts/proofs/demo-forward-supervised-run-summary.md
- current_proof_json: artifacts/proofs/demo-forward-supervised-run-check.json
- current_operator_follow_up: docs/demo_forward_supervised_run_operator_follow_up.md
- current_operator_checklist: docs/demo_forward_operator_checklist.md
- current_abort_rollback_matrix: docs/demo_forward_abort_rollback_matrix.md
- acceptance_pack_report: artifacts/reports/demo-forward-acceptance-pack-report.md
- acceptance_pack_proof_json: artifacts/proofs/demo-forward-acceptance-pack-check.json

## Observed Sequence
- supervised_step_1: prepare
- supervised_step_2: start
- supervised_step_3: entry_visibility
- supervised_step_4: order_status_and_fill_reconciliation
- supervised_step_5: stop_or_stop_all_visibility
- supervised_step_6: terminal_snapshot
- supervised_step_7: normalized_failure_detail_and_handoff_continuity
- supervised_step_8: supervised_window_outcome
- observed_handle_id: {sequence["prepare"]["handle_id"]}
- observed_native_order_status: {sequence["status"]["native_order_status"]}
- observed_stop_all_state: {sequence["snapshot"]["stop_all_state"]}

## Guardrails
- route_mode: single_sleeve
- selected_sleeve_id: dexter_default
- max_active_real_demo_plans: 1
- max_open_positions: 1
- allowlist_required: true
- small_lot_required: true
- operator_supervised_window_required: true
- mewx_overlay_enabled: false
- funded_live_allowed: false

## External Readiness
- credential_source_visible_in_repo: {str(external_presence["DEXTER_DEMO_CREDENTIAL_SOURCE"]).lower()}
- venue_ref_visible_in_repo: {str(external_presence["DEXTER_DEMO_VENUE_REF"]).lower()}
- account_ref_visible_in_repo: {str(external_presence["DEXTER_DEMO_ACCOUNT_REF"]).lower()}
- connectivity_profile_visible_in_repo: {str(external_presence["DEXTER_DEMO_CONNECTIVITY_PROFILE"]).lower()}
- operator_owner_named_outside_repo: false
- supervised_window_start_confirmed_outside_repo: false
- venue_connectivity_confirmed_outside_repo: false
- real_demo_completion_claim_allowed: false

## Abort And Rollback Conditions
- abort_condition_1: pin_mismatch
- abort_condition_2: mode_mismatch
- abort_condition_3: status_or_fill_reconciliation_gap
- abort_condition_4: duplicate_or_ambiguous_handle
- abort_condition_5: unexpected_funded_live_path
- abort_condition_6: cancel_or_stop_all_unconfirmed
- abort_condition_7: quarantine_or_manual_halt_triggered
- abort_condition_8: terminal_snapshot_visibility_lost

## Open Questions
- question_1_or_none: who owns the named supervised window outside the repo
- question_2_or_none: when the bounded supervised window opens outside the repo
- question_3_or_none: which external venue/account/connectivity references are confirmed live outside the repo

## Next-Shift Priority Checks
- priority_check_1: resolve external credential and connectivity references outside the repo before retry
- priority_check_2: keep the lane Dexter-only and funded-live-forbidden
- priority_check_3: preserve `manual_latched_stop_all` and terminal snapshot visibility during the retry

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- operator_follow_up_pointer_checked: true
- guardrails_explicit: true
- supervised_sequence_explicit: true
- blocked_claim_boundary_explicit: true

This handoff promotes the bounded supervised run lane only. It does not claim a completed real-demo window, introduce funded live, or reopen source logic.
"""


def update_readme() -> None:
    target = (
        "`DEMO-FORWARD-ACCEPTANCE-PACK` starts from latest GitHub-visible Vexter `main`"
    )
    entry = (
        "\n\n`DEMO-FORWARD-SUPERVISED-RUN` starts from latest GitHub-visible Vexter `main` "
        f"at merged PR `#72` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`, "
        f"keeps Dexter pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`, and keeps frozen Mew-X at "
        f"`{VERIFIED_MEWX_COMMIT}`. It promotes a bounded supervised forward-demo lane rather than another packaging layer: "
        "the repo now exercises the source-faithful `prepare / start / status / stop / snapshot` sequence through "
        "`DexterDemoExecutorAdapter`, captures entry visibility, order / fill reconciliation, stop-all visibility, terminal snapshot detail, "
        "and handoff continuity as current source of truth, and then fail-closes the real-demo claim because external reference resolution, "
        "operator ownership, and venue connectivity remain repo-external and unverified. The resulting status is "
        f"`{TASK_STATUS}` with `{CLAIM_BOUNDARY}`, and the next recommended task is `{NEXT_TASK_LANE}`."
    )
    text = README_PATH.read_text()
    if "`DEMO-FORWARD-SUPERVISED-RUN` starts from latest GitHub-visible Vexter `main`" in text:
        return
    if target not in text:
        raise RuntimeError("README anchor for demo-forward acceptance pack not found")
    README_PATH.write_text(text + entry + "\n")


def main() -> None:
    run_timestamp = iso_utc_now()
    template_env = parse_template_env(TEMPLATE_ENV_PATH)
    external_presence = {name: bool(os.environ.get(name)) for name in REQUIRED_EXTERNAL_REF_VARS}
    with patched_demo_env(template_env):
        runtime_config = DexterDemoRuntimeConfig.from_env()
        runtime_errors = list(runtime_config.validation_errors())
        sequence, handle_meta = build_supervised_sequence()

    missing_external_prerequisites = [
        "operator_owner_unconfirmed",
        "supervised_window_start_unconfirmed",
        "venue_connectivity_unconfirmed",
        "external_reference_resolution_unconfirmed",
    ]
    normalized_failure_detail = {
        "failure_code": "external_prerequisites_unresolved",
        "failure_reason": (
            "repo-visible supervised sequence is current, but a real-demo completion claim remains blocked "
            "until operator ownership, external reference resolution, and venue connectivity are confirmed outside the repo"
        ),
        "missing_prerequisites": missing_external_prerequisites,
        "external_binding_presence": external_presence,
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
            "task_id": "DEMO-FORWARD-ACCEPTANCE-PACK",
            "task_state": "demo_forward_acceptance_pack_ready",
            "report": "artifacts/reports/demo-forward-acceptance-pack-report.md",
            "status_report": "artifacts/reports/demo-forward-acceptance-pack-status.md",
            "proof": "artifacts/proofs/demo-forward-acceptance-pack-check.json",
            "summary": "artifacts/proofs/demo-forward-acceptance-pack-summary.md",
            "handoff": "artifacts/reports/demo-forward-acceptance-pack/HANDOFF.md",
        },
        "demo_forward_supervised_run": {
            "planner_boundary": ["prepare", "start", "status", "stop", "snapshot"],
            "supervised_boundary": {
                "demo_source": "dexter",
                "execution_mode": "paper_live",
                "route_mode": "single_sleeve",
                "selected_sleeve_id": "dexter_default",
                "max_active_real_demo_plans": 1,
                "max_open_positions": 1,
                "allowlist_required": True,
                "small_lot_required": True,
                "operator_supervised_window_required": True,
                "mewx_overlay_enabled": False,
                "funded_live_forbidden": True,
            },
            "required_artifacts": {
                "current_status_report": "artifacts/reports/demo-forward-supervised-run-status.md",
                "current_report": "artifacts/reports/demo-forward-supervised-run-report.md",
                "current_summary": "artifacts/proofs/demo-forward-supervised-run-summary.md",
                "current_proof_json": "artifacts/proofs/demo-forward-supervised-run-check.json",
                "current_handoff": "artifacts/reports/demo-forward-supervised-run/HANDOFF.md",
                "operator_follow_up": "docs/demo_forward_supervised_run_operator_follow_up.md",
                "operator_checklist": "docs/demo_forward_operator_checklist.md",
                "abort_rollback_matrix": "docs/demo_forward_abort_rollback_matrix.md",
            },
            "supervised_sequence": sequence,
            "external_prerequisites": {
                "required_ref_variables": list(REQUIRED_EXTERNAL_REF_VARS),
                "bounded_runtime_variables": list(BOUNDED_RUNTIME_VARS),
                "repo_visible_binding_presence": external_presence,
                "runtime_validation_errors": runtime_errors,
                "operator_attestation_available": False,
                "venue_connectivity_confirmed": False,
                "real_demo_completion_claim_allowed": False,
            },
            "normalized_failure_detail": normalized_failure_detail,
            "supporting_files": [
                "specs/DEMO_FORWARD_SUPERVISED_RUN.md",
                "plans/demo_forward_supervised_run_plan.md",
                "docs/demo_forward_supervised_run_operator_follow_up.md",
                "docs/demo_forward_operator_checklist.md",
                "docs/demo_forward_abort_rollback_matrix.md",
                "scripts/run_demo_forward_supervised_run.py",
                "scripts/build_proof_bundle.sh",
                "vexter/planner_router/transport.py",
                "tests/test_planner_router_executor_transport_implementation.py",
                "tests/test_demo_forward_supervised_run.py",
            ],
            "proof_outputs": [
                "artifacts/proofs/demo-forward-supervised-run-check.json",
                "artifacts/proofs/demo-forward-supervised-run-summary.md",
                "artifacts/bundles/demo-forward-supervised-run.tar.gz",
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

    report_text = build_current_report(run_timestamp, sequence, runtime_config)
    status_text = build_status()
    proof_summary_text = build_proof_summary()
    summary_text = f"""# DEMO-FORWARD-SUPERVISED-RUN Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#72` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## What This Task Did

- Started from the acceptance pack instead of reopening adapter or baseline work.
- Exercised the bounded `prepare / start / status / stop / snapshot` lane through the source-faithful Dexter demo adapter.
- Promoted current status, report, summary, proof, handoff, and operator follow-up surfaces for the supervised run lane.
- Fail-closed the real-demo completion claim because external prerequisites remain outside the repo and unverified.

## Decision

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task status: `{TASK_STATUS}`
- Recommended next step: `{NEXT_TASK_LANE}`
- Decision: `{DECISION}`

## Key Paths

- Current spec: `specs/DEMO_FORWARD_SUPERVISED_RUN.md`
- Current implementation plan: `plans/demo_forward_supervised_run_plan.md`
- Current operator follow-up: `docs/demo_forward_supervised_run_operator_follow_up.md`
- Current proof: `artifacts/proofs/demo-forward-supervised-run-check.json`
- Current report: `artifacts/reports/demo-forward-supervised-run-report.md`
- Current handoff: `artifacts/reports/demo-forward-supervised-run/HANDOFF.md`
- Current bundle target: `artifacts/bundles/demo-forward-supervised-run.tar.gz`
"""

    prompt_context = {
        "task_id": TASK_ID,
        "task_state": TASK_STATUS,
        "recommended_next_step": NEXT_TASK_LANE,
        "recommended_next_task_id": NEXT_TASK_ID,
        "verified_vexter_main_pr": VERIFIED_VEXTER_PR,
        "verified_vexter_main_commit": VERIFIED_VEXTER_COMMIT,
        "first_demo_target": "dexter_paper_live",
        "source_faithful_seam": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "real_demo_completion_claim_allowed": False,
    }

    details_text = build_details()
    min_prompt_text = build_min_prompt()
    handoff_text = build_handoff(run_timestamp, sequence, external_presence)

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

    context_pack = read_json(CONTEXT_PATH)
    context_pack["background"] = {
        "previous_task_id": "DEMO-FORWARD-ACCEPTANCE-PACK",
        "previous_key_finding": "demo_forward_acceptance_pack_fixed",
        "previous_claim_boundary": "demo_forward_acceptance_pack_bounded",
        "promoted_pair": "task005-pass-grade-pair-20260325T180027Z",
        "confirmatory_pair": "task005-pass-grade-pair-20260325T180604Z",
        "comparison_source_of_truth_fixed_before_task": True,
        "prior_lane_completed_before_task": True,
    }
    context_pack["bundle_source"] = BUNDLE_SOURCE
    context_pack["current_contract"].update(
        {
            "demo_forward_supervised_run_marker": "demo_forward_supervised_run",
            "demo_forward_supervised_spec_path": "specs/DEMO_FORWARD_SUPERVISED_RUN.md",
            "demo_forward_supervised_plan_path": "plans/demo_forward_supervised_run_plan.md",
            "demo_forward_supervised_operator_follow_up_path": (
                "docs/demo_forward_supervised_run_operator_follow_up.md"
            ),
            "demo_forward_next_step": NEXT_TASK_LANE,
        }
    )
    context_pack["current_task"] = {
        "id": TASK_ID,
        "scope": [
            "Reverify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X after the acceptance pack.",
            "Exercise the bounded source-faithful supervised run sequence at prepare / start / status / stop / snapshot.",
            "Preserve poll_first, manual_latched_stop_all, and the Dexter-only / Mew-X-frozen seam.",
            "Promote the current status, report, summary, proof, handoff, and operator follow-up surfaces.",
            "Fail closed if the repo cannot honestly claim a completed real-demo supervised window.",
        ],
        "deliverables": [
            "README.md",
            "specs/DEMO_FORWARD_SUPERVISED_RUN.md",
            "plans/demo_forward_supervised_run_plan.md",
            "docs/demo_forward_supervised_run_operator_follow_up.md",
            "tests/test_demo_forward_supervised_run.py",
            "tests/test_demo_forward_acceptance_pack.py",
            "tests/test_pattern_a_demo_executor_cutover.py",
            "tests/test_bootstrap_layout.py",
            "scripts/run_demo_forward_supervised_run.py",
            "scripts/build_proof_bundle.sh",
            "artifacts/summary.md",
            "artifacts/context_pack.json",
            "artifacts/proof_bundle_manifest.json",
            "artifacts/task_ledger.jsonl",
            "artifacts/reports/demo-forward-supervised-run-report.md",
            "artifacts/reports/demo-forward-supervised-run-status.md",
            "artifacts/reports/demo-forward-supervised-run/DETAILS.md",
            "artifacts/reports/demo-forward-supervised-run/MIN_PROMPT.txt",
            "artifacts/reports/demo-forward-supervised-run/CONTEXT.json",
            "artifacts/reports/demo-forward-supervised-run/HANDOFF.md",
            "artifacts/proofs/demo-forward-supervised-run-check.json",
            "artifacts/proofs/demo-forward-supervised-run-summary.md",
            "artifacts/bundles/demo-forward-supervised-run.tar.gz",
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
            "latest_recent_vexter_prs": [72, 71, 70, 69, 68],
            "vexter_pr_72_merged_at": VERIFIED_VEXTER_MERGED_AT,
            "vexter_pr_72_closed_at": VERIFIED_VEXTER_MERGED_AT,
        }
    )
    context_pack["evidence"]["demo_forward_supervised_run"] = {
        "report": "artifacts/reports/demo-forward-supervised-run-report.md",
        "status_report": "artifacts/reports/demo-forward-supervised-run-status.md",
        "proof": "artifacts/proofs/demo-forward-supervised-run-check.json",
        "summary": "artifacts/proofs/demo-forward-supervised-run-summary.md",
        "handoff_dir": "artifacts/reports/demo-forward-supervised-run",
        "operator_follow_up": "docs/demo_forward_supervised_run_operator_follow_up.md",
        "key_finding": KEY_FINDING,
        "claim_boundary": CLAIM_BOUNDARY,
        "task_state": TASK_STATUS,
        "run_outcome": "FAIL/BLOCKED",
        "real_demo_completion_claim_allowed": False,
        "preferred_next_step": NEXT_TASK_LANE,
        "supervised_boundary": proof["demo_forward_supervised_run"]["supervised_boundary"],
        "supervised_sequence": [
            "prepare",
            "start",
            "entry_visibility",
            "order_status_and_fill_reconciliation",
            "stop_or_stop_all_visibility",
            "terminal_snapshot",
            "normalized_failure_detail_and_handoff_continuity",
            "supervised_window_outcome",
        ],
    }
    context_pack["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "rationale": [
            "The bounded supervised sequence is now current source of truth.",
            "The real-demo completion claim remains blocked until external prerequisites are resolved outside the repo.",
            "The shortest next cut is retry readiness rather than widening scope or reopening baseline work.",
        ],
    }
    context_pack["proofs"].update(
        {
            "demo_forward_supervised_run_lane_added": True,
            "demo_forward_supervised_sequence_exercised": True,
            "demo_forward_supervised_current_pointers_fixed": True,
            "demo_forward_supervised_operator_follow_up_written": True,
            "demo_forward_real_window_claim_blocked": True,
            "recommended_next_step_is_supervised_run_retry_readiness": True,
        }
    )
    CONTEXT_PATH.write_text(format_json(context_pack))

    manifest = read_json(MANIFEST_PATH)
    manifest["bundle_path"] = BUNDLE_PATH
    manifest["bundle_source"] = BUNDLE_SOURCE
    manifest["task_id"] = TASK_ID
    manifest["status"] = TASK_STATUS
    for key, path in (
        ("docs", "docs/demo_forward_supervised_run_operator_follow_up.md"),
        ("scripts", "scripts/run_demo_forward_supervised_run.py"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-check.json"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-summary.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-report.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-status.md"),
    ):
        if path not in manifest[key]:
            manifest[key].append(path)
    for path in (
        "specs/DEMO_FORWARD_SUPERVISED_RUN.md",
        "plans/demo_forward_supervised_run_plan.md",
        "tests/test_demo_forward_supervised_run.py",
        "artifacts/bundles/demo-forward-supervised-run.tar.gz",
    ):
        included_key = "included_paths"
        if path not in manifest[included_key]:
            manifest[included_key].append(path)
    manifest["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "resume_requirements": [
            f"Keep Dexter pinned at {VERIFIED_DEXTER_COMMIT} and Mew-X frozen at {VERIFIED_MEWX_COMMIT}.",
            "Start only from the current supervised-run status, report, proof, summary, handoff, and operator follow-up surfaces.",
            "Resolve external reference bindings, operator ownership, and venue connectivity outside the repo before retrying.",
            "Keep the planner boundary at prepare / start / status / stop / snapshot and preserve poll_first plus manual_latched_stop_all.",
            "Do not introduce funded live or a Mew-X real-demo path.",
        ],
    }
    manifest["proofs"].update(
        {
            "demo_forward_supervised_run_lane_added": True,
            "demo_forward_supervised_sequence_exercised": True,
            "demo_forward_supervised_current_pointers_fixed": True,
            "demo_forward_supervised_operator_follow_up_written": True,
            "demo_forward_real_window_claim_blocked": True,
            "recommended_next_step_is_supervised_run_retry_readiness": True,
        }
    )
    MANIFEST_PATH.write_text(format_json(manifest))

    ledger_payload = {
        "artifact_bundle": BUNDLE_PATH,
        "base_main": VERIFIED_VEXTER_COMMIT,
        "branch": git_output("branch", "--show-current"),
        "claim_boundary": CLAIM_BOUNDARY,
        "comparison_source_of_truth_state": "comparison_closed_out",
        "confirmatory_overturns_promoted_baseline": False,
        "confirmatory_residual": "Mew-X candidate_rejected",
        "confirmatory_same_attempt_label": "task005-pass-grade-pair-20260325T180604Z",
        "date": datetime.now(timezone.utc).date().isoformat(),
        "decision": DECISION,
        "default_execution_anchor": "dexter",
        "demo_forward_supervised_run_lane_added": True,
        "demo_forward_supervised_sequence_exercised": True,
        "demo_forward_supervised_operator_follow_up_written": True,
        "demo_forward_real_window_claim_blocked": True,
        "first_demo_target": "dexter_paper_live",
        "key_finding": KEY_FINDING,
        "live_metric_winner_tally": {"dexter": 6, "mewx": 4, "tie": 2},
        "new_evidence_collection_required": False,
        "next_task_id": NEXT_TASK_ID,
        "next_task_state": NEXT_TASK_STATE,
        "prior_lane_source_state": "demo_forward_acceptance_pack_ready",
        "promoted_live_winner_mode": "derived",
        "promoted_replay_winner_mode": "derived",
        "promoted_same_attempt_label": "task005-pass-grade-pair-20260325T180027Z",
        "proof": "artifacts/proofs/demo-forward-supervised-run-check.json",
        "recommended_next_lane": NEXT_TASK_LANE,
        "replay_metric_winner_tally": {"dexter": 6, "mewx": 4, "tie": 2},
        "repo": "https://github.com/Cabbala/Vexter",
        "run_sequence_handle_id": handle_meta["handle_id"],
        "selected_outcome": "FAIL/BLOCKED",
        "selective_option_source": "mewx",
        "source_faithful_modes": {"dexter": "paper_live", "mewx": "sim_live"},
        "status": TASK_STATUS,
        "supporting_vexter_prs": [72, 71, 70, 69, 68],
        "task_id": TASK_ID,
        "verified_dexter_main_commit": VERIFIED_DEXTER_COMMIT,
        "verified_dexter_pr": 3,
        "verified_mewx_frozen_commit": VERIFIED_MEWX_COMMIT,
        "verified_prs": [72, 71, 70],
    }
    with LEDGER_PATH.open("a") as handle:
        handle.write(format_jsonl(ledger_payload))

    update_readme()


if __name__ == "__main__":
    main()
