# Demo Executor Adapter Implementation Plan

## Goal

Implement the smallest concrete adapter needed to let Vexter start bounded forward testing on a demo account while keeping Dexter `paper_live` and frozen Mew-X `sim_live` source-faithful.

## Scope

- implement one concrete Dexter demo adapter behind the existing `ExecutorAdapter` protocol
- preserve planner-owned `poll_first`, `manual_latched_stop_all`, quarantine, and normalized failure handling
- keep Mew-X simulated or disabled for the first real demo slice

## Work Items

1. Add one Dexter demo transport target that reuses `executor_profile_id=dexter_main_pinned` and pin `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
2. Keep demo venue and credentials outside strategy semantics; the immutable plan should not introduce a new source mode.
3. Implement `prepare(plan)` to validate pin, demo connectivity prerequisites, and stable handle allocation.
4. Implement `start(handle)` to enter Dexter `paper_live` with demo connectivity enabled.
5. Implement `status(handle)` and `snapshot(handle)` to expose demo order/session state through normalized status plus rollback detail.
6. Implement `stop(handle, reason)` so `manual_latched_stop_all` cancels or flattens the demo session without rewriting planner stop reasons.
7. Keep Mew-X `sim_live` unchanged; do not introduce `trade_live` or funded paths.

## Concrete Bounded Path

- `build_demo_executor_transport_registry(...)` installs `DexterDemoExecutorAdapter` on the existing `ExecutorAdapter` seam for the Dexter-first demo slice.
- `build_source_faithful_transport_registry(...)` stays available for the broader transport and observability suites so existing planner-owned regression lanes remain unchanged.
- `DexterDemoExecutorAdapter.prepare(...)` validates:
  - pinned Dexter commit
  - `single_sleeve` route only
  - `dexter_default` sleeve only
  - explicit allowlist and small-lot config
  - bounded demo window
  - external credential references via `DEXTER_DEMO_*`
- `DexterDemoExecutorAdapter.start(...)` owns bounded `submit_order`.
- `DexterDemoExecutorAdapter.status(...)` owns `order_status` polling plus `fill_collection`.
- `DexterDemoExecutorAdapter.stop(...)` owns `cancel_order` or `stop_all` flatten request without rewriting planner stop reasons.
- `DexterDemoExecutorAdapter.snapshot(...)` confirms terminal stop-all visibility for rollback and operator handoff.

## First Acceptance Target

- one active `dexter_default` sleeve
- `single_sleeve` route only
- explicit symbol allowlist
- small lot only
- bounded demo window
- operator can stop all and confirm terminal snapshot visibility

## Non-Goals

- no source logic changes in Dexter or Mew-X
- no funded live trading
- no portfolio split
- no mid-trade handoff
- no new comparison or evidence collection work inside this implementation lane

## Exit Criteria

- bounded adapter tests cover submit / cancel / status / fill / stop-all mapping
- current CI-gated observability surfaces remain green
- artifact outputs recommend `demo_forward_acceptance_pack` only after the concrete adapter is in place
