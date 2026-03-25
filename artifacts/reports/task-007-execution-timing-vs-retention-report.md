# TASK-007-EXECUTION-TIMING-VS-RETENTION

## Scope

This task starts from merged PR `#29` and the completed `TASK-007-CANDIDATE-GENERATION-VS-QUALITY` lane. It keeps the promoted comparison baseline frozen and asks a single bounded question:

- Is the most useful current cross-source reading a stage split between Dexter's upstream timing / slippage edge and Mew-X's post-attempt fill-speed / local-retention edge?

The task stays source-faithful by design:

- no new evidence collection
- no validator or source changes
- no baseline reopen
- only committed live/replay comparison packs, Mew-X session summaries, and Dexter close-summary metrics already visible in GitHub artifacts

## Verified GitHub State

- Latest merged Vexter `main`: PR `#29`, merge commit `17af013b0383fd142e15932108c8b4da5447f1f7`, merged at `2026-03-25T22:57:54Z`
- Supporting merged Vexter states: PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted repaired replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Dexter close-summary evidence: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-augmented-dexter-package/exports/dexter-close-summary-index.json`
- Mew-X session-summary evidence: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-replay-packages/mewx-replay/exports`
- Candidate-lane source of truth: `artifacts/reports/task-007-candidate-generation-vs-quality-report.md`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from intake and the candidate lane:

- Live winner mode: `derived`
- Replay winner mode: `derived`
- Stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Dexter upstream breadth still carries forward as `candidate_edge_supported`
- Any stronger retention claim remains bounded by the existing replay-scope caveat on Dexter `realized_vs_peak_gap_pct`

## Evidence Surfaces Reused

### Comparison matrices

Promoted live and repaired replay preserve the same winner split on the scored timing / exit metrics:

- Dexter lead:
  - `signal_to_attempt_latency_ms`
  - `quote_vs_fill_slippage_bps`
  - `max_favorable_excursion_pct`
  - `realized_exit_pct`
  - `stale_position_ratio`
- Mew-X lead:
  - `attempt_to_fill_latency_ms`
  - `max_adverse_excursion_pct`
  - `time_to_peak_ms`
  - `realized_vs_peak_gap_pct`
- Tie:
  - `fill_success_rate`
  - `replayability_grade`

### Dexter close-summary surface

Dexter close summaries stay concentrated in four closed sessions:

| Mint | Exit reason | Realized pct | MFE pct | MAE pct | Time to peak ms | Peak-to-close ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `6aH...` | `safe` | `37.5246` | `37.5246` | `0.0` | `3579` | `454` |
| `AdCv...` | `safe` | `26.4375` | `36.9798` | `0.0` | `4678` | `42` |
| `EADT...` | `malicious` | `-26.5306` | `32.7088` | `-26.5306` | `5920` | `13116` |
| `GFYv...` | `malicious` | `-12.1094` | `23.9839` | `-12.1094` | `5988` | `13098` |

Roll-up from the same four closes:

- median realized exit: `7.1641 pct`
- median MFE: `34.8443 pct`
- median MAE: `-6.0547 pct`
- median time to peak: `5299.0 ms`
- median quote-to-fill slippage: `0.0 bps`
- stale-position ratio: `0.00%`
- exit reasons: `safe=2`, `malicious=2`

### Mew-X session-summary surface

Mew-X session summaries stay concentrated in six closes:

| Mint | Exit reason | Realized pct | MFE pct | MAE pct | Time to peak ms | Peak-to-close ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `9P5...` | `inactivity_timeout` | `0.0` | `0.0` | `0.0` | `24` | `5017` |
| `AUy...` | `inactivity_timeout` | `0.0` | `13.5858` | `0.0` | `7` | `5016` |
| `BMR...` | `inactivity_timeout` | `0.0` | `0.0` | `0.0` | `7` | `5028` |
| `DYa...` | `inactivity_timeout` | `16.4377` | `16.4377` | `0.0` | `278` | `5024` |
| `H79...` | `inactivity_timeout` | `16.8682` | `16.8682` | `0.0` | `1300` | `5018` |
| `fmF...` | `inactivity_timeout` | `0.0` | `0.0` | `0.0` | `17` | `5013` |

Roll-up from the same six closes:

- median realized exit: `0.0 pct`
- median MFE: `6.7929 pct`
- median MAE: `0.0 pct`
- median time to peak: `20.5 ms`
- median quote-to-fill slippage: `7.7061 bps`
- stale-position ratio: `100.00%`
- exit reasons: `inactivity_timeout=6`

## Stage Split Reading

### Signal-to-attempt vs attempt-to-fill

The promoted comparison surfaces show a clean stage split:

- Dexter median `signal_to_attempt_latency_ms`: `0.0`
- Mew-X median `signal_to_attempt_latency_ms`: `891.0`
- Dexter median `attempt_to_fill_latency_ms`: `502.5`
- Mew-X median `attempt_to_fill_latency_ms`: `1.5`

