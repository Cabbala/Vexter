# TASK-007-EXECUTION-PLANNING Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#32` merge commit `a214ff04f0662e250b01181551a8963ce8e80dd6` on `2026-03-25T23:52:42Z`.
- Supporting merged Vexter states remained PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`, PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`, PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`, PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`, PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`, PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Started from the merged `strategy_planning` lane and kept the promoted comparison baseline frozen.
- Reused only the fixed candidate, timing, risk, and strategy outputs already visible in GitHub artifacts.
- Converted those confirmed conclusions into an execution-level design surface that fixes the default anchor, the bounded Mew-X selective role, routing scope, and next-step choice.

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Promoted live winner mode: `derived`
- Promoted replay winner mode: `derived`
- Stable scored-metric split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Confirmatory residual: `Mew-X candidate_rejected`
- Confirmatory residual overturns promoted baseline: `no`

## Execution Planning Surface

- Default execution anchor: prefer Dexter. Dexter remains the only current source that jointly owns upstream opportunity capture, low-slippage entry, realized exit capture, and stale-risk avoidance.
- Selective containment option: prefer Mew-X only when the strategy explicitly prioritizes drawdown containment, fast post-attempt fill, and local-peak retention above realized exit capture and active lifecycle control.
- Supported routing: objective-conditioned route selection or portfolio split using separate sleeves. Routing should happen before execution begins, not as in-run source fusion.
- Unsupported routing: mid-trade handoff, threshold transplant, trust-logic transplant, or any claim that a fused engine is already proven superior on current evidence.
- Default routing rule: if objective weights are mixed or unspecified, route to Dexter by default.

## Execution Assumptions Fixed Now

- Dexter should remain the default execution anchor whenever objective weights are mixed or unspecified.
- Mew-X should remain a containment-first selective option rather than a general fallback.
- No new evidence is required to move from this task into implementation planning.
- No validator, Dexter, or Mew-X source logic changes are justified by this planning task.
- Replay parity remains bounded to close-summary / realized-return fidelity and does not block bounded execution planning.
- `path_sensitive_retention_scope` remains optional unless a later design tries to claim stronger retention equivalence than current evidence supports.

## Still Open Execution Questions

- The exact config surface that declares an objective profile and routes into a Dexter or Mew-X sleeve.
- The portfolio budget or capital split between Dexter-default and Mew-X-selective sleeves.
- The monitoring and kill-switch rules around timeout-shaped Mew-X lifecycle behavior.
- The exact abstraction boundary between a planner/router layer and source-specific executors.

## Non-Goals and Bounds

- Do not reopen promoted-baseline selection.
- Do not collect new live or replay evidence.
- Do not change Dexter, Mew-X, or validator rules.
- Keep replay parity scoped to close-summary / `position_closed` realized-return fidelity, not full path equivalence.
- Keep Dexter `realized_vs_peak_gap_pct` drift and unavailable Mew-X `candidate_precision_proxy` as explicit execution-planning caveats.

## Decision

- Outcome: `A`
- Key finding: `execution_plan_ready`
- Claim boundary: `execution_plan_bounded`
- Current task status: `execution_plan_ready`
- Recommended next step: `implementation_planning`
- Decision: `implementation_planning_ready`

## Key Paths

- Execution planning report: `artifacts/reports/task-007-execution-planning-report.md`
- Execution planning status: `artifacts/reports/task-007-execution-planning-status.md`
- Execution planning proof: `artifacts/proofs/task-007-execution-planning-check.json`
- Execution planning summary: `artifacts/proofs/task-007-execution-planning-summary.md`
- Execution planning prompt pack: `artifacts/reports/task-007-execution-planning`
- Execution planning bundle: `artifacts/bundles/task-007-execution-planning.tar.gz`
