# comparison-dexter-task005-paper-validation-20260321T2005-vs-mewx-task005-paper-validation-20260321T2005

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `deferred`

## Notes

- Confirmatory TASK-005 paper validation retry task005-paper-validation-20260321T2005 increased Dexter startup serialization and removed main-runtime HTTP 429, but Dexter still emitted only creator_candidate events in paper_live and stayed at 1/12 while Mew-X sim_live validated 8/12.

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 181 | 0 |
| candidate_precision_proxy | 0 (0.00%) | unavailable |
| fill_success_rate | unavailable | 1 (100.00%) |
| signal_to_attempt_latency_ms | unavailable | 913.5 ms |
| attempt_to_fill_latency_ms | unavailable | 2 ms |
| quote_vs_fill_slippage_bps | unavailable | -220.7053 bps |
| max_favorable_excursion_pct | unavailable | 2.3924 pct |
| max_adverse_excursion_pct | unavailable | 0 pct |
| time_to_peak_ms | unavailable | 9 ms |
| realized_exit_pct | unavailable | 0 pct |
| realized_vs_peak_gap_pct | unavailable | 0 pct |
| stale_position_ratio | unavailable | 0.8333 (83.33%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: deferred until both matched-window packages validate beyond `partial`.
- Evidence still missing: pass-grade live validation, especially fill / exit / run-summary coverage on the matched pair.
- Next task: keep TASK-005 open, collect a fuller comparable matched window, and rerun replay readiness only after that; TASK-006 remains blocked.
