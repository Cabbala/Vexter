"""Contract validator for Vexter comparison run packages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .constants import (
    REQUIRED_EVENT_ENVELOPE_FIELDS,
    REQUIRED_EVENT_PAYLOAD_FIELDS,
    REQUIRED_EVENT_TYPES,
    REQUIRED_PROOF_BUCKETS,
    REQUIRED_RUN_IDENTITY_FIELDS,
    SOURCE_REQUIRED_EXPORT_KEYS,
)
from .packages import load_run_package, parse_utc_timestamp


CRITICAL_ISSUE_CODES = {
    "load_failure",
    "unknown_source_system",
    "missing_event_stream",
    "empty_event_stream",
}

ISSUE_SAMPLE_EVENT_LIMIT = 10
CLEAN_SHUTDOWN_STATUSES = {
    "closed",
    "completed",
    "exited",
    "finalized",
    "finished",
    "shutdown_complete",
    "stopped",
}


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


def _load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        with path.open() as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def _session_key(event: dict[str, Any]) -> str:
    return str(
        event.get("session_id")
        or event.get("mint")
        or event.get("event_id")
        or "unknown-session"
    )


def _attempt_key(event: dict[str, Any]) -> tuple[str, int | None]:
    payload = event.get("payload", {})
    attempt_index = payload.get("attempt_index") if isinstance(payload, dict) else None
    return (_session_key(event), attempt_index)


def _event_types_by_requirement(
    package,
    *,
    source_system: str | None,
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    observed_entry_failure = _observed_entry_failure(package.events)
    clean_shutdown_proven = _clean_shutdown_proven(package.package_dir)
    mewx_candidate_snapshots_non_empty = _mewx_candidate_snapshots_non_empty(package)

    conditional_requirements = {
        "run_summary": {
            "required": clean_shutdown_proven,
            "reason": (
                "clean shutdown completion was proven by exported run-state evidence"
                if clean_shutdown_proven
                else "no clean shutdown completion proof was exported for this run package"
            ),
        },
        "entry_rejected": {
            "required": observed_entry_failure,
            "reason": (
                "at least one entry attempt did not produce a matching fill"
                if observed_entry_failure
                else "all observed entry attempts produced matching fills"
            ),
        },
        "creator_candidate": {
            "required": source_system != "mewx" or mewx_candidate_snapshots_non_empty,
            "reason": (
                "source is not mewx, so creator_candidate stays required"
                if source_system != "mewx"
                else (
                    "mewx candidate snapshot exports contained observations or source additions"
                    if mewx_candidate_snapshots_non_empty
                    else "mewx candidate snapshot exports were empty for this run package"
                )
            ),
        },
    }

    active_required_event_types = [
        event_type
        for event_type in REQUIRED_EVENT_TYPES
        if conditional_requirements.get(event_type, {}).get("required", True)
    ]
    return active_required_event_types, conditional_requirements


def _observed_entry_failure(events: list[dict[str, Any]]) -> bool:
    fill_attempts = {
        _attempt_key(event)
        for event in events
        if str(event.get("event_type")) == "entry_fill"
    }

    for event in events:
        if str(event.get("event_type")) != "entry_attempt":
            continue
        if _attempt_key(event) not in fill_attempts:
            return True
    return any(str(event.get("event_type")) == "entry_rejected" for event in events)


def _clean_shutdown_proven(package_dir: Path) -> bool:
    for state_path in sorted((package_dir / "exports").glob("*.state.json")):
        payload = _load_optional_json(state_path)
        if payload is None:
            continue

        ended_at_utc = payload.get("ended_at_utc")
        if isinstance(ended_at_utc, str) and parse_utc_timestamp(ended_at_utc) is not None:
            return True

        status = payload.get("status")
        if isinstance(status, str) and status.strip().lower() in CLEAN_SHUTDOWN_STATUSES:
            return True
    return False


def _mewx_candidate_snapshots_non_empty(package) -> bool:
    if package.metadata.get("source_system") != "mewx":
        return False

    snapshot_paths = sorted((package.package_dir / "exports").glob("*.candidates*.json"))
    source_exports = package.metadata.get("source_exports", {})
    if isinstance(source_exports, dict):
        refresh_export = source_exports.get("candidate_refresh_snapshot")
        if isinstance(refresh_export, str):
            refresh_path = package.resolve_relative_path(refresh_export)
            if refresh_path not in snapshot_paths:
                snapshot_paths.append(refresh_path)

    for snapshot_path in snapshot_paths:
        payload = _load_optional_json(snapshot_path)
        if payload is None:
            continue
        if _candidate_snapshot_has_candidates(payload):
            return True
    return False


def _candidate_snapshot_has_candidates(payload: dict[str, Any]) -> bool:
    observations = payload.get("observations")
    if isinstance(observations, list) and observations:
        return True

    added_keys = payload.get("added_keys")
    if isinstance(added_keys, list) and added_keys:
        return True

    source_counts = payload.get("source_counts")
    if isinstance(source_counts, dict):
        for value in source_counts.values():
            if isinstance(value, (int, float)) and value > 0:
                return True

    sources = payload.get("sources")
    if isinstance(sources, list) and sources:
        return True

    return False


def _issue(
    issues: dict[tuple[str, str, str, str | None], dict[str, Any]],
    *,
    code: str,
    message: str,
    severity: str = "error",
    path: str | None = None,
    event_id: str | None = None,
) -> None:
    key = (code, severity, message, path)
    payload = issues.get(key)
    if payload is None:
        payload = {
            "code": code,
            "severity": severity,
            "message": message,
            "count": 0,
        }
        if path:
            payload["path"] = path
        issues[key] = payload

    payload["count"] += 1
    if event_id:
        sample_event_ids = payload.setdefault("sample_event_ids", [])
        if len(sample_event_ids) < ISSUE_SAMPLE_EVENT_LIMIT:
            sample_event_ids.append(event_id)


def _materialize_issues(issues: dict[tuple[str, str, str, str | None], dict[str, Any]]) -> list[dict[str, Any]]:
    materialized = []
    for payload in issues.values():
        issue = dict(payload)
        if issue.get("count") == 1:
            issue.pop("count", None)
            sample_event_ids = issue.pop("sample_event_ids", None)
            if sample_event_ids:
                issue["event_id"] = sample_event_ids[0]
        materialized.append(issue)

    materialized.sort(
        key=lambda issue: (
            issue["severity"] != "error",
            issue["code"],
            issue.get("path", ""),
            issue["message"],
        )
    )
    return materialized


def validate_run_package(package_dir: str | Path) -> dict[str, Any]:
    issues: dict[tuple[str, str, str, str | None], dict[str, Any]] = {}

    try:
        package = load_run_package(package_dir)
    except Exception as exc:  # pragma: no cover - surfaced in tests through fail path
        _issue(
            issues,
            code="load_failure",
            message=str(exc),
            path=str(package_dir),
        )
        return {
            "package_dir": str(Path(package_dir).resolve()),
            "classification": "fail",
            "comparison_readiness": "observe_only",
            "checks": {
                "run_identity_ok": False,
                "required_event_types_ok": False,
                "event_envelope_ok": False,
                "payload_fields_ok": False,
                "source_exports_ok": False,
                "proof_attribution_ok": False,
            },
            "coverage": {
                "required_event_types_present": 0,
                "required_event_types_total": len(REQUIRED_EVENT_TYPES),
                "event_completeness_ratio": 0.0,
                "observed_event_types": [],
                "missing_event_types": REQUIRED_EVENT_TYPES,
                "total_events": 0,
            },
            "issues": _materialize_issues(issues),
        }

    metadata = package.metadata
    source_system = metadata.get("source_system")
    active_required_event_types, conditional_requirements = _event_types_by_requirement(
        package,
        source_system=source_system if isinstance(source_system, str) else None,
    )

    if source_system not in SOURCE_REQUIRED_EXPORT_KEYS:
        _issue(
            issues,
            code="unknown_source_system",
            message=f"unsupported source_system: {source_system!r}",
            path=str(package.metadata_path),
        )

    run_identity_ok = True
    for field in REQUIRED_RUN_IDENTITY_FIELDS:
        if not _has_value(metadata.get(field)):
            run_identity_ok = False
            _issue(
                issues,
                code="missing_run_identity_field",
                message=f"missing run identity field: {field}",
                path=str(package.metadata_path),
            )

    if parse_utc_timestamp(metadata.get("started_at_utc")) is None:
        run_identity_ok = False
        _issue(
            issues,
            code="invalid_started_at_utc",
            message="started_at_utc must be a valid ISO-8601 UTC timestamp",
            path=str(package.metadata_path),
        )
    if parse_utc_timestamp(metadata.get("ended_at_utc")) is None:
        run_identity_ok = False
        _issue(
            issues,
            code="invalid_ended_at_utc",
            message="ended_at_utc must be a valid ISO-8601 UTC timestamp",
            path=str(package.metadata_path),
        )

    event_stream_ref = metadata.get("event_stream", "events.ndjson")
    if not package.event_stream_path.exists():
        _issue(
            issues,
            code="missing_event_stream",
            message=f"event stream not found: {event_stream_ref}",
            path=str(package.event_stream_path),
        )
    if not package.events:
        _issue(
            issues,
            code="empty_event_stream",
            message="event stream does not contain any events",
            path=str(package.event_stream_path),
        )

    config_snapshot_ref = metadata.get("config_snapshot")
    proof_attribution_ok = True
    if not _has_value(config_snapshot_ref):
        proof_attribution_ok = False
        _issue(
            issues,
            code="missing_config_snapshot",
            message="run package metadata must point to a config snapshot",
            path=str(package.metadata_path),
        )
    else:
        config_snapshot_path = package.resolve_relative_path(str(config_snapshot_ref))
        if not config_snapshot_path.exists():
            proof_attribution_ok = False
            _issue(
                issues,
                code="missing_config_snapshot_file",
                message=f"config snapshot not found: {config_snapshot_ref}",
                path=str(config_snapshot_path),
            )

    source_exports_ok = True
    source_exports = metadata.get("source_exports", {})
    if not isinstance(source_exports, dict):
        source_exports_ok = False
        _issue(
            issues,
            code="invalid_source_exports",
            message="source_exports must be a JSON object",
            path=str(package.metadata_path),
        )
        source_exports = {}

    for export_key in SOURCE_REQUIRED_EXPORT_KEYS.get(source_system, []):
        export_path = source_exports.get(export_key)
        if not _has_value(export_path):
            source_exports_ok = False
            _issue(
                issues,
                code="missing_source_export",
                message=f"missing source export pointer: {export_key}",
                path=str(package.metadata_path),
            )
            continue
        resolved_export_path = package.resolve_relative_path(str(export_path))
        if not resolved_export_path.exists():
            source_exports_ok = False
            _issue(
                issues,
                code="missing_source_export_file",
                message=f"source export not found for {export_key}: {export_path}",
                path=str(resolved_export_path),
            )

    for bucket in REQUIRED_PROOF_BUCKETS:
        if bucket not in package.proof_manifest:
            proof_attribution_ok = False
            _issue(
                issues,
                code="missing_proof_bucket",
                message=f"proof manifest missing bucket: {bucket}",
                path=str(package.proof_manifest_path),
            )
            continue
        values = package.proof_manifest.get(bucket)
        if not isinstance(values, list):
            proof_attribution_ok = False
            _issue(
                issues,
                code="invalid_proof_bucket",
                message=f"proof manifest bucket must be a list: {bucket}",
                path=str(package.proof_manifest_path),
            )

    observed_event_types: set[str] = set()
    event_envelope_ok = True
    payload_fields_ok = True

    for event in package.events:
        event_id = str(event.get("event_id", ""))
        missing_fields = [
            field
            for field in REQUIRED_EVENT_ENVELOPE_FIELDS
            if not _has_value(event.get(field))
        ]
        if missing_fields:
            event_envelope_ok = False
            _issue(
                issues,
                code="missing_event_envelope_fields",
                message=f"event is missing envelope fields: {', '.join(missing_fields)}",
                event_id=event_id,
                path=str(package.event_stream_path),
            )

        event_type = event.get("event_type")
        if _has_value(event_type):
            observed_event_types.add(str(event_type))

        if _has_value(event.get("run_id")) and _has_value(metadata.get("run_id")):
            if event.get("run_id") != metadata.get("run_id"):
                event_envelope_ok = False
                _issue(
                    issues,
                    code="run_id_mismatch",
                    message="event run_id does not match run package metadata",
                    event_id=event_id,
                    path=str(package.event_stream_path),
                )
        if _has_value(event.get("source_system")) and _has_value(source_system):
            if event.get("source_system") != source_system:
                event_envelope_ok = False
                _issue(
                    issues,
                    code="source_system_mismatch",
                    message="event source_system does not match run package metadata",
                    event_id=event_id,
                    path=str(package.event_stream_path),
                )
        if _has_value(event.get("source_commit")) and _has_value(metadata.get("source_commit")):
            if event.get("source_commit") != metadata.get("source_commit"):
                event_envelope_ok = False
                _issue(
                    issues,
                    code="source_commit_mismatch",
                    message="event source_commit does not match run package metadata",
                    event_id=event_id,
                    path=str(package.event_stream_path),
                )
        if _has_value(event.get("mode")) and _has_value(metadata.get("mode")):
            if event.get("mode") != metadata.get("mode"):
                event_envelope_ok = False
                _issue(
                    issues,
                    code="mode_mismatch",
                    message="event mode does not match run package metadata",
                    event_id=event_id,
                    path=str(package.event_stream_path),
                )

        payload = event.get("payload")
        if not isinstance(payload, dict):
            payload_fields_ok = False
            _issue(
                issues,
                code="invalid_payload",
                message="event payload must be a JSON object",
                event_id=event_id,
                path=str(package.event_stream_path),
            )
            continue

        required_payload_fields = REQUIRED_EVENT_PAYLOAD_FIELDS.get(str(event_type), [])
        missing_payload_fields = [
            field
            for field in required_payload_fields
            if not _has_value(payload.get(field))
        ]
        if missing_payload_fields:
            payload_fields_ok = False
            _issue(
                issues,
                code="missing_event_payload_fields",
                message=(
                    f"event payload missing fields for {event_type}: "
                    f"{', '.join(missing_payload_fields)}"
                ),
                event_id=event_id,
                path=str(package.event_stream_path),
            )

    missing_event_types = sorted(set(active_required_event_types) - observed_event_types)
    required_event_types_ok = not missing_event_types
    if missing_event_types:
        _issue(
            issues,
            code="missing_required_event_types",
            message=(
                "required event types were not observed in the run package: "
                + ", ".join(missing_event_types)
            ),
            path=str(package.event_stream_path),
        )

    materialized_issues = _materialize_issues(issues)
    error_codes = {
        issue["code"] for issue in materialized_issues if issue["severity"] == "error"
    }
    if error_codes & CRITICAL_ISSUE_CODES:
        classification = "fail"
    elif error_codes:
        classification = "partial"
    else:
        classification = "pass"

    active_required_event_type_set = set(active_required_event_types)
    coverage_ratio = len(observed_event_types & active_required_event_type_set) / max(
        len(active_required_event_types),
        1,
    )

    return {
        "package_dir": str(package.package_dir),
        "run_id": metadata.get("run_id"),
        "source_system": source_system,
        "classification": classification,
        "comparison_readiness": "comparable" if classification == "pass" else "observe_only",
        "contract": {
            "event_type_catalog": REQUIRED_EVENT_TYPES,
            "active_required_event_types": active_required_event_types,
            "waived_event_types": sorted(set(REQUIRED_EVENT_TYPES) - active_required_event_type_set),
            "conditional_requirements": conditional_requirements,
        },
        "checks": {
            "run_identity_ok": run_identity_ok,
            "required_event_types_ok": required_event_types_ok,
            "event_envelope_ok": event_envelope_ok,
            "payload_fields_ok": payload_fields_ok,
            "source_exports_ok": source_exports_ok,
            "proof_attribution_ok": proof_attribution_ok,
        },
        "coverage": {
            "required_event_types_present": len(observed_event_types & active_required_event_type_set),
            "required_event_types_total": len(active_required_event_types),
            "event_type_catalog_total": len(REQUIRED_EVENT_TYPES),
            "event_completeness_ratio": coverage_ratio,
            "observed_event_types": sorted(observed_event_types),
            "missing_event_types": missing_event_types,
            "total_events": len(package.events),
        },
        "issues": materialized_issues,
    }
