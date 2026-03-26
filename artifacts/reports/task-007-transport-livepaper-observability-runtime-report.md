# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-RUNTIME

## Scope

This task starts from merged PR `#48` and the completed `TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-SMOKE` lane. It keeps the promoted comparison baseline frozen and asks one bounded question:

- Does the same source-faithful observability surface proven on the live-paper seam remain continuous when the transport is entered through the runtime-oriented `plan_and_dispatch()` path and then continued across runtime follow-up, push quarantine, manual stop-all propagation, and rollback-confirmed failure handling?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source-logic changes
- no validator-rule changes
- no comparison-baseline reopen
- no external wire, subprocess, or autoscaling finalization
- no boundary-contract rewrite
- only runtime-oriented observability tests, task artifacts, and the refreshed handoff bundle required to prove continuity of the already-approved metadata surface

## Verified GitHub State

- Latest merged Vexter `main`: PR `#48`, main commit `085f2692bf150431dd39365b6c954cf069e18617`, merged at `2026-03-26T12:29:56Z`
- Supporting merged Vexter states: PR `#47` `2f993ab4e5997d092c3d08f9d98115e7f9559d5e`; PR `#46` `4df93f34a9f0cc483a38c31c2906bb6b43e5102f`; PR `#45` `b43f983848c462757a5b91e018f3200f28ec6b2b`; PR `#44` `ae1dd7ddc3ffbae893887baf042ea5e5d53bc5f3`; PR `#43` `64ffe4a58dd9ff9e5ef707d77b59f392da9e02e0`; PR `#42` `23e6f354bf261935639941d541227b0c3f7a8435`; PR `#41` `0b174515c9c0deb04b70fd38c2c2882736a22273`; PR `#40` `a4e7a3c74460dc711c3e2897ac31386272e91c27`; PR `#39` `a293d6e9260bd092297140bc82469802d6fce115`; PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`; PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior transport live-paper observability source of truth: `artifacts/reports/task-007-transport-livepaper-observability-smoke-report.md`
- Prior transport live-paper observability proof: `artifacts/proofs/task-007-transport-livepaper-observability-smoke-check.json`
- Current inherited implementation conclusion: `transport_livepaper_observability_smoke_passed`
- Current inherited claim boundary: `transport_livepaper_observability_smoke_bounded`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from comparison closeout through transport live-paper observability smoke:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- no mid-trade handoff, threshold transplant, trust-logic transplant, or fused-engine claim

## What Landed

### Runtime-oriented observability coverage

Committed runtime-oriented observability coverage now lives at `tests/test_planner_router_transport_livepaper_observability_runtime.py` and keeps the concrete transport implementation untouched while driving the same live-paper seam from the public `plan_and_dispatch()` path before continuing across runtime follow-up on the same prepared handles.

The new runtime lane covers:

- immutable handoff metadata that remains traceable from planner-owned `planned` storage into runtime-prepared handle manifests and then into sink-backed runtime snapshots
- first-call versus duplicate `prepare` and `start` visibility after the runtime path is already active, rather than only in bounded manual setup
- shared status sink fan-in that keeps Dexter and Mew-X visible on the same runtime-oriented path while preserving stable `handle_id` continuity across running, quarantined, stopping, and stopped snapshots
- pushed quarantine source reason, monitor profile, quarantine scope, and promoted poll-first reconciliation detail after runtime follow-up rather than only on the initial bounded seam
- reverse-order `manual_latched_stop_all` propagation with final sink detail backed by the adapter snapshot for both active handles
- normalized `status_timeout` failure detail on dispatch abort, including adapter-level status error visibility plus snapshot-backed rollback detail for Dexter `paper_live` and Mew-X `sim_live`

### Behavior now evidenced

- The public runtime entrypoint and the existing live-paper observability surface are continuous; the runtime lane does not hide or rewrite the metadata already proven on the seam.
- Planner-owned immutable handoff metadata remains traceable after runtime dispatch: the plan store still owns `planned`, while the prepared handles and sink snapshots carry the same source, monitor, timeout-envelope, executor-profile, and pinned-commit identity forward.
- First-call versus duplicate ack visibility remains observable after runtime follow-up, not just in pre-runtime smoke setup.
- Status sink fan-in remains shared and source-faithful across both sources while retaining stable handle identity and reverse-order stop propagation.
- Quarantine reason, manual halt propagation, and snapshot-backed terminal detail remain visible end to end after the runtime path is already in motion.
- Normalized failure detail still preserves source reason passthrough and source-faithful rollback snapshot context on the runtime-oriented path.

### What did not change

- No Dexter source behavior changed.
- No Mew-X source behavior changed.
- No validator rules changed.
- No comparison evidence was recollected.
- No external wire, process topology, or numeric timing constant was finalized.

## Tests

Planner/router transport live-paper observability runtime coverage now includes:

- `tests/test_planner_router_transport_livepaper_observability_runtime.py`
- `tests/test_planner_router_transport_livepaper_observability_smoke.py`
- `tests/test_planner_router_transport_livepaper_smoke.py`
- `tests/test_planner_router_transport_runtime_smoke.py`
- `tests/test_planner_router_transport.py`
- `tests/test_planner_router_executor_transport_implementation.py`
- `tests/test_planner_router_livepaper_smoke.py`
- `tests/test_planner_router_runtime_smoke.py`
- `tests/test_planner_router_integration_smoke.py`
- `tests/test_planner_router_dispatch_state_machine.py`
- `tests/test_planner_router_executor_transport_spec_contract.py`
- `tests/test_bootstrap_layout.py`

Validation run on this branch:

- `pytest -q`
- `87 passed`

## Recommendation Among Next Tasks

### `transport_livepaper_observability_hardening`

Recommended next because:

- the runtime-oriented lane now proves the existing observability surface survives entry through `plan_and_dispatch()` and later runtime follow-up, so the next highest-value work is hardening uncovered edge cases rather than re-proving continuity
- the remaining risks are edge-case hardening around reconciliation branches, rejection paths, and stop-confirmation variants, not missing boundary shape or missing first-pass observability fields
- a hardening lane now reduces more risk than another spec-only restatement

### `livepaper_observability_spec`

Not next because:

- the current transport now has bounded evidence on both the seam-focused smoke and the runtime-oriented continuation path
- a spec-only pass would add less confidence than targeted hardening on the remaining edge paths

### `executor_boundary_code_spec`

Not next because:

- the planner-to-transport boundary remained fixed through spec, implementation, runtime smoke, live-paper smoke, observability smoke, and now runtime-oriented observability continuity
- this task surfaced no new interface ambiguity that justifies another contract-only lane

## Decision

- Outcome: `A`
- Key finding: `executor_transport_livepaper_observability_runtime_passed`
- Claim boundary: `transport_livepaper_observability_runtime_bounded`
- Decision: `transport_livepaper_observability_hardening_ready`
- Recommended next step: `transport_livepaper_observability_hardening`
