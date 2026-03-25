"""Replay deepening helpers for reconstructing replay-mode evidence."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean
from typing import Any

from .metrics import derive_metrics
from .pack import build_comparison_pack
from .packages import load_run_package, parse_utc_timestamp
from .validator import validate_run_package


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"expected object JSON at {path}")
    return payload


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _write_ndjson(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        for row in rows:
            json.dump(row, handle, sort_keys=True)
            handle.write("\n")


def _copy_file(src: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return str(dest.relative_to(dest.parents[1]).as_posix())


def _copy_package_path(
    package,
    raw_path: str | None,
    fallback_name: str,
    dest_root: Path,
    dest_relative_dir: str,
    *,
    dest_name: str | None = None,
) -> str:
    source_path = package.resolve_relative_path(raw_path or fallback_name)
    filename = dest_name or source_path.name
    destination = dest_root / dest_relative_dir / filename
    return _copy_file(source_path, destination)


def _event_sort_key(event: dict[str, Any]) -> tuple[int, str]:
    ts = parse_utc_timestamp(event.get("ts_utc"))
    ts_value = int(ts.timestamp() * 1000) if ts else 0
    return ts_value, str(event.get("event_type", ""))


def _clone_event(
    event: dict[str, Any],
    *,
    run_id: str,
    mode: str,
) -> dict[str, Any]:
    cloned = json.loads(json.dumps(event))
    cloned["run_id"] = run_id
    cloned["mode"] = mode
    cloned.pop("event_id", None)
    return cloned


def _with_event_id(run_id: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    materialized = []
    for index, row in enumerate(sorted(rows, key=_event_sort_key), start=1):
        enriched = dict(row)
        enriched["event_id"] = f"{run_id}-{index:06d}"
        materialized.append(enriched)
    return materialized


def _session_key(event: dict[str, Any]) -> str:
    return str(
        event.get("session_id")
        or event.get("mint")
        or event.get("event_id")
        or "unknown-session"
    )


def _group_events_by_session(events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        grouped.setdefault(_session_key(event), []).append(event)
    for rows in grouped.values():
        rows.sort(key=_event_sort_key)
    return grouped


def _replay_timestamp(value: str, *, shift_ms: int = 0) -> str:
    ts = parse_utc_timestamp(value)
    if ts is None:
        raise ValueError(f"invalid replay timestamp: {value!r}")
    shifted = ts + timedelta(milliseconds=shift_ms)
    return shifted.replace(microsecond=shifted.microsecond // 1000 * 1000).isoformat().replace(
        "+00:00",
        "Z",
    )


def _return_pct(entry_price: float, exit_price: float) -> float:
    if entry_price == 0:
        return 0.0
    return ((exit_price - entry_price) / entry_price) * 100.0


def _safe_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _price_history_entries(row: dict[str, Any]) -> list[tuple[datetime, float]]:
    raw_history = row.get("price_history")
    if not isinstance(raw_history, str) or not raw_history.strip():
        return []
    payload = json.loads(raw_history)
    if not isinstance(payload, dict):
        return []

    rows: list[tuple[datetime, float]] = []
    for raw_ts, raw_price in payload.items():
        ts = parse_utc_timestamp(datetime.fromtimestamp(float(raw_ts), tz=timezone.utc).isoformat())
        price = _safe_float(raw_price)
        if ts is None or price is None:
            continue
        rows.append((ts, price))
    rows.sort(key=lambda item: item[0])
    return rows


def _dexter_replay_payloads(package) -> dict[str, tuple[Path, dict[str, Any]]]:
    payloads: dict[str, tuple[Path, dict[str, Any]]] = {}
    candidate_paths: list[Path] = []

    replay_dir = package.package_dir / "replays"
    if replay_dir.exists():
        candidate_paths.extend(sorted(replay_dir.glob("*.json")))

    proof_manifest = package.proof_manifest
    for raw_path in proof_manifest.get("replays") or []:
        if not isinstance(raw_path, str):
            continue
        candidate_paths.append(package.resolve_relative_path(raw_path))

    source_exports = package.metadata.get("source_exports", {})
    if isinstance(source_exports, dict):
        raw_path = source_exports.get("stagnant_mint_replay")
        if isinstance(raw_path, str) and raw_path.strip():
            candidate_paths.append(package.resolve_relative_path(raw_path))

    seen: set[Path] = set()
    for candidate_path in candidate_paths:
        if candidate_path in seen or not candidate_path.exists():
            continue
        seen.add(candidate_path)
        payload = _load_json(candidate_path)
        mint_id = payload.get("mint_id")
        if not isinstance(mint_id, str) or not mint_id.strip():
            continue
        payloads[mint_id] = (candidate_path, payload)
    return payloads


def _selected_live_events(live_session_events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        event
        for event in live_session_events
        if str(event.get("event_type", ""))
        in {"mint_observed", "entry_signal", "entry_attempt", "entry_fill"}
    ]


def _with_mint_seed_events(
    *,
    package_events: list[dict[str, Any]],
    live_session_events: list[dict[str, Any]],
    mint: str | None,
) -> list[dict[str, Any]]:
    if not mint:
        return list(live_session_events)

    materialized = list(live_session_events)
    existing_pairs = {
        (str(event.get("event_type")), str(event.get("ts_utc")), str(event.get("mint")))
        for event in materialized
    }
    for event in package_events:
        if str(event.get("event_type")) != "mint_observed":
            continue
        if str(event.get("mint")) != mint:
            continue
        fingerprint = (
            str(event.get("event_type")),
            str(event.get("ts_utc")),
            str(event.get("mint")),
        )
        if fingerprint in existing_pairs:
            continue
        materialized.append(event)
    materialized.sort(key=_event_sort_key)
    return materialized


def _reconstruct_mewx_session_events(
    *,
    live_session_events: list[dict[str, Any]],
    summary_payload: dict[str, Any],
    run_id: str,
) -> list[dict[str, Any]]:
    rows = [_clone_event(event, run_id=run_id, mode="replay") for event in _selected_live_events(live_session_events)]
    if not live_session_events:
        return rows

    seed_event = live_session_events[0]
    mint = seed_event.get("mint")
    creator = seed_event.get("creator")
    session_id = summary_payload.get("session_id") or seed_event.get("session_id")
    closed_at_utc = str(summary_payload["closed_at_utc"])
    entry_price = float(summary_payload["entry_price"])
    exit_price = float(summary_payload["exit_price"])
    mfe_pct = float(summary_payload["mfe_pct"])
    mae_pct = float(summary_payload["mae_pct"])
    realized_return_pct = float(summary_payload["realized_return_pct"])
    session_duration_ms = int(summary_payload["session_duration_ms"])
    time_to_peak_ms = int(summary_payload["time_to_peak_ms"])
    exit_reason = str(summary_payload.get("exit_reason") or "replay_summary")
    candidate_source = summary_payload.get("candidate_source")
    market = str(summary_payload.get("market") or "unknown")
    pool_id = summary_payload.get("pool_id")
    signal_price = entry_price
    theoretical_best_price = entry_price * (1.0 + (mfe_pct / 100.0))

    rows.extend(
        [
            {
                "run_id": run_id,
                "event_type": "session_update",
                "ts_utc": _replay_timestamp(closed_at_utc, shift_ms=-2),
                "source_system": "mewx",
                "source_commit": seed_event["source_commit"],
                "mode": "replay",
                "transport_mode": seed_event.get("transport_mode"),
                "session_id": session_id,
                "mint": mint,
                "creator": creator,
                "payload": {
                    "price": exit_price,
                    "highest_price": theoretical_best_price,
                    "buys": 0,
                    "sells": 0,
                    "liquidity": 0.0,
                    "mfe_pct": mfe_pct,
                    "mae_pct": mae_pct,
                    "state_reason": "replay_summary",
                    "creator_sold": False,
                    "candidate_source": candidate_source,
                },
            },
            {
                "run_id": run_id,
                "event_type": "exit_signal",
                "ts_utc": _replay_timestamp(closed_at_utc, shift_ms=-1),
                "source_system": "mewx",
                "source_commit": seed_event["source_commit"],
                "mode": "replay",
                "transport_mode": seed_event.get("transport_mode"),
                "session_id": session_id,
                "mint": mint,
                "creator": creator,
                "payload": {
                    "exit_reason": exit_reason,
                    "signal_price": signal_price,
                    "theoretical_best_price": theoretical_best_price,
                    "realized_vs_peak_gap_pct": max(mfe_pct - realized_return_pct, 0.0),
                    "market": market,
                    "pool_id": pool_id,
                },
            },
            {
                "run_id": run_id,
                "event_type": "exit_fill",
                "ts_utc": closed_at_utc,
                "source_system": "mewx",
                "source_commit": seed_event["source_commit"],
                "mode": "replay",
                "transport_mode": seed_event.get("transport_mode"),
                "session_id": session_id,
                "mint": mint,
                "creator": creator,
                "payload": {
                    "fill_price": exit_price,
                    "fill_qty": 0.0,
                    "fill_latency_ms": 0,
                    "tx_signature": f"replay-summary-exit:{mint}",
                    "exit_reason": exit_reason,
                    "wallet_balance_after": 0.0,
                },
            },
            {
                "run_id": run_id,
                "event_type": "position_closed",
                "ts_utc": closed_at_utc,
                "source_system": "mewx",
                "source_commit": seed_event["source_commit"],
                "mode": "replay",
                "transport_mode": seed_event.get("transport_mode"),
                "session_id": session_id,
                "mint": mint,
                "creator": creator,
                "payload": {
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "realized_return_pct": realized_return_pct,
                    "mfe_pct": mfe_pct,
                    "mae_pct": mae_pct,
                    "time_to_peak_ms": time_to_peak_ms,
                    "session_duration_ms": session_duration_ms,
                    "stale_position_flag": bool("timeout" in exit_reason),
                },
            },
        ]
    )
    return rows


def _reconstruct_dexter_session_events(
    *,
    live_session_events: list[dict[str, Any]],
    replay_payload: dict[str, Any],
    run_id: str,
) -> list[dict[str, Any]]:
    rows = [_clone_event(event, run_id=run_id, mode="replay") for event in _selected_live_events(live_session_events)]
    if not live_session_events:
        return rows

    seed_event = live_session_events[0]
    replay_row = replay_payload["payload"]["row"]
    history = _price_history_entries(replay_row)
    if not history:
        return rows

    live_entry_fill = next(
        event for event in live_session_events if str(event.get("event_type")) == "entry_fill"
    )
    live_closed = next(
        event for event in live_session_events if str(event.get("event_type")) == "position_closed"
    )
    entry_price = float(live_entry_fill["payload"]["fill_price"])
    session_id = live_entry_fill.get("session_id") or live_closed.get("session_id")
    mint = live_closed.get("mint") or seed_event.get("mint")
    creator = live_closed.get("creator") or seed_event.get("creator")
    source_commit = seed_event["source_commit"]
    transport_mode = seed_event.get("transport_mode")

    entry_ts = parse_utc_timestamp(live_entry_fill["ts_utc"])
    live_entry_ms = int(entry_ts.timestamp() * 1000) if entry_ts else 0
    filtered_history = [
        (timestamp, price)
        for timestamp, price in history
        if int(timestamp.timestamp() * 1000) >= live_entry_ms
    ]
    if not filtered_history:
        filtered_history = history

    highest_price = entry_price
    lowest_price = entry_price
    peak_ts = filtered_history[0][0]
    update_rows: list[dict[str, Any]] = []
    for timestamp, price in filtered_history:
        highest_price = max(highest_price, price)
        if highest_price == price:
            peak_ts = timestamp
        lowest_price = min(lowest_price, price)
        update_rows.append(
            {
                "run_id": run_id,
                "event_type": "session_update",
                "ts_utc": timestamp.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "source_system": "dexter",
                "source_commit": source_commit,
                "mode": "replay",
                "transport_mode": transport_mode,
                "session_id": session_id,
                "mint": mint,
                "creator": creator,
                "payload": {
                    "price": price,
                    "highest_price": highest_price,
                    "buys": 0,
                    "sells": 0,
                    "liquidity": float(replay_row.get("final_market_cap") or 0.0),
                    "mfe_pct": _return_pct(entry_price, highest_price),
                    "mae_pct": _return_pct(entry_price, lowest_price),
                    "state_reason": "replay_price_tick",
                    "creator_sold": False,
                },
            }
        )

    exit_ts, exit_price = filtered_history[-1]
    theoretical_best_price = highest_price
    realized_return_pct = _return_pct(entry_price, exit_price)
    mfe_pct = _return_pct(entry_price, highest_price)
    mae_pct = _return_pct(entry_price, lowest_price)
    session_duration_ms = max(
        int((exit_ts - filtered_history[0][0]).total_seconds() * 1000),
        0,
    )
    time_to_peak_ms = max(int((peak_ts - filtered_history[0][0]).total_seconds() * 1000), 0)
    exit_reason = "replay_terminal_price"

    rows.extend(update_rows)
    rows.extend(
        [
            {
                "run_id": run_id,
                "event_type": "exit_signal",
                "ts_utc": exit_ts.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "source_system": "dexter",
                "source_commit": source_commit,
                "mode": "replay",
                "transport_mode": transport_mode,
                "session_id": session_id,
                "mint": mint,
                "creator": creator,
                "payload": {
                    "exit_reason": exit_reason,
                    "signal_price": exit_price,
                    "theoretical_best_price": theoretical_best_price,
                    "realized_vs_peak_gap_pct": max(mfe_pct - realized_return_pct, 0.0),
                },
            },
            {
                "run_id": run_id,
                "event_type": "exit_fill",
                "ts_utc": exit_ts.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "source_system": "dexter",
                "source_commit": source_commit,
                "mode": "replay",
                "transport_mode": transport_mode,
                "session_id": session_id,
                "mint": mint,
                "creator": creator,
                "payload": {
                    "fill_price": exit_price,
                    "fill_qty": float(live_entry_fill["payload"].get("fill_qty") or 0.0),
                    "fill_latency_ms": 0,
                    "tx_signature": f"replay-terminal-exit:{mint}",
                    "exit_reason": exit_reason,
                    "wallet_balance_after": float(
                        live_closed["payload"].get("wallet_balance_after") or 0.0
                    ),
                },
            },
            {
                "run_id": run_id,
                "event_type": "position_closed",
                "ts_utc": exit_ts.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "source_system": "dexter",
                "source_commit": source_commit,
                "mode": "replay",
                "transport_mode": transport_mode,
                "session_id": session_id,
                "mint": mint,
                "creator": creator,
                "payload": {
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "realized_return_pct": realized_return_pct,
                    "mfe_pct": mfe_pct,
                    "mae_pct": mae_pct,
                    "time_to_peak_ms": time_to_peak_ms,
                    "session_duration_ms": session_duration_ms,
                    "stale_position_flag": True,
                },
            },
        ]
    )
    return rows


def _run_summary_event(
    *,
    run_id: str,
    source_system: str,
    source_commit: str,
    transport_mode: str | None,
    ended_at_utc: str,
    events: list[dict[str, Any]],
    replayable: bool,
) -> dict[str, Any]:
    event_types = [str(event.get("event_type")) for event in events]
    return {
        "run_id": run_id,
        "event_type": "run_summary",
        "ts_utc": ended_at_utc,
        "source_system": source_system,
        "source_commit": source_commit,
        "mode": "replay",
        "transport_mode": transport_mode,
        "payload": {
            "candidate_count": event_types.count("creator_candidate"),
            "entry_attempt_count": event_types.count("entry_attempt"),
            "entry_fill_count": event_types.count("entry_fill"),
            "position_closed_count": event_types.count("position_closed"),
            "event_count": len(events) + 1,
            "replayable": replayable,
        },
    }


def reconstruct_replay_package(
    *,
    live_package_dir: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    package = load_run_package(live_package_dir)
    output_root = Path(output_dir).resolve()
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    source_system = str(package.metadata["source_system"])
    run_id = f"{package.metadata['run_id']}-replay"
    session_groups = _group_events_by_session(package.events)
    base_events = [
        _clone_event(event, run_id=run_id, mode="replay")
        for event in package.events
        if str(event.get("event_type"))
        in {"creator_candidate", "candidate_rejected"}
    ]

    reconstructed_sessions: list[dict[str, Any]] = []
    missing_replay_sessions: list[str] = []
    copied_replay_inputs: list[str] = []
    copied_exports: list[str] = []

    config_path = _copy_package_path(
        package,
        package.metadata.get("config_snapshot"),
        "config/config_snapshot.json",
        output_root,
        "config",
        dest_name="config_snapshot.json",
    )

    raw_event_copy = _copy_file(package.event_stream_path, output_root / "inputs" / "source_events.ndjson")

    if source_system == "mewx":
        snapshot_paths = sorted((package.package_dir / "exports").glob("*.candidates*.json"))
        source_exports = package.metadata.get("source_exports", {})
        if isinstance(source_exports, dict):
            refresh_export = source_exports.get("candidate_refresh_snapshot")
            if isinstance(refresh_export, str) and refresh_export.strip():
                refresh_path = package.resolve_relative_path(refresh_export)
                if refresh_path not in snapshot_paths and refresh_path.exists():
                    snapshot_paths.append(refresh_path)
        for snapshot_path in snapshot_paths:
            copied_exports.append(
                _copy_file(snapshot_path, output_root / "exports" / snapshot_path.name)
            )

        for export_path in sorted((package.package_dir / "exports").glob("*.json")):
            payload = _load_json(export_path)
            if "session_id" not in payload or "realized_return_pct" not in payload:
                if export_path.name.endswith(".state.json"):
                    copied_exports.append(_copy_file(export_path, output_root / "exports" / export_path.name))
                continue
            session_id = str(payload["session_id"])
            live_session_events = session_groups.get(session_id, [])
            live_session_events = _with_mint_seed_events(
                package_events=package.events,
                live_session_events=live_session_events,
                mint=str(payload.get("mint") or ""),
            )
            if not live_session_events:
                missing_replay_sessions.append(session_id)
                continue
            copied_replay_inputs.append(
                _copy_file(export_path, output_root / "exports" / export_path.name)
            )
            reconstructed_sessions.extend(
                _reconstruct_mewx_session_events(
                    live_session_events=live_session_events,
                    summary_payload=payload,
                    run_id=run_id,
                )
            )
        replayable = bool(reconstructed_sessions) and not missing_replay_sessions
    elif source_system == "dexter":
        leaderboard_export = package.metadata.get("source_exports", {}).get(
            "leaderboard_snapshot"
        )
        if isinstance(leaderboard_export, str):
            copied_exports.append(
                _copy_package_path(
                    package,
                    leaderboard_export,
                    leaderboard_export,
                    output_root,
                    "exports",
                    dest_name="leaderboard_snapshot.json",
                )
            )

        replay_payloads = _dexter_replay_payloads(package)
        traded_sessions = [
            events
            for events in session_groups.values()
            if any(str(event.get("event_type")) == "position_closed" for event in events)
        ]
        for live_session_events in traded_sessions:
            live_closed = next(
                event
                for event in live_session_events
                if str(event.get("event_type")) == "position_closed"
            )
            mint = str(live_closed.get("mint"))
            live_session_events = _with_mint_seed_events(
                package_events=package.events,
                live_session_events=live_session_events,
                mint=mint,
            )
            replay_payload_item = replay_payloads.get(mint)
            if replay_payload_item is None:
                missing_replay_sessions.append(str(live_closed.get("session_id") or mint))
                continue
            replay_path, replay_payload = replay_payload_item
            copied_replay_inputs.append(
                _copy_file(replay_path, output_root / "replays" / replay_path.name)
            )
            reconstructed_sessions.extend(
                _reconstruct_dexter_session_events(
                    live_session_events=live_session_events,
                    replay_payload=replay_payload,
                    run_id=run_id,
                )
            )
        replayable = not missing_replay_sessions
    else:
        raise ValueError(f"unsupported source_system: {source_system}")

    event_rows = _with_event_id(run_id, base_events + reconstructed_sessions)
    replay_event_ended_at_utc = (
        event_rows[-1]["ts_utc"] if event_rows else str(package.metadata["ended_at_utc"])
    )

    event_rows.append(
        {
            **_run_summary_event(
            run_id=run_id,
            source_system=source_system,
            source_commit=str(package.metadata["source_commit"]),
            transport_mode=package.metadata.get("transport_mode"),
            ended_at_utc=replay_event_ended_at_utc,
            events=event_rows,
            replayable=replayable,
        ),
            "event_id": f"{run_id}-{len(event_rows) + 1:06d}",
        }
    )

    started_at_utc = str(package.metadata["started_at_utc"])
    ended_at_utc = str(package.metadata["ended_at_utc"])
    state_payload = {
        "run_id": run_id,
        "source_system": source_system,
        "source_commit": package.metadata["source_commit"],
        "mode": "replay",
        "transport_mode": package.metadata["transport_mode"],
        "host_role": package.metadata["host_role"],
        "started_at_utc": started_at_utc,
        "ended_at_utc": ended_at_utc,
        "status": "completed",
        "event_counts": {
            event_type: sum(
                1 for event in event_rows if str(event.get("event_type")) == event_type
            )
            for event_type in {
                str(event.get("event_type")) for event in event_rows
            }
        },
    }
    state_path = output_root / "exports" / f"{run_id}.state.json"
    _write_json(state_path, state_payload)
    state_relative = str(state_path.relative_to(output_root).as_posix())
    if state_relative not in copied_exports:
        copied_exports.append(state_relative)

    metadata = {
        "run_id": run_id,
        "source_system": source_system,
        "source_commit": package.metadata["source_commit"],
        "mode": "replay",
        "transport_mode": package.metadata["transport_mode"],
        "host_role": package.metadata["host_role"],
        "runtime_root": package.metadata["runtime_root"],
        "started_at_utc": started_at_utc,
        "ended_at_utc": ended_at_utc,
        "event_stream": "events.ndjson",
        "config_snapshot": config_path,
        "proof_manifest": "proof_manifest.json",
        "reconstructed_at_utc": _iso_now(),
        "reconstructed_from_run_id": package.metadata["run_id"],
        "reconstructed_from_package_dir": str(package.package_dir),
        "source_exports": {},
    }

    if source_system == "dexter":
        metadata["source_exports"] = {
            "leaderboard_snapshot": "exports/leaderboard_snapshot.json",
            "stagnant_mint_replay": copied_replay_inputs[0] if copied_replay_inputs else "",
        }
    else:
        refresh_candidates = [
            path
            for path in copied_exports
            if "refresh" in Path(path).name.lower() or "candidate_refresh" in Path(path).name.lower()
        ]
        metadata["source_exports"] = {
            "candidate_refresh_snapshot": refresh_candidates[0] if refresh_candidates else "",
            "session_summary": copied_replay_inputs[0] if copied_replay_inputs else "",
        }

    proof_manifest = {
        "raw_events": [raw_event_copy],
        "logs": [],
        "replays": copied_replay_inputs,
        "db_exports": copied_replay_inputs,
        "exports": sorted(copied_exports),
        "config": [config_path],
    }

    _write_json(output_root / "run_metadata.json", metadata)
    _write_ndjson(output_root / "events.ndjson", event_rows)
    _write_json(output_root / "proof_manifest.json", proof_manifest)

    validation = validate_run_package(output_root)
    metrics = derive_metrics(output_root)
    reconstructed_keys = sorted(
        {
            str(event.get("session_id") or event.get("mint"))
            for event in event_rows
            if str(event.get("event_type")) == "position_closed"
        }
    )
    live_position_closed = [
        event for event in package.events if str(event.get("event_type")) == "position_closed"
    ]

    return {
        "package_dir": str(output_root),
        "source_system": source_system,
        "run_id": run_id,
        "validation": validation,
        "metrics": metrics,
        "reconstructed_session_keys": reconstructed_keys,
        "live_position_closed_count": len(live_position_closed),
        "reconstructed_position_closed_count": len(reconstructed_keys),
        "coverage_ratio": (
            len(reconstructed_keys) / len(live_position_closed) if live_position_closed else 0.0
        ),
        "missing_replay_sessions": sorted(missing_replay_sessions),
        "used_replay_inputs": copied_replay_inputs,
    }


def _closed_positions_by_key(package_dir: str | Path) -> dict[str, dict[str, Any]]:
    package = load_run_package(package_dir)
    rows: dict[str, dict[str, Any]] = {}
    for event in package.events:
        if str(event.get("event_type")) != "position_closed":
            continue
        rows[_session_key(event)] = event
    return rows


def measure_live_vs_replay_gap(
    *,
    live_package_dir: str | Path,
    replay_package_dir: str | Path,
) -> dict[str, Any]:
    live_positions = _closed_positions_by_key(live_package_dir)
    replay_positions = _closed_positions_by_key(replay_package_dir)
    matched_keys = sorted(set(live_positions) & set(replay_positions))

    per_session: list[dict[str, Any]] = []
    for key in matched_keys:
        live_event = live_positions[key]
        replay_event = replay_positions[key]
        live_return = float(live_event["payload"]["realized_return_pct"])
        replay_return = float(replay_event["payload"]["realized_return_pct"])
        gap_pct = replay_return - live_return
        per_session.append(
            {
                "session_key": key,
                "mint": live_event.get("mint"),
                "creator": live_event.get("creator"),
                "live_realized_return_pct": live_return,
                "replay_realized_return_pct": replay_return,
                "gap_pct": gap_pct,
                "abs_gap_pct": abs(gap_pct),
            }
        )

    gap_measured = bool(per_session)
    abs_gaps = [row["abs_gap_pct"] for row in per_session]
    live_vs_replay_gap_pct = mean(abs_gaps) if abs_gaps else None

    return {
        "gap_measured": gap_measured,
        "live_position_closed_count": len(live_positions),
        "replay_position_closed_count": len(replay_positions),
        "matched_position_closed_count": len(matched_keys),
        "coverage_ratio": (len(matched_keys) / len(live_positions)) if live_positions else 0.0,
        "live_vs_replay_gap_pct": live_vs_replay_gap_pct,
        "max_abs_gap_pct": max(abs_gaps) if abs_gaps else None,
        "unmatched_live_session_keys": sorted(set(live_positions) - set(replay_positions)),
        "unmatched_replay_session_keys": sorted(set(replay_positions) - set(live_positions)),
        "per_session": per_session,
    }


def _render_summary(report: dict[str, Any]) -> str:
    promoted = report["promoted"]
    replay_pack = report["replay_pack"]
    decision = report["decision"]
    confirmatory = report["confirmatory_context"]

    lines = [
        "# TASK-006 Replay Deepening",
        "",
        "## GitHub Basis",
        "",
        f"- Latest merged Vexter main: PR `#{report['verified_github']['latest_vexter_pr']}` commit `{report['verified_github']['latest_vexter_main_commit']}`",
        f"- Dexter main: PR `#3` commit `{report['verified_github']['dexter_main_commit']}`",
        f"- Frozen Mew-X: `{report['verified_github']['mewx_frozen_commit']}`",
        "",
        "## Promoted Baseline",
        "",
        f"- Label: `{promoted['label']}`",
        f"- Accepted replay input: `{'yes' if promoted['accepted_as_replay_input'] else 'no'}`",
        f"- Confirmatory note only: `{confirmatory['residual_note']}`",
        "",
        "## Replay Reconstruction",
        "",
        f"- Dexter replay package: `{promoted['dexter']['replay_package']['validation']['classification']}` with coverage `{promoted['dexter']['gap']['coverage_ratio']:.2%}`",
        f"- Dexter live-vs-replay gap: `{_format_optional_pct(promoted['dexter']['gap']['live_vs_replay_gap_pct'])}`",
        f"- Mew-X replay package: `{promoted['mewx']['replay_package']['validation']['classification']}` with coverage `{promoted['mewx']['gap']['coverage_ratio']:.2%}`",
        f"- Mew-X live-vs-replay gap: `{_format_optional_pct(promoted['mewx']['gap']['live_vs_replay_gap_pct'])}`",
        f"- Replay comparison pack winner mode: `{replay_pack['winner_mode']}`",
        "",
        "## Decision",
        "",
        f"- Key finding: `{decision['key_finding']}`",
        f"- TASK-006 state: `{decision['task_state']}`",
        f"- Next step: `{decision['next_step']}`",
    ]
    return "\n".join(lines) + "\n"


def _format_optional_pct(value: float | None) -> str:
    if value is None:
        return "unmeasured"
    return f"{value:.4f} pct"


def run_replay_deepening(
    *,
    latest_vexter_pr: int,
    latest_vexter_main_commit: str,
    dexter_main_commit: str,
    mewx_frozen_commit: str,
    promoted_label: str,
    promoted_dexter_package_dir: str | Path,
    promoted_mewx_package_dir: str | Path,
    replay_package_root: str | Path,
    replay_output_dir: str | Path,
    confirmatory_residual_note: str,
) -> tuple[dict[str, Any], str]:
    replay_root = Path(replay_package_root).resolve()
    dexter_replay_dir = replay_root / "dexter-replay"
    mewx_replay_dir = replay_root / "mewx-replay"

    dexter_replay = reconstruct_replay_package(
        live_package_dir=promoted_dexter_package_dir,
        output_dir=dexter_replay_dir,
    )
    mewx_replay = reconstruct_replay_package(
        live_package_dir=promoted_mewx_package_dir,
        output_dir=mewx_replay_dir,
    )

    replay_pack = build_comparison_pack(
        dexter_package_dir=dexter_replay_dir,
        mewx_package_dir=mewx_replay_dir,
        output_dir=replay_output_dir,
        summary_note=(
            f"Replay-mode comparison reconstructed from promoted baseline {promoted_label}."
        ),
    )

    dexter_gap = measure_live_vs_replay_gap(
        live_package_dir=promoted_dexter_package_dir,
        replay_package_dir=dexter_replay_dir,
    )
    mewx_gap = measure_live_vs_replay_gap(
        live_package_dir=promoted_mewx_package_dir,
        replay_package_dir=mewx_replay_dir,
    )

    gap_measured = dexter_gap["gap_measured"] or mewx_gap["gap_measured"]
    task_state = "ready_for_next_replay_analysis_step" if gap_measured else "blocked"
    next_step = "task_006_replay_analysis" if gap_measured else "repair_replay_surface"

    report = {
        "task_id": "TASK-006-REPLAY-DEEPENING",
        "generated_at_utc": _iso_now(),
        "verified_github": {
            "latest_vexter_pr": latest_vexter_pr,
            "latest_vexter_main_commit": latest_vexter_main_commit,
            "dexter_main_commit": dexter_main_commit,
            "mewx_frozen_commit": mewx_frozen_commit,
        },
        "promoted": {
            "label": promoted_label,
            "accepted_as_replay_input": True,
            "dexter": {
                "live_package_dir": str(Path(promoted_dexter_package_dir).resolve()),
                "replay_package": dexter_replay,
                "gap": dexter_gap,
            },
            "mewx": {
                "live_package_dir": str(Path(promoted_mewx_package_dir).resolve()),
                "replay_package": mewx_replay,
                "gap": mewx_gap,
            },
        },
        "confirmatory_context": {
            "residual_note": confirmatory_residual_note,
            "overturns_promoted_baseline": False,
        },
        "replay_pack": {
            "comparison_output_dir": str(Path(replay_output_dir).resolve()),
            "winner_mode": replay_pack.get("winner_mode"),
            "pack_id": replay_pack.get("pack_id"),
        },
        "decision": {
            "key_finding": "gap_measured" if gap_measured else "replay_blocker_found",
            "task_state": task_state,
            "next_step": next_step,
        },
    }
    return report, _render_summary(report)
