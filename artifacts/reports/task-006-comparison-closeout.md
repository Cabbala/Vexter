# TASK-006-COMPARISON-CLOSEOUT

## Scope

This task starts from the merged PR `#25` downstream comparative analysis baseline and turns the promoted baseline into the formal closeout source of truth for TASK-006 without changing frozen Dexter or Mew-X source logic.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#25`, merge commit `727589b40d26c453c2fef78dc5060aa1098c1aad`, merged at `2026-03-25T21:43:44Z`
- Supporting merged Vexter states: PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Formal Source Of Truth

- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted repaired replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Downstream comparative analysis report: `artifacts/reports/task-006-downstream-comparative-analysis.md`
- Downstream comparative analysis proof: `artifacts/proofs/task-006-downstream-comparative-analysis-check.json`
- Confirmatory comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180604Z-comparison`

Closeout rule:

- The promoted baseline is now the official comparison source of truth for downstream use.
- The confirmatory pair remains a residual note only unless contradictory evidence appears.
- No new evidence collection is justified on current facts.

## Final Comparative Conclusion

- The promoted live pack remains `pass/pass` with `winner_mode: derived`.
- The repaired replay pack remains `pass/pass` with `winner_mode: derived`.
- The scored-metric split is stable across both live and replay:
  - Dexter leads `6`
  - Mew-X leads `4`
  - tie `2`

Dexter strengths on the promoted baseline:

- `candidate_count`
- `signal_to_attempt_latency_ms`
- `quote_vs_fill_slippage_bps`
- `max_favorable_excursion_pct`
- `realized_exit_pct`
- `stale_position_ratio`

Mew-X strengths on the promoted baseline:

- `attempt_to_fill_latency_ms`
- `max_adverse_excursion_pct`
- `time_to_peak_ms`
- `realized_vs_peak_gap_pct`

Ties on the promoted baseline:

- `fill_success_rate`
- `replayability_grade`

Interpretation:

- Dexter remains stronger on candidate generation, entry immediacy, slippage control, realized upside capture, and stale-position control.
- Mew-X remains stronger on fill latency after attempt, drawdown containment, faster peak realization, and retaining more of peak performance on exit.
- `winner_mode: derived` should continue to be interpreted as a component-level tradeoff surface, not as a scalar overall winner field.

## Replay Stability

- Dexter replay coverage: `100.00%`
- Dexter `live_vs_replay_gap_pct`: `0.0000`
- Mew-X replay coverage: `100.00%`
- Mew-X `live_vs_replay_gap_pct`: `0.0000`

Interpretation:

- Replay no longer reopens the promoted comparison. It stabilizes it.
- The repaired replay surface preserves the same component-level shape already seen on the promoted live baseline.

## Residual And Caveats

### Confirmatory residual

- Confirmatory pair: `task005-pass-grade-pair-20260325T180604Z`
- Dexter confirmatory classification: `pass`
- Mew-X confirmatory classification: `partial`
- Remaining confirmatory miss: `candidate_rejected`
- Confirmatory residual overturns promoted baseline: `no`

Treatment:

- Carry the confirmatory miss as a narrow one-sided caveat only.
- Do not reopen the promoted baseline absent contradictory evidence.

### Remaining caveats

- Current replay parity is a close-summary / `position_closed` realized-return fidelity claim, not proof of full execution-path equivalence.
- Mew-X `0.0000` replay gap remains a summary-fidelity claim because replay reconstruction uses exported session summaries from the same session state that emitted `position_closed`.
- Dexter replay parity is now source-faithful for promoted non-stagnant closes because Vexter adds narrow close-summary replay exports; the claim should stay scoped to that repaired surface.
- The gap proof measures matched `position_closed` realized return only. It does not certify that every path-sensitive derived metric is identical across live and replay.
- That scope limit is visible in Dexter `realized_vs_peak_gap_pct`, which is `20.5330` on the promoted live pack and `25.8042` on the repaired replay pack even while the measured close-return gap is `0.0000`.
- Mew-X candidate-generation precision remains asymmetric because `candidate_precision_proxy` stays unavailable when `creator_candidate` is absent under the frozen export surface.

## Research Handoff

Frozen facts safe to reuse downstream:

- Treat `task005-pass-grade-pair-20260325T180027Z` as the promoted comparison baseline.
- Treat the promoted live and repaired replay packs as the official closeout source of truth.
- Reuse the stable split Dexter `6`, Mew-X `4`, tie `2` as the comparative summary across live and replay.
- Keep Dexter strengths fixed to candidate generation, signal-to-attempt latency, slippage, favorable excursion, realized exit, and stale-position control.
- Keep Mew-X strengths fixed to fill latency, drawdown containment, time-to-peak, and realized-vs-peak retention.
- Carry only Mew-X `candidate_rejected` as the confirmatory residual note.

What not to claim downstream:

- Do not claim a scalar overall winner.
- Do not claim full path equivalence from the current replay proof.
- Do not restart evidence collection unless contradictory evidence appears.

## Decision

- Outcome: `A`
- Key finding: `comparison_closed_out`
- TASK-006 state: `comparison_closed_out`
- Downstream research handoff: `ready`
- New evidence collection: `not recommended`

Evidence-based next cut:

- Hand the current bundle to downstream research or execution planning as the frozen comparison baseline.
- If deeper replay claims are ever needed, cut that as a separate path-equivalence task rather than reopening TASK-006.

## Key Paths

- Closeout proof: `artifacts/proofs/task-006-comparison-closeout-check.json`
- Closeout summary: `artifacts/proofs/task-006-comparison-closeout-summary.md`
- Status report: `artifacts/reports/task-006-replay-validation-status.md`
- Downstream analysis proof: `artifacts/proofs/task-006-downstream-comparative-analysis-check.json`
- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Confirmatory comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180604Z-comparison`