Source-faithful interpretation:

- Dexter is faster before the order attempt exists. Its edge is at the detection-to-action boundary.
- Mew-X is faster after the attempt exists. Its edge is at the attempt-to-fill boundary.
- These are not contradictory claims. They describe two different segments of the same execution path.

### Slippage control vs fill latency

Fast fill after attempt does not map directly to better slippage on this baseline:

- Dexter median `quote_vs_fill_slippage_bps`: `0.0`
- Mew-X median `quote_vs_fill_slippage_bps`: `7.7061`

Bounded interpretation:

- Dexter's slower post-attempt fill path is still paired with tighter quote-to-fill control.
- Mew-X's very fast post-attempt fills do not carry a slippage advantage in the committed comparison packs.
- So the stage split is better read as timing versus quote control, not as a single generic execution-speed winner.

## Exit Capture Vs Retention

### Favorable excursion / realized exit vs drawdown / local-peak retention

The committed metrics split the downstream objective surface:

- Dexter median `max_favorable_excursion_pct`: `34.8443` vs Mew-X `6.7929`
- Dexter median `realized_exit_pct`: `7.1641` vs Mew-X `0.0`
- Mew-X median `max_adverse_excursion_pct`: `0.0` vs Dexter `-6.0547`
- Mew-X median `time_to_peak_ms`: `20.5` vs Dexter `5299.0`
- Mew-X median `realized_vs_peak_gap_pct`: `0.0` live / `0.0` replay vs Dexter `20.5330` live / `25.8042` replay

What this supports:

- Dexter captures materially larger upside and still realizes a positive median exit even though it gives back more from peak.
- Mew-X reaches local peak much sooner, contains adverse excursion better, and exits with almost no giveback versus that local peak.
- The retention claim is therefore narrow: Mew-X is better at local peak retention and drawdown containment on the opportunities it reaches, not at total realized exit on the frozen promoted baseline.

### Stale-position control

`stale_position_ratio` matters because it tells us whether the lifecycle ends through an active exit path or by timing out:

- Dexter stale-position ratio: `0.0`
- Mew-X stale-position ratio: `1.0`
- Dexter exit reasons: `safe=2`, `malicious=2`
- Mew-X exit reasons: `inactivity_timeout=6`

Why this matters:

- Mew-X's six closes all retain their local peak well, but they still end through inactivity timeout after roughly five seconds beyond peak.
- Dexter's closes do not go stale even when the session is longer; they close on active `safe` or `malicious` paths instead.
- That means Mew-X's retention edge should not be over-read as superior downstream lifecycle control. Dexter still owns the stale-control surface.

## Objective-Function Read

Prefer Dexter when the downstream objective weights:

- earlier signal capture
- lower quote-to-fill slippage
- larger favorable excursion capture
- positive realized exit
- active exit-path control and non-stale closes

Prefer Mew-X when the downstream objective weights:

- faster fill after an attempt exists
- lower adverse excursion
- faster peak discovery
- minimal giveback from local peak once the peak is reached

This is the bounded objective-function conclusion:

- there is no source-faithful universal winner claim on the current evidence
- there is a real stage-specific tradeoff
- the unresolved next question is how much downstream planning should weight drawdown containment versus exit capture

## Conclusion

### Key finding: `timing_retention_tradeoff_supported`

The current evidence supports a real tradeoff surface:

- Dexter is stronger earlier in the pipeline and on slippage / realized exit capture
- Mew-X is stronger later in the path on fill latency, drawdown containment, and local-peak retention

### Claim boundary: `tradeoff_bounded`

The tradeoff remains bounded because:

- Dexter still wins realized exit and stale-position control
- Mew-X's retention advantage is local-peak retention, not broader downstream realized-performance dominance
- Dexter `realized_vs_peak_gap_pct` still shows live-to-replay drift, so stronger path-equivalence claims belong in a separate lane

## Recommended Next Lane

- `risk_containment_vs_exit_capture`

Why this is the highest-value next cut:

- this lane isolated the stage split cleanly enough to stop debating generic timing
- the remaining unresolved decision is objective weighting between Mew-X drawdown containment / local retention and Dexter favorable excursion / realized exit
- that question still fits the current committed surfaces and does not require reopening evidence collection

## Key Paths

- Report: `artifacts/reports/task-007-execution-timing-vs-retention-report.md`
- Status: `artifacts/reports/task-007-execution-timing-vs-retention-status.md`
- Proof: `artifacts/proofs/task-007-execution-timing-vs-retention-check.json`
- Summary: `artifacts/proofs/task-007-execution-timing-vs-retention-summary.md`
- Prompt pack: `artifacts/reports/task-007-execution-timing-vs-retention`
- Bundle: `artifacts/bundles/task-007-execution-timing-vs-retention.tar.gz`
