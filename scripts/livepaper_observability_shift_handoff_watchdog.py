#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


DEXTER_MAIN_COMMIT = "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938"
MEWX_FROZEN_COMMIT = "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"
PROMOTED_BASELINE = "task005-pass-grade-pair-20260325T180027Z"
COMPARISON_SOURCE = "comparison_closed_out"
POLL_FIRST = "poll_first"
MANUAL_LATCHED_STOP_ALL = "manual_latched_stop_all"
SOURCE_FAITHFUL_SEAM = "Dexter `paper_live` / frozen Mew-X `sim_live`"

TEMPLATE_PATH = "docs/livepaper_observability_shift_handoff_template.md"
DRILL_DOC_PATH = "docs/livepaper_observability_shift_handoff_drill.md"
HANDOFF_PATH = "artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/HANDOFF.md"

MONITORED_SURFACES = (
    "current_status",
    "proof_and_report_pointers",
    "omission_drift_partial_visibility",
    "manual_stop_all",
    "quarantine",
    "terminal_snapshot",
    "normalized_failure_detail",
    "open_questions",
    "next_shift_priority_checks",
    "implicit_carryover_guard",
    "completeness_check",
)

SECTION_TO_SURFACE = {
    "Current Status": "current_status",
    "Proof and Report Pointers": "proof_and_report_pointers",
    "Observability Classification": "omission_drift_partial_visibility",
    "Manual Stop-All and Quarantine": "manual_stop_all",
    "Terminal Snapshot": "terminal_snapshot",
    "Normalized Failure Detail": "normalized_failure_detail",
    "Open Questions": "open_questions",
    "Next-Shift Priority Checks": "next_shift_priority_checks",
    "Completeness Check": "completeness_check",
}

REQUIRED_FIELDS = {
    "Current Status": (
        "outgoing_shift_window",
        "incoming_shift_window",
        "task_state",
        "shift_outcome",
        "current_action",
        "active_broken_surface_or_none",
        "recommended_next_step",
        "status_delivery",
        "source_faithful_seam",
        "vexter_main_commit",
        "dexter_main_commit",
        "mewx_frozen_commit",
        "promoted_baseline",
        "comparison_source_of_truth",
        "containment_anchor_plan_id",
        "failure_anchor_plan_id",
    ),
    "Proof and Report Pointers": (
        "current_status_report",
        "current_report",
        "current_proof_summary",
        "current_proof_json",
        "first_deep_proof_to_open_next",
        "shortest_proof_trail",
    ),
    "Observability Classification": (
        "omission_present",
        "omission_summary_or_none",
        "drift_present",
        "drift_summary_or_none",
        "partial_visibility_present",
        "partial_visibility_summary_or_none",
        "exact_broken_surface_or_none",
    ),
    "Manual Stop-All and Quarantine": (
        "manual_stop_all_visible",
        "halt_mode_or_none",
        "trigger_plan_id_or_none",
        "stop_reason_or_none",
        "peer_plan_propagation_confirmed",
        "quarantine_active",
        "quarantine_reason_or_none",
        "continuity_check",
    ),
    "Terminal Snapshot": (
        "terminal_snapshot_present",
        "terminal_snapshot_pointer_or_none",
        "snapshot_signal_visible",
        "terminal_stop_reason_visible",
        "terminal_anchor_native_session_id",
        "terminal_anchor_handle_id",
    ),
    "Normalized Failure Detail": (
        "normalized_failure_detail_present",
        "failure_detail_pointer_or_none",
        "normalized_identity_chain_coherent",
        "source_reason_visible",
        "rollback_snapshot_required_and_present_or_none",
        "failure_code",
        "failure_stage",
        "failure_source_reason",
        "rollback_snapshot_signal",
        "rollback_snapshot_stop_reason",
    ),
    "Open Questions": (
        "question_1_or_none",
        "question_2_or_none",
        "question_3_or_none",
    ),
    "Next-Shift Priority Checks": (
        "priority_check_1",
        "priority_check_2_or_none",
        "priority_check_3_or_none",
    ),
    "Completeness Check": (
        "every_required_face_filled_or_none",
        "status_matches_current_checklist_artifacts",
        "proof_and_report_pointers_checked",
        "omission_drift_partial_visibility_explicit",
        "containment_and_failure_faces_explicit",
        "open_questions_and_next_checks_explicit",
    ),
}

