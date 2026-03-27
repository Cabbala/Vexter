#!/usr/bin/env python3
"""Emit bounded retry-gate input-attestation surfaces from the retry-gate baseline."""

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

CHECKLIST_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_gate_input_attestation_checklist.md"
DECISION_SURFACE_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md"
SCRIPT_PATH = ROOT / "scripts" / "run_demo_forward_supervised_run_retry_gate_input_attestation.py"
SPEC_PATH = ROOT / "specs" / "DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md"
PLAN_PATH = ROOT / "plans" / "demo_forward_supervised_run_retry_gate_input_attestation_plan.md"

PREVIOUS_REPORT_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-report.md"
PREVIOUS_STATUS_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-status.md"
PREVIOUS_PROOF_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-check.json"
PREVIOUS_SUMMARY_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-summary.md"
)
PREVIOUS_HANDOFF_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate" / "HANDOFF.md"
)
PREVIOUS_CHECKLIST_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_gate_checklist.md"
PREVIOUS_MATRIX_PATH = ROOT / "docs" / "demo_forward_supervised_run_retry_gate_decision_surface.md"
PREVIOUS_SUBAGENTS_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate" / "SUBAGENTS.md"
)

REPORT_DIR = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-input-attestation"
REPORT_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-input-attestation-report.md"
STATUS_PATH = ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-input-attestation-status.md"
SUBAGENTS_PATH = REPORT_DIR / "SUBAGENTS.md"
SUBAGENT_SUMMARY_PATH = REPORT_DIR / "subagent_summary.md"
PROOF_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-input-attestation-check.json"
PROOF_SUMMARY_PATH = ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-input-attestation-summary.md"

BUNDLE_PATH = "artifacts/bundles/demo-forward-supervised-run-retry-gate-input-attestation.tar.gz"
BUNDLE_SOURCE = "/Users/cabbala/Downloads/vexter_supervised_run_retry_gate_input_attestation_bundle.tar.gz"

TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION"
TASK_STATUS = "supervised_run_retry_gate_input_attestation_blocked"
KEY_FINDING = "supervised_run_retry_gate_input_attestation_blocked_on_missing_attestation_faces"
CLAIM_BOUNDARY = "supervised_run_retry_gate_input_attestation_bounded"
NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION"
NEXT_TASK_STATE = "retry_gate_input_attestations_pending"
NEXT_TASK_LANE = "supervised_run_retry_gate_input_attestation"
PASS_NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-EXECUTION"
PASS_NEXT_TASK_STATE = "ready_for_supervised_run_retry_execution"
PASS_NEXT_TASK_LANE = "supervised_run_retry_execution"
DECISION = "retry_execution_blocked_pending_attestation_faces"

VERIFIED_DEXTER_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
VERIFIED_MEWX_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
VERIFIED_VEXTER_PR = 75
VERIFIED_VEXTER_COMMIT = "b9e556ffc57592190fdffbcabf61ab168b8ed467"
VERIFIED_VEXTER_MERGED_AT = "2026-03-27T01:50:11Z"

