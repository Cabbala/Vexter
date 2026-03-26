# TASK-007-IMPLEMENTATION-PLANNING

## Scope

This task starts from merged PR `#33` and the completed `TASK-007-EXECUTION-PLANNING` lane. It keeps the promoted comparison baseline frozen and asks a single bounded question:

- Given the fixed execution conclusion, what implementation-ready architecture boundaries can be fixed now without reopening comparison work or changing frozen source logic?

The task stays intentionally narrow:

- no new evidence collection
- no validator or source changes
- no baseline reopen
- no threshold transplant
- only minimal reaggregation of the already committed comparison, strategy, and execution outputs visible on GitHub

## Verified GitHub State

- Latest merged Vexter `main`: PR `#33`, merge commit `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`, merged at `2026-03-26T00:21:56Z`
- Supporting merged Vexter states: PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Execution planning source of truth: `artifacts/reports/task-007-execution-planning-report.md`
- Strategy planning source of truth: `artifacts/reports/task-007-strategy-planning-report.md`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from closeout and execution planning:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- supported routing scope: `objective_conditioned_route_selection_or_portfolio_split`
- unsupported routing scope: `mid_trade_handoff`, threshold transplant, trust-logic transplant, fused-engine superiority claims
- replay parity remains bounded to close-summary / `position_closed` realized-return fidelity
- Dexter `realized_vs_peak_gap_pct` remains path-sensitive
- Mew-X `candidate_precision_proxy` remains unavailable

## Implementation Planning Surface

### Planner/router layer responsibilities

The planner/router layer should own only cross-source control-plane decisions:

- validate objective profile, sleeve config, source pins, and budget declarations before execution starts
- resolve the route unit as a sleeve or template selected before any position opens
- default mixed or unspecified objectives to the Dexter sleeve
- attach budget policy, monitor profile, and executor profile to one immutable execution intent
- launch exactly one source-specific executor per selected sleeve plan
- accept normalized health and lifecycle updates from executors and translate them into sleeve quarantine or global halt decisions

The planner/router layer must not:

- modify source thresholds, trust logic, or execution semantics
- compare live source internals inside one position lifecycle
- hand an open position from Dexter to Mew-X or from Mew-X to Dexter
- claim that a blended engine is already validated

### Objective profile and config surface

The current evidence is strong enough to fix the config sections that must exist:

- `planner`: default anchor, route unit, fallback source, global kill-switch policy
- `objective_profiles`: named objective sets that bind preferred source, budget policy, and monitor profile
- `sleeves`: Dexter-default and optional Mew-X-selective sleeves with enable flags and budget semantics
- `executors`: source-specific executor profile references pinned to frozen commits
- `monitor_profiles`: source-aware health, timeout, and quarantine behavior

Minimum config shape to implement:

```json
{
  "planner": {
    "default_execution_anchor": "dexter",
    "route_unit": "sleeve",
    "fallback_source": "dexter",
    "allow_mid_trade_handoff": false
  },
  "objective_profiles": {
    "mixed_default": {
      "preferred_source": "dexter",
      "budget_policy": "single_anchor_default",
      "monitor_profile": "dexter_default"
    },
    "containment_first": {
      "preferred_source": "mewx",
      "budget_policy": "explicit_selective_sleeve",
      "monitor_profile": "mewx_timeout_guard"
    }
  },
  "sleeves": {
    "dexter_default": {
      "source": "dexter",
      "enabled": true,
      "budget_mode": "primary_default",
      "executor_profile": "dexter_main_pinned"
    },
    "mewx_containment": {
      "source": "mewx",
      "enabled": false,
      "budget_mode": "explicit_cap_only",
      "executor_profile": "mewx_frozen_pinned"
    }
  }
}
```

Config validations fixed now:

- every objective profile must resolve to exactly one preferred source
- mixed or unspecified objectives must resolve to Dexter
- any nonzero Mew-X sleeve requires explicit enablement plus a containment-first objective profile
- no config may enable mid-trade handoff
- budget declarations must be sleeve-scoped and fit inside total portfolio budget

### Dexter-default sleeve and Mew-X-selective sleeve

Dexter-default sleeve:

- selected for mixed, capture-first, low-slippage, realized-exit, or stale-risk-sensitive objectives
- supports full-allocation default or primary-share operation
- carries the default fallback when no explicit objective override is present
- uses a lifecycle-control monitor profile rather than timeout-tolerant assumptions

Mew-X selective sleeve:

- selected only for explicit containment-first templates
- stays isolated as a separate sleeve and executor profile
- accepts timeout-shaped lifecycle behavior as part of the objective tradeoff
- must not be treated as an automatic failover, blended fallback, or evidence of upstream candidate parity

### Portfolio budget and capital split candidates

Current evidence supports only bounded candidate shapes:

