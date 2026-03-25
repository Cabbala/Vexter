# TASK-007-CANDIDATE-GENERATION-VS-QUALITY

## Scope

This task starts from merged PR `#28` and the completed `TASK-007` downstream research intake. It keeps the promoted comparison baseline frozen and asks a single bounded question:

- Does Dexter's `candidate_count` advantage appear to convert into realized edge on the promoted baseline, or is it only broader upstream opportunity coverage?

The task is source-faithful by design:

- no new evidence collection
- no validator or source changes
- no baseline reopen
- only live/replay comparison packs, candidate snapshots, session summaries, and close-summary metrics already committed in GitHub-visible artifacts

## Verified GitHub State

- Latest merged Vexter `main`: PR `#28`, merge commit `4df259b90365787ac24085227fcc1b15b63d057d`, merged at `2026-03-25T22:36:55Z`
- Supporting merged Vexter states: PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted repaired replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Candidate snapshot / session-summary evidence: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-replay-packages/mewx-replay/exports`
- Dexter close-summary evidence: `artifacts/proofs/task006-replay-surface-fix-20260325T180027Z-augmented-dexter-package/exports/dexter-close-summary-index.json`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from intake:

- Live winner mode: `derived`
- Replay winner mode: `derived`
- Stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Mew-X `candidate_precision_proxy` remains unavailable because `creator_candidate` is absent under the frozen export surface

## Evidence Surfaces Reused

### Comparison matrices

- Live and repaired replay both preserve:
  - Dexter lead on `candidate_count`, `signal_to_attempt_latency_ms`, `quote_vs_fill_slippage_bps`, `max_favorable_excursion_pct`, `realized_exit_pct`, `stale_position_ratio`
  - Mew-X lead on `attempt_to_fill_latency_ms`, `max_adverse_excursion_pct`, `time_to_peak_ms`, `realized_vs_peak_gap_pct`
  - tie on `fill_success_rate`, `replayability_grade`

### Dexter candidate-to-outcome surfaces

- Dexter state export records:
  - `creator_candidate`: `255`
  - `candidate_rejected`: `8`
  - `mint_observed`: `12`
  - `entry_signal`: `4`
  - `entry_attempt`: `4`
  - `entry_fill`: `4`
  - `position_closed`: `4`
- Dexter close-summary index records `4` closed sessions and lets the lane inspect realized return, favorable excursion, stale flag, time to peak, and exit reason without reopening source logic

### Mew-X candidate / session surfaces

- Mew-X candidate snapshots remain committed but empty:
  - `initial_selection`: `0` observations
  - `refresh`: `0` observations
- Mew-X state export still shows downstream activity:
  - `mint_observed`: `9`
  - `entry_signal`: `6`
  - `entry_attempt`: `6`
  - `entry_fill`: `6`
  - `position_closed`: `6`
- Mew-X session summaries expose realized return, favorable excursion, time to peak, exit reason, and candidate source for each close

## Candidate Breadth To Outcome Flow

### Dexter flow on the promoted baseline

- `255 creator_candidate -> 12 mint_observed -> 4 entry_signal -> 4 fills -> 4 closes`
- `candidate -> fill` ratio: `4 / 255 = 1.57%`
- `candidate -> positive realized close` ratio: `2 / 255 = 0.78%`
- `candidate -> positive MFE close` ratio: `4 / 255 = 1.57%`
- `mint_observed -> fill` ratio: `4 / 12 = 33.33%`

Dexter close summaries show the downstream quality of the filtered set:

| Mint | Exit reason | Realized return pct | MFE pct |
| --- | --- | ---: | ---: |
| `6aH...` | `safe` | `37.5246` | `37.5246` |
| `AdCv...` | `safe` | `26.4375` | `36.9798` |
| `EADT...` | `malicious` | `-26.5306` | `32.7088` |
| `GFYv...` | `malicious` | `-12.1094` | `23.9839` |

Roll-up from the same four closes:

- positive realized closes: `2 / 4`
- positive MFE closes: `4 / 4`
- median realized exit: `7.1641 pct`
- median favorable excursion: `34.8443 pct`
- median quote-to-fill slippage: `0.0 bps`
- stale-position ratio: `0.00%`

Interpretation bounded to these surfaces:

- Dexter breadth is not converting into more fills than Mew-X.
- It is converting into a smaller set of fills with much higher median favorable excursion and higher median realized exit.
- That makes the candidate-count edge look more like upstream screening that feeds better downstream opportunity capture than mere fill-volume inflation.

### Mew-X observable comparison boundary

Mew-X does not provide a cross-source comparable upstream candidate-quality surface here:

- `creator_candidate` events observed: `0`
- `candidate_precision_proxy`: unavailable
- committed candidate snapshots: empty on both `initial_selection` and `refresh`

What remains observable downstream:

- `9 mint_observed -> 6 fills -> 6 closes`
- `mint_observed -> fill` ratio: `6 / 9 = 66.67%`
- positive realized closes: `2 / 6`
- positive MFE closes: `3 / 6`
- median realized exit: `0.0 pct`
- median favorable excursion: `6.7929 pct`
- median quote-to-fill slippage: `7.7061 bps`
- stale-position ratio: `100.00%`
- exit reason: all `6` closes end as `inactivity_timeout`

This keeps the claim bounded:

- Mew-X converts observed sessions to fills more often than Dexter converts observed mints to fills.
- But the observable downstream outcome surface still underperforms Dexter on realized exit, favorable excursion, slippage, and stale-position control.
- Because upstream Mew-X candidate precision is missing, the lane cannot prove that Dexter's candidates are intrinsically higher quality across sources.

## Live / Replay Stability

The promoted repaired replay comparison preserves the same candidate and downstream medians used in the live lane reading:

- `candidate_count`: Dexter `255`, Mew-X `0`
- `signal_to_attempt_latency_ms`: Dexter `0`, Mew-X `891`
- `quote_vs_fill_slippage_bps`: Dexter `0.0`, Mew-X `7.7061`
- `max_favorable_excursion_pct`: Dexter `34.8443`, Mew-X `6.7929`
- `realized_exit_pct`: Dexter `7.1641`, Mew-X `0.0`
- `stale_position_ratio`: Dexter `0.0`, Mew-X `1.0`

Replay caveat preserved:

- Dexter `realized_vs_peak_gap_pct` still drifts from live `20.5330` to replay `25.8042`
- That drift is path-sensitive scope caveat, not an overturn of the realized-return conclusion

## Conclusion

### Key finding: `candidate_edge_supported`

Dexter's `candidate_count` advantage is supported as more than simple breadth on the frozen promoted baseline. The committed evidence shows a broad upstream candidate surface that narrows into fewer closed positions than Mew-X, but those positions carry:

- materially higher median favorable excursion
- positive median realized exit where Mew-X stays at `0.0 pct`
- zero median slippage where Mew-X does not
- zero stale positions where Mew-X closes all six sessions stale

### Bound: `candidate_quality_bounded`

The lane still cannot make a strong cross-source upstream precision claim because:

- Mew-X `candidate_precision_proxy` is unavailable
- Mew-X `creator_candidate` remains absent
- both committed Mew-X candidate snapshots are empty

So the source-faithful conclusion is:

- Dexter candidate breadth appears to convert into better realized edge within the promoted baseline pipeline
- cross-source candidate quality remains bounded, not proven

## Recommended Next Lane

- `execution_timing_vs_retention`

Why this is the highest-value next cut:

- this lane already established Dexter's upstream breadth and downstream realized-edge connection
- the next unresolved tradeoff is where Mew-X still wins after attempt placement: fill latency and peak retention
- that follow-up can stay inside existing committed surfaces without reopening comparison or evidence collection

## Key Paths

- Report: `artifacts/reports/task-007-candidate-generation-vs-quality-report.md`
- Status: `artifacts/reports/task-007-candidate-generation-vs-quality-status.md`
- Proof: `artifacts/proofs/task-007-candidate-generation-vs-quality-check.json`
- Summary: `artifacts/proofs/task-007-candidate-generation-vs-quality-summary.md`
- Prompt pack: `artifacts/reports/task-007-candidate-generation-vs-quality`
- Bundle: `artifacts/bundles/task-007-candidate-generation-vs-quality.tar.gz`
