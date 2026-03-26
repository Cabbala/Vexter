# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME

## Scope

This task starts from merged `main` after the watchdog lane and keeps the promoted comparison baseline frozen. It asks one bounded question:

- Do the drift / omission / partial-visibility checks already locked by the CI gate and watchdog stay effective when the transport is entered through `plan_and_dispatch()` and then driven across runtime follow-up on the same source-faithful handles?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source-logic changes
- no validator-rule changes
- no comparison-baseline reopen
- no trust-logic rewrite or funded live-trading expansion
- only runtime-follow-up watchdog tests, CI wiring, artifacts, manifest, ledger, and refreshed handoff bundle metadata

## Verified GitHub State

- Latest merged Vexter `main`: PR `#55`, main commit `79a74ee187f222be74d11a30cf7204cd5777f01e`, merged at `2026-03-26T14:56:13Z`
- Prior supporting Vexter merged states remain PR `#54` `099f4444a16938039ec5b74364ed3bd9424dc985` and PR `#53` `64cd0e22c284c759a64939348a59c3152afc77dc`
- Open Vexter PR `#50` remained non-authoritative relative to merged `main`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Current inherited task conclusion: `transport_livepaper_observability_watchdog_passed`
- Current inherited claim boundary: `transport_livepaper_observability_watchdog_bounded`
- Frozen seam: Dexter `paper_live`, Mew-X `sim_live`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from comparison closeout through watchdog:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- no mid-trade handoff, threshold transplant, trust-logic transplant, or fused-engine claim

## What Landed

### Runtime-follow-up watchdog continuity

Committed runtime-follow-up watchdog coverage now lives at `tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py` and keeps the concrete transport implementation untouched while feeding the existing watchdog with runtime-shaped follow-up on top of the public `plan_and_dispatch()` path.

The new lane proves that watchdog detection still covers:

- immutable handoff metadata continuity from planner-owned storage into runtime handle metadata and sink-visible follow-up snapshots
- handle lifecycle continuity and planned-versus-runtime metadata drift across repeated `prepare`, `start`, `status`, and `stop` follow-up on the same handles
- partial status-sink fan-in and ack-history retention loss after duplicate follow-up and terminal visibility
- push quarantine reason completeness on runtime-follow-up snapshots
- reverse-order `manual_latched_stop_all` propagation with snapshot-backed terminal detail
- normalized failure-detail passthrough on runtime-shaped failure follow-up without source drift

### Continuous enforcement

- Added `transport_livepaper_observability_watchdog_runtime` as a dedicated pytest marker and CI step.
- Wired `./scripts/run_transport_livepaper_observability_watchdog_runtime.sh` into `validate.yml` after the existing watchdog step and before bundle construction.
- Retargeted the proof bundle to the watchdog-runtime lane and refreshed the top-level summary, context pack, proof bundle manifest, task ledger, report, status, and handoff metadata.

### What did not change

- No Dexter source behavior changed.
- No Mew-X source behavior changed.
- No validator rules changed.
- No new comparison evidence was collected.
- No planner/router source logic changed to satisfy this lane.

## Tests

Runtime-oriented watchdog validation now includes:

- `tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py`
- `tests/test_planner_router_transport_livepaper_observability_watchdog.py`
- `tests/test_planner_router_transport_livepaper_observability_ci_gate.py`
- `tests/test_bootstrap_layout.py`

The dedicated runner remains:

- `./scripts/run_transport_livepaper_observability_watchdog_runtime.sh`

## Recommendation Among Next Tasks

### `transport_livepaper_observability_watchdog_regression_pack`

Recommended next because:

- the watchdog now has bounded evidence on both the base synthetic seam and runtime-oriented follow-up continuity
- the next highest-value step is packaging this runtime-shaped watchdog surface into a durable regression pack rather than restating the contract
- that path reduces more risk than another spec-only pass because the remaining uncertainty is regression containment, not interface discovery

### `livepaper_observability_spec`

Not next because:

- the observability surface is already evidenced through CI gate, watchdog, and runtime-follow-up continuity
- a spec-only pass would add less confidence than regression-pack enforcement

### `executor_boundary_code_spec`

Not next because:

- the planner-to-transport boundary did not surface new ambiguity in this lane
- the remaining work is about preserving the existing surface, not discovering a missing contract

## Decision

- Outcome: `A`
- Key finding: `executor_transport_livepaper_observability_watchdog_runtime_passed`
- Claim boundary: `transport_livepaper_observability_watchdog_runtime_bounded`
- Decision: `transport_livepaper_observability_watchdog_regression_pack_ready`
- Recommended next step: `transport_livepaper_observability_watchdog_regression_pack`
