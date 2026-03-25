"""Downstream replay-validation helpers for promoted comparison packs."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .constants import SOURCE_REQUIRED_EXPORT_KEYS
from .metrics import derive_metrics
from .pack import build_comparison_pack
from .packages import load_run_package
from .validator import validate_run_package


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _source_exports_status(package) -> dict[str, Any]:
    source_system = str(package.metadata.get("source_system", ""))
    source_exports = package.metadata.get("source_exports", {})
    if not isinstance(source_exports, dict):
        source_exports = {}

    required_keys = SOURCE_REQUIRED_EXPORT_KEYS.get(source_system, [])
    present_keys: list[str] = []
    missing_keys: list[str] = []

    for export_key in required_keys:
        export_path = source_exports.get(export_key)
        if not isinstance(export_path, str) or not export_path.strip():
            missing_keys.append(export_key)
            continue
        if package.resolve_relative_path(export_path).exists():
            present_keys.append(export_key)
            continue
        missing_keys.append(export_key)

    return {
        "required_keys": required_keys,
        "present_keys": sorted(present_keys),
        "missing_keys": sorted(missing_keys),
        "all_present": not missing_keys,
    }


def _package_replay_surface(
    package_dir: str | Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    package = load_run_package(package_dir)
    validation = validate_run_package(package_dir)
    metrics = derive_metrics(package_dir)

    replayability_metric = metrics["metrics"].get("replayability_grade", {})
    replayability_grade = (
        replayability_metric.get("value")
        if replayability_metric.get("status") == "ok"
        else "none"
    )
    proof_manifest = package.proof_manifest
    source_exports_status = _source_exports_status(package)
    raw_events = len(proof_manifest.get("raw_events") or [])
    logs = len(proof_manifest.get("logs") or [])
    replays = len(proof_manifest.get("replays") or [])
    db_exports = len(proof_manifest.get("db_exports") or [])

    surface = {
        "package_dir": str(package.package_dir),
        "run_id": package.metadata.get("run_id"),
        "source_system": package.metadata.get("source_system"),
        "mode": package.metadata.get("mode"),
        "transport_mode": package.metadata.get("transport_mode"),
        "started_at_utc": package.metadata.get("started_at_utc"),
        "ended_at_utc": package.metadata.get("ended_at_utc"),
        "validation_classification": validation.get("classification"),
        "replayability_grade": replayability_grade,
        "source_exports": source_exports_status,
        "proof_surface": {
            "raw_events": raw_events,
            "logs": logs,
            "replays": replays,
            "db_exports": db_exports,
        },
        "offline_reconstruction_surface_present": bool(raw_events)
        and source_exports_status["all_present"],
    }
    return surface, validation, metrics


def _matched_measurement_window(
    dexter_surface: dict[str, Any],
    mewx_surface: dict[str, Any],
) -> bool:
    return (
        dexter_surface.get("started_at_utc") == mewx_surface.get("started_at_utc")
        and dexter_surface.get("ended_at_utc") == mewx_surface.get("ended_at_utc")
        and bool(dexter_surface.get("started_at_utc"))
        and bool(dexter_surface.get("ended_at_utc"))
    )


def _baseline_payload(
    *,
    dexter_package_dir: str | Path,
    mewx_package_dir: str | Path,
    output_dir: str | Path,
    summary_note: str | None,
) -> dict[str, Any]:
    dexter_surface, dexter_validation, dexter_metrics = _package_replay_surface(
        dexter_package_dir
    )
    mewx_surface, mewx_validation, mewx_metrics = _package_replay_surface(
        mewx_package_dir
    )
    comparison_pack = build_comparison_pack(
        dexter_package_dir=dexter_package_dir,
        mewx_package_dir=mewx_package_dir,
        output_dir=output_dir,
        summary_note=summary_note,
    )
    matched_window = _matched_measurement_window(dexter_surface, mewx_surface)
    replay_input_accepted = (
        comparison_pack.get("winner_mode") == "derived"
        and dexter_validation.get("classification") == "pass"
        and mewx_validation.get("classification") == "pass"
        and matched_window
        and dexter_surface["offline_reconstruction_surface_present"]
        and mewx_surface["offline_reconstruction_surface_present"]
        and dexter_surface["replayability_grade"] != "none"
        and mewx_surface["replayability_grade"] != "none"
    )

    return {
        "comparison_output_dir": str(Path(output_dir).resolve()),
        "comparison_pack": {
            "pack_id": comparison_pack.get("pack_id"),
            "winner_mode": comparison_pack.get("winner_mode"),
            "summary_note": comparison_pack.get("summary_note"),
        },
        "matched_measurement_window": matched_window,
        "accepted_as_replay_input": replay_input_accepted,
        "dexter": {
            "surface": dexter_surface,
            "validation": dexter_validation,
            "metrics": dexter_metrics,
        },
        "mewx": {
            "surface": mewx_surface,
            "validation": mewx_validation,
            "metrics": mewx_metrics,
        },
    }


def _confirmatory_residual(confirmatory: dict[str, Any]) -> dict[str, Any]:
    mewx_missing = confirmatory["mewx"]["validation"]["coverage"]["missing_event_types"]
    only_candidate_rejected = mewx_missing == ["candidate_rejected"]
    return {
        "mewx_missing_event_types": mewx_missing,
        "narrow_note_only": only_candidate_rejected,
        "overturns_promoted_baseline": not only_candidate_rejected,
    }


def _render_summary(report: dict[str, Any]) -> str:
    promoted = report["promoted"]
    confirmatory = report["confirmatory"]
    decision = report["decision"]
    residual = confirmatory["residual"]

    lines = [
        "# TASK-006 Replay Validation",
        "",
        "## Promoted Baseline",
        "",
        f"- Input accepted: `{'yes' if promoted['accepted_as_replay_input'] else 'no'}`",
        f"- Winner mode: `{promoted['comparison_pack']['winner_mode']}`",
        f"- Dexter: `{promoted['dexter']['validation']['classification']}` / replayability `{promoted['dexter']['surface']['replayability_grade']}`",
        f"- Mew-X: `{promoted['mewx']['validation']['classification']}` / replayability `{promoted['mewx']['surface']['replayability_grade']}`",
        f"- Matched measurement window: `{'yes' if promoted['matched_measurement_window'] else 'no'}`",
        "",
        "## Confirmatory Context",
        "",
        f"- Winner mode: `{confirmatory['comparison_pack']['winner_mode']}`",
        f"- Dexter: `{confirmatory['dexter']['validation']['classification']}`",
        f"- Mew-X: `{confirmatory['mewx']['validation']['classification']}`",
        f"- Residual note: `{', '.join(residual['mewx_missing_event_types']) or 'none'}`",
        "",
        "## Decision",
        "",
        f"- Key finding: `{decision['key_finding']}`",
        f"- TASK-006 state: `{decision['task_state']}`",
        f"- Downstream comparability: `{decision['downstream_comparability']}`",
        f"- Replay exit ready: `{'yes' if decision['replay_exit_ready'] else 'no'}`",
        f"- Next step: `{decision['next_step']}`",
    ]
    return "\n".join(lines) + "\n"


def run_replay_validation(
    *,
    promoted_dexter_package_dir: str | Path,
    promoted_mewx_package_dir: str | Path,
    promoted_output_dir: str | Path,
    confirmatory_dexter_package_dir: str | Path,
    confirmatory_mewx_package_dir: str | Path,
    confirmatory_output_dir: str | Path,
    promoted_summary_note: str | None = None,
    confirmatory_summary_note: str | None = None,
) -> tuple[dict[str, Any], str]:
    promoted = _baseline_payload(
        dexter_package_dir=promoted_dexter_package_dir,
        mewx_package_dir=promoted_mewx_package_dir,
        output_dir=promoted_output_dir,
        summary_note=promoted_summary_note,
    )
    confirmatory = _baseline_payload(
        dexter_package_dir=confirmatory_dexter_package_dir,
        mewx_package_dir=confirmatory_mewx_package_dir,
        output_dir=confirmatory_output_dir,
        summary_note=confirmatory_summary_note,
    )
    confirmatory["residual"] = _confirmatory_residual(confirmatory)

    replay_exit_ready = (
        promoted["accepted_as_replay_input"]
        and promoted["dexter"]["surface"]["replayability_grade"] == "full"
        and promoted["mewx"]["surface"]["replayability_grade"] == "full"
    )
    downstream_comparability = (
        "accepted_for_replay_validation"
        if promoted["accepted_as_replay_input"]
        else "blocked"
    )
    if replay_exit_ready:
        downstream_comparability = "accepted_with_full_replayability"

    decision = {
        "key_finding": (
            "replay_input_accepted"
            if promoted["accepted_as_replay_input"]
            else "replay_blocker_found"
        ),
        "task_state": (
            "in_progress" if promoted["accepted_as_replay_input"] else "blocked"
        ),
        "downstream_comparability": downstream_comparability,
        "replay_exit_ready": replay_exit_ready,
        "next_step": (
            "task_006_replay_deepening"
            if promoted["accepted_as_replay_input"]
            else "repair_replay_input_surface"
        ),
    }

    report = {
        "task_id": "TASK-006-REPLAY-VALIDATION",
        "generated_at_utc": _iso_now(),
        "promoted": promoted,
        "confirmatory": confirmatory,
        "decision": decision,
    }
    return report, _render_summary(report)
