#!/usr/bin/env python3
"""Emit bounded retry-gate proof surfaces from the retry-readiness baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vexter.planner_router.transport import DexterDemoRuntimeConfig

from scripts.run_demo_forward_supervised_run_retry_readiness import (
    format_json,
    git_output,
    iso_utc_now,
    parse_template_env,
    patched_demo_env,
    read_json,
)


TEMPLATE_ENV_PATH = ROOT / "templates" / "windows_runtime" / "dexter.env.example"
CONTEXT_PATH = ROOT / "artifacts" / "context_pack.json"
MANIFEST_PATH = ROOT / "artifacts" / "proof_bundle_manifest.json"
SUMMARY_PATH = ROOT / "artifacts" / "summary.md"
README_PATH = ROOT / "README.md"
LEDGER_PATH = ROOT / "artifacts" / "task_ledger.jsonl"

CHECKLIST_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_gate_checklist.md"
DECISION_SURFACE_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_gate_decision_surface.md"
SCRIPT_PATH = ROOT / "scripts" / "run_demo_forward_supervised_run_retry_gate.py"
SPEC_PATH = ROOT / "specs" / "DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md"
PLAN_PATH = ROOT / "plans" / "demo_forward_supervised_run_retry_gate_plan.md"

PREVIOUS_REPORT_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-readiness-report.md"
PREVIOUS_STATUS_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-readiness-status.md"
PREVIOUS_PROOF_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-readiness-check.json"
PREVIOUS_SUMMARY_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-readiness-summary.md"
)
PREVIOUS_HANDOFF_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-readiness" / "HANDOFF.md"
)
PREVIOUS_CHECKLIST_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_readiness_checklist.md"
PREVIOUS_MATRIX_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_prerequisite_matrix.md"
PREVIOUS_SUBAGENTS_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-readiness" / "SUBAGENTS.md"
)

REPORT_DIR = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate"
REPORT_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-report.md"
STATUS_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-status.md"
SUBAGENTS_PATH = REPORT_DIR / "SUBAGENTS.md"
SUBAGENT_SUMMARY_PATH = REPORT_DIR / "subagent_summary.md"
PROOF_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-check.json"
PROOF_SUMMARY_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-summary.md"

BUNDLE_PATH = "artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz"
BUNDLE_SOURCE = "/Users/cabbala/Downloads/vexter_supervised_run_retry_gate_bundle.tar.gz"

TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
TASK_STATUS = "supervised_run_retry_gate_blocked"
KEY_FINDING = "supervised_run_retry_gate_blocked_on_unresolved_gate_inputs"
CLAIM_BOUNDARY = "supervised_run_retry_gate_bounded"
NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
NEXT_TASK_STATE = "retry_gate_inputs_pending"
NEXT_TASK_LANE = "supervised_run_retry_gate"
PASS_NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-EXECUTION"
PASS_NEXT_TASK_STATE = "ready_for_supervised_run_retry_execution"
PASS_NEXT_TASK_LANE = "supervised_run_retry_execution"
DECISION = "retry_execution_blocked_pending_gate_inputs"

VERIFIED_DEXTER_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
VERIFIED_MEWX_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
VERIFIED_VEXTER_PR = 74
VERIFIED_VEXTER_COMMIT = "d06856cecf42c336af05902a1d932468c5d280b0"
VERIFIED_VEXTER_MERGED_AT = "2026-03-27T01:20:35Z"

SUB_AGENT_SUMMARIES = (
    {
        "name": "Anscombe",
        "lines": [
            "Confirmed the retry-readiness quartet should remain current until a complete retry-gate quartet exists, then switch atomically to the new gate report, status, proof, summary, and handoff surfaces.",
            "Flagged the readiness-era prerequisite-count drift as a reason to keep the retry-gate decision surface on one explicit, stable list of gate inputs.",
            "Recommended keeping fail-closed wording observation-based: repo-visible markers may be named, but retry execution stays blocked until external confirmations are explicitly observed enough for the gate to pass.",
        ],
    },
    {
        "name": "Euler",
        "lines": [
            "Kept the retry-gate boundary identical to the accepted retry-readiness boundary: Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, allowlist-only, small-lot, one-plan, one-position, bounded supervision, and funded-live forbidden.",
            "Recommended the smallest next-step cut: hold the current lane at `supervised_run_retry_gate` while blocked, and expose `supervised_run_retry_execution` only as the gate-pass successor once every required input is explicit.",
            "Confirmed there is no need for planner or adapter code drift: `prepare / start / status / stop / snapshot` stays fixed, `manual_latched_stop_all` stays planner-owned, and Mew-X remains unchanged.",
        ],
    },
    {
        "name": "Parfit",
        "lines": [
            "Scoped the smallest safe change set to docs, proof-generation script, generated artifacts, manifest/context/ledger updates, and tests; no `vexter/` runtime behavior changes are needed for this lane.",
            "Recommended validating the generator plus the affected regression surfaces with `python3 scripts/run_demo_forward_supervised_run_retry_gate.py` and focused `pytest` coverage on the supervised-run and bundle-layout tests.",
            "Merge readiness depends on an atomic current-pointer switch to retry-gate, a regenerated tarball at the new bundle path, and a clean blocked decision that does not claim retry execution success.",
        ],
    },
)


def format_marker(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)


def format_jsonl(payload: object) -> str:
    return json.dumps(payload, sort_keys=False) + "\n"


def rewrite_local_ledger(entry: dict[str, object]) -> None:
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


def build_gate_inputs(template_env: dict[str, str], runtime_config: DexterDemoRuntimeConfig) -> list[dict]:
    runtime_guardrails = {
        "allowed_symbols": list(runtime_config.allowed_symbols),
        "default_symbol": runtime_config.default_symbol,
        "order_size_lots": str(runtime_config.order_size_lots),
        "max_order_size_lots": str(runtime_config.max_order_size_lots),
        "bounded_window_minutes": runtime_config.bounded_window_minutes,
        "max_open_positions": runtime_config.max_open_positions,
    }
    return [
        {
            "name": "external_credential_source_face",
            "repo_visible_marker": template_env["DEXTER_DEMO_CREDENTIAL_SOURCE"],
            "current_observation": (
                "A reference name is visible in repo, but the external credential resolution is not observed in repo."
            ),
            "who_confirms": "named_operator_owner_outside_repo",
            "explicit_enough_for_retry_execution": False,
            "pass_when": (
                "the named operator explicitly attests that the reference resolves to the intended Dexter paper-live credential source for the bounded retry window"
            ),
        },
        {
            "name": "venue_ref_face",
            "repo_visible_marker": template_env["DEXTER_DEMO_VENUE_REF"],
            "current_observation": (
                "A venue reference is visible in repo, but the active venue mapping for the retry window is not observed in repo."
            ),
            "who_confirms": "named_operator_owner_plus_venue_owner_outside_repo",
            "explicit_enough_for_retry_execution": False,
            "pass_when": (
                "the venue reference is explicitly matched to the intended Dexter demo venue for the bounded retry window"
            ),
        },
        {
            "name": "account_ref_face",
            "repo_visible_marker": template_env["DEXTER_DEMO_ACCOUNT_REF"],
            "current_observation": (
                "An account reference is visible in repo, but the retry-window account binding is not observed in repo."
            ),
            "who_confirms": "named_operator_owner_outside_repo",
            "explicit_enough_for_retry_execution": False,
            "pass_when": (
                "the account reference is explicitly matched to the intended Dexter paper-live account for the retry window"
            ),
        },
        {
            "name": "connectivity_profile_face",
            "repo_visible_marker": template_env["DEXTER_DEMO_CONNECTIVITY_PROFILE"],
            "current_observation": (
                "A connectivity profile marker is visible in repo, but the live retry-path reachability is not observed in repo."
            ),
            "who_confirms": "named_operator_owner_plus_connectivity_owner_outside_repo",
            "explicit_enough_for_retry_execution": False,
            "pass_when": (
                "the connectivity profile is explicitly confirmed to reach the intended venue and account during the bounded retry window"
            ),
        },
        {
            "name": "operator_owner_face",
            "repo_visible_marker": "unconfirmed_outside_repo",
            "current_observation": (
                "The repo does not identify one retry owner for the full supervised window."
            ),
            "who_confirms": "demo_operator_lead_outside_repo",
            "explicit_enough_for_retry_execution": False,
            "pass_when": "one explicit operator owner is named for the full retry gate and supervised window",
        },
        {
            "name": "bounded_start_criteria_face",
            "repo_visible_marker": {
                "bounded_window_minutes": runtime_config.bounded_window_minutes,
                "status_delivery": "poll_first",
                "halt_mode": "manual_latched_stop_all",
            },
            "current_observation": (
                "The bounded window and stop model are fixed in repo, but the actual retry start time, go/no-go owner, and abort owner are not observed in repo."
            ),
            "who_confirms": "named_operator_owner_outside_repo",
            "explicit_enough_for_retry_execution": False,
            "pass_when": (
                "the retry start time, bounded window, abort owner, and go/no-go criteria are explicitly agreed before entry"
            ),
        },
        {
            "name": "allowlist_symbol_lot_reconfirmed",
            "repo_visible_marker": runtime_guardrails,
            "current_observation": (
                "The bounded symbol, lot-size, window, and one-position guardrails parse cleanly from repo, but retry-time reconfirmation is not observed in repo."
            ),
            "who_confirms": "named_operator_owner_outside_repo",
            "explicit_enough_for_retry_execution": False,
            "pass_when": (
                "the operator explicitly reconfirms allowlist, default symbol, lot size, bounded window, and one-position cap immediately before retry"
            ),
        },
        {
            "name": "manual_latched_stop_all_visibility_reconfirmed",
            "repo_visible_marker": "baseline_stop_all_state=flatten_confirmed",
            "current_observation": (
                "The blocked supervised baseline preserved `manual_latched_stop_all`, but retry-path visibility is not yet re-observed for the next gate window."
            ),
            "who_confirms": "named_operator_owner_outside_repo",
            "explicit_enough_for_retry_execution": False,
            "pass_when": (
                "`manual_latched_stop_all` visibility is explicitly reconfirmed on the bounded retry path before entry"
            ),
        },
        {
            "name": "terminal_snapshot_readability_reconfirmed",
            "repo_visible_marker": "baseline_terminal_snapshot_readable=true",
            "current_observation": (
                "The baseline handoff shows terminal snapshot detail, but retry-path terminal snapshot readability is not yet re-observed for the next gate window."
            ),
            "who_confirms": "named_operator_owner_outside_repo",
            "explicit_enough_for_retry_execution": False,
            "pass_when": (
                "terminal snapshot readability is explicitly reconfirmed on the retry path before entry"
            ),
        },
    ]


def build_gate_checklist(inputs: list[dict], runtime_errors: list[str]) -> dict[str, bool]:
    return {
        "runtime_guardrails_parse_cleanly": not runtime_errors,
        "external_credential_source_face_explicit": False,
        "venue_ref_face_explicit": False,
        "account_ref_face_explicit": False,
        "connectivity_profile_face_explicit": False,
        "operator_owner_face_explicit": False,
        "bounded_start_criteria_face_explicit": False,
        "allowlist_symbol_lot_reconfirmed": False,
        "manual_latched_stop_all_visibility_reconfirmed": False,
        "terminal_snapshot_readability_reconfirmed": False,
        "all_gate_inputs_explicit_enough": all(
            row["explicit_enough_for_retry_execution"] for row in inputs
        ),
        "real_demo_retry_execution_allowed": all(
            row["explicit_enough_for_retry_execution"] for row in inputs
        ),
    }


def build_spec() -> str:
    return f"""# Demo Forward Supervised Run Retry Gate

