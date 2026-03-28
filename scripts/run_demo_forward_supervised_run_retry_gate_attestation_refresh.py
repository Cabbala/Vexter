#!/usr/bin/env python3
"""Emit bounded retry-gate attestation-refresh surfaces from the regeneration baseline."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vexter.demo_readiness.external_evidence import (
    CONTRACT_SPEC_REL_PATH,
    GAP_PROOF_REL_PATH,
    GAP_REPORT_REL_PATH,
    GAP_SUMMARY_REL_PATH,
    MANIFEST_REL_PATH as EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
    PREFLIGHT_PROOF_REL_PATH,
    PREFLIGHT_REPORT_REL_PATH,
    PREFLIGHT_SUMMARY_REL_PATH,
    write_external_evidence_artifacts,
)
from vexter.planner_router.transport import DexterDemoRuntimeConfig

from scripts.run_demo_forward_supervised_run_retry_gate_attestation_record_pack import (
    boundary_lines,
)
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

CHECKLIST_PATH = (
    ROOT / "docs" / "demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md"
)
DECISION_SURFACE_PATH = (
    ROOT / "docs" / "demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md"
)
SPEC_PATH = ROOT / "specs" / "DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_REFRESH.md"
PLAN_PATH = ROOT / "plans" / "demo_forward_supervised_run_retry_gate_attestation_refresh_plan.md"

PREVIOUS_REPORT_PATH = (
    ROOT
    / "artifacts"
    / "reports"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md"
)
PREVIOUS_STATUS_PATH = (
    ROOT
    / "artifacts"
    / "reports"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md"
)
PREVIOUS_PROOF_PATH = (
    ROOT
    / "artifacts"
    / "proofs"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json"
)
PREVIOUS_SUMMARY_PATH = (
    ROOT
    / "artifacts"
    / "proofs"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-summary.md"
)
PREVIOUS_HANDOFF_PATH = (
    ROOT
    / "artifacts"
    / "reports"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration"
    / "HANDOFF.md"
)
PREVIOUS_CHECKLIST_PATH = (
    ROOT
    / "docs"
    / "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md"
)
PREVIOUS_DECISION_SURFACE_PATH = (
    ROOT
    / "docs"
    / "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md"
)
PREVIOUS_SUBAGENTS_PATH = (
    ROOT
    / "artifacts"
    / "reports"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration"
    / "SUBAGENTS.md"
)

REPORT_DIR = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-refresh"
)
REPORT_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-refresh-report.md"
)
STATUS_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-refresh-status.md"
)
SUBAGENTS_PATH = REPORT_DIR / "SUBAGENTS.md"
SUBAGENT_SUMMARY_PATH = REPORT_DIR / "subagent_summary.md"
PROOF_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-attestation-refresh-check.json"
)
PROOF_SUMMARY_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-attestation-refresh-summary.md"
)

BUNDLE_PATH = "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-refresh.tar.gz"
BUNDLE_SOURCE = "/Users/cabbala/Downloads/vexter_attestation_refresh_bundle_latest.tar.gz"

TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH"
TASK_STATUS = "supervised_run_retry_gate_attestation_refresh_blocked"
KEY_FINDING = "supervised_run_retry_gate_attestation_refresh_blocked_on_missing_or_stale_fresh_evidence_locators"
CLAIM_BOUNDARY = "supervised_run_retry_gate_attestation_refresh_bounded"
CURRENT_LANE = "supervised_run_retry_gate_attestation_refresh"
NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION"
NEXT_TASK_STATE = "ready_for_attestation_record_pack_regeneration"
NEXT_TASK_LANE = "supervised_run_retry_gate_attestation_record_pack_regeneration"
PASS_NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
PASS_NEXT_TASK_STATE = "ready_for_supervised_run_retry_gate_recheck"
PASS_NEXT_TASK_LANE = "supervised_run_retry_gate"
DECISION = "retry_gate_review_blocked_pending_fresh_attestation_refresh_and_record_pack_regeneration"

VERIFIED_DEXTER_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
VERIFIED_MEWX_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
VERIFIED_VEXTER_PR = 97
VERIFIED_VEXTER_COMMIT = "1bde9ef2b19da11e8b61772e560dc3d60874c461"
VERIFIED_VEXTER_MERGED_AT = "2026-03-28T13:40:06Z"
SUPPORTING_VEXTER_PRS = [97, 96, 95, 93, 92]
VERIFIED_VEXTER_PRS = [97, 96, 95]

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
            "Reverified PR `#97` / merge commit `1bde9ef2b19da11e8b61772e560dc3d60874c461` as latest merged `main`, then traced the atomic current-pointer set that flips the repo from the PR #97 regeneration baseline back to refresh without inventing a pass claim or fabricating evidence.",
            "Confirmed the summary, context, manifest, ledger, bundle metadata, README, and refresh handoff surfaces all agree that refresh is current, regeneration is the blocked next step, and retry-gate remains only the pass successor.",
            "Confirmed the refresh-side gap, canonical manifest, evidence preflight, and handoff mappings stay internally consistent so the canonical manifest remains template-only/honest and the preflight stays fail-closed.",
        ],
    },
    {
        "name": "Euler",
        "lines": [
            "Confirmed the unchanged guardrail envelope: Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one active plan, one open position, explicit allowlist, small lot, bounded supervised window, outside-repo credential refs, and funded-live forbidden.",
            "Verified the planner/runtime boundary remains `prepare / start / status / stop / snapshot`, `manual_latched_stop_all` stays planner-owned, Dexter remains the real-demo seam, and frozen Mew-X stays unchanged on `sim_live`.",
            "The fail-closed control point remains the canonical template-only manifest plus blocked evidence preflight; no runtime, routing, or ownership boundary widens in this promotion.",
        ],
    },
    {
        "name": "Parfit",
        "lines": [
            "The smallest safe change set is the refresh generator provenance and honesty update, the regenerated refresh-side current-pointer artifacts, and the regression expectations that pin repo-wide current-task truth.",
            "Refresh should keep consuming the shared canonical contract, template, compatibility gap, and evidence-preflight outputs from the PR `#97` regeneration baseline instead of reintroducing or widening those surfaces.",
            "Merge readiness depends on rerunning the refresh path, rebuilding the proof bundle, validating the shared refresh/regeneration/retry-gate/evidence-preflight expectations, and finishing with full `python3.12 -m pytest -q`.",
        ],
    },
)

REGENERATION_COVERAGE_SUFFIX = (
    " The regenerated pack must keep that same bounded-window meaning without widening scope or implying "
    "retry execution success."
)
REGENERATION_TRIGGER_MARKER = "; regenerate the current record-pack face again whenever "
REGENERATION_LOCATOR_SUFFIX = (
    "; plus regenerated face name, regeneration timestamp, bundle-relative proof pointer, and one "
    "reviewer-readable locator path that reopens the same bounded-window evidence without exposing secrets"
)
REGENERATION_RESET_PREFIX = (
    "inherit freshness only while the underlying fresh locator remains current, reviewable, and inside "
    "the same bounded supervised window; reset the regenerated face to FAIL/BLOCKED when "
)
REGENERATION_RESET_SUFFIX = " or when the locator cannot be reopened without secrets"
REGENERATION_REVIEWABLE_SUFFIX = (
    " and the regenerated face points to the same bounded-window locator plus an explicit regeneration "
    "timestamp and reviewer-readable proof path"
)


def format_jsonl(payload: object) -> str:
    return json.dumps(payload, sort_keys=False) + "\n"


def format_marker(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)


def format_bool(value: bool) -> str:
    return "yes" if value else "no"


def strip_repeated_suffix(value: str, suffix: str) -> str:
    while value.endswith(suffix):
        value = value[: -len(suffix)].rstrip()
    return value


def extract_refresh_trigger(value: str) -> str:
    if REGENERATION_TRIGGER_MARKER in value:
        return value.split(REGENERATION_TRIGGER_MARKER, 1)[0].strip()
    return value.strip()


def extract_refresh_locator_shape(value: str) -> str:
    if REGENERATION_LOCATOR_SUFFIX in value:
        return value.split(REGENERATION_LOCATOR_SUFFIX, 1)[0].strip()
    return value.strip()


def extract_refresh_stale_condition(value: str) -> str:
    if value.startswith(REGENERATION_RESET_PREFIX):
        middle = value[len(REGENERATION_RESET_PREFIX) :]
        if REGENERATION_RESET_SUFFIX in middle:
            return middle.split(REGENERATION_RESET_SUFFIX, 1)[0].strip()
    return value.strip()


def extract_refresh_reviewable_condition(value: str) -> str:
    if REGENERATION_REVIEWABLE_SUFFIX in value:
        return value.split(REGENERATION_REVIEWABLE_SUFFIX, 1)[0].strip()
    return value.strip()


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


def build_refresh_trigger(stale_condition: str) -> str:
    return f"refresh before {stale_condition}; otherwise keep the face blocked for record-pack regeneration"


def build_minimum_fresh_locator_shape(locator_shape: str) -> str:
    return (
        f"{locator_shape}; plus one repo-visible fresh-enough verification timestamp inside the current bounded "
        "supervised window and a locator that can be reopened without exposing secrets"
    )


def build_usable_condition(reviewable_enough_when: str) -> str:
    return (
        f"{reviewable_enough_when} and the located evidence is still fresh enough for the current bounded "
        "supervised window"
    )


def build_refresh_rows(gap_faces: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for face in gap_faces:
        refresh_owner = face.get("refresh_owner", "").strip()
        refresh_trigger = build_refresh_trigger(face.get("stale_condition", "").strip())
        minimum_locator_shape = build_minimum_fresh_locator_shape(
            face.get("minimum_evidence_locator_shape", "").strip()
        )
        stale_condition = face.get("stale_condition", "").strip()
        usable_condition = build_usable_condition(
            face.get("usable_for_retry_gate_review_when", "").strip()
        )
        refreshed_face_covers = face.get("what_face_covers", "").strip()
        refresh_rule_complete = all(
            bool(value)
            for value in (
                refresh_owner,
                refreshed_face_covers,
                refresh_trigger,
                minimum_locator_shape,
                stale_condition,
                usable_condition,
            )
        )
        current_fresh_locator_present = bool(face.get("present"))
        current_fresh_enough = bool(face.get("fresh_enough"))
        usable_now = bool(face.get("current")) and bool(face.get("reviewable")) and not bool(
            face.get("blocked")
        )
        rows.append(
            {
                "name": face["name"],
                "repo_visible_marker": face["repo_visible_marker"],
                "refresh_owner": refresh_owner,
                "what_refreshed_face_covers": refreshed_face_covers,
                "refresh_trigger": refresh_trigger,
                "minimum_fresh_evidence_locator_shape": minimum_locator_shape,
                "stale_condition": stale_condition,
                "usable_for_retry_gate_review_when": usable_condition,
                "required_manifest_fields": list(face.get("required_manifest_fields", [])),
                "proof_paths_to_recheck": list(face.get("proof_paths_to_recheck", [])),
                "refresh_rule_complete": refresh_rule_complete,
                "current_fresh_evidence_locator_present": current_fresh_locator_present,
                "current_evidence_fresh_enough": current_fresh_enough,
                "usable_now": usable_now,
                "current_refresh_observation": face["current_observation"],
                "refresh_status": "PASS" if usable_now else "FAIL/BLOCKED",
            }
        )
    return rows


def build_refresh_checklist(rows: list[dict], runtime_errors: list[str]) -> dict[str, bool]:
    row_names = {row["name"] for row in rows}
    return {
        "runtime_guardrails_parse_cleanly": not runtime_errors,
        "all_required_faces_present": row_names == set(REQUIRED_FACE_NAMES),
        "all_refresh_owners_explicit": all(bool(row["refresh_owner"]) for row in rows),
        "all_refresh_triggers_explicit": all(bool(row["refresh_trigger"]) for row in rows),
        "all_minimum_fresh_locator_shapes_explicit": all(
            bool(row["minimum_fresh_evidence_locator_shape"]) for row in rows
        ),
        "all_stale_conditions_explicit": all(bool(row["stale_condition"]) for row in rows),
        "all_retry_gate_usable_conditions_explicit": all(
            bool(row["usable_for_retry_gate_review_when"]) for row in rows
        ),
        "all_current_fresh_evidence_locators_present": all(
            row["current_fresh_evidence_locator_present"] for row in rows
        ),
        "all_current_evidence_fresh_enough": all(row["current_evidence_fresh_enough"] for row in rows),
        "all_faces_usable_now": all(row["usable_now"] for row in rows),
        "record_pack_regeneration_ready": all(
            (
                row["refresh_rule_complete"],
                bool(row["refresh_owner"]),
                bool(row["refresh_trigger"]),
                bool(row["minimum_fresh_evidence_locator_shape"]),
                bool(row["stale_condition"]),
                bool(row["usable_for_retry_gate_review_when"]),
            )
            for row in rows
        ),
        "retry_gate_review_reopen_ready": all(row["usable_now"] for row in rows),
    }


def build_next_human_pass_lines(readiness: dict[str, object]) -> list[str]:
    next_human_pass = readiness["next_human_pass"]
    lines = [
        f"Keep manifest_role at template: {next_human_pass['hold_manifest_role_until_ready']}",
        f"Template-only false path: {next_human_pass['template_only_false_path']}",
        "Fill bounded window once: "
        + ", ".join(next_human_pass["bounded_window_fields_once"]),
    ]
    for face in next_human_pass["faces"]:
        blocker_groups = "; ".join(
            f"{group}={', '.join(reasons)}"
            for group, reasons in face["blocked_reason_groups"].items()
        )
        lines.append(
            f"{face['face']}: fill {', '.join(face['manifest_fields_to_fill'])}; "
            f"blockers {blocker_groups or 'none'}; operator input {face['operator_input_needed']}"
        )
    lines.extend(
        [
            "Rerun in order: " + " -> ".join(next_human_pass["rerun_sequence"]),
            f"Optional legacy compatibility rerun: {next_human_pass['legacy_compatibility_command']}",
        ]
    )
    return lines


def build_status() -> str:
    return f"""# {TASK_ID} Status

