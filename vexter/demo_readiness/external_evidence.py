"""Canonical outside-repo evidence contract and gap analysis helpers."""

from __future__ import annotations

from collections import Counter
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MANIFEST_KIND = "demo_forward_supervised_run_retry_gate_external_evidence_manifest"
SCHEMA_VERSION = 1
TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-EXTERNAL-EVIDENCE-GAP"
PREFLIGHT_TASK_ID = "DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-EVIDENCE-PREFLIGHT"

MANIFEST_REL_PATH = "manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json"
CONTRACT_SPEC_REL_PATH = "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_EXTERNAL_EVIDENCE_CONTRACT.md"
GAP_PROOF_REL_PATH = "artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-check.json"
GAP_REPORT_REL_PATH = "artifacts/reports/demo-forward-supervised-run-retry-gate-external-evidence-gap-report.md"
GAP_SUMMARY_REL_PATH = "artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-summary.md"
PREFLIGHT_PROOF_REL_PATH = (
    "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json"
)
PREFLIGHT_REPORT_REL_PATH = (
    "artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md"
)
PREFLIGHT_SUMMARY_REL_PATH = (
    "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-summary.md"
)
PREFLIGHT_COMMAND = "python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py"
LEGACY_GAP_COMMAND = (
    "python3.12 scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py"
)

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

