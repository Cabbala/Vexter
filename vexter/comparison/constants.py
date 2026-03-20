"""Frozen comparison-analysis contract constants."""

REQUIRED_RUN_IDENTITY_FIELDS = [
    "run_id",
    "source_system",
    "source_commit",
    "mode",
    "transport_mode",
    "host_role",
    "runtime_root",
    "started_at_utc",
    "ended_at_utc",
]

REQUIRED_EVENT_ENVELOPE_FIELDS = [
    "run_id",
    "event_id",
    "event_type",
    "ts_utc",
    "source_system",
    "source_commit",
    "mode",
    "payload",
]

REQUIRED_EVENT_TYPES = [
    "creator_candidate",
    "candidate_rejected",
    "mint_observed",
    "entry_signal",
    "entry_attempt",
    "entry_fill",
    "entry_rejected",
    "session_update",
    "exit_signal",
    "exit_fill",
    "position_closed",
    "run_summary",
]

REQUIRED_EVENT_PAYLOAD_FIELDS = {
    "creator_candidate": [
        "candidate_source",
        "score_components",
        "score_total",
        "cohort_size",
        "reason",
    ],
    "candidate_rejected": [
        "candidate_source",
        "reject_reason",
        "gate_name",
    ],
    "mint_observed": [
        "market",
        "pool_id",
        "first_seen_slot",
        "open_price",
        "is_migrated",
    ],
    "entry_signal": [
        "candidate_source",
        "market",
        "signal_reason",
        "signal_price",
        "signal_slot",
        "signal_latency_ms",
    ],
    "entry_attempt": [
        "attempt_index",
        "market",
        "route",
        "quote_price",
        "expected_tokens_out",
        "slippage_bps",
        "wallet_available_before",
        "tx_strategy",
    ],
    "entry_fill": [
        "attempt_index",
        "fill_price",
        "fill_qty",
        "fill_latency_ms",
        "tx_signature",
        "wallet_balance_after",
    ],
    "entry_rejected": [
        "attempt_index",
        "reject_reason",
    ],
    "session_update": [
        "price",
        "highest_price",
        "buys",
        "sells",
        "liquidity",
        "mfe_pct",
        "mae_pct",
        "state_reason",
    ],
    "exit_signal": [
        "exit_reason",
        "signal_price",
        "theoretical_best_price",
        "realized_vs_peak_gap_pct",
    ],
    "exit_fill": [
        "fill_price",
        "fill_qty",
        "fill_latency_ms",
        "tx_signature",
        "exit_reason",
    ],
    "position_closed": [
        "entry_price",
        "exit_price",
        "realized_return_pct",
        "mfe_pct",
        "mae_pct",
        "time_to_peak_ms",
        "session_duration_ms",
        "stale_position_flag",
    ],
    "run_summary": [
        "candidate_count",
        "entry_attempt_count",
        "entry_fill_count",
        "position_closed_count",
        "event_count",
        "replayable",
    ],
}

SOURCE_REQUIRED_EXPORT_KEYS = {
    "dexter": [
        "leaderboard_snapshot",
        "stagnant_mint_replay",
    ],
    "mewx": [
        "candidate_refresh_snapshot",
        "session_summary",
    ],
}

REQUIRED_PROOF_BUCKETS = [
    "raw_events",
    "logs",
    "replays",
    "db_exports",
    "exports",
]

COMPARISON_CRITICAL_METRICS = [
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

COMPARISON_MATRIX_ROWS = {
    "candidate_generation": [
        "candidate_count",
        "candidate_precision_proxy",
        "candidate_coverage",
        "source_mix",
        "creator_score_distribution",
    ],
    "entry_execution": [
        "signal_to_attempt_latency_ms",
        "attempt_to_fill_latency_ms",
        "fill_success_rate",
        "quote_vs_fill_slippage_bps",
        "entry_reject_reason_rate",
    ],
    "session_exit": [
        "max_favorable_excursion_pct",
        "max_adverse_excursion_pct",
        "time_to_peak_ms",
        "realized_exit_pct",
        "realized_vs_peak_gap_pct",
        "stale_position_ratio",
    ],
    "portfolio_operations": [
        "concurrent_positions_max",
        "capital_lock_efficiency",
        "token_concurrency_rejects",
        "failure_to_exit_incidence",
        "replayability_grade",
    ],
}

REPLAYABILITY_RANK = {
    "none": 0,
    "partial": 1,
    "full": 2,
}
