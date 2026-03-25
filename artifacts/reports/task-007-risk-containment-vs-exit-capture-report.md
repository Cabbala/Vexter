# TASK-007-RISK-CONTAINMENT-VS-EXIT-CAPTURE

## Scope

This task starts from merged PR `#30` and the completed `TASK-007-EXECUTION-TIMING-VS-RETENTION` lane. It keeps the promoted comparison baseline frozen and asks a single bounded question:

- Once the objective function explicitly weights drawdown containment against favorable excursion, realized exit capture, and stale-position avoidance, how should Dexter and Mew-X be read on the current evidence?

The task stays source-faithful by design:

- no new evidence collection
- no validator or source changes
- no baseline reopen
- only committed live/replay comparison packs, Mew-X session summaries, and Dexter close-summary metrics already visible in GitHub artifacts

## Verified GitHub State

- Latest merged Vexter `main`: PR `#30`, merge commit `052de6ccecef1461d2291fb4f0ef5fbf8883d548`, merged at `2026-03-25T23:15:40Z`
- Supporting merged Vexter states: PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted repaired replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Dexter close-summary evidence: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-augmented-dexter-package/exports/dexter-close-summary-index.json`
- Mew-X session-summary evidence: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-replay-packages/mewx-replay/exports`
- Timing/retention lane source of truth: `artifacts/reports/task-007-execution-timing-vs-retention-report.md`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from intake and prior lanes:

- Live winner mode: `derived`
- Replay winner mode: `derived`
- Stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Timing/retention already established that Dexter owns earlier timing and Mew-X owns post-attempt fill speed
- Any stronger path-equivalence claim remains bounded by the existing Dexter `realized_vs_peak_gap_pct` live/replay drift

## Evidence Surfaces Reused

### Comparison matrices

Promoted live and repaired replay preserve the same scored winners on the metrics that matter for this lane:

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

Dexter close summaries stay concentrated in four non-stale closed sessions:

- median realized exit: `7.1641 pct`
- median MFE: `34.8443 pct`
- median MAE: `-6.0547 pct`
- median time to peak: `5299.0 ms`
- median quote-to-fill slippage: `0.0 bps`
- stale-position ratio: `0.00%`
- exit reasons: `safe=2`, `malicious=2`

The per-close surface shows what the tradeoff looks like inside those four sessions:

| Mint | Exit reason | Realized pct | MFE pct | MAE pct | Realized-vs-peak gap pct |
| --- | --- | ---: | ---: | ---: | ---: |
| `6aH...` | `safe` | `37.5246` | `37.5246` | `0.0` | `0.0` |
| `AdCv...` | `safe` | `26.4375` | `36.9798` | `0.0` | `0.0` |
| `EADT...` | `malicious` | `-26.5306` | `32.7088` | `-26.5306` | `80.6314` |
| `GFYv...` | `malicious` | `-12.1094` | `23.9839` | `-12.1094` | `41.0661` |

### Mew-X session-summary surface

Mew-X session summaries stay concentrated in six timeout-shaped closes:

- median realized exit: `0.0 pct`
- median MFE: `6.7929 pct`
- median MAE: `0.0 pct`
- median time to peak: `20.5 ms`
- median realized-vs-peak gap: `0.0 pct`
- median quote-to-fill slippage: `7.7061 bps`
- stale-position ratio: `100.00%`
- exit reasons: `inactivity_timeout=6`

The local-peak behavior is consistent across the six closes:

| Mint | Exit reason | Realized pct | MFE pct | MAE pct | Peak-to-close ms |
| --- | --- | ---: | ---: | ---: | ---: |
| `9P5...` | `inactivity_timeout` | `0.0` | `0.0` | `0.0` | `5017` |
| `AUy...` | `inactivity_timeout` | `0.0` | `13.5858` | `0.0` | `5016` |
| `BMR...` | `inactivity_timeout` | `0.0` | `0.0` | `0.0` | `5028` |
| `DYa...` | `inactivity_timeout` | `16.4377` | `16.4377` | `0.0` | `5024` |
| `H79...` | `inactivity_timeout` | `16.8682` | `16.8682` | `0.0` | `5018` |
| `fmF...` | `inactivity_timeout` | `0.0` | `0.0` | `0.0` | `5013` |

## Risk Containment Vs Exit Capture

### Price-path containment

The cleanest Mew-X advantage remains inside the intra-position path:

- Mew-X median `max_adverse_excursion_pct`: `0.0`
- Dexter median `max_adverse_excursion_pct`: `-6.0547`
- Mew-X median `time_to_peak_ms`: `20.5`
- Dexter median `time_to_peak_ms`: `5299.0`
- Mew-X median `realized_vs_peak_gap_pct`: `0.0` live / `0.0` replay
- Dexter median `realized_vs_peak_gap_pct`: `20.5330` live / `25.8042` replay

What this supports:

- Mew-X reaches a local best price almost immediately after fill.
- Mew-X does not go materially underwater on the median close.
- Mew-X also gives back essentially none of that local peak on the median close.