This document fixes the bounded retry-gate lane after `DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS` made the external prerequisite gap current and reviewable.

## Verified Base

- Latest merged Vexter `main`: PR `#74`, merge commit `{VERIFIED_VEXTER_COMMIT}`, merged at `{VERIFIED_VEXTER_MERGED_AT}`
- Dexter merged `main`: PR `#3`, merge commit `{VERIFIED_DEXTER_COMMIT}`
- Frozen Mew-X commit: `{VERIFIED_MEWX_COMMIT}`
- Retry-readiness baseline proof: `artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json`

## Purpose

The shortest next lane is not retry execution. It is fixing one bounded retry gate that decides, fail-closed, whether the repo-visible and externally confirmed inputs are explicit enough to let `supervised_run_retry_execution` begin.

## Planner Boundary Remains Fixed

The public planner surface remains:

- `prepare`
- `start`
- `status`
- `stop`
- `snapshot`

Planner ownership remains unchanged:

- immutable plan emission
- `poll_first` reconciliation
- `manual_latched_stop_all`
- quarantine classification
- normalized failure detail fan-in

Adapter-owned runtime detail remains unchanged:

- source-native demo submit
- source-native cancel
- order status polling
- fill collection
- stop-all fanout and terminal snapshot detail

## Retry Gate Boundary

