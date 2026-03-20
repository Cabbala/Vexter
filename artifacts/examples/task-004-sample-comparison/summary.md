# comparison-dexter-fixture-001-vs-mewx-fixture-001

## Validation

- Dexter readiness: `pass`
- Mew-X readiness: `pass`
- Winner mode: `deferred`

## Notes

- Fixture-based sample pack for TASK-004 scaffolding. Live Windows comparison remains pending.

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 2 | 3 |
| candidate_precision_proxy | 0.5 (50.00%) | 0.6667 (66.67%) |
| fill_success_rate | 0.5 (50.00%) | 0.6667 (66.67%) |
| signal_to_attempt_latency_ms | 2000 ms | 1000 ms |
| attempt_to_fill_latency_ms | 2000 ms | 1000 ms |
| quote_vs_fill_slippage_bps | 294.1176 bps | 127.6316 bps |
| max_favorable_excursion_pct | 20 pct | 14.5 pct |
| max_adverse_excursion_pct | -4 pct | -9 pct |
| time_to_peak_ms | 60000 ms | 67500 ms |
| realized_exit_pct | 13.3333 pct | 3.5817 pct |
| realized_vs_peak_gap_pct | 6 pct | 14 pct |
| stale_position_ratio | 0 (0.00%) | 0.5 (50.00%) |
| replayability_grade | full | full |

## Decision

- Winning component candidates: pending live matched-window evidence.
- Evidence still missing: live Dexter and Mew-X run packages gathered from the same measurement window with pass-grade validation.
- Next task: Resume TASK-005 with a matched comparable live window; TASK-006 remains blocked.
