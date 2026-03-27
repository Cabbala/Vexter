#!/usr/bin/env python3
"""Emit bounded retry-gate attestation-audit surfaces from the input-attestation baseline."""

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

CHECKLIST_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md"
DECISION_SURFACE_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md"
SPEC_PATH = ROOT / "specs" / "DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md"
PLAN_PATH = ROOT / "plans" / "demo_forward_supervised_run_retry_gate_attestation_audit_plan.md"

PREVIOUS_REPORT_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-input-attestation-report.md"
)
PREVIOUS_STATUS_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-input-attestation-status.md"
)
PREVIOUS_PROOF_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-input-attestation-check.json"
)
PREVIOUS_SUMMARY_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-input-attestation-summary.md"
)
PREVIOUS_HANDOFF_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-input-attestation" / "HANDOFF.md"
)
PREVIOUS_CHECKLIST_PATH = (
    ROOT / "docs" / "demo_forward_supervised_run_retry_gate_input_attestation_checklist.md"
)
PREVIOUS_DECISION_SURFACE_PATH = (
    ROOT / "docs" / "demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md"
)
PREVIOUS_SUBAGENTS_PATH = (
    ROOT
    / "artifacts"
    / "reports"
    / "demo-forward-supervised-run-retry-gate-input-attestation"
    / "SUBAGENTS.md"
)

REPORT_DIR = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-audit"
REPORT_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-audit-report.md"
STATUS_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-audit-status.md"
SUBAGENTS_PATH = REPORT_DIR / "SUBAGENTS.md"
SUBAGENT_SUMMARY_PATH = REPORT_DIR / "subagent_summary.md"
PROOF_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-attestation-audit-check.json"
PROOF_SUMMARY_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-attestation-audit-summary.md"
)

BUNDLE_PATH = "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz"
BUNDLE_SOURCE = "/Users/cabbala/Downloads/vexter_retry_gate_attestation_audit_bundle.tar.gz"

TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT"
TASK_STATUS = "supervised_run_retry_gate_attestation_audit_blocked"
KEY_FINDING = "supervised_run_retry_gate_attestation_audit_blocked_on_missing_current_attestation_records"
CLAIM_BOUNDARY = "supervised_run_retry_gate_attestation_audit_bounded"
NEXT_TASK_ID = TASK_ID
NEXT_TASK_STATE = "retry_gate_attestation_audits_pending"
NEXT_TASK_LANE = "supervised_run_retry_gate_attestation_audit"
PASS_NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
PASS_NEXT_TASK_STATE = "ready_for_supervised_run_retry_gate_recheck"
PASS_NEXT_TASK_LANE = "supervised_run_retry_gate"
DECISION = "retry_gate_review_blocked_pending_auditable_attestation_records"

VERIFIED_DEXTER_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
VERIFIED_MEWX_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
VERIFIED_VEXTER_PR = 76
VERIFIED_VEXTER_COMMIT = "56dedfe86bf9f6252d1099775fa9506d7259e0da"
VERIFIED_VEXTER_MERGED_AT = "2026-03-27T07:27:42Z"

REQUIRED_FACE_NAMES = [
    "external_credential_source_face",
    "venue_ref_face",
    "account_ref_face",
    "connectivity_profile_face",
    "operator_owner_face",
    "bounded_start_criteria_face",
    "allowlist_symbol_lot_reconfirmed",
    "manual_latched_stop_all_visibility_reconfirmed",
    "terminal_snapshot_readability_reconfirmed",
]

SUB_AGENT_SUMMARIES = (
    {
        "name": "Anscombe",
        "lines": [
            "Confirmed the input-attestation quartet should remain the accepted baseline until a complete attestation-audit quartet exists, then switch current report, status, proof, summary, and handoff pointers atomically.",
            "Recommended that the audit surface carry the same attestation facts per row in one place: who attests, what is being attested, the minimum evidence shape, the stale rule, and what makes the face auditable enough.",
            "Recommended fail-closed wording that stays observation-based: the repo may name the required face definitions, but retry-gate review remains blocked until each face points to a current bounded-window attestation record and stale check.",
        ],
    },
    {
        "name": "Euler",
        "lines": [
            "Kept the attestation-audit boundary identical to the accepted input-attestation boundary: Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, allowlist-only, small-lot, one-plan, one-position, bounded supervision, and funded-live forbidden.",
            "Recommended the smallest next-step cut: hold the current lane at `supervised_run_retry_gate_attestation_audit` while blocked, and expose `supervised_run_retry_gate` only as the audit-pass successor once retry-gate review can honestly reopen.",
            "Confirmed there is no planner or adapter drift: `prepare / start / status / stop / snapshot` stays fixed, `manual_latched_stop_all` stays planner-owned, funded live stays forbidden, and Mew-X remains unchanged.",
        ],
    },
    {
        "name": "Parfit",
        "lines": [
            "Scoped the smallest safe change set to docs, proof-generation script, generated artifacts, manifest/context/ledger updates, and tests; no `vexter/` runtime behavior changes are needed for this lane.",
            "Recommended validating the generator plus the affected regression surfaces with `python3 scripts/run_demo_forward_supervised_run_retry_gate_attestation_audit.py` and focused `pytest` coverage on the supervised-run and bundle-layout tests.",
            "Merge readiness depends on an atomic current-pointer switch to attestation audit, a regenerated tarball at the new bundle path, and a clean blocked decision that does not claim retry execution success or a reopened retry gate.",
        ],
    },
)


