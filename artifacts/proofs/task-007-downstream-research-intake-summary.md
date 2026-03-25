# TASK-007 Downstream Research Intake

## Verified GitHub State

- Latest merged Vexter `main`: PR `#27` at `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`
- Dexter pinned `main`: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Formal research handoff report: `artifacts/reports/task-006-research-handoff-report.md`
- Formal comparison closeout report: `artifacts/reports/task-006-comparison-closeout.md`
- Confirmatory residual: `Mew-X candidate_rejected`

## Research Intake Result

- Live winner mode: `derived`
- Replay winner mode: `derived`
- Live scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Replay scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Priority lanes: `candidate_generation_vs_quality`, `execution_timing_vs_retention`, `risk_containment_vs_exit_capture`, `path_sensitive_retention_scope`

## Caveat

- Replay parity is scoped to close-summary and `position_closed` realized-return fidelity, not full path equivalence.
- Dexter `realized_vs_peak_gap_pct` still differs between live `20.5330` and replay `25.8042`.
- Mew-X candidate-generation precision remains asymmetric because `creator_candidate` is absent on the frozen export surface.

## Decision

- Key finding: `research_intake_ready`
- Current task state: `research_intake_ready`
- Next step: `hypothesis_specific_research`
- Next research workstream ready: `yes`
