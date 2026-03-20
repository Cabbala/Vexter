# Vexter Common Analysis Contract

## Goal
Provide one shared contract so Dexter and Mew-X can be compared before integration.

## Required normalized entities
- creator_candidate
- mint_observed
- entry_signal
- entry_attempt
- entry_fill
- session_update
- exit_signal
- exit_fill
- position_closed
- run_summary

## Required metrics
### Candidate / Universe
- candidate_count
- candidate_precision_proxy
- candidate_freshness
- source_mix
- creator_score_distribution
- top_decile_outcome_concentration

### Entry
- signal_to_attempt_latency_ms
- attempt_to_fill_latency_ms
- fill_success_rate
- quote_vs_fill_slippage_bps
- false_positive_rate_proxy

### Session / Exit
- max_favorable_excursion_pct
- max_adverse_excursion_pct
- realized_vs_peak_gap_pct
- time_to_peak_ms
- stale_position_ratio
- forced_exit_ratio

### Portfolio / Risk
- concurrent_positions_max
- capital_lock_efficiency
- failure_to_exit_incidence
- exposure_concentration
- reserved_balance_utilization

## Artifact format
Each measured run should be exportable into:
- normalized NDJSON or JSONL event stream
- metrics JSON summary
- environment / config snapshot
- human summary markdown
