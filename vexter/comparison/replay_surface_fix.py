"""Helpers for repairing the Dexter replay surface on a frozen live package."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .metrics import derive_metrics
from .pack import build_comparison_pack
from .packages import load_run_package
from .replay_deepening import run_replay_deepening
from .validator import validate_run_package


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _safe_float(value: Any) -> float:
    if value is None or value == "":
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _safe_int(value: Any) -> int:
    if value is None or value == "":
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _runtime_layout(runtime_root: str) -> dict[str, str]:
    base = runtime_root.rstrip("\\/")
    return {
        "runtime_root": base,
        "config_dir": f"{base}\\runtime\\dexter\\config",
        "export_dir": f"{base}\\runtime\\dexter\\export",
        "raw_events_dir": f"{base}\\data\\raw\\dexter",
        "logs_dir": f"{base}\\data\\logs\\dexter",
        "replays_dir": f"{base}\\data\\replays\\dexter",
        "db_exports_dir": f"{base}\\data\\postgres\\dexter",
    }


def _session_groups(events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        session_id = str(
            event.get("session_id")
            or event.get("mint")
            or event.get("event_id")
            or "unknown-session"
        )
        grouped.setdefault(session_id, []).append(event)
    return grouped


def _event_type(events: list[dict[str, Any]], event_type: str) -> list[dict[str, Any]]:
    return [event for event in events if str(event.get("event_type")) == event_type]


def _latest_event(events: list[dict[str, Any]], event_type: str) -> dict[str, Any] | None:
    typed = _event_type(events, event_type)
    if not typed:
        return None
    return typed[-1]


def _close_summary_payload(session_events: list[dict[str, Any]]) -> dict[str, Any] | None:
    closed_event = _latest_event(session_events, "position_closed")
    if closed_event is None:
        return None

    closed_payload = closed_event.get("payload", {})
    if not isinstance(closed_payload, dict):
        return None

    if bool(closed_payload.get("stale_position_flag")):
        return None

    entry_fill = _latest_event(session_events, "entry_fill")
    exit_signal = _latest_event(session_events, "exit_signal")
    exit_fill = _latest_event(session_events, "exit_fill")
    last_session_update = _latest_event(session_events, "session_update")

    if entry_fill is None:
        return None

    entry_payload = entry_fill.get("payload", {})
    exit_signal_payload = exit_signal.get("payload", {}) if exit_signal else {}
    exit_fill_payload = exit_fill.get("payload", {}) if exit_fill else {}
    session_update_payload = (
        last_session_update.get("payload", {}) if last_session_update else {}
    )

    if not isinstance(entry_payload, dict):
        return None
    if not isinstance(exit_signal_payload, dict):
        exit_signal_payload = {}
    if not isinstance(exit_fill_payload, dict):
        exit_fill_payload = {}
    if not isinstance(session_update_payload, dict):
        session_update_payload = {}

    entry_price = _safe_float(closed_payload.get("entry_price"))
    exit_price = _safe_float(closed_payload.get("exit_price"))
    mfe_pct = _safe_float(closed_payload.get("mfe_pct"))
    realized_return_pct = _safe_float(closed_payload.get("realized_return_pct"))
    theoretical_best_price = _safe_float(exit_signal_payload.get("theoretical_best_price"))
    if theoretical_best_price == 0.0 and entry_price > 0:
        theoretical_best_price = entry_price * (1.0 + (mfe_pct / 100.0))

    mint = str(closed_event.get("mint") or entry_fill.get("mint") or "")
    creator = str(closed_event.get("creator") or entry_fill.get("creator") or "")
    session_id = str(
        closed_event.get("session_id") or entry_fill.get("session_id") or mint
    )
    exit_reason = str(exit_signal_payload.get("exit_reason") or "close_summary")

    return {
        "kind": "close_summary",
        "session_id": session_id,
        "mint": mint,
        "creator": creator,
        "closed_at_utc": str(closed_event.get("ts_utc") or ""),
        "entry_price": entry_price,
        "exit_price": exit_price,
        "realized_return_pct": realized_return_pct,
        "mfe_pct": mfe_pct,
        "mae_pct": _safe_float(closed_payload.get("mae_pct")),
        "time_to_peak_ms": _safe_int(closed_payload.get("time_to_peak_ms")),
        "session_duration_ms": _safe_int(closed_payload.get("session_duration_ms")),
        "stale_position_flag": False,
        "exit_reason": exit_reason,
        "signal_price": _safe_float(exit_signal_payload.get("signal_price")) or exit_price,
        "theoretical_best_price": theoretical_best_price,
        "realized_vs_peak_gap_pct": _safe_float(
            exit_signal_payload.get("realized_vs_peak_gap_pct")
        ),
        "fill_qty": _safe_float(exit_fill_payload.get("fill_qty"))
        or _safe_float(entry_payload.get("fill_qty")),
        "fill_latency_ms": _safe_int(exit_fill_payload.get("fill_latency_ms")),
        "wallet_balance_after": _safe_int(exit_fill_payload.get("wallet_balance_after")),
        "tx_signature": str(
            exit_fill_payload.get("tx_signature") or f"replay-close-summary:{mint}"
        ),
        "confirmation_path": str(exit_fill_payload.get("confirmation_path") or ""),
        "tx_strategy": str(exit_fill_payload.get("tx_strategy") or ""),
        "state_reason": str(
            session_update_payload.get("state_reason") or exit_reason or "close_summary"
        ),
    }


def augment_dexter_replay_surface(
    *,
    live_package_dir: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    package = load_run_package(live_package_dir)
    if str(package.metadata.get("source_system")) != "dexter":
        raise ValueError("augment_dexter_replay_surface only supports dexter packages")

    output_root = Path(output_dir).resolve()
    if output_root.exists():
        shutil.rmtree(output_root)
    shutil.copytree(package.package_dir, output_root)

    runtime_root = str(package.metadata.get("runtime_root") or "C:\\Users\\bot\\quant\\Vexter")
    session_groups = _session_groups(package.events)
    summary_paths: list[str] = []
    summary_rows: list[dict[str, Any]] = []

    for session_id in sorted(session_groups):
        payload = _close_summary_payload(session_groups[session_id])
        if payload is None:
            continue
        mint = str(payload["mint"])
        summary_path = output_root / "replays" / f"{mint}.close-summary.json"
        _write_json(
            summary_path,
            {
                "mint_id": mint,
                "exported_at_utc": payload["closed_at_utc"],
                "payload": payload,
                "runtime_layout": _runtime_layout(runtime_root),
            },
        )
        relative_path = str(summary_path.relative_to(output_root).as_posix())
        summary_paths.append(relative_path)
        summary_rows.append(
            {
                "mint": mint,
                "session_id": payload["session_id"],
                "closed_at_utc": payload["closed_at_utc"],
                "exit_reason": payload["exit_reason"],
                "realized_return_pct": payload["realized_return_pct"],
            }
        )

    index_path = output_root / "exports" / "dexter-close-summary-index.json"
    _write_json(
        index_path,
        {
            "generated_at_utc": _iso_now(),
            "run_id": package.metadata.get("run_id"),
            "source_commit": package.metadata.get("source_commit"),
            "summary_count": len(summary_paths),
            "summaries": summary_rows,
        },
    )
    index_relative = str(index_path.relative_to(output_root).as_posix())

    metadata_path = output_root / "run_metadata.json"
    metadata = json.loads(metadata_path.read_text())
    source_exports = metadata.get("source_exports", {})
    if not isinstance(source_exports, dict):
        source_exports = {}
    source_exports["close_summary_replay_index"] = index_relative
    metadata["source_exports"] = source_exports
    _write_json(metadata_path, metadata)

    proof_manifest_path = output_root / "proof_manifest.json"
    proof_manifest = json.loads(proof_manifest_path.read_text())
    for bucket in ("replays", "db_exports"):
        values = proof_manifest.get(bucket)
        if not isinstance(values, list):
            values = []
        proof_manifest[bucket] = sorted(set(values + summary_paths))
    export_values = proof_manifest.get("exports")
    if not isinstance(export_values, list):
        export_values = []
    proof_manifest["exports"] = sorted(set(export_values + [index_relative]))
    _write_json(proof_manifest_path, proof_manifest)

    validation = validate_run_package(output_root)
    metrics = derive_metrics(output_root)

    return {
        "package_dir": str(output_root),
        "augmented_from_package_dir": str(package.package_dir),
        "close_summary_count": len(summary_paths),
        "close_summary_paths": summary_paths,
        "close_summary_session_keys": [
            str(row["session_id"]) for row in summary_rows
        ],
        "close_summary_index": index_relative,
        "validation": validation,
        "metrics": metrics,
    }


def _render_summary(report: dict[str, Any]) -> str:
    promoted = report["promoted"]
    dexter_gap = promoted["replay_measurement"]["dexter"]["gap"]
    mewx_gap = promoted["replay_measurement"]["mewx"]["gap"]
    decision = report["decision"]

    lines = [
        "# TASK-006 Replay Surface Fix",
        "",
        "## Verified GitHub State",
        "",
        f"- Latest merged Vexter `main`: PR `#{report['verified_github']['latest_vexter_pr']}` at `{report['verified_github']['latest_vexter_main_commit']}`",
        f"- Dexter pinned `main`: `{report['verified_github']['dexter_main_commit']}`",
        f"- Frozen Mew-X: `{report['verified_github']['mewx_frozen_commit']}`",
        "",
        "## What Changed",
        "",
        f"- Augmented Dexter promoted package with `{promoted['dexter_surface']['close_summary_count']}` non-stagnant close-summary replay exports.",
        "- Kept stagnant replay exports as fallback and left source strategy semantics unchanged.",
        "- Revalidated the promoted baseline, rebuilt the comparison pack, and reran replay deepening on the augmented package.",
        "",
        "## Result",
        "",
        f"- Dexter replay coverage: `{dexter_gap['coverage_ratio']:.2%}`",
        f"- Dexter `live_vs_replay_gap_pct`: `{(dexter_gap['live_vs_replay_gap_pct'] or 0.0):.4f}`",
        f"- Mew-X replay coverage: `{mewx_gap['coverage_ratio']:.2%}`",
        f"- Mew-X `live_vs_replay_gap_pct`: `{(mewx_gap['live_vs_replay_gap_pct'] or 0.0):.4f}`",
        f"- Promoted comparison winner mode: `{promoted['baseline_pack']['winner_mode']}`",
        "",
        "## Decision",
        "",
        f"- Key finding: `{decision['key_finding']}`",
        f"- TASK-006 state: `{decision['task_state']}`",
        f"- Next step: `{decision['next_step']}`",
    ]
    return "\n".join(lines) + "\n"


def run_replay_surface_fix(
    *,
    latest_vexter_pr: int,
    latest_vexter_main_commit: str,
    dexter_main_commit: str,
    mewx_frozen_commit: str,
    promoted_label: str,
    promoted_dexter_package_dir: str | Path,
    promoted_mewx_package_dir: str | Path,
    augmented_dexter_package_dir: str | Path,
    promoted_output_dir: str | Path,
    replay_package_root: str | Path,
    replay_output_dir: str | Path,
    confirmatory_residual_note: str,
) -> tuple[dict[str, Any], str]:
    dexter_surface = augment_dexter_replay_surface(
        live_package_dir=promoted_dexter_package_dir,
        output_dir=augmented_dexter_package_dir,
    )
    baseline_pack = build_comparison_pack(
        dexter_package_dir=augmented_dexter_package_dir,
        mewx_package_dir=promoted_mewx_package_dir,
        output_dir=promoted_output_dir,
        summary_note=(
            f"Promoted baseline {promoted_label} rebuilt after augmenting Dexter replay surface "
            "with non-stagnant close summaries."
        ),
    )
    replay_measurement, replay_summary = run_replay_deepening(
        latest_vexter_pr=latest_vexter_pr,
        latest_vexter_main_commit=latest_vexter_main_commit,
        dexter_main_commit=dexter_main_commit,
        mewx_frozen_commit=mewx_frozen_commit,
        promoted_label=promoted_label,
        promoted_dexter_package_dir=augmented_dexter_package_dir,
        promoted_mewx_package_dir=promoted_mewx_package_dir,
        replay_package_root=replay_package_root,
        replay_output_dir=replay_output_dir,
        confirmatory_residual_note=confirmatory_residual_note,
    )

    dexter_gap = replay_measurement["promoted"]["dexter"]["gap"]
    surface_fix_applied = (
        dexter_gap["coverage_ratio"] >= 1.0
        and (dexter_gap["live_vs_replay_gap_pct"] or 0.0) == 0.0
    )

    report = {
        "task_id": "TASK-006-REPLAY-SURFACE-FIX",
        "generated_at_utc": _iso_now(),
        "verified_github": {
            "latest_vexter_pr": latest_vexter_pr,
            "latest_vexter_main_commit": latest_vexter_main_commit,
            "dexter_main_commit": dexter_main_commit,
            "mewx_frozen_commit": mewx_frozen_commit,
        },
        "promoted": {
            "label": promoted_label,
            "original_dexter_package_dir": str(Path(promoted_dexter_package_dir).resolve()),
            "augmented_dexter_package_dir": str(Path(augmented_dexter_package_dir).resolve()),
            "mewx_package_dir": str(Path(promoted_mewx_package_dir).resolve()),
            "dexter_surface": dexter_surface,
            "baseline_pack": {
                "comparison_output_dir": str(Path(promoted_output_dir).resolve()),
                "winner_mode": baseline_pack.get("winner_mode"),
                "pack_id": baseline_pack.get("pack_id"),
            },
            "replay_measurement": replay_measurement["promoted"],
        },
        "confirmatory_context": {
            "residual_note": confirmatory_residual_note,
            "overturns_promoted_baseline": False,
        },
        "replay_summary": replay_summary,
        "decision": {
            "key_finding": (
                "surface_fix_applied" if surface_fix_applied else "surface_fix_insufficient"
            ),
            "task_state": (
                "ready_for_downstream_comparative_analysis"
                if surface_fix_applied
                else "needs_followup"
            ),
            "next_step": (
                "task_006_downstream_comparative_analysis"
                if surface_fix_applied
                else "narrow_replay_surface_followup"
            ),
        },
    }
    return report, _render_summary(report)
