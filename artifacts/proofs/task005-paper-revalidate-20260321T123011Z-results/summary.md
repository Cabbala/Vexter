# comparison-dexter-task005-paper-revalidate-20260321T123011Z-vs-mewx-task005-paper-revalidate-20260321T123011Z

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `deferred`

## Notes

- Fresh same-attempt Dexter paper_live x Mew-X sim_live recollection after Dexter PR #3 merged to main (ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938).

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 208 | 0 |
| candidate_precision_proxy | 0.0096 (0.96%) | unavailable |
| fill_success_rate | 1 (100.00%) | 1 (100.00%) |
| signal_to_attempt_latency_ms | 0 ms | 963.5 ms |
| attempt_to_fill_latency_ms | 553.5 ms | 2 ms |
| quote_vs_fill_slippage_bps | 0 bps | -755.3364 bps |
| max_favorable_excursion_pct | 15.2663 pct | 25.3429 pct |
| max_adverse_excursion_pct | -17.8535 pct | 0 pct |
| time_to_peak_ms | 17197 ms | 1504 ms |
| realized_exit_pct | -5.5282 pct | 25.3429 pct |
| realized_vs_peak_gap_pct | 32.3434 pct | 0 pct |
| stale_position_ratio | 0.5 (50.00%) | 1 (100.00%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: deferred until both matched-window packages validate beyond `partial`.
- Evidence still missing: pass-grade live validation, especially fill / exit / run-summary coverage on the matched pair.
- Next task: keep TASK-005 open, collect a fuller comparable matched window, and rerun replay readiness only after that; TASK-006 remains blocked.
