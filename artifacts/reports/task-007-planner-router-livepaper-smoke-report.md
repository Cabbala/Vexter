# TASK-007-PLANNER-ROUTER-LIVEPAPER-SMOKE

## Scope

This task starts from merged PR `#41` and the completed `TASK-007-MONITOR-KILLSWITCH-SPEC` lane. It keeps the promoted comparison baseline frozen and asks one bounded question:

- Given the already-implemented planner/router control plane plus the fixed monitor/killswitch contract, do the public `plan_request()` and `plan_and_dispatch()` paths stay source-faithful when exercised through paper-shaped executor seams with admission-gate rejection, immutable plan emission, dispatch start, bounded runtime progression, profile-bound quarantine, and manual latched stop-all?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source-logic changes
- no validator-rule changes
- no comparison-baseline reopen
- no numeric monitor-threshold finalization
- no executor-transport or process-model redesign
- only live-paper smoke tests, task artifacts, and the refreshed proof bundle required to prove the paper-shaped control-plane path is live

## Verified GitHub State

- Latest merged Vexter `main`: PR `#41`, main commit `0b174515c9c0deb04b70fd38c2c2882736a22273`, merged at `2026-03-26T03:08:04Z`
- Supporting merged Vexter states: PR `#40` `a4e7a3c74460dc711c3e2897ac31386272e91c27`; PR `#39` `a293d6e9260bd092297140bc82469802d6fce115`; PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`; PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior monitor/killswitch source of truth: `artifacts/reports/task-007-monitor-killswitch-spec-report.md`
- Prior monitor/killswitch proof: `artifacts/proofs/task-007-monitor-killswitch-spec-check.json`
- Current inherited implementation conclusion: `monitor_killswitch_contract_fixed`
- Current inherited claim boundary: `monitor_killswitch_spec_bounded`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from comparison closeout through monitor/killswitch spec:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- no mid-trade handoff, threshold transplant, trust-logic transplant, or fused-engine claim

## What Landed

### Live-paper smoke coverage

Committed live-paper smoke now lives at `tests/test_planner_router_livepaper_smoke.py` and keeps the planner/router code untouched while driving the existing public entrypoints through source-faithful paper-like executor seams.

The new smoke covers:

- `plan_request()` on the explicit overlay path with committed config plus smoke-only enablement of `mewx_containment`, proving immutable batch emission and plan-store writes can be handed to Dexter `paper_live` and Mew-X `sim_live` executor stubs with pinned commits and fixed monitor bindings preserved
- fail-closed rejection for active `manual_latched_stop_all` before any live-paper batch is emitted or partially stored
- `plan_and_dispatch()` across the same overlay path, proving store -> prepare -> start -> status ordering into paper-like adapters with the immutable emitted plans carried through the seam
- bounded runtime follow-up where the Mew-X leg quarantines under its fixed `mewx_timeout_guard` profile and active plans then receive reverse-order `manual_latched_stop_all` stop propagation

### Behavior now evidenced

- Live-paper shaped requests do not require planner/router logic changes: the immutable emitted plans already carry the monitor, executor, sleeve, budget, and source-pin bindings needed by paper-like adapters.
- Source-faithful safe modes stay bounded to the seam: Dexter executes as `paper_live` via `monitor_mint_session`, while Mew-X stays `sim_live` via `sim_session` in the smoke harness rather than claiming a new frozen-source mode.
- Admission gates still fail closed before any batch write when global halt is already latched active.
- `plan_and_dispatch()` still performs atomic store, ordered prepare/start, and runtime status normalization before any quarantine/halt follow-up is applied.
- Quarantine signaling stays profile-bound: the Mew-X leg quarantines with `mewx_timeout_guard` and `mewx_timeout_tolerant` metadata preserved, and the subsequent halt propagates as planner-owned `manual_latched_stop_all` without cross-source handoff.

### What did not change

- No Dexter source behavior changed.
- No Mew-X source behavior changed.
- No validator rules changed.
- No comparison evidence was recollected.
- No monitor numeric policy or executor transport ownership was finalized.

### Tests

Planner/router coverage now includes:

- `tests/test_planner_router_config_loader.py`
- `tests/test_planner_router_objective_resolver.py`
- `tests/test_planner_router_plan_emitter.py`
- `tests/test_planner_router_dispatch_state_machine.py`
- `tests/test_planner_router_integration_smoke.py`
- `tests/test_planner_router_runtime_smoke.py`
- `tests/test_monitor_killswitch_spec_contract.py`
- `tests/test_planner_router_livepaper_smoke.py`

Validation run on this branch:

- `./scripts/build_proof_bundle.sh`
- `pytest -q`
- `61 passed`

## Recommendation Among Next Tasks

### `planner_router_executor_transport_spec`

Recommended next because:

- live-paper smoke now proves the planner/router control plane and fixed kill-switch contract against paper-like adapter seams, so the largest remaining unknown is the concrete transport contract from immutable plan to source-native session start/status/stop
- transport spec can pin how Dexter `monitor_mint_session` and Mew-X `sim_session` or session-control methods map onto the existing seam without reopening baseline or strategy semantics
- observability can then be attached to a fixed transport surface rather than another stub-only path

### `livepaper_observability_spec`

Not next because:

- the smoke already demonstrates the planner-owned status, quarantine, and halt lifecycle at a bounded seam
- the sharper unresolved question is how the real adapter transport will surface those events, not which logs or metrics we would like before that transport is fixed

### `executor_boundary_spec`

Not next because:

- the abstract planner/router boundary has already been fixed, runtime-smoked, and now live-paper-smoked
- another boundary-only pass would largely restate the same contract without reducing the next implementation risk

## Decision

- Outcome: `A`
- Key finding: `planner_router_livepaper_smoke_passed`
- Claim boundary: `livepaper_smoke_bounded`
- Current task status: `planner_router_livepaper_smoke_passed`
- Recommended next step: `planner_router_executor_transport_spec`
- Decision: `planner_router_executor_transport_spec_ready`