- task_id: `{TASK_ID}`
- task_state: `{TASK_STATUS}`
- run_outcome: `FAIL/BLOCKED`
- key_finding: `{KEY_FINDING}`
- claim_boundary: `{CLAIM_BOUNDARY}`
- verified_vexter_main_pr: `{VERIFIED_VEXTER_PR}`
- verified_vexter_main_commit: `{VERIFIED_VEXTER_COMMIT}`
- verified_dexter_main_commit: `{VERIFIED_DEXTER_COMMIT}`
- verified_mewx_frozen_commit: `{VERIFIED_MEWX_COMMIT}`
- baseline_task: `DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION`
- baseline_task_state: `supervised_run_retry_gate_attestation_record_pack_regeneration_blocked`
- planner_boundary: `prepare/start/status/stop/snapshot`
- current_attestation_refresh_lane: `{CURRENT_LANE}`
- recommended_next_step: `{NEXT_TASK_LANE}`
- refresh_pass_successor: `{PASS_NEXT_TASK_LANE}`
"""


def build_current_report(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    rows: list[dict],
    gap_payload: dict[str, object],
    preflight_payload: dict[str, object],
) -> str:
    blocked_faces = [row["name"] for row in rows if row["refresh_status"] != "PASS"]
    refresh_rules_explicit_count = sum(row["refresh_rule_complete"] for row in rows)
    manifest = gap_payload["manifest"]
    readiness = preflight_payload["reopen_readiness"]
    next_human_pass_lines = build_next_human_pass_lines(readiness)
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Refresh Report

## Verified GitHub State
- Reverified latest GitHub-visible Vexter `main` at merged PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`.
- Dexter stayed pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen Mew-X stayed pinned at `{VERIFIED_MEWX_COMMIT}`.
- Report timestamp: `{run_timestamp}`.

## Baseline Accepted
- Accepted `supervised_run_retry_gate_attestation_record_pack_regeneration_blocked` as the bounded baseline current source of truth.
- Did not claim regenerated record-pack success, retry-gate reopen, retry execution success, funded live access, or any Mew-X seam expansion.
- Promoted one bounded attestation refresh lane as the new current source of truth for additional freshness ownership, triggers, and locator expectations on top of the regeneration baseline.
- Kept refresh consuming the shared canonical outside-repo evidence manifest, validator, and evidence preflight / compatibility gap surfaces added by the earlier regeneration work instead of re-deriving blockers from older lane prose.

## Refresh Boundary
{chr(10).join(f"- {line}" for line in boundary_lines())}

## Decision
- Outcome: `FAIL/BLOCKED`
- Decision: `{DECISION}`
- Current lane: `{CURRENT_LANE}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Retry-gate pass successor: `{PASS_NEXT_TASK_LANE}`
- Runtime validation errors: `{json.dumps(list(runtime_config.validation_errors()))}`

## Refresh Surfaces
- current status report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-status.md`
- current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md`
- current summary: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-summary.md`
- current proof json: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json`
- current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md`
- attestation refresh checklist: `docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md`
- attestation refresh decision surface: `docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md`
- current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/SUBAGENTS.md`

## Canonical External Evidence
- contract spec: `{CONTRACT_SPEC_REL_PATH}`
- manifest template: `{EXTERNAL_EVIDENCE_MANIFEST_REL_PATH}`
- preflight proof: `{PREFLIGHT_PROOF_REL_PATH}`
- preflight report: `{PREFLIGHT_REPORT_REL_PATH}`
- preflight summary: `{PREFLIGHT_SUMMARY_REL_PATH}`
- gap proof: `{GAP_PROOF_REL_PATH}`
- gap report: `{GAP_REPORT_REL_PATH}`
- gap summary: `{GAP_SUMMARY_REL_PATH}`
- manifest status: `{manifest['status']}`
- preflight status: `{readiness['status']}`
- blocked faces from canonical validator: `{", ".join(readiness['blocked_faces'])}`
- aggregated blocked reasons: `{json.dumps(readiness['blocked_reason_counts'], sort_keys=True)}`
- canonical face-to-manifest map: `{PREFLIGHT_REPORT_REL_PATH}` under `Face-To-Manifest And Proof Map`
- template-only false path: `{readiness['template_only_false_path']}`
- consistency checks: `{json.dumps(readiness['consistency_checks'], sort_keys=True)}`

## Next Human Pass
{chr(10).join(f"- {line}" for line in next_human_pass_lines)}

## Refresh Findings
- required refresh faces: `{len(rows)}`
- refresh rules explicit count: `{refresh_rules_explicit_count}`
- current fresh evidence locator present count: `{sum(row["current_fresh_evidence_locator_present"] for row in rows)}`
- current evidence fresh-enough count: `{sum(row["current_evidence_fresh_enough"] for row in rows)}`
- usable now count: `{sum(row["usable_now"] for row in rows)}`
- blocked refresh faces: `{", ".join(blocked_faces)}`

## Honest Model
- `PASS` only if every required face has explicit refresh ownership and freshness rules plus one current, fresh-enough, reviewable evidence locator sufficient to rerun record-pack regeneration and reopen retry-gate review honestly.
- `FAIL/BLOCKED` if any face remains missing, stale, ambiguous, non-refreshable, or not usable enough for retry-gate review.
- Current result remains `FAIL/BLOCKED` because the canonical manifest is `{manifest['status']}`, the preflight status remains `{readiness['status']}`, and the repo still does not point to current, fresh-enough, reviewer-readable evidence locators for the required faces, so record-pack regeneration cannot yet be rerun honestly.
"""


