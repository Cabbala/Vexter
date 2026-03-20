"""Helpers for loading frozen comparison run packages."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"expected object JSON at {path}")
    return payload


def _load_ndjson(path: Path) -> list[dict[str, Any]]:
    payload: list[dict[str, Any]] = []
    with path.open() as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            item = json.loads(line)
            if not isinstance(item, dict):
                raise ValueError(f"expected object NDJSON at {path}:{line_number}")
            payload.append(item)
    return payload


def _normalize_package_relative_path(raw_path: str) -> str:
    return raw_path.replace("\\", "/").strip()


def _resolve_package_path(package_dir: Path, raw_path: str | None, default_name: str) -> Path:
    if raw_path:
        candidate = Path(_normalize_package_relative_path(raw_path))
        if candidate.is_absolute():
            return candidate
        return package_dir / candidate
    return package_dir / default_name


def parse_utc_timestamp(raw_value: str | None) -> datetime | None:
    if not raw_value or not isinstance(raw_value, str):
        return None
    normalized = raw_value.strip()
    if not normalized:
        return None
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class RunPackage:
    package_dir: Path
    metadata_path: Path
    metadata: dict[str, Any]
    event_stream_path: Path
    events: list[dict[str, Any]]
    proof_manifest_path: Path
    proof_manifest: dict[str, Any]

    def resolve_relative_path(self, raw_path: str) -> Path:
        return _resolve_package_path(self.package_dir, raw_path, raw_path)


def load_run_package(package_dir: str | Path) -> RunPackage:
    package_root = Path(package_dir).resolve()
    metadata_path = package_root / "run_metadata.json"
    metadata = _load_json(metadata_path)

    event_stream_path = _resolve_package_path(
        package_root,
        metadata.get("event_stream"),
        "events.ndjson",
    )
    proof_manifest_path = _resolve_package_path(
        package_root,
        metadata.get("proof_manifest"),
        "proof_manifest.json",
    )

    events = _load_ndjson(event_stream_path)
    proof_manifest = _load_json(proof_manifest_path)

    return RunPackage(
        package_dir=package_root,
        metadata_path=metadata_path,
        metadata=metadata,
        event_stream_path=event_stream_path,
        events=events,
        proof_manifest_path=proof_manifest_path,
        proof_manifest=proof_manifest,
    )
