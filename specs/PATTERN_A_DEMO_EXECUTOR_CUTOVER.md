# Pattern A Demo Executor Cutover

This document fixes the bounded Pattern A cutover boundary for Vexter after the transport and handoff observability lanes were completed on GitHub-visible `main`.

## Purpose

The next shortest route is not more observability deepening. It is enabling a demo-account forward path on the existing source-faithful seam so the next implementation task can wire a real demo executor without reopening comparison work or changing frozen source logic.

## Fixed Inputs

- Latest merged Vexter `main`: PR `#69`, merge commit `289eb1bc87a8db9a9801b9b0583a8dbc6b17a5b3`, merged at `2026-03-26T23:03:14Z`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Comparison source of truth: `comparison_closed_out`
- Status delivery: `poll_first`
- Global halt mode: `manual_latched_stop_all`

## Stop Boundary

The repo already treats observability, handoff, and watchdog work as sufficient:

- transport watchdog CI gate is fixed and GitHub-visible
- shift-handoff watchdog CI gate is fixed and GitHub-visible
- immutable plan and handle continuity remain bounded
- no new evidence collection is required before choosing the executor cutover boundary

This task therefore freezes the current CI-gated observability surface as the operator-facing sufficient condition for moving to Pattern A.

## Source-Faithful Seam

The seam remains unchanged:

- Dexter stays `paper_live` via `monitor_mint_session`
- Mew-X stays frozen `sim_live` via `start_session` / `sim_session`
- no mid-trade handoff
- no threshold transplant
- no trust-logic transplant
- no funded live trading
- no comparison-baseline reopen

## First Demo Target

The first demo target is Dexter only.

Why:

- Dexter is the default execution anchor on the fixed planning surface
- Dexter already owns the source-faithful `paper_live` entrypoint
- Mew-X is explicitly frozen on `sim_live`, so forcing it into a new real-demo role would break the current seam

## Minimal Executor Boundary

Planner/router ownership remains unchanged:

- immutable plan emission
- correlation ids and idempotency intent
- timeout classification and quarantine escalation
- `manual_latched_stop_all`
- normalized status fan-in via `StatusSink`

The new adapter-owned boundary for Pattern A is limited to source-native demo execution:

- `submit_order`
- `cancel_order`
- `order_status`
- `fill_state`
- `stop_all`

These stay behind the existing `ExecutorAdapter` lifecycle:

- `prepare(plan)` validates pins, demo transport readiness, and allocates a stable handle
- `start(handle)` starts the Dexter `paper_live` session and enables source-local order activity
- `status(handle)` polls the demo runtime and maps source-native order/session state back to normalized `StatusSnapshot`
- `stop(handle, reason)` cancels or flattens the live demo session and preserves planner-owned stop reasons
- `snapshot(handle)` surfaces native session and order detail for rollback, failure detail, and handoff readability

## Real vs Simulated

Real now:

- Dexter `paper_live` demo-account connectivity through a concrete Dexter adapter
- demo order submit / cancel / status / fill / stop-all on the Dexter leg

Still simulated or deferred:

- Mew-X remains `sim_live`
- Mew-X overlay stays disabled for the first real demo slice
- funded live execution remains disabled
- portfolio split remains deferred
- push-first status delivery remains deferred

## Guardrails

The first real demo slice must stay narrow:

- one active real demo plan at a time
- `single_sleeve` route only
- `dexter_default` sleeve only
- explicit allowlist required
- small-lot execution required
- bounded forward window required
- immediate abort on pin mismatch, quarantine escalation, stop-confirmation loss, or status continuity loss

## Acceptance Slice

Pattern A acceptance is satisfied only when all of the following are true:

1. The existing transport watchdog CI gate and shift-handoff watchdog CI gate are green.
2. A concrete Dexter demo adapter implements `prepare`, `start`, `status`, `stop`, and `snapshot` without changing source semantics.
3. The adapter proves source-native demo order submit / cancel / status / fill / stop-all ownership while preserving normalized planner status and failure detail.
4. The first forward slice runs only on Dexter `paper_live`, while Mew-X remains `sim_live` or disabled.
5. `manual_latched_stop_all` remains planner-owned and visibly reaches the real demo session.
6. Terminal snapshot and normalized failure detail remain available on the same proof and handoff surfaces already fixed in CI.

## Recommended Next Task

`demo_executor_adapter_implementation`

Another code-spec restatement would duplicate the existing executor transport boundary, and an acceptance pack would be premature before the concrete Dexter demo adapter exists.