def build_proof_summary(gap_payload: dict[str, object], preflight_payload: dict[str, object]) -> str:
    return f"""# {TASK_ID} Proof Summary

- Verified latest GitHub-visible Vexter `main` at PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}`.
- Accepted attestation record-pack regeneration as the bounded baseline current source of truth.
- Re-promoted attestation refresh as the current operator-visible lane for additional freshness ownership, triggers, fresh locator shape, stale rules, and retry-gate usability.
- Revalidated refresh against the shared canonical external-evidence contract at `{CONTRACT_SPEC_REL_PATH}`, preflight report `{PREFLIGHT_REPORT_REL_PATH}`, and compatibility gap report `{GAP_REPORT_REL_PATH}`.
- Held the result at `FAIL/BLOCKED` because the manifest status is `{gap_payload['manifest']['status']}`, the preflight status is `{preflight_payload['reopen_readiness']['status']}`, the template-only false path remains `{preflight_payload['reopen_readiness']['template_only_false_path']}`, and current fresh-enough evidence locators are still missing or stale.
- Recommended next step: `{NEXT_TASK_LANE}`.
- Retry-gate pass successor: `{PASS_NEXT_TASK_LANE}`.
"""


def build_spec() -> str:
    boundary = "\n".join(f"- {line}" for line in boundary_lines())
    return f"""# DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_REFRESH

## Goal
Promote a bounded `attestation_refresh` lane as the current source of truth after attestation record-pack regeneration, without fabricating regenerated current records, retry-gate reopen, or retry execution success.

## Boundary
{boundary}

## Required Current Surfaces
- current status report
- current report
- current summary
- current proof json
- current handoff
- attestation refresh checklist
- attestation refresh decision surface
- canonical external evidence contract
- canonical external evidence manifest
- canonical evidence preflight proof / report / summary
- canonical external evidence gap proof / gap report / gap summary
- next recommended step

## Honest Refresh Model
- `PASS`: every required record face has explicit refresh rules plus one current, fresh-enough, reviewable evidence locator sufficient to rerun record-pack regeneration and reopen retry-gate review honestly
- `FAIL/BLOCKED`: one or more record faces remain missing, stale, ambiguous, non-refreshable, or not usable enough for retry-gate review

## Required Refresh Face Detail
Each refresh face must make explicit:
- refresh owner
- refresh trigger
- minimum fresh evidence locator shape
- stale condition
- what makes the refreshed face usable for retry-gate review

The lane must derive those fields from the canonical external-evidence validator instead of re-parsing older lane prose.

## Planner Boundary
- `prepare`
- `start`
- `status`
- `stop`
- `snapshot`
- `manual_latched_stop_all` remains planner-owned

## Out Of Scope
- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success
- no secret material committed to repo

## Result Model
The promoted lane remains fail-closed until fresh-enough current evidence locators exist for every required face and the current attestation record-pack regeneration can be rerun honestly for retry-gate review.
"""


def build_plan() -> str:
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Refresh Plan

## Implementation Steps
1. Reverify the latest GitHub-visible Vexter `main` state at PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}`.
2. Accept attestation record-pack regeneration as the blocked baseline current source of truth.
3. Keep refresh consuming the shared canonical outside-repo evidence manifest template, contract, validator, and unified evidence preflight / reopen-readiness surface from the regeneration baseline.
4. Regenerate the explicit next-human-pass checklist plus template-only false-path explanation from the canonical preflight blockers.
5. Generate one bounded attestation refresh lane with current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.
6. For each required face, carry forward the repo-visible marker and regeneration owner, then fix refresh trigger, minimum fresh evidence locator shape, stale condition, and retry-gate-usable rule from the canonical gap output.
7. Keep `FAIL/BLOCKED` unless every face points to a current, fresh-enough, reviewable evidence locator.
8. Recommend `{NEXT_TASK_LANE}` while blocked and expose `{PASS_NEXT_TASK_LANE}` only as the pass successor.

## Guardrails
{chr(10).join(f"- {line}" for line in boundary_lines())}

## Validation
- generate the canonical evidence preflight with `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py`
- generate the lane with `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py`
- verify pointer-sensitive shared surfaces with `python3.12 -m pytest -q tests/test_demo_forward_supervised_run_retry_gate_attestation_refresh.py tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py tests/test_demo_forward_supervised_run_retry_gate.py tests/test_demo_forward_supervised_run_retry_gate_evidence_preflight.py tests/test_demo_forward_supervised_run_retry_gate_external_evidence_gap.py`
- rebuild the tarball with `./scripts/build_proof_bundle.sh`
- finish with `python3.12 -m pytest -q`
"""


def build_checklist(rows: list[dict]) -> str:
    face_lines = []
    for row in rows:
        face_lines.append(
            "| "
            f"`{row['name']}` | "
            f"`{row['refresh_owner']}` | "
            f"{row['refresh_trigger']} | "
            f"{row['minimum_fresh_evidence_locator_shape']} | "
            f"{row['stale_condition']} | "
            f"{row['usable_for_retry_gate_review_when']} |"
        )
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Refresh Checklist

## Required Runtime Markers
- `DEXTER_DEMO_CREDENTIAL_SOURCE`
- `DEXTER_DEMO_VENUE_REF`
- `DEXTER_DEMO_ACCOUNT_REF`
- `DEXTER_DEMO_CONNECTIVITY_PROFILE`
- `DEXTER_DEMO_ALLOWED_SYMBOLS`
- `DEXTER_DEMO_DEFAULT_SYMBOL`
- `DEXTER_DEMO_ORDER_SIZE_LOTS`
- `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`
- `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`
- `DEXTER_DEMO_WINDOW_MINUTES=15`
- `manual_latched_stop_all`
- terminal snapshot readability
- funded live forbidden

## Review Steps
1. Start at `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json`.
4. Review the canonical manifest template at `manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json`.
5. Review the canonical evidence preflight report at `artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md`.
6. Use the `Next Human Pass Checklist` section in `artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md` as the canonical fill order and false-path explanation.
7. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md`.
8. Use `docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md` as the single attestation refresh decision surface.
9. Keep one refresh row per required face: credential source, venue ref, account ref, connectivity profile, operator owner, bounded start criteria, allowlist / symbol / lot reconfirmation, `manual_latched_stop_all` visibility, and terminal snapshot readability.
10. For every row, confirm refresh owner, refresh trigger, minimum fresh evidence locator shape, stale condition, and what makes the refreshed face usable for retry-gate review are explicit.
11. For every row, record whether a current fresh-enough bounded-window locator is present without embedding secret material.
12. Hold the lane at `FAIL/BLOCKED` until every required face is current, fresh enough, and usable enough to rerun the current record-pack regeneration honestly.

