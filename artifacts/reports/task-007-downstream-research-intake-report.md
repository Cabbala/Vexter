# TASK-007-DOWNSTREAM-RESEARCH-INTAKE

## Scope

This task starts from merged PR `#27` and the completed `TASK-006` research handoff package. Its job is not to reopen comparison work, but to turn the frozen comparison conclusion into a direct-use operating intake for downstream research without changing Dexter, Mew-X, validator rules, or frozen source pins.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#27`, merge commit `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`, merged at `2026-03-25T22:17:31Z`
- Supporting merged Vexter states: PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Intake Source Of Truth

- Formal research handoff report: `artifacts/reports/task-006-research-handoff-report.md`
- Formal research handoff proof: `artifacts/proofs/task-006-research-handoff-check.json`
- Formal comparison closeout report: `artifacts/reports/task-006-comparison-closeout.md`
- Formal comparison closeout proof: `artifacts/proofs/task-006-comparison-closeout-check.json`
- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted repaired replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Confirmatory comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180604Z-comparison`

Intake rule:

- Treat `TASK-006` research handoff plus comparison closeout as the fixed comparison input surface.
- Treat the promoted baseline as frozen unless contradictory evidence appears.
- Do not reopen evidence collection or comparison-layer logic as part of this intake.

## Fixed Facts And Assumptions

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

Dexter strengths that stay fixed for research intake:

- `candidate_count`
- `signal_to_attempt_latency_ms`
- `quote_vs_fill_slippage_bps`
- `max_favorable_excursion_pct`
- `realized_exit_pct`
- `stale_position_ratio`

Mew-X strengths that stay fixed for research intake:

- `attempt_to_fill_latency_ms`
- `max_adverse_excursion_pct`
- `time_to_peak_ms`
- `realized_vs_peak_gap_pct`

Ties that stay fixed for research intake:

- `fill_success_rate`
- `replayability_grade`

Assumptions research should preserve:

- `winner_mode: derived` is a component-level comparison surface, not a scalar overall winner.
- Replay parity is a close-summary / `position_closed` realized-return fidelity claim, not a full path-equivalence claim.
- Dexter still shows path-sensitive drift in `realized_vs_peak_gap_pct` (`20.5330` live versus `25.8042` replay).
- Mew-X `candidate_precision_proxy` remains unavailable because `creator_candidate` is absent under the frozen export surface.

## Comparison / Research Boundary

Research workstream may do the following:

- Interpret the fixed comparison tradeoffs in terms of research priorities and downstream objective functions.
- Reuse promoted live, repaired replay, and confirmatory comparison surfaces as evidence inputs.
- Decide which hypothesis lane deserves the next dedicated task.
- Define what evidence would be required for a future deeper claim.

Research workstream must not do the following inside this intake:

- Do not rerun promoted-baseline selection.
- Do not reopen evidence collection on current facts.
- Do not change Dexter, Mew-X, or validator rules.
- Do not widen replay parity to full execution-path equivalence.
- Do not convert `winner_mode: derived` into a scalar overall winner claim.
- Do not use funded live trading as part of intake.

## Priority Research Questions

### `candidate_generation_vs_quality`

- Question: How much of Dexter's `candidate_count` lead converts into realized edge rather than simple breadth?
- Working hypothesis: Dexter's upstream candidate volume plus its slippage and realized-exit lead suggest real edge conversion on the promoted baseline, but cross-source candidate-quality claims remain bounded because Mew-X `candidate_precision_proxy` is unavailable.
- Required evidence: promoted live and replay comparison matrices, candidate snapshot surfaces, session summaries, and close-summary outcome metrics.
- Non-goal: do not infer missing Mew-X candidate precision from absent `creator_candidate` exports.

### `execution_timing_vs_retention`

- Question: Is the main cross-source tradeoff Dexter's signal-to-attempt/slippage advantage versus Mew-X's attempt-to-fill and retention advantage once an attempt is placed?
- Working hypothesis: Dexter wins earlier in the pipeline, while Mew-X wins later in the path by filling faster after attempt and retaining more local peak performance.
- Required evidence: promoted live and replay metric tables, session-level timing fields, and exit/peak summary metrics already exported in the current packs.
- Non-goal: do not change entry thresholds, trust logic, or routing semantics while evaluating this lane.

### `risk_containment_vs_exit_capture`

- Question: Which source should downstream planning prefer once the objective function explicitly weights drawdown containment against favorable excursion and realized exit?
- Working hypothesis: There is no missing comparison evidence here; the next decision is likely objective-dependent rather than evidence-blocked.
- Required evidence: current metric surfaces plus downstream strategy or execution-planning objective weights.
- Non-goal: do not claim a universal winner without an explicit objective function.

### `path_sensitive_retention_scope`

- Question: Does any next claim require path-level evidence beyond the current close-summary replay scope?
- Working hypothesis: Current facts are enough for research intake and planning, but any stronger claim about exit-path retention or path equivalence should become a separate future evidence task rather than a reopen of `TASK-006`.
- Required evidence: current replay-scope caveat, promoted replay comparison, and, only if this lane is selected, a separate path-equivalence evidence design.
- Non-goal: do not treat the existing Dexter `realized_vs_peak_gap_pct` drift as proof that current close-summary parity is invalid.

## Required Evidence Types

- Comparison matrices and summary metrics from the promoted live and repaired replay packs
- Candidate snapshot and refresh export surfaces already committed in the promoted packages
- Session summaries and `position_closed` close-summary metrics already committed in the promoted packages
- Confirmatory residual context from the confirmatory comparison pack
- Explicit downstream objective weighting if research is choosing between risk containment and exit capture
- A separate future path-equivalence evidence design only if the path-sensitive lane is explicitly selected

## Artifact Surfaces To Reuse

Primary intake surfaces:

- `artifacts/reports/task-007-downstream-research-intake-report.md`
- `artifacts/reports/task-007-downstream-research-intake-status.md`
- `artifacts/proofs/task-007-downstream-research-intake-check.json`
- `artifacts/proofs/task-007-downstream-research-intake-summary.md`

Fixed input surfaces:

- `artifacts/reports/task-006-research-handoff-report.md`
- `artifacts/proofs/task-006-research-handoff-check.json`
- `artifacts/proofs/task-006-research-handoff-summary.md`
- `artifacts/reports/task-006-comparison-closeout.md`
- `artifacts/proofs/task-006-comparison-closeout-check.json`

Supporting evidence surfaces:

- `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- `artifacts/reports/task005-validator-rule-implement-20260325T180604Z-comparison`