SUB_AGENT_SUMMARIES = (
    {
        "name": "Anscombe",
        "lines": [
            "Confirmed the retry-gate quartet should remain the accepted baseline until a complete input-attestation quartet exists, then switch current report, status, proof, summary, and handoff pointers atomically.",
            "Recommended that every attestation row carry the same five faces in one place: repo-visible marker, who attests, what is being attested, minimal evidence shape, and stale boundary.",
            "Recommended fail-closed wording that stays observation-based: the repo may name markers and attestation requirements, but gate recheck remains blocked until each attestation face is explicit enough to reopen review.",
        ],
    },
    {
        "name": "Euler",
        "lines": [
            "Kept the attestation boundary identical to the accepted retry-gate boundary: Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, allowlist-only, small-lot, one-plan, one-position, bounded supervision, and funded-live forbidden.",
            "Recommended the smallest next-step cut: hold the current lane at `supervised_run_retry_gate_input_attestation` while blocked, and expose `supervised_run_retry_execution` only as the attestation-pass successor once gate review can honestly reopen.",
            "Confirmed there is no need for planner or adapter code drift: `prepare / start / status / stop / snapshot` stays fixed, `manual_latched_stop_all` stays planner-owned, and Mew-X remains unchanged.",
        ],
    },
    {
        "name": "Parfit",
        "lines": [
            "Scoped the smallest safe change set to docs, proof-generation script, generated artifacts, manifest/context/ledger updates, and tests; no `vexter/` runtime behavior changes are needed for this lane.",
            "Recommended validating the generator plus the affected regression surfaces with `python3 scripts/run_demo_forward_supervised_run_retry_gate_input_attestation.py` and focused `pytest` coverage on the supervised-run and bundle-layout tests.",
            "Merge readiness depends on an atomic current-pointer switch to input attestation, a regenerated tarball at the new bundle path, and a clean blocked decision that does not claim retry execution success or a passed gate review.",
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
                "A credential-source marker is visible in repo, but no current attestation names who resolved it, how it was checked, or when the check expires."
            ),
            "who_attests": "named_operator_owner_outside_repo",
            "what_is_being_attested": (
                "The external credential reference resolves to the intended Dexter paper-live demo credential source for the bounded supervised window."
            ),
            "minimal_evidence_shape": (
                "attestor name, reference label only, bounded window, verification timestamp, and a plain-language confirmation that the referenced credential source was resolved outside repo"
            ),
            "stale_when": "the credential reference changes or the bounded supervised window rolls forward",
            "explicit_enough_for_retry_gate_recheck": False,
            "pass_when": (
                "the repo can point to a current attestation record for this face without exposing secret material"
            ),
        },
        {
            "name": "venue_ref_face",
            "repo_visible_marker": template_env["DEXTER_DEMO_VENUE_REF"],
            "current_observation": (
                "A venue marker is visible in repo, but no current attestation records which venue the upcoming supervised window is meant to hit."
            ),
            "who_attests": "named_operator_owner_plus_venue_owner_outside_repo",
            "what_is_being_attested": (
                "The repo-visible venue reference points to the intended Dexter demo venue for the bounded supervised retry window."
            ),
            "minimal_evidence_shape": (
                "attestor names, venue reference label, bounded window, verification timestamp, and explicit match confirmation between the marker and the intended venue"
            ),
            "stale_when": "the venue reference changes, venue routing changes, or the supervised window is rescheduled",
            "explicit_enough_for_retry_gate_recheck": False,
            "pass_when": (
                "the venue attestation is current, explicit, and reviewable without requiring the reviewer to infer the mapping"
            ),
        },
        {
            "name": "account_ref_face",
            "repo_visible_marker": template_env["DEXTER_DEMO_ACCOUNT_REF"],
            "current_observation": (
                "An account marker is visible in repo, but no current attestation ties it to the intended demo account for the next supervised window."
            ),
            "who_attests": "named_operator_owner_outside_repo",
            "what_is_being_attested": (
                "The repo-visible account reference points to the intended Dexter paper-live demo account for the bounded supervised window."
            ),
            "minimal_evidence_shape": (
                "attestor name, account reference label, bounded window, verification timestamp, and a statement that the external account binding was checked outside repo"
            ),
            "stale_when": "the account reference changes or a different demo account is selected for the window",
            "explicit_enough_for_retry_gate_recheck": False,
            "pass_when": (
                "the account attestation makes the intended demo account explicit enough to reopen gate review"
            ),
        },
        {
            "name": "connectivity_profile_face",
            "repo_visible_marker": template_env["DEXTER_DEMO_CONNECTIVITY_PROFILE"],
            "current_observation": (
                "A connectivity-profile marker is visible in repo, but no current attestation records that the intended venue and account path was checked for the target window."
            ),
            "who_attests": "named_operator_owner_plus_connectivity_owner_outside_repo",
            "what_is_being_attested": (
                "The intended connectivity profile can reach the intended Dexter demo venue and account during the bounded supervised window."
            ),
            "minimal_evidence_shape": (
                "attestor names, connectivity profile label, verification timestamp, bounded window, and a short reachability result"
            ),
            "stale_when": "network routing changes, connectivity profile changes, or the verification timestamp is outside the current window",
            "explicit_enough_for_retry_gate_recheck": False,
            "pass_when": (
                "the connectivity attestation is current enough that a gate reviewer can treat reachability as explicitly checked"
            ),
        },
        {
            "name": "operator_owner_face",
            "repo_visible_marker": "unconfirmed_outside_repo",
            "current_observation": (
                "The repo still does not point to one named operator owner for the full supervised window."
            ),
            "who_attests": "demo_operator_lead_outside_repo",
            "what_is_being_attested": (
                "One explicit operator owner is responsible for the full retry-gate review and bounded supervised window."
            ),
            "minimal_evidence_shape": (
                "owner name or handle, verification timestamp, window label, and explicit ownership statement"
            ),
            "stale_when": "the named owner changes or the supervised window changes",
            "explicit_enough_for_retry_gate_recheck": False,
            "pass_when": "the owner attestation is explicit enough that gate recheck does not rely on unnamed responsibility",
        },
        {
            "name": "bounded_start_criteria_face",
            "repo_visible_marker": {
                "bounded_window_minutes": runtime_config.bounded_window_minutes,
                "status_delivery": "poll_first",
                "halt_mode": "manual_latched_stop_all",
            },
            "current_observation": (
                "The bounded window and stop model are fixed in repo, but no current attestation records start time, go/no-go owner, or abort ownership for the target window."
            ),
            "who_attests": "named_operator_owner_outside_repo",
            "what_is_being_attested": (
                "The intended supervised start window, go/no-go owner, and abort owner are explicit and bounded for the next reviewable retry attempt."
            ),
            "minimal_evidence_shape": (
                "planned start window, bounded window minutes, go/no-go owner, abort owner, verification timestamp, and explicit stop condition note"
            ),
            "stale_when": "the scheduled window moves or ownership for go/no-go or abort changes",
            "explicit_enough_for_retry_gate_recheck": False,
            "pass_when": (
                "the bounded-start attestation makes timing and ownership explicit enough to reopen gate review"
            ),
        },
        {
            "name": "allowlist_symbol_lot_reconfirmed",
            "repo_visible_marker": runtime_guardrails,
            "current_observation": (
                "The bounded symbol, lot-size, window, and one-position guardrails parse cleanly from repo, but no current attestation confirms they were rechecked for the upcoming supervised window."
            ),
            "who_attests": "named_operator_owner_outside_repo",
            "what_is_being_attested": (
                "The explicit allowlist, default symbol, lot size, bounded window, and one-position cap were reconfirmed for the upcoming supervised window."
            ),
            "minimal_evidence_shape": (
                "attestor name, verification timestamp, allowlist values, lot-size values, position cap, and a plain-language reconfirmation note"
            ),
            "stale_when": "any guardrail value changes or the supervised window moves",
            "explicit_enough_for_retry_gate_recheck": False,
            "pass_when": (
                "the guardrail attestation is current enough that gate recheck can treat the bounded demo envelope as explicitly reconfirmed"
            ),
        },
        {
            "name": "manual_latched_stop_all_visibility_reconfirmed",
            "repo_visible_marker": "baseline_stop_all_state=flatten_confirmed",
            "current_observation": (
                "The blocked supervised baseline preserved `manual_latched_stop_all`, but no current attestation records who reconfirmed visibility for the next review window."
            ),
            "who_attests": "named_operator_owner_outside_repo",
            "what_is_being_attested": (
                "`manual_latched_stop_all` remains visibly reachable on the bounded retry path for the next supervised window."
            ),
            "minimal_evidence_shape": (
                "attestor name, verification timestamp, referenced stop-all surface, and a plain-language visibility confirmation"
            ),
            "stale_when": "the stop-all surface changes or the window advances without reconfirmation",
            "explicit_enough_for_retry_gate_recheck": False,
            "pass_when": (
                "the stop-all visibility attestation is current enough to reopen gate review without assuming prior visibility still holds"
            ),
        },
        {
            "name": "terminal_snapshot_readability_reconfirmed",
            "repo_visible_marker": "baseline_terminal_snapshot_readable=true",
            "current_observation": (
                "The baseline handoff shows terminal snapshot detail, but no current attestation records who rechecked readability for the next review window."
            ),
            "who_attests": "named_operator_owner_outside_repo",
            "what_is_being_attested": (
                "Terminal snapshot detail remains readable enough for the upcoming supervised retry window."
            ),
            "minimal_evidence_shape": (
                "attestor name, verification timestamp, referenced snapshot surface, and a short readability confirmation"
            ),
            "stale_when": "the snapshot format changes or the supervised window advances without reconfirmation",
            "explicit_enough_for_retry_gate_recheck": False,
            "pass_when": (
                "the snapshot-readability attestation is current enough that a gate reviewer can rely on terminal visibility without inference"
            ),
        },
    ]


