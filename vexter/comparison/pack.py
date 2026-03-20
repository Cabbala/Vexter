"""Side-by-side comparison pack builder."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .constants import COMPARISON_MATRIX_ROWS, REPLAYABILITY_RANK
from .metrics import derive_metrics
from .packages import load_run_package
from .validator import validate_run_package


METRIC_LABELS = {
    "candidate_count": "candidate_count",
    "candidate_precision_proxy": "candidate_precision_proxy",
    "candidate_coverage": "candidate_coverage",
    "source_mix": "source_mix",
    "creator_score_distribution": "creator_score_distribution",
    "signal_to_attempt_latency_ms": "signal_to_attempt_latency_ms",
    "attempt_to_fill_latency_ms": "attempt_to_fill_latency_ms",
    "fill_success_rate": "fill_success_rate",
    "quote_vs_fill_slippage_bps": "quote_vs_fill_slippage_bps",
    "entry_reject_reason_rate": "entry_reject_reason_rate",
    "max_favorable_excursion_pct": "max_favorable_excursion_pct",
    "max_adverse_excursion_pct": "max_adverse_excursion_pct",
    "time_to_peak_ms": "time_to_peak_ms",
    "realized_exit_pct": "realized_exit_pct",
    "realized_vs_peak_gap_pct": "realized_vs_peak_gap_pct",
    "stale_position_ratio": "stale_position_ratio",
    "concurrent_positions_max": "concurrent_positions_max",
    "capital_lock_efficiency": "capital_lock_efficiency",
    "token_concurrency_rejects": "token_concurrency_rejects",
    "failure_to_exit_incidence": "failure_to_exit_incidence",
    "replayability_grade": "replayability_grade",
}

METRIC_DIRECTIONS = {
    "candidate_count": "higher",
    "candidate_precision_proxy": "higher",
    "signal_to_attempt_latency_ms": "lower",
    "attempt_to_fill_latency_ms": "lower",
    "fill_success_rate": "higher",
    "quote_vs_fill_slippage_bps": "lower",
    "max_favorable_excursion_pct": "higher",
    "max_adverse_excursion_pct": "contextual_drawdown",
    "time_to_peak_ms": "lower",
    "realized_exit_pct": "higher",
    "realized_vs_peak_gap_pct": "lower",
    "stale_position_ratio": "lower",
    "replayability_grade": "higher_grade",
}

NON_LIVE_EVIDENCE_KINDS = {
    "fixture",
    "fixture_sample",
    "sample",
    "sample_fixture",
}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _metric_value(metric: dict[str, Any] | None) -> Any:
    if not metric or metric.get("status") != "ok":
        return None
    return metric.get("value")


def _requires_winner_deferral(metadata: dict[str, Any]) -> bool:
    evidence_kind = metadata.get("evidence_kind")
    if not isinstance(evidence_kind, str):
        return False
    return evidence_kind.strip().lower() in NON_LIVE_EVIDENCE_KINDS


def _format_metric(metric: dict[str, Any] | None) -> str:
    if not metric:
        return "unavailable"
    if metric.get("status") != "ok":
        return "unavailable"
    value = metric.get("value")
    unit = metric.get("unit")
    if isinstance(value, float):
        text = f"{value:.4f}".rstrip("0").rstrip(".")
    else:
        text = str(value)
    if unit in {"count", "grade"}:
        return text
    if unit == "ratio":
        return f"{text} ({float(value):.2%})"
    return f"{text} {unit}"


def _compare_metric(
    metric_name: str,
    dexter_metric: dict[str, Any] | None,
    mewx_metric: dict[str, Any] | None,
    *,
    defer_winners: bool,
) -> tuple[str, str]:
    if defer_winners:
        return ("pending_live_evidence", "Winner deferred until matched live packages are collected.")

    dexter_value = _metric_value(dexter_metric)
    mewx_value = _metric_value(mewx_metric)
    if dexter_value is None or mewx_value is None:
        return ("pending", "Metric unavailable for one or both sources.")

    direction = METRIC_DIRECTIONS.get(metric_name)
    if direction == "higher":
        if dexter_value == mewx_value:
            return ("tie", "Both sources matched on the derived metric.")
        return ("dexter" if dexter_value > mewx_value else "mewx", "Higher value is treated as better.")
    if direction == "lower":
        if dexter_value == mewx_value:
            return ("tie", "Both sources matched on the derived metric.")
        return ("dexter" if dexter_value < mewx_value else "mewx", "Lower value is treated as better.")
    if direction == "contextual_drawdown":
        if dexter_value == mewx_value:
            return ("tie", "Both sources matched on the derived metric.")
        if dexter_value <= 0 and mewx_value <= 0:
            return (
                "dexter" if dexter_value > mewx_value else "mewx",
                "Values closer to zero are treated as better drawdown outcomes.",
            )
        return (
            "dexter" if dexter_value < mewx_value else "mewx",
            "Smaller adverse excursion is treated as better.",
        )
    if direction == "higher_grade":
        dex_rank = REPLAYABILITY_RANK[str(dexter_value)]
        mew_rank = REPLAYABILITY_RANK[str(mewx_value)]
        if dex_rank == mew_rank:
            return ("tie", "Both sources mapped to the same replayability grade.")
        return (
            "dexter" if dex_rank > mew_rank else "mewx",
            "Higher replayability grade is treated as better.",
        )
    return ("needs_context", "No automatic winner rule is encoded for this metric.")


def _metric_row(
    metric_name: str,
    dexter_metrics: dict[str, dict[str, Any]],
    mewx_metrics: dict[str, dict[str, Any]],
    *,
    defer_winners: bool,
) -> dict[str, Any]:
    dexter_metric = dexter_metrics.get(metric_name)
    mewx_metric = mewx_metrics.get(metric_name)
    winner, note = _compare_metric(
        metric_name,
        dexter_metric,
        mewx_metric,
        defer_winners=defer_winners,
    )
    if dexter_metric is None:
        dexter_metric = {
            "status": "unavailable",
            "value": None,
            "unit": "n/a",
            "reason": "not derived in TASK-004 critical subset",
        }
    if mewx_metric is None:
        mewx_metric = {
            "status": "unavailable",
            "value": None,
            "unit": "n/a",
            "reason": "not derived in TASK-004 critical subset",
        }
    return {
        "metric": metric_name,
        "dexter": dexter_metric,
        "mewx": mewx_metric,
        "winner": winner,
        "notes": note,
    }


def _render_markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _render_matrix_markdown(matrix: dict[str, Any]) -> str:
    parts: list[str] = ["# Comparison Matrix"]

    metadata_rows = [
        [
            "Source commit",
            str(matrix["run_metadata"]["dexter"]["source_commit"]),
            str(matrix["run_metadata"]["mewx"]["source_commit"]),
            "",
        ],
        [
            "Runtime mode",
            str(matrix["run_metadata"]["dexter"]["mode"]),
            str(matrix["run_metadata"]["mewx"]["mode"]),
            "",
        ],
        [
            "Transport mode",
            str(matrix["run_metadata"]["dexter"]["transport_mode"]),
            str(matrix["run_metadata"]["mewx"]["transport_mode"]),
            "",
        ],
        [
            "Measurement window",
            matrix["run_metadata"]["dexter"]["measurement_window"],
            matrix["run_metadata"]["mewx"]["measurement_window"],
            "",
        ],
        [
            "Config snapshot",
            str(matrix["run_metadata"]["dexter"]["config_snapshot"]),
            str(matrix["run_metadata"]["mewx"]["config_snapshot"]),
            "",
        ],
    ]
    parts.append("\n## Run Metadata\n")
    parts.append(_render_markdown_table(["Field", "Dexter", "Mew-X", "Notes"], metadata_rows))

    section_titles = {
        "candidate_generation": "Candidate Generation",
        "entry_execution": "Entry and Execution",
        "session_exit": "Session and Exit",
        "portfolio_operations": "Portfolio and Operations",
    }
    for key, title in section_titles.items():
        parts.append(f"\n## {title}\n")
        rows = [
            [
                item["metric"],
                _format_metric(item["dexter"]),
                _format_metric(item["mewx"]),
                item["winner"],
                item["notes"],
            ]
            for item in matrix[key]
        ]
        parts.append(
            _render_markdown_table(
                ["Metric", "Dexter", "Mew-X", "Winner", "Notes"],
                rows,
            )
        )

    parts.append("\n## Qualitative Findings\n")
    qualitative_rows = [
        [
            "Candidate edge",
            f"candidate_count={_format_metric(matrix['candidate_generation'][0]['dexter'])}; "
            f"candidate_precision_proxy={_format_metric(matrix['candidate_generation'][1]['dexter'])}",
            f"candidate_count={_format_metric(matrix['candidate_generation'][0]['mewx'])}; "
            f"candidate_precision_proxy={_format_metric(matrix['candidate_generation'][1]['mewx'])}",
            "Validate sourcing deltas on matched live windows before naming a winner.",
        ],
        [
            "Execution substrate",
            f"signal_to_attempt={_format_metric(matrix['entry_execution'][0]['dexter'])}; "
            f"fill_success_rate={_format_metric(matrix['entry_execution'][2]['dexter'])}",
            f"signal_to_attempt={_format_metric(matrix['entry_execution'][0]['mewx'])}; "
            f"fill_success_rate={_format_metric(matrix['entry_execution'][2]['mewx'])}",
            "Pair latency and slippage with the same market window before carrying any component forward.",
        ],
        [
            "Exit behavior",
            f"realized_exit={_format_metric(matrix['session_exit'][3]['dexter'])}; "
            f"stale_ratio={_format_metric(matrix['session_exit'][5]['dexter'])}",
            f"realized_exit={_format_metric(matrix['session_exit'][3]['mewx'])}; "
            f"stale_ratio={_format_metric(matrix['session_exit'][5]['mewx'])}",
            "Exit quality stays provisional until live and replay measurements agree.",
        ],
        [
            "Observability gaps",
            matrix["validation"]["dexter"]["classification"],
            matrix["validation"]["mewx"]["classification"],
            "Any partial validation result should block integration work.",
        ],
        [
            "Replay feasibility",
            _format_metric(matrix["portfolio_operations"][-1]["dexter"]),
            _format_metric(matrix["portfolio_operations"][-1]["mewx"]),
            "Replay validation is the gate before TASK-005 begins.",
        ],
    ]
    parts.append(
        _render_markdown_table(
            ["Area", "Dexter", "Mew-X", "Integration Implication"],
            qualitative_rows,
        )
    )
    return "\n".join(parts) + "\n"


def _render_summary_markdown(
    *,
    pack_id: str,
    dexter_validation: dict[str, Any],
    mewx_validation: dict[str, Any],
    dexter_metrics: dict[str, Any],
    mewx_metrics: dict[str, Any],
    summary_note: str | None,
    defer_winners: bool,
) -> str:
    lines = [
        f"# {pack_id}",
        "",
        "## Validation",
        "",
        f"- Dexter readiness: `{dexter_validation['classification']}`",
        f"- Mew-X readiness: `{mewx_validation['classification']}`",
        f"- Winner mode: `{'deferred' if defer_winners else 'derived'}`",
    ]
    if summary_note:
        lines.extend(["", "## Notes", "", f"- {summary_note}"])

    lines.extend(
        [
            "",
            "## Critical Metrics",
            "",
            _render_markdown_table(
                ["Metric", "Dexter", "Mew-X"],
                [
                    [
                        metric_name,
                        _format_metric(dexter_metrics["metrics"].get(metric_name)),
                        _format_metric(mewx_metrics["metrics"].get(metric_name)),
                    ]
                    for metric_name in [
                        "candidate_count",
                        "candidate_precision_proxy",
                        "fill_success_rate",
                        "signal_to_attempt_latency_ms",
                        "attempt_to_fill_latency_ms",
                        "quote_vs_fill_slippage_bps",
                        "max_favorable_excursion_pct",
                        "max_adverse_excursion_pct",
                        "time_to_peak_ms",
                        "realized_exit_pct",
                        "realized_vs_peak_gap_pct",
                        "stale_position_ratio",
                        "replayability_grade",
                    ]
                ],
            ),
            "",
            "## Decision",
            "",
            "- Winning component candidates: pending live matched-window evidence.",
            "- Evidence still missing: live Dexter and Mew-X run packages gathered from the same measurement window.",
            "- Next task: TASK-005 remains not started.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_comparison_pack(
    *,
    dexter_package_dir: str | Path,
    mewx_package_dir: str | Path,
    output_dir: str | Path,
    summary_note: str | None = None,
    defer_winners: bool = False,
) -> dict[str, Any]:
    output_root = Path(output_dir).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    dexter_package = load_run_package(dexter_package_dir)
    mewx_package = load_run_package(mewx_package_dir)
    defer_winners = defer_winners or _requires_winner_deferral(
        dexter_package.metadata
    ) or _requires_winner_deferral(mewx_package.metadata)
    dexter_validation = validate_run_package(dexter_package_dir)
    mewx_validation = validate_run_package(mewx_package_dir)
    dexter_metrics = derive_metrics(dexter_package_dir)
    mewx_metrics = derive_metrics(mewx_package_dir)

    matrix = {
        "run_metadata": {
            "dexter": {
                "source_commit": dexter_package.metadata.get("source_commit"),
                "mode": dexter_package.metadata.get("mode"),
                "transport_mode": dexter_package.metadata.get("transport_mode"),
                "measurement_window": (
                    f"{dexter_package.metadata.get('started_at_utc')} -> "
                    f"{dexter_package.metadata.get('ended_at_utc')}"
                ),
                "config_snapshot": dexter_package.metadata.get("config_snapshot"),
            },
            "mewx": {
                "source_commit": mewx_package.metadata.get("source_commit"),
                "mode": mewx_package.metadata.get("mode"),
                "transport_mode": mewx_package.metadata.get("transport_mode"),
                "measurement_window": (
                    f"{mewx_package.metadata.get('started_at_utc')} -> "
                    f"{mewx_package.metadata.get('ended_at_utc')}"
                ),
                "config_snapshot": mewx_package.metadata.get("config_snapshot"),
            },
        },
        "validation": {
            "dexter": dexter_validation,
            "mewx": mewx_validation,
        },
    }

    for section_key, metrics in COMPARISON_MATRIX_ROWS.items():
        matrix[section_key] = [
            _metric_row(
                metric_name,
                dexter_metrics["metrics"],
                mewx_metrics["metrics"],
                defer_winners=defer_winners,
            )
            for metric_name in metrics
        ]

    pack_id = (
        f"comparison-{dexter_package.metadata.get('run_id')}"
        f"-vs-{mewx_package.metadata.get('run_id')}"
    )
    built_at_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )

    summary_markdown = _render_summary_markdown(
        pack_id=pack_id,
        dexter_validation=dexter_validation,
        mewx_validation=mewx_validation,
        dexter_metrics=dexter_metrics,
        mewx_metrics=mewx_metrics,
        summary_note=summary_note,
        defer_winners=defer_winners,
    )
    matrix_markdown = _render_matrix_markdown(matrix)

    comparison_pack = {
        "pack_id": pack_id,
        "built_at_utc": built_at_utc,
        "winner_mode": "deferred" if defer_winners else "derived",
        "summary_note": summary_note,
        "validation": {
            "dexter": dexter_validation,
            "mewx": mewx_validation,
        },
        "metrics": {
            "dexter": dexter_metrics,
            "mewx": mewx_metrics,
        },
        "comparison_matrix": matrix,
    }

    _write_json(output_root / "dexter_validation.json", dexter_validation)
    _write_json(output_root / "mewx_validation.json", mewx_validation)
    _write_json(output_root / "dexter_metrics.json", dexter_metrics)
    _write_json(output_root / "mewx_metrics.json", mewx_metrics)
    _write_json(output_root / "comparison_matrix.json", matrix)
    _write_json(output_root / "comparison_pack.json", comparison_pack)

    pack_manifest = {
        "pack_id": pack_id,
        "built_at_utc": built_at_utc,
        "inputs": {
            "dexter_package": str(Path(dexter_package_dir).resolve()),
            "mewx_package": str(Path(mewx_package_dir).resolve()),
        },
        "winner_mode": comparison_pack["winner_mode"],
        "outputs": [
            "dexter_validation.json",
            "mewx_validation.json",
            "dexter_metrics.json",
            "mewx_metrics.json",
            "comparison_matrix.json",
            "comparison_matrix.md",
            "comparison_pack.json",
            "summary.md",
        ],
    }
    _write_json(output_root / "pack_manifest.json", pack_manifest)
    (output_root / "summary.md").write_text(summary_markdown)
    (output_root / "comparison_matrix.md").write_text(matrix_markdown)

    return comparison_pack