IMPLICIT_CARRYOVER_PHRASES = (
    "same as before",
    "same as prior shift",
    "same as previous shift",
    "same as previous",
    "same as prior",
    "see above",
    "as above",
    "carry over",
    "carry-over",
    "implicit",
    "ditto",
)

BOOLEAN_FIELDS = {
    "manual_stop_all_visible",
    "peer_plan_propagation_confirmed",
    "quarantine_active",
    "terminal_snapshot_present",
    "snapshot_signal_visible",
    "terminal_stop_reason_visible",
    "normalized_failure_detail_present",
    "normalized_identity_chain_coherent",
    "source_reason_visible",
    "omission_present",
    "drift_present",
    "partial_visibility_present",
    "every_required_face_filled_or_none",
    "status_matches_current_checklist_artifacts",
    "proof_and_report_pointers_checked",
    "omission_drift_partial_visibility_explicit",
    "containment_and_failure_faces_explicit",
    "open_questions_and_next_checks_explicit",
}

PATH_FIELDS = {
    "current_status_report",
    "current_report",
    "current_proof_summary",
    "current_proof_json",
    "first_deep_proof_to_open_next",
    "terminal_snapshot_pointer_or_none",
    "failure_detail_pointer_or_none",
}

REQUIRED_TEMPLATE_PHRASES = (
    'Treat the handoff as incomplete if any required face is blank, implied, or replaced by "same as before."',
    "proof/report pointers are present and openable",
    "open questions and next-shift priority checks are explicit, not implied",
)

REQUIRED_DRILL_PHRASES = (
    "Confirm every required handoff face is explicit or marked `none`.",
    "Confirm the sample handoff encodes absence as `false` or `none` instead of leaving fields implied.",
    'No face relies on "same as before" or other unstated carryover.',
)


@dataclass(frozen=True)
class HandoffWatchdogFinding:
    surface: str
    classification: str
    field: str
    detail: str


@dataclass(frozen=True)
class HandoffWatchdogReport:
    passed: bool
    monitored_surfaces: tuple[str, ...]
    surface_status: dict[str, bool]
    findings: tuple[HandoffWatchdogFinding, ...]
    checked_files: dict[str, str]


def _parse_sections(markdown_text: str) -> dict[str, dict[str, str]]:
    sections: dict[str, dict[str, str]] = {}
    current_section: str | None = None
    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            current_section = line[3:].strip()
            sections[current_section] = {}
            continue
        if current_section is None or not line.startswith("- "):
            continue
        field_name, separator, value = line[2:].partition(":")
        if not separator:
            continue
        sections[current_section][field_name.strip()] = value.strip()
    return sections


