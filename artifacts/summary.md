# TASK-007-IMPLEMENTATION-PLANNING Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#33` merge commit `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc` on `2026-03-26T00:21:56Z`.
- Supporting merged Vexter states remained PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`, PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`, PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`, PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`, PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`, PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`, PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Started from the merged `execution_planning` lane and kept the promoted comparison baseline frozen.
- Reused only the fixed comparison, strategy, and execution outputs already visible in GitHub artifacts.
- Converted the bounded execution conclusion into implementation-ready planner/router, config, sleeve, portfolio, monitoring, and executor boundaries.
- Chose the next narrow spec cut based on which boundary must be fixed first for implementation to stay source-faithful.

## Implementation Planning Surface

- Planner/router boundary: route by objective-profile-bound sleeve before execution starts, validate pins and budgets, emit an immutable execution intent, and never perform mid-trade handoff or threshold transplant.
- Config surface: require explicit `planner`, `objective_profiles`, `sleeves`, `executors`, and `monitor_profiles` sections, with Dexter as the default fallback whenever objectives are mixed or unspecified.
- Sleeve boundary: keep a Dexter default sleeve for mixed, capture, low-slippage, realized-exit, and stale-control objectives; keep a separate Mew-X sleeve only for explicit containment-first templates that accept timeout-shaped lifecycle behavior.
- Portfolio split design: support `single_anchor_default`, `selective_overlay`, and `dedicated_containment_template` as the only current candidate shapes; do not imply blended alpha or adaptive cross-source rebalancing.
- Monitoring and kill-switch boundary: use planner admission gates, sleeve quarantine, and global halt actions; treat Mew-X `inactivity_timeout` as source-native rather than an automatic incident, but quarantine on unresolved sessions beyond the configured timeout envelope.
- Executor boundary: planner/router owns route choice, budget binding, monitor-profile binding, and kill-switch dispatch; source-specific executors own source-native lifecycle, thresholds, trust logic, and stop semantics.

## Assumptions Fixed Now

- Dexter remains the default execution anchor whenever objectives are mixed or unspecified.
- Mew-X remains a containment-first selective sleeve rather than a general fallback or failover engine.
- Any Mew-X allocation must be explicit, sleeve-scoped, and pre-run; no implicit split is allowed for mixed objectives.
- The first implementation contract must bind route choice, sleeve budget, monitor profile, and executor profile together in one immutable plan object.
- No new evidence is required before writing the first implementation spec.
- Replay parity remains bounded to close-summary / realized-return fidelity and does not justify stronger blended-engine claims.

## Points Still Not Fixed

- The exact numeric Mew-X cap for mixed portfolios.
- The concrete heartbeat, timeout, and retry thresholds inside each monitor profile.
- The runtime transport for executors, such as subprocess versus service boundary.
- Any adaptive rebalance logic between sleeves after start.

## Decision

- Outcome: `A`
- Key finding: `implementation_plan_ready`
- Claim boundary: `implementation_plan_bounded`
- Current task status: `implementation_plan_ready`
- Recommended next step: `planner_router_interface_spec`
- Decision: `next_spec_ready`

## Key Paths

- Implementation planning report: `artifacts/reports/task-007-implementation-planning-report.md`
- Implementation planning status: `artifacts/reports/task-007-implementation-planning-status.md`
- Implementation planning proof: `artifacts/proofs/task-007-implementation-planning-check.json`
- Implementation planning summary: `artifacts/proofs/task-007-implementation-planning-summary.md`
- Implementation planning prompt pack: `artifacts/reports/task-007-implementation-planning`
- Implementation planning bundle: `artifacts/bundles/task-007-implementation-planning.tar.gz`
