# TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-SPEC

## Scope

This task starts from merged PR `#42` and the completed `TASK-007-PLANNER-ROUTER-LIVEPAPER-SMOKE` lane. It keeps the promoted comparison baseline frozen and asks one bounded implementation question:

- Given the fixed immutable plan contract, runtime/live-paper smoke, and source-faithful executor seam, what transport contract can now be fixed for real `prepare/start/status/stop/snapshot` traffic without reopening comparison work or changing frozen source logic?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source-logic changes
- no validator-rule changes
- no comparison-baseline reopen
- no numeric monitor-threshold, retry, heartbeat, timeout, or cap finalization
- no trust-logic transplant, threshold transplant, or fused-engine claim
- only the executor transport/process boundary needed to move beyond stub adapters

## Verified GitHub State

- Latest merged Vexter `main`: PR `#42`, main commit `23e6f354bf261935639941d541227b0c3f7a8435`, merged at `2026-03-26T03:27:34Z`
- Supporting merged Vexter states: PR `#41` `0b174515c9c0deb04b70fd38c2c2882736a22273`; PR `#40` `a4e7a3c74460dc711c3e2897ac31386272e91c27`; PR `#39` `a293d6e9260bd092297140bc82469802d6fce115`; PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`; PR `#37` `786221a664637925f790e89af0448fa04832426e`; PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`; PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`; PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`; PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`; PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`; PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`; PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`; PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`; PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`; PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`; PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`; PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`; PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`; PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`; PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`; PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`; PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`; PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`; PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`; PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior live-paper source of truth: `artifacts/reports/task-007-planner-router-livepaper-smoke-report.md`
- Prior live-paper proof: `artifacts/proofs/task-007-planner-router-livepaper-smoke-check.json`
- Current inherited implementation conclusion: `planner_router_livepaper_smoke_passed`
- Current inherited claim boundary: `livepaper_smoke_bounded`
- Confirmatory residual context: `Mew-X candidate_rejected`

Facts preserved from comparison closeout through live-paper smoke:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- default execution anchor: `Dexter`
- selective sleeve source: `Mew-X`
- immutable emitted plans already bind route, sleeve, budget, monitor, executor, and source pin before runtime
- normalized lifecycle remains `planned -> starting -> running -> quarantined -> stopping -> stopped|failed`
- unsupported scope remains `mid_trade_handoff`, threshold transplant, trust-logic transplant, funded live trading, and fused-engine claims

## What Landed

### Ownership boundary

Transport ownership is now fixed around the already-coded four seams.

`PlanStore` ownership is planner-local only:

- persist exactly one immutable `PlanBatch` before any transport traffic
- remain the authoritative planner-side record for emitted `plan_id` and `plan_batch_id`
- never own native handles, transport retries, or source session lifecycle

`ExecutorRegistry` ownership is planner-local lookup only:

- map one immutable `ExecutionPlan` to one in-process `ExecutorAdapter` proxy
- cache or construct adapter clients by `executor_profile_id`
- never own batch persistence, status normalization, or cross-source fallback decisions

`ExecutorAdapter` ownership is the full transport bridge:

- translate `prepare/start/status/stop/snapshot` onto source-native Dexter and Mew-X runtime calls
- own request serialization, dedupe, native handle allocation, and handle rehydration
- preserve source-native reasons and lifecycle semantics without planner reinterpretation

`StatusSink` ownership is planner-local normalized fan-in only:

- ingest normalized `StatusSnapshot` records from polling and any later push path
- remain separate from `PlanStore` so pre-runtime plan emission and runtime status ingestion do not collapse into one store
- never own transport command issuance or source-local stop semantics

Shared but bounded split:

- planner/router owns message issuance intent, correlation ids, retry intent, timeout classification, quarantine, and `manual_latched_stop_all`
- executor runtime owns message receipt, dedupe, native dispatch, source-session state, and terminal confirmation
- neither side may reinterpret explicit Mew-X intent as Dexter fallback or create cross-source handoff semantics

### Bounded process boundary

The first non-stub transport cut now fixes one narrow process model:

- one in-process Vexter planner/router control-plane runtime
- one in-process planner-local `PlanStore`, `ExecutorRegistry`, and `StatusSink`
- one long-lived adapter-owned executor runtime per `executor_profile_id` on the target runtime host
- one native source session and one transport handle per emitted `plan_id`

Source-faithful consequence:

- Dexter `paper_live` transport stays adapter-owned and targets Dexter `monitor_mint_session`
- Mew-X safe-mode transport stays adapter-owned and targets a long-lived Mew-X runtime that uses `start_session` plus `sim_session`
- later Mew-X funded execution, if ever opened in a separate lane, would reuse the same process boundary and swap the session entrypoint to `trade_session` without changing planner ownership