def _is_hex_commit(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{40}", value))


def evaluate_livepaper_observability_shift_handoff_watchdog(root: Path) -> HandoffWatchdogReport:
    template_path = root / TEMPLATE_PATH
    drill_doc_path = root / DRILL_DOC_PATH
    handoff_path = root / HANDOFF_PATH

    checked_files = {
        "template": TEMPLATE_PATH,
        "drill_doc": DRILL_DOC_PATH,
        "sample_handoff": HANDOFF_PATH,
    }

    findings: list[HandoffWatchdogFinding] = []
    surface_status = {surface: True for surface in MONITORED_SURFACES}

    def fail(surface: str, classification: str, field: str, detail: str) -> None:
        surface_status[surface] = False
        findings.append(
            HandoffWatchdogFinding(
                surface=surface,
                classification=classification,
                field=field,
                detail=detail,
            )
        )

    template_text = template_path.read_text()
    drill_doc_text = drill_doc_path.read_text()
    handoff_text = handoff_path.read_text()
    handoff_sections = _parse_sections(handoff_text)

    for required_phrase in REQUIRED_TEMPLATE_PHRASES:
        if required_phrase not in template_text:
            fail(
                "implicit_carryover_guard",
                "drift",
                "template_phrase",
                f"missing baseline phrase `{required_phrase}` in {TEMPLATE_PATH}",
            )

    for required_phrase in REQUIRED_DRILL_PHRASES:
        if required_phrase not in drill_doc_text:
            fail(
                "implicit_carryover_guard",
                "drift",
                "drill_phrase",
                f"missing baseline phrase `{required_phrase}` in {DRILL_DOC_PATH}",
            )

    for section_name, fields in REQUIRED_FIELDS.items():
        surface = SECTION_TO_SURFACE[section_name]
        section_values = handoff_sections.get(section_name)
        if section_values is None:
            fail(
                surface,
                "omission",
                section_name,
                f"missing `{section_name}` section in {HANDOFF_PATH}",
            )
            continue
        for field_name in fields:
            if field_name not in section_values:
                fail(
                    surface,
                    "omission",
                    field_name,
                    f"missing `{field_name}` in `{section_name}`",
                )
                continue
            if not section_values[field_name]:
                fail(
                    surface,
                    "omission",
                    field_name,
                    f"`{field_name}` is blank in `{section_name}`",
                )

    for section_values in handoff_sections.values():
        for field_name, value in section_values.items():
            lowered_value = value.lower()
            for phrase in IMPLICIT_CARRYOVER_PHRASES:
                if phrase in lowered_value:
                    fail(
                        "implicit_carryover_guard",
                        "drift",
                        field_name,
                        f"`{field_name}` uses forbidden carry-over phrase `{phrase}`",
                    )
            if field_name in BOOLEAN_FIELDS and value not in {"true", "false"}:
                fail(
                    SECTION_TO_SURFACE.get(
                        next(
                            (
                                section_name
                                for section_name, fields in REQUIRED_FIELDS.items()
                                if field_name in fields
                            ),
                            "Open Questions",
                        ),
                        "implicit_carryover_guard",
                    ),
                    "drift",
                    field_name,
                    f"`{field_name}` must be `true` or `false`, found `{value}`",
                )

    current_status = handoff_sections.get("Current Status", {})
    if current_status:
        if current_status.get("status_delivery") != POLL_FIRST:
            fail(
                "current_status",
                "drift",
                "status_delivery",
                f"expected `{POLL_FIRST}`",
            )
        if current_status.get("source_faithful_seam") != SOURCE_FAITHFUL_SEAM:
            fail(
                "current_status",
                "drift",
                "source_faithful_seam",
                f"expected `{SOURCE_FAITHFUL_SEAM}`",
            )
        if current_status.get("dexter_main_commit") != DEXTER_MAIN_COMMIT:
            fail(
                "current_status",
                "drift",
                "dexter_main_commit",
                f"expected pinned Dexter commit `{DEXTER_MAIN_COMMIT}`",
            )
        if current_status.get("mewx_frozen_commit") != MEWX_FROZEN_COMMIT:
            fail(
                "current_status",
                "drift",
                "mewx_frozen_commit",
                f"expected frozen Mew-X commit `{MEWX_FROZEN_COMMIT}`",
            )
        if current_status.get("promoted_baseline") != PROMOTED_BASELINE:
            fail(
                "current_status",
                "drift",
                "promoted_baseline",
                f"expected promoted baseline `{PROMOTED_BASELINE}`",
            )
        if current_status.get("comparison_source_of_truth") != COMPARISON_SOURCE:
            fail(
                "current_status",
                "drift",
                "comparison_source_of_truth",
                f"expected comparison source `{COMPARISON_SOURCE}`",
            )
        vexter_main_commit = current_status.get("vexter_main_commit")
        if vexter_main_commit and not _is_hex_commit(vexter_main_commit):
            fail(
                "current_status",
                "drift",
                "vexter_main_commit",
                "expected a 40-character git commit",
            )

    proof_and_report = handoff_sections.get("Proof and Report Pointers", {})
    if proof_and_report:
        pointer_values = []
        for field_name in REQUIRED_FIELDS["Proof and Report Pointers"]:
            value = proof_and_report.get(field_name)
            if not value:
                continue
            if field_name == "shortest_proof_trail":
                if "status" not in value or "proof" not in value or "sample handoff" not in value:
                    fail(
                        "proof_and_report_pointers",
                        "drift",
                        field_name,
                        "proof trail lost the bounded status/report/summary/proof/handoff order",
                    )
                continue
            pointer_values.append(value)
            if value == "none":
                fail(
                    "proof_and_report_pointers",
                    "partial_visibility",
                    field_name,
                    f"`{field_name}` may not collapse to `none`",
                )
                continue
            pointed_path = root / value
            if not pointed_path.exists():
                fail(
                    "proof_and_report_pointers",
                    "partial_visibility",
                    field_name,
                    f"`{field_name}` points to missing path `{value}`",
                )
        if len(pointer_values) != len(set(pointer_values)):
            fail(
                "proof_and_report_pointers",
                "drift",
                "proof_pointer_set",
                "proof/report pointer set became ambiguous because at least two pointers collapsed to the same path",
            )

    classification = handoff_sections.get("Observability Classification", {})
    if classification:
        triage_fields = (
            ("omission_present", "omission_summary_or_none"),
            ("drift_present", "drift_summary_or_none"),
            ("partial_visibility_present", "partial_visibility_summary_or_none"),
        )
        any_visible_break = False
        for present_field, summary_field in triage_fields:
            present_value = classification.get(present_field)
            summary_value = classification.get(summary_field)
            if present_value == "true":
                any_visible_break = True
                if summary_value == "none":
                    fail(
                        "omission_drift_partial_visibility",
                        "partial_visibility",
                        summary_field,
                        f"`{summary_field}` must not be `none` when `{present_field}` is `true`",
                    )
            if present_value == "false" and summary_value not in {None, "none"}:
                fail(
                    "omission_drift_partial_visibility",
                    "drift",
                    summary_field,
                    f"`{summary_field}` must be `none` when `{present_field}` is `false`",
                )
        exact_broken_surface = classification.get("exact_broken_surface_or_none")
        if any_visible_break and exact_broken_surface == "none":
            fail(
                "omission_drift_partial_visibility",
                "partial_visibility",
                "exact_broken_surface_or_none",
                "an explicit broken surface is required when omission/drift/partial_visibility is present",
            )
        if not any_visible_break and exact_broken_surface not in {None, "none"}:
            fail(
                "omission_drift_partial_visibility",
                "drift",
                "exact_broken_surface_or_none",
                "broken surface must collapse to `none` when no observability break is present",
            )

    containment = handoff_sections.get("Manual Stop-All and Quarantine", {})
    if containment:
        if containment.get("manual_stop_all_visible") == "true":
            if containment.get("halt_mode_or_none") != MANUAL_LATCHED_STOP_ALL:
                fail(
                    "manual_stop_all",
                    "drift",
                    "halt_mode_or_none",
                    f"manual stop-all must keep `{MANUAL_LATCHED_STOP_ALL}` visible",
                )
            if containment.get("stop_reason_or_none") != MANUAL_LATCHED_STOP_ALL:
                fail(
                    "manual_stop_all",
                    "partial_visibility",
                    "stop_reason_or_none",
                    f"manual stop-all must keep `{MANUAL_LATCHED_STOP_ALL}` visible",
                )
            if containment.get("trigger_plan_id_or_none") == "none":
                fail(
                    "manual_stop_all",
                    "partial_visibility",
                    "trigger_plan_id_or_none",
                    "manual stop-all trigger plan may not collapse to `none` while visible",
                )
        if containment.get("quarantine_active") == "true" and containment.get("quarantine_reason_or_none") == "none":
            fail(
                "quarantine",
                "partial_visibility",
                "quarantine_reason_or_none",
                "quarantine reason may not collapse to `none` while quarantine is active",
            )
        continuity_check = containment.get("continuity_check", "")
        for required_fragment in (
            "monitor_profile_id=",
            "quarantine_scope=",
            "execution_mode=",
            "ack_history_visible=",
        ):
            if required_fragment not in continuity_check:
                fail(
                    "quarantine",
                    "partial_visibility",
                    "continuity_check",
                    f"continuity check lost `{required_fragment}`",
                )

    terminal_snapshot = handoff_sections.get("Terminal Snapshot", {})
    if terminal_snapshot:
        if terminal_snapshot.get("terminal_snapshot_present") == "true":
            pointer_value = terminal_snapshot.get("terminal_snapshot_pointer_or_none")
            if pointer_value == "none":
                fail(
                    "terminal_snapshot",
                    "partial_visibility",
                    "terminal_snapshot_pointer_or_none",
                    "terminal snapshot pointer may not collapse to `none` while present",
                )
            elif pointer_value and not (root / pointer_value).exists():
                fail(
                    "terminal_snapshot",
                    "partial_visibility",
                    "terminal_snapshot_pointer_or_none",
                    f"terminal snapshot pointer `{pointer_value}` is missing",
                )
            for field_name in ("terminal_anchor_native_session_id", "terminal_anchor_handle_id"):
                if terminal_snapshot.get(field_name) == "none":
                    fail(
                        "terminal_snapshot",
                        "partial_visibility",
                        field_name,
                        f"`{field_name}` may not collapse to `none` while terminal snapshot is present",
                    )

    failure_detail = handoff_sections.get("Normalized Failure Detail", {})
    if failure_detail:
        if failure_detail.get("normalized_failure_detail_present") == "true":
            pointer_value = failure_detail.get("failure_detail_pointer_or_none")
            if pointer_value == "none":
                fail(
                    "normalized_failure_detail",
                    "partial_visibility",
                    "failure_detail_pointer_or_none",
                    "failure detail pointer may not collapse to `none` while normalized failure detail is present",
                )
            elif pointer_value and not (root / pointer_value).exists():
                fail(
                    "normalized_failure_detail",
                    "partial_visibility",
                    "failure_detail_pointer_or_none",
                    f"failure detail pointer `{pointer_value}` is missing",
                )
            if failure_detail.get("rollback_snapshot_required_and_present_or_none") not in {"present", "none"}:
                fail(
                    "normalized_failure_detail",
                    "drift",
                    "rollback_snapshot_required_and_present_or_none",
                    "rollback snapshot field must stay explicit as `present` or `none`",
                )
            for field_name in (
                "failure_code",
                "failure_stage",
                "failure_source_reason",
                "rollback_snapshot_signal",
                "rollback_snapshot_stop_reason",
            ):
                if failure_detail.get(field_name) == "none":
                    fail(
                        "normalized_failure_detail",
                        "partial_visibility",
                        field_name,
                        f"`{field_name}` may not collapse to `none` while normalized failure detail is present",
                    )

    for surface_name, section_name in (
        ("open_questions", "Open Questions"),
        ("next_shift_priority_checks", "Next-Shift Priority Checks"),
        ("completeness_check", "Completeness Check"),
    ):
        section_values = handoff_sections.get(section_name, {})
        for field_name in REQUIRED_FIELDS[section_name]:
            if field_name in section_values and not section_values[field_name]:
                fail(
                    surface_name,
                    "omission",
                    field_name,
                    f"`{field_name}` must stay explicit in `{section_name}`",
                )

    completeness = handoff_sections.get("Completeness Check", {})
    if completeness:
        for field_name in REQUIRED_FIELDS["Completeness Check"]:
            if completeness.get(field_name) != "true":
                fail(
                    "completeness_check",
                    "drift",
                    field_name,
                    f"`{field_name}` must stay `true` on the fixed sample handoff",
                )

    return HandoffWatchdogReport(
        passed=all(surface_status.values()),
        monitored_surfaces=MONITORED_SURFACES,
        surface_status=surface_status,
        findings=tuple(findings),
        checked_files=checked_files,
    )


def _serialize_report(report: HandoffWatchdogReport) -> dict[str, object]:
    return {
        "passed": report.passed,
        "monitored_surfaces": list(report.monitored_surfaces),
        "surface_status": report.surface_status,
        "findings": [asdict(finding) for finding in report.findings],
        "checked_files": report.checked_files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--json-output")
    args = parser.parse_args()

    report = evaluate_livepaper_observability_shift_handoff_watchdog(Path(args.root).resolve())
    serialized = _serialize_report(report)

    if args.json_output:
        Path(args.json_output).write_text(json.dumps(serialized, indent=2) + "\n")
    else:
        print(json.dumps(serialized, indent=2))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