def build_gate_checklist(inputs: list[dict], runtime_errors: list[str]) -> dict[str, bool]:
    return {
        "runtime_guardrails_parse_cleanly": not runtime_errors,
        "external_credential_source_face_attested": False,
        "venue_ref_face_attested": False,
        "account_ref_face_attested": False,
        "connectivity_profile_face_attested": False,
        "operator_owner_face_attested": False,
        "bounded_start_criteria_face_attested": False,
        "allowlist_symbol_lot_reconfirmed": False,
        "manual_latched_stop_all_visibility_reconfirmed": False,
        "terminal_snapshot_readability_reconfirmed": False,
        "all_attestation_faces_explicit_enough": all(
            row["explicit_enough_for_retry_gate_recheck"] for row in inputs
        ),
        "retry_execution_review_ready": all(
            row["explicit_enough_for_retry_gate_recheck"] for row in inputs
        ),
    }


def build_spec() -> str:
    return f"""# Demo Forward Supervised Run Retry Gate Input Attestation

This document fixes the bounded retry-gate input-attestation lane after `DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE` made the unresolved gate inputs current and reviewable.

## Verified Base

- Latest merged Vexter `main`: PR `#75`, merge commit `{VERIFIED_VEXTER_COMMIT}`, merged at `{VERIFIED_VEXTER_MERGED_AT}`
- Dexter merged `main`: PR `#3`, merge commit `{VERIFIED_DEXTER_COMMIT}`
- Frozen Mew-X commit: `{VERIFIED_MEWX_COMMIT}`
- Retry-gate baseline proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`

## Purpose

The shortest next lane is not retry execution. It is fixing one bounded retry-gate input-attestation lane that records, fail-closed, who attests each required gate face, what is being attested, the minimum evidence shape, and when the attestation becomes stale.

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

## Attestation Boundary

The bounded retry-gate input-attestation lane remains:

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
- operator owner explicit
- venue / connectivity confirmation explicit
- bounded start criteria explicit
- allowlist / symbol / lot-size reconfirmation explicit
- `manual_latched_stop_all` visibility reconfirmation explicit
- terminal snapshot readability reconfirmation explicit
- Mew-X unchanged
- funded live forbidden

## Required Current Surfaces

The repo must expose the following as current source of truth:

- current status report
- current report
- current summary
- current proof json
- current handoff
- gate input attestation checklist
- gate input attestation decision surface
- next recommended step

## Honest Attestation Model

The bounded attestation lane must hold one of these honest outcomes:

- PASS: the required gate-input attestation faces are explicit enough to reopen retry-gate review
- FAIL/BLOCKED: one or more attestation faces remain unresolved, stale, or not explicit enough to reopen retry-gate review

The repo may name external references, attesters, timestamps, and evidence shapes, but it must not embed credentials, secrets, or fabricated pass evidence.

## Attestation Face Model

The current attestation decision surface must include at least:

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

## Next-Step Boundary

- While blocked, the current lane remains `supervised_run_retry_gate_input_attestation`.
- Only after every required attestation face is explicit enough may the next recommended lane advance to `supervised_run_retry_execution`.
- That pass means gate review can honestly reopen without hidden assumptions; it does not fabricate a completed retry execution.

## Out Of Scope

- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no portfolio split
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success
"""


def build_plan() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION Plan

## Objective

Promote a bounded `supervised_run_retry_gate_input_attestation` lane to the repo-visible current source of truth after retry gate, without widening planner scope or fabricating retry execution success.

## Inputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-report.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md`
- `docs/demo_forward_supervised_run_retry_gate_checklist.md`
- `docs/demo_forward_supervised_run_retry_gate_decision_surface.md`

## Steps

