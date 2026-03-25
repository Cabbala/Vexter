# TASK-007 Downstream Research Intake Status

## Verified Start

- Vexter `origin/main` verified at PR `#27` merge commit `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`
- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Current Result

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Research handoff source state: `research_handoff_completed`
- Promoted live comparison winner mode: `derived`
- Promoted replay comparison winner mode: `derived`
- Live scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Replay scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Confirmatory residual overturning: `no`
- Confirmatory residual note: `Mew-X candidate_rejected`
- Dexter replay coverage: `100.00%`
- Dexter `live_vs_replay_gap_pct`: `0.0000`
- Mew-X replay coverage: `100.00%`
- Mew-X `live_vs_replay_gap_pct`: `0.0000`
- Remaining replay caveat: close-summary / `position_closed` realized-return fidelity only
- Hypothesis lanes defined: `4`
- Primary intake surfaces ready: `yes`

## Priority Lanes

- `candidate_generation_vs_quality`
- `execution_timing_vs_retention`
- `risk_containment_vs_exit_capture`
- `path_sensitive_retention_scope`

## Decision

- Current task: `research_intake_ready`
- Key finding: `research_intake_ready`
- Next step: `hypothesis_specific_research`
- Next research workstream ready: `yes`

The comparison workstream is now explicitly closed off from downstream research intake. Downstream teams can reuse the frozen promoted baseline, repaired replay parity, stable metric split, confirmatory residual treatment, and scope caveats as fixed inputs, then choose one hypothesis lane for the next dedicated task without reopening `TASK-006`.
