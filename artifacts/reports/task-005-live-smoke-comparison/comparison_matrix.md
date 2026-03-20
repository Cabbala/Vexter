# Comparison Matrix

## Run Metadata

| Field | Dexter | Mew-X | Notes |
| --- | --- | --- | --- |
| Source commit | 69de8b6ca57ca3d03025d85329c88aa4a167da34 | dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a |  |
| Runtime mode | observe_live | sim_live |  |
| Transport mode | ws | mixed |  |
| Measurement window | 2026-03-20T19:35:54.840946Z -> 2026-03-20T19:37:22.502765Z | 2026-03-20T19:39:07.814Z -> 2026-03-20T19:39:28.769Z |  |
| Config snapshot | config/dexter-smoke-20260320T193452Z.config.json | config/mewx-smoke-20260320T193850Z.config.json |  |

## Candidate Generation

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| candidate_count | 57 | 0 | dexter | Higher value is treated as better. |
| candidate_precision_proxy | 0 (0.00%) | unavailable | pending | Metric unavailable for one or both sources. |
| candidate_coverage | unavailable | unavailable | pending | Metric unavailable for one or both sources. |
| source_mix | unavailable | unavailable | pending | Metric unavailable for one or both sources. |
| creator_score_distribution | unavailable | unavailable | pending | Metric unavailable for one or both sources. |

## Entry and Execution

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| signal_to_attempt_latency_ms | unavailable | 898 ms | pending | Metric unavailable for one or both sources. |
| attempt_to_fill_latency_ms | unavailable | 1 ms | pending | Metric unavailable for one or both sources. |
| fill_success_rate | unavailable | 1 (100.00%) | pending | Metric unavailable for one or both sources. |
| quote_vs_fill_slippage_bps | unavailable | -1197.3549 bps | pending | Metric unavailable for one or both sources. |
| entry_reject_reason_rate | unavailable | unavailable | pending | Metric unavailable for one or both sources. |

## Session and Exit

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| max_favorable_excursion_pct | unavailable | 45.8871 pct | pending | Metric unavailable for one or both sources. |
| max_adverse_excursion_pct | unavailable | 0 pct | pending | Metric unavailable for one or both sources. |
| time_to_peak_ms | unavailable | 14937 ms | pending | Metric unavailable for one or both sources. |
| realized_exit_pct | unavailable | 16.4908 pct | pending | Metric unavailable for one or both sources. |
| realized_vs_peak_gap_pct | unavailable | 25.2349 pct | pending | Metric unavailable for one or both sources. |
| stale_position_ratio | unavailable | 1 (100.00%) | pending | Metric unavailable for one or both sources. |

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
| Candidate edge | candidate_count=57; candidate_precision_proxy=0 (0.00%) | candidate_count=0; candidate_precision_proxy=unavailable | Validate sourcing deltas on matched live windows before naming a winner. |
| Execution substrate | signal_to_attempt=unavailable; fill_success_rate=unavailable | signal_to_attempt=898 ms; fill_success_rate=1 (100.00%) | Pair latency and slippage with the same market window before carrying any component forward. |
| Exit behavior | realized_exit=unavailable; stale_ratio=unavailable | realized_exit=16.4908 pct; stale_ratio=1 (100.00%) | Exit quality stays provisional until live and replay measurements agree. |
| Observability gaps | partial | partial | Any partial validation result should block integration work. |
| Replay feasibility | partial | partial | Replay validation is the gate before TASK-005 begins. |
