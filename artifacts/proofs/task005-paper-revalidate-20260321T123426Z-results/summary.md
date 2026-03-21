# comparison-dexter-task005-paper-revalidate-20260321T123426Z-vs-mewx-task005-paper-revalidate-20260321T123426Z

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `deferred`

## Notes

- Confirmatory same-attempt Dexter paper_live x Mew-X sim_live recollection after Dexter PR #3 merged to main (ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938).

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 212 | 0 |
| candidate_precision_proxy | 0.0047 (0.47%) | unavailable |
| fill_success_rate | 1 (100.00%) | 1 (100.00%) |
| signal_to_attempt_latency_ms | 0 ms | 972 ms |
| attempt_to_fill_latency_ms | 321 ms | 1 ms |
| quote_vs_fill_slippage_bps | 0 bps | -1193.4193 bps |
| max_favorable_excursion_pct | 6.9324 pct | 34.8818 pct |
| max_adverse_excursion_pct | -28.5856 pct | 0 pct |
| time_to_peak_ms | 29057 ms | 234 ms |
| realized_exit_pct | -27.1919 pct | 34.8818 pct |
| realized_vs_peak_gap_pct | 46.8688 pct | 0 pct |
| stale_position_ratio | 0 (0.00%) | 0.8 (80.00%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: deferred until both matched-window packages validate beyond `partial`.
- Evidence still missing: pass-grade live validation, especially fill / exit / run-summary coverage on the matched pair.
- Next task: keep TASK-005 open, collect a fuller comparable matched window, and rerun replay readiness only after that; TASK-006 remains blocked.