The bounded retry-gate lane remains:

- Dexter-only real demo slice
- `single_sleeve`
- `dexter_default`
- Dexter `paper_live`
- frozen Mew-X `sim_live`
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded supervised window required
- external credential refs remain outside repo
- operator owner must be explicit
- venue / connectivity confirmation must be explicit
- bounded start criteria must be explicit
- allowlist / symbol / lot-size reconfirmation must be explicit
- `manual_latched_stop_all` visibility must be reconfirmed
- terminal snapshot readability must be reconfirmed
- Mew-X unchanged
- funded live forbidden

## Required Current Surfaces

The repo must expose the following as current source of truth:

- current status report
- current report
- current summary
- current proof json
- current handoff
- retry gate checklist
- retry gate decision surface
- next recommended step

## Honest Gate Model

The bounded retry gate must hold one of these honest outcomes:

- PASS: the gate inputs are explicit enough to enter `supervised_run_retry_execution`
- FAIL/BLOCKED: one or more gate inputs remain unresolved, so retry execution does not begin

The repo may name external references and confirmations, but it must not embed credentials, secrets, or fabricated pass evidence.

## Gate Input Model

The gate decision surface must include at least:

- external credential source face explicit
- venue ref face explicit
- account ref face explicit
- connectivity profile face explicit
- operator owner face explicit
- bounded start criteria explicit
- allowlist / symbol / lot-size reconfirmed
- `manual_latched_stop_all` visibility reconfirmed
- terminal snapshot readability reconfirmed

## Next-Step Boundary

- While blocked, the current lane remains `supervised_run_retry_gate`.
- Only after every gate input is explicit enough may the next recommended lane advance to `supervised_run_retry_execution`.

## Out Of Scope

- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no portfolio split
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success
"""


def build_plan() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE Plan

## Objective

Promote a bounded `supervised_run_retry_gate` lane to the repo-visible current source of truth after retry readiness, without widening planner scope or fabricating retry execution success.

## Inputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md`
- `docs/demo_forward_supervised_run_retry_readiness_checklist.md`
- `docs/demo_forward_supervised_run_retry_prerequisite_matrix.md`

## Steps

1. Reverify latest GitHub-visible `main` after PR `#74`.
2. Keep Dexter pinned at merged PR `#3` and keep frozen Mew-X unchanged.
3. Accept `supervised_run_retry_readiness_blocked` as the current baseline instead of retrying execution.
4. Promote a retry-gate spec, status, report, summary, proof, handoff, checklist, and decision surface as the current source of truth.
5. Fix one bounded gate decision surface that makes every required gate input explicit and fail-closed.
6. Preserve the planner boundary at `prepare / start / status / stop / snapshot`, keep `poll_first`, and keep `manual_latched_stop_all` planner-owned.
7. Keep the current lane blocked unless every gate input is explicit enough to enter `supervised_run_retry_execution`.

## Guardrails

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
- bounded start criteria must be explicit
- `manual_latched_stop_all` visibility must be reconfirmed
- terminal snapshot readability must be reconfirmed
- Mew-X unchanged
- funded live forbidden

## Required Outputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md`
- `plans/demo_forward_supervised_run_retry_gate_plan.md`
- `docs/demo_forward_supervised_run_retry_gate_checklist.md`
- `docs/demo_forward_supervised_run_retry_gate_decision_surface.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-report.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/DETAILS.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/MIN_PROMPT.txt`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/CONTEXT.json`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md`
- `artifacts/summary.md`
- `artifacts/context_pack.json`
- `artifacts/proof_bundle_manifest.json`
- `artifacts/task_ledger.jsonl`
- `artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz`

## Acceptance

- Retry readiness remains the accepted baseline.
- The retry-gate surface records every required gate input without embedding external secrets.
- The current handoff points directly at checklist and decision-surface artifacts.
- The current lane remains `FAIL/BLOCKED` until retry execution is honestly permitted.
"""


