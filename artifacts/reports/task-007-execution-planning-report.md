# TASK-007-EXECUTION-PLANNING

## Scope

This task starts from merged PR `#32` and the completed `TASK-007-STRATEGY-PLANNING` lane. It keeps the promoted comparison baseline frozen and asks a single bounded question:

- Given the fixed objective-weighted strategy conclusion, what execution-level design surface is source-faithful without reopening comparison work or changing frozen source logic?

The task stays intentionally narrow:

- no new evidence collection
- no validator or source changes
- no baseline reopen
- no threshold transplant
- only minimal reaggregation of the already committed comparison, strategy, and lane outputs visible on GitHub

## Verified GitHub State

- Latest merged Vexter `main`: PR `#32`, merge commit `a214ff04f0662e250b01181551a8963ce8e80dd6`, merged at `2026-03-25T23:52:42Z`
- Supporting merged Vexter states: PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Strategy planning source of truth: `artifacts/reports/task-007-strategy-planning-report.md`
- Candidate lane source of truth: `artifacts/reports/task-007-candidate-generation-vs-quality-report.md`
- Timing lane source of truth: `artifacts/reports/task-007-execution-timing-vs-retention-report.md`
- Risk lane source of truth: `artifacts/reports/task-007-risk-containment-vs-exit-capture-report.md`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from closeout and strategy planning:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- Dexter-favored objectives: `upstream_opportunity_capture`, `low_slippage_entry`, `realized_exit_capture`, `stale_risk_avoidance`
- Mew-X-favored objectives: `drawdown_containment`, `local_peak_retention`
- default primary planning source: `Dexter`
- supported hybrid scope: `selective_adoption_or_objective_conditioned_portfolio_split`
- replay parity still remains bounded to close-summary / `position_closed` realized-return fidelity
- Dexter `realized_vs_peak_gap_pct` remains path-sensitive
- Mew-X `candidate_precision_proxy` remains unavailable

## Execution-Level Design Surface

### Default execution anchor

Primary execution anchor: `Dexter`

Why that remains source-faithful at execution level:

- Dexter is the only current source that simultaneously owns upstream opportunity capture, pre-attempt timing, low-slippage entry, realized exit capture, and stale-risk avoidance.
- Dexter keeps the broader operational objective set even after the strategy split is made explicit.
- A default execution backbone should inherit the source with active lifecycle control rather than the source whose observed closes are still entirely timeout-shaped.
- Choosing Dexter as default does not erase the Mew-X containment edge; it simply places that edge in a bounded selective lane instead of a general default.

Execution implication:

- If objective weights are mixed, unspecified, or dominated by realized-outcome and lifecycle-control concerns, route to Dexter by default.

### Mew-X as a containment-first selective option

Selective execution option: `Mew-X`

Use Mew-X only when all of the following are true:

- the strategy objective explicitly prioritizes drawdown containment
- local-peak retention matters more than realized exit capture
- fast post-attempt fill is desirable even with worse observed slippage
- timeout-shaped lifecycle behavior is acceptable for that strategy sleeve
- the deployment can remain a separate execution template, sleeve, or objective-conditioned route rather than an in-run fusion layer

Do not reinterpret the current evidence as support for:

- Mew-X as the default primary engine
- Mew-X as an automatic failover inside a Dexter-managed position
- Mew-X as evidence of upstream candidate-quality parity
- Mew-X as justification for threshold or trust-logic transplant into Dexter

### Objective-conditioned routing and portfolio split

Supported on current evidence:

- pre-run route selection by explicit objective profile
- a Dexter default lane for opportunity capture, low-slippage entry, realized exit capture, and lifecycle control
- a separate Mew-X containment lane for drawdown containment, fast post-attempt fill, and local-peak retention
- portfolio split across independent sleeves where the objective charter is fixed before execution begins

Not supported on current evidence:

- mid-trade handoff from Dexter to Mew-X or from Mew-X to Dexter
- a fused single-engine design that mixes both source logics inside one live position lifecycle
- claims that a blended engine is already proven superior to either standalone source
- widening replay parity into a full path-equivalence or retention-equivalence proof

Source-faithful routing rule:

- The routing unit should be the strategy template or portfolio sleeve selected before execution, not a per-event fusion layer built inside one trade.

### Current evidence can fix these execution assumptions

- Dexter should remain the default execution anchor whenever objective weights are mixed or unspecified.
- Mew-X should remain a containment-first selective option rather than a general fallback.
- Hybrid use should stay ex ante and objective-conditioned, not in-run and compositional.
- No new evidence is required to plan execution boundaries at this level.
- No validator, Dexter, or Mew-X source logic changes are justified by this planning task.
- The replay claim stays bounded to realized-return fidelity and does not block bounded execution planning.
- `path_sensitive_retention_scope` is not required before implementation planning unless later design work tries to claim stronger retention equivalence than current evidence supports.

### Current evidence still cannot fix these execution questions

- the exact config surface that declares an objective profile and routes into a Dexter or Mew-X sleeve
- the portfolio budget or capital split between Dexter-default and Mew-X-selective sleeves
- the monitoring and kill-switch rules needed around timeout-shaped Mew-X lifecycle behavior
- the exact abstraction boundary between a planner/router layer and source-specific executors
- any claim that a future hybrid implementation will outperform both standalone sources after build-out

These remain execution-design or implementation-planning questions, not evidence blockers for the current bounded step.

## Non-Goals

- Do not reopen promoted-baseline selection.
- Do not collect new live or replay evidence.
- Do not change Dexter, Mew-X, or validator rules.
- Do not claim in-run source fusion is now validated.
- Do not transplant thresholds, trust logic, or semantic assumptions across frozen sources.
- Do not widen replay fidelity into full path equivalence.
- Do not move to funded live trading.

## Recommended Next Lane

- `implementation_planning`

Why this is the best next cut:

- The execution surface is already bounded enough to decompose work into implementation-scoped decisions without another evidence task.
- `path_sensitive_retention_scope` remains optional because no current execution recommendation depends on a stronger path-equivalence claim.
- A separate `concrete_execution_design` task is not required to unlock progress because the critical boundary is already fixed: Dexter default, Mew-X selective containment option, objective-conditioned routing, and explicit non-goals.

## Conclusion

### Key finding: `execution_plan_ready`

The current GitHub-visible evidence is now sufficient to translate strategy preference into a bounded execution plan:

- Dexter is the default execution anchor.
- Mew-X is the containment-first selective option.
- Hybrid use remains limited to objective-conditioned route selection or portfolio split.
- No new comparison work is needed before implementation planning.

### Claim boundary: `execution_plan_bounded`

The execution plan remains bounded because:

- Mew-X upstream candidate quality is still not comparable on the frozen surface.
- Dexter `realized_vs_peak_gap_pct` remains path-sensitive.
- Current replay parity is still not a full path-equivalence claim.
- The exact execution config, routing interface, and capital-allocation details remain implementation-scoped rather than evidence-fixed.