1. Reverify latest GitHub-visible `main` after PR `#75`.
2. Keep Dexter pinned at merged PR `#3` and keep frozen Mew-X unchanged.
3. Accept `supervised_run_retry_gate_blocked` as the current baseline instead of retrying execution.
4. Promote an input-attestation spec, status, report, summary, proof, handoff, checklist, and decision surface as the current source of truth.
5. Fix one bounded attestation surface that makes every required gate face explicit with who attests, what is being attested, minimal evidence shape, and stale boundary.
6. Preserve the planner boundary at `prepare / start / status / stop / snapshot`, keep `poll_first`, and keep `manual_latched_stop_all` planner-owned.
7. Keep the current lane blocked unless every required attestation face is explicit enough to reopen retry-gate review.

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
- operator owner explicit
- venue / connectivity confirmation explicit
- bounded start criteria explicit
- `manual_latched_stop_all` visibility reconfirmation explicit
- terminal snapshot readability reconfirmation explicit
- Mew-X unchanged
- funded live forbidden

## Required Outputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md`
- `plans/demo_forward_supervised_run_retry_gate_input_attestation_plan.md`
- `docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md`
- `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/DETAILS.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/MIN_PROMPT.txt`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/CONTEXT.json`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md`
- `artifacts/summary.md`
- `artifacts/context_pack.json`
- `artifacts/proof_bundle_manifest.json`
- `artifacts/task_ledger.jsonl`
- `artifacts/bundles/demo-forward-supervised-run-retry-gate-input-attestation.tar.gz`

## Acceptance

- Retry gate remains the accepted baseline.
- The input-attestation surface records every required gate face without embedding external secrets.
- The current handoff points directly at checklist and decision-surface artifacts.
- The current lane remains `FAIL/BLOCKED` until retry execution can honestly be reconsidered from explicit attestation faces.
"""


def build_checklist() -> str:
    return f"""# Demo Forward Supervised Run Retry Gate Input Attestation Checklist

This checklist fixes the minimum operator-visible surface that must be explicit before retry execution may honestly be reconsidered.

## Current Pointers

1. Start at `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`.
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md`.
5. Use `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md` as the single attestation decision surface.

## Input Attestation Checklist

1. Accept the prior `supervised_run_retry_gate_blocked` lane as baseline and do not claim retry execution success.
2. Keep one attestation row per required face: credential source, venue ref, account ref, connectivity profile, operator owner, bounded start criteria, allowlist/symbol/lot reconfirmation, `manual_latched_stop_all` visibility, and terminal snapshot readability.
3. Keep the repo-visible markers explicit: `DEXTER_DEMO_CREDENTIAL_SOURCE`, `DEXTER_DEMO_VENUE_REF`, `DEXTER_DEMO_ACCOUNT_REF`, and `DEXTER_DEMO_CONNECTIVITY_PROFILE`.
4. For every row, record who attests the face outside the repo.
5. For every row, record what is being attested without embedding secrets or credential material.
6. For every row, record the minimum evidence shape that would be enough for a gate reviewer to inspect the attestation.
7. For every row, record when the attestation becomes stale.
8. Reconfirm `DEXTER_DEMO_ALLOWED_SYMBOLS`, `DEXTER_DEMO_DEFAULT_SYMBOL`, `DEXTER_DEMO_ORDER_SIZE_LOTS`, `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`, `DEXTER_DEMO_WINDOW_MINUTES=15`, and `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`.
9. Reconfirm venue/connectivity, `manual_latched_stop_all` visibility, and terminal snapshot readability stay explicit for the bounded supervised window.
10. Reconfirm Mew-X remains unchanged on `sim_live`.
11. Reconfirm funded live remains forbidden.

## Input Attestation Exit Criteria

- every attestation row in `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md` is explicit enough to reopen gate review for retry execution
- operator owner is named outside the repo
- venue and connectivity attestations are current for the bounded window
- allowlist, symbol, lot-size, window, and one-position cap are reconfirmed
- `manual_latched_stop_all` visibility and terminal snapshot readability are reconfirmed
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


def build_decision_surface(inputs: list[dict]) -> str:
    lines = [
        "# Demo Forward Supervised Run Retry Gate Input Attestation Decision Surface",
        "",
        "This decision surface is the current source of truth for `supervised_run_retry_gate_input_attestation`.",
        "",
        "| Attestation face | Repo-visible marker | Who attests | What is being attested | Minimal evidence shape | Stale when | Current observation | Face passes when |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in inputs:
        lines.append(
            f"| `{row['name']}` | `{format_marker(row['repo_visible_marker'])}` | `{row['who_attests']}` | {row['what_is_being_attested']} | {row['minimal_evidence_shape']} | {row['stale_when']} | {row['current_observation']} | {row['pass_when']} |"
        )
    lines.extend(
        [
            "",
            "## Current Decision",
            "",
            "- Attestation outcome: `FAIL/BLOCKED`",
            f"- Key finding: `{KEY_FINDING}`",
            f"- Claim boundary: `{CLAIM_BOUNDARY}`",
            f"- Current task state: `{TASK_STATUS}`",
            f"- Recommended next step while blocked: `{NEXT_TASK_LANE}`",
            f"- Attestation-pass successor: `{PASS_NEXT_TASK_LANE}`",
            "- Retry execution allowed now: `false`",
            "",
            "Retry execution does not begin unless every attestation row is explicit enough to reopen gate review honestly.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_current_report(
    run_timestamp: str,
    previous_proof: dict,
    runtime_config: DexterDemoRuntimeConfig,
    inputs: list[dict],
) -> str:
    unresolved = [
        row["name"] for row in inputs if not row["explicit_enough_for_retry_gate_recheck"]
    ]
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION Report

## Verified Base

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#75`, merge commit `{VERIFIED_VEXTER_COMMIT}`, merged at `{VERIFIED_VEXTER_MERGED_AT}`.
- Dexter remained pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen Mew-X remained pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## Starting Point

