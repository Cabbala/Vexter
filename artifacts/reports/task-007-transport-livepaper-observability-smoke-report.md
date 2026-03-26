# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-SMOKE

## Scope

This task starts from merged PR `#46` and the completed `TASK-007-TRANSPORT-LIVEPAPER-SMOKE` lane. It keeps the promoted comparison baseline frozen and asks one bounded question:

- Does the implemented live-paper transport not only stay coherent, but also keep immutable handoff metadata, handle lifecycle, ack metadata, quarantine reason, manual halt propagation, and normalized failure detail observable end to end on the same source-faithful Dexter `paper_live` and Mew-X `sim_live` seam?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source-logic changes
- no validator-rule changes
- no comparison-baseline reopen
- no external wire, subprocess, or autoscaling finalization
- no boundary-contract rewrite
- only observability smoke tests, task artifacts, and the refreshed handoff bundle required to prove the current metadata surface is visible on the approved live-paper seam

## Verified GitHub State

- Latest merged Vexter `main`: PR `#46`, main commit `4df93f34a9f0cc483a38c31c2906bb6b43e5102f`, merged at `2026-03-26T11:55:02Z`
- Supporting merged Vexter states: PR `#45` `b43f983848c462757a5b91e018f3200f28ec6b2b`; PR `#44` `ae1dd7ddc3ffbae893887baf042ea5e5d53bc5f3`; PR `#43` `64ffe4a58dd9ff9e5ef707d77b59f392da9e02e0`; PR `#42` `23e6f354bf261935639941d541227b0c3f7a8435`; PR `#41` `0b174515c9c0deb04b70fd38c2c2882736a22273`; PR `#40` `a4e7a3c74460dc711c3e2897ac31386272e91c27`; PR `#39` `a293d6e9260bd092297140bc82469802d6fce115`; PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`; PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior transport live-paper source of truth: `artifacts/reports/task-007-transport-livepaper-smoke-report.md`
- Prior transport live-paper proof: `artifacts/proofs/task-007-transport-livepaper-smoke-check.json`
- Current inherited implementation conclusion: `transport_livepaper_smoke_passed`
- Current inherited claim boundary: `transport_livepaper_smoke_bounded`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from comparison closeout through transport live-paper smoke:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- no mid-trade handoff, threshold transplant, trust-logic transplant, or fused-engine claim

## What Landed

### Live-paper observability smoke coverage

Committed live-paper observability smoke now lives at `tests/test_planner_router_transport_livepaper_observability_smoke.py` and keeps the concrete transport implementation untouched while driving the existing public `plan_request()` and `plan_and_dispatch()` surfaces through the approved live-paper seam.

The new smoke covers:

- immutable handoff metadata that remains traceable from planner-owned `planned` storage into prepared handle manifests with source, monitor, timeout envelope, executor profile, pinned commit, handle id, execution mode, entrypoint, and first-vs-duplicate prepare ack state
- shared status sink fan-in that records Dexter and Mew-X lifecycle snapshots in one observable stream while preserving per-plan stable handle identity
- runtime-side first-vs-duplicate ack visibility for `start` and `stop`, including duplicate ack metadata on running, stopping, and final halted sink snapshots
- pushed quarantine source reason, monitor profile, quarantine scope, and promoted poll-first reconciliation detail on the live-paper seam
- reverse-order `manual_latched_stop_all` propagation with visible trigger plan id, stop reason, halt mode, and snapshot-backed adapter detail on both active handles
- normalized `status_timeout` failure detail with source reason passthrough plus source-faithful rollback snapshot metadata for Dexter `paper_live` and Mew-X `sim_live`

### Behavior now evidenced

- The current live-paper transport surface was already instrumented enough to prove end-to-end observability without changing source logic.
- Planner-owned immutable handoff metadata remains traceable after `prepare`; observability does not require mutating the stored plan batch.
- The shared status sink now visibly fans in both sources while preserving stable `handle_id` continuity on the sink snapshots themselves.
- First-call versus duplicate ack metadata remains distinguishable across prepare, start, and stop rather than collapsing into a single untyped "success."
- Quarantine stays sleeve-scoped and source-faithful: the live-paper sink still exposes the Mew-X reason, monitor profile, and promoted push detail.
- Manual halt remains planner-owned and reverse ordered, but the propagated stop metadata is now explicitly smoke-verified as visible on the sink and adapter snapshots.
- Normalized failure detail keeps the transport-originated `status_timeout` reason visible while preserving source-faithful runtime snapshot context for rollback confirmation.

### What did not change

- No Dexter source behavior changed.
- No Mew-X source behavior changed.
- No validator rules changed.
- No comparison evidence was recollected.
- No external wire, process topology, or numeric timing constant was finalized.

## Tests

Planner/router transport live-paper observability coverage now includes:

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

### `transport_livepaper_observability_runtime`

Recommended next because:

- the bounded smoke now proves the current metadata surface is visible on the approved live-paper seam, so the sharpest remaining risk is carrying that observability through a fuller runtime-oriented lane
- this lane removed uncertainty around handoff traceability, sink fan-in, ack visibility, halt propagation, and failure metadata, which are exactly the prerequisites for a runtime follow-up
- a runtime follow-up now reduces more uncertainty than restating the same surface in another spec-only pass

### `livepaper_observability_spec`

Not next because:

- the existing transport already exposed the observability fields that needed first-pass behavioral confirmation
- a spec-only pass would add less confidence than exercising the already-proven fields on a broader runtime-oriented lane

### `executor_boundary_code_spec`

Not next because:

- the boundary remained fixed through spec, implementation, runtime smoke, live-paper smoke, and now observability smoke
- this task surfaced no new interface ambiguity that would justify another contract-only lane

## Decision

- Outcome: `A`
- Key finding: `executor_transport_livepaper_observability_smoke_passed`
- Claim boundary: `transport_livepaper_observability_smoke_bounded`
- Decision: `transport_livepaper_observability_runtime_ready`
- Recommended next step: `transport_livepaper_observability_runtime`
