# TASK-007-PLANNER-ROUTER-INTERFACE-SPEC Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#34` merge commit `981f0977788cffd10de4bf78f14e5b430fbce4c1` on `2026-03-26T00:39:22Z`.
- Supporting merged Vexter states remained PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`, PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`, PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`, PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`, PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`, PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`, PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`, PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Started from the merged `implementation_planning` lane and kept the promoted comparison baseline frozen.
- Reused only the fixed comparison, strategy, execution, and implementation-planning artifacts already visible on GitHub.
- Converted the bounded implementation surface into the first source-faithful planner/router interface contract.
- Fixed one immutable plan object that binds route choice, sleeve binding, budget binding, monitor profile binding, and executor profile binding before any executor starts.

## Planner/Router Interface Contract

- Immutable plan object: one `execution_plan` record per selected sleeve, carrying `plan_id`, `objective_profile_id`, `route`, `sleeve_binding`, `budget_binding`, `monitor_binding`, `executor_binding`, `source_pin`, and immutable invariants.
- Objective profile contract: every profile resolves to exactly one preferred source and allowed sleeve set; mixed or unspecified objectives still route to Dexter by default.
- Sleeve binding contract: a plan selects exactly one sleeve and exactly one source pre-run; no multi-source sleeve and no in-place route rebinding are allowed.
- Budget binding contract: all budgets remain sleeve-scoped; any Mew-X allocation requires explicit enablement and explicit cap semantics; supported split shapes remain `single_anchor_default`, `selective_overlay`, and `dedicated_containment_template`.
- Monitor profile binding contract: each plan binds exactly one monitor profile that defines admission-gate class, timeout-envelope class, quarantine scope, and global-halt participation, but not numeric thresholds yet.
- Executor profile binding contract: each plan binds exactly one source-matched executor profile pinned to a frozen commit and exposing the normalized `prepare`, `start`, `status`, `stop`, and `snapshot` surface.

## Unsupported Patterns

- Mid-trade handoff from Dexter to Mew-X or from Mew-X to Dexter.
- Threshold transplant or trust-logic transplant across frozen sources.
- Implicit Mew-X budget inside mixed-objective plans.
- Multi-source sleeves or fused-engine superiority claims.
- Upgrading replay fidelity into full path equivalence.

## Decision

- Outcome: `A`
- Key finding: `planner_router_spec_ready`
- Claim boundary: `planner_router_spec_bounded`
- Current task status: `planner_router_spec_ready`
- Recommended next step: `concrete_planner_router_implementation_spec`
- Decision: `next_spec_ready`

## Key Paths

- Planner/router interface report: `artifacts/reports/task-007-planner-router-interface-spec-report.md`
- Planner/router interface status: `artifacts/reports/task-007-planner-router-interface-spec-status.md`
- Planner/router interface proof: `artifacts/proofs/task-007-planner-router-interface-spec-check.json`
- Planner/router interface summary: `artifacts/proofs/task-007-planner-router-interface-spec-summary.md`
- Planner/router interface prompt pack: `artifacts/reports/task-007-planner-router-interface-spec`
- Planner/router interface bundle: `artifacts/bundles/task-007-planner-router-interface-spec.tar.gz`
