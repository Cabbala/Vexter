# Comparison Matrix

## Run Metadata

| Field | Dexter | Mew-X | Notes |
| --- | --- | --- | --- |
| Source commit | 69de8b6ca57ca3d03025d85329c88aa4a167da34 | dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a |  |
| Runtime mode | observe_live | observe_live |  |
| Transport mode | ws | grpc |  |
| Measurement window | 2026-03-21T01:00:00Z -> 2026-03-21T01:20:00Z | 2026-03-21T01:00:00Z -> 2026-03-21T01:20:00Z |  |
| Config snapshot | config/config_snapshot.json | config/config_snapshot.json |  |

## Candidate Generation

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| candidate_count | 2 | 3 | pending_live_evidence | Winner deferred until matched live packages are collected. |
| candidate_precision_proxy | 0.5 (50.00%) | 0.6667 (66.67%) | pending_live_evidence | Winner deferred until matched live packages are collected. |
| candidate_coverage | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| source_mix | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| creator_score_distribution | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Entry and Execution

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| signal_to_attempt_latency_ms | 2000 ms | 1000 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| attempt_to_fill_latency_ms | 2000 ms | 1000 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| fill_success_rate | 0.5 (50.00%) | 0.6667 (66.67%) | pending_live_evidence | Winner deferred until matched live packages are collected. |
| quote_vs_fill_slippage_bps | 294.1176 bps | 127.6316 bps | pending_live_evidence | Winner deferred until matched live packages are collected. |
| entry_reject_reason_rate | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Session and Exit

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| max_favorable_excursion_pct | 20 pct | 14.5 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| max_adverse_excursion_pct | -4 pct | -9 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| time_to_peak_ms | 60000 ms | 67500 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| realized_exit_pct | 13.3333 pct | 3.5817 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| realized_vs_peak_gap_pct | 6 pct | 14 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| stale_position_ratio | 0 (0.00%) | 0.5 (50.00%) | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Portfolio and Operations

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| concurrent_positions_max | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| capital_lock_efficiency | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| token_concurrency_rejects | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| failure_to_exit_incidence | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| replayability_grade | full | full | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Qualitative Findings

| Area | Dexter | Mew-X | Integration Implication |
| --- | --- | --- | --- |
| Candidate edge | candidate_count=2; candidate_precision_proxy=0.5 (50.00%) | candidate_count=3; candidate_precision_proxy=0.6667 (66.67%) | Validate sourcing deltas on matched live windows before naming a winner. |
| Execution substrate | signal_to_attempt=2000 ms; fill_success_rate=0.5 (50.00%) | signal_to_attempt=1000 ms; fill_success_rate=0.6667 (66.67%) | Pair latency and slippage with the same market window before carrying any component forward. |
| Exit behavior | realized_exit=13.3333 pct; stale_ratio=0 (0.00%) | realized_exit=3.5817 pct; stale_ratio=0.5 (50.00%) | Exit quality stays provisional until live and replay measurements agree. |
| Observability gaps | pass | pass | Any partial validation result should block integration work. |
| Replay feasibility | full | full | Replay validation stays downstream of matched live comparison closeout. |
