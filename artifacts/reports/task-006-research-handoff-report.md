# TASK-006-RESEARCH-HANDOFF

## Scope

This task starts from merged PR `#26` and the already closed-out comparison baseline. Its job is not to reopen comparison work, but to turn the frozen comparison conclusion into the final downstream research handoff package without changing Dexter, Mew-X, or validator logic.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#26`, merge commit `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, merged at `2026-03-25T22:05:02Z`
- Supporting merged Vexter states: PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Handoff Source Of Truth

- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted repaired replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Formal comparison closeout report: `artifacts/reports/task-006-comparison-closeout.md`
- Formal comparison closeout proof: `artifacts/proofs/task-006-comparison-closeout-check.json`
- Confirmatory comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180604Z-comparison`

Handoff rule:

- Treat the comparison closeout outputs as the frozen source of truth.
- Treat the promoted baseline as fixed unless contradictory evidence appears.
- Do not reopen evidence collection or comparison-layer changes as part of downstream research intake.

## Fixed Comparative Conclusion

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Promoted live pack: `pass/pass`, `winner_mode: derived`
- Promoted repaired replay pack: `pass/pass`, `winner_mode: derived`
- Stable scored-metric split across live and replay:
  - Dexter leads `6`
  - Mew-X leads `4`
  - tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Confirmatory residual: `Mew-X candidate_rejected`
- Confirmatory residual overturns promoted baseline: `no`

Dexter strengths to carry downstream:

- `candidate_count`
- `signal_to_attempt_latency_ms`
- `quote_vs_fill_slippage_bps`
- `max_favorable_excursion_pct`
- `realized_exit_pct`
- `stale_position_ratio`

Mew-X strengths to carry downstream:

- `attempt_to_fill_latency_ms`
- `max_adverse_excursion_pct`
- `time_to_peak_ms`
- `realized_vs_peak_gap_pct`

Ties to carry downstream:

- `fill_success_rate`
- `replayability_grade`

Interpretation:

- Dexter remains stronger on candidate generation, entry immediacy, slippage control, favorable excursion, realized exit, and stale-position control.
- Mew-X remains stronger on fill latency after attempt, drawdown containment, faster peak realization, and realized-vs-peak retention.
- `winner_mode: derived` continues to mean component-level tradeoff surface, not a scalar overall winner.

## Residual And Caveats

### Confirmatory residual

- Confirmatory pair: `task005-pass-grade-pair-20260325T180604Z`
- Remaining confirmatory miss: `candidate_rejected`
- Treatment: carry as a narrow caveat only
- Downstream implication: do not reopen the promoted baseline on this fact alone

### Scope caveats

- Replay parity remains a close-summary / `position_closed` realized-return fidelity claim, not a full execution-path equivalence claim.
- Dexter still shows one path-sensitive derived-metric drift: `realized_vs_peak_gap_pct` is `20.5330` on live and `25.8042` on replay even while realized-return gap is `0.0000`.
- Mew-X candidate-generation precision remains asymmetric because `candidate_precision_proxy` cannot be computed when `creator_candidate` is absent under the frozen export surface.

## Artifact Surfaces For Downstream Research

Primary decision surfaces:

- `artifacts/reports/task-006-research-handoff-report.md`
- `artifacts/proofs/task-006-research-handoff-check.json`
- `artifacts/proofs/task-006-research-handoff-summary.md`
- `artifacts/reports/task-006-research-handoff-status.md`

Supporting evidence surfaces:

- `artifacts/reports/task-006-comparison-closeout.md`
- `artifacts/proofs/task-006-comparison-closeout-check.json`
- `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- `artifacts/reports/task005-validator-rule-implement-20260325T180604Z-comparison`

Bundle surface:

- `artifacts/bundles/task-006-research-handoff.tar.gz`

## What Downstream Does Not Need To Redo

- Do not rerun promoted-baseline selection.
- Do not rerun live evidence collection on current facts.
- Do not rerun replay gap analysis unless a new claim requires path equivalence.
- Do not change Dexter, Mew-X, or validator rules as part of this handoff.
- Do not reinterpret `winner_mode: derived` as a scalar overall winner.

## Decision

- Outcome: `A`
- Key finding: `research_handoff_completed`
- Current task state: `research_handoff_completed`
- Comparison source-of-truth state: `comparison_closed_out`
- Downstream research handoff: `ready`
- New evidence collection: `not recommended`

Evidence-based next cut:

- Hand this package to downstream research, strategy, or execution-planning work without reopening TASK-006 comparison work.
- If stronger replay claims are needed later, cut a separate path-equivalence task rather than revisiting this handoff baseline.

## Key Paths

- Research handoff proof: `artifacts/proofs/task-006-research-handoff-check.json`
- Research handoff summary: `artifacts/proofs/task-006-research-handoff-summary.md`
- Research handoff status: `artifacts/reports/task-006-research-handoff-status.md`
- Research handoff prompt pack: `artifacts/reports/task-006-research-handoff`
- Comparison closeout proof: `artifacts/proofs/task-006-comparison-closeout-check.json`
- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Confirmatory comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180604Z-comparison`
