# comparison-dexter-resume-after-pr8-20260321T0801-vs-mewx-resume-after-pr8-20260321T0801

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `deferred`

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 122 | 0 |
| candidate_precision_proxy | 0 (0.00%) | unavailable |
| fill_success_rate | unavailable | 1 (100.00%) |
| signal_to_attempt_latency_ms | unavailable | 892.5 ms |
| attempt_to_fill_latency_ms | unavailable | 1 ms |
| quote_vs_fill_slippage_bps | unavailable | -1074.5948 bps |
| max_favorable_excursion_pct | unavailable | 32.6073 pct |
| max_adverse_excursion_pct | unavailable | 0 pct |
| time_to_peak_ms | unavailable | 2797 ms |
| realized_exit_pct | unavailable | 32.6073 pct |
| realized_vs_peak_gap_pct | unavailable | 0 pct |
| stale_position_ratio | unavailable | 1 (100.00%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: deferred until both matched-window packages validate beyond `partial`.
- Evidence still missing: pass-grade live validation, especially fill / exit / run-summary coverage on the matched pair.
- Next task: keep TASK-005 open, collect a fuller comparable matched window, and rerun replay readiness only after that; TASK-006 remains blocked.
