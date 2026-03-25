# TASK-006 Comparison Closeout

## Verified GitHub State

- Latest merged Vexter `main`: PR `#25` at `727589b40d26c453c2fef78dc5060aa1098c1aad`
- Dexter pinned `main`: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Formal Source Of Truth

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Live comparison pack: `task005-validator-rule-implement-20260325T180027Z-comparison`
- Repaired replay comparison pack: `task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Confirmatory residual: `Mew-X candidate_rejected`

## Final Conclusion

- Live winner mode: `derived`
- Replay winner mode: `derived`
- Live scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Replay scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`

## Caveat

- Replay parity is scoped to close-summary and `position_closed` realized-return fidelity, not full path equivalence.
- Dexter `realized_vs_peak_gap_pct` still differs between live `20.5330` and replay `25.8042`.
- Mew-X candidate-generation precision remains asymmetric because `creator_candidate` is absent on the frozen export surface.

## Decision

- Key finding: `comparison_closed_out`
- TASK-006 state: `comparison_closed_out`
- Next step: `research_handoff`
- Downstream research handoff ready: `yes`
