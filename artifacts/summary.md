# TASK-007-DOWNSTREAM-RESEARCH-INTAKE Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#27` merge commit `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df` on `2026-03-25T22:17:31Z`.
- Supporting merged Vexter states remained PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Took the completed `TASK-006` research handoff package as the formal downstream input surface.
- Kept the promoted baseline fixed without reopening evidence collection or changing Dexter, Mew-X, or validator logic.
- Turned the frozen comparison conclusion into an operating research intake with explicit scope, fixed assumptions, non-goals, reusable artifact surfaces, and rerun prohibitions.
- Defined the first priority research questions, hypothesis lanes, and required evidence types for downstream work.
- Refreshed TASK-007 summary, context pack, proof manifest, task ledger, status, report, prompt pack, and bundle outputs for direct reuse.

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Promoted live winner mode: `derived`
- Promoted replay winner mode: `derived`
- Stable scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Confirmatory residual: `Mew-X candidate_rejected`
- Confirmatory residual overturns promoted baseline: `no`

Inference from the frozen source of truth:

- Dexter remains stronger on candidate generation, signal-to-attempt latency, slippage, favorable excursion, realized exit, and stale-position control.
- Mew-X remains stronger on fill latency, drawdown containment, time-to-peak, and realized-vs-peak retention.
- `winner_mode: derived` remains a component-level comparison surface rather than a scalar overall winner field.

## Comparison / Research Boundary

- Comparison work is closed; research must treat the promoted baseline, repaired replay parity, and residual handling as fixed inputs.
- Research may interpret tradeoffs, choose objective functions, and define targeted next questions, but it must not rerun baseline selection, reopen evidence collection, or change frozen source or validator behavior.
- Replay parity remains scoped to close-summary / `position_closed` realized-return fidelity, not full path equivalence.
- Dexter still shows path-sensitive drift in `realized_vs_peak_gap_pct` (`20.5330` live versus `25.8042` replay), and Mew-X `candidate_precision_proxy` remains unavailable under the frozen export surface.

## Priority Research Questions

- `candidate_generation_vs_quality`: How much of Dexter's candidate-count lead converts into usable edge rather than just wider opportunity breadth?
- `execution_timing_vs_retention`: Is the core tradeoff Dexter's upstream reaction/slippage advantage versus Mew-X's fill-speed and retention advantage once an attempt is placed?
- `risk_containment_vs_exit_capture`: Which source looks preferable once downstream work applies an explicit objective weighting between drawdown containment and realized upside capture?
- `path_sensitive_retention_scope`: Does any next claim require path-level evidence beyond the current close-summary replay scope, or is the current scope sufficient for planning?

## Required Evidence And Reuse

- Reuse `artifacts/reports/task-007-downstream-research-intake-report.md` and `artifacts/proofs/task-007-downstream-research-intake-check.json` as the primary intake surfaces.
- Reuse `artifacts/reports/task-006-research-handoff-report.md` and `artifacts/proofs/task-006-research-handoff-check.json` as the frozen handoff basis.
- Reuse the promoted live and repaired replay comparison directories plus the confirmatory comparison directory as the only approved evidence surfaces for current research intake.
- Use candidate snapshots, session summaries, comparison matrices, and close-summary metrics as the allowed evidence types on the current intake surface.
- If a lane truly needs path equivalence or missing Mew-X candidate-quality exports, cut a separate future task instead of widening claims inside this intake.

## Decision

- Outcome: `A`
- Key finding: `research_intake_ready`
- Current task status: `research_intake_ready`
- Comparison source-of-truth state: `comparison_closed_out`
- Next research workstream ready: `yes`
- New evidence collection required: `no`

## Key Paths

- Research intake report: `artifacts/reports/task-007-downstream-research-intake-report.md`
- Research intake status: `artifacts/reports/task-007-downstream-research-intake-status.md`
- Research intake proof: `artifacts/proofs/task-007-downstream-research-intake-check.json`
- Research intake summary: `artifacts/proofs/task-007-downstream-research-intake-summary.md`
- Research intake prompt pack: `artifacts/reports/task-007-downstream-research-intake`
- Research handoff report: `artifacts/reports/task-006-research-handoff-report.md`
- Comparison closeout report: `artifacts/reports/task-006-comparison-closeout.md`
- Intake bundle: `artifacts/bundles/task-007-downstream-research-intake.tar.gz`
