# TASK-007 Risk Containment Vs Exit Capture Status

## Verified Start

- Vexter `origin/main` verified at PR `#30` merge commit `052de6ccecef1461d2291fb4f0ef5fbf8883d548`
- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Current Result

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior lane source state: `timing_retention_tradeoff_supported`
- Promoted live comparison winner mode: `derived`
- Promoted replay comparison winner mode: `derived`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Price-path containment split: Mew-X MAE `0.0 pct`, time-to-peak `20.5 ms`, realized-vs-peak gap `0.0 pct`
- Exit-capture split: Dexter MFE `34.8443 pct`, realized exit `7.1641 pct`, slippage `0.0 bps`
- Lifecycle-control split: Dexter stale `0.00%` with `safe=2` and `malicious=2`; Mew-X stale `100.00%` with `inactivity_timeout=6`
- Mew-X timeout shape: peak-to-close windows remain clustered at `5013-5028 ms`
- Remaining replay caveat: Dexter `realized_vs_peak_gap_pct` stays path-sensitive at `20.5330` live vs `25.8042` replay

## Decision

- Current task: `risk_exit_tradeoff_supported`
- Key finding: `risk_exit_tradeoff_supported`
- Claim boundary: `tradeoff_bounded`
- Recommended next step: `strategy_planning`
- Decision: `planning_ready`

The bounded interpretation is now stable on committed evidence only: Mew-X owns price-path drawdown containment and local-peak retention, while Dexter owns realized exit capture and stale-position control. That makes objective weighting the next blocker, so `strategy_planning` is the right next cut before any execution-level design work.
