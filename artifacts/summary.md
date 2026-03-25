# TASK-006-COMPARISON-CLOSEOUT Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#25` merge commit `727589b40d26c453c2fef78dc5060aa1098c1aad` on `2026-03-25T21:43:44Z`.
- Supporting merged Vexter states remained PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Took the merged downstream comparative analysis outputs as the formal closeout source of truth for TASK-006.
- Fixed the promoted live / repaired replay baseline as the frozen comparison conclusion without changing Dexter or Mew-X source logic.
- Consolidated the final comparative conclusion, residual handling, remaining caveats, and research handoff facts into one closeout surface.
- Refreshed TASK-006 summary, context pack, status, proof manifest, handoff, and bundle outputs for final downstream use.

## Final Comparative Conclusion

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Promoted live winner mode: `derived`
- Promoted replay winner mode: `derived`
- Stable scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Confirmatory residual: `Mew-X candidate_rejected`
- Confirmatory residual overturns promoted baseline: `no`

Inference from the closeout proof:

- Dexter remains stronger on candidate generation, signal-to-attempt latency, slippage, favorable excursion, realized exit, and stale-position control.
- Mew-X remains stronger on fill latency, drawdown containment, time-to-peak, and realized-vs-peak retention.
- The stable live / replay split means the promoted baseline is now suitable as a frozen downstream comparison source of truth rather than only a provisional analysis input.

## Remaining Caveat

- Current replay parity is scoped to close-summary / `position_closed` realized-return fidelity, not a full path-equivalence claim.
- Dexter still shows one path-sensitive derived-metric drift between live and replay: `realized_vs_peak_gap_pct` changes from `20.5330` live to `25.8042` replay even though the measured close-return gap is `0.0000`.
- Mew-X `candidate_precision_proxy` remains unavailable because `creator_candidate` is absent under the frozen export surface.

## Decision

- Outcome: `A`
- Key finding: `comparison_closed_out`
- TASK-006 status: `comparison_closed_out`
- Downstream research handoff ready: `yes`
- New evidence collection required: `no`

## Key Paths

- Closeout report: `artifacts/reports/task-006-comparison-closeout.md`
- Updated status report: `artifacts/reports/task-006-replay-validation-status.md`
- Closeout proof: `artifacts/proofs/task-006-comparison-closeout-check.json`
- Closeout summary: `artifacts/proofs/task-006-comparison-closeout-summary.md`
- Handoff: `artifacts/reports/task-006-comparison-closeout-handoff`
- Handoff bundle: `artifacts/bundles/task-006-comparison-closeout.tar.gz`
