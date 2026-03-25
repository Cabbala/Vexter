# comparison-dexter-task005-pass-grade-pair-20260325T180027Z-vs-mewx-task005-pass-grade-pair-20260325T180027Z

## Validation

- Dexter readiness: `pass`
- Mew-X readiness: `pass`
- Winner mode: `derived`

## Notes

- Approved validator rule implementation reclassified the promoted matched pair against the frozen-source contract.

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 255 | 0 |
| candidate_precision_proxy | 0.0157 (1.57%) | unavailable |
| fill_success_rate | 1 (100.00%) | 1 (100.00%) |
| signal_to_attempt_latency_ms | 0 ms | 891 ms |
| attempt_to_fill_latency_ms | 502.5 ms | 1.5 ms |
| quote_vs_fill_slippage_bps | 0 bps | 7.7061 bps |
| max_favorable_excursion_pct | 34.8443 pct | 6.7929 pct |
| max_adverse_excursion_pct | -6.0547 pct | 0 pct |
| time_to_peak_ms | 5299 ms | 20.5 ms |
| realized_exit_pct | 7.1641 pct | 0 pct |
| realized_vs_peak_gap_pct | 20.533 pct | -0 pct |
| stale_position_ratio | 0 (0.00%) | 1 (100.00%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: recorded in the current comparison matrix.
- Evidence still missing: none in this pack beyond the downstream replay-validation gate.
- Next task: Use this comparison pack as input to the next replay-validation gate.
