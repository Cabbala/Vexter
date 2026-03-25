# TASK-006 Replay And Comparison Status

## Verified Start

- Vexter `origin/main` verified at PR `#24` merge commit `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`
- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Current Result

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
- Remaining caveat: replay parity is scoped to close-summary / `position_closed` realized-return fidelity

## Decision

- TASK-006: `comparison_closeout_ready`
- Key finding: `comparison_closeout_ready`
- Next step: `task_006_comparison_closeout`
- Downstream research handoff ready: `yes`

The repaired replay surface leaves the promoted cross-source interpretation stable rather than reopening it. Dexter still leads on candidate generation, signal-to-attempt latency, slippage, realized exit, favorable excursion, and stale-position control; Mew-X still leads on fill latency, drawdown containment, time-to-peak, and realized-vs-peak retention. The only remaining confirmatory miss is Mew-X `candidate_rejected`, and it does not overturn the promoted baseline.
