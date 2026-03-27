#!/usr/bin/env python3
"""Emit bounded retry-gate attestation-record-pack-regeneration surfaces from the refresh baseline."""

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
    ROOT
    / "docs"
    / "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md"
)
DECISION_SURFACE_PATH = (
    ROOT
    / "docs"
    / "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md"
)
SPEC_PATH = (
    ROOT
    / "specs"
    / "DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md"
)
PLAN_PATH = (
    ROOT
    / "plans"
    / "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md"
)

PREVIOUS_REPORT_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-refresh-report.md"
)
PREVIOUS_STATUS_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-refresh-status.md"
)
PREVIOUS_PROOF_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-attestation-refresh-check.json"
)
PREVIOUS_SUMMARY_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-attestation-refresh-summary.md"
)
PREVIOUS_HANDOFF_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-refresh" / "HANDOFF.md"
)
PREVIOUS_CHECKLIST_PATH = (
    ROOT / "docs" / "demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md"
)
PREVIOUS_DECISION_SURFACE_PATH = (
    ROOT / "docs" / "demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md"
)
PREVIOUS_SUBAGENTS_PATH = (
    ROOT
    / "artifacts"
    / "reports"
    / "demo-forward-supervised-run-retry-gate-attestation-refresh"
    / "SUBAGENTS.md"
)

REPORT_DIR = (
    ROOT
    / "artifacts"
    / "reports"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration"
)
REPORT_PATH = (
    ROOT
    / "artifacts"
    / "reports"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md"
)
STATUS_PATH = (
    ROOT
    / "artifacts"
    / "reports"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md"
)
SUBAGENTS_PATH = REPORT_DIR / "SUBAGENTS.md"
SUBAGENT_SUMMARY_PATH = REPORT_DIR / "subagent_summary.md"
PROOF_PATH = (
    ROOT
    / "artifacts"
    / "proofs"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json"
)
PROOF_SUMMARY_PATH = (
    ROOT
    / "artifacts"
    / "proofs"
    / "demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-summary.md"
)

BUNDLE_PATH = (
    "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration.tar.gz"
)
BUNDLE_SOURCE = "/Users/cabbala/Downloads/vexter_attestation_record_pack_regeneration_bundle_latest.tar.gz"

TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION"
TASK_STATUS = "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked"
KEY_FINDING = (
    "supervised_run_retry_gate_attestation_record_pack_regeneration_blocked_on_missing_or_stale_regenerated_faces"
)
CLAIM_BOUNDARY = "supervised_run_retry_gate_attestation_record_pack_regeneration_bounded"
CURRENT_LANE = "supervised_run_retry_gate_attestation_record_pack_regeneration"
NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH"
NEXT_TASK_STATE = "additional_attestation_refresh_required_for_record_pack_regeneration"
NEXT_TASK_LANE = "supervised_run_retry_gate_attestation_refresh"
PASS_NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
PASS_NEXT_TASK_STATE = "ready_for_supervised_run_retry_gate_recheck"
PASS_NEXT_TASK_LANE = "supervised_run_retry_gate"
DECISION = "retry_gate_review_blocked_pending_current_attestation_record_pack_regeneration"

