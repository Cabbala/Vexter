# comparison-dexter-task005-paper-validation-20260321T1950-vs-mewx-task005-paper-validation-20260321T1950

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `deferred`

## Notes

- Fresh TASK-005 paper validation attempt task005-paper-validation-20260321T1950 used Dexter paper_live against Mew-X sim_live. Dexter remained limited to creator_candidate-only coverage at 1/12 while Mew-X improved to 9/12; this run still included a Dexter startup websocket HTTP 429 in stderr.

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 175 | 0 |
| candidate_precision_proxy | 0 (0.00%) | unavailable |
| fill_success_rate | unavailable | 1 (100.00%) |
| signal_to_attempt_latency_ms | unavailable | 940 ms |
| attempt_to_fill_latency_ms | unavailable | 2 ms |
| quote_vs_fill_slippage_bps | unavailable | 162.9882 bps |
| max_favorable_excursion_pct | unavailable | 0 pct |
| max_adverse_excursion_pct | unavailable | -0.1997 pct |
| time_to_peak_ms | unavailable | 15 ms |
| realized_exit_pct | unavailable | -0.1997 pct |
| realized_vs_peak_gap_pct | unavailable | 0 pct |
| stale_position_ratio | unavailable | 0.6 (60.00%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: deferred until both matched-window packages validate beyond `partial`.
- Evidence still missing: pass-grade live validation, especially fill / exit / run-summary coverage on the matched pair.
- Next task: keep TASK-005 open, collect a fuller comparable matched window, and rerun replay readiness only after that; TASK-006 remains blocked.