What is fixed now:

- `prepare(plan)` allocates or rehydrates exactly one handle for one `plan_id`
- `start(handle)` addresses that prepared handle and does not resend the full plan payload
- `status(handle)` and `snapshot(handle)` reconcile the same single-plan handle
- `stop(handle, reason)` targets the prepared or running session and does not imply process termination
- overlay batches may create multiple concurrent handles, but every handle remains single-plan and single-source

What is deliberately excluded:

- planner-managed subprocess trees
- per-message ephemeral workers
- cross-host failover or autoscaling
- any model where stop implies automatic source handoff
- any transport that requires the planner to understand source-native trust or threshold internals

### Request and response envelope

The transport contract is now fixed as a common envelope that can be serialized over any later wire, while the current Python seam continues to expose it as `ExecutionPlan`, `DispatchHandle.native_handle`, `StatusSnapshot`, and `snapshot()` data.

Required envelope fields for every serialized command or reply:

- `transport_version`
- `message_type`
- `message_id`
- `sent_at_utc`
- `plan_id`
- `plan_batch_id`
- `source`
- `executor_profile_id`
- `idempotency_key`
- `payload`

Python seam mapping fixed now:

- `prepare(plan)` request carries the full immutable `ExecutionPlan`
- `prepare(plan)` response is `DispatchHandle`, and `DispatchHandle.native_handle` is the prepare-ack payload carrier
- `start(handle)` and `stop(handle, reason)` keep `None` returns in Python, so transport ack success is represented by successful completion of the call and any later details in `status()` or `snapshot()`
- `status(handle)` response remains `StatusSnapshot`
- `snapshot(handle)` response remains a plain mapping for adapter-owned native detail

Required `prepare` ack fields inside `DispatchHandle.native_handle`:

- `transport_version`
- `handle_id`
- `ack_state`
- `entrypoint`
- `executor_profile_id`
- `pinned_commit`
- `status_delivery`
- `prepared_at_utc`

Required `status(handle)` fields:

- `StatusSnapshot.plan_id`
- `StatusSnapshot.status`
- `StatusSnapshot.source_reason`
- `StatusSnapshot.observed_at_utc`
- `StatusSnapshot.detail.handle_id`
- `StatusSnapshot.detail.signal`
- `StatusSnapshot.detail.sequence`
- `StatusSnapshot.detail.entrypoint`
- `StatusSnapshot.detail.pinned_commit`

Required `stop(handle, reason)` request payload fields at the wire boundary:

- `handle_id`
- `stop_reason`
- `requested_by`
- `requested_at_utc`

Required `snapshot(handle)` fields:

- `handle_id`
- `native_session_id`
- `executor_status`
- `last_sequence`
- `entrypoint`
- `pinned_commit`

Envelope invariants fixed now:

- `prepare` is the only command that may carry the full immutable plan payload
- `start`, `status`, `stop`, and `snapshot` address the prior `handle_id`
- `pinned_commit` and `executor_profile_id` remain visible at the seam for auditability and pin validation
- source-native reasons stay under `source_reason` or detail passthrough keys; they are not reclassified into planner strategy semantics

### Identity and idempotency

Identity is now fixed across the transport surface:

- `plan_id` is the primary execution identity and must stay stable for the life of one source-native session
- `plan_batch_id` identifies the rollback domain and reverse-stop ordering group
- `PlanBatch.request_id` stays planner correlation only; it is not a substitute for `plan_id`
- `handle_id` is adapter-owned, opaque to the planner, and must remain stable after accepted `prepare`

Mandatory idempotency keys:

- `prepare`: `plan_id:prepare:v1`
- `start`: `plan_id:start:v1`
- `stop`: `plan_id:stop:<normalized_reason>:v1`
- `snapshot`: `plan_id:snapshot:<request_counter>`
- `status`: `plan_id:status:<poll_counter>`

Executor-runtime dedupe behavior fixed now:

- repeating `prepare` with the same key returns the same `handle_id` and latest known executor status
- repeating `start` with the same key must not create a second source-native session
- repeating `stop` with the same key must not trigger a second native shutdown when the first is already accepted or terminal
- duplicates must be visible through `ack_state=duplicate` or `detail.duplicate=true`
- dedupe retention lasts until terminal plan state plus a bounded cleanup window

Planner/router retry behavior fixed now:

- retries reuse the exact same idempotency key
- planner never changes `plan_id`, `source`, `executor_profile_id`, or `pinned_commit` across retries
- ambiguous `prepare` success is reconciled against `status` or `snapshot`, not by opening another session
- no retry path may downgrade explicit Mew-X selection to Dexter