- Accepted `supervised_run_retry_gate_blocked` as the current blocked baseline instead of fabricating a retry execution.
- Carried forward the bounded retry-gate proof, report, summary, and handoff as the baseline current source of truth.
- Promoted retry-gate input attestation as the new current operator-visible lane.

## Attestation Boundary

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

## Baseline Continuity

- retry-gate status path: `artifacts/reports/demo-forward-supervised-run-retry-gate-status.md`
- retry-gate proof path: `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`
- retry-gate handoff path: `artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md`
- retry-gate checklist path: `docs/demo_forward_supervised_run_retry_gate_checklist.md`
- retry-gate decision surface path: `docs/demo_forward_supervised_run_retry_gate_decision_surface.md`
- bounded runtime guardrails stayed parseable from `templates/windows_runtime/dexter.env.example`
- runtime validation errors: `{len(runtime_config.validation_errors())}`
- retry-gate recommended next step: `{previous_proof['task_result']['recommended_next_step']}`

## Required Current Surfaces

- current status report: `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md`
- current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md`
- current summary: `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md`
- current proof json: `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`
- current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md`
- gate input attestation checklist: `docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md`
- gate input attestation decision surface: `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md`
- sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md`

## Attestation Decision Summary

- unresolved attestation face count: `{len(unresolved)}`
- unresolved attestation faces: `{", ".join(unresolved)}`
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
- Blocker: one or more gate-input attestation faces remain external, unresolved, stale, or not explicit enough in repo-visible form to reopen gate review honestly.
- Run timestamp: `{run_timestamp}`

## Recommendation

- Current task state: `{TASK_STATUS}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Attestation-pass successor: `{PASS_NEXT_TASK_LANE}`
- Reason: the attestation lane is now current source of truth, but retry execution remains fail-closed until every required attestation face is explicit enough to reopen gate review honestly.
"""


def build_status() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION Status

- task_id: `{TASK_ID}`
- task_state: `{TASK_STATUS}`
- run_outcome: `FAIL/BLOCKED`
- key_finding: `{KEY_FINDING}`
- claim_boundary: `{CLAIM_BOUNDARY}`
- verified_vexter_main_pr: `{VERIFIED_VEXTER_PR}`
- verified_vexter_main_commit: `{VERIFIED_VEXTER_COMMIT}`
- verified_dexter_main_commit: `{VERIFIED_DEXTER_COMMIT}`
- verified_mewx_frozen_commit: `{VERIFIED_MEWX_COMMIT}`
- baseline_task: `DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE`
- baseline_task_state: `supervised_run_retry_gate_blocked`
- planner_boundary: `prepare/start/status/stop/snapshot`
- current_attestation_lane: `{NEXT_TASK_LANE}`
- attestation_pass_successor: `{PASS_NEXT_TASK_LANE}`
"""


def build_proof_summary() -> str:
    return f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION Summary

- Verified base: Vexter `main` at PR `#75` merge commit `{VERIFIED_VEXTER_COMMIT}`.
- Starting point: retry gate already bounded the missing gate-input set without claiming retry execution.
- Promoted boundary: retry-gate input attestation is now current source of truth for the same Dexter-only `paper_live` / frozen Mew-X `sim_live` seam, `single_sleeve`, `dexter_default`, explicit allowlist, small lot, bounded supervised window, one active real demo plan max, and one open position max.
- Added current surfaces: input-attestation status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary.
- Outcome: `FAIL/BLOCKED` because the attestation faces are still not explicit enough to permit retry execution to be reconsidered honestly.
- Recommended next step while blocked: `{NEXT_TASK_LANE}`.
- Attestation-pass successor: `{PASS_NEXT_TASK_LANE}`.
"""


def build_details() -> str:
    return f"""# {TASK_ID}

## 1. Intent
- Accept the blocked retry-gate lane as baseline.
- Promote retry-gate input attestation to the repo-visible current source of truth.

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

## 4. Honest Attestation Model
- `PASS` only if every attestation face is explicit enough to reopen gate review for `supervised_run_retry_execution`.
- `FAIL/BLOCKED` if any attestation face remains unresolved, stale, or unobserved enough.

## 5. Next-Step Boundary
- blocked current lane: `{NEXT_TASK_LANE}`
- attestation-pass successor: `{PASS_NEXT_TASK_LANE}`
"""


def build_min_prompt() -> str:
    return (
        "GitHub最新状態を確認し、Vexter `main` PR #75 merge 後の retry-gate input-attestation surface を current source of truth として扱ってください。\n"
        "出発点は `supervised_run_retry_gate_blocked` で、Dexter `paper_live` のみ・frozen Mew-X `sim_live` のみ・`single_sleeve`・`dexter_default`・explicit allowlist・small lot・max open positions=1・bounded supervised window を維持してください。\n"
        "planner の public boundary は `prepare / start / status / stop / snapshot` のまま、`manual_latched_stop_all` は planner-owned のまま保ってください。\n"
        "external credential refs は repo 外に残し、attestation face が揃わない限り `FAIL/BLOCKED` を維持し、retry execution success を捏造しないでください。\n"
        "current status / report / proof / handoff / checklist / decision surface / sub-agent summary を更新し、必要 attestation が explicit enough の場合にのみ次を `supervised_run_retry_execution` と示してください。\n"
    )


def build_handoff(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    inputs: list[dict],
) -> str:
    return f"""# Demo Forward Supervised Run Retry Gate Input Attestation Handoff