def build_checklist() -> str:
    return f"""# Demo Forward Supervised Run Retry Gate Checklist

This checklist fixes the minimum operator-visible surface that must be explicit before retry execution may begin.

## Current Pointers

1. Start at `artifacts/reports/demo-forward-supervised-run-retry-gate-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-gate-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`.
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md`.
5. Use `docs/demo_forward_supervised_run_retry_gate_decision_surface.md` as the single retry-gate decision surface.

## Retry Gate Checklist

1. Accept the prior `supervised_run_retry_readiness_blocked` lane as baseline and do not claim retry execution success.
2. Name the operator owner outside the repo and record who owns the bounded retry window.
3. Explicitly resolve `DEXTER_DEMO_CREDENTIAL_SOURCE`, `DEXTER_DEMO_VENUE_REF`, `DEXTER_DEMO_ACCOUNT_REF`, and `DEXTER_DEMO_CONNECTIVITY_PROFILE` outside the repo.
4. Explicitly record the bounded start time, go/no-go owner, abort owner, and stop conditions outside the repo before entry.
5. Reconfirm `DEXTER_DEMO_ALLOWED_SYMBOLS`, `DEXTER_DEMO_DEFAULT_SYMBOL`, `DEXTER_DEMO_ORDER_SIZE_LOTS`, `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`, `DEXTER_DEMO_WINDOW_MINUTES=15`, and `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`.
6. Reconfirm venue and connectivity readiness for the bounded retry window.
7. Reconfirm `manual_latched_stop_all` visibility on the retry path.
8. Reconfirm terminal snapshot readability on the retry path.
9. Reconfirm Mew-X remains unchanged on `sim_live`.
10. Reconfirm funded live remains forbidden.

## Retry Gate Exit Criteria

- every gate-input row in `docs/demo_forward_supervised_run_retry_gate_decision_surface.md` is explicit enough to allow retry execution
- operator owner is named outside the repo
- venue and connectivity are confirmed for the bounded window
- allowlist, symbol, lot-size, window, and one-position cap are reconfirmed
- `manual_latched_stop_all` visibility and terminal snapshot readability are reconfirmed
- retry remains Dexter-only `paper_live`

## Never Relax

- `prepare / start / status / stop / snapshot`
- `poll_first`
- `manual_latched_stop_all`
- explicit allowlist
- small lot
- one active real demo plan max
- one open position max
- Mew-X unchanged
- funded live forbidden
"""


