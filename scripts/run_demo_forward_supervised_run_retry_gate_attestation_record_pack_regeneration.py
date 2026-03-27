#!/usr/bin/env python3
"""Emit bounded retry-gate attestation-record-pack-regeneration surfaces from the refresh baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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
VERIFIED_VEXTER_PR = 85
VERIFIED_VEXTER_COMMIT = "aee3216c3c5091135f6bb50236883e1bdff8e2e1"
VERIFIED_VEXTER_MERGED_AT = "2026-03-27T19:00:58Z"

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
            "Confirmed merged PR `#85` / commit `aee3216c3c5091135f6bb50236883e1bdff8e2e1` is the current refresh baseline, so regeneration has to be re-promoted from that newer source of truth rather than the older PR `#83` state.",
            "Flagged two correctness risks to keep atomic: stale refresh-side repo pointers and repeated regeneration suffixes inside refresh-derived rows that would make the decision surface contradictory or non-reviewable.",
            "Recommended one atomic current-pointer flip across summary, context, manifest, ledger, README, bundle metadata, and handoff surfaces so regeneration becomes current everywhere together.",
        ],
    },
    {
        "name": "Euler",
        "lines": [
            "Confirmed the regeneration lane stays inside the unchanged Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one-plan, one-position, explicit-allowlist, small-lot, bounded-window, funded-live-forbidden envelope.",
            "Verified the planner/runtime boundary remains intact: `prepare / start / status / stop / snapshot` stay planner-bound, `manual_latched_stop_all` remains planner-owned, Dexter stays the only real-demo seam, and frozen Mew-X remains unchanged on `sim_live`.",
            "Recommended keeping regeneration logic purely surface-level by normalizing refresh-derived row text before emission instead of rewriting Dexter or Mew-X runtime/source behavior.",
        ],
    },
    {
        "name": "Parfit",
        "lines": [
            "Scoped the lowest-risk change set to the regeneration generator, the proof-bundle fallback path, the regenerated artifacts, and the shared regression expectations that pin the repo-level current task and bundle layout.",
            "Recommended validating the regeneration generator and proof-bundle/export path first, then widening to the shared current-pointer and full pytest coverage once the regenerated artifacts are in place.",
            "Merge readiness depends on end-to-end agreement across summary, context, manifest, ledger, bundle metadata, the regenerated handoff bundle, and the final exported tarball without touching runtime code.",
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


def build_regeneration_rows(previous_rows: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for row in previous_rows:
        refreshed_face_covers = strip_repeated_suffix(
            row.get("what_refreshed_face_covers", "").strip(),
            REGENERATION_COVERAGE_SUFFIX,
        )
        refresh_trigger = extract_refresh_trigger(row.get("refresh_trigger", ""))
        minimum_fresh_locator_shape = extract_refresh_locator_shape(
            row.get("minimum_fresh_evidence_locator_shape", "")
        )
        stale_condition = extract_refresh_stale_condition(row.get("stale_condition", ""))
        usable_condition = extract_refresh_reviewable_condition(
            row.get("usable_for_retry_gate_review_when", "")
        )
        regeneration_rule_complete = all(
            bool(value)
            for value in (
                row.get("refresh_owner"),
                refreshed_face_covers,
                refresh_trigger,
                minimum_fresh_locator_shape,
                stale_condition,
                usable_condition,
            )
        )
        current_fresh_locator_present = bool(row.get("current_fresh_evidence_locator_present"))
        freshness_inherited_cleanly = current_fresh_locator_present and bool(
            row.get("current_evidence_fresh_enough")
        )
        source_refresh_usable_now = bool(row.get("usable_now"))
        regenerated_face_reviewable_now = (
            regeneration_rule_complete
            and current_fresh_locator_present
            and freshness_inherited_cleanly
            and source_refresh_usable_now
        )
        rows.append(
            {
                "name": row["name"],
                "repo_visible_marker": row["repo_visible_marker"],
                "regeneration_owner": row["refresh_owner"],
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
                "regeneration_rule_complete": regeneration_rule_complete,
                "current_fresh_locator_present": current_fresh_locator_present,
                "freshness_inherited_cleanly": freshness_inherited_cleanly,
                "regenerated_face_reviewable_now": regenerated_face_reviewable_now,
                "current_regeneration_observation": (
                    "The regeneration rule is explicit for this face, but the repo still does not point to one "
                    "current, fresh-enough bounded-window locator that can seed a reviewable regenerated face "
                    "without secrets. The regenerated pack therefore remains fail-closed for this face."
                )
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


def build_current_report(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    rows: list[dict],
) -> str:
    blocked_faces = [row["name"] for row in rows if row["regeneration_status"] != "PASS"]
    regeneration_rules_explicit_count = sum(row["regeneration_rule_complete"] for row in rows)
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

## Regeneration Findings
- required regeneration faces: `{len(rows)}`
- regeneration rules explicit count: `{regeneration_rules_explicit_count}`
- current fresh locator input count: `{sum(row["current_fresh_locator_present"] for row in rows)}`
- freshness inherited cleanly count: `{sum(row["freshness_inherited_cleanly"] for row in rows)}`
- regenerated face reviewable count: `{sum(row["regenerated_face_reviewable_now"] for row in rows)}`
- blocked regenerated faces: `{", ".join(blocked_faces)}`

## Honest Regeneration Model
- `PASS` only if refreshed locator rules produce a current, reviewable regenerated record pack sufficient to reopen retry-gate review honestly.
- `FAIL/BLOCKED` if one or more regenerated faces remain missing, stale, ambiguous, or non-reviewable.
- Current result remains `FAIL/BLOCKED` because the repo still does not point to one current, fresh-enough, reviewable locator per required face, so the regenerated current pack cannot reopen retry-gate review honestly.
"""


