# Comparison Matrix

## Run Metadata

| Field | Dexter | Mew-X | Notes |
| --- | --- | --- | --- |
| Source commit | 69de8b6ca57ca3d03025d85329c88aa4a167da34 | dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a |  |
| Runtime mode | observe_live | sim_live |  |
| Transport mode | ws | mixed |  |
| Measurement window | 2026-03-21T08:39:25.571218Z -> 2026-03-21T08:42:25.644005Z | 2026-03-21T08:39:25.571218Z -> 2026-03-21T08:42:25.644005Z |  |
| Config snapshot | config/dexter-resume-after-pr9-20260321T1737.config.json | config/mewx-resume-after-pr9-20260321T1737.config.json |  |

## Candidate Generation

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| candidate_count | 163 | 0 | pending_live_evidence | Winner deferred until matched live packages are collected. |
| candidate_precision_proxy | 0 (0.00%) | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| candidate_coverage | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| source_mix | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |
| creator_score_distribution | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Entry and Execution

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| signal_to_attempt_latency_ms | unavailable | 921.5 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| attempt_to_fill_latency_ms | unavailable | 1 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| fill_success_rate | unavailable | 1 (100.00%) | pending_live_evidence | Winner deferred until matched live packages are collected. |
| quote_vs_fill_slippage_bps | unavailable | -413.031 bps | pending_live_evidence | Winner deferred until matched live packages are collected. |
| entry_reject_reason_rate | unavailable | unavailable | pending_live_evidence | Winner deferred until matched live packages are collected. |

## Session and Exit

| Metric | Dexter | Mew-X | Winner | Notes |
| --- | --- | --- | --- | --- |
| max_favorable_excursion_pct | unavailable | 5.6112 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| max_adverse_excursion_pct | unavailable | 0 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| time_to_peak_ms | unavailable | 14.5 ms | pending_live_evidence | Winner deferred until matched live packages are collected. |
| realized_exit_pct | unavailable | 0 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| realized_vs_peak_gap_pct | unavailable | 0 pct | pending_live_evidence | Winner deferred until matched live packages are collected. |
| stale_position_ratio | unavailable | 1 (100.00%) | pending_live_evidence | Winner deferred until matched live packages are collected. |

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
| Candidate edge | candidate_count=163; candidate_precision_proxy=0 (0.00%) | candidate_count=0; candidate_precision_proxy=unavailable | Validate sourcing deltas on matched live windows before naming a winner. |
| Execution substrate | signal_to_attempt=unavailable; fill_success_rate=unavailable | signal_to_attempt=921.5 ms; fill_success_rate=1 (100.00%) | Pair latency and slippage with the same market window before carrying any component forward. |
| Exit behavior | realized_exit=unavailable; stale_ratio=unavailable | realized_exit=0 pct; stale_ratio=1 (100.00%) | Exit quality stays provisional until live and replay measurements agree. |
| Observability gaps | partial | partial | Any partial validation result should block integration work. |
| Replay feasibility | partial | partial | Replay validation stays downstream of matched live comparison closeout. |