## What Must Not Be Rerun

- Do not rerun live collection or replay collection on current facts.
- Do not rerun validator or source-rule changes.
- Do not rerun baseline selection or comparison-closeout judgment.
- Do not rerun replay-gap interpretation unless a separate path-equivalence task is approved.

## Decision

- Outcome: `A`
- Key finding: `research_intake_ready`
- Current task state: `research_intake_ready`
- Comparison source-of-truth state: `comparison_closed_out`
- Next research workstream ready: `yes`
- New evidence collection: `not recommended`

Evidence-based next cut:

- Pick one of the four hypothesis lanes and cut a hypothesis-specific research, strategy-planning, or execution-planning task from this intake surface.
- Keep the comparison baseline frozen while doing so.

## Key Paths

- Research intake proof: `artifacts/proofs/task-007-downstream-research-intake-check.json`
- Research intake summary: `artifacts/proofs/task-007-downstream-research-intake-summary.md`
- Research intake status: `artifacts/reports/task-007-downstream-research-intake-status.md`
- Research intake prompt pack: `artifacts/reports/task-007-downstream-research-intake`
- Research handoff proof: `artifacts/proofs/task-006-research-handoff-check.json`
- Comparison closeout proof: `artifacts/proofs/task-006-comparison-closeout-check.json`
- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