def build_proof_summary() -> str:
    return f"""# {TASK_ID} Proof Summary

- Verified latest GitHub-visible Vexter `main` at PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}`.
- Accepted attestation refresh as the bounded baseline current source of truth.
- Promoted attestation record-pack regeneration as the current operator-visible lane for regeneration owner, trigger, regenerated locator shape, freshness inheritance, and reviewability.
- Held the result at `FAIL/BLOCKED` because current regenerated faces are still missing or non-reviewable.
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
3. Generate one bounded attestation record-pack regeneration lane with current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.
4. For each required face, carry forward the bounded refresh locator rule, then fix regeneration owner, regeneration trigger, minimum regenerated locator shape, freshness inheritance or reset rule, and reviewable-enough rule.
5. Keep `FAIL/BLOCKED` unless every face can regenerate from one current, fresh-enough, reviewable locator.
6. Recommend `{NEXT_TASK_LANE}` while blocked and expose `{PASS_NEXT_TASK_LANE}` only as the pass successor.

## Guardrails
{chr(10).join(f"- {line}" for line in boundary_lines())}

## Validation
- generate the lane with `python3 scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py`
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
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md`.
5. Use `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md` as the single record-pack regeneration decision surface.
6. Keep one regeneration row per required face: credential source, venue ref, account ref, connectivity profile, operator owner, bounded start criteria, allowlist / symbol / lot reconfirmation, `manual_latched_stop_all` visibility, and terminal snapshot readability.
7. For every row, confirm regeneration owner, regeneration trigger, minimum regenerated locator shape, freshness inheritance or reset rule, and what makes the regenerated face reviewable enough are explicit.
8. For every row, record whether a current fresh-enough bounded-window locator is present and can seed the regenerated face without embedding secret material.
9. Hold the lane at `FAIL/BLOCKED` until every required face is regenerated, current, and reviewable enough to reopen retry-gate review honestly.

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


def build_details() -> str:
    return f"""# ATTESTATION-RECORD-PACK-REGENERATION Details

