# comparison-dexter-smoke-20260320T193452Z-vs-mewx-smoke-20260320T193850Z

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `derived`

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 57 | 0 |
| candidate_precision_proxy | 0 (0.00%) | unavailable |
| fill_success_rate | unavailable | 1 (100.00%) |
| signal_to_attempt_latency_ms | unavailable | 898 ms |
| attempt_to_fill_latency_ms | unavailable | 1 ms |
| quote_vs_fill_slippage_bps | unavailable | -1197.3549 bps |
| max_favorable_excursion_pct | unavailable | 45.8871 pct |
| max_adverse_excursion_pct | unavailable | 0 pct |
| time_to_peak_ms | unavailable | 14937 ms |
| realized_exit_pct | unavailable | 16.4908 pct |
| realized_vs_peak_gap_pct | unavailable | 25.2349 pct |
| stale_position_ratio | unavailable | 1 (100.00%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: pending live matched-window evidence.
- Evidence still missing: live Dexter and Mew-X run packages gathered from the same measurement window.
- Next task: TASK-005 remains not started.
