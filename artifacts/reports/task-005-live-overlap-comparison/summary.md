# comparison-dexter-window-20260320T202100Z-vs-mewx-desktop-nnc6mps-20260320T201918Z

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `deferred`

## Notes

- Matched-overlap retry captured only a 281 ms shared live window before Mew-X stopped producing events and Dexter remained zero-balance observe-only.

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 57 | 0 |
| candidate_precision_proxy | 0 (0.00%) | unavailable |
| fill_success_rate | unavailable | unavailable |
| signal_to_attempt_latency_ms | unavailable | unavailable |
| attempt_to_fill_latency_ms | unavailable | unavailable |
| quote_vs_fill_slippage_bps | unavailable | unavailable |
| max_favorable_excursion_pct | unavailable | unavailable |
| max_adverse_excursion_pct | unavailable | unavailable |
| time_to_peak_ms | unavailable | unavailable |
| realized_exit_pct | unavailable | unavailable |
| realized_vs_peak_gap_pct | unavailable | unavailable |
| stale_position_ratio | unavailable | unavailable |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: deferred until both matched-window packages validate beyond `partial`.
- Evidence still missing: pass-grade live validation, especially fill / exit / run-summary coverage on the matched pair.
- Next task: keep TASK-005 open, collect a fuller comparable matched window, and rerun replay readiness only after that; TASK-006 remains blocked.
