# comparison-dexter-task005-pass-grade-pair-20260325T180604Z-vs-mewx-task005-pass-grade-pair-20260325T180604Z

## Validation

- Dexter readiness: `partial`
- Mew-X readiness: `partial`
- Winner mode: `deferred`

## Notes

- Confirmatory TASK-005 pass-grade-pair attempt after Vexter PR #15 / Dexter PR #3 merged: Dexter paper_live x Mew-X sim_live collected from the same attempt on 2026-03-25T18:07Z with extended grace.

## Critical Metrics

| Metric | Dexter | Mew-X |
| --- | --- | --- |
| candidate_count | 274 | 0 |
| candidate_precision_proxy | 0.0146 (1.46%) | unavailable |
| fill_success_rate | 1 (100.00%) | 1 (100.00%) |
| signal_to_attempt_latency_ms | 0 ms | 1413 ms |
| attempt_to_fill_latency_ms | 319 ms | 1 ms |
| quote_vs_fill_slippage_bps | 0 bps | 0 bps |
| max_favorable_excursion_pct | 22.473 pct | 1.0139 pct |
| max_adverse_excursion_pct | -17.1695 pct | 0 pct |
| time_to_peak_ms | 2517 ms | 7 ms |
| realized_exit_pct | -14.931 pct | 0 pct |
| realized_vs_peak_gap_pct | 43.969 pct | 0 pct |
| stale_position_ratio | 0 (0.00%) | 1 (100.00%) |
| replayability_grade | partial | partial |

## Decision

- Winning component candidates: deferred until both matched-window packages validate beyond `partial`.
- Evidence still missing: pass-grade live validation, especially fill / exit / run-summary coverage on the matched pair.
- Next task: keep TASK-005 open, collect a fuller comparable matched window, and rerun replay readiness only after that; TASK-006 remains blocked.