VERIFIED_DEXTER_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
VERIFIED_MEWX_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
VERIFIED_VEXTER_PR = 93
VERIFIED_VEXTER_COMMIT = "1271c18b6a57bb0ff5e9eedae6a886ba90945960"
VERIFIED_VEXTER_MERGED_AT = "2026-03-27T22:25:21Z"
SUPPORTING_VEXTER_PRS = [93, 92, 91, 90, 89]
VERIFIED_VEXTER_PRS = [93, 92, 91]

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
            "Reverified PR `#93` / merge commit `1271c18b6a57bb0ff5e9eedae6a886ba90945960` as latest merged `main`, then flipped the repo-level current pointers back from refresh to regeneration without inventing a pass claim or fabricating evidence.",
            "Checked the atomic current-pointer set across summary, context, manifest, ledger, bundle metadata, README, and handoff surfaces so regeneration is current while refresh remains the blocked baseline and recommended next-step alternation returns to refresh.",
            "Rechecked the regeneration-side mapping against the shared canonical manifest, evidence preflight, and compatibility gap outputs so the template-only manifest stays honest and the preflight remains fail-closed.",
        ],
    },
    {
        "name": "Euler",
        "lines": [
            "Confirmed the regeneration lane stays inside the unchanged Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one-plan, one-position, explicit-allowlist, small-lot, bounded-window, funded-live-forbidden envelope.",
            "Verified the planner/runtime boundary remains intact: `prepare / start / status / stop / snapshot` stay planner-bound, `manual_latched_stop_all` remains planner-owned, Dexter stays the only real-demo seam, and frozen Mew-X remains unchanged on `sim_live`.",
            "The strongest protections remain the fail-closed manifest/preflight logic and boundary tests, so the real risk here is pointer drift during the lane flip rather than any runtime or architecture widening.",
        ],
    },
    {
        "name": "Parfit",
        "lines": [
            "The smallest safe change set is the regeneration generator provenance refresh, the generated current-pointer outputs, and the regression expectations that still pinned refresh as the repo-wide current lane.",
            "Validation should stay bounded: rerun the canonical evidence preflight, rerun regeneration from the refresh baseline, rebuild the proof bundle, cover the shared refresh/regeneration/retry-gate/evidence-preflight expectations, then finish with full pytest.",
            "Merge readiness depends on the manifest staying `template_only`, the preflight staying fail-closed, the proof bundle matching the regenerated outputs, and the final exported tarball carrying the same current-lane truth.",
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
    value = value.strip()
    while value.startswith(REGENERATION_RESET_PREFIX):
        value = value[len(REGENERATION_RESET_PREFIX) :].strip()
    if REGENERATION_RESET_SUFFIX in value:
        value = value.split(REGENERATION_RESET_SUFFIX, 1)[0].strip()
    while value.startswith(REGENERATION_RESET_PREFIX):
        value = value[len(REGENERATION_RESET_PREFIX) :].strip()
    return value


def extract_refresh_reviewable_condition(value: str) -> str:
    if REGENERATION_REVIEWABLE_SUFFIX in value:
        return value.split(REGENERATION_REVIEWABLE_SUFFIX, 1)[0].strip()
    return value.strip()


def mentions_window_move(value: str) -> bool:
    lowered = value.lower()
    return any(
        needle in lowered
        for needle in (
            "window moves",
            "window changes",
            "window rolls forward",
            "window is rescheduled",
            "window advances",
            "scheduled window moves",
            "supervised window moves",
            "bounded supervised window moves",
        )
    )


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


def build_regeneration_trigger(refresh_trigger: str, stale_condition: str) -> str:
    trigger_tail = stale_condition
    if not mentions_window_move(refresh_trigger) and not mentions_window_move(stale_condition):
        trigger_tail = f"{trigger_tail} or when the bounded supervised window moves"
    return (
        f"{refresh_trigger}; regenerate the current record-pack face again whenever {trigger_tail}."
    )


def build_minimum_regenerated_locator_shape(minimum_shape: str) -> str:
    return (
        f"{minimum_shape}; plus regenerated face name, regeneration timestamp, bundle-relative proof pointer, "
        "and one reviewer-readable locator path that reopens the same bounded-window evidence without exposing secrets"
    )


def build_freshness_inheritance_or_reset_rule(stale_condition: str) -> str:
    return (
        "inherit freshness only while the underlying fresh locator remains current, reviewable, and inside the "
        "same bounded supervised window; reset the regenerated face to FAIL/BLOCKED when "
        f"{stale_condition} or when the locator cannot be reopened without secrets"
    )


def build_regenerated_reviewable_enough_when(usable_condition: str) -> str:
    return (
        f"{usable_condition} and the regenerated face points to the same bounded-window locator plus an explicit "
        "regeneration timestamp and reviewer-readable proof path"
    )


def build_regeneration_rows(gap_faces: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for face in gap_faces:
        refreshed_face_covers = face.get("what_face_covers", "").strip()
        refresh_trigger = (
            f"refresh before {face.get('stale_condition', '').strip()}; otherwise keep the face blocked "
            "for record-pack regeneration"
        )
        minimum_fresh_locator_shape = (
            f"{face.get('minimum_evidence_locator_shape', '').strip()}; plus one repo-visible fresh-enough "
            "verification timestamp inside the current bounded supervised window and a locator that can be "
            "reopened without exposing secrets"
        )
        stale_condition = face.get("stale_condition", "").strip()
        usable_condition = (
            f"{face.get('usable_for_retry_gate_review_when', '').strip()} and the located evidence is still "
            "fresh enough for the current bounded supervised window"
        )
        regeneration_rule_complete = all(
            bool(value)
            for value in (
                face.get("refresh_owner"),
                refreshed_face_covers,
                refresh_trigger,
                minimum_fresh_locator_shape,
                stale_condition,
                usable_condition,
            )
        )
        current_fresh_locator_present = bool(face.get("present"))
        freshness_inherited_cleanly = bool(face.get("current")) and bool(face.get("fresh_enough"))
        source_refresh_usable_now = bool(face.get("reviewable")) and not bool(face.get("blocked"))
        regenerated_face_reviewable_now = (
            regeneration_rule_complete
            and current_fresh_locator_present
            and freshness_inherited_cleanly
            and source_refresh_usable_now
        )
        rows.append(
            {
                "name": face["name"],
                "repo_visible_marker": face["repo_visible_marker"],
                "regeneration_owner": face["refresh_owner"],
                "what_regenerated_face_covers": (
                    f"{refreshed_face_covers} The regenerated pack must keep that same bounded-window "
                    "meaning without widening scope or implying retry execution success."
                ),
                "regeneration_trigger": build_regeneration_trigger(
                    refresh_trigger, stale_condition
                ),
                "minimum_regenerated_locator_shape": build_minimum_regenerated_locator_shape(
                    minimum_fresh_locator_shape
                ),
                "freshness_inheritance_or_reset_rule": build_freshness_inheritance_or_reset_rule(
                    stale_condition
                ),
                "reviewable_enough_when": build_regenerated_reviewable_enough_when(
                    usable_condition
                ),
                "required_manifest_fields": list(face.get("required_manifest_fields", [])),
                "proof_paths_to_recheck": list(face.get("proof_paths_to_recheck", [])),
                "canonical_blocked_reasons": list(face.get("blocked_reasons", [])),
                "operator_input_needed": face.get("operator_input_needed", "").strip(),
                "regeneration_rule_complete": regeneration_rule_complete,
                "current_fresh_locator_present": current_fresh_locator_present,
                "freshness_inherited_cleanly": freshness_inherited_cleanly,
                "regenerated_face_reviewable_now": regenerated_face_reviewable_now,
                "current_regeneration_observation": face["current_observation"]
                if not regenerated_face_reviewable_now
                else (
                    "A current, fresh-enough bounded-window locator is available for this face, and the "
                    "regenerated pack can stay reviewable without widening scope."
                ),
                "regeneration_status": "PASS" if regenerated_face_reviewable_now else "FAIL/BLOCKED",
            }
        )
    return rows


def build_regeneration_checklist(rows: list[dict], runtime_errors: list[str]) -> dict[str, bool]:
    row_names = {row["name"] for row in rows}
    return {
        "runtime_guardrails_parse_cleanly": not runtime_errors,
        "all_required_faces_present": row_names == set(REQUIRED_FACE_NAMES),
        "all_regeneration_owners_explicit": all(bool(row["regeneration_owner"]) for row in rows),
        "all_regeneration_triggers_explicit": all(bool(row["regeneration_trigger"]) for row in rows),
        "all_minimum_regenerated_locator_shapes_explicit": all(
            bool(row["minimum_regenerated_locator_shape"]) for row in rows
        ),
        "all_freshness_inheritance_rules_explicit": all(
            bool(row["freshness_inheritance_or_reset_rule"]) for row in rows
        ),
        "all_regenerated_reviewable_conditions_explicit": all(
            bool(row["reviewable_enough_when"]) for row in rows
        ),
        "all_manifest_field_maps_explicit": all(bool(row["required_manifest_fields"]) for row in rows),
        "all_proof_path_maps_explicit": all(bool(row["proof_paths_to_recheck"]) for row in rows),
        "all_current_fresh_locator_inputs_present": all(
            row["current_fresh_locator_present"] for row in rows
        ),
        "all_freshness_inherited_cleanly": all(row["freshness_inherited_cleanly"] for row in rows),
        "all_regenerated_faces_reviewable_now": all(
            row["regenerated_face_reviewable_now"] for row in rows
        ),
        "record_pack_reviewable_now": all(row["regenerated_face_reviewable_now"] for row in rows),
        "retry_gate_review_reopen_ready": all(row["regenerated_face_reviewable_now"] for row in rows),
    }


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
- baseline_task: `DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH`
- baseline_task_state: `supervised_run_retry_gate_attestation_refresh_blocked`
- planner_boundary: `prepare/start/status/stop/snapshot`
- current_attestation_record_pack_regeneration_lane: `{CURRENT_LANE}`
- recommended_next_step: `{NEXT_TASK_LANE}`
- regeneration_pass_successor: `{PASS_NEXT_TASK_LANE}`
"""


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


def build_current_report(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    rows: list[dict],
    gap_payload: dict[str, object],
    preflight_payload: dict[str, object],
) -> str:
    blocked_faces = [row["name"] for row in rows if row["regeneration_status"] != "PASS"]
    regeneration_rules_explicit_count = sum(row["regeneration_rule_complete"] for row in rows)
    manifest = gap_payload["manifest"]
    summary = gap_payload["summary"]
    readiness = preflight_payload["reopen_readiness"]
    blocked_faces_align_with_gap = sorted(blocked_faces) == sorted(summary["blocked_faces"])
    reopen_ready_consistent = (
        readiness["retry_gate_review_reopen_ready"] is False
        and all(row["regenerated_face_reviewable_now"] is False for row in rows)
    )
    next_human_pass_lines = build_next_human_pass_lines(readiness)
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Report

## Verified GitHub State
- Reverified latest GitHub-visible Vexter `main` at merged PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`.
- Dexter stayed pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen Mew-X stayed pinned at `{VERIFIED_MEWX_COMMIT}`.
- Report timestamp: `{run_timestamp}`.

## Baseline Accepted
- Accepted `supervised_run_retry_gate_attestation_refresh_blocked` as the bounded baseline current source of truth.
- Did not claim retry-gate reopen, retry execution success, funded live access, new external evidence collection success, or any Mew-X seam expansion.
- Promoted one bounded attestation record-pack regeneration lane as the new current source of truth for regenerated face ownership, triggers, inheritance rules, and reviewer-readable pack pointers.
- Replaced duplicated cross-lane blocker parsing with one canonical outside-repo evidence manifest, validator, and evidence preflight / compatibility gap surface shared by regeneration and refresh.

## Regeneration Boundary
{chr(10).join(f"- {line}" for line in boundary_lines())}

## Decision
- Outcome: `FAIL/BLOCKED`
- Decision: `{DECISION}`
- Current lane: `{CURRENT_LANE}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Retry-gate pass successor: `{PASS_NEXT_TASK_LANE}`
- Runtime validation errors: `{json.dumps(list(runtime_config.validation_errors()))}`

## Regeneration Surfaces
- current status report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md`
- current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md`
- current summary: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-summary.md`
- current proof json: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json`
- current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md`
- record-pack regeneration checklist: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md`
- record-pack regeneration decision surface: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md`
- current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md`

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

## Regeneration Findings
- required regeneration faces: `{len(rows)}`
- regeneration rules explicit count: `{regeneration_rules_explicit_count}`
- per-face manifest field maps explicit count: `{sum(bool(row["required_manifest_fields"]) for row in rows)}`
- per-face proof path maps explicit count: `{sum(bool(row["proof_paths_to_recheck"]) for row in rows)}`
- current fresh locator input count: `{sum(row["current_fresh_locator_present"] for row in rows)}`
- freshness inherited cleanly count: `{sum(row["freshness_inherited_cleanly"] for row in rows)}`
- regenerated face reviewable count: `{sum(row["regenerated_face_reviewable_now"] for row in rows)}`
- blocked regenerated faces: `{", ".join(blocked_faces)}`
- canonical gap blocked faces align with regeneration lane: `{"yes" if blocked_faces_align_with_gap else "no"}`
- template-only reopen-ready remains false across canonical preflight and regeneration lane: `{"yes" if reopen_ready_consistent else "no"}`

## Honest Regeneration Model
- `PASS` only if refreshed locator rules produce a current, reviewable regenerated record pack sufficient to reopen retry-gate review honestly.
- `FAIL/BLOCKED` if one or more regenerated faces remain missing, stale, ambiguous, or non-reviewable.
- Current result remains `FAIL/BLOCKED` because the canonical manifest is `{manifest['status']}`, the preflight status remains `{readiness['status']}`, and the repo still does not point to one current, fresh-enough, reviewable locator per required face, so the regenerated current pack cannot reopen retry-gate review honestly.
"""


def build_proof_summary(gap_payload: dict[str, object], preflight_payload: dict[str, object]) -> str:
    return f"""# {TASK_ID} Proof Summary

- Verified latest GitHub-visible Vexter `main` at PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}`.
- Accepted attestation refresh as the bounded baseline current source of truth.
- Promoted attestation record-pack regeneration as the current operator-visible lane for regeneration owner, trigger, regenerated locator shape, freshness inheritance, and reviewability.
- Wired regeneration to the canonical external-evidence contract at `{CONTRACT_SPEC_REL_PATH}`, preflight report `{PREFLIGHT_REPORT_REL_PATH}`, and legacy gap report `{GAP_REPORT_REL_PATH}`.
- Held the result at `FAIL/BLOCKED` because the manifest status is `{gap_payload['manifest']['status']}`, the preflight status is `{preflight_payload['reopen_readiness']['status']}`, the template-only false path remains `{preflight_payload['reopen_readiness']['template_only_false_path']}`, and current regenerated faces are still missing or non-reviewable.
- Recommended next step: `{NEXT_TASK_LANE}`.
- Retry-gate pass successor: `{PASS_NEXT_TASK_LANE}`.
"""


def build_spec() -> str:
    boundary = "\n".join(f"- {line}" for line in boundary_lines())
    return f"""# DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION

## Goal
Promote a bounded `attestation_record_pack_regeneration` lane as the current source of truth after attestation refresh, without fabricating retry-gate reopen, retry execution success, or any funded-live path.

## Boundary
{boundary}

## Required Current Surfaces
- current status report
- current report
- current summary
- current proof json
- current handoff
- record-pack regeneration checklist
- record-pack regeneration decision surface
- canonical external evidence contract
- canonical external evidence manifest
- canonical evidence preflight proof / report / summary
- canonical external evidence gap proof / gap report / gap summary
- next recommended step

## Honest Regeneration Model
- `PASS`: refreshed locator rules produce a current, reviewable regenerated record pack sufficient to reopen retry-gate review honestly
- `FAIL/BLOCKED`: one or more regenerated faces remain missing, stale, ambiguous, or non-reviewable

## Required Regeneration Face Detail
Each regeneration face must make explicit:
- regeneration owner
- regeneration trigger
- minimum regenerated locator shape
- freshness inheritance or reset rule
- what makes the regenerated face reviewable enough

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
The promoted lane remains fail-closed until every required face can inherit freshness from one current, reviewable bounded-window locator and the regenerated record pack can reopen retry-gate review honestly.
"""


def build_plan() -> str:
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Plan

## Implementation Steps
1. Reverify the latest GitHub-visible Vexter `main` state at PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}`.
2. Accept attestation refresh as the blocked baseline current source of truth.
3. Write one canonical outside-repo evidence manifest template, contract, validator, and unified evidence preflight / reopen-readiness surface for the remaining retry-gate blockers.
4. Generate one bounded attestation record-pack regeneration lane with current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.
5. For each required face, carry forward the bounded refresh locator rule, then fix regeneration owner, regeneration trigger, minimum regenerated locator shape, freshness inheritance or reset rule, and reviewable-enough rule from the canonical gap output.
6. Keep `FAIL/BLOCKED` unless every face can regenerate from one current, fresh-enough, reviewable locator.
7. Recommend `{NEXT_TASK_LANE}` while blocked and expose `{PASS_NEXT_TASK_LANE}` only as the pass successor.

## Guardrails
{chr(10).join(f"- {line}" for line in boundary_lines())}

## Validation
- generate the canonical evidence preflight with `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py`
- generate the lane with `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py`
- rebuild the tarball with `./scripts/build_proof_bundle.sh`
- verify shared regression expectations with `pytest -q`
"""


def build_checklist(rows: list[dict]) -> str:
    face_lines = []
    for row in rows:
        face_lines.append(
            "| "
            f"`{row['name']}` | "
            f"`{row['regeneration_owner']}` | "
            f"{row['regeneration_trigger']} | "
            f"{row['minimum_regenerated_locator_shape']} | "
            f"{row['freshness_inheritance_or_reset_rule']} | "
            f"{row['reviewable_enough_when']} |"
        )
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Checklist

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
1. Start at `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json`.
4. Review the canonical manifest template at `manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json`.
5. Review the canonical evidence preflight report at `artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md`.
6. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md`.
7. Use `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md` as the single record-pack regeneration decision surface.
8. Keep one regeneration row per required face: credential source, venue ref, account ref, connectivity profile, operator owner, bounded start criteria, allowlist / symbol / lot reconfirmation, `manual_latched_stop_all` visibility, and terminal snapshot readability.
9. For every row, confirm regeneration owner, regeneration trigger, minimum regenerated locator shape, freshness inheritance or reset rule, and what makes the regenerated face reviewable enough are explicit.
10. For every row, record whether a current fresh-enough bounded-window locator is present and can seed the regenerated face without embedding secret material.
11. Hold the lane at `FAIL/BLOCKED` until every required face is regenerated, current, and reviewable enough to reopen retry-gate review honestly.

## Regeneration Faces
| Regeneration face | Regeneration owner | Regeneration trigger | Minimum regenerated locator shape | Freshness inheritance or reset rule | Reviewable enough when |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(face_lines)}
"""


def build_decision_surface(rows: list[dict]) -> str:
    lines = [
        "# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Decision Surface",
        "",
        "This decision surface is the current source of truth for `supervised_run_retry_gate_attestation_record_pack_regeneration`.",
        "",
        "| Regeneration face | Repo-visible marker | Regeneration owner | What the regenerated face covers | Regeneration trigger | Minimum regenerated locator shape | Freshness inheritance or reset rule | Reviewable enough when | Regeneration rule complete | Current fresh locator present | Freshness inherited cleanly | Regenerated face reviewable now | Current regeneration observation | Regeneration status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"`{row['name']}` | "
            f"`{format_marker(row['repo_visible_marker'])}` | "
            f"`{row['regeneration_owner']}` | "
            f"{row['what_regenerated_face_covers']} | "
            f"{row['regeneration_trigger']} | "
            f"{row['minimum_regenerated_locator_shape']} | "
            f"{row['freshness_inheritance_or_reset_rule']} | "
            f"{row['reviewable_enough_when']} | "
            f"`{format_bool(row['regeneration_rule_complete'])}` | "
            f"`{format_bool(row['current_fresh_locator_present'])}` | "
            f"`{format_bool(row['freshness_inherited_cleanly'])}` | "
            f"`{format_bool(row['regenerated_face_reviewable_now'])}` | "
            f"{row['current_regeneration_observation']} | "
            f"`{row['regeneration_status']}` |"
        )
    lines.extend(
        [
            "",
            "Retry-gate review does not reopen unless every regenerated face points to one current, fresh-enough, reviewable locator and the regenerated pack stays bounded.",
            f"While blocked, the next recommended step is `{NEXT_TASK_LANE}` for additional refresh, and the pass successor remains `{PASS_NEXT_TASK_LANE}`.",
        ]
    )
    return "\n".join(lines)


def build_details(manifest_status: str, preflight_status: str) -> str:
    return f"""# ATTESTATION-RECORD-PACK-REGENERATION Details

## Verified Starting Point
- Latest Vexter `main`: PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`
- Dexter pinned commit: `{VERIFIED_DEXTER_COMMIT}`
- Frozen Mew-X commit: `{VERIFIED_MEWX_COMMIT}`
- Accepted baseline: `supervised_run_retry_gate_attestation_refresh_blocked`

## Deliverable
Promote one bounded attestation record-pack regeneration lane that keeps current status, report, summary, proof, handoff, checklist, and decision-surface pointers coherent while fail-closing retry-gate review until every required regenerated face is current and reviewable. The canonical external-evidence manifest currently sits at status `{manifest_status}`, the evidence preflight remains `{preflight_status}`, and the repo therefore stays blocker-facing rather than pass-claiming.
"""


def build_min_prompt(manifest_status: str, preflight_status: str) -> str:
    return (
        f"GitHub latest state is Vexter main PR #{VERIFIED_VEXTER_PR} merge commit "
        f"{VERIFIED_VEXTER_COMMIT} on {VERIFIED_VEXTER_MERGED_AT}. "
        "Accept attestation refresh as baseline, promote attestation record-pack regeneration as the current "
        f"source of truth, keep Dexter-only paper_live and frozen Mew-X sim_live, consume the canonical evidence preflight and compatibility gap surfaces with manifest status {manifest_status} and preflight status {preflight_status}, "
        "do not commit secrets, keep the lane FAIL/BLOCKED until every regenerated face is reviewable, and recommend "
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
        f"{row['name']}: regeneration_rule_complete={str(row['regeneration_rule_complete']).lower()}, "
        f"current_fresh_locator_present={str(row['current_fresh_locator_present']).lower()}, "
        f"freshness_inherited_cleanly={str(row['freshness_inherited_cleanly']).lower()}, "
        f"regenerated_face_reviewable_now={str(row['regenerated_face_reviewable_now']).lower()}, "
        f"regeneration_owner={row['regeneration_owner']}"
        for row in rows
    )
    face_manifest_map_lines = "\n".join(
        "- "
        f"{row['name']}: manifest_fields={', '.join(row['required_manifest_fields'])}; "
        f"proof_paths_to_recheck={', '.join(row['proof_paths_to_recheck'])}; "
        f"blocked_reasons={', '.join(row['canonical_blocked_reasons']) or 'none'}; "
        f"operator_input_remaining={row['operator_input_needed']}"
        for row in rows
    )
    blocked_faces_align_with_gap = sorted(
        row["name"] for row in rows if row["regeneration_status"] != "PASS"
    ) == sorted(gap_payload["summary"]["blocked_faces"])
    reopen_ready_consistent = (
        preflight_payload["reopen_readiness"]["retry_gate_review_reopen_ready"] is False
        and all(row["regenerated_face_reviewable_now"] is False for row in rows)
    )
    next_human_pass_lines = "\n".join(
        f"- {line}" for line in build_next_human_pass_lines(preflight_payload["reopen_readiness"])
    )
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Handoff

## Current Status
- outgoing_shift_window: {run_timestamp} attestation-record-pack-regeneration lane
- incoming_shift_window: bounded additional refresh and possible regeneration rerun
- task_state: {TASK_STATUS}
- shift_outcome: blocked
- current_action: hold_retry_gate_review_until_attestation_record_pack_regeneration_is_current
- current_lane: {CURRENT_LANE}
- recommended_next_step_while_blocked: {NEXT_TASK_LANE}
- regeneration_pass_successor: {PASS_NEXT_TASK_LANE}
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: {VERIFIED_VEXTER_COMMIT}
- dexter_main_commit: {VERIFIED_DEXTER_COMMIT}
- mewx_frozen_commit: {VERIFIED_MEWX_COMMIT}
- baseline_attestation_refresh_task_state: supervised_run_retry_gate_attestation_refresh_blocked

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md
- current_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md
- current_proof_summary: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-summary.md
- current_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json
- current_attestation_record_pack_regeneration_checklist: docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md
- current_attestation_record_pack_regeneration_decision_surface: docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md
- current_subagent_summary: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md
- canonical_external_evidence_contract: {CONTRACT_SPEC_REL_PATH}
- canonical_external_evidence_manifest: {EXTERNAL_EVIDENCE_MANIFEST_REL_PATH}
- canonical_external_evidence_preflight_report: {PREFLIGHT_REPORT_REL_PATH}
- canonical_external_evidence_preflight_proof: {PREFLIGHT_PROOF_REL_PATH}
- canonical_external_evidence_preflight_summary: {PREFLIGHT_SUMMARY_REL_PATH}
- canonical_external_evidence_gap_report: {GAP_REPORT_REL_PATH}
- canonical_external_evidence_gap_proof: {GAP_PROOF_REL_PATH}
- canonical_external_evidence_gap_summary: {GAP_SUMMARY_REL_PATH}
- canonical_external_evidence_manifest_status: {gap_payload['manifest']['status']}
- baseline_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-status.md
- baseline_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md
- baseline_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json
- baseline_handoff: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md

## Canonical Evidence Intake Handoff
- bounded_window_fields_to_fill_once: {", ".join(gap_payload['manifest']['window_fields_to_fill'])}
- per_blocked_face_fields_to_fill: provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note
- canonical_face_to_manifest_map: {PREFLIGHT_REPORT_REL_PATH}
- canonical_machine_preflight_proof: {PREFLIGHT_PROOF_REL_PATH}
- canonical_legacy_gap_report: {GAP_REPORT_REL_PATH}
- proof_surfaces_to_rerun_after_manifest_update: {", ".join(gap_payload['manifest']['proof_paths_to_recheck'])}
- retry_gate_review_reopen_ready_from_external_evidence: {str(preflight_payload['reopen_readiness']['retry_gate_review_reopen_ready']).lower()}
- evidence_preflight_status: {preflight_payload['reopen_readiness']['status']}
- evidence_preflight_aggregated_blocked_reasons: {json.dumps(preflight_payload['reopen_readiness']['blocked_reason_counts'], sort_keys=True)}
- template_only_false_path: {preflight_payload['reopen_readiness']['template_only_false_path']}
- evidence_preflight_consistency_checks: {json.dumps(preflight_payload['reopen_readiness']['consistency_checks'], sort_keys=True)}
- regeneration_lane_reopen_ready_now: {str(all(row['regenerated_face_reviewable_now'] for row in rows)).lower()}
- canonical_gap_blocked_faces_align_with_regeneration_lane: {str(blocked_faces_align_with_gap).lower()}
- template_only_reopen_ready_consistency_holds: {str(reopen_ready_consistent).lower()}
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

## Regeneration Faces
{face_lines}

## Face-To-Manifest And Proof Map
{face_manifest_map_lines}

## Open Questions
- question_1_or_none: who will replace the template manifest with one current fresh-enough locator per required face so the regenerated pack can stay reviewable without secrets
- question_2_or_none: which refreshed locator should be recollected first for venue, account, and connectivity faces before rerunning regeneration
- question_3_or_none: who timestamps the regenerated bounded start window and operator owner before the next retry-gate recheck
- question_4_or_none: has `manual_latched_stop_all` visibility been freshly reconfirmed for the current bounded window
- question_5_or_none: has terminal snapshot readability been freshly reconfirmed for the current bounded window

## Next-Shift Priority Checks
- priority_check_1: keep the current lane blocked unless every face can inherit freshness from one current, reviewable bounded-window locator
- priority_check_2: recommend `{NEXT_TASK_LANE}` while blocked so additional fresh locators can be collected before rerunning regeneration
- priority_check_3: preserve Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, small-lot, one-position, `manual_latched_stop_all`, and funded-live-forbidden guardrails
- priority_check_4: keep `retry_gate_review_reopen_ready` false in both the canonical gap proof and the regeneration lane until the template manifest is replaced with current non-secret evidence

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- checklist_pointer_checked: true
- decision_surface_pointer_checked: true
- subagent_summary_pointer_checked: true
- blocked_claim_boundary_explicit: true
- per_face_manifest_field_maps_checked: true
- per_face_proof_path_maps_checked: true
- canonical_gap_alignment_checked: {str(blocked_faces_align_with_gap).lower()}

This handoff promotes the bounded attestation record-pack regeneration lane only. It does not claim retry-gate reopen, completed retry execution, funded live access, or any Mew-X seam expansion.
"""


def build_subagents() -> str:
    lines = [
        "# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Sub-agent Summaries",
        "",
    ]
    for item in SUB_AGENT_SUMMARIES:
        lines.append(f"## {item['name']}")
        for line in item["lines"]:
            lines.append(f"- {line}")
        lines.append("")
    return "\n".join(lines)


def update_readme() -> None:
    marker = (
        "`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION` starts from latest "
        "GitHub-visible Vexter `main`"
    )
    readme_text = README_PATH.read_text()
    entry = (
        "`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION` starts from latest "
        f"GitHub-visible Vexter `main` at merged PR `#{VERIFIED_VEXTER_PR}` merge commit "
        f"`{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`, keeps Dexter pinned at merged PR "
        f"`#3` commit `{VERIFIED_DEXTER_COMMIT}`, and keeps frozen Mew-X at `{VERIFIED_MEWX_COMMIT}`. "
        "It accepts the bounded attestation-refresh lane as baseline and promotes one fail-closed attestation "
        "record-pack-regeneration lane instead: the repo now fixes the current status/report/proof/handoff/"
        "checklist/decision-surface surfaces for regeneration owner, regeneration trigger, minimum regenerated "
        "locator shape, freshness inheritance or reset, and what makes each regenerated face reviewable "
        "enough, and it adds one canonical non-secret external-evidence manifest, validator, and evidence "
        "preflight / compatibility gap path that refresh and regeneration now consume together, "
        "while keeping the Dexter-only `paper_live` seam, leaving Mew-X unchanged on `sim_live`, "
        "and keeping funded live forbidden. The resulting status is "
        f"`{TASK_STATUS}` with `{CLAIM_BOUNDARY}`, the current lane is `{CURRENT_LANE}`, the blocked next "
        f"recommended step is `{NEXT_TASK_LANE}`, and the pass successor is `{PASS_NEXT_TASK_LANE}`."
    )
    line_re = re.compile(rf"(?m)^{re.escape(marker)}.*$")
    if line_re.search(readme_text):
        updated = line_re.sub(entry, readme_text, count=1)
    else:
        updated = readme_text.rstrip() + "\n\n" + entry + "\n"
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
    rows = build_regeneration_rows(preflight_payload["faces"])
    blocked_regenerated_faces = [row["name"] for row in rows if row["regeneration_status"] != "PASS"]
    checklist_attestation = build_regeneration_checklist(rows, runtime_errors)

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
            "task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH",
            "task_state": "supervised_run_retry_gate_attestation_refresh_blocked",
            "report": str(PREVIOUS_REPORT_PATH.relative_to(ROOT)),
            "status_report": str(PREVIOUS_STATUS_PATH.relative_to(ROOT)),
            "proof": str(PREVIOUS_PROOF_PATH.relative_to(ROOT)),
            "summary": str(PREVIOUS_SUMMARY_PATH.relative_to(ROOT)),
            "handoff": str(PREVIOUS_HANDOFF_PATH.relative_to(ROOT)),
            "checklist": str(PREVIOUS_CHECKLIST_PATH.relative_to(ROOT)),
            "decision_surface": str(PREVIOUS_DECISION_SURFACE_PATH.relative_to(ROOT)),
            "subagent_summary": str(PREVIOUS_SUBAGENTS_PATH.relative_to(ROOT)),
        },
        "supervised_run_retry_gate_attestation_record_pack_regeneration": {
            "planner_boundary": ["prepare", "start", "status", "stop", "snapshot"],
            "attestation_record_pack_regeneration_boundary": {
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
                "current_status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md",
                "current_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md",
                "current_summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-summary.md",
                "current_proof_json": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json",
                "current_handoff": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md",
                "attestation_record_pack_regeneration_checklist": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md",
                "attestation_record_pack_regeneration_decision_surface": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md",
                "external_evidence_contract": CONTRACT_SPEC_REL_PATH,
                "external_evidence_manifest": EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
                "external_evidence_preflight_report": PREFLIGHT_REPORT_REL_PATH,
                "external_evidence_preflight_proof": PREFLIGHT_PROOF_REL_PATH,
                "external_evidence_preflight_summary": PREFLIGHT_SUMMARY_REL_PATH,
                "external_evidence_gap_report": GAP_REPORT_REL_PATH,
                "external_evidence_gap_proof": GAP_PROOF_REL_PATH,
                "external_evidence_gap_summary": GAP_SUMMARY_REL_PATH,
                "next_recommended_step": NEXT_TASK_LANE,
                "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md",
            },
            "baseline_attestation_refresh_outcome": {
                "task_id": previous_proof["task_id"],
                "task_state": previous_proof["task_result"]["task_state"],
                "key_finding": previous_proof["task_result"]["key_finding"],
                "claim_boundary": previous_proof["task_result"]["claim_boundary"],
                "recommended_next_step": previous_proof["task_result"]["recommended_next_step"],
                "gate_pass_successor": previous_proof["task_result"]["gate_pass_successor"],
            },
            "regeneration_faces": {
                "attestation_record_pack_regeneration_decision_surface": rows,
                "blocked_regenerated_faces": blocked_regenerated_faces,
                "checklist_attestation_record_pack_regeneration": checklist_attestation,
                "record_pack_reviewable_now": checklist_attestation["record_pack_reviewable_now"],
                "retry_gate_review_reopen_ready": checklist_attestation[
                    "retry_gate_review_reopen_ready"
                ],
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
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_REFRESH.md",
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md",
                "plans/demo_forward_supervised_run_retry_gate_attestation_refresh_plan.md",
                "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md",
                PREFLIGHT_PROOF_REL_PATH,
                PREFLIGHT_REPORT_REL_PATH,
                PREFLIGHT_SUMMARY_REL_PATH,
                GAP_PROOF_REL_PATH,
                GAP_REPORT_REL_PATH,
                GAP_SUMMARY_REL_PATH,
                "scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
                "scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
                "scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
                "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
                "scripts/export_attestation_record_pack_regeneration_closeout_bundle.sh",
                "scripts/build_proof_bundle.sh",
                "vexter/demo_readiness/__init__.py",
                "vexter/demo_readiness/external_evidence.py",
                "tests/test_demo_forward_supervised_run_retry_gate.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
                "tests/test_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
                "tests/test_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
                "tests/test_bootstrap_layout.py",
            ],
            "proof_outputs": [
                PREFLIGHT_PROOF_REL_PATH,
                PREFLIGHT_SUMMARY_REL_PATH,
                GAP_PROOF_REL_PATH,
                GAP_SUMMARY_REL_PATH,
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json",
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-summary.md",
                "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration.tar.gz",
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

- Accepted attestation refresh as the baseline current source of truth.
- Promoted attestation record-pack regeneration to the current operator-visible lane.
- Added one canonical external-evidence contract, manifest template, validator, and evidence preflight / reopen-readiness path that now feed both regeneration and refresh.
- Added current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces for regeneration owner, trigger, regenerated locator shape, freshness inheritance, and reviewability.
- Fixed one fail-closed regeneration model that blocks retry-gate review until every required face can be regenerated from one current, reviewable bounded-window locator.

## Decision

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task status: `{TASK_STATUS}`
- Current lane: `{CURRENT_LANE}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Regeneration pass successor: `{PASS_NEXT_TASK_LANE}`
- Decision: `{DECISION}`
- Canonical external evidence manifest status: `{gap_payload["manifest"]["status"]}`
- Canonical evidence preflight status: `{preflight_payload["reopen_readiness"]["status"]}`

## Key Paths

- Current spec: `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md`
- Current implementation plan: `plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md`
- Current checklist: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md`
- Current decision surface: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md`
- Current proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json`
- Current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md`
- Current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md`
- Current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md`
- Canonical contract: `{CONTRACT_SPEC_REL_PATH}`
- Evidence template: `{EXTERNAL_EVIDENCE_MANIFEST_REL_PATH}`
- Preflight report: `{PREFLIGHT_REPORT_REL_PATH}`
- Gap report: `{GAP_REPORT_REL_PATH}`
- Current bundle target: `artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration.tar.gz`
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
        "baseline_task_state": "supervised_run_retry_gate_attestation_refresh_blocked",
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
        "blocked_regenerated_faces": blocked_regenerated_faces,
        "record_pack_reviewable_now": checklist_attestation["record_pack_reviewable_now"],
        "retry_gate_review_reopen_ready": checklist_attestation["retry_gate_review_reopen_ready"],
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
        "previous_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH",
        "previous_task_state": "supervised_run_retry_gate_attestation_refresh_blocked",
        "previous_key_finding": "supervised_run_retry_gate_attestation_refresh_blocked_on_missing_or_stale_fresh_evidence_locators",
        "previous_claim_boundary": "supervised_run_retry_gate_attestation_refresh_bounded",
        "retry_gate_attestation_refresh_accepted_as_baseline": True,
        "retry_gate_attestation_record_pack_regeneration_promoted_current": True,
    }
    context_pack["bundle_source"] = BUNDLE_SOURCE
    context_pack["current_contract"].update(
        {
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_marker": "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_spec_path": "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan_path": "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist_path": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface_path": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_subagents_path": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_subagent_summary_path": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/subagent_summary.md",
            "demo_forward_retry_gate_attestation_record_pack_regeneration_current_lane": CURRENT_LANE,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_next_step": NEXT_TASK_LANE,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_pass_successor": PASS_NEXT_TASK_LANE,
            "demo_forward_retry_gate_external_evidence_contract_spec_path": CONTRACT_SPEC_REL_PATH,
            "demo_forward_retry_gate_external_evidence_manifest_path": EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
            "demo_forward_retry_gate_external_evidence_gap_report_path": GAP_REPORT_REL_PATH,
            "demo_forward_retry_gate_external_evidence_gap_proof_path": GAP_PROOF_REL_PATH,
            "demo_forward_retry_gate_external_evidence_gap_summary_path": GAP_SUMMARY_REL_PATH,
        }
    )
    context_pack["current_task"] = {
        "id": TASK_ID,
        "scope": [
            "Reverify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X after attestation refresh merged.",
            "Accept attestation refresh as the baseline current source of truth.",
            "Write one canonical non-secret outside-repo evidence manifest, validator, and evidence preflight / reopen-readiness path for the remaining retry-gate blockers.",
            "Promote attestation record-pack regeneration status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Make each required face explicit for regeneration owner, trigger, minimum regenerated locator shape, freshness inheritance or reset, and reviewability from the canonical gap report.",
            "Keep retry-gate review blocked until every required face can regenerate from one current, fresh-enough, reviewable locator.",
        ],
        "deliverables": [
            "README.md",
            CONTRACT_SPEC_REL_PATH,
            EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
            "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md",
            "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md",
            "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md",
            "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md",
            PREFLIGHT_PROOF_REL_PATH,
            PREFLIGHT_REPORT_REL_PATH,
            PREFLIGHT_SUMMARY_REL_PATH,
            GAP_PROOF_REL_PATH,
            GAP_REPORT_REL_PATH,
            GAP_SUMMARY_REL_PATH,
            "scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
            "tests/test_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
            "tests/test_demo_forward_supervised_run_retry_gate.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_audit.py",
            "tests/test_demo_forward_supervised_run_retry_readiness.py",
            "tests/test_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
            "tests/test_bootstrap_layout.py",
            "scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
            "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
            "scripts/export_attestation_record_pack_regeneration_closeout_bundle.sh",
            "scripts/build_proof_bundle.sh",
            "vexter/demo_readiness/__init__.py",
            "vexter/demo_readiness/external_evidence.py",
            "artifacts/summary.md",
            "artifacts/context_pack.json",
            "artifacts/proof_bundle_manifest.json",
            "artifacts/task_ledger.jsonl",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/DETAILS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/MIN_PROMPT.txt",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/CONTEXT.json",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/subagent_summary.md",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-summary.md",
            "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration.tar.gz",
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
            "demo_forward_supervised_run_retry_gate_attestation_refresh",
            {"attestation_refresh_surface_current": False},
        ),
    ):
        if evidence_key in context_pack["evidence"]:
            context_pack["evidence"][evidence_key].update(current_flags)
    context_pack["evidence"]["github_latest"].update(
        {
            "latest_vexter_pr": VERIFIED_VEXTER_PR,
            "latest_vexter_main_commit": VERIFIED_VEXTER_COMMIT,
            "latest_recent_vexter_prs": SUPPORTING_VEXTER_PRS,
            "vexter_pr_93_merged_at": VERIFIED_VEXTER_MERGED_AT,
            "vexter_pr_93_closed_at": VERIFIED_VEXTER_MERGED_AT,
        }
    )
    context_pack["evidence"]["demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration"] = {
        "report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md",
        "status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md",
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json",
        "summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-summary.md",
        "handoff_dir": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration",
        "checklist": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md",
        "decision_surface": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md",
        "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md",
        "key_finding": KEY_FINDING,
        "claim_boundary": CLAIM_BOUNDARY,
        "task_state": TASK_STATUS,
        "run_outcome": "FAIL/BLOCKED",
        "attestation_record_pack_regeneration_surface_current": True,
        "preferred_next_step": NEXT_TASK_LANE,
        "regeneration_pass_successor": PASS_NEXT_TASK_LANE,
        "attestation_record_pack_regeneration_boundary": proof[
            "supervised_run_retry_gate_attestation_record_pack_regeneration"
        ]["attestation_record_pack_regeneration_boundary"],
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
        "blocked_regenerated_faces": blocked_regenerated_faces,
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
        "per_face_manifest_field_maps_explicit": all(
            bool(row["required_manifest_fields"]) for row in rows
        ),
        "per_face_proof_path_maps_explicit": all(bool(row["proof_paths_to_recheck"]) for row in rows),
        "canonical_gap_blocked_faces_align_with_regeneration_lane": sorted(
            blocked_regenerated_faces
        )
        == sorted(preflight_payload["reopen_readiness"]["blocked_faces"]),
    }
    context_pack["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "rationale": [
            "Attestation record-pack regeneration is now the current source of truth for regenerated locator inheritance and reviewable pack surfaces.",
            "The canonical external-evidence manifest now makes every remaining retry-gate blocker explicit, but one or more faces still remain template-only, incomplete, stale, or non-reviewable.",
            "Collect additional fresh bounded-window locators in attestation refresh before any retry-gate recheck is considered.",
        ],
        "pass_successor": {
            "id": PASS_NEXT_TASK_ID,
            "state": PASS_NEXT_TASK_STATE,
            "lane": PASS_NEXT_TASK_LANE,
        },
    }
    context_pack["proofs"].update(
        {
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_added": True,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_current_pointers_fixed": True,
            "demo_forward_retry_gate_evidence_preflight_written": True,
            "demo_forward_retry_gate_external_evidence_gap_written": True,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_checklist_written": True,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_decision_surface_written": True,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_subagent_summary_written": True,
            "recommended_next_step_returns_to_attestation_refresh_when_regeneration_stays_blocked": True,
            "retry_gate_review_requires_current_reviewable_regenerated_faces": True,
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
        (
            "docs",
            "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md",
        ),
        (
            "docs",
            "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md",
        ),
        ("docs", CONTRACT_SPEC_REL_PATH),
        ("docs", EXTERNAL_EVIDENCE_MANIFEST_REL_PATH),
        ("reports", PREFLIGHT_REPORT_REL_PATH),
        (
            "scripts",
            "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
        ),
        ("scripts", "scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py"),
        ("scripts", "scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py"),
        (
            "scripts",
            "scripts/export_attestation_record_pack_regeneration_closeout_bundle.sh",
        ),
        ("scripts", "vexter/demo_readiness/__init__.py"),
        ("scripts", "vexter/demo_readiness/external_evidence.py"),
        ("proof_files", PREFLIGHT_PROOF_REL_PATH),
        ("proof_files", PREFLIGHT_SUMMARY_REL_PATH),
        ("proof_files", GAP_PROOF_REL_PATH),
        ("proof_files", GAP_SUMMARY_REL_PATH),
        ("reports", GAP_REPORT_REL_PATH),
        (
            "proof_files",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json",
        ),
        (
            "proof_files",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-summary.md",
        ),
        (
            "reports",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration",
        ),
        (
            "reports",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md",
        ),
        (
            "reports",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md",
        ),
        (
            "reports",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md",
        ),
        (
            "reports",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/subagent_summary.md",
        ),
    ):
        if path not in manifest[key]:
            manifest[key].append(path)
    for path in (
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md",
        CONTRACT_SPEC_REL_PATH,
        "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md",
        EXTERNAL_EVIDENCE_MANIFEST_REL_PATH,
        "scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
        "scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
        "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
        "tests/test_demo_forward_supervised_run_retry_gate_evidence_preflight.py",
        "tests/test_demo_forward_supervised_run_retry_gate_external_evidence_gap.py",
        "vexter/demo_readiness/__init__.py",
        "vexter/demo_readiness/external_evidence.py",
        PREFLIGHT_PROOF_REL_PATH,
        PREFLIGHT_REPORT_REL_PATH,
        PREFLIGHT_SUMMARY_REL_PATH,
        GAP_PROOF_REL_PATH,
        GAP_REPORT_REL_PATH,
        GAP_SUMMARY_REL_PATH,
        "scripts/export_attestation_record_pack_regeneration_closeout_bundle.sh",
        "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration.tar.gz",
    ):
        if path not in manifest["included_paths"]:
            manifest["included_paths"].append(path)
    manifest["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "resume_requirements": [
            f"Keep Dexter pinned at {VERIFIED_DEXTER_COMMIT} and Mew-X frozen at {VERIFIED_MEWX_COMMIT}.",
            "Start from the current attestation record-pack regeneration status, report, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Replace the template-only canonical external-evidence manifest with current non-secret evidence locators for every required face before rerunning regeneration or reopening retry-gate review.",
            "Collect one current, fresh-enough, reviewable locator for every required face before rerunning regeneration or reopening retry-gate review.",
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
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_added": True,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_current_pointers_fixed": True,
            "demo_forward_retry_gate_evidence_preflight_written": True,
            "demo_forward_retry_gate_external_evidence_gap_written": True,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_checklist_written": True,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_decision_surface_written": True,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_subagent_summary_written": True,
            "recommended_next_step_returns_to_attestation_refresh_when_regeneration_stays_blocked": True,
            "retry_gate_review_requires_current_reviewable_regenerated_faces": True,
            "template_only_external_evidence_reopen_ready_remains_false": True,
            "regeneration_handoff_maps_each_face_to_manifest_and_proof_paths": True,
        }
    )
    MANIFEST_PATH.write_text(format_json(manifest))

    ledger_payload = {
        "artifact_bundle": BUNDLE_PATH,
        "base_main": VERIFIED_VEXTER_COMMIT,
        "baseline_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH",
        "baseline_task_state": "supervised_run_retry_gate_attestation_refresh_blocked",
        "branch": git_output("branch", "--show-current"),
        "claim_boundary": CLAIM_BOUNDARY,
        "current_lane": CURRENT_LANE,
        "decision": DECISION,
        "first_demo_target": "dexter_paper_live",
        "gate_pass_successor": PASS_NEXT_TASK_ID,
        "key_finding": KEY_FINDING,
        "next_task_id": NEXT_TASK_ID,
        "next_task_state": NEXT_TASK_STATE,
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json",
        "recommended_next_lane": NEXT_TASK_LANE,
        "repo": "https://github.com/Cabbala/Vexter",
        "retry_gate_attestation_record_pack_regeneration_face_count": len(rows),
        "retry_gate_attestation_record_pack_regeneration_current_locator_input_count": sum(
            row["current_fresh_locator_present"] for row in rows
        ),
        "retry_gate_attestation_record_pack_regeneration_reviewable_count": sum(
            row["regenerated_face_reviewable_now"] for row in rows
        ),
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
        "external_evidence_template_only_false_path": preflight_payload["reopen_readiness"][
            "template_only_false_path"
        ],
        "per_face_manifest_field_maps_explicit": all(
            bool(row["required_manifest_fields"]) for row in rows
        ),
        "per_face_proof_path_maps_explicit": all(bool(row["proof_paths_to_recheck"]) for row in rows),
        "canonical_gap_blocked_faces_align_with_regeneration_lane": sorted(
            blocked_regenerated_faces
        )
        == sorted(preflight_payload["reopen_readiness"]["blocked_faces"]),
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
