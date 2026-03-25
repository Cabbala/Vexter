# TASK-007-STRATEGY-PLANNING

## Scope

This task starts from merged PR `#31` and the completed `TASK-007-RISK-CONTAINMENT-VS-EXIT-CAPTURE` lane. It keeps the promoted comparison baseline frozen and asks a single bounded question:

- Given the confirmed Dexter versus Mew-X split, which source should be preferred for each strategy objective, and where is hybrid or selective adoption source-faithful on the current evidence?

The task stays source-faithful by design:

- no new evidence collection
- no validator or source changes
- no baseline reopen
- only committed live/replay comparison packs plus the completed candidate, timing, and risk lanes already visible in GitHub artifacts

## Verified GitHub State

- Latest merged Vexter `main`: PR `#31`, merge commit `0905ec8c991ca6046b13d0c326c3224c49709a2d`, merged at `2026-03-25T23:36:30Z`
- Supporting merged Vexter states: PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Promoted live comparison: `artifacts/reports/task005-validator-rule-implement-20260325T180027Z-comparison`
- Promoted repaired replay comparison: `artifacts/reports/task006-replay-surface-fix-20260325T180027Z-replay-comparison`
- Candidate lane source of truth: `artifacts/reports/task-007-candidate-generation-vs-quality-report.md`
- Timing lane source of truth: `artifacts/reports/task-007-execution-timing-vs-retention-report.md`
- Risk lane source of truth: `artifacts/reports/task-007-risk-containment-vs-exit-capture-report.md`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from closeout and prior lanes:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- replay parity remains scoped to close-summary / `position_closed` realized-return fidelity
- Dexter `realized_vs_peak_gap_pct` remains the only path-sensitive live/replay drift
- Mew-X `candidate_precision_proxy` remains unavailable on the frozen export surface

## Confirmed Lane Conclusions Reused

### Candidate generation versus quality

The completed candidate lane already fixed the upstream asymmetry:

- Dexter `creator_candidate`: `255`
- Mew-X comparable `creator_candidate` surface: unavailable
- Dexter median `max_favorable_excursion_pct`: `34.8443`
- Dexter median `realized_exit_pct`: `7.1641`
- Dexter median quote-to-fill slippage: `0.0 bps`
- Mew-X median `realized_exit_pct`: `0.0`
- Mew-X stale-position ratio: `100.00%`

Bounded conclusion carried forward:

- Dexter owns the observable upstream opportunity-capture edge.
- A stronger cross-source candidate-precision proof is still unavailable because Mew-X does not expose a comparable upstream candidate surface here.

### Execution timing versus retention

The completed timing lane fixed the stage split:

- Dexter median `signal_to_attempt_latency_ms`: `0.0`
- Mew-X median `signal_to_attempt_latency_ms`: `891.0`
- Dexter median `attempt_to_fill_latency_ms`: `502.5`
- Mew-X median `attempt_to_fill_latency_ms`: `1.5`
- Dexter median quote-to-fill slippage: `0.0 bps`
- Mew-X median quote-to-fill slippage: `7.7061 bps`

Bounded conclusion carried forward:

- Dexter owns the earlier pre-attempt timing edge and the better slippage surface.
- Mew-X owns the later post-attempt fill-speed edge.

### Risk containment versus exit capture

The completed risk lane fixed the downstream split:

- Mew-X median `max_adverse_excursion_pct`: `0.0` vs Dexter `-6.0547`
- Mew-X median `time_to_peak_ms`: `20.5` vs Dexter `5299.0`
- Mew-X median `realized_vs_peak_gap_pct`: `0.0` live / `0.0` replay vs Dexter `20.5330` live / `25.8042` replay
- Dexter median `max_favorable_excursion_pct`: `34.8443` vs Mew-X `6.7929`
- Dexter median `realized_exit_pct`: `7.1641` vs Mew-X `0.0`
- Dexter stale-position ratio: `0.00%` vs Mew-X `100.00%`

Bounded conclusion carried forward:

- Mew-X owns price-path drawdown containment and local-peak retention.
- Dexter owns realized exit capture, slippage control, and stale-position avoidance.

## Objective-Weighted Strategy Surface

### Upstream opportunity capture

Primary source: `Dexter`

Why:

- Dexter is the only source with a material upstream `creator_candidate` surface in the current comparison.
- Dexter also keeps the earlier `signal_to_attempt_latency_ms` edge.
- The same promoted baseline that starts with Dexter candidate breadth still closes with stronger favorable excursion and stronger realized exit.

Bound:

- This is not a proof that Dexter has universally better candidate precision across sources.
- It is the strongest source-faithful planning choice because Mew-X upstream precision is not comparable on the frozen surface.

### Low-slippage entry and execution quality

Primary source: `Dexter`

Why:

- Dexter keeps median quote-to-fill slippage at `0.0 bps`.
- Dexter reaches the order-attempt boundary earlier at median `0.0 ms` signal-to-attempt latency.
- Mew-X is faster after attempt placement, but that does not translate into better slippage on the promoted baseline.

Bound:

- This preference is about entry quality under the current comparison surface, not about generic absolute speed.
- Mew-X still keeps the faster attempt-to-fill edge once an attempt exists.

### Drawdown containment and local-peak retention

Primary source: `Mew-X`

Why:

- Mew-X keeps median `max_adverse_excursion_pct` at `0.0`.
- Mew-X reaches local peak almost immediately at median `time_to_peak_ms` `20.5`.
- Mew-X gives back essentially none of that local peak at median `realized_vs_peak_gap_pct` `0.0`.
- Mew-X also fills almost immediately once it has placed an attempt.

Bound:

- This is a local-path containment and retention preference, not a realized-exit preference.
- All six observed Mew-X closes still end through `inactivity_timeout`, so this objective class accepts timeout-shaped lifecycle behavior.

### Realized exit capture

Primary source: `Dexter`

Why:

- Dexter keeps much larger median `max_favorable_excursion_pct` at `34.8443`.
- Dexter keeps positive median `realized_exit_pct` at `7.1641` while Mew-X remains `0.0`.
- Dexter does this without giving up its slippage edge.

Bound:

- Dexter does give back more from peak than Mew-X.
- This is therefore an absolute-upside and realized-exit preference rather than a peak-retention preference.

### Stale-risk avoidance and lifecycle control

Primary source: `Dexter`

Why:

- Dexter stale-position ratio remains `0.00%`.
- Dexter closes through active `safe` and `malicious` paths.
- Mew-X stale-position ratio remains `100.00%`, and all observed closes remain `inactivity_timeout`.

Bound:

- This objective class is about lifecycle containment, not a denial of Mew-X's local price-path containment edge.

## Single-Primary Planning Choice

If one source must anchor execution planning now, prefer `Dexter`.

Why that is source-faithful:

- Dexter is the primary source for upstream opportunity capture.
- Dexter is the primary source for low-slippage entry.
- Dexter is the primary source for realized exit capture.
- Dexter is the primary source for stale-risk avoidance and active lifecycle control.
- Mew-X retains a real but narrower primary role when the strategy explicitly prioritizes drawdown containment and local-peak retention over realized exit and active close-path control.

So the planning default is:

- Dexter as the execution-planning backbone
- Mew-X as a bounded selective or secondary strategy template

## Hybrid And Selective Adoption

### Supported on current evidence

- Objective-conditioned source selection
- Parallel strategy lanes or portfolio split where Dexter handles opportunity-capture / exit-driven objectives and Mew-X handles containment-first objectives
- Selective use of Mew-X only when timeout-shaped lifecycle behavior is an accepted trade for faster local retention

### Not supported on current evidence

- In-run fusion of Dexter and Mew-X source logic
- Threshold or trust-logic transplant claims across frozen sources
- Any claim that a hybrid design is already proven to outperform both standalone sources
- Any widening of replay fidelity into a full path-equivalence claim

### Source-faithful reading

Hybrid room exists at the design level, not yet at the proof level:

- the evidence supports objective-specific routing or selective adoption
- the evidence does not support additive or compositional claims about a fused execution engine

## What Current Evidence Can Decide

- Which source is primary for each strategy objective class
- That Dexter should be the default anchor for execution planning when realized outcome and lifecycle control matter materially
- That Mew-X should be preferred only for explicit containment-first or local-retention-first strategies
- That execution planning can begin without reopening comparison work

## What Current Evidence Cannot Decide

- Whether a hybrid implementation would outperform both standalone sources after build-out
- Whether Mew-X would show upstream candidate-quality parity on a comparable `creator_candidate` surface
- Whether stronger path-sensitive retention claims would survive a full path-equivalence review
- Whether any threshold migration between sources would remain source-faithful

## Non-Goals And Caveats

- Do not reopen promoted-baseline selection.
- Do not collect new live or replay evidence.
- Do not change Dexter, Mew-X, or validator rules.
- Do not turn Mew-X local-peak retention into a universal winner claim.
- Keep replay parity scoped to close-summary / `position_closed` realized-return fidelity.
- Preserve Dexter `realized_vs_peak_gap_pct` drift and unavailable Mew-X `candidate_precision_proxy` as explicit planning caveats.

## Conclusion

### Key finding: `strategy_plan_ready`

The fixed comparison now supports an execution-ready strategy plan:

- Dexter is the default primary source for opportunity capture, low-slippage entry, realized exit capture, and stale-risk avoidance.
- Mew-X is the bounded primary source for drawdown containment, fast post-attempt fills, and local-peak retention.
- Hybrid use is plausible only as selective adoption or objective-conditioned portfolio split, not as proven source fusion.

### Claim boundary: `strategy_plan_bounded`

The strategy plan remains bounded because:

- Mew-X upstream candidate quality remains unobservable on a comparable source surface.
- Dexter still carries a path-sensitive `realized_vs_peak_gap_pct` caveat.
- Current replay parity is still not a full path-equivalence claim.

## Recommended Next Step

- `execution_planning`

Why this is now the highest-value next cut:

- objective weights are now explicit enough to pick a primary planning source
- no new evidence collection is needed to begin execution-level design
- `path_sensitive_retention_scope` should stay optional until a stronger retention/path-equivalence claim is required

## Key Paths

- Report: `artifacts/reports/task-007-strategy-planning-report.md`
- Status: `artifacts/reports/task-007-strategy-planning-status.md`
- Proof: `artifacts/proofs/task-007-strategy-planning-check.json`
- Summary: `artifacts/proofs/task-007-strategy-planning-summary.md`
- Prompt pack: `artifacts/reports/task-007-strategy-planning`
- Bundle: `artifacts/bundles/task-007-strategy-planning.tar.gz`
