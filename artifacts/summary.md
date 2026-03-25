# TASK-006-RESEARCH-HANDOFF Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#26` merge commit `9d235176e628e0fcbdcf2182ce83def25f6a6b02` on `2026-03-25T22:05:02Z`.
- Supporting merged Vexter states remained PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Took the comparison closeout outputs as the formal handoff source of truth for downstream research.
- Kept the promoted baseline fixed without reopening evidence collection or changing Dexter, Mew-X, or validator logic.
- Organized the final comparison conclusion, caveats, residual treatment, artifact surfaces, and "do not redo" guidance into a direct-use handoff package.
- Refreshed TASK-006 summary, context pack, proof manifest, task ledger, status, report, and bundle outputs for downstream use.

## Frozen Comparative Conclusion

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Promoted live winner mode: `derived`
- Promoted replay winner mode: `derived`
- Stable scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Confirmatory residual: `Mew-X candidate_rejected`
- Confirmatory residual overturns promoted baseline: `no`

Inference from the handoff source of truth:

- Dexter remains stronger on candidate generation, signal-to-attempt latency, slippage, favorable excursion, realized exit, and stale-position control.
- Mew-X remains stronger on fill latency, drawdown containment, time-to-peak, and realized-vs-peak retention.
- `winner_mode: derived` remains a component-level comparison surface rather than a scalar overall winner field.

## Remaining Caveats

- Current replay parity is scoped to close-summary / `position_closed` realized-return fidelity, not a full path-equivalence claim.
- Dexter still shows one path-sensitive derived-metric drift between live and replay: `realized_vs_peak_gap_pct` changes from `20.5330` live to `25.8042` replay even though the measured close-return gap is `0.0000`.
- Mew-X `candidate_precision_proxy` remains unavailable because `creator_candidate` is absent under the frozen export surface.

## Downstream Use

- Use `artifacts/reports/task-006-research-handoff-report.md` as the primary handoff narrative.
- Use `artifacts/proofs/task-006-research-handoff-check.json` as the machine-readable source of truth.
- Reuse the promoted live, repaired replay, and confirmatory comparison directories as backing evidence surfaces.
- Do not rerun baseline selection, evidence collection, or source / validator edits unless contradictory evidence appears.

## Decision

- Outcome: `A`
- Key finding: `research_handoff_completed`
- Current task status: `research_handoff_completed`
- Comparison source-of-truth state: `comparison_closed_out`
- Downstream research handoff ready: `yes`
- New evidence collection required: `no`

## Key Paths

- Research handoff report: `artifacts/reports/task-006-research-handoff-report.md`
- Research handoff status: `artifacts/reports/task-006-research-handoff-status.md`
- Research handoff proof: `artifacts/proofs/task-006-research-handoff-check.json`
- Research handoff summary: `artifacts/proofs/task-006-research-handoff-summary.md`
- Research handoff prompt pack: `artifacts/reports/task-006-research-handoff`
- Comparison closeout report: `artifacts/reports/task-006-comparison-closeout.md`
- Handoff bundle: `artifacts/bundles/task-006-research-handoff.tar.gz`