## Refresh Faces
| Refresh face | Refresh owner | Refresh trigger | Minimum fresh evidence locator shape | Stale condition | Usable for retry-gate review when |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(face_lines)}
"""


def build_decision_surface(rows: list[dict]) -> str:
    lines = [
        "# Demo Forward Supervised Run Retry Gate Attestation Refresh Decision Surface",
        "",
        "This decision surface is the current source of truth for `supervised_run_retry_gate_attestation_refresh`.",
        "",
        "| Refresh face | Repo-visible marker | Refresh owner | What the refreshed face covers | Refresh trigger | Minimum fresh evidence locator shape | Stale condition | Usable for retry-gate review when | Refresh rule complete | Current fresh evidence locator present | Current evidence fresh enough | Usable now | Current refresh observation | Refresh status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"`{row['name']}` | "
            f"`{format_marker(row['repo_visible_marker'])}` | "
            f"`{row['refresh_owner']}` | "
            f"{row['what_refreshed_face_covers']} | "
            f"{row['refresh_trigger']} | "
            f"{row['minimum_fresh_evidence_locator_shape']} | "
            f"{row['stale_condition']} | "
            f"{row['usable_for_retry_gate_review_when']} | "
            f"`{format_bool(row['refresh_rule_complete'])}` | "
            f"`{format_bool(row['current_fresh_evidence_locator_present'])}` | "
            f"`{format_bool(row['current_evidence_fresh_enough'])}` | "
            f"`{format_bool(row['usable_now'])}` | "
            f"{row['current_refresh_observation']} | "
            f"`{row['refresh_status']}` |"
        )
    lines.extend(
        [
            "",
            "Retry-gate review does not reopen unless every record face points to a current, fresh-enough, reviewable evidence locator.",
            f"While blocked, the next recommended step is `{NEXT_TASK_LANE}` so the record-pack regeneration can be rerun from refreshed evidence, and the pass successor remains `{PASS_NEXT_TASK_LANE}`.",
        ]
    )
    return "\n".join(lines)


def build_details(manifest_status: str, preflight_status: str) -> str:
    return f"""# ATTESTATION-REFRESH Details

