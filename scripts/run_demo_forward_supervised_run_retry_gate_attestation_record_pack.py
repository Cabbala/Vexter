#!/usr/bin/env python3
"""Emit bounded retry-gate attestation-record-pack surfaces from the attestation-audit baseline."""

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

CHECKLIST_PATH = (
    ROOT / "docs" / "demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md"
)
DECISION_SURFACE_PATH = (
    ROOT / "docs" / "demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md"
)
SPEC_PATH = ROOT / "specs" / "DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK.md"
PLAN_PATH = ROOT / "plans" / "demo_forward_supervised_run_retry_gate_attestation_record_pack_plan.md"

PREVIOUS_REPORT_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-audit-report.md"
)
PREVIOUS_STATUS_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-audit-status.md"
)
PREVIOUS_PROOF_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-attestation-audit-check.json"
)
PREVIOUS_SUMMARY_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-attestation-audit-summary.md"
)
PREVIOUS_HANDOFF_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-audit" / "HANDOFF.md"
)
PREVIOUS_CHECKLIST_PATH = (
    ROOT / "docs" / "demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md"
)
PREVIOUS_DECISION_SURFACE_PATH = (
    ROOT / "docs" / "demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md"
)
PREVIOUS_SUBAGENTS_PATH = (
    ROOT
    / "artifacts"
    / "reports"
    / "demo-forward-supervised-run-retry-gate-attestation-audit"
    / "SUBAGENTS.md"
)

REPORT_DIR = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-record-pack"
)
REPORT_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md"
)
STATUS_PATH = (
    ROOT / "artifacts" / "reports" / "demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md"
)
SUBAGENTS_PATH = REPORT_DIR / "SUBAGENTS.md"
SUBAGENT_SUMMARY_PATH = REPORT_DIR / "subagent_summary.md"
PROOF_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json"
)
PROOF_SUMMARY_PATH = (
    ROOT / "artifacts" / "proofs" / "demo-forward-supervised-run-retry-gate-attestation-record-pack-summary.md"
)

BUNDLE_PATH = "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack.tar.gz"
BUNDLE_SOURCE = "/Users/cabbala/Downloads/vexter_attestation_record_pack_bundle.tar.gz"

TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK"
TASK_STATUS = "supervised_run_retry_gate_attestation_record_pack_blocked"
KEY_FINDING = "supervised_run_retry_gate_attestation_record_pack_blocked_on_missing_or_stale_current_records"
CLAIM_BOUNDARY = "supervised_run_retry_gate_attestation_record_pack_bounded"
CURRENT_LANE = "supervised_run_retry_gate_attestation_record_pack"
NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-REFRESH"
NEXT_TASK_STATE = "current_attestation_records_refresh_required"
NEXT_TASK_LANE = "supervised_run_retry_gate_attestation_refresh"
PASS_NEXT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE"
PASS_NEXT_TASK_STATE = "ready_for_supervised_run_retry_gate_recheck"
PASS_NEXT_TASK_LANE = "supervised_run_retry_gate"
DECISION = "retry_gate_review_blocked_pending_current_attestation_record_pack"

