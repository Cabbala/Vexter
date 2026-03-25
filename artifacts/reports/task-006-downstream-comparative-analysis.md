# TASK-006-DOWNSTREAM-COMPARATIVE-ANALYSIS

## Scope

This task starts from the merged PR `#24` replay-surface-fix baseline and turns the repaired promoted baseline into a downstream comparative interpretation without changing frozen Dexter or Mew-X source logic.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#24`, merge commit `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, merged at `2026-03-25T21:27:28Z`
- Supporting merged Vexter states: PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Formal Source Of Truth

- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted repaired replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Replay-surface-fix proof: `artifacts/proofs/task-006-replay-surface-fix-check.json`
- Confirmatory comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180604Z-comparison`
- Confirmatory residual proof: `artifacts/proofs/task-005-validator-rule-implement-check.json`

## Live Comparison Interpretation

- The promoted live pack remains `pass/pass` with `winner_mode: derived`.
- In this repo, `winner_mode: derived` means the comparison matrix now records component-level winners for the scored metrics. It does not encode a scalar overall winner field.
- Across the `12` scored metrics with concrete winner outcomes, the promoted live split is stable and interpretable:
  - Dexter leads `6`
  - Mew-X leads `4`
  - tie `2`

Dexter edges on the promoted live pack:

- `candidate_count`
- `signal_to_attempt_latency_ms`
- `quote_vs_fill_slippage_bps`
- `max_favorable_excursion_pct`
- `realized_exit_pct`
- `stale_position_ratio`

Mew-X edges on the promoted live pack:

- `attempt_to_fill_latency_ms`
- `max_adverse_excursion_pct`
- `time_to_peak_ms`
- `realized_vs_peak_gap_pct`

Ties on the promoted live pack:

- `fill_success_rate`
- `replayability_grade`

Interpretation:

- Dexter is stronger on candidate generation, immediate reaction after signal, slippage control at fill time, realized upside capture, and avoiding stale positions on this promoted baseline.
- Mew-X is stronger on fill latency once an attempt is placed, drawdown containment, faster path to peak, and holding closer to its local peak on exit.
- The promoted live baseline is therefore no longer blocked or winner-deferred; it is a comparable component-level tradeoff surface.

## Replay Consistency Interpretation

- The repaired replay pack also remains `pass/pass` with `winner_mode: derived`.
- The replay comparison keeps the same scored-metric split as live:
  - Dexter `6`
  - Mew-X `4`
  - tie `2`
- Dexter replay coverage is `100.00%` and Dexter `live_vs_replay_gap_pct` is `0.0000`.
- Mew-X replay coverage is `100.00%` and Mew-X `live_vs_replay_gap_pct` is `0.0000`.

Interpretation:

- The replay-surface repair did not invert or materially weaken the live comparison. It preserved the same component-level superiority pattern after replay reconstruction.
- That stability is the key downstream result: the promoted live conclusion survives the repaired replay surface instead of depending on an unresolved replay caveat.

## Confirmatory Residual

- Confirmatory pair: `task005-pass-grade-pair-20260325T180604Z`
- Dexter confirmatory classification: `pass`
- Mew-X confirmatory classification: `partial`
- Remaining confirmatory miss: `candidate_rejected`
- Confirmatory winner mode: `deferred`
- Confirmatory residual overturns promoted baseline: `no`

Interpretation:

- The confirmatory rerun is weaker than the promoted pair, but its weakness is narrow and one-sided.
- Because the residual is only Mew-X `candidate_rejected`, it does not reopen the promoted live/replay interpretation and should stay a caveat rather than a new blocker.

## Remaining Caveats

- Current replay parity is a close-summary / `position_closed` realized-return fidelity claim, not proof of full execution-path equivalence.
- Mew-X `0.0000` replay gap should still be read as summary fidelity because replay reconstruction uses exported session summaries from the same frozen session state that emitted `position_closed`.
- Dexter replay parity is now source-faithful for promoted non-stagnant closes because Vexter added narrow close-summary exports; stagnant replay exports still remain as fallback, so the claim should stay scoped to the repaired surface.
- The replay gap proof measures matched `position_closed` realized return only. It does not certify that every path-sensitive derived metric is identical across live and replay.
- That scope caveat is visible in the promoted Dexter metrics: `realized_vs_peak_gap_pct` is `20.5330` on the promoted live pack and `25.8042` on the repaired replay pack even though Dexter `live_vs_replay_gap_pct` is `0.0000`.
- Mew-X candidate-generation comparison remains asymmetric because `candidate_precision_proxy` stays unavailable when `creator_candidate` is absent under the frozen export surface.

## Decision

- Outcome: `A`
- Key finding: `comparison_closeout_ready`
- TASK-006 state: `comparison_closeout_ready`
- Downstream research handoff: `ready`
- New evidence collection: `not recommended`

Evidence-based next cut:

- If one more Vexter task is desired, it should be `TASK-006` comparison closeout rather than new evidence collection.
- The current bundle is already sufficient for downstream research or judgment handoff because the remaining caveats are about scope and interpretation, not about unresolved evidence holes.

## Key Paths

- Comparative analysis proof: `artifacts/proofs/task-006-downstream-comparative-analysis-check.json`
- Comparative analysis summary: `artifacts/proofs/task-006-downstream-comparative-analysis-summary.md`
- Status report: `artifacts/reports/task-006-replay-validation-status.md`
- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Confirmatory comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180604Z-comparison`