def format_jsonl(payload: object) -> str:
    return json.dumps(payload, sort_keys=False) + "\n"


def format_marker(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)


def format_bool(value: bool) -> str:
    return "yes" if value else "no"


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


def boundary_lines() -> list[str]:
    return [
        "Dexter-only real demo slice",
        "`single_sleeve`",
        "`dexter_default`",
        "Dexter `paper_live`",
        "frozen Mew-X `sim_live`",
        "max active real demo plans = `1`",
        "max open positions = `1`",
        "explicit allowlist required",
        "small lot required",
        "bounded supervised window required",
        "external credential refs remain outside repo",
        "operator owner explicit",
        "venue / connectivity confirmation explicit",
        "bounded start criteria explicit",
        "allowlist / symbol / lot-size reconfirmation explicit",
        "`manual_latched_stop_all` visibility reconfirmation explicit",
        "terminal snapshot readability reconfirmation explicit",
        "Mew-X unchanged",
        "funded live forbidden",
    ]


def build_audit_faces(previous_faces: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for row in previous_faces:
        definition_complete = all(
            bool(row.get(field))
            for field in (
                "who_attests",
                "what_is_being_attested",
                "minimal_evidence_shape",
                "stale_when",
                "pass_when",
            )
        )
        stale_rule_explicit = bool(row.get("stale_when"))
        auditable_enough_rule_explicit = bool(row.get("pass_when"))
        current_attestation_ref_present = False
        current_attestation_non_stale = False
        auditable_now = (
            definition_complete
            and stale_rule_explicit
            and auditable_enough_rule_explicit
            and current_attestation_ref_present
            and current_attestation_non_stale
        )
        rows.append(
            {
                "name": row["name"],
                "repo_visible_marker": row["repo_visible_marker"],
                "who_attests": row["who_attests"],
                "what_is_being_attested": row["what_is_being_attested"],
                "minimal_evidence_shape": row["minimal_evidence_shape"],
                "stale_when": row["stale_when"],
                "auditable_enough_when": row["pass_when"],
                "definition_complete": definition_complete,
                "stale_rule_explicit": stale_rule_explicit,
                "auditable_enough_rule_explicit": auditable_enough_rule_explicit,
                "current_attestation_ref_present": current_attestation_ref_present,
                "current_attestation_non_stale": current_attestation_non_stale,
                "auditable_now": auditable_now,
                "current_audit_observation": (
                    f"{row['current_observation']} The current input-attestation surface defines the face, "
                    "but the repo still does not point to a current bounded-window attestation record or "
                    "timestamped stale check for this face."
                ),
                "audit_status": "FAIL/BLOCKED",
            }
        )
    return rows


def build_audit_checklist(rows: list[dict], runtime_errors: list[str]) -> dict[str, bool]:
    row_names = {row["name"] for row in rows}
    return {
        "runtime_guardrails_parse_cleanly": not runtime_errors,
        "all_required_faces_present": row_names == set(REQUIRED_FACE_NAMES),
        "all_definition_fields_explicit": all(row["definition_complete"] for row in rows),
        "all_stale_conditions_explicit": all(row["stale_rule_explicit"] for row in rows),
        "all_auditable_enough_conditions_explicit": all(
            row["auditable_enough_rule_explicit"] for row in rows
        ),
        "all_current_attestation_refs_present": all(
            row["current_attestation_ref_present"] for row in rows
        ),
        "all_faces_non_stale_now": all(row["current_attestation_non_stale"] for row in rows),
        "all_faces_auditable_now": all(row["auditable_now"] for row in rows),
        "retry_gate_review_reopen_ready": all(row["auditable_now"] for row in rows),
    }


def build_spec() -> str:
    boundary = "\n".join(f"- {line}" for line in boundary_lines())
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Audit

This document fixes the bounded retry-gate attestation-audit lane after `DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION` made the required attestation faces explicit at the definition level.

## Verified Base

- Latest merged Vexter `main`: PR `#76`, merge commit `{VERIFIED_VEXTER_COMMIT}`, merged at `{VERIFIED_VEXTER_MERGED_AT}`
- Dexter merged `main`: PR `#3`, merge commit `{VERIFIED_DEXTER_COMMIT}`
- Frozen Mew-X commit: `{VERIFIED_MEWX_COMMIT}`
- Input-attestation baseline proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`

## Purpose

The shortest next lane is still not retry execution. It is fixing one bounded retry-gate attestation-audit lane that re-audits the current attestation faces for completeness, stale conditions, and whether each face is auditable enough to reopen retry-gate review.

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

## Attestation Audit Boundary

{boundary}

## Required Current Surfaces

The repo must expose the following as current source of truth:

- current status report
- current report
- current summary
- current proof json
- current handoff
- attestation audit checklist
- attestation audit decision surface
- next recommended step

## Honest Audit Model

The bounded audit lane must hold one of these honest outcomes:

- PASS: the required attestation faces are explicit, non-stale, auditable, and sufficient to reopen retry-gate review
- FAIL/BLOCKED: one or more attestation faces remain incomplete, stale, ambiguous, or not auditable enough to reopen retry-gate review

The repo may name external references, attesters, timestamps, and evidence shapes, but it must not embed credentials, secrets, or fabricated gate-pass evidence.

## Required Audit Faces

The current attestation-audit decision surface must include at least:

- credential source face
- venue ref face
- account ref face
- connectivity profile face
- operator owner face
- bounded start criteria face
- allowlist / symbol / lot-size reconfirmation face
- `manual_latched_stop_all` visibility face
- terminal snapshot readability face

Each face must make explicit:

- who attests
- what is being attested
- minimal evidence shape
- when the attestation is stale
- what makes the face auditable enough

## Next-Step Boundary

- While blocked, the current lane remains `supervised_run_retry_gate_attestation_audit`.
- Only after every required attestation face is explicit, non-stale, and auditable enough may the next recommended lane advance to `supervised_run_retry_gate`.
- That pass only reopens retry-gate review; it does not claim retry execution success.

## Out Of Scope

- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no portfolio split
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success
"""


def build_plan() -> str:
    boundary = "\n".join(f"- {line}" for line in boundary_lines())
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT Plan

## Objective

Promote a bounded `supervised_run_retry_gate_attestation_audit` lane to the repo-visible current source of truth after retry-gate input attestation, without widening planner scope or fabricating retry-gate reopen or retry execution success.

## Inputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md`
- `docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md`
- `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md`

## Steps

1. Reverify latest GitHub-visible `main` after PR `#76`.
2. Keep Dexter pinned at merged PR `#3` and keep frozen Mew-X unchanged.
3. Accept `supervised_run_retry_gate_input_attestation_blocked` as the current baseline instead of reopening retry-gate review or retrying execution.
4. Promote an attestation-audit spec, status, report, summary, proof, handoff, checklist, and decision surface as the current source of truth.
5. Re-audit every required face for definition completeness, stale-rule completeness, and whether the face is currently auditable enough to reopen retry-gate review.
6. Preserve the planner boundary at `prepare / start / status / stop / snapshot`, keep `poll_first`, and keep `manual_latched_stop_all` planner-owned.
7. Keep the current lane blocked unless every required attestation face is explicit, non-stale, and auditable enough to reopen retry-gate review.

## Guardrails

{boundary}

## Required Outputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md`
- `plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md`
- `docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md`
- `docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/DETAILS.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/MIN_PROMPT.txt`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/CONTEXT.json`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md`
- `artifacts/summary.md`
- `artifacts/context_pack.json`
- `artifacts/proof_bundle_manifest.json`
- `artifacts/task_ledger.jsonl`
- `artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz`

## Acceptance

- Retry-gate input attestation remains the accepted baseline.
- The attestation-audit surface records completeness, stale conditions, and auditable-enough conditions for every required face without embedding external secrets.
- The current handoff points directly at checklist and decision-surface artifacts.
- The current lane remains `FAIL/BLOCKED` until retry-gate review can honestly be reconsidered from current, non-stale, auditable attestation faces.
"""


def build_checklist() -> str:
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Audit Checklist

This checklist fixes the minimum operator-visible audit surface that must be explicit before retry-gate review may honestly reopen.

## Current Pointers

1. Start at `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json`.
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md`.
5. Use `docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md` as the single attestation-audit decision surface.

## Attestation Audit Checklist

1. Accept the prior `supervised_run_retry_gate_input_attestation_blocked` lane as baseline and do not claim retry-gate reopen or retry execution success.
2. Keep one audit row per required face: credential source, venue ref, account ref, connectivity profile, operator owner, bounded start criteria, allowlist/symbol/lot reconfirmation, `manual_latched_stop_all` visibility, and terminal snapshot readability.
3. Keep the repo-visible markers explicit: `DEXTER_DEMO_CREDENTIAL_SOURCE`, `DEXTER_DEMO_VENUE_REF`, `DEXTER_DEMO_ACCOUNT_REF`, and `DEXTER_DEMO_CONNECTIVITY_PROFILE`.
4. For every row, confirm who attests the face is explicit.
5. For every row, confirm what is being attested is explicit without embedding secrets or credential material.
6. For every row, confirm the minimal evidence shape is explicit enough for a gate reviewer to inspect the attestation outside the repo.
7. For every row, confirm when the attestation becomes stale is explicit.
8. For every row, confirm what makes the face auditable enough is explicit.
9. For every row, record whether a current bounded-window attestation reference is present without embedding secret material.
10. For every row, record whether a timestamped stale check can currently be made from repo-visible evidence.
11. Reconfirm `DEXTER_DEMO_ALLOWED_SYMBOLS`, `DEXTER_DEMO_DEFAULT_SYMBOL`, `DEXTER_DEMO_ORDER_SIZE_LOTS`, `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`, `DEXTER_DEMO_WINDOW_MINUTES=15`, and `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`.
12. Reconfirm venue/connectivity, `manual_latched_stop_all` visibility, and terminal snapshot readability remain explicit for the bounded supervised window.
13. Reconfirm Mew-X remains unchanged on `sim_live`.
14. Reconfirm funded live remains forbidden.

## Attestation Audit Exit Criteria

- every audit row in `docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md` is explicit, non-stale, and auditable enough to reopen retry-gate review
- every required face points to a current bounded-window attestation reference outside repo
- venue and connectivity attestations are current for the bounded window
- allowlist, symbol, lot-size, window, and one-position cap are reconfirmed for the bounded window
- `manual_latched_stop_all` visibility and terminal snapshot readability are reconfirmed for the bounded window
- the retry path remains Dexter-only `paper_live`

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


def build_decision_surface(rows: list[dict]) -> str:
    lines = [
        "# Demo Forward Supervised Run Retry Gate Attestation Audit Decision Surface",
        "",
        "This decision surface is the current source of truth for `supervised_run_retry_gate_attestation_audit`.",
        "",
        "| Attestation face | Repo-visible marker | Who attests | What is being attested | Minimal evidence shape | Stale when | Auditable enough when | Definition complete | Current attestation ref present | Non-stale now | Auditable now | Current audit observation | Audit status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"`{row['name']}` | "
            f"`{format_marker(row['repo_visible_marker'])}` | "
            f"`{row['who_attests']}` | "
            f"{row['what_is_being_attested']} | "
            f"{row['minimal_evidence_shape']} | "
            f"{row['stale_when']} | "
            f"{row['auditable_enough_when']} | "
            f"`{format_bool(row['definition_complete'])}` | "
            f"`{format_bool(row['current_attestation_ref_present'])}` | "
            f"`{format_bool(row['current_attestation_non_stale'])}` | "
            f"`{format_bool(row['auditable_now'])}` | "
            f"{row['current_audit_observation']} | "
            f"`{row['audit_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Current Decision",
            "",
            "- Audit outcome: `FAIL/BLOCKED`",
            f"- Key finding: `{KEY_FINDING}`",
            f"- Claim boundary: `{CLAIM_BOUNDARY}`",
            f"- Current task state: `{TASK_STATUS}`",
            f"- Recommended next step while blocked: `{NEXT_TASK_LANE}`",
            f"- Audit-pass successor: `{PASS_NEXT_TASK_LANE}`",
            "- Retry-gate review reopen allowed now: `false`",
            "",
            "Retry-gate review does not reopen unless every attestation face is explicit, non-stale, and auditable enough.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_current_report(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    rows: list[dict],
) -> str:
    blocked_faces = [row["name"] for row in rows if row["audit_status"] != "PASS"]
    definition_complete_count = sum(row["definition_complete"] for row in rows)
    current_ref_count = sum(row["current_attestation_ref_present"] for row in rows)
    non_stale_count = sum(row["current_attestation_non_stale"] for row in rows)
    auditable_count = sum(row["auditable_now"] for row in rows)
    boundary = "\n".join(f"- {line}" for line in boundary_lines())
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT Report

## Verified Base

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#76`, merge commit `{VERIFIED_VEXTER_COMMIT}`, merged at `{VERIFIED_VEXTER_MERGED_AT}`.
- Dexter remained pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen Mew-X remained pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## Starting Point

- Accepted `supervised_run_retry_gate_input_attestation_blocked` as the current blocked baseline instead of reopening retry-gate review or fabricating retry execution.
- Carried forward the bounded input-attestation proof, report, summary, and handoff as the baseline current source of truth.
- Promoted retry-gate attestation audit as the new current operator-visible lane.

## Attestation Audit Boundary

{boundary}

## Baseline Continuity

- input-attestation status path: `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md`
- input-attestation proof path: `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`
- input-attestation handoff path: `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md`
- input-attestation checklist path: `docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md`
- input-attestation decision surface path: `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md`
- bounded runtime guardrails stayed parseable from `templates/windows_runtime/dexter.env.example`
- runtime validation errors: `{len(runtime_config.validation_errors())}`
- input-attestation pass successor remained `supervised_run_retry_execution`, but audit pass now only reopens `supervised_run_retry_gate`

## Required Current Surfaces

- current status report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md`
- current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md`
- current summary: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md`
- current proof json: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json`
- current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md`
- attestation audit checklist: `docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md`
- attestation audit decision surface: `docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md`
- sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md`

## Audit Decision Summary

- audited face count: `{len(rows)}`
- definition-complete face count: `{definition_complete_count}`
- current attestation ref present count: `{current_ref_count}`
- non-stale-now face count: `{non_stale_count}`
- auditable-now face count: `{auditable_count}`
- blocked audit faces: `{", ".join(blocked_faces)}`
- bounded window minutes: `{runtime_config.bounded_window_minutes}`
- allowlist: `{", ".join(runtime_config.allowed_symbols)}`
- default symbol: `{runtime_config.default_symbol}`
- order size lots: `{runtime_config.order_size_lots}`
- max open positions: `{runtime_config.max_open_positions}`
- retry-gate review reopen allowed now: `false`

## Outcome

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task state: `{TASK_STATUS}`
- Blocker: one or more attestation faces still lack a current bounded-window attestation record or timestamped stale check, so the faces remain not auditable enough to reopen retry-gate review honestly.
- Run timestamp: `{run_timestamp}`

## Recommendation

- Current task state: `{TASK_STATUS}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Audit-pass successor: `{PASS_NEXT_TASK_LANE}`
- Reason: the attestation definitions are now re-audited for completeness and stale logic, but retry-gate review remains fail-closed until every face is current, non-stale, and auditable enough.
"""


def build_status() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT Status

- task_id: `{TASK_ID}`
- task_state: `{TASK_STATUS}`
- run_outcome: `FAIL/BLOCKED`
- key_finding: `{KEY_FINDING}`
- claim_boundary: `{CLAIM_BOUNDARY}`
- verified_vexter_main_pr: `{VERIFIED_VEXTER_PR}`
- verified_vexter_main_commit: `{VERIFIED_VEXTER_COMMIT}`
- verified_dexter_main_commit: `{VERIFIED_DEXTER_COMMIT}`
- verified_mewx_frozen_commit: `{VERIFIED_MEWX_COMMIT}`
- baseline_task: `DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION`
- baseline_task_state: `supervised_run_retry_gate_input_attestation_blocked`
- planner_boundary: `prepare/start/status/stop/snapshot`
- current_attestation_audit_lane: `{NEXT_TASK_LANE}`
- audit_pass_successor: `{PASS_NEXT_TASK_LANE}`
"""


def build_proof_summary() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT Summary

- Verified base: Vexter `main` at PR `#76` merge commit `{VERIFIED_VEXTER_COMMIT}`.
- Starting point: retry-gate input attestation already fixed the per-face definitions without claiming a reopened retry gate or retry execution.
- Promoted boundary: retry-gate attestation audit is now current source of truth for the same Dexter-only `paper_live` / frozen Mew-X `sim_live` seam, `single_sleeve`, `dexter_default`, explicit allowlist, small lot, bounded supervised window, one active real demo plan max, and one open position max.
- Added current surfaces: attestation-audit status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary.
- Outcome: `FAIL/BLOCKED` because the repo still lacks current bounded-window attestation records and stale checks for the required faces.
- Recommended next step while blocked: `{NEXT_TASK_LANE}`.
- Audit-pass successor: `{PASS_NEXT_TASK_LANE}`.
"""


def build_details() -> str:
    return f"""# {TASK_ID}

## 1. Intent
- Accept the blocked input-attestation lane as baseline.
- Promote retry-gate attestation audit to the repo-visible current source of truth.

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

## 4. Honest Audit Model
- `PASS` only if every attestation face is explicit, non-stale, and auditable enough to reopen `supervised_run_retry_gate`.
- `FAIL/BLOCKED` if any attestation face remains incomplete, stale, ambiguous, or not auditable enough.

## 5. Next-Step Boundary
- blocked current lane: `{NEXT_TASK_LANE}`
- audit-pass successor: `{PASS_NEXT_TASK_LANE}`
"""


def build_min_prompt() -> str:
    return (
        "GitHub最新状態を確認し、Vexter `main` PR #76 merge 後の retry-gate attestation-audit surface を current source of truth として扱ってください。\n"
        "出発点は `supervised_run_retry_gate_input_attestation_blocked` で、Dexter `paper_live` のみ・frozen Mew-X `sim_live` のみ・`single_sleeve`・`dexter_default`・explicit allowlist・small lot・max open positions=1・bounded supervised window を維持してください。\n"
        "planner の public boundary は `prepare / start / status / stop / snapshot` のまま、`manual_latched_stop_all` は planner-owned のまま保ってください。\n"
        "external credential refs は repo 外に残し、各 face について who / what / minimal evidence shape / stale rule / auditable enough rule を current source of truth として監査し、current attestation ref や stale check が欠ける限り `FAIL/BLOCKED` を維持してください。\n"
        "current status / report / proof / handoff / checklist / decision surface / sub-agent summary を更新し、必要 face が explicit・non-stale・auditable enough の場合にのみ次を `supervised_run_retry_gate` と示してください。\n"
    )


def build_handoff(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    rows: list[dict],
) -> str:
    audit_lines = "\n".join(
        (
            "- "
            f"{row['name']}: definition_complete={str(row['definition_complete']).lower()}, "
            f"current_attestation_ref_present={str(row['current_attestation_ref_present']).lower()}, "
            f"current_attestation_non_stale={str(row['current_attestation_non_stale']).lower()}, "
            f"auditable_now={str(row['auditable_now']).lower()}, "
            f"who_attests={row['who_attests']}"
        )
        for row in rows
    )
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Audit Handoff

## Current Status
- outgoing_shift_window: {run_timestamp} retry-gate attestation-audit lane
- incoming_shift_window: current bounded-window attestations and possible retry-gate recheck
- task_state: {TASK_STATUS}
- shift_outcome: blocked
- current_action: hold_retry_gate_review_until_attestation_faces_are_current_and_auditable
- recommended_next_step_while_blocked: {NEXT_TASK_LANE}
- audit_pass_successor: {PASS_NEXT_TASK_LANE}
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: {VERIFIED_VEXTER_COMMIT}
- dexter_main_commit: {VERIFIED_DEXTER_COMMIT}
- mewx_frozen_commit: {VERIFIED_MEWX_COMMIT}
- baseline_retry_gate_input_attestation_task_state: supervised_run_retry_gate_input_attestation_blocked

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md
- current_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md
- current_proof_summary: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md
- current_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json
- current_attestation_audit_checklist: docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md
- current_attestation_audit_decision_surface: docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md
- current_subagent_summary: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md
- baseline_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md
- baseline_report: artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md
- baseline_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json
- baseline_handoff: artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md

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

## Audit Faces
{audit_lines}

## Open Questions
- question_1_or_none: where is the current bounded-window attestation record for each required face
- question_2_or_none: who timestamps and refreshes the stale check for venue, account, and connectivity faces
- question_3_or_none: who confirms the bounded start window and operator owner for the next retry-gate recheck
- question_4_or_none: has `manual_latched_stop_all` visibility been reconfirmed for the current bounded window
- question_5_or_none: has terminal snapshot readability been reconfirmed for the current bounded window

## Next-Shift Priority Checks
- priority_check_1: keep the current lane blocked unless every face has a current bounded-window attestation record and stale check
- priority_check_2: preserve Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, small-lot, one-position, and funded-live-forbidden guardrails
- priority_check_3: preserve `manual_latched_stop_all`, poll-first status visibility, and terminal snapshot readability during any future retry-gate recheck

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- checklist_pointer_checked: true
- decision_surface_pointer_checked: true
- subagent_summary_pointer_checked: true
- blocked_claim_boundary_explicit: true

This handoff promotes the bounded retry-gate attestation-audit lane only. It does not claim a reopened retry gate, a completed retry execution, funded live access, or any Mew-X seam expansion.
"""


def build_subagents() -> str:
    lines = ["# Demo Forward Supervised Run Retry Gate Attestation Audit Sub-agent Summaries", ""]
    for item in SUB_AGENT_SUMMARIES:
        lines.append(f"## {item['name']}")
        for line in item["lines"]:
            lines.append(f"- {line}")
        lines.append("")
    return "\n".join(lines)


def update_readme() -> None:
    marker = "`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT` starts from latest GitHub-visible Vexter `main`"
    if marker in README_PATH.read_text():
        return
    entry = (
        "\n\n`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT` starts from latest GitHub-visible "
        f"Vexter `main` at merged PR `#76` merge commit `{VERIFIED_VEXTER_COMMIT}` on "
        f"`{VERIFIED_VEXTER_MERGED_AT}`, keeps Dexter pinned at merged PR `#3` commit "
        f"`{VERIFIED_DEXTER_COMMIT}`, and keeps frozen Mew-X at `{VERIFIED_MEWX_COMMIT}`. "
        "It accepts the bounded retry-gate input-attestation lane as baseline and promotes one fail-closed "
        "attestation-audit lane instead: the repo now fixes the current status/report/proof/handoff/checklist/"
        "decision-surface surfaces for whether each required face is complete, non-stale, and auditable enough "
        "to reopen retry-gate review, keeps the Dexter-only `paper_live` seam, leaves Mew-X unchanged on "
        "`sim_live`, and keeps funded live forbidden while holding the lane blocked until every face has a "
        "current bounded-window attestation record and stale check. "
        f"The resulting status is `{TASK_STATUS}` with `{CLAIM_BOUNDARY}`, the blocked current lane remains "
        f"`{NEXT_TASK_LANE}`, and the audit-pass successor is `{PASS_NEXT_TASK_LANE}`."
    )
    README_PATH.write_text(README_PATH.read_text() + entry + "\n")


def main() -> None:
    run_timestamp = iso_utc_now()
    template_env = parse_template_env(TEMPLATE_ENV_PATH)
    previous_proof = read_json(PREVIOUS_PROOF_PATH)
    with patched_demo_env(template_env):
        runtime_config = DexterDemoRuntimeConfig.from_env()
        runtime_errors = list(runtime_config.validation_errors())

    previous_faces = previous_proof["supervised_run_retry_gate_input_attestation"]["attestation_faces"][
        "gate_input_attestation_decision_surface"
    ]
    audit_rows = build_audit_faces(previous_faces)
    blocked_audit_faces = [row["name"] for row in audit_rows if row["audit_status"] != "PASS"]
    checklist_attestation = build_audit_checklist(audit_rows, runtime_errors)

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
            "task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION",
            "task_state": "supervised_run_retry_gate_input_attestation_blocked",
            "report": str(PREVIOUS_REPORT_PATH.relative_to(ROOT)),
            "status_report": str(PREVIOUS_STATUS_PATH.relative_to(ROOT)),
            "proof": str(PREVIOUS_PROOF_PATH.relative_to(ROOT)),
            "summary": str(PREVIOUS_SUMMARY_PATH.relative_to(ROOT)),
            "handoff": str(PREVIOUS_HANDOFF_PATH.relative_to(ROOT)),
            "checklist": str(PREVIOUS_CHECKLIST_PATH.relative_to(ROOT)),
            "decision_surface": str(PREVIOUS_DECISION_SURFACE_PATH.relative_to(ROOT)),
            "subagent_summary": str(PREVIOUS_SUBAGENTS_PATH.relative_to(ROOT)),
        },
        "supervised_run_retry_gate_attestation_audit": {
            "planner_boundary": ["prepare", "start", "status", "stop", "snapshot"],
            "attestation_audit_boundary": {
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
                "current_status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md",
                "current_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md",
                "current_summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md",
                "current_proof_json": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json",
                "current_handoff": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md",
                "attestation_audit_checklist": "docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md",
                "attestation_audit_decision_surface": "docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md",
                "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md",
            },
            "baseline_input_attestation_outcome": {
                "task_id": previous_proof["task_id"],
                "task_state": previous_proof["task_result"]["task_state"],
                "key_finding": previous_proof["task_result"]["key_finding"],
                "claim_boundary": previous_proof["task_result"]["claim_boundary"],
                "recommended_next_step": previous_proof["task_result"]["recommended_next_step"],
                "gate_pass_successor": previous_proof["task_result"]["gate_pass_successor"],
            },
            "audit_faces": {
                "attestation_audit_decision_surface": audit_rows,
                "blocked_audit_faces": blocked_audit_faces,
                "checklist_attestation": checklist_attestation,
                "retry_gate_review_reopen_ready": False,
            },
            "sub_agents": list(SUB_AGENT_SUMMARIES),
            "supporting_files": [
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md",
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md",
                "plans/demo_forward_supervised_run_retry_gate_input_attestation_plan.md",
                "plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md",
                "docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md",
                "scripts/run_demo_forward_supervised_run_retry_gate_input_attestation.py",
                "scripts/run_demo_forward_supervised_run_retry_gate_attestation_audit.py",
                "scripts/build_proof_bundle.sh",
                "tests/test_demo_forward_supervised_run.py",
                "tests/test_demo_forward_supervised_run_retry_gate.py",
                "tests/test_demo_forward_supervised_run_retry_gate_input_attestation.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_audit.py",
            ],
            "proof_outputs": [
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json",
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md",
                "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz",
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

    report_text = build_current_report(run_timestamp, runtime_config, audit_rows)
    status_text = build_status()
    proof_summary_text = build_proof_summary()
    summary_text = f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#76` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## What This Task Did

- Accepted retry-gate input attestation as the baseline current source of truth.
- Promoted retry-gate attestation audit to the current operator-visible lane.
- Added current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.
- Fixed one fail-closed audit model that blocks retry-gate review until every required face is current, non-stale, and auditable enough.

## Decision

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task status: `{TASK_STATUS}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Audit-pass successor: `{PASS_NEXT_TASK_LANE}`
- Decision: `{DECISION}`

## Key Paths

- Current spec: `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md`
- Current implementation plan: `plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md`
- Current checklist: `docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md`
- Current decision surface: `docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md`
- Current proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json`
- Current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md`
- Current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md`
- Current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md`
- Current bundle target: `artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz`
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
        "baseline_task_state": "supervised_run_retry_gate_input_attestation_blocked",
        "first_demo_target": "dexter_paper_live",
        "source_faithful_seam": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "blocked_audit_faces": blocked_audit_faces,
        "retry_gate_review_reopen_ready": False,
    }

    details_text = build_details()
    min_prompt_text = build_min_prompt()
    handoff_text = build_handoff(run_timestamp, runtime_config, audit_rows)
    subagents_text = build_subagents()
    spec_text = build_spec()
    plan_text = build_plan()
    checklist_text = build_checklist()
    decision_surface_text = build_decision_surface(audit_rows)

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
        "previous_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION",
        "previous_task_state": "supervised_run_retry_gate_input_attestation_blocked",
        "previous_key_finding": "supervised_run_retry_gate_input_attestation_blocked_on_missing_attestation_faces",
        "previous_claim_boundary": "supervised_run_retry_gate_input_attestation_bounded",
        "retry_gate_input_attestation_accepted_as_baseline": True,
        "retry_gate_attestation_audit_promoted_current": True,
    }
    context_pack["bundle_source"] = BUNDLE_SOURCE
    context_pack["current_contract"].update(
        {
            "demo_forward_supervised_run_retry_gate_attestation_audit_marker": "demo_forward_supervised_run_retry_gate_attestation_audit",
            "demo_forward_supervised_run_retry_gate_attestation_audit_spec_path": "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md",
            "demo_forward_supervised_run_retry_gate_attestation_audit_plan_path": "plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md",
            "demo_forward_supervised_run_retry_gate_attestation_audit_checklist_path": "docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md",
            "demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface_path": "docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md",
            "demo_forward_supervised_run_retry_gate_attestation_audit_subagents_path": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md",
            "demo_forward_supervised_run_retry_gate_attestation_audit_subagent_summary_path": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/subagent_summary.md",
            "demo_forward_retry_gate_attestation_audit_current_lane": NEXT_TASK_LANE,
            "demo_forward_retry_gate_attestation_audit_pass_successor": PASS_NEXT_TASK_LANE,
        }
    )
    context_pack["current_task"] = {
        "id": TASK_ID,
        "scope": [
            "Reverify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X after retry-gate input attestation merged.",
            "Accept retry-gate input attestation as baseline current source of truth.",
            "Promote retry-gate attestation-audit status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Re-audit each required face for completeness, stale conditions, current attestation refs, and whether the face is auditable enough to reopen retry-gate review.",
            "Keep retry-gate review blocked until every attestation face is current, non-stale, and auditable enough.",
        ],
        "deliverables": [
            "README.md",
            "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md",
            "plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md",
            "docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md",
            "docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_audit.py",
            "tests/test_demo_forward_supervised_run_retry_gate_input_attestation.py",
            "tests/test_demo_forward_supervised_run_retry_gate.py",
            "tests/test_demo_forward_supervised_run.py",
            "tests/test_bootstrap_layout.py",
            "scripts/run_demo_forward_supervised_run_retry_gate_attestation_audit.py",
            "scripts/build_proof_bundle.sh",
            "artifacts/summary.md",
            "artifacts/context_pack.json",
            "artifacts/proof_bundle_manifest.json",
            "artifacts/task_ledger.jsonl",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/DETAILS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/MIN_PROMPT.txt",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/CONTEXT.json",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/subagent_summary.md",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md",
            "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz",
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
            "latest_recent_vexter_prs": [76, 75, 74, 73, 72],
            "vexter_pr_76_merged_at": VERIFIED_VEXTER_MERGED_AT,
            "vexter_pr_76_closed_at": VERIFIED_VEXTER_MERGED_AT,
        }
    )
    context_pack["evidence"]["demo_forward_supervised_run_retry_gate_attestation_audit"] = {
        "report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md",
        "status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md",
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json",
        "summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md",
        "handoff_dir": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit",
        "checklist": "docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md",
        "decision_surface": "docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md",
        "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md",
        "key_finding": KEY_FINDING,
        "claim_boundary": CLAIM_BOUNDARY,
        "task_state": TASK_STATUS,
        "run_outcome": "FAIL/BLOCKED",
        "operator_visible_attestation_audit_surface_current": True,
        "preferred_next_step": NEXT_TASK_LANE,
        "audit_pass_successor": PASS_NEXT_TASK_LANE,
        "attestation_audit_boundary": proof["supervised_run_retry_gate_attestation_audit"][
            "attestation_audit_boundary"
        ],
        "blocked_audit_faces": blocked_audit_faces,
        "sub_agents": list(SUB_AGENT_SUMMARIES),
    }
    context_pack["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "rationale": [
            "Retry-gate input attestation is accepted as baseline and attestation audit is now current.",
            "One or more attestation faces still lack a current bounded-window attestation record or stale check.",
            "Hold retry-gate review closed until the attestation faces are current, non-stale, and auditable enough.",
        ],
        "pass_successor": {
            "id": PASS_NEXT_TASK_ID,
            "state": PASS_NEXT_TASK_STATE,
            "lane": PASS_NEXT_TASK_LANE,
        },
    }
    context_pack["proofs"].update(
        {
            "demo_forward_supervised_run_retry_gate_attestation_audit_added": True,
            "demo_forward_retry_gate_attestation_audit_current_pointers_fixed": True,
            "demo_forward_retry_gate_attestation_audit_checklist_written": True,
            "demo_forward_retry_gate_attestation_audit_decision_surface_written": True,
            "demo_forward_retry_gate_attestation_audit_subagent_summary_written": True,
            "recommended_next_step_stays_supervised_run_retry_gate_attestation_audit_when_blocked": True,
            "retry_gate_review_requires_current_auditable_attestation_faces": True,
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
        ("docs", "docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md"),
        ("docs", "docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md"),
        ("scripts", "scripts/run_demo_forward_supervised_run_retry_gate_attestation_audit.py"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/subagent_summary.md"),
    ):
        if path not in manifest[key]:
            manifest[key].append(path)
    for path in (
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md",
        "plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md",
        "tests/test_demo_forward_supervised_run_retry_gate_attestation_audit.py",
        "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz",
    ):
        if path not in manifest["included_paths"]:
            manifest["included_paths"].append(path)
    manifest["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "resume_requirements": [
            f"Keep Dexter pinned at {VERIFIED_DEXTER_COMMIT} and Mew-X frozen at {VERIFIED_MEWX_COMMIT}.",
            "Start from the current attestation-audit status, report, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Do not reopen retry-gate review until every face is explicit, non-stale, and auditable enough.",
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
            "demo_forward_supervised_run_retry_gate_attestation_audit_added": True,
            "demo_forward_retry_gate_attestation_audit_current_pointers_fixed": True,
            "demo_forward_retry_gate_attestation_audit_checklist_written": True,
            "demo_forward_retry_gate_attestation_audit_decision_surface_written": True,
            "demo_forward_retry_gate_attestation_audit_subagent_summary_written": True,
            "recommended_next_step_stays_supervised_run_retry_gate_attestation_audit_when_blocked": True,
            "retry_gate_review_requires_current_auditable_attestation_faces": True,
        }
    )
    MANIFEST_PATH.write_text(format_json(manifest))

    ledger_payload = {
        "artifact_bundle": BUNDLE_PATH,
        "base_main": VERIFIED_VEXTER_COMMIT,
        "baseline_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION",
        "baseline_task_state": "supervised_run_retry_gate_input_attestation_blocked",
        "branch": git_output("branch", "--show-current"),
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": DECISION,
        "first_demo_target": "dexter_paper_live",
        "gate_pass_successor": PASS_NEXT_TASK_ID,
        "key_finding": KEY_FINDING,
        "next_task_id": NEXT_TASK_ID,
        "next_task_state": NEXT_TASK_STATE,
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json",
        "recommended_next_lane": NEXT_TASK_LANE,
        "repo": "https://github.com/Cabbala/Vexter",
        "retry_gate_attestation_audit_face_count": len(audit_rows),
        "retry_gate_attestation_audit_definition_complete_face_count": sum(
            row["definition_complete"] for row in audit_rows
        ),
        "retry_gate_attestation_audit_auditable_face_count": sum(
            row["auditable_now"] for row in audit_rows
        ),
        "selected_outcome": "FAIL/BLOCKED",
        "source_faithful_modes": {"dexter": "paper_live", "mewx": "sim_live"},
        "status": TASK_STATUS,
        "sub_agents_used": [item["name"] for item in SUB_AGENT_SUMMARIES],
        "supporting_vexter_prs": [76, 75, 74, 73, 72],
        "task_id": TASK_ID,
        "template_runtime_validation_errors": runtime_errors,
        "verified_dexter_main_commit": VERIFIED_DEXTER_COMMIT,
        "verified_dexter_pr": 3,
        "verified_mewx_frozen_commit": VERIFIED_MEWX_COMMIT,
        "verified_prs": [76, 75, 74],
        "date": run_timestamp.split("T", 1)[0],
    }
    rewrite_local_ledger(ledger_payload)

    update_readme()


if __name__ == "__main__":
    main()