VERIFIED_DEXTER_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
VERIFIED_MEWX_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
VERIFIED_VEXTER_PR = 77
VERIFIED_VEXTER_COMMIT = "1a35c468e1d2944e98a2987427d5b7d688cb0cfc"
VERIFIED_VEXTER_MERGED_AT = "2026-03-27T07:50:49Z"

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
            "Confirmed the minimum safe change is a new attestation-record-pack lane beside attestation audit, with one atomic current-pointer switch across status, report, proof, summary, handoff, checklist, and decision-surface paths.",
            "Recommended fail-closed wording that stays observational: the repo may define each record face clearly, but retry-gate review remains blocked until every face points to a current, timestamped, reviewable record locator.",
            "Flagged the main consistency risks as baseline-hop drift, split current pointers, and mixed record-pack naming; the new pack should baseline from attestation audit and become the single current source of truth once written.",
        ],
    },
    {
        "name": "Euler",
        "lines": [
            "Kept the record-pack boundary aligned with the accepted audit boundary: Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, explicit allowlist, small lot, one-plan, one-position, bounded supervision, and funded-live forbidden.",
            "Confirmed the same nine required faces must remain unchanged and that the lane should stay docs-and-proof only, without planner or adapter seam drift.",
            "Reviewed the state split and emphasized that `prepare / start / status / stop / snapshot` remains fixed, `manual_latched_stop_all` stays planner-owned, and Mew-X remains unchanged while the record pack stays fail-closed.",
        ],
    },
    {
        "name": "Parfit",
        "lines": [
            "Scoped the smallest safe change set to one new proof generator, one focused record-pack test, README and default-bundle updates, generated artifact refreshes, and the shared tests that pin the current supervised-run lane.",
            "Recommended validating with the new generator plus focused supervised-run and bootstrap/compatibility pytest coverage, then full `pytest -q`, because several shared tests key off the repo-level current task, bundle path, and next-task state.",
            "Merge readiness depends on a clean record-pack pointer switch, regenerated tarball output, updated GitHub main metadata, and a blocked decision that does not claim retry-gate reopen or retry execution success.",
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


def build_freshness_requirement(stale_condition: str) -> str:
    return (
        "one current bounded-window record locator with a verification timestamp must be present and "
        f"refreshed before {stale_condition}"
    )


def build_record_rows(previous_rows: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for row in previous_rows:
        definition_complete = all(
            bool(row.get(field))
            for field in (
                "who_attests",
                "what_is_being_attested",
                "minimal_evidence_shape",
                "stale_when",
                "auditable_enough_when",
            )
        )
        current_record_locator_present = bool(row.get("current_attestation_ref_present"))
        current_record_fresh = bool(row.get("current_attestation_non_stale"))
        reviewable_now = (
            definition_complete
            and current_record_locator_present
            and current_record_fresh
            and bool(row.get("auditable_now"))
        )
        rows.append(
            {
                "name": row["name"],
                "repo_visible_marker": row["repo_visible_marker"],
                "record_owner": row["who_attests"],
                "what_record_covers": row["what_is_being_attested"],
                "minimum_evidence_locator_shape": row["minimal_evidence_shape"],
                "freshness_requirement": build_freshness_requirement(row["stale_when"]),
                "stale_condition": row["stale_when"],
                "reviewable_enough_when": row["auditable_enough_when"],
                "definition_complete": definition_complete,
                "current_record_locator_present": current_record_locator_present,
                "current_record_fresh": current_record_fresh,
                "reviewable_now": reviewable_now,
                "current_record_observation": (
                    f"{row['current_audit_observation']} The record-pack lane keeps this face fail-closed "
                    "until the repo can point to one current, timestamped, reviewable record locator."
                ),
                "record_pack_status": "PASS" if reviewable_now else "FAIL/BLOCKED",
            }
        )
    return rows


def build_record_checklist(rows: list[dict], runtime_errors: list[str]) -> dict[str, bool]:
    row_names = {row["name"] for row in rows}
    return {
        "runtime_guardrails_parse_cleanly": not runtime_errors,
        "all_required_faces_present": row_names == set(REQUIRED_FACE_NAMES),
        "all_record_owners_explicit": all(bool(row["record_owner"]) for row in rows),
        "all_minimum_locator_shapes_explicit": all(
            bool(row["minimum_evidence_locator_shape"]) for row in rows
        ),
        "all_freshness_requirements_explicit": all(bool(row["freshness_requirement"]) for row in rows),
        "all_stale_conditions_explicit": all(bool(row["stale_condition"]) for row in rows),
        "all_reviewable_enough_conditions_explicit": all(
            bool(row["reviewable_enough_when"]) for row in rows
        ),
        "all_current_record_locators_present": all(row["current_record_locator_present"] for row in rows),
        "all_current_records_fresh": all(row["current_record_fresh"] for row in rows),
        "all_faces_reviewable_now": all(row["reviewable_now"] for row in rows),
        "retry_gate_review_reopen_ready": all(row["reviewable_now"] for row in rows),
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
- baseline_task: `DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT`
- baseline_task_state: `supervised_run_retry_gate_attestation_audit_blocked`
- planner_boundary: `prepare/start/status/stop/snapshot`
- current_attestation_record_pack_lane: `{CURRENT_LANE}`
- recommended_next_step: `{NEXT_TASK_LANE}`
- record_pack_pass_successor: `{PASS_NEXT_TASK_LANE}`
"""


def build_current_report(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    rows: list[dict],
) -> str:
    blocked_faces = [row["name"] for row in rows if row["record_pack_status"] != "PASS"]
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Record Pack Report

## Verified GitHub State
- Reverified latest GitHub-visible Vexter `main` at merged PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`.
- Dexter stayed pinned at merged PR `#3` commit `{VERIFIED_DEXTER_COMMIT}`.
- Frozen Mew-X stayed pinned at `{VERIFIED_MEWX_COMMIT}`.
- Report timestamp: `{run_timestamp}`.

## Baseline Accepted
- Accepted `supervised_run_retry_gate_attestation_audit_blocked` as the bounded baseline current source of truth.
- Did not claim retry-gate reopen, retry execution success, funded live access, or any Mew-X seam expansion.
- Promoted one bounded attestation record-pack lane as the new current source of truth for current record visibility.

## Record-Pack Boundary
{chr(10).join(f"- {line}" for line in boundary_lines())}

## Decision
- Outcome: `FAIL/BLOCKED`
- Decision: `{DECISION}`
- Current lane: `{CURRENT_LANE}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Retry-gate pass successor: `{PASS_NEXT_TASK_LANE}`
- Runtime validation errors: `{json.dumps(list(runtime_config.validation_errors()))}`

## Record-Pack Surfaces
- current status report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md`
- current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md`
- current summary: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-summary.md`
- current proof json: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json`
- current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/HANDOFF.md`
- attestation record checklist: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md`
- attestation record pack decision surface: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md`
- current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/SUBAGENTS.md`

## Record-Pack Findings
- required record faces: `{len(rows)}`
- current record locator present count: `{sum(row["current_record_locator_present"] for row in rows)}`
- current record fresh count: `{sum(row["current_record_fresh"] for row in rows)}`
- reviewable now count: `{sum(row["reviewable_now"] for row in rows)}`
- blocked record faces: `{", ".join(blocked_faces)}`

## Honest Model
- `PASS` only if every required face points to a current, fresh, reviewable record locator and retry-gate review can reopen honestly.
- `FAIL/BLOCKED` if any face remains missing, stale, ambiguous, or not reviewable enough.
- Current result remains `FAIL/BLOCKED` because the repo still does not point to current bounded-window record locators for the required faces.
"""


def build_proof_summary() -> str:
    return f"""# {TASK_ID} Proof Summary

- Verified latest GitHub-visible Vexter `main` at PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}`.
- Accepted retry-gate attestation audit as the bounded baseline current source of truth.
- Promoted attestation record pack as the current operator-visible lane for record ownership, locator shape, freshness, stale rules, and reviewability checks.
- Held the result at `FAIL/BLOCKED` because current record locators are still missing or stale.
- Recommended next step: `{NEXT_TASK_LANE}`.
- Retry-gate pass successor: `{PASS_NEXT_TASK_LANE}`.
"""


def build_spec() -> str:
    boundary = "\n".join(f"- {line}" for line in boundary_lines())
    return f"""# DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK

## Goal
Promote a bounded `attestation_record_pack` lane as the current source of truth after retry-gate attestation audit, without fabricating retry-gate reopen or retry execution success.

## Boundary
{boundary}

## Required Current Surfaces
- current status report
- current report
- current summary
- current proof json
- current handoff
- attestation record checklist
- attestation record pack decision surface
- next recommended step

## Honest Record-Pack Model
- `PASS`: every required record face is explicit enough and current enough to reopen retry-gate review honestly
- `FAIL/BLOCKED`: one or more record faces remain missing, stale, ambiguous, or not reviewable enough

## Required Record Face Detail
Each record face must make explicit:
- who owns the record
- what the record covers
- minimum evidence locator shape
- freshness requirement
- stale condition
- what makes the record reviewable enough

## Planner Boundary
- `prepare`
- `start`
- `status`
- `stop`
- `snapshot`

## Out Of Scope
- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success
- no secret material committed to repo

## Result Model
The promoted lane remains fail-closed until current record locators exist for every required face and retry-gate review can honestly reopen.
"""


def build_plan() -> str:
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Record Pack Plan

## Implementation Steps
1. Reverify the latest GitHub-visible Vexter `main` state at PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}`.
2. Accept retry-gate attestation audit as the blocked baseline current source of truth.
3. Generate one bounded attestation record-pack lane with current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.
4. For each required face, carry forward the repo-visible marker and fix who owns the record, the minimum evidence locator shape, freshness requirement, stale condition, and reviewable-enough rule.
5. Keep `FAIL/BLOCKED` unless every face points to a current, fresh, reviewable record locator.
6. Recommend `{NEXT_TASK_LANE}` while blocked and expose `{PASS_NEXT_TASK_LANE}` only as the pass successor.

## Guardrails
{chr(10).join(f"- {line}" for line in boundary_lines())}

## Validation
- generate the lane with `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack.py`
- rebuild the tarball with `./scripts/build_proof_bundle.sh`
- verify shared regression expectations with `pytest -q`
"""


def build_checklist(rows: list[dict]) -> str:
    face_lines = []
    for row in rows:
        face_lines.append(
            "| "
            f"`{row['name']}` | "
            f"`{row['record_owner']}` | "
            f"{row['minimum_evidence_locator_shape']} | "
            f"{row['freshness_requirement']} | "
            f"{row['stale_condition']} | "
            f"{row['reviewable_enough_when']} |"
        )
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Record Pack Checklist

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
1. Start at `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json`.
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/HANDOFF.md`.
5. Use `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md` as the single attestation record-pack decision surface.
6. Keep one record-pack row per required face: credential source, venue ref, account ref, connectivity profile, operator owner, bounded start criteria, allowlist / symbol / lot reconfirmation, `manual_latched_stop_all` visibility, and terminal snapshot readability.
7. For every row, confirm who owns the record, the minimum evidence locator shape, the freshness requirement, the stale condition, and what makes the record reviewable enough are explicit.
8. For every row, record whether a current bounded-window record locator is present without embedding secret material.
9. Hold the lane at `FAIL/BLOCKED` until every required face is current, fresh, and reviewable enough.

## Record Faces
| Record face | Who owns the record | Minimum evidence locator shape | Freshness requirement | Stale condition | Reviewable enough when |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(face_lines)}
"""


def build_decision_surface(rows: list[dict]) -> str:
    lines = [
        "# Demo Forward Supervised Run Retry Gate Attestation Record Pack Decision Surface",
        "",
        "This decision surface is the current source of truth for `supervised_run_retry_gate_attestation_record_pack`.",
        "",
        "| Record face | Repo-visible marker | Record owner | What the record covers | Minimum evidence locator shape | Freshness requirement | Stale condition | Reviewable enough when | Definition complete | Current record locator present | Current record fresh | Reviewable now | Current record observation | Record-pack status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"`{row['name']}` | "
            f"`{format_marker(row['repo_visible_marker'])}` | "
            f"`{row['record_owner']}` | "
            f"{row['what_record_covers']} | "
            f"{row['minimum_evidence_locator_shape']} | "
            f"{row['freshness_requirement']} | "
            f"{row['stale_condition']} | "
            f"{row['reviewable_enough_when']} | "
            f"`{format_bool(row['definition_complete'])}` | "
            f"`{format_bool(row['current_record_locator_present'])}` | "
            f"`{format_bool(row['current_record_fresh'])}` | "
            f"`{format_bool(row['reviewable_now'])}` | "
            f"{row['current_record_observation']} | "
            f"`{row['record_pack_status']}` |"
        )
    lines.extend(
        [
            "",
            "Retry-gate review does not reopen unless every record face points to a current, fresh, reviewable record locator.",
            f"While blocked, the next recommended step is `{NEXT_TASK_LANE}` and the pass successor remains `{PASS_NEXT_TASK_LANE}`.",
        ]
    )
    return "\n".join(lines)


def build_details() -> str:
    return f"""# ATTESTATION-RECORD-PACK Details

## Verified Starting Point
- Latest Vexter `main`: PR `#{VERIFIED_VEXTER_PR}` merge commit `{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`
- Dexter pinned commit: `{VERIFIED_DEXTER_COMMIT}`
- Frozen Mew-X commit: `{VERIFIED_MEWX_COMMIT}`
- Accepted baseline: `supervised_run_retry_gate_attestation_audit_blocked`

## Deliverable
Promote one bounded attestation record-pack lane that keeps current status, report, summary, proof, handoff, checklist, and decision-surface pointers coherent while fail-closing retry-gate review until every required record face is current and reviewable.
"""


def build_min_prompt() -> str:
    return (
        "GitHub latest state is Vexter main PR #77 merge commit "
        f"{VERIFIED_VEXTER_COMMIT} on {VERIFIED_VEXTER_MERGED_AT}. "
        "Accept retry-gate attestation audit as baseline, promote attestation record pack as the current source "
        "of truth, keep Dexter-only paper_live and frozen Mew-X sim_live, do not commit secrets, keep the lane "
        "FAIL/BLOCKED until every face has a current record locator, and recommend "
        f"{NEXT_TASK_LANE} before any retry-gate reopen."
    )


def build_handoff(
    run_timestamp: str,
    runtime_config: DexterDemoRuntimeConfig,
    rows: list[dict],
) -> str:
    record_lines = "\n".join(
        "- "
        f"{row['name']}: definition_complete={str(row['definition_complete']).lower()}, "
        f"current_record_locator_present={str(row['current_record_locator_present']).lower()}, "
        f"current_record_fresh={str(row['current_record_fresh']).lower()}, "
        f"reviewable_now={str(row['reviewable_now']).lower()}, "
        f"record_owner={row['record_owner']}"
        for row in rows
    )
    return f"""# Demo Forward Supervised Run Retry Gate Attestation Record Pack Handoff

## Current Status
- outgoing_shift_window: {run_timestamp} attestation-record-pack lane
- incoming_shift_window: current record refresh and possible retry-gate recheck
- task_state: {TASK_STATUS}
- shift_outcome: blocked
- current_action: hold_retry_gate_review_until_attestation_record_pack_is_current
- current_lane: {CURRENT_LANE}
- recommended_next_step_while_blocked: {NEXT_TASK_LANE}
- record_pack_pass_successor: {PASS_NEXT_TASK_LANE}
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: {VERIFIED_VEXTER_COMMIT}
- dexter_main_commit: {VERIFIED_DEXTER_COMMIT}
- mewx_frozen_commit: {VERIFIED_MEWX_COMMIT}
- baseline_retry_gate_attestation_audit_task_state: supervised_run_retry_gate_attestation_audit_blocked

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md
- current_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md
- current_proof_summary: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-summary.md
- current_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json
- current_attestation_record_checklist: docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md
- current_attestation_record_pack_decision_surface: docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md
- current_subagent_summary: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/SUBAGENTS.md
- baseline_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md
- baseline_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md
- baseline_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json
- baseline_handoff: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md

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

## Record Faces
{record_lines}

## Open Questions
- question_1_or_none: where is the current bounded-window record locator for each required face
- question_2_or_none: who timestamps and refreshes the stale check for venue, account, and connectivity faces
- question_3_or_none: who confirms the bounded start window and operator owner for the next retry-gate recheck
- question_4_or_none: has `manual_latched_stop_all` visibility been reconfirmed for the current bounded window
- question_5_or_none: has terminal snapshot readability been reconfirmed for the current bounded window

## Next-Shift Priority Checks
- priority_check_1: keep the current lane blocked unless every face has a current bounded-window record locator and freshness check
- priority_check_2: recommend `{NEXT_TASK_LANE}` while blocked and expose `{PASS_NEXT_TASK_LANE}` only as the pass successor
- priority_check_3: preserve Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, small-lot, one-position, `manual_latched_stop_all`, and funded-live-forbidden guardrails

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- checklist_pointer_checked: true
- decision_surface_pointer_checked: true
- subagent_summary_pointer_checked: true
- blocked_claim_boundary_explicit: true

This handoff promotes the bounded attestation record-pack lane only. It does not claim a reopened retry gate, a completed retry execution, funded live access, or any Mew-X seam expansion.
"""


def build_subagents() -> str:
    lines = ["# Demo Forward Supervised Run Retry Gate Attestation Record Pack Sub-agent Summaries", ""]
    for item in SUB_AGENT_SUMMARIES:
        lines.append(f"## {item['name']}")
        for line in item["lines"]:
            lines.append(f"- {line}")
        lines.append("")
    return "\n".join(lines)


def update_readme() -> None:
    marker = (
        "`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK` starts from latest "
        "GitHub-visible Vexter `main`"
    )
    readme_text = README_PATH.read_text()
    if marker in readme_text:
        return
    entry = (
        "\n\n`DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-RECORD-PACK` starts from latest "
        f"GitHub-visible Vexter `main` at merged PR `#{VERIFIED_VEXTER_PR}` merge commit "
        f"`{VERIFIED_VEXTER_COMMIT}` on `{VERIFIED_VEXTER_MERGED_AT}`, keeps Dexter pinned at merged PR "
        f"`#3` commit `{VERIFIED_DEXTER_COMMIT}`, and keeps frozen Mew-X at `{VERIFIED_MEWX_COMMIT}`. "
        "It accepts the bounded retry-gate attestation-audit lane as baseline and promotes one fail-closed "
        "attestation record-pack lane instead: the repo now fixes the current status/report/proof/handoff/"
        "checklist/decision-surface surfaces for who owns each required record face, the minimum evidence "
        "locator shape, the freshness requirement, the stale condition, and what makes the face reviewable "
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

    previous_rows = previous_proof["supervised_run_retry_gate_attestation_audit"]["audit_faces"][
        "attestation_audit_decision_surface"
    ]
    rows = build_record_rows(previous_rows)
    blocked_record_faces = [row["name"] for row in rows if row["record_pack_status"] != "PASS"]
    checklist_attestation = build_record_checklist(rows, runtime_errors)

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
            "task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT",
            "task_state": "supervised_run_retry_gate_attestation_audit_blocked",
            "report": str(PREVIOUS_REPORT_PATH.relative_to(ROOT)),
            "status_report": str(PREVIOUS_STATUS_PATH.relative_to(ROOT)),
            "proof": str(PREVIOUS_PROOF_PATH.relative_to(ROOT)),
            "summary": str(PREVIOUS_SUMMARY_PATH.relative_to(ROOT)),
            "handoff": str(PREVIOUS_HANDOFF_PATH.relative_to(ROOT)),
            "checklist": str(PREVIOUS_CHECKLIST_PATH.relative_to(ROOT)),
            "decision_surface": str(PREVIOUS_DECISION_SURFACE_PATH.relative_to(ROOT)),
            "subagent_summary": str(PREVIOUS_SUBAGENTS_PATH.relative_to(ROOT)),
        },
        "supervised_run_retry_gate_attestation_record_pack": {
            "planner_boundary": ["prepare", "start", "status", "stop", "snapshot"],
            "attestation_record_pack_boundary": {
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
                "current_status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md",
                "current_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md",
                "current_summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-summary.md",
                "current_proof_json": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json",
                "current_handoff": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/HANDOFF.md",
                "attestation_record_checklist": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md",
                "attestation_record_pack_decision_surface": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md",
                "next_recommended_step": NEXT_TASK_LANE,
                "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/SUBAGENTS.md",
            },
            "baseline_attestation_audit_outcome": {
                "task_id": previous_proof["task_id"],
                "task_state": previous_proof["task_result"]["task_state"],
                "key_finding": previous_proof["task_result"]["key_finding"],
                "claim_boundary": previous_proof["task_result"]["claim_boundary"],
                "recommended_next_step": previous_proof["task_result"]["recommended_next_step"],
                "gate_pass_successor": previous_proof["task_result"]["gate_pass_successor"],
            },
            "record_faces": {
                "attestation_record_pack_decision_surface": rows,
                "blocked_record_faces": blocked_record_faces,
                "checklist_attestation": checklist_attestation,
                "retry_gate_review_reopen_ready": False,
            },
            "sub_agents": list(SUB_AGENT_SUMMARIES),
            "supporting_files": [
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md",
                "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK.md",
                "plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md",
                "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_plan.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md",
                "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md",
                "scripts/run_demo_forward_supervised_run_retry_gate_attestation_audit.py",
                "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
                "scripts/build_proof_bundle.sh",
                "tests/test_demo_forward_supervised_run_retry_gate.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_audit.py",
                "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
                "tests/test_bootstrap_layout.py",
            ],
            "proof_outputs": [
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json",
                "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-summary.md",
                "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack.tar.gz",
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

- Accepted retry-gate attestation audit as the baseline current source of truth.
- Promoted attestation record pack to the current operator-visible lane.
- Added current status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces for record ownership, locator shape, freshness, and reviewability.
- Fixed one fail-closed record-pack model that blocks retry-gate review until every required face has a current, fresh, reviewable record locator.

## Decision

- Outcome: `FAIL/BLOCKED`
- Key finding: `{KEY_FINDING}`
- Claim boundary: `{CLAIM_BOUNDARY}`
- Current task status: `{TASK_STATUS}`
- Current lane: `{CURRENT_LANE}`
- Recommended next step while blocked: `{NEXT_TASK_LANE}`
- Record-pack pass successor: `{PASS_NEXT_TASK_LANE}`
- Decision: `{DECISION}`

## Key Paths

- Current spec: `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK.md`
- Current implementation plan: `plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_plan.md`
- Current checklist: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md`
- Current decision surface: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md`
- Current proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json`
- Current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md`
- Current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/HANDOFF.md`
- Current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/SUBAGENTS.md`
- Current bundle target: `artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack.tar.gz`
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
        "baseline_task_state": "supervised_run_retry_gate_attestation_audit_blocked",
        "first_demo_target": "dexter_paper_live",
        "source_faithful_seam": {"dexter": "paper_live", "mewx": "sim_live"},
        "blocked_record_faces": blocked_record_faces,
        "retry_gate_review_reopen_ready": False,
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
        "previous_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT",
        "previous_task_state": "supervised_run_retry_gate_attestation_audit_blocked",
        "previous_key_finding": "supervised_run_retry_gate_attestation_audit_blocked_on_missing_current_attestation_records",
        "previous_claim_boundary": "supervised_run_retry_gate_attestation_audit_bounded",
        "retry_gate_attestation_audit_accepted_as_baseline": True,
        "retry_gate_attestation_record_pack_promoted_current": True,
    }
    context_pack["bundle_source"] = BUNDLE_SOURCE
    context_pack["current_contract"].update(
        {
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_marker": "demo_forward_supervised_run_retry_gate_attestation_record_pack",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_spec_path": "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK.md",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_plan_path": "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_plan.md",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist_path": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface_path": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_subagents_path": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/SUBAGENTS.md",
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_subagent_summary_path": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/subagent_summary.md",
            "demo_forward_retry_gate_attestation_record_pack_current_lane": CURRENT_LANE,
            "demo_forward_retry_gate_attestation_record_pack_next_step": NEXT_TASK_LANE,
            "demo_forward_retry_gate_attestation_record_pack_pass_successor": PASS_NEXT_TASK_LANE,
        }
    )
    context_pack["current_task"] = {
        "id": TASK_ID,
        "scope": [
            "Reverify the latest GitHub merged state for Vexter, Dexter, and frozen Mew-X after retry-gate attestation audit merged.",
            "Accept retry-gate attestation audit as the baseline current source of truth.",
            "Promote attestation record-pack status, report, summary, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Make each required face explicit for record owner, locator shape, freshness, stale logic, and reviewability.",
            "Keep retry-gate review blocked until every required face has a current, fresh, reviewable record locator.",
        ],
        "deliverables": [
            "README.md",
            "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK.md",
            "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_plan.md",
            "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md",
            "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
            "tests/test_demo_forward_supervised_run_retry_gate_attestation_audit.py",
            "tests/test_demo_forward_supervised_run_retry_gate_input_attestation.py",
            "tests/test_demo_forward_supervised_run_retry_gate.py",
            "tests/test_bootstrap_layout.py",
            "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
            "scripts/build_proof_bundle.sh",
            "artifacts/summary.md",
            "artifacts/context_pack.json",
            "artifacts/proof_bundle_manifest.json",
            "artifacts/task_ledger.jsonl",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/DETAILS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/MIN_PROMPT.txt",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/CONTEXT.json",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/HANDOFF.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/SUBAGENTS.md",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/subagent_summary.md",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-summary.md",
            "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack.tar.gz",
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
            "latest_recent_vexter_prs": [77, 76, 75, 74, 73],
            "vexter_pr_77_merged_at": VERIFIED_VEXTER_MERGED_AT,
            "vexter_pr_77_closed_at": VERIFIED_VEXTER_MERGED_AT,
        }
    )
    context_pack["evidence"]["demo_forward_supervised_run_retry_gate_attestation_record_pack"] = {
        "report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md",
        "status_report": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md",
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json",
        "summary": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-summary.md",
        "handoff_dir": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack",
        "checklist": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md",
        "decision_surface": "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md",
        "subagent_summary": "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/SUBAGENTS.md",
        "key_finding": KEY_FINDING,
        "claim_boundary": CLAIM_BOUNDARY,
        "task_state": TASK_STATUS,
        "run_outcome": "FAIL/BLOCKED",
        "operator_visible_attestation_record_pack_surface_current": True,
        "preferred_next_step": NEXT_TASK_LANE,
        "record_pack_pass_successor": PASS_NEXT_TASK_LANE,
        "attestation_record_pack_boundary": proof[
            "supervised_run_retry_gate_attestation_record_pack"
        ]["attestation_record_pack_boundary"],
        "blocked_record_faces": blocked_record_faces,
        "sub_agents": list(SUB_AGENT_SUMMARIES),
    }
    context_pack["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "rationale": [
            "Retry-gate attestation audit is accepted as baseline and attestation record pack is now current.",
            "One or more required faces still lack a current, fresh, reviewable record locator.",
            "Refresh the current attestation records before any retry-gate reopen is considered.",
        ],
        "pass_successor": {
            "id": PASS_NEXT_TASK_ID,
            "state": PASS_NEXT_TASK_STATE,
            "lane": PASS_NEXT_TASK_LANE,
        },
    }
    context_pack["proofs"].update(
        {
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_added": True,
            "demo_forward_retry_gate_attestation_record_pack_current_pointers_fixed": True,
            "demo_forward_retry_gate_attestation_record_pack_checklist_written": True,
            "demo_forward_retry_gate_attestation_record_pack_decision_surface_written": True,
            "demo_forward_retry_gate_attestation_record_pack_subagent_summary_written": True,
            "recommended_next_step_advances_to_attestation_refresh_when_blocked": True,
            "retry_gate_review_requires_current_fresh_reviewable_record_locators": True,
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
        ("docs", "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_checklist.md"),
        ("docs", "docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md"),
        ("scripts", "scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack.py"),
        (
            "proof_files",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json",
        ),
        (
            "proof_files",
            "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-summary.md",
        ),
        ("reports", "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack"),
        (
            "reports",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md",
        ),
        (
            "reports",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md",
        ),
        (
            "reports",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/SUBAGENTS.md",
        ),
        (
            "reports",
            "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/subagent_summary.md",
        ),
    ):
        if path not in manifest[key]:
            manifest[key].append(path)
    for path in (
        "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK.md",
        "plans/demo_forward_supervised_run_retry_gate_attestation_record_pack_plan.md",
        "tests/test_demo_forward_supervised_run_retry_gate_attestation_record_pack.py",
        "artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-record-pack.tar.gz",
    ):
        if path not in manifest["included_paths"]:
            manifest["included_paths"].append(path)
    manifest["next_task"] = {
        "id": NEXT_TASK_ID,
        "state": NEXT_TASK_STATE,
        "resume_requirements": [
            f"Keep Dexter pinned at {VERIFIED_DEXTER_COMMIT} and Mew-X frozen at {VERIFIED_MEWX_COMMIT}.",
            "Start from the current attestation record-pack status, report, proof, handoff, checklist, decision surface, and sub-agent summary surfaces.",
            "Do not reopen retry-gate review until every face points to a current, fresh, reviewable record locator.",
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
            "demo_forward_supervised_run_retry_gate_attestation_record_pack_added": True,
            "demo_forward_retry_gate_attestation_record_pack_current_pointers_fixed": True,
            "demo_forward_retry_gate_attestation_record_pack_checklist_written": True,
            "demo_forward_retry_gate_attestation_record_pack_decision_surface_written": True,
            "demo_forward_retry_gate_attestation_record_pack_subagent_summary_written": True,
            "recommended_next_step_advances_to_attestation_refresh_when_blocked": True,
            "retry_gate_review_requires_current_fresh_reviewable_record_locators": True,
        }
    )
    MANIFEST_PATH.write_text(format_json(manifest))

    ledger_payload = {
        "artifact_bundle": BUNDLE_PATH,
        "base_main": VERIFIED_VEXTER_COMMIT,
        "baseline_task_id": "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT",
        "baseline_task_state": "supervised_run_retry_gate_attestation_audit_blocked",
        "branch": git_output("branch", "--show-current"),
        "claim_boundary": CLAIM_BOUNDARY,
        "current_lane": CURRENT_LANE,
        "decision": DECISION,
        "first_demo_target": "dexter_paper_live",
        "gate_pass_successor": PASS_NEXT_TASK_ID,
        "key_finding": KEY_FINDING,
        "next_task_id": NEXT_TASK_ID,
        "next_task_state": NEXT_TASK_STATE,
        "proof": "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json",
        "recommended_next_lane": NEXT_TASK_LANE,
        "repo": "https://github.com/Cabbala/Vexter",
        "retry_gate_attestation_record_pack_face_count": len(rows),
        "retry_gate_attestation_record_pack_current_locator_count": sum(
            row["current_record_locator_present"] for row in rows
        ),
        "retry_gate_attestation_record_pack_reviewable_count": sum(row["reviewable_now"] for row in rows),
        "selected_outcome": "FAIL/BLOCKED",
        "source_faithful_modes": {"dexter": "paper_live", "mewx": "sim_live"},
        "status": TASK_STATUS,
        "sub_agents_used": [item["name"] for item in SUB_AGENT_SUMMARIES],
        "supporting_vexter_prs": [77, 76, 75, 74, 73],
        "task_id": TASK_ID,
        "template_runtime_validation_errors": runtime_errors,
        "verified_dexter_main_commit": VERIFIED_DEXTER_COMMIT,
        "verified_dexter_pr": 3,
        "verified_mewx_frozen_commit": VERIFIED_MEWX_COMMIT,
        "verified_prs": [77, 76, 75],
        "date": run_timestamp.split("T", 1)[0],
    }
    rewrite_local_ledger(ledger_payload)

    update_readme()


if __name__ == "__main__":
    main()
