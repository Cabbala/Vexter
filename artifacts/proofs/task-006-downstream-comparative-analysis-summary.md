# TASK-006 Downstream Comparative Analysis

## Verified GitHub State

- Latest merged Vexter `main`: PR `#24` at `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`
- Dexter pinned `main`: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Promoted Baseline

- Live comparison pack: `task005-validator-rule-implement-20260325T180027Z-comparison`
- Repaired replay comparison pack: `task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Confirmatory residual: `Mew-X candidate_rejected`

## Comparative Result

- Live winner mode: `derived`
- Replay winner mode: `derived`
- Live scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Replay scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`

## Caveat

- Current zero-gap evidence is scoped to close-summary and `position_closed` realized-return fidelity, not full path equivalence.
- Dexter `realized_vs_peak_gap_pct` still differs between live `20.5330` and replay `25.8042`.

## Decision

- Key finding: `comparison_closeout_ready`
- TASK-006 state: `comparison_closeout_ready`
- Next step: `task_006_comparison_closeout`
- Downstream research handoff ready: `yes`
