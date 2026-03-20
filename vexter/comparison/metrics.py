"""Metrics derivation for comparison-critical Vexter catalog entries."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any

from .constants import COMPARISON_CRITICAL_METRICS
from .packages import load_run_package, parse_utc_timestamp


def _metric_ok(
    value: Any,
    *,
    unit: str,
    aggregation: str,
    samples: int | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": "ok",
        "value": value,
        "unit": unit,
        "aggregation": aggregation,
    }
    if samples is not None:
        payload["samples"] = samples
    if details:
        payload["details"] = details
    return payload


def _metric_unavailable(reason: str, *, unit: str) -> dict[str, Any]:
    return {
        "status": "unavailable",
        "value": None,
        "unit": unit,
        "reason": reason,
    }


def _to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _event_timestamp_ms(event: dict[str, Any]) -> int | None:
    timestamp = parse_utc_timestamp(event.get("ts_utc"))
    if timestamp is None:
        return None
    return int(timestamp.timestamp() * 1000)


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


def _median_metric(
    values: list[float],
    *,
    unit: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not values:
        return _metric_unavailable("no samples available", unit=unit)
    return _metric_ok(
        float(median(values)),
        unit=unit,
        aggregation="median",
        samples=len(values),
        details=details,
    )


def derive_metrics(package_dir: str | Path) -> dict[str, Any]:
    package = load_run_package(package_dir)
    metadata = package.metadata

    events_by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in package.events:
        event_type = str(event.get("event_type", ""))
        events_by_type[event_type].append(event)

    candidate_events = events_by_type["creator_candidate"]
    attempt_events = events_by_type["entry_attempt"]
    fill_events = events_by_type["entry_fill"]
    close_events = events_by_type["position_closed"]
    signal_events = events_by_type["entry_signal"]
    exit_signal_events = events_by_type["exit_signal"]
    session_update_events = events_by_type["session_update"]
    run_summary_events = events_by_type["run_summary"]

    metrics: dict[str, dict[str, Any]] = {}

    candidate_count = len(candidate_events)
    metrics["candidate_count"] = _metric_ok(
        candidate_count,
        unit="count",
        aggregation="count",
    )

    successful_positions = [
        event
        for event in close_events
        if (_to_float(event["payload"].get("realized_return_pct")) or 0.0) > 0
        or (_to_float(event["payload"].get("mfe_pct")) or 0.0) > 0
    ]
    if candidate_count:
        metrics["candidate_precision_proxy"] = _metric_ok(
            len(successful_positions) / candidate_count,
            unit="ratio",
            aggregation="run_ratio",
            details={
                "successful_positions": len(successful_positions),
                "candidate_count": candidate_count,
            },
        )
    else:
        metrics["candidate_precision_proxy"] = _metric_unavailable(
            "no creator_candidate events were observed",
            unit="ratio",
        )

    if attempt_events:
        metrics["fill_success_rate"] = _metric_ok(
            len(fill_events) / len(attempt_events),
            unit="ratio",
            aggregation="run_ratio",
            details={
                "fills": len(fill_events),
                "attempts": len(attempt_events),
            },
        )
    else:
        metrics["fill_success_rate"] = _metric_unavailable(
            "no entry_attempt events were observed",
            unit="ratio",
        )

    signal_by_session = {_session_key(event): event for event in signal_events}
    attempts_by_session: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in attempt_events:
        attempts_by_session[_session_key(event)].append(event)
    for events in attempts_by_session.values():
        events.sort(key=lambda item: _event_timestamp_ms(item) or 0)

    signal_to_attempt_latencies: list[float] = []
    for session_id, signal_event in signal_by_session.items():
        attempts = attempts_by_session.get(session_id, [])
        if not attempts:
            continue
        signal_ms = _event_timestamp_ms(signal_event)
        attempt_ms = _event_timestamp_ms(attempts[0])
        if signal_ms is not None and attempt_ms is not None and attempt_ms >= signal_ms:
            signal_to_attempt_latencies.append(float(attempt_ms - signal_ms))
            continue
        fallback = _to_float(signal_event["payload"].get("signal_latency_ms"))
        if fallback is not None:
            signal_to_attempt_latencies.append(fallback)
    metrics["signal_to_attempt_latency_ms"] = _median_metric(
        signal_to_attempt_latencies,
        unit="ms",
    )

    attempt_lookup = {
        _attempt_key(event): event
        for event in attempt_events
    }

    attempt_to_fill_latencies: list[float] = []
    quote_vs_fill_slippage: list[float] = []
    for fill_event in fill_events:
        matched_attempt = attempt_lookup.get(_attempt_key(fill_event))
        if matched_attempt is None:
            latency_fallback = _to_float(fill_event["payload"].get("fill_latency_ms"))
            if latency_fallback is not None:
                attempt_to_fill_latencies.append(latency_fallback)
            continue

        attempt_ms = _event_timestamp_ms(matched_attempt)
        fill_ms = _event_timestamp_ms(fill_event)
        if attempt_ms is not None and fill_ms is not None and fill_ms >= attempt_ms:
            attempt_to_fill_latencies.append(float(fill_ms - attempt_ms))
        else:
            latency_fallback = _to_float(fill_event["payload"].get("fill_latency_ms"))
            if latency_fallback is not None:
                attempt_to_fill_latencies.append(latency_fallback)

        quote_price = _to_float(matched_attempt["payload"].get("quote_price"))
        fill_price = _to_float(fill_event["payload"].get("fill_price"))
        if quote_price and fill_price is not None:
            quote_vs_fill_slippage.append(((fill_price - quote_price) / quote_price) * 10000.0)

    metrics["attempt_to_fill_latency_ms"] = _median_metric(
        attempt_to_fill_latencies,
        unit="ms",
    )
    metrics["quote_vs_fill_slippage_bps"] = _median_metric(
        quote_vs_fill_slippage,
        unit="bps",
    )

    max_favorable_excursions: list[float] = []
    max_adverse_excursions: list[float] = []
    time_to_peak_values: list[float] = []
    realized_exit_values: list[float] = []
    realized_vs_peak_gap_values: list[float] = []
    stale_positions = 0

    exit_signal_by_session = {_session_key(event): event for event in exit_signal_events}
    update_mfe_by_session: dict[str, list[float]] = defaultdict(list)
    update_mae_by_session: dict[str, list[float]] = defaultdict(list)
    for event in session_update_events:
        session_id = _session_key(event)
        mfe = _to_float(event["payload"].get("mfe_pct"))
        mae = _to_float(event["payload"].get("mae_pct"))
        if mfe is not None:
            update_mfe_by_session[session_id].append(mfe)
        if mae is not None:
            update_mae_by_session[session_id].append(mae)

    for close_event in close_events:
        payload = close_event["payload"]
        session_id = _session_key(close_event)

        mfe = _to_float(payload.get("mfe_pct"))
        if mfe is None and update_mfe_by_session.get(session_id):
            mfe = max(update_mfe_by_session[session_id])
        if mfe is not None:
            max_favorable_excursions.append(mfe)

        mae = _to_float(payload.get("mae_pct"))
        if mae is None and update_mae_by_session.get(session_id):
            mae = min(update_mae_by_session[session_id])
        if mae is not None:
            max_adverse_excursions.append(mae)

        time_to_peak = _to_float(payload.get("time_to_peak_ms"))
        if time_to_peak is not None:
            time_to_peak_values.append(time_to_peak)

        realized_exit = _to_float(payload.get("realized_return_pct"))
        if realized_exit is not None:
            realized_exit_values.append(realized_exit)

        exit_signal = exit_signal_by_session.get(session_id)
        exit_gap = _to_float(payload.get("realized_vs_peak_gap_pct"))
        if exit_gap is None and exit_signal is not None:
            exit_gap = _to_float(exit_signal["payload"].get("realized_vs_peak_gap_pct"))
        if exit_gap is not None:
            realized_vs_peak_gap_values.append(exit_gap)

        if bool(payload.get("stale_position_flag")):
            stale_positions += 1

    metrics["max_favorable_excursion_pct"] = _median_metric(
        max_favorable_excursions,
        unit="pct",
    )
    metrics["max_adverse_excursion_pct"] = _median_metric(
        max_adverse_excursions,
        unit="pct",
    )
    metrics["time_to_peak_ms"] = _median_metric(
        time_to_peak_values,
        unit="ms",
    )
    metrics["realized_exit_pct"] = _median_metric(
        realized_exit_values,
        unit="pct",
    )
    metrics["realized_vs_peak_gap_pct"] = _median_metric(
        realized_vs_peak_gap_values,
        unit="pct",
    )

    if close_events:
        metrics["stale_position_ratio"] = _metric_ok(
            stale_positions / len(close_events),
            unit="ratio",
            aggregation="run_ratio",
            details={
                "stale_positions": stale_positions,
                "closed_positions": len(close_events),
            },
        )
    else:
        metrics["stale_position_ratio"] = _metric_unavailable(
            "no position_closed events were observed",
            unit="ratio",
        )

    latest_run_summary = run_summary_events[-1]["payload"] if run_summary_events else {}
    replayable_flag = bool(latest_run_summary.get("replayable"))
    proof_manifest = package.proof_manifest
    raw_events = proof_manifest.get("raw_events") or []
    logs = proof_manifest.get("logs") or []
    replays = proof_manifest.get("replays") or []
    db_exports = proof_manifest.get("db_exports") or []

    if replayable_flag and raw_events and logs and replays and db_exports:
        replayability_grade = "full"
    elif replayable_flag or raw_events or logs or replays or db_exports:
        replayability_grade = "partial"
    else:
        replayability_grade = "none"

    metrics["replayability_grade"] = _metric_ok(
        replayability_grade,
        unit="grade",
        aggregation="classification",
        details={
            "replayable_flag": replayable_flag,
            "raw_events": len(raw_events),
            "logs": len(logs),
            "replays": len(replays),
            "db_exports": len(db_exports),
        },
    )

    return {
        "package_dir": str(package.package_dir),
        "run_id": metadata.get("run_id"),
        "source_system": metadata.get("source_system"),
        "derived_metrics": COMPARISON_CRITICAL_METRICS,
        "metrics": metrics,
    }