TOP_LEVEL_KEYS = {
    "manifest_kind",
    "schema_version",
    "manifest_role",
    "updated_at",
    "bounded_supervised_window",
    "notes",
    "faces",
}
WINDOW_KEYS = {"label", "starts_at", "ends_at"}
FACE_KEYS = {
    "provided",
    "attested_by",
    "evidence_locator",
    "locator_kind",
    "verified_at",
    "fresh_until",
    "reviewable_without_secrets",
    "reviewability_note",
    "summary",
    "marker_match_note",
    "operator_input_remaining",
}
WINDOW_FIELD_PATHS = [
    "bounded_supervised_window.label",
    "bounded_supervised_window.starts_at",
    "bounded_supervised_window.ends_at",
]
FACE_FILL_FIELD_NAMES = [
    "provided",
    "attested_by",
    "evidence_locator",
    "locator_kind",
    "verified_at",
    "fresh_until",
    "reviewable_without_secrets",
    "reviewability_note",
]
PROOF_PATHS_TO_RECHECK = [
    PREFLIGHT_PROOF_REL_PATH,
    PREFLIGHT_REPORT_REL_PATH,
    PREFLIGHT_SUMMARY_REL_PATH,
    GAP_PROOF_REL_PATH,
    GAP_REPORT_REL_PATH,
    GAP_SUMMARY_REL_PATH,
    "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json",
    "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md",
    "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json",
    "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md",
]
RERUN_COMMANDS = [
    PREFLIGHT_COMMAND,
    "python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py",
    "python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py",
]
BLOCKED_REASON_GROUP_ORDER = ("state", "missing", "stale", "malformed", "other")


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _normalize_string(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def _format_marker(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)


def _format_bool(value: bool) -> str:
    return "yes" if value else "no"


def _required_manifest_fields_for_face(name: str) -> list[str]:
    return WINDOW_FIELD_PATHS + [f"faces.{name}.{field_name}" for field_name in FACE_FILL_FIELD_NAMES]


def _classify_blocked_reason(reason: str) -> str:
    if reason in {"template_only_manifest", "manifest_missing"}:
        return "state"
    if reason == "evidence_stale_or_window_elapsed":
        return "stale"
    if reason in {
        "face_missing_from_manifest",
        "outside_repo_locator_not_supplied",
        "attestors_missing",
        "evidence_locator_missing",
        "locator_kind_missing",
        "verification_timestamp_missing",
        "fresh_until_missing",
        "bounded_window_missing",
        "reviewable_without_secrets_not_confirmed",
        "reviewability_note_missing",
    }:
        return "missing"
    if (
        reason in {"bounded_window_not_object", "faces_not_object", "face_entry_not_object", "attested_by_not_list"}
        or reason.startswith("manifest_invalid_json:")
        or reason.startswith("manifest_unexpected_keys:")
        or reason.startswith("bounded_window_unexpected_keys:")
        or reason.startswith("faces_unexpected_entries:")
        or reason.startswith("unexpected_face_keys:")
    ):
        return "malformed"
    return "other"


def _format_reason_counts(reason_counts: dict[str, int]) -> str:
    if not reason_counts:
        return "none"
    return ", ".join(f"{reason}={count}" for reason, count in sorted(reason_counts.items()))


def _group_reason_counts(reasons: list[str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {group: [] for group in BLOCKED_REASON_GROUP_ORDER}
    for reason in reasons:
        grouped[_classify_blocked_reason(reason)].append(reason)
    return {group: values for group, values in grouped.items() if values}


def _build_runtime_guardrails(runtime_config: Any) -> dict[str, Any]:
    return {
        "allowed_symbols": list(runtime_config.allowed_symbols),
        "default_symbol": runtime_config.default_symbol,
        "order_size_lots": str(runtime_config.order_size_lots),
        "max_order_size_lots": str(runtime_config.max_order_size_lots),
        "bounded_window_minutes": runtime_config.bounded_window_minutes,
        "max_open_positions": runtime_config.max_open_positions,
    }


def build_expected_faces(template_env: dict[str, str], runtime_config: Any) -> list[dict[str, Any]]:
    runtime_guardrails = _build_runtime_guardrails(runtime_config)
    return [
        {
            "name": "external_credential_source_face",
            "label": "credential source",
            "repo_visible_marker": template_env["DEXTER_DEMO_CREDENTIAL_SOURCE"],
            "refresh_owner": "named_operator_owner_outside_repo",
            "what_face_covers": (
                "The external credential reference resolves to the intended Dexter paper-live demo "
                "credential source for the bounded supervised window."
            ),
            "minimum_evidence_locator_shape": (
                "attestor name, reference label only, bounded window, verification timestamp, and a "
                "plain-language confirmation that the referenced credential source was resolved outside repo"
            ),
            "stale_condition": (
                "the credential reference changes or the bounded supervised window rolls forward"
            ),
            "usable_for_retry_gate_review_when": (
                "the repo can point to a current attestation record for this face without exposing secret material"
            ),
            "operator_input_needed": (
                "Provide one current non-secret locator that confirms which Dexter paper-live credential "
                "source was resolved for the bounded supervised window."
            ),
        },
        {
            "name": "venue_ref_face",
            "label": "venue reference",
            "repo_visible_marker": template_env["DEXTER_DEMO_VENUE_REF"],
            "refresh_owner": "named_operator_owner_plus_venue_owner_outside_repo",
            "what_face_covers": (
                "The repo-visible venue reference points to the intended Dexter demo venue for the bounded "
                "supervised retry window."
            ),
            "minimum_evidence_locator_shape": (
                "attestor names, venue reference label, bounded window, verification timestamp, and explicit "
                "match confirmation between the marker and the intended venue"
            ),
            "stale_condition": (
                "the venue reference changes, venue routing changes, or the supervised window is rescheduled"
            ),
            "usable_for_retry_gate_review_when": (
                "the venue attestation is current, explicit, and reviewable without requiring the reviewer "
                "to infer the mapping"
            ),
            "operator_input_needed": (
                "Provide one current non-secret locator that ties the repo-visible venue marker to the exact "
                "Dexter demo venue for the bounded supervised window."
            ),
        },
        {
            "name": "account_ref_face",
            "label": "account reference",
            "repo_visible_marker": template_env["DEXTER_DEMO_ACCOUNT_REF"],
            "refresh_owner": "named_operator_owner_outside_repo",
            "what_face_covers": (
                "The repo-visible account reference points to the intended Dexter paper-live demo account for "
                "the bounded supervised window."
            ),
            "minimum_evidence_locator_shape": (
                "attestor name, account reference label, bounded window, verification timestamp, and a "
                "statement that the external account binding was checked outside repo"
            ),
            "stale_condition": (
                "the account reference changes or a different demo account is selected for the window"
            ),
            "usable_for_retry_gate_review_when": (
                "the account attestation makes the intended demo account explicit enough to reopen gate review"
            ),
            "operator_input_needed": (
                "Provide one current non-secret locator that shows which Dexter paper-live demo account the "
                "bounded supervised window is bound to."
            ),
        },
        {
            "name": "connectivity_profile_face",
            "label": "connectivity profile",
            "repo_visible_marker": template_env["DEXTER_DEMO_CONNECTIVITY_PROFILE"],
            "refresh_owner": "named_operator_owner_plus_connectivity_owner_outside_repo",
            "what_face_covers": (
                "The intended connectivity profile can reach the intended Dexter demo venue and account during "
                "the bounded supervised window."
            ),
            "minimum_evidence_locator_shape": (
                "attestor names, connectivity profile label, verification timestamp, bounded window, and a "
                "short reachability result"
            ),
            "stale_condition": (
                "network routing changes, connectivity profile changes, or the verification timestamp is "
                "outside the current window"
            ),
            "usable_for_retry_gate_review_when": (
                "the connectivity attestation is current enough that a gate reviewer can treat reachability "
                "as explicitly checked"
            ),
            "operator_input_needed": (
                "Provide one current non-secret locator that shows the intended connectivity profile was "
                "checked for venue/account reachability inside the bounded supervised window."
            ),
        },
        {
            "name": "operator_owner_face",
            "label": "operator owner",
            "repo_visible_marker": "unconfirmed_outside_repo",
            "refresh_owner": "demo_operator_lead_outside_repo",
            "what_face_covers": (
                "One explicit operator owner is responsible for the full retry-gate review and bounded "
                "supervised window."
            ),
            "minimum_evidence_locator_shape": (
                "owner name or handle, verification timestamp, window label, and explicit ownership statement"
            ),
            "stale_condition": "the named owner changes or the supervised window changes",
            "usable_for_retry_gate_review_when": (
                "the owner attestation is explicit enough that gate recheck does not rely on unnamed "
                "responsibility"
            ),
            "operator_input_needed": (
                "Name one explicit operator owner and provide one reviewable non-secret locator that shows "
                "ownership for the bounded supervised window."
            ),
        },
        {
            "name": "bounded_start_criteria_face",
            "label": "bounded start criteria",
            "repo_visible_marker": {
                "bounded_window_minutes": runtime_config.bounded_window_minutes,
                "status_delivery": "poll_first",
                "halt_mode": "manual_latched_stop_all",
            },
            "refresh_owner": "named_operator_owner_outside_repo",
            "what_face_covers": (
                "The intended supervised start window, go/no-go owner, and abort owner are explicit and "
                "bounded for the next reviewable retry attempt."
            ),
            "minimum_evidence_locator_shape": (
                "planned start window, bounded window minutes, go/no-go owner, abort owner, verification "
                "timestamp, and explicit stop condition note"
            ),
            "stale_condition": (
                "the scheduled window moves or ownership for go/no-go or abort changes"
            ),
            "usable_for_retry_gate_review_when": (
                "the bounded-start attestation makes timing and ownership explicit enough to reopen gate review"
            ),
            "operator_input_needed": (
                "Provide one current non-secret locator that fixes the bounded start window plus the go/no-go "
                "and abort owners for the next supervised retry attempt."
            ),
        },
        {
            "name": "allowlist_symbol_lot_reconfirmed",
            "label": "allowlist / symbol / lot reconfirmation",
            "repo_visible_marker": runtime_guardrails,
            "refresh_owner": "named_operator_owner_outside_repo",
            "what_face_covers": (
                "The explicit allowlist, default symbol, lot size, bounded window, and one-position cap were "
                "reconfirmed for the upcoming supervised window."
            ),
            "minimum_evidence_locator_shape": (
                "attestor name, verification timestamp, allowlist values, lot-size values, position cap, and "
                "a plain-language reconfirmation note"
            ),
            "stale_condition": "any guardrail value changes or the supervised window moves",
            "usable_for_retry_gate_review_when": (
                "the guardrail attestation is current enough that gate recheck can treat the bounded demo "
                "envelope as explicitly reconfirmed"
            ),
            "operator_input_needed": (
                "Provide one current non-secret locator that reconfirms the allowlist, default symbol, lot "
                "size, one-position cap, and bounded window guardrails for the next supervised attempt."
            ),
        },
        {
            "name": "manual_latched_stop_all_visibility_reconfirmed",
            "label": "manual_latched_stop_all visibility",
            "repo_visible_marker": "baseline_stop_all_state=flatten_confirmed",
            "refresh_owner": "named_operator_owner_outside_repo",
            "what_face_covers": (
                "`manual_latched_stop_all` remains visibly reachable on the bounded retry path for the next "
                "supervised window."
            ),
            "minimum_evidence_locator_shape": (
                "attestor name, verification timestamp, referenced stop-all surface, and a plain-language "
                "visibility confirmation"
            ),
            "stale_condition": (
                "the stop-all surface changes or the window advances without reconfirmation"
            ),
            "usable_for_retry_gate_review_when": (
                "the stop-all visibility attestation is current enough to reopen gate review without assuming "
                "prior visibility still holds"
            ),
            "operator_input_needed": (
                "Provide one current non-secret locator that freshly reconfirms `manual_latched_stop_all` "
                "visibility for the bounded supervised window."
            ),
        },
        {
            "name": "terminal_snapshot_readability_reconfirmed",
            "label": "terminal snapshot readability",
            "repo_visible_marker": "baseline_terminal_snapshot_readable=true",
            "refresh_owner": "named_operator_owner_outside_repo",
            "what_face_covers": (
                "Terminal snapshot detail remains readable enough for the upcoming supervised retry window."
            ),
            "minimum_evidence_locator_shape": (
                "attestor name, verification timestamp, referenced snapshot surface, and a short readability "
                "confirmation"
            ),
            "stale_condition": (
                "the snapshot format changes or the supervised window advances without reconfirmation"
            ),
            "usable_for_retry_gate_review_when": (
                "the snapshot-readability attestation is current enough that a gate reviewer can rely on "
                "terminal visibility without inference"
            ),
            "operator_input_needed": (
                "Provide one current non-secret locator that freshly reconfirms terminal snapshot readability "
                "for the bounded supervised window."
            ),
        },
    ]


def build_manifest_template(template_env: dict[str, str], runtime_config: Any) -> dict[str, Any]:
    faces = {}
    for face in build_expected_faces(template_env, runtime_config):
        faces[face["name"]] = {
            "provided": False,
            "attested_by": [],
            "evidence_locator": None,
            "locator_kind": None,
            "verified_at": None,
            "fresh_until": None,
            "reviewable_without_secrets": False,
            "reviewability_note": None,
            "summary": face["what_face_covers"],
            "marker_match_note": f"Expected repo-visible marker: {_format_marker(face['repo_visible_marker'])}",
            "operator_input_remaining": face["operator_input_needed"],
        }
    return {
        "manifest_kind": MANIFEST_KIND,
        "schema_version": SCHEMA_VERSION,
        "manifest_role": "template",
        "updated_at": None,
        "bounded_supervised_window": {
            "label": "fill_current_bounded_supervised_window",
            "starts_at": None,
            "ends_at": None,
        },
        "notes": [
            "Replace placeholder values with current non-secret outside-repo evidence locators.",
            "Keep secrets outside repo; this manifest should point to reviewable locators only.",
            "Fill bounded_supervised_window.label, starts_at, and ends_at before switching manifest_role to evidence.",
            "For each blocked face, fill provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, and reviewability_note.",
            "After updating the manifest, rerun the canonical gap script plus the refresh and regeneration generators to refresh the proof surfaces.",
        ],
        "faces": faces,
    }


def _load_manifest(manifest_path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not manifest_path.exists():
        return None, [f"manifest_missing:{manifest_path.as_posix()}"]
    try:
        payload = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as exc:
        return None, [f"manifest_invalid_json:{exc.msg}"]
    if not isinstance(payload, dict):
        return None, ["manifest_top_level_not_object"]
    errors: list[str] = []
    extra_top_level = sorted(set(payload) - TOP_LEVEL_KEYS)
    if extra_top_level:
        errors.append(f"manifest_unexpected_keys:{','.join(extra_top_level)}")
    return payload, errors


def validate_external_evidence_manifest(
    root: Path,
    template_env: dict[str, str],
    runtime_config: Any,
    *,
    as_of: str | None = None,
) -> dict[str, Any]:
    as_of_value = _parse_timestamp(as_of) if as_of else datetime.now(timezone.utc).replace(microsecond=0)
    manifest_path = root / MANIFEST_REL_PATH
    expected_faces = build_expected_faces(template_env, runtime_config)
    manifest, validation_errors = _load_manifest(manifest_path)

    manifest_role = "missing"
    manifest_kind = None
    schema_version = None
    updated_at = None
    notes: list[str] = []
    window = {"label": "", "starts_at": None, "ends_at": None}
    window_start = None
    window_end = None
    face_payloads: dict[str, Any] = {}

    if manifest:
        manifest_role = _normalize_string(manifest.get("manifest_role")) or "template"
        manifest_kind = manifest.get("manifest_kind")
        schema_version = manifest.get("schema_version")
        updated_at = manifest.get("updated_at")
        notes_value = manifest.get("notes", [])
        if isinstance(notes_value, list):
            notes = [_normalize_string(item) for item in notes_value if _normalize_string(item)]
        window_value = manifest.get("bounded_supervised_window", {})
        if not isinstance(window_value, dict):
            validation_errors.append("bounded_window_not_object")
            window_value = {}
        extra_window_keys = sorted(set(window_value) - WINDOW_KEYS)
        if extra_window_keys:
            validation_errors.append(f"bounded_window_unexpected_keys:{','.join(extra_window_keys)}")
        window = {
            "label": _normalize_string(window_value.get("label")),
            "starts_at": window_value.get("starts_at"),
            "ends_at": window_value.get("ends_at"),
        }
        window_start = _parse_timestamp(window_value.get("starts_at"))
        window_end = _parse_timestamp(window_value.get("ends_at"))
        face_values = manifest.get("faces", {})
        if not isinstance(face_values, dict):
            validation_errors.append("faces_not_object")
            face_values = {}
        face_payloads = face_values
        extra_face_names = sorted(set(face_values) - set(REQUIRED_FACE_NAMES))
        if extra_face_names:
            validation_errors.append(f"faces_unexpected_entries:{','.join(extra_face_names)}")

    face_results: list[dict[str, Any]] = []
    blocked_faces: list[str] = []
    operator_inputs_remaining: list[str] = []

    for expected_face in expected_faces:
        name = expected_face["name"]
        entry = face_payloads.get(name, {})
        face_errors: list[str] = []
        if entry and not isinstance(entry, dict):
            face_errors.append("face_entry_not_object")
            entry = {}
        extra_face_keys = sorted(set(entry) - FACE_KEYS)
        if extra_face_keys:
            face_errors.append(f"unexpected_face_keys:{','.join(extra_face_keys)}")

        provided_flag = entry.get("provided") is True
        attested_by_value = entry.get("attested_by", [])
        if not isinstance(attested_by_value, list):
            face_errors.append("attested_by_not_list")
            attested_by_value = []
        attested_by = [_normalize_string(item) for item in attested_by_value if _normalize_string(item)]
        evidence_locator = _normalize_string(entry.get("evidence_locator"))
        locator_kind = _normalize_string(entry.get("locator_kind"))
        verified_at = _parse_timestamp(entry.get("verified_at"))
        fresh_until = _parse_timestamp(entry.get("fresh_until"))
        reviewable_without_secrets = entry.get("reviewable_without_secrets") is True
        reviewability_note = _normalize_string(entry.get("reviewability_note"))
        summary = _normalize_string(entry.get("summary"))
        marker_match_note = _normalize_string(entry.get("marker_match_note"))
        operator_input_remaining = (
            _normalize_string(entry.get("operator_input_remaining"))
            or expected_face["operator_input_needed"]
        )
        required_manifest_fields = _required_manifest_fields_for_face(name)

        present = provided_flag and bool(attested_by) and bool(evidence_locator) and bool(locator_kind)
        fresh_enough = bool(present and fresh_until and fresh_until >= as_of_value)
        current = bool(present and verified_at and fresh_enough and window_end and window_end >= as_of_value)
        reviewable = bool(present and reviewable_without_secrets and reviewability_note)
        stale = bool(
            (fresh_until and fresh_until < as_of_value)
            or (window_end and window_end < as_of_value)
        )

        blocked_reasons: list[str] = []
        if manifest_role == "missing":
            blocked_reasons.append("manifest_missing")
        elif manifest_role != "evidence":
            blocked_reasons.append("template_only_manifest")
        if not entry:
            blocked_reasons.append("face_missing_from_manifest")
        if not provided_flag:
            blocked_reasons.append("outside_repo_locator_not_supplied")
        if not attested_by:
            blocked_reasons.append("attestors_missing")
        if not evidence_locator:
            blocked_reasons.append("evidence_locator_missing")
        if not locator_kind:
            blocked_reasons.append("locator_kind_missing")
        if not verified_at:
            blocked_reasons.append("verification_timestamp_missing")
        if not fresh_until:
            blocked_reasons.append("fresh_until_missing")
        if not window_start or not window_end:
            blocked_reasons.append("bounded_window_missing")
        if stale:
            blocked_reasons.append("evidence_stale_or_window_elapsed")
        if present and not reviewable_without_secrets:
            blocked_reasons.append("reviewable_without_secrets_not_confirmed")
        if present and not reviewability_note:
            blocked_reasons.append("reviewability_note_missing")
        if face_errors:
            blocked_reasons.extend(face_errors)

        if blocked_reasons:
            blocked_faces.append(name)
            operator_inputs_remaining.append(f"{name}: {operator_input_remaining}")

        current_observation = (
            "Current non-secret outside-repo evidence for this face is present, fresh enough, and reviewable."
            if not blocked_reasons
            else (
                "Blocked because "
                + ", ".join(blocked_reasons)
                + f". Operator input still needed: {operator_input_remaining}"
            )
        )

        face_results.append(
            {
                "name": name,
                "label": expected_face["label"],
                "repo_visible_marker": expected_face["repo_visible_marker"],
                "refresh_owner": expected_face["refresh_owner"],
                "what_face_covers": expected_face["what_face_covers"],
                "minimum_evidence_locator_shape": expected_face["minimum_evidence_locator_shape"],
                "stale_condition": expected_face["stale_condition"],
                "usable_for_retry_gate_review_when": expected_face[
                    "usable_for_retry_gate_review_when"
                ],
                "operator_input_needed": operator_input_remaining,
                "declared": name in face_payloads,
                "present": present,
                "current": current,
                "fresh_enough": fresh_enough,
                "reviewable": reviewable,
                "stale": stale,
                "blocked": bool(blocked_reasons),
                "blocked_reasons": blocked_reasons,
                "attested_by": attested_by,
                "evidence_locator": evidence_locator,
                "locator_kind": locator_kind,
                "verified_at": verified_at.isoformat().replace("+00:00", "Z")
                if verified_at
                else None,
                "fresh_until": fresh_until.isoformat().replace("+00:00", "Z")
                if fresh_until
                else None,
                "summary": summary,
                "marker_match_note": marker_match_note,
                "required_manifest_fields": required_manifest_fields,
                "proof_paths_to_recheck": PROOF_PATHS_TO_RECHECK,
                "current_observation": current_observation,
            }
        )

    retry_gate_review_reopen_ready = all(
        not face["blocked"] and face["current"] and face["reviewable"] for face in face_results
    )

    if manifest_role == "missing":
        manifest_status = "missing"
    elif validation_errors:
        manifest_status = "invalid"
    elif manifest_role != "evidence":
        manifest_status = "template_only"
    elif retry_gate_review_reopen_ready:
        manifest_status = "ready"
    else:
        manifest_status = "incomplete"

    return {
        "task_id": TASK_ID,
        "generated_at": as_of_value.isoformat().replace("+00:00", "Z"),
        "manifest": {
            "path": MANIFEST_REL_PATH,
            "exists": manifest is not None,
            "status": manifest_status,
            "role": manifest_role,
            "manifest_kind": manifest_kind,
            "schema_version": schema_version,
            "updated_at": updated_at,
            "contract_spec": CONTRACT_SPEC_REL_PATH,
            "notes": notes,
            "window_fields_to_fill": WINDOW_FIELD_PATHS,
            "proof_paths_to_recheck": PROOF_PATHS_TO_RECHECK,
            "preflight_proof": PREFLIGHT_PROOF_REL_PATH,
            "preflight_report": PREFLIGHT_REPORT_REL_PATH,
            "preflight_summary": PREFLIGHT_SUMMARY_REL_PATH,
            "preflight_command": PREFLIGHT_COMMAND,
            "legacy_gap_command": LEGACY_GAP_COMMAND,
            "rerun_commands": RERUN_COMMANDS,
        },
        "bounded_supervised_window": {
            "label": window["label"],
            "starts_at": window_start.isoformat().replace("+00:00", "Z")
            if window_start
            else None,
            "ends_at": window_end.isoformat().replace("+00:00", "Z") if window_end else None,
        },
        "summary": {
            "required_face_count": len(face_results),
            "present_face_count": sum(face["present"] for face in face_results),
            "current_face_count": sum(face["current"] for face in face_results),
            "reviewable_face_count": sum(face["reviewable"] for face in face_results),
            "stale_face_count": sum(face["stale"] for face in face_results),
            "blocked_face_count": len(blocked_faces),
            "blocked_faces": blocked_faces,
            "retry_gate_review_reopen_ready": retry_gate_review_reopen_ready,
            "operator_inputs_remaining": operator_inputs_remaining,
            "window_fields_to_fill": WINDOW_FIELD_PATHS,
            "proof_paths_to_recheck": PROOF_PATHS_TO_RECHECK,
            "rerun_commands": RERUN_COMMANDS,
        },
        "validation_errors": validation_errors,
        "faces": face_results,
    }


def build_external_evidence_preflight(gap_payload: dict[str, Any]) -> dict[str, Any]:
    manifest = gap_payload["manifest"]
    summary = gap_payload["summary"]
    validation_errors = list(gap_payload["validation_errors"])

    blocked_reason_counts: Counter[str] = Counter()
    blocked_reason_group_counts: Counter[str] = Counter()
    grouped_reason_counts: dict[str, Counter[str]] = {
        group: Counter() for group in BLOCKED_REASON_GROUP_ORDER
    }
    faces: list[dict[str, Any]] = []

    for face in gap_payload["faces"]:
        blocked_reasons = list(face["blocked_reasons"])
        reopen_blockers = _group_reason_counts(blocked_reasons)
        reopen_ready_now = bool(face["current"] and face["reviewable"] and not face["blocked"])
        for reason in blocked_reasons:
            blocked_reason_counts[reason] += 1
            reason_group = _classify_blocked_reason(reason)
            blocked_reason_group_counts[reason_group] += 1
            grouped_reason_counts[reason_group][reason] += 1
        faces.append(
            {
                **face,
                "reopen_ready_now": reopen_ready_now,
                "reopen_status": "PASS" if reopen_ready_now else "FAIL/BLOCKED",
                "reopen_blockers": reopen_blockers,
            }
        )

    for error in validation_errors:
        blocked_reason_counts[error] += 1
        blocked_reason_group_counts["malformed"] += 1
        grouped_reason_counts["malformed"][error] += 1

    aggregated_reason_groups = {
        group: dict(sorted(counter.items()))
        for group, counter in grouped_reason_counts.items()
        if counter
    }
    grouped_reason_totals = {
        group: blocked_reason_group_counts[group]
        for group in BLOCKED_REASON_GROUP_ORDER
        if blocked_reason_group_counts[group]
    }
    retry_gate_review_reopen_ready = bool(summary["retry_gate_review_reopen_ready"])
    preflight_status = "ready" if retry_gate_review_reopen_ready else "blocked"

    return {
        "task_id": PREFLIGHT_TASK_ID,
        "generated_at": gap_payload["generated_at"],
        "manifest": {
            **manifest,
            "gap_proof": GAP_PROOF_REL_PATH,
            "gap_report": GAP_REPORT_REL_PATH,
            "gap_summary": GAP_SUMMARY_REL_PATH,
        },
        "reopen_readiness": {
            "status": preflight_status,
            "decision": (
                "retry_gate_review_reopen_ready"
                if retry_gate_review_reopen_ready
                else "retry_gate_review_reopen_blocked"
            ),
            "manifest_status": manifest["status"],
            "retry_gate_review_reopen_ready": retry_gate_review_reopen_ready,
            "blocked_face_count": summary["blocked_face_count"],
            "blocked_faces": list(summary["blocked_faces"]),
            "present_face_count": summary["present_face_count"],
            "current_face_count": summary["current_face_count"],
            "reviewable_face_count": summary["reviewable_face_count"],
            "stale_face_count": summary["stale_face_count"],
            "operator_inputs_remaining": list(summary["operator_inputs_remaining"]),
            "blocked_reason_counts": dict(sorted(blocked_reason_counts.items())),
            "blocked_reason_group_counts": grouped_reason_totals,
            "blocked_reason_groups": aggregated_reason_groups,
            "canonical_command": manifest["preflight_command"],
            "proof_paths_to_recheck": list(manifest["proof_paths_to_recheck"]),
            "rerun_commands": list(manifest["rerun_commands"]),
        },
        "faces": faces,
        "validation_errors": validation_errors,
    }


def render_preflight_summary_markdown(preflight_payload: dict[str, Any]) -> str:
    readiness = preflight_payload["reopen_readiness"]
    manifest = preflight_payload["manifest"]
    return "\n".join(
        [
            f"# {PREFLIGHT_TASK_ID} Summary",
            "",
            f"- Preflight status: `{readiness['status']}`",
            f"- Manifest status: `{readiness['manifest_status']}`",
            f"- Manifest path: `{manifest['path']}`",
            f"- Retry-gate review reopen ready: `{_format_bool(readiness['retry_gate_review_reopen_ready'])}`",
            f"- Blocked faces: `{', '.join(readiness['blocked_faces']) or 'none'}`",
            f"- Aggregated blocked reasons: `{_format_reason_counts(readiness['blocked_reason_counts'])}`",
            f"- Aggregated blocker groups: `{_format_reason_counts(readiness['blocked_reason_group_counts'])}`",
            f"- Canonical preflight command: `{readiness['canonical_command']}`",
            "",
            "## Operator Inputs Remaining",
            *[f"- `{item}`" for item in readiness["operator_inputs_remaining"]],
            "",
        ]
    )


def render_preflight_report_markdown(preflight_payload: dict[str, Any]) -> str:
    manifest = preflight_payload["manifest"]
    readiness = preflight_payload["reopen_readiness"]
    lines = [
        "# Demo Forward Supervised Run Retry Gate Evidence Preflight Report",
        "",
        "## Canonical Preflight",
        f"- Contract spec: `{manifest['contract_spec']}`",
        f"- Canonical manifest: `{manifest['path']}`",
        f"- Preflight proof: `{manifest['preflight_proof']}`",
        f"- Preflight report: `{manifest['preflight_report']}`",
        f"- Preflight summary: `{manifest['preflight_summary']}`",
        f"- Legacy gap proof: `{manifest['gap_proof']}`",
        f"- Legacy gap report: `{manifest['gap_report']}`",
        f"- Legacy gap summary: `{manifest['gap_summary']}`",
        f"- Generated at: `{preflight_payload['generated_at']}`",
        f"- Manifest status: `{readiness['manifest_status']}`",
        f"- Retry-gate review reopen ready: `{_format_bool(readiness['retry_gate_review_reopen_ready'])}`",
        "",
        "## Unified Reopen-Readiness",
        f"- Decision: `{readiness['decision']}`",
        f"- Preflight status: `{readiness['status']}`",
        f"- Blocked faces: `{', '.join(readiness['blocked_faces']) or 'none'}`",
        f"- Aggregated blocked reasons: `{_format_reason_counts(readiness['blocked_reason_counts'])}`",
        f"- Aggregated blocker groups: `{_format_reason_counts(readiness['blocked_reason_group_counts'])}`",
        f"- Single canonical command: `{readiness['canonical_command']}`",
        "",
        "## Template-Only Handoff",
        f"- Fill these bounded-window fields once per supervised window: `{', '.join(manifest['window_fields_to_fill'])}`",
        "- Leave `manifest_role` at `template` until every blocked face has a current, non-secret, reviewable locator.",
        f"- Proof/report surfaces to recheck after manifest updates: `{', '.join(readiness['proof_paths_to_recheck'])}`",
        *[f"- Rerun: `{command}`" for command in readiness["rerun_commands"]],
        f"- Legacy compatibility rerun: `{manifest['legacy_gap_command']}`",
        "",
        "## Face Status",
        "",
        "| Face | Present | Current | Reviewable | Reopen ready now | Blocker groups | Operator input still needed |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for face in preflight_payload["faces"]:
        blocker_groups = "; ".join(
            f"{group}={', '.join(reasons)}" for group, reasons in face["reopen_blockers"].items()
        )
        lines.append(
            "| "
            f"`{face['name']}` | "
            f"`{_format_bool(face['present'])}` | "
            f"`{_format_bool(face['current'])}` | "
            f"`{_format_bool(face['reviewable'])}` | "
            f"`{_format_bool(face['reopen_ready_now'])}` | "
            f"{blocker_groups or 'none'} | "
            f"{face['operator_input_needed']} |"
        )
    lines.extend(
        [
            "",
            "## Face-To-Manifest And Proof Map",
            "",
        ]
    )
    for face in preflight_payload["faces"]:
        aggregated_blockers = "; ".join(
            f"{group}={', '.join(reasons)}" for group, reasons in face["reopen_blockers"].items()
        )
        lines.extend(
            [
                f"### `{face['name']}`",
                f"- Manifest fields to fill: `{', '.join(face['required_manifest_fields'])}`",
                f"- Proof/report surfaces to recheck: `{', '.join(face['proof_paths_to_recheck'])}`",
                f"- Aggregated reopen blockers: `{aggregated_blockers or 'none'}`",
                f"- Repo-visible marker: `{_format_marker(face['repo_visible_marker'])}`",
                f"- Operator input still needed: {face['operator_input_needed']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Validation Errors",
            *(
                [f"- `{error}`" for error in preflight_payload["validation_errors"]]
                if preflight_payload["validation_errors"]
                else ["- none"]
            ),
            "",
            "The preflight stays fail-closed. It does not claim retry-gate reopen unless the canonical manifest "
            "is marked `evidence`, every required face is present, current, and reviewable, and the manifest "
            "remains non-secret by construction.",
            "",
        ]
    )
    return "\n".join(lines)


def render_gap_summary_markdown(gap_payload: dict[str, Any]) -> str:
    summary = gap_payload["summary"]
    manifest = gap_payload["manifest"]
    return "\n".join(
        [
            f"# {TASK_ID} Summary",
            "",
            f"- Manifest status: `{manifest['status']}`",
            f"- Manifest path: `{manifest['path']}`",
            f"- Required faces: `{summary['required_face_count']}`",
            f"- Present/current/reviewable: `{summary['present_face_count']}` / `{summary['current_face_count']}` / `{summary['reviewable_face_count']}`",
            f"- Blocked faces: `{', '.join(summary['blocked_faces']) or 'none'}`",
            f"- Retry-gate review reopen ready: `{_format_bool(summary['retry_gate_review_reopen_ready'])}`",
            f"- Window fields to fill: `{', '.join(summary['window_fields_to_fill'])}`",
            f"- Canonical preflight command: `{manifest['preflight_command']}`",
            f"- Legacy gap command: `{manifest['legacy_gap_command']}`",
            f"- Next operator step: `{manifest['preflight_command']}` after filling the template, then rerun refresh/regeneration surfaces.",
            "",
            "## Operator Inputs Remaining",
            *[f"- `{item}`" for item in summary["operator_inputs_remaining"]],
            "",
        ]
    )


def render_gap_report_markdown(gap_payload: dict[str, Any]) -> str:
    manifest = gap_payload["manifest"]
    summary = gap_payload["summary"]
    lines = [
        "# Demo Forward Supervised Run Retry Gate External Evidence Gap Report",
        "",
        "## Canonical Contract",
        f"- Contract spec: `{manifest['contract_spec']}`",
        f"- Canonical manifest: `{manifest['path']}`",
        f"- Manifest status: `{manifest['status']}`",
        f"- Manifest role: `{manifest['role']}`",
        f"- Generated at: `{gap_payload['generated_at']}`",
        f"- Retry-gate review reopen ready: `{_format_bool(summary['retry_gate_review_reopen_ready'])}`",
        "",
        "## Summary",
        f"- Required faces: `{summary['required_face_count']}`",
        f"- Present faces: `{summary['present_face_count']}`",
        f"- Current faces: `{summary['current_face_count']}`",
        f"- Reviewable faces: `{summary['reviewable_face_count']}`",
        f"- Stale faces: `{summary['stale_face_count']}`",
        f"- Blocked faces: `{', '.join(summary['blocked_faces']) or 'none'}`",
        "",
        "## Template-Only Handoff",
        f"- Fill these bounded-window fields once per supervised window: `{', '.join(manifest['window_fields_to_fill'])}`",
        "- Leave `manifest_role` at `template` until every blocked face has a current, non-secret, reviewable locator.",
        f"- Canonical preflight command: `{manifest['preflight_command']}`",
        f"- Canonical preflight report: `{manifest['preflight_report']}`",
        f"- Proof/report surfaces to recheck after manifest updates: `{', '.join(manifest['proof_paths_to_recheck'])}`",
        *[f"- Rerun: `{command}`" for command in manifest["rerun_commands"]],
        f"- Legacy compatibility rerun: `{manifest['legacy_gap_command']}`",
        "",
        "## Face Status",
        "",
        "| Face | Repo-visible marker | Present | Current | Fresh enough | Reviewable | Blocked reasons | Operator input still needed |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for face in gap_payload["faces"]:
        lines.append(
            "| "
            f"`{face['name']}` | "
            f"`{_format_marker(face['repo_visible_marker'])}` | "
            f"`{_format_bool(face['present'])}` | "
            f"`{_format_bool(face['current'])}` | "
            f"`{_format_bool(face['fresh_enough'])}` | "
            f"`{_format_bool(face['reviewable'])}` | "
            f"{', '.join(face['blocked_reasons']) or 'none'} | "
            f"{face['operator_input_needed']} |"
        )
    lines.extend(
        [
            "",
            "## Face-To-Manifest Map",
            "",
        ]
    )
    for face in gap_payload["faces"]:
        lines.extend(
            [
                f"### `{face['name']}`",
                f"- Manifest fields to fill: `{', '.join(face['required_manifest_fields'])}`",
                f"- Repo-visible marker: `{_format_marker(face['repo_visible_marker'])}`",
                f"- Operator input still needed: {face['operator_input_needed']}",
                f"- Proof/report surfaces to recheck: `{', '.join(face['proof_paths_to_recheck'])}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Validation Errors",
            *(
                [f"- `{error}`" for error in gap_payload["validation_errors"]]
                if gap_payload["validation_errors"]
                else ["- none"]
            ),
            "",
            "The gap report stays fail-closed. It does not claim current external evidence exists unless the "
            "canonical manifest is marked `evidence`, every required face is present, current, and reviewable, "
            "and the manifest remains non-secret by construction.",
            "",
        ]
    )
    return "\n".join(lines)


def write_external_evidence_gap_artifacts(
    root: Path,
    template_env: dict[str, str],
    runtime_config: Any,
    *,
    as_of: str | None = None,
) -> dict[str, Any]:
    return write_external_evidence_artifacts(
        root,
        template_env,
        runtime_config,
        as_of=as_of,
    )["gap"]


def write_external_evidence_preflight_artifacts(
    root: Path,
    template_env: dict[str, str],
    runtime_config: Any,
    *,
    as_of: str | None = None,
) -> dict[str, Any]:
    return write_external_evidence_artifacts(
        root,
        template_env,
        runtime_config,
        as_of=as_of,
    )["preflight"]


def write_external_evidence_artifacts(
    root: Path,
    template_env: dict[str, str],
    runtime_config: Any,
    *,
    as_of: str | None = None,
) -> dict[str, Any]:
    gap_payload = validate_external_evidence_manifest(
        root,
        template_env,
        runtime_config,
        as_of=as_of,
    )
    preflight_payload = build_external_evidence_preflight(gap_payload)
    preflight_proof_path = root / PREFLIGHT_PROOF_REL_PATH
    preflight_report_path = root / PREFLIGHT_REPORT_REL_PATH
    preflight_summary_path = root / PREFLIGHT_SUMMARY_REL_PATH
    proof_path = root / GAP_PROOF_REL_PATH
    report_path = root / GAP_REPORT_REL_PATH
    summary_path = root / GAP_SUMMARY_REL_PATH
    preflight_proof_path.parent.mkdir(parents=True, exist_ok=True)
    preflight_report_path.parent.mkdir(parents=True, exist_ok=True)
    proof_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    preflight_proof_path.write_text(json.dumps(preflight_payload, indent=2, sort_keys=False) + "\n")
    preflight_report_path.write_text(render_preflight_report_markdown(preflight_payload))
    preflight_summary_path.write_text(render_preflight_summary_markdown(preflight_payload))
    proof_path.write_text(json.dumps(gap_payload, indent=2, sort_keys=False) + "\n")
    report_path.write_text(render_gap_report_markdown(gap_payload))
    summary_path.write_text(render_gap_summary_markdown(gap_payload))
    return {"gap": gap_payload, "preflight": preflight_payload}
