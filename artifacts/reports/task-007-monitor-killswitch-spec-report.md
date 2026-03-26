# TASK-007-MONITOR-KILLSWITCH-SPEC

## Scope

This task starts from merged PR `#40` and the completed `TASK-007-PLANNER-ROUTER-RUNTIME-SMOKE` lane. It keeps the promoted comparison baseline frozen and asks one bounded policy question:

- Given the already-proven planner/router runtime seam, what monitor / kill-switch contract can be fixed now without reopening comparison work, changing frozen source logic, or finalizing numeric thresholds?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source-logic changes
- no validator-rule changes
- no baseline reopen
- no executor-transport or process-model redesign
- no numeric threshold finalization; bounded defaults and deferred boundaries only
- only monitor/killswitch contract definition, companion tests, and refreshed task artifacts/bundle

## Verified GitHub State

- Latest merged Vexter `main`: PR `#40`, main commit `a4e7a3c74460dc711c3e2897ac31386272e91c27`, merged at `2026-03-26T02:45:48Z`
- Supporting merged Vexter states: PR `#39` `a293d6e9260bd092297140bc82469802d6fce115`; PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`; PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior runtime source of truth: `artifacts/reports/task-007-planner-router-runtime-smoke-report.md`
- Prior runtime proof: `artifacts/proofs/task-007-planner-router-runtime-smoke-check.json`
- Current inherited implementation conclusion: `planner_router_runtime_smoke_passed`
- Current inherited claim boundary: `runtime_smoke_bounded`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from comparison closeout through runtime smoke:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- no mid-trade handoff, threshold transplant, trust-logic transplant, or fused-engine claim
- externally visible lifecycle stays `planned -> starting -> running -> quarantined -> stopping -> stopped|failed`

## What Landed

### Monitor profile class

A monitor profile is now fixed as an immutable per-plan binding resolved before a plan reaches `planned`. The planner/router contract keeps exactly five fields on that binding:

- `monitor_profile_id`
- `admission_gate_class`
- `timeout_envelope_class`
- `quarantine_scope`
- `global_halt_participation`

Committed profile classes are fixed now:

- `dexter_default` = `lifecycle_control` / `dexter_lifecycle_control` / `sleeve` / `true`
- `mewx_timeout_guard` = `timeout_aware` / `mewx_timeout_tolerant` / `sleeve` / `true`

Binding rules fixed now:

- every emitted plan binds exactly one monitor profile
- overlay Dexter plans keep `dexter_default`
- overlay or dedicated Mew-X plans keep `mewx_timeout_guard`
- monitor binding is copied into the immutable plan rather than resolved dynamically after start

### Admission-gate class

Admission gates remain pre-emission and fail closed. The planner/router may reject launch before any plan is emitted for:

- config invalidity or missing references
- source-pin mismatch
- disabled sleeve
- budget overflow or missing explicit Mew-X cap reference
- active global halt

The fixed consequence is narrow:

- active global halt blocks planning before plan emission
- failed admission never emits a partial batch
- admission failure never silently downgrades explicit Mew-X intent to Dexter default

### Timeout-envelope class

Timeout envelopes are fixed as source-shaped lifecycle boundaries, not finalized durations.

Dexter boundary fixed now:

- `dexter_default` keeps lifecycle-control monitoring
- stale-position or close-summary absence beyond the active-lifecycle envelope is abnormal
- numeric heartbeat and timeout values remain deferred

Mew-X boundary fixed now:

- `mewx_timeout_guard` stays timeout-aware and timeout-tolerant
- a normal `inactivity_timeout` close reason is source-native and not an automatic incident by itself
- quarantine triggers only when the session outlives the configured envelope or fails to emit normalized close or shutdown confirmation
- numeric heartbeat, retry, and timeout values remain deferred

### Quarantine scope

Quarantine remains sleeve-scoped on the public status surface.

What is fixed now:

- runtime smoke preserves `planned -> starting -> running -> quarantined -> stopping -> stopped`
- quarantine disables new work for the affected sleeve only
- quarantining a Mew-X sleeve must not transfer the position to Dexter
- reverse-order stop-all rollback remains the bounded batch rollback shape once quarantine escalates under the current participating profiles

What is not fixed now:

- numeric incident counts before quarantine
- latency thresholds for escalation
- any cross-source recovery or live migration path

### Global-halt participation

Global halt remains a planner-owned policy and not a rebinding path.

Fixed now:

- planner policy mode remains `manual_latched_stop_all`
- both committed monitor profiles currently participate in that halt policy
- global halt freezes new planning and issues source-native stop requests only
- global halt does not rewrite source thresholds, trust logic, or transport ownership
- global halt does not imply cross-source handoff

### Typed failure escalation

Failure escalation stays typed and planner-owned even when source-native reasons pass through as metadata.

Pre-emission rejection codes fixed now:

- `config_missing`
- `duplicate_config_id`
- `unknown_objective_profile`
- `route_mode_invalid`
- `sleeve_disabled`
- `executor_source_mismatch`
- `pin_mismatch`
- `unknown_budget_policy`
- `mewx_cap_required`
- `budget_share_overflow`
- `global_halt_active`

Post-emission lifecycle codes fixed now:

- `prepare_failed`
- `start_failed`
- `status_timeout`
- `shutdown_unconfirmed`
- `invalid_status_transition`
- `source_stop_failed`

Typed escalation boundary fixed now:

- `FailureDetail` carries planner-owned `code`, `stage`, `plan_id`, `source`, and passthrough `source_reason`
- `StatusSnapshot.detail` carries typed runtime follow-up such as `quarantine`, `stop`, `rollback_complete`, or `rollback_failed`
- source-native reasons remain passthrough metadata instead of being reclassified as source-strategy semantics

## What Did Not Change

- No Dexter source behavior changed.
- No Mew-X source behavior changed.
- No validator rules changed.
- No comparison evidence was recollected.
- No numeric timeout, retry, heartbeat, or budget threshold was finalized.

## Tests

Contract coverage now includes:

- `tests/test_monitor_killswitch_spec_contract.py`
- `tests/test_planner_router_runtime_smoke.py`
- `tests/test_bootstrap_layout.py`

Validation run on this branch:

- `pytest -q`
- `58 passed`

## Recommendation Among Next Tasks

### `planner_router_livepaper_smoke`

Recommended next because:

- monitor-driven quarantine, stop-all rollback participation, and global halt semantics are now fixed against the already-proven runtime seam
- live-paper smoke can now inherit explicit killswitch behavior instead of guessing escalation rules
- the next bounded question is whether the same monitor contract stays source-faithful once live-paper execution is exercised

### `executor_boundary_spec`

Not next because:

- the abstract adapter, status, and pin surfaces are already fixed and runtime-smoked
- another executor-boundary pass would mostly restate a contract that is now already concrete enough for live-paper validation

## Decision

- Outcome: `A`
- Key finding: `monitor_killswitch_contract_fixed`
- Claim boundary: `monitor_killswitch_spec_bounded`
- Current task status: `monitor_killswitch_spec_ready`
- Recommended next step: `planner_router_livepaper_smoke`
- Decision: `planner_router_livepaper_smoke_ready`
