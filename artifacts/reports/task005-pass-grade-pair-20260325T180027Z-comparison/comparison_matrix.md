# Comparison Matrix

## Run Metadata

| Field | Dexter | Mew-X | Notes |
| --- | --- | --- | --- |
| Source commit | ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938 | dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a |  |
| Runtime mode | paper_live | sim_live |  |
| Transport mode | ws | mixed |  |
| Measurement window | 2026-03-25T18:02:11.066878Z -> 2026-03-25T18:05:11.148258Z | 2026-03-25T18:02:11.066878Z -> 2026-03-25T18:05:11.148258Z |  |
| Config snapshot | config/dexter-task005-pass-grade-pair-20260325T180027Z.config.json | config/mewx-task005-pass-grade-pair-20260325T180027Z.config.json |  |

## Candidate Generation

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| candidate_count | 255 | 0 | pending_live_evidence | Winner deferred until matched live packages are collected. |
| candidate_precision_proxy | 0.0157 (1.57%) | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| candidate_coverage | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| source_mix | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| creator_score_distribution | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Entry and Execution

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| signal_to_attempt_latency_ms | 0 ms | 891 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| attempt_to_fill_latency_ms | 502.5 ms | 1.5 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| fill_success_rate | 1 (100.00%) | 1 (100.00%) | pending_live_evidence | Winner deferred until matched live packages are collected. |
| quote_vs_fill_slippage_bps | 0 bps | 7.7061 bps | pending_live_evidence | Winner deferred until matched live packages are collected. |
| entry_reject_reason_rate | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Session and Exit

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| max_favorable_excursion_pct | 34.8443 pct | 6.7929 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| max_adverse_excursion_pct | -6.0547 pct | 0 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| time_to_peak_ms | 5299 ms | 20.5 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| realized_exit_pct | 7.1641 pct | 0 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| realized_vs_peak_gap_pct | 20.533 pct | -0 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| stale_position_ratio | 0 (0.00%) | 1 (100.00%) | pending_live_evidence | Winner deferred until matched live packages are collected. |

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
| Candidate edge | candidate_count=255; candidate_precision_proxy=0.0157 (1.57%) | candidate_count=0; candidate_precision_proxy=unavailable | Validate sourcing deltas on matched live windows before naming a winner. |
| Execution substrate | signal_to_attempt=0 ms; fill_success_rate=1 (100.00%) | signal_to_attempt=891 ms; fill_success_rate=1 (100.00%) | Pair latency and slippage with the same market window before carrying any component forward. |
| Exit behavior | realized_exit=7.1641 pct; stale_ratio=0 (0.00%) | realized_exit=0 pct; stale_ratio=1 (100.00%) | Exit quality stays provisional until live and replay measurements agree. |
| Observability gaps | partial | partial | Any partial validation result should block integration work. |
| Replay feasibility | partial | partial | Replay validation stays downstream of matched live comparison closeout. |
