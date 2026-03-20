"""Contract validator for Vexter comparison run packages."""

from __future__ import annotations

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


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


def _issue(
    issues: list[dict[str, Any]],
    *,
    code: str,
    message: str,
    severity: str = "error",
    path: str | None = None,
    event_id: str | None = None,
) -> None:
    payload: dict[str, Any] = {
        "code": code,
        "severity": severity,
        "message": message,
    }
    if path:
        payload["path"] = path
    if event_id:
        payload["event_id"] = event_id
    issues.append(payload)


def validate_run_package(package_dir: str | Path) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []

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
            "issues": issues,
        }

    metadata = package.metadata
    source_system = metadata.get("source_system")

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

    missing_event_types = sorted(set(REQUIRED_EVENT_TYPES) - observed_event_types)
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

    error_codes = {issue["code"] for issue in issues if issue["severity"] == "error"}
    if error_codes & CRITICAL_ISSUE_CODES:
        classification = "fail"
    elif error_codes:
        classification = "partial"
    else:
        classification = "pass"

    coverage_ratio = len(observed_event_types & set(REQUIRED_EVENT_TYPES)) / len(
        REQUIRED_EVENT_TYPES
    )

    return {
        "package_dir": str(package.package_dir),
        "run_id": metadata.get("run_id"),
        "source_system": source_system,
        "classification": classification,
        "comparison_readiness": "comparable" if classification == "pass" else "observe_only",
        "checks": {
            "run_identity_ok": run_identity_ok,
            "required_event_types_ok": required_event_types_ok,
            "event_envelope_ok": event_envelope_ok,
            "payload_fields_ok": payload_fields_ok,
            "source_exports_ok": source_exports_ok,
            "proof_attribution_ok": proof_attribution_ok,
        },
        "coverage": {
            "required_event_types_present": len(observed_event_types & set(REQUIRED_EVENT_TYPES)),
            "required_event_types_total": len(REQUIRED_EVENT_TYPES),
            "event_completeness_ratio": coverage_ratio,
            "observed_event_types": sorted(observed_event_types),
            "missing_event_types": missing_event_types,
            "total_events": len(package.events),
        },
        "issues": issues,
    }
