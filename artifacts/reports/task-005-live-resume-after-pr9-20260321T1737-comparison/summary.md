# comparison-dexter-resume-after-pr9-20260321T1737-vs-mewx-resume-after-pr9-20260321T1737

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `deferred`

## Notes

- Fresh same-attempt recollection on 2026-03-21 JST kept Dexter on observe_live with one startup retry after an initial wallet-balance HTTP 429, preserved a 167.174 s exact event overlap from 2026-03-21T08:39:09.961841Z to 2026-03-21T08:41:57.136Z, and recovered Mew-X session-summary packaging while Dexter remained capped at 4/12 required event types.

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 163 | 0 |
| candidate_precision_proxy | 0 (0.00%) | unavailable |
| fill_success_rate | unavailable | 1 (100.00%) |
| signal_to_attempt_latency_ms | unavailable | 921.5 ms |
| attempt_to_fill_latency_ms | unavailable | 1 ms |
| quote_vs_fill_slippage_bps | unavailable | -413.031 bps |
| max_favorable_excursion_pct | unavailable | 5.6112 pct |
| max_adverse_excursion_pct | unavailable | 0 pct |
| time_to_peak_ms | unavailable | 14.5 ms |
| realized_exit_pct | unavailable | 0 pct |
| realized_vs_peak_gap_pct | unavailable | 0 pct |
| stale_position_ratio | unavailable | 1 (100.00%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: deferred until both matched-window packages validate beyond `partial`.
- Evidence still missing: pass-grade live validation, especially fill / exit / run-summary coverage on the matched pair.
- Next task: keep TASK-005 open, collect a fuller comparable matched window, and rerun replay readiness only after that; if retries keep stalling on Dexter coverage, limit follow-up to a design-only review of a minimal paper-mode or paper-equivalent path. Keep Mew-X on `sim` / `sim_live` and Dexter on the observe-only / zero-balance safety path unless a formal paper mode is confirmed; TASK-006 remains blocked.
