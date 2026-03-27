# DEMO-EXECUTOR-ADAPTER-IMPLEMENTATION Report

## Verified Base

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#70`, merge commit `ccea54002189eaa8f6885284c7ef63506bb470be`, merged at `2026-03-26T23:42:15Z`.
- Dexter remained pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen Mew-X remained pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What Landed

- Added `DexterDemoExecutorAdapter` in `vexter/planner_router/transport.py` as the smallest concrete Dexter demo runtime behind the unchanged `prepare / start / status / stop / snapshot` planner boundary.
- Added `build_demo_executor_transport_registry(...)` so the first bounded real-demo slice can select the concrete Dexter path without disturbing the existing source-faithful transport and observability suites.
- Kept `build_source_faithful_transport_registry(...)` intact for the current broad regression lanes.
- Kept Mew-X unchanged on the existing `sim_live` path.

## Adapter Behavior

- `prepare(plan)` validates the pinned Dexter commit, `single_sleeve`, `dexter_default`, explicit symbol allowlist, small-lot cap, bounded demo window, and external credential references.
- `start(handle)` owns bounded `submit_order`.
- `status(handle)` owns `order_status` polling and `fill_collection`.
- `stop(handle, reason)` owns `cancel_order` or stop-all flatten request while preserving planner stop reasons.
- `snapshot(handle)` confirms terminal stop-all visibility for rollback and operator readability.

## Guardrails Preserved

- one active Dexter demo plan at a time
- `single_sleeve` route only
- `dexter_default` sleeve only
- explicit allowlist only
- small lot only
- bounded supervised demo window only
- no funded live path
- no Mew-X real-demo conversion
- no public planner API drift

## Validation

- `tests/test_planner_router_executor_transport_implementation.py`
- `tests/test_planner_router_transport.py`
- `tests/test_planner_router_transport_runtime_smoke.py`
- `tests/test_planner_router_livepaper_smoke.py`
- `tests/test_planner_router_transport_livepaper_observability_smoke.py`
- `tests/test_planner_router_transport_livepaper_observability_runtime.py`
- `tests/test_planner_router_transport_livepaper_observability_hardening.py`
- `tests/test_planner_router_transport_livepaper_observability_regression_pack.py`
- `tests/test_planner_router_transport_livepaper_observability_ci_gate.py`
- `tests/test_planner_router_transport_livepaper_observability_watchdog.py`
- `tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py`
- `tests/test_planner_router_transport_livepaper_observability_watchdog_ci_gate.py`
- `tests/test_planner_router_executor_transport_spec_contract.py`

## Recommendation

- Current task state: `demo_executor_adapter_implemented`
- Recommended next step: `DEMO-FORWARD-ACCEPTANCE-PACK`
- Reason: the concrete Dexter demo adapter now exists in bounded form, and the next meaningful lane is a forward acceptance pack rather than more boundary work.