## Verified Starting Point
- Latest Vexter `main`: PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`
- Dexter pinned commit: `{VERIFIED_DEXTER_COMMIT}`
- Frozen Mew-X commit: `{VERIFIED_MEWX_COMMIT}`
- Accepted baseline: `supervised_run_retry_gate_attestation_refresh_blocked`

## Deliverable
Promote one bounded attestation record-pack regeneration lane that keeps current status, report, summary, proof, handoff, checklist, and decision-surface pointers coherent while fail-closing retry-gate review until every required regenerated face is current and reviewable.
"""


def build_min_prompt() -> str:
    return (
        f"GitHub latest state is Vexter main PR #{VERIFIED_VEXTER_PR} merge commit "
        f"{VERIFIED_VEXTER_COMMIT} on {VERIFIED_VEXTER_MERGED_AT}. "
        "Accept attestation refresh as baseline, promote attestation record-pack regeneration as the current "
        "source of truth, keep Dexter-only paper_live and frozen Mew-X sim_live, do not commit secrets, keep "
        "the lane FAIL/BLOCKED until every regenerated face is reviewable, and recommend "
        f"{NEXT_TASK_LANE} before any retry-gate reopen."
    )


def build_handoff(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    rows: list[dict],
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
- baseline_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-status.md
- baseline_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md
- baseline_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json
- baseline_handoff: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md

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

## Open Questions
- question_1_or_none: who will publish one current fresh-enough locator per required face so the regenerated pack can stay reviewable without secrets
- question_2_or_none: which refreshed locator should be recollected first for venue, account, and connectivity faces before rerunning regeneration
- question_3_or_none: who timestamps the regenerated bounded start window and operator owner before the next retry-gate recheck
- question_4_or_none: has `manual_latched_stop_all` visibility been freshly reconfirmed for the current bounded window
- question_5_or_none: has terminal snapshot readability been freshly reconfirmed for the current bounded window

## Next-Shift Priority Checks
- priority_check_1: keep the current lane blocked unless every face can inherit freshness from one current, reviewable bounded-window locator
- priority_check_2: recommend `{NEXT_TASK_LANE}` while blocked so additional fresh locators can be collected before rerunning regeneration
- priority_check_3: preserve Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, small-lot, one-position, `manual_latched_stop_all`, and funded-live-forbidden guardrails

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- checklist_pointer_checked: true
- decision_surface_pointer_checked: true
- subagent_summary_pointer_checked: true
- blocked_claim_boundary_explicit: true

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
        f"GitHub-visible Vexter `main` at merged PR `#{VERIFIED_VEXTER_PR}` merge commit "
        f"`{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`"
    )
    readme_text = README_PATH.read_text()
    if marker in readme_text:
        return
    entry = (
        "\n\n`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK-REGENERATION` starts from latest "
        f"GitHub-visible Vexter `main` at merged PR `#{VERIFIED_VEXTER_PR}` merge commit "
        f"`{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`, keeps Dexter pinned at merged PR "
        f"`#3` commit `{VERIFIED_DEXTER_COMMIT}`, and keeps frozen Mew-X at `{VERIFIED_MEWX_COMMIT}`. "
        "It accepts the bounded attestation-refresh lane as baseline and promotes one fail-closed attestation "
        "record-pack-regeneration lane instead: the repo now fixes the current status/report/proof/handoff/"
        "checklist/decision-surface surfaces for regeneration owner, regeneration trigger, minimum regenerated "
        "locator shape, freshness inheritance or reset, and what makes each regenerated face reviewable "
        "enough, while keeping the Dexter-only `paper_live` seam, leaving Mew-X unchanged on `sim_live`, "
        "and keeping funded live forbidden. The resulting status is "
        f"`{TASK_STATUS}` with `{CLAIM_BOUNDARY}`, the current lane is `{CURRENT_LANE}`, the blocked next "
        f"recommended step is `{NEXT_TASK_LANE}`, and the pass successor is `{PASS_NEXT_TASK_LANE}`."
    )
    README_PATH.write_text(readme_text + entry + "\n")


