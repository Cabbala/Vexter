# Metrics Catalog

## Candidate Metrics

| Metric | Event Inputs | Definition | Why It Matters |
| --- | --- | --- | --- |
| `candidate_count` | `creator_candidate` | Total candidates emitted per run | Measures sourcing breadth |
| `candidate_precision_proxy` | `creator_candidate`, `entry_fill`, `position_closed` | Filled candidates that reach positive realized return or positive MFE divided by candidates | First profitability screen |
| `candidate_coverage` | `creator_candidate`, `mint_observed` | Observed mints tied to eligible creators divided by all observed mints in scope | Measures how much of the opportunity set is captured |
| `source_mix` | `creator_candidate` | Distribution of candidate source labels | Shows dependence on one upstream heuristic |
| `source_overlap_ratio` | candidate snapshots from both systems | Shared creator or mint opportunities divided by combined opportunities | Separates unique edge from common overlap |
| `creator_score_distribution` | `creator_candidate` | Percentiles of source-specific candidate score | Detects over-concentration in a narrow score band |

## Entry Metrics

| Metric | Event Inputs | Definition | Why It Matters |
| --- | --- | --- | --- |
| `signal_to_attempt_latency_ms` | `entry_signal`, `entry_attempt` | First attempt time minus signal time | Measures control-plane and routing responsiveness |
| `attempt_to_fill_latency_ms` | `entry_attempt`, `entry_fill` | Fill time minus attempt time | Measures execution quality |
| `signal_to_fill_latency_ms` | `entry_signal`, `entry_fill` | Fill time minus signal time | End-to-end entry latency |
| `fill_success_rate` | `entry_attempt`, `entry_fill` | Filled attempts divided by attempts | Measures practical fillability |
| `quote_vs_fill_slippage_bps` | `entry_attempt`, `entry_fill` | Filled price versus quote price, in basis points | Quantifies entry drag |
| `entry_reject_reason_rate` | `entry_rejected` | Share by reject reason | Shows dominant blockers |
| `migration_before_fill_rate` | `entry_rejected` | Share of entry failures caused by migration or market change | Measures fragility around venue transitions |

## Session Metrics

| Metric | Event Inputs | Definition | Why It Matters |
| --- | --- | --- | --- |
| `max_favorable_excursion_pct` | `session_update`, `position_closed` | Maximum gain from entry price during session | Core upside capture metric |
| `max_adverse_excursion_pct` | `session_update`, `position_closed` | Maximum drawdown from entry price during session | Core downside exposure metric |
| `time_to_peak_ms` | `session_update`, `position_closed` | Time from fill to best price | Helps size hold-time risk |
| `session_duration_ms` | `position_closed` | Time from fill to close | Needed for capital efficiency |
| `dev_sell_latency_ms` | `session_update` | Time from fill to first creator-sold flag | Useful for meme-token risk behavior |
| `stagnation_event_rate` | `session_update`, `exit_signal` | Sessions with inactivity or stagnation conditions divided by closed positions | Measures dead-capital risk |

## Exit Metrics

| Metric | Event Inputs | Definition | Why It Matters |
| --- | --- | --- | --- |
| `realized_exit_pct` | `position_closed` | Realized return at close | Direct profitability number |
| `theoretical_best_exit_pct` | `exit_signal`, `position_closed` | Best achievable return seen during session | Upper bound for execution analysis |
| `realized_vs_peak_gap_pct` | `exit_signal`, `position_closed` | Theoretical best exit minus realized exit | Shows exit quality loss |
| `forced_exit_ratio` | `exit_signal` | Share of exits caused by risk or inactivity gates | Shows how often profit targets are not the driver |
| `stale_position_ratio` | `position_closed` | Closed positions marked stale divided by total closed positions | Measures operational drag |
| `failure_to_exit_incidence` | `exit_signal`, `exit_fill` | Exit signals without a successful fill within SLA | High-severity operational risk |

## Portfolio Metrics

| Metric | Event Inputs | Definition | Why It Matters |
| --- | --- | --- | --- |
| `concurrent_positions_max` | `entry_fill`, `position_closed` | Maximum open positions in a run | Needed for stress testing |
| `capital_lock_efficiency` | `entry_fill`, `position_closed`, balance snapshots | Time-weighted deployed capital divided by reserved or available capital | Shows whether cash is sitting idle |
| `reserved_balance_utilization` | source-specific reservation events | Reserved spend actually converted to fills | Important for Dexter's balance model |
| `token_concurrency_rejects` | `candidate_rejected` | Count of rejects caused by concurrency caps | Shows constraint pressure |
| `exposure_concentration` | `position_closed` | Share of PnL or capital by top creators or sources | Detects fragile dependence |

## Replay and Observability Metrics

| Metric | Event Inputs | Definition | Why It Matters |
| --- | --- | --- | --- |
| `event_completeness_ratio` | exported event stream | Required event types present divided by required event types | Contract compliance |
| `config_attribution_ok` | run metadata | Boolean: commit, config, host, and mode are captured | Required for trustworthy comparisons |
| `replayability_grade` | events plus raw artifacts | `none`, `partial`, or `full` based on reconstructability | Decides whether deeper analysis is possible |
| `live_vs_replay_gap_pct` | matched live and replay runs | Difference between live realized return and replay reconstructed return | Measures how trustworthy replay is |