### Ack and failure propagation

Ack semantics are now fixed as transport acceptance only. An ack does not by itself prove that the native session is already `running` or terminal.

Allowed ack states:

- `accepted`
- `duplicate`
- `rejected`
- `terminal`

Rejection classes fixed now:

- `pin_mismatch`
- `unsupported_transport_version`
- `unknown_handle`
- `invalid_plan_state`
- `source_mismatch`
- `executor_profile_mismatch`
- `transport_unavailable`
- `native_prepare_rejected`
- `native_start_rejected`
- `native_stop_rejected`

Normalization rules fixed now:

- pre-start rejection on `prepare` or `start` maps to planner `prepare_failed` or `start_failed`
- status silence after accepted `start` still maps through existing `status_timeout`
- stop accepted without later terminal confirmation still maps through existing `shutdown_unconfirmed`
- explicit native stop failure still maps through existing `source_stop_failed`
- pin mismatch remains `pin_mismatch`; this task does not invent a parallel planner failure taxonomy

### Stop and rollback transport semantics

`stop(handle, reason)` stays planner-owned as a control-plane command and executor-owned as a source-native shutdown action.

Stop rules fixed now:

- planner stop reasons stay in the control-plane namespace, for example `manual_latched_stop_all`, `prepare_failed`, `start_failed`, or `quarantine_escalation`
- executor may append source-native shutdown detail, but may not rewrite the planner stop reason
- stop is best-effort, idempotent, and higher priority than further optimistic runtime progress
- reverse-order stop fanout for rollback or global halt stays the batch rule, matching the already-smoked runtime and live-paper behavior
- stop may be issued after accepted `prepare` even if `start` has not yet produced `running`
- stop completion requires both transport acceptance and later terminal confirmation through `status()` or `snapshot()`
- stop ack without terminal confirmation is not sufficient to mark `stopped`

### Status polling versus push

The normative correctness path for the first real transport cut is now fixed as planner-driven polling.

Why polling is fixed first:

- the current public seam is already `status(handle)`
- runtime smoke and live-paper smoke already prove bounded behavior with poll-shaped reconciliation
- polling keeps ordering, retry, idempotency, and terminal detection simpler for the first non-stub adapter cut

Push remains optional and bounded:

- optional pushed lifecycle events may be added later as an optimization
- push cannot be the sole correctness path for terminal-state detection
- every pushed update must be representable as a `StatusSnapshot` and reconcilable against `status(handle)`
- `StatusSink.record()` remains the normalized landing surface for both poll-derived and push-derived snapshots
- if poll and push disagree, planner keeps the latest valid monotonic transition and preserves raw disagreement in detail metadata

## What Did Not Change

- No Dexter source behavior changed.
- No Mew-X source behavior changed.
- No validator rules changed.
- No comparison evidence was recollected.
- No numeric timeout, retry, heartbeat, poll-cadence, or cap threshold was finalized.
- No wire protocol choice was finalized.

## Tests

Contract coverage now includes:

- `tests/test_planner_router_executor_transport_spec_contract.py`
- `tests/test_planner_router_livepaper_smoke.py`
- `tests/test_planner_router_runtime_smoke.py`
- `tests/test_monitor_killswitch_spec_contract.py`
- `tests/test_bootstrap_layout.py`

Validation run on this branch:

- `./scripts/build_proof_bundle.sh`
- `pytest -q`
- `64 passed`

## Recommendation Among Next Tasks

### `planner_router_executor_transport_implementation`

Recommended next because:

- transport ownership, handle semantics, idempotency, ack/failure mapping, stop confirmation, and poll-first status reconciliation are now fixed enough to implement
- another spec-only pass would reduce less risk than building the adapter/runtime bridge that this task just bounded
- observability can sit on top of the fixed transport surface rather than freezing telemetry before the real transport exists

### `livepaper_observability_spec`

Not next because:

- live-paper smoke already proves the planner-owned lifecycle at a bounded seam
- observability will be sharper once real handle ids, ack timing, and transport error classes exist in implementation

### `executor_boundary_code_spec`

Not next because:

- the abstract seam was already fixed in the interface and code-spec lanes
- this transport spec now fixes the remaining ownership/process/envelope gap without needing another boundary-only restatement

## Decision

- Outcome: `A`
- Key finding: `executor_transport_contract_fixed`
- Claim boundary: `executor_transport_spec_bounded`
- Current task status: `planner_router_executor_transport_spec_ready`
- Recommended next step: `planner_router_executor_transport_implementation`
- Decision: `planner_router_executor_transport_implementation_ready`