## Current Status
- outgoing_shift_window: {run_timestamp} retry-gate input-attestation lane
- incoming_shift_window: explicit attestation completion and possible retry execution review
- task_state: {TASK_STATUS}
- shift_outcome: blocked
- current_action: hold_retry_execution_until_attestation_is_explicit_enough
- recommended_next_step_while_blocked: {NEXT_TASK_LANE}
- attestation_pass_successor: {PASS_NEXT_TASK_LANE}
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: {VERIFIED_VEXTER_COMMIT}
- dexter_main_commit: {VERIFIED_DEXTER_COMMIT}
- mewx_frozen_commit: {VERIFIED_MEWX_COMMIT}
- baseline_retry_gate_task_state: supervised_run_retry_gate_blocked

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md
- current_report: artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md
- current_proof_summary: artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md
- current_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json
- current_attestation_checklist: docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md
- current_attestation_decision_surface: docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md
- current_subagent_summary: artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md
- baseline_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-status.md
- baseline_report: artifacts/reports/demo-forward-supervised-run-retry-gate-report.md
- baseline_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json
- baseline_handoff: artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md

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

## Attestation Faces
{chr(10).join(f"- {row['name']}: explicit_enough_for_retry_execution_review={str(row['explicit_enough_for_retry_gate_recheck']).lower()}, who_attests={row['who_attests']}, stale_when={row['stale_when']}" for row in inputs)}

## Open Questions
- question_1_or_none: who is the named operator owner for the bounded retry window
- question_2_or_none: when does the bounded retry window open and who gives final go/no-go
- question_3_or_none: which venue, account, and connectivity refs are explicitly confirmed live outside the repo
- question_4_or_none: has `manual_latched_stop_all` visibility been reconfirmed before entry
- question_5_or_none: has terminal snapshot readability been reconfirmed before entry

## Next-Shift Priority Checks
- priority_check_1: keep the current lane blocked unless every attestation row is explicit enough
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

This handoff promotes the bounded retry-gate input-attestation lane only. It does not claim a passed gate, a completed retry execution, funded live access, or any Mew-X seam expansion.
"""


def build_subagents() -> str:
    lines = ["# Demo Forward Supervised Run Retry Gate Input Attestation Sub-agent Summaries", ""]
    for item in SUB_AGENT_SUMMARIES:
        lines.append(f"## {item['name']}")
        for line in item["lines"]:
            lines.append(f"- {line}")
        lines.append("")
    return "\n".join(lines)


def update_readme() -> None:
    marker = "`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION` starts from latest GitHub-visible Vexter `main`"
    if marker in README_PATH.read_text():
        return
    entry = (
        "\n\n`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION` starts from latest GitHub-visible "
        f"Vexter `main` at merged PR `#75` merge commit `{VERIFIED_VEXTER_COMMIT}` on "
        f"`{VERIFIED_VEXTER_MERGED_AT}`, keeps Dexter pinned at merged PR `#3` commit "
        f"`{VERIFIED_DEXTER_COMMIT}`, and keeps frozen Mew-X at `{VERIFIED_MEWX_COMMIT}`. "
        "It accepts the bounded retry-gate lane as baseline and promotes one fail-closed input-attestation lane instead: "
        "the repo now fixes the current status/report/proof/handoff/checklist/decision-surface surfaces for who attests "
        "each required gate face, what is being attested, the minimum evidence shape, and when the attestation goes stale, "
        "keeps the Dexter-only `paper_live` seam, leaves Mew-X unchanged on `sim_live`, and keeps funded live forbidden "
        "while holding the lane blocked until every attestation face is explicit enough. "
        f"The resulting status is `{TASK_STATUS}` with `{CLAIM_BOUNDARY}`, the blocked current lane "
        f"remains `{NEXT_TASK_LANE}`, and the attestation-pass successor is `{PASS_NEXT_TASK_LANE}`."
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
    unresolved_attestation_faces = [
        row["name"] for row in inputs if not row["explicit_enough_for_retry_gate_recheck"]
    ]
    checklist_attestation = build_gate_checklist(inputs, runtime_errors)

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
            "task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE",
            "task_state": "supervised_run_retry_gate_blocked",
            "report": str(PREVIOUS_REPORT_PATH.relative_to(ROOT)),
            "status_report": str(PREVIOUS_STATUS_PATH.relative_to(ROOT)),
            "proof": str(PREVIOUS_PROOF_PATH.relative_to(ROOT)),
            "summary": str(PREVIOUS_SUMMARY_PATH.relative_to(ROOT)),
            "handoff": str(PREVIOUS_HANDOFF_PATH.relative_to(ROOT)),
            "checklist": str(PREVIOUS_CHECKLIST_PATH.relative_to(ROOT)),
            "decision_surface": str(PREVIOUS_MATRIX_PATH.relative_to(ROOT)),
            "subagent_summary": str(PREVIOUS_SUBAGENTS_PATH.relative_to(ROOT)),
        },
        "supervised_run_retry_gate_input_attestation": {
            "planner_boundary": ["prepare", "start", "status", "stop", "snapshot"],
            "attestation_boundary": {
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
                "current_status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md",
                "current_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md",
                "current_summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md",
                "current_proof_json": "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json",
                "current_handoff": "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md",
                "gate_input_attestation_checklist": "docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md",
                "gate_input_attestation_decision_surface": "docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md",
                "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md",
            },
            "baseline_retry_gate_outcome": {
                "task_id": previous_proof["task_id"],
                "task_state": previous_proof["task_result"]["task_state"],
                "key_finding": previous_proof["task_result"]["key_finding"],
                "claim_boundary": previous_proof["task_result"]["claim_boundary"],
                "recommended_next_step": previous_proof["task_result"]["recommended_next_step"],
            },
            "attestation_faces": {
                "gate_input_attestation_decision_surface": inputs,
                "unresolved_attestation_faces": unresolved_attestation_faces,
                "checklist_attestation": checklist_attestation,
                "retry_execution_entry_allowed": False,
            },
            "sub_agents": list(SUB_AGENT_SUMMARIES),
            "supporting_files": [
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md",
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md",
                "plans/demo_forward_supervised_run_retry_gate_plan.md",
                "plans/demo_forward_supervised_run_retry_gate_input_attestation_plan.md",
                "docs/demo_forward_supervised_run_retry_gate_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_decision_surface.md",
                "docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md",
                "scripts/run_demo_forward_supervised_run_retry_gate.py",
                "scripts/run_demo_forward_supervised_run_retry_gate_input_attestation.py",
                "scripts/build_proof_bundle.sh",
                "tests/test_demo_forward_supervised_run.py",
                "tests/test_demo_forward_supervised_run_retry_gate.py",
                "tests/test_demo_forward_supervised_run_retry_gate_input_attestation.py",
            ],
            "proof_outputs": [
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json",
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md",
                "artifacts/bundles/demo-forward-supervised-run-retry-gate-input-attestation.tar.gz",
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
    summary_text = f"""# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#75` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## What This Task Did

