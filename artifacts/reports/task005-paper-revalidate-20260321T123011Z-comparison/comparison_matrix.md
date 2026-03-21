# Comparison Matrix

## Run Metadata

| Field | Dexter | Mew-X | Notes |
| --- | --- | --- | --- |
| Source commit | ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938 | dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a |  |
| Runtime mode | paper_live | sim_live |  |
| Transport mode | ws | mixed |  |
| Measurement window | 2026-03-21T12:32:30.070774Z -> 2026-03-21T12:34:30.127310Z | 2026-03-21T12:32:30.070774Z -> 2026-03-21T12:34:30.127310Z |  |
| Config snapshot | config/dexter-task005-paper-revalidate-20260321T123011Z.config.json | config/mewx-task005-paper-revalidate-20260321T123011Z.config.json |  |

## Candidate Generation

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| candidate_count | 208 | 0 | pending_live_evidence | Winner deferred until matched live packages are collected. |
| candidate_precision_proxy | 0.0096 (0.96%) | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| candidate_coverage | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| source_mix | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| creator_score_distribution | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Entry and Execution

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| signal_to_attempt_latency_ms | 0 ms | 963.5 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| attempt_to_fill_latency_ms | 553.5 ms | 2 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| fill_success_rate | 1 (100.00%) | 1 (100.00%) | pending_live_evidence | Winner deferred until matched live packages are collected. |
| quote_vs_fill_slippage_bps | 0 bps | -755.3364 bps | pending_live_evidence | Winner deferred until matched live packages are collected. |
| entry_reject_reason_rate | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Session and Exit

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| max_favorable_excursion_pct | 15.2663 pct | 25.3429 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| max_adverse_excursion_pct | -17.8535 pct | 0 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| time_to_peak_ms | 17197 ms | 1504 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| realized_exit_pct | -5.5282 pct | 25.3429 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| realized_vs_peak_gap_pct | 32.3434 pct | 0 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| stale_position_ratio | 0.5 (50.00%) | 1 (100.00%) | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Portfolio and Operations

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| concurrent_positions_max | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| capital_lock_efficiency | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| token_concurrency_rejects | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| failure_to_exit_incidence | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| replayability_grade | partial | partial | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Qualitative Findings

| Area | Dexter | Mew-X | Integration Implication |
| --- | --- | --- | --- |
| Candidate edge | candidate_count=208; candidate_precision_proxy=0.0096 (0.96%) | candidate_count=0; candidate_precision_proxy=unavailable | Validate sourcing deltas on matched live windows before naming a winner. |
| Execution substrate | signal_to_attempt=0 ms; fill_success_rate=1 (100.00%) | signal_to_attempt=963.5 ms; fill_success_rate=1 (100.00%) | Pair latency and slippage with the same market window before carrying any component forward. |
| Exit behavior | realized_exit=-5.5282 pct; stale_ratio=0.5 (50.00%) | realized_exit=25.3429 pct; stale_ratio=1 (100.00%) | Exit quality stays provisional until live and replay measurements agree. |
| Observability gaps | partial | partial | Any partial validation result should block integration work. |
| Replay feasibility | partial | partial | Replay validation stays downstream of matched live comparison closeout. |