## Verified Starting Point
- Latest Vexter `main`: PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`
- Dexter pinned commit: `{VERIFIED_DEXTER_COMMIT}`
- Frozen Mew-X commit: `{VERIFIED_MEWX_COMMIT}`
- Accepted baseline: `supervised_run_retry_gate_attestation_record_pack_regeneration_blocked`

## Deliverable
Promote one bounded attestation refresh lane that keeps current status, report, summary, proof, handoff, checklist, and decision-surface pointers coherent while fail-closing retry-gate review until every required face has a current, fresh-enough, reviewable evidence locator and the current record-pack regeneration can be rerun honestly. The canonical external-evidence manifest currently sits at status `{manifest_status}`, the evidence preflight remains `{preflight_status}`, and the repo therefore stays blocker-facing rather than pass-claiming.
"""


def build_min_prompt(manifest_status: str, preflight_status: str) -> str:
    return (
        f"GitHub latest state is Vexter main PR #{VERIFIED_VEXTER_PR} merge commit "
        f"{VERIFIED_VEXTER_COMMIT} on {VERIFIED_VEXTER_MERGED_AT}. "
        "Accept attestation record-pack regeneration as baseline, promote attestation refresh as the current source of truth, "
        f"keep Dexter-only paper_live and frozen Mew-X sim_live, consume the canonical evidence preflight and compatibility gap surfaces with manifest status {manifest_status} and preflight status {preflight_status}, "
        "do not commit secrets, keep the lane FAIL/BLOCKED until every face has a current fresh-enough evidence locator, and recommend "
        f"{NEXT_TASK_LANE} before any retry-gate reopen."
    )


def build_handoff(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    rows: list[dict],
    gap_payload: dict[str, object],
    preflight_payload: dict[str, object],
) -> str:
    face_lines = "\n".join(
        "- "
        f"{row['name']}: refresh_rule_complete={str(row['refresh_rule_complete']).lower()}, "
        f"current_fresh_evidence_locator_present={str(row['current_fresh_evidence_locator_present']).lower()}, "
        f"current_evidence_fresh_enough={str(row['current_evidence_fresh_enough']).lower()}, "
        f"usable_now={str(row['usable_now']).lower()}, "
        f"refresh_owner={row['refresh_owner']}"
        for row in rows
    )
    next_human_pass_lines = "\n".join(
        f"- {line}" for line in build_next_human_pass_lines(preflight_payload["reopen_readiness"])
    )
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Refresh Handoff

## Current Status
- outgoing_shift_window: {run_timestamp} attestation-refresh lane
- incoming_shift_window: fresh locator collection and record-pack regeneration
- task_state: {TASK_STATUS}
- shift_outcome: blocked
- current_action: hold_retry_gate_review_until_attestation_refresh_is_current_and_record_pack_can_be_regenerated
- current_lane: {CURRENT_LANE}
- recommended_next_step_while_blocked: {NEXT_TASK_LANE}
- refresh_pass_successor: {PASS_NEXT_TASK_LANE}
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: {VERIFIED_VEXTER_COMMIT}
- dexter_main_commit: {VERIFIED_DEXTER_COMMIT}
- mewx_frozen_commit: {VERIFIED_MEWX_COMMIT}
- baseline_attestation_record_pack_regeneration_task_state: supervised_run_retry_gate_attestation_record_pack_regeneration_blocked

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-status.md
- current_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md
- current_proof_summary: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-summary.md
- current_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json
- current_attestation_refresh_checklist: docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md
- current_attestation_refresh_decision_surface: docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md
- current_subagent_summary: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/SUBAGENTS.md
- canonical_external_evidence_contract: {CONTRACT_SPEC_REL_PATH}
- canonical_external_evidence_manifest: {EXTERNAL_EVIDENCE_MANIFEST_REL_PATH}
- canonical_external_evidence_preflight_report: {PREFLIGHT_REPORT_REL_PATH}
- canonical_external_evidence_preflight_proof: {PREFLIGHT_PROOF_REL_PATH}
- canonical_external_evidence_preflight_summary: {PREFLIGHT_SUMMARY_REL_PATH}
- canonical_external_evidence_gap_report: {GAP_REPORT_REL_PATH}
- canonical_external_evidence_gap_proof: {GAP_PROOF_REL_PATH}
- canonical_external_evidence_gap_summary: {GAP_SUMMARY_REL_PATH}
- canonical_external_evidence_manifest_status: {gap_payload['manifest']['status']}
- baseline_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md
- baseline_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md
- baseline_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json
- baseline_handoff: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md

## Canonical Evidence Intake Handoff
- bounded_window_fields_to_fill_once: {", ".join(gap_payload['manifest']['window_fields_to_fill'])}
- per_blocked_face_fields_to_fill: provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note
- canonical_face_to_manifest_map: {PREFLIGHT_REPORT_REL_PATH}
- canonical_machine_preflight_proof: {PREFLIGHT_PROOF_REL_PATH}
- canonical_legacy_gap_report: {GAP_REPORT_REL_PATH}
- proof_surfaces_to_rerun_after_manifest_update: {", ".join(gap_payload['manifest']['proof_paths_to_recheck'])}
- evidence_preflight_status: {preflight_payload['reopen_readiness']['status']}
- evidence_preflight_aggregated_blocked_reasons: {json.dumps(preflight_payload['reopen_readiness']['blocked_reason_counts'], sort_keys=True)}
- template_only_false_path: {preflight_payload['reopen_readiness']['template_only_false_path']}
- evidence_preflight_consistency_checks: {json.dumps(preflight_payload['reopen_readiness']['consistency_checks'], sort_keys=True)}
- rerun_gap_and_lane_commands:
  - {gap_payload['manifest']['rerun_commands'][0]}
  - {gap_payload['manifest']['rerun_commands'][1]}
  - {gap_payload['manifest']['rerun_commands'][2]}

## Next Human Pass Checklist
{next_human_pass_lines}

## Guardrails
- route_mode: single_sleeve
- selected_sleeve_id: dexter_default
- max_active_real_demo_plans: 1
- max_open_positions: {runtime_config.max_open_positions}
- allowlist_required: true
- allowlist_symbols: BONK/USDC
- demo_symbol: BONK/USDC
- small_lot_required: true
- small_lot_order_size: 0.05
- bounded_window_minutes: 15
- operator_supervised_window_required: true
- external_credential_refs_outside_repo: true
- operator_owner_explicit_required: true
- venue_connectivity_confirmation_required: true
- manual_latched_stop_all_visibility_reconfirmation_required: true
- terminal_snapshot_readability_reconfirmation_required: true
- mewx_overlay_enabled: false
- funded_live_allowed: false

## Refresh Faces
{face_lines}

## Open Questions
- question_1_or_none: who will replace the template manifest with current evidence locators for each required face without exposing secrets
- question_2_or_none: which refreshed evidence locator should seed the next record-pack regeneration rerun for venue, account, and connectivity faces
- question_3_or_none: who timestamps the bounded start window and operator owner for the next retry-gate recheck
- question_4_or_none: has `manual_latched_stop_all` visibility been freshly reconfirmed for the current bounded window
- question_5_or_none: has terminal snapshot readability been freshly reconfirmed for the current bounded window

## Next-Shift Priority Checks
- priority_check_1: keep the current lane blocked unless every face has a current, fresh-enough bounded-window locator and freshness check
- priority_check_2: recommend `{NEXT_TASK_LANE}` while blocked so the current record-pack regeneration can be rerun, and expose `{PASS_NEXT_TASK_LANE}` only as the pass successor
- priority_check_3: preserve Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, small-lot, one-position, `manual_latched_stop_all`, and funded-live-forbidden guardrails

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- checklist_pointer_checked: true
- decision_surface_pointer_checked: true
- subagent_summary_pointer_checked: true
- blocked_claim_boundary_explicit: true

This handoff promotes the bounded attestation refresh lane only. It does not claim regenerated record-pack success, reopened retry gate, completed retry execution, funded live access, or any Mew-X seam expansion.
"""


def build_subagents() -> str:
    lines = ["# Demo Forward Supervised Run Retry Gate Attestation Refresh Sub-agent Summaries", ""]
    for item in SUB_AGENT_SUMMARIES:
        lines.append(f"## {item['name']}")
        for line in item["lines"]:
            lines.append(f"- {line}")
        lines.append("")
    return "\n".join(lines)


def update_readme() -> None:
    marker = (
        "`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH` starts from latest "
        "GitHub-visible Vexter `main`"
    )
    regeneration_marker = (
        "`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION` starts from latest "
        "GitHub-visible Vexter `main`"
    )
    readme_text = README_PATH.read_text()
    entry = (
        "`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH` starts from latest "
        f"GitHub-visible Vexter `main` at merged PR `#{VERIFIED_VEXTER_PR}` merge commit "
        f"`{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`, keeps Dexter pinned at merged PR "
        f"`#3` commit `{VERIFIED_DEXTER_COMMIT}`, and keeps frozen Mew-X at `{VERIFIED_MEWX_COMMIT}`. "
        "It accepts the bounded attestation-record-pack-regeneration lane as baseline and promotes one fail-closed "
        "attestation-refresh lane instead: the repo now fixes the current status/report/proof/handoff/"
        "checklist/decision-surface surfaces for refresh owner, refresh trigger, minimum fresh evidence "
        "locator shape, stale condition, and what makes each refreshed face usable for retry-gate review, while "
        "continuing to consume the shared canonical non-secret external-evidence manifest, validator, and evidence preflight / "
        "compatibility gap path that refresh and regeneration already share, plus one explicit "
        "next-human-pass checklist and template-only false-path explanation for the first real evidence submission, while "
        "keeping the Dexter-only `paper_live` seam, leaving Mew-X unchanged on `sim_live`, and keeping "
        "funded live forbidden. The resulting status is "
        f"`{TASK_STATUS}` with `{CLAIM_BOUNDARY}`, the current lane is `{CURRENT_LANE}`, the blocked next "
        f"recommended step is `{NEXT_TASK_LANE}` so the record-pack regeneration can be rerun from refreshed inputs, "
        f"and the pass successor is `{PASS_NEXT_TASK_LANE}`."
    )
    line_re = re.compile(rf"(?m)^{re.escape(marker)}.*$")
    updated = line_re.sub("", readme_text)
    regeneration_re = re.compile(rf"(?m)^{re.escape(regeneration_marker)}.*$")
    matches = list(regeneration_re.finditer(updated))
    match = matches[-1] if matches else None
    if match:
        updated = updated[: match.end()] + "\n" + entry + "\n\n" + updated[match.end() :].lstrip("\n")
    else:
        updated = updated.rstrip() + "\n\n" + entry + "\n"
    README_PATH.write_text(updated)


