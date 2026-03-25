# TASK-007 Execution Timing Vs Retention Status

## Verified Start

- Vexter `origin/main` verified at PR `#29` merge commit `17af013b0383fd142e15932108c8b4da5447f1f7`
- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Current Result

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior lane source state: `candidate_edge_supported`
- Promoted live comparison winner mode: `derived`
- Promoted replay comparison winner mode: `derived`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Timing split: Dexter signal-to-attempt `0.0 ms` vs Mew-X `891.0 ms`; Mew-X attempt-to-fill `1.5 ms` vs Dexter `502.5 ms`
- Slippage split: Dexter `0.0 bps` vs Mew-X `7.7061 bps`
- Exit split: Dexter realized `7.1641 pct`, MFE `34.8443 pct`, stale `0.00%`
- Retention split: Mew-X MAE `0.0 pct`, time-to-peak `20.5 ms`, realized-vs-peak gap `0.0 pct`
- Mew-X close pattern: all `6` closes end as `inactivity_timeout`
- Dexter close pattern: `2` `safe`, `2` `malicious`, zero stale closes
- Remaining replay caveat: Dexter `realized_vs_peak_gap_pct` stays path-sensitive at `20.5330` live vs `25.8042` replay

## Decision

- Current task: `timing_retention_tradeoff_supported`
- Key finding: `timing_retention_tradeoff_supported`
- Claim boundary: `tradeoff_bounded`
- Recommended next lane: `risk_containment_vs_exit_capture`
- Decision: `next_lane_ready`

The bounded interpretation is now stable on committed evidence only: Dexter owns the earlier timing, slippage, realized-exit, and stale-control surfaces, while Mew-X owns faster post-attempt fill, lower drawdown, faster peak discovery, and tighter local-peak retention. That makes the next unresolved question an explicit risk-containment versus exit-capture weighting problem rather than another generic timing debate.
