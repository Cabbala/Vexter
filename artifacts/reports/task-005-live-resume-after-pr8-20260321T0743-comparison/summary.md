# comparison-dexter-resume-after-pr8-20260321T0743-vs-mewx-resume-after-pr8-20260321T0743

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `deferred`

## Notes

- Fresh same-attempt recollection on 2026-03-21 JST avoided Dexter startup wallet-balance HTTP 429 via Vexter-side quiet period, wsLogs subscription wait, and spaced retries. Exact event overlap now spans 2026-03-20T22:42:56.215162Z to 2026-03-20T22:44:27.240Z; Dexter improved to 4/12 required event types while Mew-X remains partial at 8/12.

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 114 | 0 |
| candidate_precision_proxy | 0 (0.00%) | unavailable |
| fill_success_rate | unavailable | 1 (100.00%) |
| signal_to_attempt_latency_ms | unavailable | 888 ms |
| attempt_to_fill_latency_ms | unavailable | 1 ms |
| quote_vs_fill_slippage_bps | unavailable | 4.5031 bps |
| max_favorable_excursion_pct | unavailable | 0 pct |
| max_adverse_excursion_pct | unavailable | 0 pct |
| time_to_peak_ms | unavailable | 10 ms |
| realized_exit_pct | unavailable | 0 pct |
| realized_vs_peak_gap_pct | unavailable | -0.045 pct |
| stale_position_ratio | unavailable | 1 (100.00%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: deferred until both matched-window packages validate beyond `partial`.
- Evidence still missing: pass-grade live validation, especially fill / exit / run-summary coverage on the matched pair.
- Next task: keep TASK-005 open, collect a fuller comparable matched window, and rerun replay readiness only after that; TASK-006 remains blocked.