- Accepted retry gate as the baseline current source of truth.
- Promoted retry-gate input attestation to the current operator-visible lane.
- Added current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.
- Fixed one fail-closed attestation model that blocks retry execution until every required face is explicit enough.

## Decision

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task status: `{TASK_STATUS}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Attestation-pass successor: `{PASS_NEXT_TASK_LANE}`
- Decision: `{DECISION}`

## Key Paths

- Current spec: `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md`
- Current implementation plan: `plans/demo_forward_supervised_run_retry_gate_input_attestation_plan.md`
- Current checklist: `docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md`
- Current decision surface: `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md`
- Current proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`
- Current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md`
- Current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md`
- Current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md`
- Current bundle target: `artifacts/bundles/demo-forward-supervised-run-retry-gate-input-attestation.tar.gz`
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
        "baseline_task_state": "supervised_run_retry_gate_blocked",
        "first_demo_target": "dexter_paper_live",
        "source_faithful_seam": {
            "dexter": "paper_live",
            "mewx": "sim_live",
        },
        "unresolved_attestation_faces": unresolved_attestation_faces,
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
        "previous_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE",
        "previous_task_state": "supervised_run_retry_gate_blocked",
        "previous_key_finding": "supervised_run_retry_gate_blocked_on_unresolved_gate_inputs",
        "previous_claim_boundary": "supervised_run_retry_gate_bounded",
        "retry_gate_accepted_as_baseline": True,
        "retry_gate_input_attestation_promoted_current": True,
    }
    context_pack["bundle_source"] = BUNDLE_SOURCE
    context_pack["current_contract"].update(
        {
            "demo_forward_supervised_run_retry_gate_input_attestation_marker": "demo_forward_supervised_run_retry_gate_input_attestation",
            "demo_forward_supervised_run_retry_gate_input_attestation_spec_path": "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md",
            "demo_forward_supervised_run_retry_gate_input_attestation_plan_path": "plans/demo_forward_supervised_run_retry_gate_input_attestation_plan.md",
            "demo_forward_supervised_run_retry_gate_input_attestation_checklist_path": "docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md",
            "demo_forward_supervised_run_retry_gate_input_attestation_decision_surface_path": "docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md",
            "demo_forward_supervised_run_retry_gate_input_attestation_subagents_path": "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md",
            "demo_forward_supervised_run_retry_gate_input_attestation_subagent_summary_path": "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/subagent_summary.md",
            "demo_forward_retry_gate_input_attestation_current_lane": NEXT_TASK_LANE,
            "demo_forward_retry_gate_input_attestation_pass_successor": PASS_NEXT_TASK_LANE,
        }
    )
    context_pack["current_task"] = {
        "id": TASK_ID,
        "scope": [
            "Reverify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X after retry gate merged.",
            "Accept retry gate as baseline current source of truth.",
            "Promote retry-gate input-attestation status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Bound each required gate face with a repo-visible marker, attester, attestation target, evidence shape, stale boundary, and fail-closed observation.",
            "Keep retry execution blocked until every attestation face is explicit enough.",
        ],
        "deliverables": [
            "README.md",
            "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md",
            "plans/demo_forward_supervised_run_retry_gate_input_attestation_plan.md",
            "docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md",
            "docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md",
            "tests/test_demo_forward_supervised_run_retry_gate_input_attestation.py",
            "tests/test_demo_forward_supervised_run_retry_gate.py",
            "tests/test_demo_forward_supervised_run.py",
            "tests/test_bootstrap_layout.py",
            "scripts/run_demo_forward_supervised_run_retry_gate_input_attestation.py",
            "scripts/build_proof_bundle.sh",
            "artifacts/summary.md",
            "artifacts/context_pack.json",
            "artifacts/proof_bundle_manifest.json",
            "artifacts/task_ledger.jsonl",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/DETAILS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/MIN_PROMPT.txt",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/CONTEXT.json",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/subagent_summary.md",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md",
            "artifacts/bundles/demo-forward-supervised-run-retry-gate-input-attestation.tar.gz",
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
            "latest_recent_vexter_prs": [75, 74, 73, 72, 71],
            "vexter_pr_75_merged_at": VERIFIED_VEXTER_MERGED_AT,
            "vexter_pr_75_closed_at": VERIFIED_VEXTER_MERGED_AT,
        }
    )
    context_pack["evidence"]["demo_forward_supervised_run_retry_gate_input_attestation"] = {
        "report": "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md",
        "status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md",
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json",
        "summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md",
        "handoff_dir": "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation",
        "checklist": "docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md",
        "decision_surface": "docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md",
        "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md",
        "key_finding": KEY_FINDING,
        "claim_boundary": CLAIM_BOUNDARY,
        "task_state": TASK_STATUS,
        "run_outcome": "FAIL/BLOCKED",
        "operator_visible_attestation_surface_current": True,
        "preferred_next_step": NEXT_TASK_LANE,
        "attestation_pass_successor": PASS_NEXT_TASK_LANE,
        "attestation_boundary": proof["supervised_run_retry_gate_input_attestation"]["attestation_boundary"],
        "unresolved_attestation_faces": unresolved_attestation_faces,
        "sub_agents": list(SUB_AGENT_SUMMARIES),
    }
    context_pack["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "rationale": [
            "Retry gate is accepted as baseline and input attestation is now current.",
            "One or more attestation faces remain unresolved or not explicit enough in repo-visible form.",
            "Hold retry execution closed until the attestation surface is explicit enough.",
        ],
        "pass_successor": {
            "id": PASS_NEXT_TASK_ID,
            "state": PASS_NEXT_TASK_STATE,
            "lane": PASS_NEXT_TASK_LANE,
        },
    }
    context_pack["proofs"].update(
        {
            "demo_forward_supervised_run_retry_gate_input_attestation_added": True,
            "demo_forward_retry_gate_input_attestation_current_pointers_fixed": True,
            "demo_forward_retry_gate_input_attestation_checklist_written": True,
            "demo_forward_retry_gate_input_attestation_decision_surface_written": True,
            "demo_forward_retry_gate_input_attestation_subagent_summary_written": True,
            "recommended_next_step_stays_supervised_run_retry_gate_input_attestation_when_blocked": True,
            "retry_execution_requires_attestation_faces": True,
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
        ("docs", "docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md"),
        ("docs", "docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md"),
        ("scripts", "scripts/run_demo_forward_supervised_run_retry_gate_input_attestation.py"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/subagent_summary.md"),
    ):
        if path not in manifest[key]:
            manifest[key].append(path)
    for path in (
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md",
        "plans/demo_forward_supervised_run_retry_gate_input_attestation_plan.md",
        "tests/test_demo_forward_supervised_run_retry_gate_input_attestation.py",
        "artifacts/bundles/demo-forward-supervised-run-retry-gate-input-attestation.tar.gz",
    ):
        if path not in manifest["included_paths"]:
            manifest["included_paths"].append(path)
    manifest["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "resume_requirements": [
            f"Keep Dexter pinned at {VERIFIED_DEXTER_COMMIT} and Mew-X frozen at {VERIFIED_MEWX_COMMIT}.",
            "Start from the current input-attestation status, report, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Do not enter retry execution until every attestation face is explicit enough.",
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
            "demo_forward_supervised_run_retry_gate_input_attestation_added": True,
            "demo_forward_retry_gate_input_attestation_current_pointers_fixed": True,
            "demo_forward_retry_gate_input_attestation_checklist_written": True,
            "demo_forward_retry_gate_input_attestation_decision_surface_written": True,
            "demo_forward_retry_gate_input_attestation_subagent_summary_written": True,
            "recommended_next_step_stays_supervised_run_retry_gate_input_attestation_when_blocked": True,
            "retry_execution_requires_attestation_faces": True,
        }
    )
    MANIFEST_PATH.write_text(format_json(manifest))

    ledger_payload = {
        "artifact_bundle": BUNDLE_PATH,
        "base_main": VERIFIED_VEXTER_COMMIT,
        "baseline_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE",
        "baseline_task_state": "supervised_run_retry_gate_blocked",
        "branch": git_output("branch", "--show-current"),
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": DECISION,
        "first_demo_target": "dexter_paper_live",
        "gate_pass_successor": PASS_NEXT_TASK_ID,
        "key_finding": KEY_FINDING,
        "next_task_id": NEXT_TASK_ID,
        "next_task_state": NEXT_TASK_STATE,
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json",
        "recommended_next_lane": NEXT_TASK_LANE,
        "repo": "https://github.com/Cabbala/Vexter",
        "retry_gate_input_attestation_face_count": len(inputs),
        "retry_gate_input_attestation_unresolved_face_count": len(unresolved_attestation_faces),
        "selected_outcome": "FAIL/BLOCKED",
        "source_faithful_modes": {"dexter": "paper_live", "mewx": "sim_live"},
        "status": TASK_STATUS,
        "sub_agents_used": [item["name"] for item in SUB_AGENT_SUMMARIES],
        "supporting_vexter_prs": [75, 74, 73, 72, 71],
        "task_id": TASK_ID,
        "template_runtime_validation_errors": runtime_errors,
        "verified_dexter_main_commit": VERIFIED_DEXTER_COMMIT,
        "verified_dexter_pr": 3,
        "verified_mewx_frozen_commit": VERIFIED_MEWX_COMMIT,
        "verified_prs": [75, 74, 73],
        "date": run_timestamp.split("T", 1)[0],
    }
    rewrite_local_ledger(ledger_payload)

    update_readme()


if __name__ == "__main__":
    main()
