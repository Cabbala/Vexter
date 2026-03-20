# comparison-dexter-pass-20260320T205803Z-vs-mewx-pass-20260320T205803Z

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `deferred`

## Notes

- Safe-mode retry kept both frozen sources running concurrently from 2026-03-20T20:58:40.760Z to 2026-03-20T21:01:52.838Z, with exact event overlap from 2026-03-20T20:59:55.254Z to 2026-03-20T21:01:52.838Z. Dexter remained zero-balance observe-only while Mew-X sim reached nine required event types.

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 0 | 0 |
| candidate_precision_proxy | unavailable | unavailable |
| fill_success_rate | unavailable | 1 (100.00%) |
| signal_to_attempt_latency_ms | unavailable | 896 ms |
| attempt_to_fill_latency_ms | unavailable | 1 ms |
| quote_vs_fill_slippage_bps | unavailable | 0 bps |
| max_favorable_excursion_pct | unavailable | 10.8275 pct |
| max_adverse_excursion_pct | unavailable | 0 pct |
| time_to_peak_ms | unavailable | 11 ms |
| realized_exit_pct | unavailable | 0 pct |
| realized_vs_peak_gap_pct | unavailable | 0 pct |
| stale_position_ratio | unavailable | 1 (100.00%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: deferred until both matched-window packages validate beyond `partial`.
- Evidence still missing: pass-grade live validation, especially fill / exit / run-summary coverage on the matched pair.
- Next task: keep TASK-005 open, collect a fuller comparable matched window, and rerun replay readiness only after that; TASK-006 remains blocked.
