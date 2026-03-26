"""Bounded watchdog helpers for live-paper observability shift handoffs."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES = (
    "current_status",
    "proof_and_report_pointers",
    "omission_drift_partial_visibility",
    "manual_stop_all",
    "quarantine",
    "terminal_snapshot",
    "normalized_failure_detail",
    "open_questions",
    "next_shift_priority_checks",
)
MONITORED_SURFACES = LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES
HANDOFF_PATH = Path("artifacts/reports/task-007-livepaper-observability-shift-handoff-drill/HANDOFF.md")

_IMPLICIT_VALUE_MARKERS = (
    "same as before",
    "same-as-before",
    "unchanged",
    "carry over",
    "carry-over",
    "see above",
    "as above",
    "ditto",
    "tbd",
    "todo",
)
_BOOLEAN_VALUES = frozenset({"true", "false"})
_PATH_LIKE_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+$")
_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True, slots=True)
class LivepaperShiftHandoffWatchdogFinding:
    surface: str
    severity: str
    message: str
    field_name: str | None = None
    detail: Mapping[str, Any] = field(default_factory=dict)

    @property
    def classification(self) -> str:
        return self.severity


@dataclass(frozen=True, slots=True)
class LivepaperShiftHandoffWatchdogReport:
    findings: tuple[LivepaperShiftHandoffWatchdogFinding, ...]

    @property
    def passed(self) -> bool:
        return not self.findings

    @property
    def surface_status(self) -> Mapping[str, bool]:
        surfaced = {finding.surface for finding in self.findings}
        return {
            surface: surface not in surfaced for surface in LIVEPAPER_SHIFT_HANDOFF_WATCHDOG_SURFACES
        }


def evaluate_livepaper_observability_shift_handoff_watchdog(
    markdown: str,
    *,
    repo_root: str | Path | None = None,
) -> LivepaperShiftHandoffWatchdogReport:
    """Evaluate one handoff markdown body against the bounded shift handoff surface."""

    repo_path = Path(repo_root) if repo_root is not None else None
    sections = _parse_handoff_sections(markdown)
    findings: list[LivepaperShiftHandoffWatchdogFinding] = []

    _check_current_status(sections, findings)
    _check_proof_and_report_pointers(sections, findings, repo_root=repo_path)
    _check_observability_classification(sections, findings)
    _check_manual_stop_all(sections, findings)
    _check_quarantine(sections, findings)
    _check_terminal_snapshot(sections, findings, repo_root=repo_path)
    _check_normalized_failure_detail(sections, findings, repo_root=repo_path)
    _check_open_questions(sections, findings)
    _check_next_shift_priority_checks(sections, findings)

    return LivepaperShiftHandoffWatchdogReport(findings=tuple(findings))


def _parse_handoff_sections(markdown: str) -> dict[str, dict[str, list[str]]]:
    sections: dict[str, dict[str, list[str]]] = {}
    current_section: str | None = None
    in_code_block = False

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if line.startswith("## "):
            current_section = line[3:].strip()
            sections.setdefault(current_section, {})
            continue
        if current_section is None or not stripped.startswith("- "):
            continue
        content = stripped[2:]
        if ":" not in content:
            continue
        field_name, value = content.split(":", 1)
        sections[current_section].setdefault(field_name.strip(), []).append(value.strip())

    return sections


def _issue(
    findings: list[LivepaperShiftHandoffWatchdogFinding],
    surface: str,
    severity: str,
    message: str,
    *,
    field_name: str | None = None,
    detail: Mapping[str, Any] | None = None,
) -> None:
    findings.append(
        LivepaperShiftHandoffWatchdogFinding(
            surface=surface,
            severity=severity,
            message=message,
            field_name=field_name,
            detail=detail or {},
        )
    )


def _read_face_fields(
    sections: Mapping[str, Mapping[str, list[str]]],
    surface: str,
    section_name: str,
    required_fields: tuple[str, ...],
    findings: list[LivepaperShiftHandoffWatchdogFinding],
) -> dict[str, str]:
    section = sections.get(section_name)
    if section is None:
        _issue(
            findings,
            surface,
            "omission",
            "handoff section is missing",
            detail={"missing_section": section_name},
        )
        return {}

    values: dict[str, str] = {}
    for field_name in required_fields:
        entries = list(section.get(field_name, ()))
        if not entries:
            _issue(
                findings,
                surface,
                "omission",
                "required handoff field is missing",
                field_name=field_name,
                detail={"section": section_name},
            )
            continue
        if len(entries) > 1:
            _issue(
                findings,
                surface,
                "partial_visibility",
                "handoff field became ambiguous",
                field_name=field_name,
                detail={"section": section_name, "observed_values": entries},
            )
        value = entries[-1].strip()
        if not value:
            _issue(
                findings,
                surface,
                "omission",
                "handoff field is blank",
                field_name=field_name,
                detail={"section": section_name},
            )
            continue
        values[field_name] = value
    return values


def _is_implicit(value: str) -> bool:
    normalized = value.strip().lower()
    if not normalized:
        return True
    return any(marker in normalized for marker in _IMPLICIT_VALUE_MARKERS)


def _is_explicit_bool(value: str) -> bool:
    return value.strip().lower() in _BOOLEAN_VALUES


def _is_none(value: str) -> bool:
    return value.strip().lower() == "none"


def _is_commit(value: str) -> bool:
    return bool(_COMMIT_PATTERN.fullmatch(value.strip().lower()))


def _is_path_like(value: str) -> bool:
    return bool(_PATH_LIKE_PATTERN.fullmatch(value.strip()))


def _check_no_implicit(
    findings: list[LivepaperShiftHandoffWatchdogFinding],
    surface: str,
    values: Mapping[str, str],
    field_names: tuple[str, ...],
) -> None:
    for field_name in field_names:
        value = values.get(field_name)
        if value is None or _is_none(value):
            continue
        if _is_implicit(value):
            _issue(
                findings,
                surface,
                "partial_visibility",
                "handoff field relies on implicit carry-over instead of explicit content",
                field_name=field_name,
            )


def _check_current_status(
    sections: Mapping[str, Mapping[str, list[str]]],
    findings: list[LivepaperShiftHandoffWatchdogFinding],
) -> None:
    surface = "current_status"
    values = _read_face_fields(
        sections,
        surface,
        "Current Status",
        (
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
        ),
        findings,
    )
    _check_no_implicit(
        findings,
        surface,
        values,
        (
            "outgoing_shift_window",
            "incoming_shift_window",
            "task_state",
            "shift_outcome",
            "current_action",
            "active_broken_surface_or_none",
            "recommended_next_step",
            "promoted_baseline",
        ),
    )

    if values.get("shift_outcome") not in {"contained", "escalated", "closed"}:
        _issue(
            findings,
            surface,
            "drift",
            "shift outcome drifted away from the fixed handoff vocabulary",
            field_name="shift_outcome",
        )
    if values.get("current_action") not in {"halt", "quarantine", "continue"}:
        _issue(
            findings,
            surface,
            "drift",
            "current action drifted away from the fixed handoff vocabulary",
            field_name="current_action",
        )
    if values.get("status_delivery") != "poll_first":
        _issue(
            findings,
            surface,
            "drift",
            "status delivery drifted away from the fixed poll_first contract",
            field_name="status_delivery",
        )
    seam = values.get("source_faithful_seam", "")
    if "paper_live" not in seam or "sim_live" not in seam:
        _issue(
            findings,
            surface,
            "drift",
            "source-faithful seam is no longer explicit",
            field_name="source_faithful_seam",
        )
    for field_name in ("vexter_main_commit", "dexter_main_commit", "mewx_frozen_commit"):
        value = values.get(field_name)
        if value is not None and not _is_commit(value):
            _issue(
                findings,
                surface,
                "drift",
                "commit pin is no longer explicit and hash-shaped",
                field_name=field_name,
            )
    if values.get("comparison_source_of_truth") != "comparison_closed_out":
        _issue(
            findings,
            surface,
            "drift",
            "comparison source of truth drifted away from the fixed closed-out baseline",
            field_name="comparison_source_of_truth",
        )
    if values.get("promoted_baseline") != "task005-pass-grade-pair-20260325T180027Z":
        _issue(
            findings,
            surface,
            "drift",
            "promoted baseline drifted away from the fixed pass-grade pair",
            field_name="promoted_baseline",
        )
    if values.get("dexter_main_commit") != "ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938":
        _issue(
            findings,
            surface,
            "drift",
            "Dexter pin drifted away from the fixed merged PR #3 commit",
            field_name="dexter_main_commit",
        )
    if values.get("mewx_frozen_commit") != "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a":
        _issue(
            findings,
            surface,
            "drift",
            "Mew-X frozen pin drifted away from the fixed commit",
            field_name="mewx_frozen_commit",
        )


def _check_proof_and_report_pointers(
    sections: Mapping[str, Mapping[str, list[str]]],
    findings: list[LivepaperShiftHandoffWatchdogFinding],
    *,
    repo_root: Path | None,
) -> None:
    surface = "proof_and_report_pointers"
    pointer_fields = (
        "current_status_report",
        "current_report",
        "current_proof_summary",
        "current_proof_json",
        "first_deep_proof_to_open_next",
    )
    values = _read_face_fields(
        sections,
        surface,
        "Proof and Report Pointers",
        pointer_fields + ("shortest_proof_trail",),
        findings,
    )
    _check_no_implicit(findings, surface, values, ("shortest_proof_trail",))

    observed_paths: list[str] = []
    for field_name in pointer_fields:
        value = values.get(field_name)
        if value is None:
            continue
        if _is_implicit(value) or _is_none(value):
            _issue(
                findings,
                surface,
                "partial_visibility",
                "pointer field is implicit or collapsed to none",
                field_name=field_name,
            )
            continue
        if not _is_path_like(value):
            _issue(
                findings,
                surface,
                "partial_visibility",
                "pointer field is no longer path-like and openable",
                field_name=field_name,
            )
            continue
        observed_paths.append(value)
        if repo_root is not None and not (repo_root / value).exists():
            _issue(
                findings,
                surface,
                "partial_visibility",
                "pointer field no longer resolves to an existing repo path",
                field_name=field_name,
                detail={"path": value},
            )
    if observed_paths and len(set(observed_paths)) != len(observed_paths):
        _issue(
            findings,
            surface,
            "partial_visibility",
            "pointer set shrank into ambiguous duplicate paths",
            detail={"observed_paths": observed_paths},
        )

    trail = values.get("shortest_proof_trail")
    if trail is not None and ("->" not in trail or _is_none(trail) or _is_implicit(trail)):
        _issue(
            findings,
            surface,
            "partial_visibility",
            "shortest proof trail is no longer explicit",
            field_name="shortest_proof_trail",
        )
    if values.get("first_deep_proof_to_open_next") != (
        "artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json"
    ):
        _issue(
            findings,
            surface,
            "drift",
            "first deep proof drifted away from the fixed watchdog CI-gate entry point",
            field_name="first_deep_proof_to_open_next",
        )


def _check_observability_classification(
    sections: Mapping[str, Mapping[str, list[str]]],
    findings: list[LivepaperShiftHandoffWatchdogFinding],
) -> None:
    surface = "omission_drift_partial_visibility"
    values = _read_face_fields(
        sections,
        surface,
        "Observability Classification",
        (
            "omission_present",
            "omission_summary_or_none",
            "drift_present",
            "drift_summary_or_none",
            "partial_visibility_present",
            "partial_visibility_summary_or_none",
            "exact_broken_surface_or_none",
        ),
        findings,
    )
    for field_name in ("omission_present", "drift_present", "partial_visibility_present"):
        value = values.get(field_name)
        if value is not None and not _is_explicit_bool(value):
            _issue(
                findings,
                surface,
                "drift",
                "classification boolean is no longer explicit true/false",
                field_name=field_name,
            )
    pairs = (
        ("omission_present", "omission_summary_or_none"),
        ("drift_present", "drift_summary_or_none"),
        ("partial_visibility_present", "partial_visibility_summary_or_none"),
    )
    any_present = False
    for bool_field, summary_field in pairs:
        bool_value = values.get(bool_field, "").lower()
        summary_value = values.get(summary_field)
        if bool_value == "true":
            any_present = True
            if summary_value is None or _is_none(summary_value) or _is_implicit(summary_value):
                _issue(
                    findings,
                    surface,
                    "partial_visibility",
                    "classification summary disappeared while the incident stayed visible",
                    field_name=summary_field,
                )
        elif bool_value == "false" and summary_value is not None and not _is_none(summary_value):
            _issue(
                findings,
                surface,
                "drift",
                "classification summary drifted away from explicit none while the flag is false",
                field_name=summary_field,
            )
    broken_surface = values.get("exact_broken_surface_or_none")
    if any_present and (broken_surface is None or _is_none(broken_surface) or _is_implicit(broken_surface)):
        _issue(
            findings,
            surface,
            "partial_visibility",
            "exact broken surface disappeared while a classification stayed true",
            field_name="exact_broken_surface_or_none",
        )
    if not any_present and broken_surface is not None and not _is_none(broken_surface):
        _issue(
            findings,
            surface,
            "drift",
            "exact broken surface drifted away from none while all classifications are false",
            field_name="exact_broken_surface_or_none",
        )


def _check_manual_stop_all(
    sections: Mapping[str, Mapping[str, list[str]]],
    findings: list[LivepaperShiftHandoffWatchdogFinding],
) -> None:
    surface = "manual_stop_all"
    values = _read_face_fields(
        sections,
        surface,
        "Manual Stop-All and Quarantine",
        (
            "manual_stop_all_visible",
            "halt_mode_or_none",
            "trigger_plan_id_or_none",
            "stop_reason_or_none",
            "peer_plan_propagation_confirmed",
        ),
        findings,
    )
    for field_name in ("manual_stop_all_visible", "peer_plan_propagation_confirmed"):
        value = values.get(field_name)
        if value is not None and not _is_explicit_bool(value):
            _issue(
                findings,
                surface,
                "drift",
                "manual stop-all boolean is no longer explicit true/false",
                field_name=field_name,
            )

    visible = values.get("manual_stop_all_visible", "").lower() == "true"
    if visible:
        if values.get("halt_mode_or_none") != "manual_latched_stop_all":
            _issue(
                findings,
                surface,
                "partial_visibility",
                "halt mode is missing or no longer source-faithful while stop-all is visible",
                field_name="halt_mode_or_none",
            )
        for field_name in ("trigger_plan_id_or_none", "stop_reason_or_none"):
            value = values.get(field_name)
            if value is None or _is_none(value) or _is_implicit(value):
                _issue(
                    findings,
                    surface,
                    "partial_visibility",
                    "manual stop-all detail disappeared while the stop-all face stayed visible",
                    field_name=field_name,
                )
    else:
        for field_name in ("halt_mode_or_none", "trigger_plan_id_or_none", "stop_reason_or_none"):
            value = values.get(field_name)
            if value is not None and not _is_none(value):
                _issue(
                    findings,
                    surface,
                    "drift",
                    "manual stop-all detail drifted away from explicit none while stop-all is false",
                    field_name=field_name,
                )


def _check_quarantine(
    sections: Mapping[str, Mapping[str, list[str]]],
    findings: list[LivepaperShiftHandoffWatchdogFinding],
) -> None:
    surface = "quarantine"
    values = _read_face_fields(
        sections,
        surface,
        "Manual Stop-All and Quarantine",
        (
            "quarantine_active",
            "quarantine_reason_or_none",
            "continuity_check",
        ),
        findings,
    )
    active = values.get("quarantine_active", "").lower()
    if active and not _is_explicit_bool(active):
        _issue(
            findings,
            surface,
            "drift",
            "quarantine_active is no longer explicit true/false",
            field_name="quarantine_active",
        )
    if active == "true":
        reason = values.get("quarantine_reason_or_none")
        if reason is None or _is_none(reason) or _is_implicit(reason):
            _issue(
                findings,
                surface,
                "partial_visibility",
                "quarantine reason disappeared while quarantine stayed visible",
                field_name="quarantine_reason_or_none",
            )
        continuity = values.get("continuity_check")
        if continuity is None or _is_none(continuity) or _is_implicit(continuity):
            _issue(
                findings,
                surface,
                "partial_visibility",
                "continuity check became implicit while quarantine stayed visible",
                field_name="continuity_check",
            )
    elif active == "false":
        reason = values.get("quarantine_reason_or_none")
        if reason is not None and not _is_none(reason):
            _issue(
                findings,
                surface,
                "drift",
                "quarantine reason drifted away from explicit none while quarantine is false",
                field_name="quarantine_reason_or_none",
            )


def _check_terminal_snapshot(
    sections: Mapping[str, Mapping[str, list[str]]],
    findings: list[LivepaperShiftHandoffWatchdogFinding],
    *,
    repo_root: Path | None,
) -> None:
    surface = "terminal_snapshot"
    values = _read_face_fields(
        sections,
        surface,
        "Terminal Snapshot",
        (
            "terminal_snapshot_present",
            "terminal_snapshot_pointer_or_none",
            "snapshot_signal_visible",
            "terminal_stop_reason_visible",
        ),
        findings,
    )
    present = values.get("terminal_snapshot_present", "").lower()
    for field_name in ("terminal_snapshot_present", "snapshot_signal_visible", "terminal_stop_reason_visible"):
        value = values.get(field_name)
        if value is not None and not _is_explicit_bool(value):
            _issue(
                findings,
                surface,
                "drift",
                "terminal snapshot boolean is no longer explicit true/false",
                field_name=field_name,
            )
    pointer = values.get("terminal_snapshot_pointer_or_none")
    if present == "true":
        if pointer is None or _is_none(pointer) or _is_implicit(pointer) or not _is_path_like(pointer):
            _issue(
                findings,
                surface,
                "partial_visibility",
                "terminal snapshot pointer degraded while the terminal snapshot face stayed visible",
                field_name="terminal_snapshot_pointer_or_none",
            )
        elif repo_root is not None and not (repo_root / pointer).exists():
            _issue(
                findings,
                surface,
                "partial_visibility",
                "terminal snapshot pointer no longer resolves inside the repo",
                field_name="terminal_snapshot_pointer_or_none",
                detail={"path": pointer},
            )
    elif present == "false" and pointer is not None and not _is_none(pointer):
        _issue(
            findings,
            surface,
            "drift",
            "terminal snapshot pointer drifted away from explicit none while the face is false",
            field_name="terminal_snapshot_pointer_or_none",
        )


def _check_normalized_failure_detail(
    sections: Mapping[str, Mapping[str, list[str]]],
    findings: list[LivepaperShiftHandoffWatchdogFinding],
    *,
    repo_root: Path | None,
) -> None:
    surface = "normalized_failure_detail"
    values = _read_face_fields(
        sections,
        surface,
        "Normalized Failure Detail",
        (
            "normalized_failure_detail_present",
            "failure_detail_pointer_or_none",
            "normalized_identity_chain_coherent",
            "source_reason_visible",
            "rollback_snapshot_required_and_present_or_none",
        ),
        findings,
    )
    present = values.get("normalized_failure_detail_present", "").lower()
    for field_name in (
        "normalized_failure_detail_present",
        "normalized_identity_chain_coherent",
        "source_reason_visible",
    ):
        value = values.get(field_name)
        if value is not None and not _is_explicit_bool(value):
            _issue(
                findings,
                surface,
                "drift",
                "normalized failure detail boolean is no longer explicit true/false",
                field_name=field_name,
            )
    pointer = values.get("failure_detail_pointer_or_none")
    rollback = values.get("rollback_snapshot_required_and_present_or_none")
    if present == "true":
        if pointer is None or _is_none(pointer) or _is_implicit(pointer) or not _is_path_like(pointer):
            _issue(
                findings,
                surface,
                "partial_visibility",
                "failure-detail pointer degraded while normalized failure detail stayed visible",
                field_name="failure_detail_pointer_or_none",
            )
        elif repo_root is not None and not (repo_root / pointer).exists():
            _issue(
                findings,
                surface,
                "partial_visibility",
                "failure-detail pointer no longer resolves inside the repo",
                field_name="failure_detail_pointer_or_none",
                detail={"path": pointer},
            )
        if rollback is None or _is_implicit(rollback):
            _issue(
                findings,
                surface,
                "partial_visibility",
                "rollback snapshot state became implicit while normalized failure detail stayed visible",
                field_name="rollback_snapshot_required_and_present_or_none",
            )
    elif present == "false":
        if pointer is not None and not _is_none(pointer):
            _issue(
                findings,
                surface,
                "drift",
                "failure-detail pointer drifted away from explicit none while the face is false",
                field_name="failure_detail_pointer_or_none",
            )
        if rollback is not None and not _is_none(rollback):
            _issue(
                findings,
                surface,
                "drift",
                "rollback snapshot state drifted away from explicit none while the face is false",
                field_name="rollback_snapshot_required_and_present_or_none",
            )


def _check_open_questions(
    sections: Mapping[str, Mapping[str, list[str]]],
    findings: list[LivepaperShiftHandoffWatchdogFinding],
) -> None:
    surface = "open_questions"
    values = _read_face_fields(
        sections,
        surface,
        "Open Questions",
        (
            "question_1_or_none",
            "question_2_or_none",
            "question_3_or_none",
        ),
        findings,
    )
    for field_name in ("question_1_or_none", "question_2_or_none", "question_3_or_none"):
        value = values.get(field_name)
        if value is not None and _is_implicit(value):
            _issue(
                findings,
                surface,
                "partial_visibility",
                "open question field became implicit instead of explicit or none",
                field_name=field_name,
            )


def _check_next_shift_priority_checks(
    sections: Mapping[str, Mapping[str, list[str]]],
    findings: list[LivepaperShiftHandoffWatchdogFinding],
) -> None:
    surface = "next_shift_priority_checks"
    values = _read_face_fields(
        sections,
        surface,
        "Next-Shift Priority Checks",
        (
            "priority_check_1",
            "priority_check_2_or_none",
            "priority_check_3_or_none",
        ),
        findings,
    )
    required_explicit = ("priority_check_1", "priority_check_2_or_none", "priority_check_3_or_none")
    for field_name in required_explicit:
        value = values.get(field_name)
        if value is None:
            continue
        if field_name == "priority_check_1" and _is_none(value):
            _issue(
                findings,
                surface,
                "omission",
                "first priority check disappeared",
                field_name=field_name,
            )
            continue
        if _is_implicit(value):
            _issue(
                findings,
                surface,
                "partial_visibility",
                "next-shift priority check became implicit",
                field_name=field_name,
            )
