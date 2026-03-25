# Comparison Matrix

## Run Metadata

| Field | Dexter | Mew-X | Notes |
| --- | --- | --- | --- |
| Source commit | ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938 | dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a |  |
| Runtime mode | replay | replay |  |
| Transport mode | ws | mixed |  |
| Measurement window | 2026-03-25T18:02:11.066878Z -> 2026-03-25T18:05:11.148258Z | 2026-03-25T18:02:11.066878Z -> 2026-03-25T18:05:11.148258Z |  |
| Config snapshot | config/config_snapshot.json | config/config_snapshot.json |  |

## Candidate Generation

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| candidate_count | 255 | 0 | dexter | Higher value is treated as better. |
| candidate_precision_proxy | 0.0078 (0.78%) | unavailable | pending | Metric unavailable for one or both sources. |
| candidate_coverage | unavailable | unavailable | pending | Metric unavailable for one or both sources. |
| source_mix | unavailable | unavailable | pending | Metric unavailable for one or both sources. |
| creator_score_distribution | unavailable | unavailable | pending | Metric unavailable for one or both sources. |

## Entry and Execution

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| signal_to_attempt_latency_ms | 0 ms | 891 ms | dexter | Lower value is treated as better. |
| attempt_to_fill_latency_ms | 770 ms | 1.5 ms | mewx | Lower value is treated as better. |
| fill_success_rate | 1 (100.00%) | 1 (100.00%) | tie | Both sources matched on the derived metric. |
| quote_vs_fill_slippage_bps | 0 bps | 7.7061 bps | dexter | Lower value is treated as better. |
| entry_reject_reason_rate | unavailable | unavailable | pending | Metric unavailable for one or both sources. |

## Session and Exit

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| max_favorable_excursion_pct | 22.4009 pct | 6.7929 pct | dexter | Higher value is treated as better. |
| max_adverse_excursion_pct | -26.424 pct | 0 pct | mewx | Values closer to zero are treated as better drawdown outcomes. |
| time_to_peak_ms | 0 ms | 20.5 ms | dexter | Lower value is treated as better. |
| realized_exit_pct | -26.424 pct | 0 pct | mewx | Higher value is treated as better. |
| realized_vs_peak_gap_pct | 48.9315 pct | 0 pct | mewx | Lower value is treated as better. |
| stale_position_ratio | 1 (100.00%) | 1 (100.00%) | tie | Both sources matched on the derived metric. |

## Portfolio and Operations

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| concurrent_positions_max | unavailable | unavailable | pending | Metric unavailable for one or both sources. |
| capital_lock_efficiency | unavailable | unavailable | pending | Metric unavailable for one or both sources. |
| token_concurrency_rejects | unavailable | unavailable | pending | Metric unavailable for one or both sources. |
| failure_to_exit_incidence | unavailable | unavailable | pending | Metric unavailable for one or both sources. |
| replayability_grade | partial | partial | tie | Both sources mapped to the same replayability grade. |

## Qualitative Findings

| Area | Dexter | Mew-X | Integration Implication |
| --- | --- | --- | --- |
| Candidate edge | candidate_count=255; candidate_precision_proxy=0.0078 (0.78%) | candidate_count=0; candidate_precision_proxy=unavailable | Validate sourcing deltas on matched live windows before naming a winner. |
| Execution substrate | signal_to_attempt=0 ms; fill_success_rate=1 (100.00%) | signal_to_attempt=891 ms; fill_success_rate=1 (100.00%) | Pair latency and slippage with the same market window before carrying any component forward. |
| Exit behavior | realized_exit=-26.424 pct; stale_ratio=1 (100.00%) | realized_exit=0 pct; stale_ratio=1 (100.00%) | Exit quality stays provisional until live and replay measurements agree. |
| Observability gaps | pass | pass | Any partial validation result should block integration work. |
| Replay feasibility | partial | partial | Replay validation stays downstream of matched live comparison closeout. |