- `single_anchor_default`: Dexter `100%`, Mew-X `0%` whenever objectives are mixed or unspecified
- `selective_overlay`: Dexter primary sleeve plus an explicitly capped Mew-X containment sleeve for templates that opt in
- `dedicated_containment_template`: a fully separate Mew-X-only sleeve for strategies whose objective charter is explicitly containment-first

What is fixed now:

- the default deployment shape is `single_anchor_default`
- any Mew-X budget must be explicit rather than implicit
- a portfolio split may exist only across separate sleeves, not inside one live position lifecycle

What is not fixed now:

- the exact numeric cap for a mixed-portfolio Mew-X overlay
- dynamic rebalance rules between sleeves after start
- per-strategy leverage or drawdown budgets inside the sleeve allocator

### Monitoring, kill-switch, and timeout handling

The design boundary is now clear enough to separate three layers:

- planner admission gates: config invalid, pin mismatch, disabled sleeve, budget overflow, or active global halt prevents launch
- sleeve quarantine: repeated startup failures, heartbeat loss, unresolved lifecycle beyond the profile timeout envelope, or budget exhaustion disables new work for that sleeve
- global halt: freeze all new planning and send source-native stop requests to every active executor

Mew-X-specific timeout boundary:

- a normal `inactivity_timeout` close reason is source-native and should be recorded, not treated as an automatic incident
- the kill-switch boundary is an unresolved session that outlives the configured timeout envelope or fails to emit the expected normalized close/shutdown confirmation
- quarantining the Mew-X sleeve must stop new entries only; it must not transfer the position to Dexter

Dexter-specific monitoring boundary:

- stale-position or close-summary absence beyond the active-lifecycle envelope is abnormal
- Dexter retains the stricter default lifecycle-control monitor profile because it is the default execution backbone

### Executor boundary

The planner/router should communicate with executors through an immutable normalized contract.

Required execution-intent fields:

- `plan_id`
- `sleeve_id`
- `source`
- `objective_profile`
- `budget_policy`
- `monitor_profile`
- `executor_profile`
- `pinned_commit`

Expected executor methods:

- `prepare(intent)`
- `start(intent)`
- `status(handle)`
- `stop(handle, reason)`
- `snapshot(handle)`

Normalized statuses:

- `planned`
- `starting`
- `running`
- `quarantined`
- `stopping`
- `stopped`
- `failed`

Ownership split:

- planner/router owns route choice, budget binding, monitor-profile binding, and kill-switch dispatch
- executors own source-native startup, lifecycle, threshold use, trust logic, and stop semantics

The implementation does not need to fix the runtime transport yet. Subprocess versus service is still an implementation detail, not an evidence decision.

## Assumptions Fixed Now

- Dexter remains the default execution anchor whenever objective weights are mixed or unspecified.
- Mew-X remains a containment-first selective sleeve rather than a general fallback.
- The route unit is an ex ante sleeve or template choice, not a mid-trade fusion mechanism.
- Any first implementation must bind routing, budget, monitor profile, and executor profile in one immutable plan contract.
- No new evidence collection is required before writing the first implementation spec.
- No validator, Dexter, or Mew-X source logic changes are justified by this planning task.
- `path_sensitive_retention_scope` remains optional unless a later task needs a stronger retention-equivalence claim.

## What Still Remains Open

- exact numeric Mew-X overlay caps
- exact heartbeat, retry, and timeout thresholds inside each monitor profile
- executor transport and process model
- any adaptive cross-sleeve rebalance logic
- any claim that a future hybrid implementation will outperform both standalone sources

## Recommended Next Spec

### `planner_router_interface_spec`

Recommended first because:

- it fixes the top-level contract that every other piece depends on
- it locks the route unit, config schema, immutable execution intent, sleeve budget binding, and monitor-profile references
- monitoring and kill-switch details can then attach to normalized statuses instead of inventing parallel contracts

### `concrete_implementation_spec`

Not first because:

- it would be too broad before the planner/router contract is explicit
- it would mix route schema, monitoring, and executor transport decisions in one step

### `monitoring_kill_switch_spec`

Not first because:

- timeout and quarantine thresholds depend on the normalized interface between planner/router and executors
- the action verbs for sleeve quarantine versus global halt should be defined against the shared contract first

## Conclusion

### Key finding: `implementation_plan_ready`

The current GitHub-visible evidence is sufficient to translate the bounded execution plan into implementation-ready architecture boundaries:

- planner/router responsibilities are fixed
- config sections and sleeve boundaries are fixed
- portfolio split shapes are bounded
- monitoring and executor ownership boundaries are fixed

### Claim boundary: `implementation_plan_bounded`

The implementation plan remains bounded because:

- exact numeric split caps and kill-switch thresholds are still implementation defaults rather than evidence-fixed facts
- replay parity is still not a full path-equivalence claim
- Mew-X candidate precision remains unavailable on the frozen export surface
- Dexter `realized_vs_peak_gap_pct` remains path-sensitive
