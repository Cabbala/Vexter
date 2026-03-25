# TASK-006 Research Handoff

## Verified GitHub State

- Latest merged Vexter `main`: PR `#26` at `9d235176e628e0fcbdcf2182ce83def25f6a6b02`
- Dexter pinned `main`: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Frozen Source Of Truth

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Formal closeout report: `artifacts/reports/task-006-comparison-closeout.md`
- Formal closeout proof: `artifacts/proofs/task-006-comparison-closeout-check.json`
- Confirmatory residual: `Mew-X candidate_rejected`

## Handed-Off Conclusion

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

- Key finding: `research_handoff_completed`
- Current task state: `research_handoff_completed`
- Next step: `downstream_research`
- Downstream research handoff ready: `yes`