What this does not support:

- It does not show a better realized-exit surface in absolute terms.
- It does not show better active lifecycle control, because every observed close still times out.

### Exit capture and realized upside

The cleanest Dexter advantage remains inside absolute upside capture:

- Dexter median `max_favorable_excursion_pct`: `34.8443` vs Mew-X `6.7929`
- Dexter median `realized_exit_pct`: `7.1641` vs Mew-X `0.0`
- Dexter median quote-to-fill slippage: `0.0 bps` vs Mew-X `7.7061 bps`

What this supports:

- Dexter captures much larger favorable excursions on the promoted baseline.
- Dexter still realizes positive median exit despite giving back more from peak.
- Dexter's slower post-attempt fill path does not erase its exit-capture edge because slippage stays tighter.

Bounded interpretation:

- Mew-X's near-zero `realized_vs_peak_gap_pct` is best read as retaining a smaller or faster local peak.
- Dexter's larger giveback is paired with a much larger absolute upside surface and a higher realized median exit.
- So an objective that values absolute realized upside still prefers Dexter on the current baseline.

### Stale-position control and the meaning of `stale_position_ratio`

`stale_position_ratio` is the operational risk-control surface in this lane:

- Dexter stale-position ratio: `0.0`
- Mew-X stale-position ratio: `1.0`
- Dexter exit reasons: `safe=2`, `malicious=2`
- Mew-X exit reasons: `inactivity_timeout=6`

Why this matters:

- Mew-X's drawdown containment edge is price-path containment, not lifecycle containment.
- All six Mew-X closes rely on the same timeout-style terminal path roughly five seconds after local peak.
- Dexter closes every observed position through an active `safe` or `malicious` path and never leaves a stale position open.

So the source-faithful split is:

- price-path containment: Mew-X
- lifecycle containment / stale avoidance: Dexter

### `time_to_peak_ms` and early-decay risk

`time_to_peak_ms` matters here because it changes what kind of retention claim the data can support:

- Mew-X median `time_to_peak_ms` `20.5` means the local best print arrives almost immediately after fill, which limits time exposed before the best observed price is reached.
- Dexter median `time_to_peak_ms` `5299.0` means the larger upside surface often develops later, so realized-vs-peak readings are more path-sensitive.

This is why the retention claim stays narrow:

- Mew-X is better at holding onto a very early local peak.
- Dexter is better at converting a much larger and later-developing excursion into realized exit and non-stale closure.

## Objective-Function Read

### Drawdown containment weighted highest

Prefer Mew-X when the objective is primarily:

- minimal adverse excursion
- faster local peak discovery
- minimal giveback versus that local peak

Bound on that preference:

- this preference assumes timeout-shaped closes are acceptable or secondary
- it does not imply superior realized exit or lifecycle control

### Upside capture weighted highest

Prefer Dexter when the objective is primarily:

- larger favorable excursion
- positive realized exit
- tighter quote-to-fill control

Why this stays source-faithful:

- Dexter wins both MFE and realized exit on the promoted baseline
- Mew-X's retention edge does not overturn the absolute-exit surface

### Stale-risk avoidance weighted highest

Prefer Dexter decisively when the objective is primarily:

- active close-path control
- avoiding timeout-shaped stale closes
- reducing operational ambiguity around how positions end

Why this matters downstream:

- the current evidence already shows that stale avoidance is not a tie-breaker here
- it is a first-order surface where Dexter is strictly better on the frozen baseline

## Conclusion

### Key finding: `risk_exit_tradeoff_supported`

The current evidence supports a real objective-dependent split:

- Mew-X is stronger on price-path drawdown containment and local-peak retention
- Dexter is stronger on absolute exit capture and lifecycle control

### Claim boundary: `tradeoff_bounded`

The tradeoff remains bounded because:

- Mew-X's risk edge is local to the path, not a broader downstream realized-exit edge
- Dexter still wins realized exit and stale-position control
- Dexter `realized_vs_peak_gap_pct` remains path-sensitive, so a stronger path-equivalence claim still belongs in a separate task

## Recommended Next Step

- `strategy_planning`

Why this is the highest-value next cut:

- the remaining unresolved work is now explicit objective weighting, not missing evidence
- `path_sensitive_retention_scope` is not required to choose between drawdown containment and exit capture on the current bounded claim
- `execution_planning` should follow only after the strategy objective weights are fixed

## Key Paths

- Report: `artifacts/reports/task-007-risk-containment-vs-exit-capture-report.md`
- Status: `artifacts/reports/task-007-risk-containment-vs-exit-capture-status.md`
- Proof: `artifacts/proofs/task-007-risk-containment-vs-exit-capture-check.json`
- Summary: `artifacts/proofs/task-007-risk-containment-vs-exit-capture-summary.md`
- Prompt pack: `artifacts/reports/task-007-risk-containment-vs-exit-capture`
- Bundle: `artifacts/bundles/task-007-risk-containment-vs-exit-capture.tar.gz`