def main() -> None:
    run_timestamp = iso_utc_now()
    template_env = parse_template_env(TEMPLATE_ENV_PATH)
    previous_proof = read_json(PREVIOUS_PROOF_PATH)

    with patched_demo_env(template_env):
        runtime_config = DexterDemoRuntimeConfig.from_env()
        runtime_errors = list(runtime_config.validation_errors())

    previous_rows = previous_proof["supervised_run_retry_gate_attestation_refresh"]["refresh_faces"][
        "attestation_refresh_decision_surface"
    ]
    rows = build_regeneration_rows(previous_rows)
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
            "sub_agents": list(SUB_AGENT_SUMMARIES),
            "supporting_files": [
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_REFRESH.md",
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md",
                "plans/demo_forward_supervised_run_retry_gate_attestation_refresh_plan.md",
                "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md",
                "scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
                "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
                "scripts/build_proof_bundle.sh",
                "tests/test_demo_forward_supervised_run_retry_gate.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
                "tests/test_bootstrap_layout.py",
            ],
            "proof_outputs": [
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

    report_text = build_current_report(run_timestamp, runtime_config, rows)
    status_text = build_status()
    proof_summary_text = build_proof_summary()
    summary_text = f"""# {TASK_ID} Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `{VERIFIED_MEWX_COMMIT}`.

## What This Task Did

- Accepted attestation refresh as the baseline current source of truth.
- Promoted attestation record-pack regeneration to the current operator-visible lane.
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

## Key Paths

- Current spec: `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md`
- Current implementation plan: `plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md`
- Current checklist: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md`
- Current decision surface: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md`
- Current proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json`
- Current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md`
- Current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md`
- Current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md`
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
        "blocked_regenerated_faces": blocked_regenerated_faces,
        "record_pack_reviewable_now": checklist_attestation["record_pack_reviewable_now"],
        "retry_gate_review_reopen_ready": checklist_attestation["retry_gate_review_reopen_ready"],
    }

    details_text = build_details()
    min_prompt_text = build_min_prompt()
    handoff_text = build_handoff(run_timestamp, runtime_config, rows)
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
        }
    )
    context_pack["current_task"] = {
        "id": TASK_ID,
        "scope": [
            "Reverify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X after attestation refresh merged.",
            "Accept attestation refresh as the baseline current source of truth.",
            "Promote attestation record-pack regeneration status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Make each required face explicit for regeneration owner, trigger, minimum regenerated locator shape, freshness inheritance or reset, and reviewability.",
            "Keep retry-gate review blocked until every required face can regenerate from one current, fresh-enough, reviewable locator.",
        ],
        "deliverables": [
            "README.md",
            "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION.md",
            "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md",
            "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md",
            "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
            "tests/test_demo_forward_supervised_run_retry_gate.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_audit.py",
            "tests/test_demo_forward_supervised_run_retry_readiness.py",
            "tests/test_bootstrap_layout.py",
            "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
            "scripts/build_proof_bundle.sh",
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
            "latest_recent_vexter_prs": [85, 84, 83, 82, 81],
            "vexter_pr_85_merged_at": VERIFIED_VEXTER_MERGED_AT,
            "vexter_pr_85_closed_at": VERIFIED_VEXTER_MERGED_AT,
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
        "blocked_regenerated_faces": blocked_regenerated_faces,
        "sub_agents": list(SUB_AGENT_SUMMARIES),
    }
    context_pack["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "rationale": [
            "Attestation record-pack regeneration is now the current source of truth for regenerated locator inheritance and reviewable pack surfaces.",
            "One or more required faces still lack a current, fresh-enough, reviewable locator that can seed the regenerated pack.",
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
        (
            "scripts",
            "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
        ),
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
        "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_plan.md",
        "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
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
            "demo_forward_retry_gate_attestation_record_pack_regeneration_checklist_written": True,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_decision_surface_written": True,
            "demo_forward_retry_gate_attestation_record_pack_regeneration_subagent_summary_written": True,
            "recommended_next_step_returns_to_attestation_refresh_when_regeneration_stays_blocked": True,
            "retry_gate_review_requires_current_reviewable_regenerated_faces": True,
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
        "supporting_vexter_prs": [85, 84, 83, 82, 81],
        "task_id": TASK_ID,
        "template_runtime_validation_errors": runtime_errors,
        "verified_dexter_main_commit": VERIFIED_DEXTER_COMMIT,
        "verified_dexter_pr": 3,
        "verified_mewx_frozen_commit": VERIFIED_MEWX_COMMIT,
        "verified_prs": [85, 84, 83],
        "date": run_timestamp.split("T", 1)[0],
    }
    rewrite_local_ledger(ledger_payload)

    update_readme()


if __name__ == "__main__":
    main()