def main() -> None:
    run_timestamp = iso_utc_now()
    template_env = parse_template_env(TEMPLATE_ENV_PATH)
    previous_proof = read_json(PREVIOUS_PROOF_PATH)

    with patched_demo_env(template_env):
        runtime_config = DexterDemoRuntimeConfig.from_env()
        runtime_errors = list(runtime_config.validation_errors())

    external_evidence = write_external_evidence_artifacts(ROOT, template_env, runtime_config)
    gap_payload = external_evidence["gap"]
    preflight_payload = external_evidence["preflight"]
    rows = build_refresh_rows(preflight_payload["faces"])
    blocked_refresh_faces = [row["name"] for row in rows if row["refresh_status"] != "PASS"]
    checklist_attestation = build_refresh_checklist(rows, runtime_errors)

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
            "task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION",
            "task_state": "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked",
            "report": str(PREVIOUS_REPORT_PATH.relative_to(ROOT)),
            "status_report": str(PREVIOUS_STATUS_PATH.relative_to(ROOT)),
            "proof": str(PREVIOUS_PROOF_PATH.relative_to(ROOT)),
            "summary": str(PREVIOUS_SUMMARY_PATH.relative_to(ROOT)),
            "handoff": str(PREVIOUS_HANDOFF_PATH.relative_to(ROOT)),
            "checklist": str(PREVIOUS_CHECKLIST_PATH.relative_to(ROOT)),
            "decision_surface": str(PREVIOUS_DECISION_SURFACE_PATH.relative_to(ROOT)),
            "subagent_summary": str(PREVIOUS_SUBAGENTS_PATH.relative_to(ROOT)),
        },
        "supervised_run_retry_gate_attestation_refresh": {
            "planner_boundary": ["prepare", "start", "status", "stop", "snapshot"],
            "attestation_refresh_boundary": {
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
                "current_status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-status.md",
                "current_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md",
                "current_summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-summary.md",
                "current_proof_json": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json",
                "current_handoff": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md",
                "attestation_refresh_checklist": "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md",
                "attestation_refresh_decision_surface": "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md",
                "external_evidence_contract": CONTRACT_SPEC_REL_PATH,
                "external_evidence_manifest": EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
                "external_evidence_preflight_report": PREFLIGHT_REPORT_REL_PATH,
                "external_evidence_preflight_proof": PREFLIGHT_PROOF_REL_PATH,
                "external_evidence_preflight_summary": PREFLIGHT_SUMMARY_REL_PATH,
                "external_evidence_gap_report": GAP_REPORT_REL_PATH,
                "external_evidence_gap_proof": GAP_PROOF_REL_PATH,
                "external_evidence_gap_summary": GAP_SUMMARY_REL_PATH,
                "next_recommended_step": NEXT_TASK_LANE,
                "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/SUBAGENTS.md",
            },
            "baseline_attestation_record_pack_regeneration_outcome": {
                "task_id": previous_proof["task_id"],
                "task_state": previous_proof["task_result"]["task_state"],
                "key_finding": previous_proof["task_result"]["key_finding"],
                "claim_boundary": previous_proof["task_result"]["claim_boundary"],
                "recommended_next_step": previous_proof["task_result"]["recommended_next_step"],
                "gate_pass_successor": previous_proof["task_result"]["gate_pass_successor"],
            },
            "refresh_faces": {
                "attestation_refresh_decision_surface": rows,
                "blocked_refresh_faces": blocked_refresh_faces,
                "checklist_attestation_refresh": checklist_attestation,
                "record_pack_regeneration_ready": checklist_attestation[
                    "record_pack_regeneration_ready"
                ],
                "retry_gate_review_reopen_ready": False,
            },
            "canonical_external_evidence": {
                "contract_spec": CONTRACT_SPEC_REL_PATH,
                "manifest_path": EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
                "preflight_proof": PREFLIGHT_PROOF_REL_PATH,
                "preflight_report": PREFLIGHT_REPORT_REL_PATH,
                "preflight_summary": PREFLIGHT_SUMMARY_REL_PATH,
                "preflight_status": preflight_payload["reopen_readiness"]["status"],
                "gap_proof": GAP_PROOF_REL_PATH,
                "gap_report": GAP_REPORT_REL_PATH,
                "gap_summary": GAP_SUMMARY_REL_PATH,
                "manifest_status": gap_payload["manifest"]["status"],
                "retry_gate_review_reopen_ready": preflight_payload["reopen_readiness"][
                    "retry_gate_review_reopen_ready"
                ],
                "aggregated_blocked_reason_counts": preflight_payload["reopen_readiness"][
                    "blocked_reason_counts"
                ],
                "template_only_false_path": preflight_payload["reopen_readiness"][
                    "template_only_false_path"
                ],
                "consistency_checks": preflight_payload["reopen_readiness"][
                    "consistency_checks"
                ],
                "next_human_pass": preflight_payload["reopen_readiness"]["next_human_pass"],
            },
            "sub_agents": list(SUB_AGENT_SUMMARIES),
            "supporting_files": [
                CONTRACT_SPEC_REL_PATH,
                EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md",
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_REFRESH.md",
                "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md",
                "plans/demo_forward_supervised_run_retry_gate_attestation_refresh_plan.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md",
                PREFLIGHT_PROOF_REL_PATH,
                PREFLIGHT_REPORT_REL_PATH,
                PREFLIGHT_SUMMARY_REL_PATH,
                GAP_PROOF_REL_PATH,
                GAP_REPORT_REL_PATH,
                GAP_SUMMARY_REL_PATH,
                "scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
                "scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
                "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
                "scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
                "scripts/export_attestation_refresh_closeout_bundle.sh",
                "scripts/build_proof_bundle.sh",
                "vexter/demo_readiness/__init__.py",
                "vexter/demo_readiness/external_evidence.py",
                "tests/test_demo_forward_supervised_run_retry_gate.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
                "tests/test_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
                "tests/test_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
                "tests/test_bootstrap_layout.py",
            ],
            "proof_outputs": [
                PREFLIGHT_PROOF_REL_PATH,
                PREFLIGHT_SUMMARY_REL_PATH,
                GAP_PROOF_REL_PATH,
                GAP_SUMMARY_REL_PATH,
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json",
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-summary.md",
                "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-refresh.tar.gz",
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

    report_text = build_current_report(
        run_timestamp,
        runtime_config,
        rows,
        gap_payload,
        preflight_payload,
    )
    status_text = build_status()
    proof_summary_text = build_proof_summary(gap_payload, preflight_payload)
    summary_text = f"""# {TASK_ID} Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## What This Task Did

- Accepted attestation record-pack regeneration as the baseline current source of truth.
- Re-promoted attestation refresh to the current operator-visible lane.
- Kept attestation refresh consuming the shared canonical external-evidence contract, manifest template, validator, and evidence preflight / reopen-readiness path from the regeneration baseline.
- Regenerated the explicit next-human-pass checklist plus template-only false-path explanation derived from the canonical preflight blockers.
- Added current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces for refresh ownership, freshness triggers, locator shape, and retry-gate usability.
- Fixed one fail-closed refresh model that blocks retry-gate review until every required face has a current, fresh-enough, reviewable evidence locator.

## Decision

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task status: `{TASK_STATUS}`
- Current lane: `{CURRENT_LANE}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Refresh pass successor: `{PASS_NEXT_TASK_LANE}`
- Decision: `{DECISION}`
- Canonical external evidence manifest status: `{gap_payload["manifest"]["status"]}`

## Key Paths

- Current spec: `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_REFRESH.md`
- Current implementation plan: `plans/demo_forward_supervised_run_retry_gate_attestation_refresh_plan.md`
- Current checklist: `docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md`
- Current decision surface: `docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md`
- Current proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json`
- Current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md`
- Current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md`
- Current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/SUBAGENTS.md`
- Canonical contract: `{CONTRACT_SPEC_REL_PATH}`
- Evidence template: `{EXTERNAL_EVIDENCE_MANIFEST_REL_PATH}`
- Preflight report: `{PREFLIGHT_REPORT_REL_PATH}`
- Gap report: `{GAP_REPORT_REL_PATH}`
- Current bundle target: `artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-refresh.tar.gz`
"""

    prompt_context = {
        "task_id": TASK_ID,
        "task_state": TASK_STATUS,
        "current_lane": CURRENT_LANE,
        "recommended_next_step": NEXT_TASK_LANE,
        "recommended_next_task_id": NEXT_TASK_ID,
        "candidate_pass_next_step": PASS_NEXT_TASK_LANE,
        "candidate_pass_next_task_id": PASS_NEXT_TASK_ID,
        "verified_vexter_main_pr": VERIFIED_VEXTER_PR,
        "verified_vexter_main_commit": VERIFIED_VEXTER_COMMIT,
        "baseline_task_state": "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked",
        "first_demo_target": "dexter_paper_live",
        "source_faithful_seam": {"dexter": "paper_live", "mewx": "sim_live"},
        "external_evidence_manifest_status": gap_payload["manifest"]["status"],
        "external_evidence_preflight_status": preflight_payload["reopen_readiness"]["status"],
        "external_evidence_preflight_report": PREFLIGHT_REPORT_REL_PATH,
        "external_evidence_gap_report": GAP_REPORT_REL_PATH,
        "external_evidence_template_only_false_path": preflight_payload["reopen_readiness"][
            "template_only_false_path"
        ],
        "external_evidence_consistency_checks": preflight_payload["reopen_readiness"][
            "consistency_checks"
        ],
        "blocked_refresh_faces": blocked_refresh_faces,
        "record_pack_regeneration_ready": checklist_attestation["record_pack_regeneration_ready"],
        "retry_gate_review_reopen_ready": False,
    }

    details_text = build_details(
        gap_payload["manifest"]["status"],
        preflight_payload["reopen_readiness"]["status"],
    )
    min_prompt_text = build_min_prompt(
        gap_payload["manifest"]["status"],
        preflight_payload["reopen_readiness"]["status"],
    )
    handoff_text = build_handoff(
        run_timestamp,
        runtime_config,
        rows,
        gap_payload,
        preflight_payload,
    )
    subagents_text = build_subagents()
    spec_text = build_spec()
    plan_text = build_plan()
    checklist_text = build_checklist(rows)
    decision_surface_text = build_decision_surface(rows)

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
        "previous_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION",
        "previous_task_state": "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked",
        "previous_key_finding": "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked_on_missing_or_stale_regenerated_faces",
        "previous_claim_boundary": "supervised_run_retry_gate_attestation_record_pack_regeneration_bounded",
        "retry_gate_attestation_record_pack_regeneration_accepted_as_baseline": True,
        "retry_gate_attestation_refresh_repromoted_current": True,
    }
    context_pack["bundle_source"] = BUNDLE_SOURCE
    context_pack["current_contract"].update(
        {
            "demo_forward_supervised_run_retry_gate_attestation_refresh_marker": "demo_forward_supervised_run_retry_gate_attestation_refresh",
            "demo_forward_supervised_run_retry_gate_attestation_refresh_spec_path": "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_REFRESH.md",
            "demo_forward_supervised_run_retry_gate_attestation_refresh_plan_path": "plans/demo_forward_supervised_run_retry_gate_attestation_refresh_plan.md",
            "demo_forward_supervised_run_retry_gate_attestation_refresh_checklist_path": "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md",
            "demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface_path": "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md",
            "demo_forward_supervised_run_retry_gate_attestation_refresh_subagents_path": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/SUBAGENTS.md",
            "demo_forward_supervised_run_retry_gate_attestation_refresh_subagent_summary_path": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/subagent_summary.md",
            "demo_forward_retry_gate_attestation_refresh_current_lane": CURRENT_LANE,
            "demo_forward_retry_gate_attestation_refresh_next_step": NEXT_TASK_LANE,
            "demo_forward_retry_gate_attestation_refresh_pass_successor": PASS_NEXT_TASK_LANE,
            "demo_forward_retry_gate_external_evidence_contract_spec_path": CONTRACT_SPEC_REL_PATH,
            "demo_forward_retry_gate_external_evidence_manifest_path": EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
            "demo_forward_retry_gate_external_evidence_preflight_report_path": PREFLIGHT_REPORT_REL_PATH,
            "demo_forward_retry_gate_external_evidence_preflight_proof_path": PREFLIGHT_PROOF_REL_PATH,
            "demo_forward_retry_gate_external_evidence_preflight_summary_path": PREFLIGHT_SUMMARY_REL_PATH,
            "demo_forward_retry_gate_external_evidence_gap_report_path": GAP_REPORT_REL_PATH,
            "demo_forward_retry_gate_external_evidence_gap_proof_path": GAP_PROOF_REL_PATH,
            "demo_forward_retry_gate_external_evidence_gap_summary_path": GAP_SUMMARY_REL_PATH,
        }
    )
    context_pack["current_task"] = {
        "id": TASK_ID,
        "scope": [
            "Reverify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X after attestation record-pack regeneration merged.",
            "Accept attestation record-pack regeneration as the baseline current source of truth.",
            "Keep refresh consuming the shared canonical non-secret outside-repo evidence manifest, validator, and evidence preflight / reopen-readiness path from the regeneration baseline.",
            "Re-promote attestation refresh status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Make each required face explicit for refresh owner, refresh trigger, fresh locator shape, stale logic, and retry-gate usability from the canonical gap report.",
            "Keep retry-gate review blocked until every required face has a current, fresh-enough, reviewable evidence locator.",
        ],
        "deliverables": [
            "README.md",
            CONTRACT_SPEC_REL_PATH,
            EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
            "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_REFRESH.md",
            "plans/demo_forward_supervised_run_retry_gate_attestation_refresh_plan.md",
            "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md",
            "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md",
            PREFLIGHT_PROOF_REL_PATH,
            PREFLIGHT_REPORT_REL_PATH,
            PREFLIGHT_SUMMARY_REL_PATH,
            GAP_PROOF_REL_PATH,
            GAP_REPORT_REL_PATH,
            GAP_SUMMARY_REL_PATH,
            "scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
            "tests/test_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
            "tests/test_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
            "tests/test_demo_forward_supervised_run_retry_gate.py",
            "tests/test_demo_forward_supervised_run_retry_gate_input_attestation.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_audit.py",
            "tests/test_demo_forward_supervised_run_retry_readiness.py",
            "tests/test_bootstrap_layout.py",
            "scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
            "scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
            "scripts/export_attestation_refresh_closeout_bundle.sh",
            "scripts/build_proof_bundle.sh",
            "vexter/demo_readiness/__init__.py",
            "vexter/demo_readiness/external_evidence.py",
            "artifacts/summary.md",
            "artifacts/context_pack.json",
            "artifacts/proof_bundle_manifest.json",
            "artifacts/task_ledger.jsonl",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-status.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/DETAILS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/MIN_PROMPT.txt",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/CONTEXT.json",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/SUBAGENTS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/subagent_summary.md",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-summary.md",
            "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-refresh.tar.gz",
        ],
        "frozen_source_commits": {
            "dexter": VERIFIED_DEXTER_COMMIT,
            "mewx": VERIFIED_MEWX_COMMIT,
        },
    }
    for evidence_key, current_flags in (
        (
            "demo_forward_supervised_run_retry_readiness",
            {"operator_visible_readiness_surface_current": False},
        ),
        (
            "demo_forward_supervised_run_retry_gate",
            {"operator_visible_gate_surface_current": False},
        ),
        (
            "demo_forward_supervised_run_retry_gate_input_attestation",
            {"operator_visible_attestation_surface_current": False},
        ),
        (
            "demo_forward_supervised_run_retry_gate_attestation_audit",
            {"operator_visible_attestation_audit_surface_current": False},
        ),
        (
            "demo_forward_supervised_run_retry_gate_attestation_record_pack",
            {"operator_visible_attestation_record_pack_surface_current": False},
        ),
        (
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration",
            {"attestation_record_pack_regeneration_surface_current": False},
        ),
    ):
        if evidence_key in context_pack["evidence"]:
            context_pack["evidence"][evidence_key].update(current_flags)
    context_pack["evidence"]["github_latest"].update(
        {
            "latest_vexter_pr": VERIFIED_VEXTER_PR,
            "latest_vexter_main_commit": VERIFIED_VEXTER_COMMIT,
            "latest_recent_vexter_prs": SUPPORTING_VEXTER_PRS,
            "vexter_pr_95_merged_at": "2026-03-27T23:26:51Z",
            "vexter_pr_95_closed_at": "2026-03-27T23:26:51Z",
            "vexter_pr_96_merged_at": "2026-03-28T03:29:12Z",
            "vexter_pr_96_closed_at": "2026-03-28T03:29:12Z",
            "vexter_pr_97_merged_at": VERIFIED_VEXTER_MERGED_AT,
            "vexter_pr_97_closed_at": VERIFIED_VEXTER_MERGED_AT,
        }
    )
    context_pack["evidence"]["demo_forward_supervised_run_retry_gate_attestation_refresh"] = {
        "report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md",
        "status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-status.md",
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json",
        "summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-summary.md",
        "handoff_dir": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh",
        "checklist": "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md",
        "decision_surface": "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md",
        "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/SUBAGENTS.md",
        "key_finding": KEY_FINDING,
        "claim_boundary": CLAIM_BOUNDARY,
        "task_state": TASK_STATUS,
        "run_outcome": "FAIL/BLOCKED",
        "attestation_refresh_surface_current": True,
        "preferred_next_step": NEXT_TASK_LANE,
        "refresh_pass_successor": PASS_NEXT_TASK_LANE,
        "attestation_refresh_boundary": proof["supervised_run_retry_gate_attestation_refresh"][
            "attestation_refresh_boundary"
        ],
        "external_evidence_contract": CONTRACT_SPEC_REL_PATH,
        "external_evidence_manifest": EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
        "external_evidence_preflight_proof": PREFLIGHT_PROOF_REL_PATH,
        "external_evidence_preflight_report": PREFLIGHT_REPORT_REL_PATH,
        "external_evidence_preflight_summary": PREFLIGHT_SUMMARY_REL_PATH,
        "external_evidence_preflight_status": preflight_payload["reopen_readiness"]["status"],
        "external_evidence_gap_proof": GAP_PROOF_REL_PATH,
        "external_evidence_gap_report": GAP_REPORT_REL_PATH,
        "external_evidence_gap_summary": GAP_SUMMARY_REL_PATH,
        "external_evidence_manifest_status": gap_payload["manifest"]["status"],
        "blocked_refresh_faces": blocked_refresh_faces,
        "sub_agents": list(SUB_AGENT_SUMMARIES),
        "retry_gate_review_reopen_ready_from_external_evidence": preflight_payload["reopen_readiness"][
            "retry_gate_review_reopen_ready"
        ],
        "aggregated_blocked_reason_counts": preflight_payload["reopen_readiness"][
            "blocked_reason_counts"
        ],
        "template_only_false_path": preflight_payload["reopen_readiness"]["template_only_false_path"],
        "consistency_checks": preflight_payload["reopen_readiness"]["consistency_checks"],
        "next_human_pass": preflight_payload["reopen_readiness"]["next_human_pass"],
    }
    context_pack["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "rationale": [
            "Attestation refresh is now the current source of truth for additional freshness ownership, triggers, and evidence-locator requirements.",
            "The canonical external-evidence manifest now makes every remaining retry-gate blocker explicit, but one or more faces still remain template-only, incomplete, stale, or non-reviewable.",
            "Rerun the current attestation record-pack regeneration from refreshed inputs before any retry-gate recheck is considered.",
        ],
        "pass_successor": {
            "id": PASS_NEXT_TASK_ID,
            "state": PASS_NEXT_TASK_STATE,
            "lane": PASS_NEXT_TASK_LANE,
        },
    }
    context_pack["proofs"].update(
        {
            "demo_forward_supervised_run_retry_gate_attestation_refresh_added": True,
            "demo_forward_retry_gate_evidence_preflight_written": True,
            "demo_forward_retry_gate_attestation_refresh_current_pointers_fixed": True,
            "demo_forward_retry_gate_external_evidence_gap_written": True,
            "demo_forward_retry_gate_attestation_refresh_checklist_written": True,
            "demo_forward_retry_gate_attestation_refresh_decision_surface_written": True,
            "demo_forward_retry_gate_attestation_refresh_subagent_summary_written": True,
            "recommended_next_step_advances_to_attestation_record_pack_regeneration_when_blocked": True,
            "retry_gate_review_requires_current_fresh_enough_reviewable_locators": True,
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
        ("docs", "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md"),
        ("docs", "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md"),
        ("docs", CONTRACT_SPEC_REL_PATH),
        ("docs", EXTERNAL_EVIDENCE_MANIFEST_REL_PATH),
        ("scripts", "scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py"),
        ("scripts", "scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py"),
        ("scripts", "scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py"),
        ("scripts", "scripts/export_attestation_refresh_closeout_bundle.sh"),
        ("scripts", "vexter/demo_readiness/__init__.py"),
        ("scripts", "vexter/demo_readiness/external_evidence.py"),
        ("proof_files", PREFLIGHT_PROOF_REL_PATH),
        ("proof_files", PREFLIGHT_SUMMARY_REL_PATH),
        ("reports", PREFLIGHT_REPORT_REL_PATH),
        ("proof_files", GAP_PROOF_REL_PATH),
        ("proof_files", GAP_SUMMARY_REL_PATH),
        ("reports", GAP_REPORT_REL_PATH),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json"),
        ("proof_files", "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-summary.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-status.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/SUBAGENTS.md"),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/subagent_summary.md"),
    ):
        if path not in manifest[key]:
            manifest[key].append(path)
    for path in (
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_REFRESH.md",
        CONTRACT_SPEC_REL_PATH,
        "plans/demo_forward_supervised_run_retry_gate_attestation_refresh_plan.md",
        EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
        "scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
        "scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
        "tests/test_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
        "tests/test_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
        "tests/test_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
        "vexter/demo_readiness/__init__.py",
        "vexter/demo_readiness/external_evidence.py",
        PREFLIGHT_PROOF_REL_PATH,
        PREFLIGHT_REPORT_REL_PATH,
        PREFLIGHT_SUMMARY_REL_PATH,
        GAP_PROOF_REL_PATH,
        GAP_REPORT_REL_PATH,
        GAP_SUMMARY_REL_PATH,
        "scripts/export_attestation_refresh_closeout_bundle.sh",
        "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-refresh.tar.gz",
    ):
        if path not in manifest["included_paths"]:
            manifest["included_paths"].append(path)
    manifest["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "resume_requirements": [
            f"Keep Dexter pinned at {VERIFIED_DEXTER_COMMIT} and Mew-X frozen at {VERIFIED_MEWX_COMMIT}.",
            "Start from the current attestation refresh status, report, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Replace the template-only canonical external-evidence manifest with current non-secret evidence locators for every required face before rerunning the current record-pack regeneration.",
            "Collect one current, fresh-enough, reviewable evidence locator for every required face before rerunning the current record-pack regeneration.",
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
            "demo_forward_supervised_run_retry_gate_attestation_refresh_added": True,
            "demo_forward_retry_gate_attestation_refresh_current_pointers_fixed": True,
            "demo_forward_retry_gate_external_evidence_gap_written": True,
            "demo_forward_retry_gate_attestation_refresh_checklist_written": True,
            "demo_forward_retry_gate_attestation_refresh_decision_surface_written": True,
            "demo_forward_retry_gate_attestation_refresh_subagent_summary_written": True,
            "recommended_next_step_advances_to_attestation_record_pack_regeneration_when_blocked": True,
            "retry_gate_review_requires_current_fresh_enough_reviewable_locators": True,
        }
    )
    MANIFEST_PATH.write_text(format_json(manifest))

    ledger_payload = {
        "artifact_bundle": BUNDLE_PATH,
        "base_main": VERIFIED_VEXTER_COMMIT,
        "baseline_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION",
        "baseline_task_state": "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked",
        "branch": git_output("branch", "--show-current"),
        "claim_boundary": CLAIM_BOUNDARY,
        "current_lane": CURRENT_LANE,
        "decision": DECISION,
        "first_demo_target": "dexter_paper_live",
        "gate_pass_successor": PASS_NEXT_TASK_ID,
        "key_finding": KEY_FINDING,
        "next_task_id": NEXT_TASK_ID,
        "next_task_state": NEXT_TASK_STATE,
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json",
        "recommended_next_lane": NEXT_TASK_LANE,
        "repo": "https://github.com/Cabbala/Vexter",
        "retry_gate_attestation_refresh_face_count": len(rows),
        "retry_gate_attestation_refresh_current_locator_count": sum(
            row["current_fresh_evidence_locator_present"] for row in rows
        ),
        "retry_gate_attestation_refresh_usable_count": sum(row["usable_now"] for row in rows),
        "selected_outcome": "FAIL/BLOCKED",
        "source_faithful_modes": {"dexter": "paper_live", "mewx": "sim_live"},
        "status": TASK_STATUS,
        "sub_agents_used": [item["name"] for item in SUB_AGENT_SUMMARIES],
        "supporting_vexter_prs": SUPPORTING_VEXTER_PRS,
        "task_id": TASK_ID,
        "template_runtime_validation_errors": runtime_errors,
        "external_evidence_manifest_status": gap_payload["manifest"]["status"],
        "external_evidence_preflight_status": preflight_payload["reopen_readiness"]["status"],
        "external_evidence_preflight_report": PREFLIGHT_REPORT_REL_PATH,
        "external_evidence_gap_report": GAP_REPORT_REL_PATH,
        "verified_dexter_main_commit": VERIFIED_DEXTER_COMMIT,
        "verified_dexter_pr": 3,
        "verified_mewx_frozen_commit": VERIFIED_MEWX_COMMIT,
        "verified_prs": VERIFIED_VEXTER_PRS,
        "date": run_timestamp.split("T", 1)[0],
    }
    rewrite_local_ledger(ledger_payload)

    update_readme()


if __name__ == "__main__":
    main()
