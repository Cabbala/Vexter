# TASK-007-DOWNSTREAM-RESEARCH-INTAKE Package

## Verified GitHub State

- Vexter latest merged `main`: PR `#27`, `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`
- Supporting Vexter states: PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Package Does

- Treats `TASK-006` research handoff as the formal input surface for downstream research
- Preserves the comparison closeout facts, caveats, and residual treatment without changing source logic
- Defines the comparison-versus-research boundary explicitly
- Packages fixed assumptions, non-goals, research questions, hypothesis lanes, required evidence, and reusable artifact surfaces

## Key Finding

- `research_intake_ready`

## Frozen Input Surface

- Selected outcome: `A`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Promoted live winner mode: `derived`
- Promoted replay winner mode: `derived`
- Stable scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Confirmatory residual: `Mew-X candidate_rejected`
- Current task status: `research_intake_ready`

## Priority Hypothesis Lanes

- `candidate_generation_vs_quality`
- `execution_timing_vs_retention`
- `risk_containment_vs_exit_capture`
- `path_sensitive_retention_scope`

## Artifact Surfaces To Use

- `artifacts/reports/task-007-downstream-research-intake-report.md`
- `artifacts/reports/task-007-downstream-research-intake-status.md`
- `artifacts/proofs/task-007-downstream-research-intake-check.json`
- `artifacts/proofs/task-007-downstream-research-intake-summary.md`
- `artifacts/reports/task-006-research-handoff-report.md`
- `artifacts/proofs/task-006-research-handoff-check.json`
- `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- `artifacts/reports/task005-validator-rule-implement-20260325T180604Z-comparison`

## What Not To Redo

- Do not reopen evidence collection.
- Do not rerun promoted-baseline selection.
- Do not widen the replay claim to full path equivalence.
- Do not change Dexter, Mew-X, or validator rules during intake.
- Do not declare a scalar overall winner from `winner_mode: derived`.

## Recommended Next Step

- Start a hypothesis-specific research, strategy-planning, or execution-planning task from one defined lane.
- Keep the replay claim scoped to close-summary and `position_closed` realized-return fidelity.
- Keep the confirmatory `candidate_rejected` miss as a narrow caveat unless contradictory evidence appears.