def build_decision_surface(inputs: list[dict]) -> str:
    lines = [
        "# Demo Forward Supervised Run Retry Gate Decision Surface",
        "",
        "This decision surface is the current source of truth for `supervised_run_retry_gate`.",
        "",
        "| Gate input | Repo-visible face | Current observation | Gate passes when |",
        "| --- | --- | --- | --- |",
    ]
    for row in inputs:
        lines.append(
            f"| `{row['name']}` | `{format_marker(row['repo_visible_marker'])}` | {row['current_observation']} | {row['pass_when']} |"
        )
    lines.extend(
        [
            "",
            "## Current Decision",
            "",
            "- Gate outcome: `FAIL/BLOCKED`",
            f"- Key finding: `{KEY_FINDING}`",
            f"- Claim boundary: `{CLAIM_BOUNDARY}`",
            f"- Current task state: `{TASK_STATUS}`",
            f"- Recommended next step while blocked: `{NEXT_TASK_LANE}`",
            f"- Gate-pass successor: `{PASS_NEXT_TASK_LANE}`",
            "- Retry execution allowed now: `false`",
            "",
            "Retry execution does not begin unless every gate-input row is explicit enough to permit it.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_current_report(
    run_timestamp: str,
    previous_proof: dict,
    runtime_config: DexterDemoRuntimeConfig,
    inputs: list[dict],
) -> str:
    unresolved = [row["name"] for row in inputs if not row["explicit_enough_for_retry_execution"]]
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE Report

## Verified Base

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#74`, merge commit `{VERIFIED_VEXTER_COMMIT}`, merged at `{VERIFIED_VEXTER_MERGED_AT}`.
- Dexter remained pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen Mew-X remained pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## Starting Point

- Accepted `supervised_run_retry_readiness_blocked` as the current blocked baseline instead of fabricating a retry execution.
- Carried forward the bounded retry-readiness proof, report, summary, and handoff as the baseline current source of truth.
- Promoted retry gate as the new current operator-visible lane.

## Retry Gate Boundary

- Dexter-only real demo slice
- `single_sleeve`
- `dexter_default`
- Dexter `paper_live`
- frozen Mew-X `sim_live`
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded supervised window required
- external credential refs remain outside repo
- operator owner must be explicit
- venue / connectivity confirmation must be explicit
- bounded start criteria must be explicit
- allowlist / symbol / lot-size reconfirmation must be explicit
- `manual_latched_stop_all` visibility must be reconfirmed
- terminal snapshot readability must be reconfirmed
- funded live forbidden

## Baseline Continuity

- retry-readiness status path: `artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md`
- retry-readiness proof path: `artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json`
- retry-readiness handoff path: `artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md`
- retry-readiness checklist path: `docs/demo_forward_supervised_run_retry_readiness_checklist.md`
- retry-readiness prerequisite matrix path: `docs/demo_forward_supervised_run_retry_prerequisite_matrix.md`
- bounded runtime guardrails stayed parseable from `templates/windows_runtime/dexter.env.example`
- runtime validation errors: `{len(list(runtime_config.validation_errors()))}`
- retry-readiness recommended next step: `{previous_proof['task_result']['recommended_next_step']}`

## Required Current Surfaces

- current status report: `artifacts/reports/demo-forward-supervised-run-retry-gate-status.md`
- current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-report.md`
- current summary: `artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md`
- current proof json: `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`
- current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md`
- retry gate checklist: `docs/demo_forward_supervised_run_retry_gate_checklist.md`
- retry gate decision surface: `docs/demo_forward_supervised_run_retry_gate_decision_surface.md`
- sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md`

## Gate Decision Summary

- unresolved gate input count: `{len(unresolved)}`
- unresolved gate inputs: `{", ".join(unresolved)}`
- bounded window minutes: `{runtime_config.bounded_window_minutes}`
- allowlist: `{", ".join(runtime_config.allowed_symbols)}`
- default symbol: `{runtime_config.default_symbol}`
- order size lots: `{runtime_config.order_size_lots}`
- max open positions: `{runtime_config.max_open_positions}`
- retry execution allowed now: `false`

## Outcome

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task state: `{TASK_STATUS}`
- Blocker: one or more retry-gate inputs remain external, unresolved, or not explicit enough in repo-visible form to allow retry execution.
- Run timestamp: `{run_timestamp}`

## Recommendation

- Current task state: `{TASK_STATUS}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Gate-pass successor: `{PASS_NEXT_TASK_LANE}`
- Reason: the gate is now current source of truth, but retry execution remains fail-closed until every required gate input is explicit enough.
"""


def build_status() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE Status

- task_id: `{TASK_ID}`
- task_state: `{TASK_STATUS}`
- run_outcome: `FAIL/BLOCKED`
- key_finding: `{KEY_FINDING}`
- claim_boundary: `{CLAIM_BOUNDARY}`
- verified_vexter_main_pr: `{VERIFIED_VEXTER_PR}`
- verified_vexter_main_commit: `{VERIFIED_VEXTER_COMMIT}`
- verified_dexter_main_commit: `{VERIFIED_DEXTER_COMMIT}`
- verified_mewx_frozen_commit: `{VERIFIED_MEWX_COMMIT}`
- baseline_task: `DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS`
- baseline_task_state: `supervised_run_retry_readiness_blocked`
- planner_boundary: `prepare/start/status/stop/snapshot`
- current_gate_lane: `{NEXT_TASK_LANE}`
- gate_pass_successor: `{PASS_NEXT_TASK_LANE}`
"""


def build_proof_summary() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE Summary

- Verified base: Vexter `main` at PR `#74` merge commit `{VERIFIED_VEXTER_COMMIT}`.
- Starting point: retry readiness already bounded the missing prerequisite set without claiming retry execution.
- Promoted boundary: retry gate is now current source of truth for the same Dexter-only `paper_live` / frozen Mew-X `sim_live` seam, `single_sleeve`, `dexter_default`, explicit allowlist, small lot, bounded supervised window, one active real demo plan max, and one open position max.
- Added current surfaces: retry gate status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary.
- Outcome: `FAIL/BLOCKED` because the gate inputs are still not explicit enough to permit retry execution.
- Recommended next step while blocked: `{NEXT_TASK_LANE}`.
- Gate-pass successor: `{PASS_NEXT_TASK_LANE}`.
"""


def build_details() -> str:
    return f"""# {TASK_ID}

## 1. Intent
- Accept the blocked retry-readiness lane as baseline.
- Promote retry gate to the repo-visible current source of truth.

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
- decision surface
- sub-agent summary

## 4. Honest Gate Model
- `PASS` only if every gate input is explicit enough to allow `supervised_run_retry_execution`.
- `FAIL/BLOCKED` if any gate input remains unresolved or unobserved enough.

## 5. Next-Step Boundary
- blocked current lane: `{NEXT_TASK_LANE}`
- gate-pass successor: `{PASS_NEXT_TASK_LANE}`
"""


def build_min_prompt() -> str:
    return (
        "GitHub最新状態を確認し、Vexter `main` PR #74 merge 後の retry-gate surface を current source of truth として扱ってください。\n"
        "出発点は `supervised_run_retry_readiness_blocked` で、Dexter `paper_live` のみ・frozen Mew-X `sim_live` のみ・`single_sleeve`・`dexter_default`・explicit allowlist・small lot・max open positions=1・bounded supervised window を維持してください。\n"
        "planner の public boundary は `prepare / start / status / stop / snapshot` のまま、`manual_latched_stop_all` は planner-owned のまま保ってください。\n"
        "external credential refs は repo 外に残し、gate input が揃わない限り `FAIL/BLOCKED` を維持し、retry execution success を捏造しないでください。\n"
        "current status / report / proof / handoff / checklist / decision surface / sub-agent summary を更新し、gate が pass した場合にのみ次を `supervised_run_retry_execution` と示してください。\n"
    )


def build_handoff(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    inputs: list[dict],
) -> str:
    return f"""# Demo Forward Supervised Run Retry Gate Handoff

## Current Status
- outgoing_shift_window: {run_timestamp} retry-gate lane
- incoming_shift_window: explicit gate-input resolution and possible retry execution entry
- task_state: {TASK_STATUS}
- shift_outcome: blocked
- current_action: hold_retry_execution_until_gate_passes
- recommended_next_step_while_blocked: {NEXT_TASK_LANE}
- gate_pass_successor: {PASS_NEXT_TASK_LANE}
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: {VERIFIED_VEXTER_COMMIT}
- dexter_main_commit: {VERIFIED_DEXTER_COMMIT}
- mewx_frozen_commit: {VERIFIED_MEWX_COMMIT}
- baseline_retry_readiness_task_state: supervised_run_retry_readiness_blocked

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-status.md
- current_report: artifacts/reports/demo-forward-supervised-run-retry-gate-report.md
- current_proof_summary: artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md
- current_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json
- current_retry_gate_checklist: docs/demo_forward_supervised_run_retry_gate_checklist.md
- current_retry_gate_decision_surface: docs/demo_forward_supervised_run_retry_gate_decision_surface.md
- current_subagent_summary: artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md
- baseline_status_report: artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md
- baseline_report: artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md
- baseline_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json
- baseline_handoff: artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md

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
- manual_latched_stop_all_visibility_reconfirmation_required: true
- terminal_snapshot_readability_reconfirmation_required: true
- mewx_overlay_enabled: false
- funded_live_allowed: false

## Gate Inputs
{chr(10).join(f"- {row['name']}: explicit_enough_for_retry_execution={str(row['explicit_enough_for_retry_execution']).lower()}, who_confirms={row['who_confirms']}" for row in inputs)}

## Open Questions
- question_1_or_none: who is the named operator owner for the bounded retry window
- question_2_or_none: when does the bounded retry window open and who gives final go/no-go
- question_3_or_none: which venue, account, and connectivity refs are explicitly confirmed live outside the repo
- question_4_or_none: has `manual_latched_stop_all` visibility been reconfirmed before entry
- question_5_or_none: has terminal snapshot readability been reconfirmed before entry

## Next-Shift Priority Checks
- priority_check_1: keep the current lane blocked unless every gate-input row is explicit enough
- priority_check_2: preserve Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, small-lot, one-position, and funded-live-forbidden guardrails
- priority_check_3: preserve `manual_latched_stop_all`, poll-first status visibility, and terminal snapshot readability during any future gate-pass attempt

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- checklist_pointer_checked: true
- decision_surface_pointer_checked: true
- subagent_summary_pointer_checked: true
- blocked_claim_boundary_explicit: true

This handoff promotes the bounded retry-gate lane only. It does not claim a passed gate, a completed retry execution, funded live access, or any Mew-X seam expansion.
"""


def build_subagents() -> str:
    lines = ["# Demo Forward Supervised Run Retry Gate Sub-agent Summaries", ""]
    for item in SUB_AGENT_SUMMARIES:
        lines.append(f"## {item['name']}")
        for line in item["lines"]:
            lines.append(f"- {line}")
        lines.append("")
    return "\n".join(lines)


def update_readme() -> None:
    marker = "`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE` starts from latest GitHub-visible Vexter `main`"
    if marker in README_PATH.read_text():
        return
    entry = (
        "\n\n`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE` starts from latest GitHub-visible "
        f"Vexter `main` at merged PR `#74` merge commit `{VERIFIED_VEXTER_COMMIT}` on "
        f"`{VERIFIED_VEXTER_MERGED_AT}`, keeps Dexter pinned at merged PR `#3` commit "
        f"`{VERIFIED_DEXTER_COMMIT}`, and keeps frozen Mew-X at `{VERIFIED_MEWX_COMMIT}`. "
        "It accepts the bounded retry-readiness lane as baseline and promotes one fail-closed "
        "retry gate instead: the repo now fixes the current status/report/proof/handoff/checklist/"
        "decision-surface surfaces for deciding whether retry execution may start, keeps the "
        "Dexter-only `paper_live` seam, leaves Mew-X unchanged on `sim_live`, and keeps funded "
        "live forbidden while holding the lane blocked until every gate input is explicit enough. "
        f"The resulting status is `{TASK_STATUS}` with `{CLAIM_BOUNDARY}`, the blocked current lane "
        f"remains `{NEXT_TASK_LANE}`, and the gate-pass successor is `{PASS_NEXT_TASK_LANE}`."
    )
    README_PATH.write_text(README_PATH.read_text() + entry + "\n")


def main() -> None:
    run_timestamp = iso_utc_now()
    template_env = parse_template_env(TEMPLATE_ENV_PATH)
    previous_proof = read_json(PREVIOUS_PROOF_PATH)
    with patched_demo_env(template_env):
        runtime_config = DexterDemoRuntimeConfig.from_env()
        runtime_errors = list(runtime_config.validation_errors())

    inputs = build_gate_inputs(template_env, runtime_config)
    unresolved_gate_inputs = [
        row["name"] for row in inputs if not row["explicit_enough_for_retry_execution"]
    ]
    checklist_gate = build_gate_checklist(inputs, runtime_errors)

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
            "task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS",
            "task_state": "supervised_run_retry_readiness_blocked",
            "report": str(PREVIOUS_REPORT_PATH.relative_to(ROOT)),
            "status_report": str(PREVIOUS_STATUS_PATH.relative_to(ROOT)),
            "proof": str(PREVIOUS_PROOF_PATH.relative_to(ROOT)),
            "summary": str(PREVIOUS_SUMMARY_PATH.relative_to(ROOT)),
            "handoff": str(PREVIOUS_HANDOFF_PATH.relative_to(ROOT)),
            "checklist": str(PREVIOUS_CHECKLIST_PATH.relative_to(ROOT)),
            "prerequisite_matrix": str(PREVIOUS_MATRIX_PATH.relative_to(ROOT)),
            "subagent_summary": str(PREVIOUS_SUBAGENTS_PATH.relative_to(ROOT)),
        },
        "supervised_run_retry_gate": {
            "planner_boundary": ["prepare", "start", "status", "stop", "snapshot"],
            "retry_gate_boundary": {
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
                "bounded_start_criteria_explicit_required": True,
                "manual_latched_stop_all_visibility_reconfirmation_required": True,
                "terminal_snapshot_readability_reconfirmation_required": True,
                "mewx_unchanged": True,
                "funded_live_forbidden": True,
            },
            "required_artifacts": {
                "current_status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-status.md",
                "current_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-report.md",
                "current_summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md",
                "current_proof_json": "artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json",
                "current_handoff": "artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md",
                "retry_gate_checklist": "docs/demo_forward_supervised_run_retry_gate_checklist.md",
                "retry_gate_decision_surface": "docs/demo_forward_supervised_run_retry_gate_decision_surface.md",
                "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md",
            },
            "baseline_retry_readiness_outcome": {
                "task_id": previous_proof["task_id"],
                "task_state": previous_proof["task_result"]["task_state"],
                "key_finding": previous_proof["task_result"]["key_finding"],
                "claim_boundary": previous_proof["task_result"]["claim_boundary"],
                "recommended_next_step": previous_proof["task_result"]["recommended_next_step"],
            },
            "gate_inputs": {
                "retry_gate_decision_surface": inputs,
                "unresolved_gate_inputs": unresolved_gate_inputs,
                "checklist_gate": checklist_gate,
                "retry_execution_entry_allowed": False,
            },
            "sub_agents": list(SUB_AGENT_SUMMARIES),
            "supporting_files": [
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md",
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md",
                "plans/demo_forward_supervised_run_retry_readiness_plan.md",
                "plans/demo_forward_supervised_run_retry_gate_plan.md",
                "docs/demo_forward_supervised_run_retry_readiness_checklist.md",
                "docs/demo_forward_supervised_run_retry_prerequisite_matrix.md",
                "docs/demo_forward_supervised_run_retry_gate_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_decision_surface.md",
                "scripts/run_demo_forward_supervised_run_retry_readiness.py",
                "scripts/run_demo_forward_supervised_run_retry_gate.py",
                "scripts/build_proof_bundle.sh",
                "tests/test_demo_forward_supervised_run.py",
                "tests/test_demo_forward_supervised_run_retry_readiness.py",
                "tests/test_demo_forward_supervised_run_retry_gate.py",
            ],
            "proof_outputs": [
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json",
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md",
                "artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz",
            ],
        },
        "task_result": {
            "outcome": "FAIL/BLOCKED",
            "key_finding": KEY_FINDING,
            "claim_boundary": CLAIM_BOUNDARY,
            "task_state": TASK_STATUS,
            "recommended_next_step": NEXT_TASK_LANE,
            "recommended_next_task_id": NEXT_TASK_ID,
            "gate_pass_successor": PASS_NEXT_TASK_LANE,
            "gate_pass_successor_task_id": PASS_NEXT_TASK_ID,
            "decision": DECISION,
        },
    }

    report_text = build_current_report(run_timestamp, previous_proof, runtime_config, inputs)
    status_text = build_status()
    proof_summary_text = build_proof_summary()
    summary_text = f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#74` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## What This Task Did

- Accepted retry readiness as the baseline current source of truth.
- Promoted retry gate to the current operator-visible lane.
- Added current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.
- Fixed one fail-closed gate-input model that blocks retry execution until every required face is explicit enough.

## Decision

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task status: `{TASK_STATUS}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Gate-pass successor: `{PASS_NEXT_TASK_LANE}`
- Decision: `{DECISION}`

## Key Paths

- Current spec: `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md`
- Current implementation plan: `plans/demo_forward_supervised_run_retry_gate_plan.md`
- Current checklist: `docs/demo_forward_supervised_run_retry_gate_checklist.md`
- Current decision surface: `docs/demo_forward_supervised_run_retry_gate_decision_surface.md`
- Current proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`
- Current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-report.md`
- Current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md`
- Current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md`
- Current bundle target: `artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz`
"""

    prompt_context = {
        "task_id": TASK_ID,
        "task_state": TASK_STATUS,
        "recommended_next_step": NEXT_TASK_LANE,
        "recommended_next_task_id": NEXT_TASK_ID,
        "candidate_pass_next_step": PASS_NEXT_TASK_LANE,
        "candidate_pass_next_task_id": PASS_NEXT_TASK_ID,
        "verified_vexter_main_pr": VERIFIED_VEXTER_PR,
        "verified_vexter_main_commit": VERIFIED_VEXTER_COMMIT,
        "baseline_task_state": "supervised_run_retry_readiness_blocked",
        "first_demo_target": "dexter_paper_live",
        "source_faithful_seam": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "unresolved_gate_inputs": unresolved_gate_inputs,
        "real_demo_retry_execution_allowed": False,
    }

    details_text = build_details()
    min_prompt_text = build_min_prompt()
    handoff_text = build_handoff(run_timestamp, runtime_config, inputs)
    subagents_text = build_subagents()
    spec_text = build_spec()
    plan_text = build_plan()
    checklist_text = build_checklist()
    decision_surface_text = build_decision_surface(inputs)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts" / "proofs").mkdir(parents=True, exist_ok=True)

    SPEC_PATH.write_text(spec_text)
    PLAN_PATH.write_text(plan_text)
    CHECKLIST_PATH.write_text(checklist_text)
    DECISION_SURFACE_PATH.write_text(decision_surface_text)

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
    SUBAGENT_SUMMARY_PATH.write_text(subagents_text)

    context_pack = read_json(CONTEXT_PATH)
    context_pack["background"] = {
        "previous_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS",
        "previous_task_state": "supervised_run_retry_readiness_blocked",
        "previous_key_finding": "supervised_run_retry_readiness_blocked_on_external_prerequisites",
        "previous_claim_boundary": "supervised_run_retry_readiness_bounded",
        "retry_readiness_accepted_as_baseline": True,
        "retry_gate_promoted_current": True,
    }
    context_pack["bundle_source"] = BUNDLE_SOURCE
    context_pack["current_contract"].update(
        {
            "demo_forward_supervised_run_retry_gate_marker": "demo_forward_supervised_run_retry_gate",
            "demo_forward_supervised_run_retry_gate_spec_path": "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md",
            "demo_forward_supervised_run_retry_gate_plan_path": "plans/demo_forward_supervised_run_retry_gate_plan.md",
            "demo_forward_supervised_run_retry_gate_checklist_path": "docs/demo_forward_supervised_run_retry_gate_checklist.md",
            "demo_forward_supervised_run_retry_gate_decision_surface_path": "docs/demo_forward_supervised_run_retry_gate_decision_surface.md",
            "demo_forward_supervised_run_retry_gate_subagents_path": "artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md",
            "demo_forward_supervised_run_retry_gate_subagent_summary_path": "artifacts/reports/demo-forward-supervised-run-retry-gate/subagent_summary.md",
            "demo_forward_retry_gate_current_lane": NEXT_TASK_LANE,
            "demo_forward_retry_gate_pass_successor": PASS_NEXT_TASK_LANE,
        }
    )
    context_pack["current_task"] = {
        "id": TASK_ID,
        "scope": [
            "Reverify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X after retry readiness merged.",
            "Accept retry readiness as baseline current source of truth.",
            "Promote retry gate status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Bound each required gate input with a repo-visible marker, current observation, confirmer, and pass condition.",
            "Keep retry execution blocked until every gate input is explicit enough.",
        ],
        "deliverables": [
            "README.md",
            "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md",
            "plans/demo_forward_supervised_run_retry_gate_plan.md",
            "docs/demo_forward_supervised_run_retry_gate_checklist.md",
            "docs/demo_forward_supervised_run_retry_gate_decision_surface.md",
            "tests/test_demo_forward_supervised_run_retry_gate.py",
            "tests/test_demo_forward_supervised_run_retry_readiness.py",
            "tests/test_demo_forward_supervised_run.py",
            "tests/test_bootstrap_layout.py",
            "scripts/run_demo_forward_supervised_run_retry_gate.py",
            "scripts/build_proof_bundle.sh",
            "artifacts/summary.md",
            "artifacts/context_pack.json",
            "artifacts/proof_bundle_manifest.json",
            "artifacts/task_ledger.jsonl",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-report.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-status.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate/DETAILS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate/MIN_PROMPT.txt",
            "artifacts/reports/demo-forward-supervised-run-retry-gate/CONTEXT.json",
            "artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate/subagent_summary.md",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md",
            "artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz",
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
            "latest_recent_vexter_prs": [74, 73, 72, 71, 70],
            "vexter_pr_74_merged_at": VERIFIED_VEXTER_MERGED_AT,
            "vexter_pr_74_closed_at": VERIFIED_VEXTER_MERGED_AT,
        }
    )
    context_pack["evidence"]["demo_forward_supervised_run_retry_gate"] = {
        "report": "artifacts/reports/demo-forward-supervised-run-retry-gate-report.md",
        "status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-status.md",
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json",
        "summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md",
        "handoff_dir": "artifacts/reports/demo-forward-supervised-run-retry-gate",
        "checklist": "docs/demo_forward_supervised_run_retry_gate_checklist.md",
        "decision_surface": "docs/demo_forward_supervised_run_retry_gate_decision_surface.md",
        "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md",
        "key_finding": KEY_FINDING,
        "claim_boundary": CLAIM_BOUNDARY,
        "task_state": TASK_STATUS,
        "run_outcome": "FAIL/BLOCKED",
        "operator_visible_gate_surface_current": True,
        "preferred_next_step": NEXT_TASK_LANE,
        "gate_pass_successor": PASS_NEXT_TASK_LANE,
        "retry_gate_boundary": proof["supervised_run_retry_gate"]["retry_gate_boundary"],
        "unresolved_gate_inputs": unresolved_gate_inputs,
        "sub_agents": list(SUB_AGENT_SUMMARIES),
    }
    context_pack["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "rationale": [
            "Retry readiness is accepted as baseline and retry gate is now current.",
            "One or more gate inputs remain unresolved or not explicit enough in repo-visible form.",
            "Hold retry execution closed until the gate passes.",
        ],
        "pass_successor": {
            "id": PASS_NEXT_TASK_ID,
            "state": PASS_NEXT_TASK_STATE,
            "lane": PASS_NEXT_TASK_LANE,
        },
    }
    context_pack["proofs"].update(
        {
            "demo_forward_supervised_run_retry_gate_added": True,
            "demo_forward_retry_gate_current_pointers_fixed": True,
            "demo_forward_retry_gate_checklist_written": True,
            "demo_forward_retry_gate_decision_surface_written": True,
            "demo_forward_retry_gate_subagent_summary_written": True,
            "recommended_next_step_stays_supervised_run_retry_gate_when_blocked": True,
            "retry_execution_requires_gate_pass": True,
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
        ("docs", "docs/demo_forward_supervised_run_retry_gate_checklist.md"),
        ("docs", "docs/demo_forward_supervised_run_retry_gate_decision_surface.md"),
        ("scripts", "scripts/run_demo_forward_supervised_run_retry_gate.py"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-report.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-status.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate/subagent_summary.md"),
    ):
        if path not in manifest[key]:
            manifest[key].append(path)
    for path in (
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md",
        "plans/demo_forward_supervised_run_retry_gate_plan.md",
        "tests/test_demo_forward_supervised_run_retry_gate.py",
        "artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz",
    ):
        if path not in manifest["included_paths"]:
            manifest["included_paths"].append(path)
    manifest["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "resume_requirements": [
            f"Keep Dexter pinned at {VERIFIED_DEXTER_COMMIT} and Mew-X frozen at {VERIFIED_MEWX_COMMIT}.",
            "Start from the current retry-gate status, report, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Do not enter retry execution until every gate input is explicit enough.",
            "Keep the planner boundary at prepare / start / status / stop / snapshot and preserve poll_first plus manual_latched_stop_all.",
            "Do not introduce funded live or a Mew-X real-demo path.",
        ],
        "pass_successor": {
            "id": PASS_NEXT_TASK_ID,
            "state": PASS_NEXT_TASK_STATE,
            "lane": PASS_NEXT_TASK_LANE,
        },
    }
    manifest["proofs"].update(
        {
            "demo_forward_supervised_run_retry_gate_added": True,
            "demo_forward_retry_gate_current_pointers_fixed": True,
            "demo_forward_retry_gate_checklist_written": True,
            "demo_forward_retry_gate_decision_surface_written": True,
            "demo_forward_retry_gate_subagent_summary_written": True,
            "recommended_next_step_stays_supervised_run_retry_gate_when_blocked": True,
            "retry_execution_requires_gate_pass": True,
        }
    )
    MANIFEST_PATH.write_text(format_json(manifest))

    ledger_payload = {
        "artifact_bundle": BUNDLE_PATH,
        "base_main": VERIFIED_VEXTER_COMMIT,
        "baseline_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS",
        "baseline_task_state": "supervised_run_retry_readiness_blocked",
        "branch": git_output("branch", "--show-current"),
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": DECISION,
        "first_demo_target": "dexter_paper_live",
        "gate_pass_successor": PASS_NEXT_TASK_ID,
        "key_finding": KEY_FINDING,
        "next_task_id": NEXT_TASK_ID,
        "next_task_state": NEXT_TASK_STATE,
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json",
        "recommended_next_lane": NEXT_TASK_LANE,
        "repo": "https://github.com/Cabbala/Vexter",
        "retry_gate_input_count": len(inputs),
        "retry_gate_unresolved_input_count": len(unresolved_gate_inputs),
        "selected_outcome": "FAIL/BLOCKED",
        "source_faithful_modes": {"dexter": "paper_live", "mewx": "sim_live"},
        "status": TASK_STATUS,
        "sub_agents_used": [item["name"] for item in SUB_AGENT_SUMMARIES],
        "supporting_vexter_prs": [74, 73, 72, 71, 70],
        "task_id": TASK_ID,
        "template_runtime_validation_errors": runtime_errors,
        "verified_dexter_main_commit": VERIFIED_DEXTER_COMMIT,
        "verified_dexter_pr": 3,
        "verified_mewx_frozen_commit": VERIFIED_MEWX_COMMIT,
        "verified_prs": [74, 73, 72],
        "date": run_timestamp.split("T", 1)[0],
    }
    rewrite_local_ledger(ledger_payload)

    update_readme()


if __name__ == "__main__":
    main()
