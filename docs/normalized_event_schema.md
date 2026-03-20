# Normalized Event Schema

## Envelope

Every normalized event is one NDJSON object with this shared envelope:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `run_id` | string | yes | Stable ID for one measured run |
| `event_id` | string | yes | Unique within the run |
| `event_type` | string | yes | One of the types listed below |
| `ts_utc` | string | yes | ISO-8601 UTC timestamp |
| `source_system` | string | yes | `dexter` or `mewx` |
| `source_commit` | string | yes | Git SHA of the measured source repo |
| `mode` | string | yes | `observe_live`, `trade_live`, `sim_live`, or `replay` |
| `transport_mode` | string | no | `ws`, `grpc`, `rpc`, `swqos`, or `mixed` |
| `session_id` | string | no | Required once a position/session exists |
| `mint` | string | no | Required for mint-specific events |
| `creator` | string | no | Required for creator-specific events |
| `payload` | object | yes | Event-specific body |

## Required Event Types

### `creator_candidate`

Emitted when a creator becomes eligible for monitoring or direct entry consideration.

Required payload fields:

- `candidate_source`
- `score_components`
- `score_total`
- `cohort_size`
- `reason`

### `candidate_rejected`

Emitted when a creator or mint is rejected before session start.

Required payload fields:

- `candidate_source`
- `reject_reason`
- `gate_name`

### `mint_observed`

Emitted when a source first notices a mint or pool worth tracking.

Required payload fields:

- `market`
- `pool_id`
- `first_seen_slot`
- `open_price`
- `is_migrated`

### `entry_signal`

Emitted when the strategy decides a mint should be entered.

Required payload fields:

- `candidate_source`
- `market`
- `signal_reason`
- `signal_price`
- `signal_slot`
- `signal_latency_ms`

### `entry_attempt`

Emitted for each outbound entry attempt.

Required payload fields:

- `attempt_index`
- `market`
- `route`
- `quote_price`
- `expected_tokens_out`
- `slippage_bps`
- `wallet_available_before`
- `tx_strategy`

### `entry_fill`

Emitted when an entry attempt resolves to a fill.

Required payload fields:

- `attempt_index`
- `fill_price`
- `fill_qty`
- `fill_latency_ms`
- `tx_signature`
- `wallet_balance_after`

### `entry_rejected`

Emitted when an entry attempt fails or is skipped after signal time.

Required payload fields:

- `attempt_index`
- `reject_reason`
- `tx_signature`

### `session_update`

Emitted on meaningful session-state transitions or periodic checkpoints.

Required payload fields:

- `price`
- `highest_price`
- `buys`
- `sells`
- `liquidity`
- `mfe_pct`
- `mae_pct`
- `state_reason`

Optional but recommended payload fields:

- `creator_token_amount`
- `creator_sold`
- `txns_in_zero`
- `txns_in_n`
- `composite_score`
- `current_target_pct`

### `exit_signal`

Emitted when the strategy decides to exit.

Required payload fields:

- `exit_reason`
- `signal_price`
- `theoretical_best_price`
- `realized_vs_peak_gap_pct`

### `exit_fill`

Emitted when exit execution resolves.

Required payload fields:

- `fill_price`
- `fill_qty`
- `fill_latency_ms`
- `tx_signature`
- `exit_reason`

### `position_closed`

Emitted once the session is fully closed.

Required payload fields:

- `entry_price`
- `exit_price`
- `realized_return_pct`
- `mfe_pct`
- `mae_pct`
- `time_to_peak_ms`
- `session_duration_ms`
- `stale_position_flag`

### `run_summary`

Emitted once per run.

Required payload fields:

- `candidate_count`
- `entry_attempt_count`
- `entry_fill_count`
- `position_closed_count`
- `event_count`
- `replayable`

## Source Mapping Notes

- Dexter should map leaderboard admission to `creator_candidate`, session creation to `entry_signal`, buy submission and fallback resolution to `entry_attempt` and `entry_fill`, and adaptive sell conditions to `exit_signal`.
- Mew-X should map `algo_choose_creators()` output and refresh diffs to `creator_candidate`, session gate rejections to `candidate_rejected`, market subscriptions to `mint_observed`, and `buy()` or `sell()` transport attempts to entry and exit events.

## Replay Minimum

A run is replayable only if the exported events, plus the associated raw logs and DB extracts, are sufficient to reconstruct:

- why a candidate was eligible
- when the entry signal was raised
- what quote and route were attempted
- how session checkpoints evolved
- why exit occurred
