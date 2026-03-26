# PATTERN-A-DEMO-EXECUTOR-CUTOVER Report

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#69` merge commit `289eb1bc87a8db9a9801b9b0583a8dbc6b17a5b3` on `2026-03-26T23:03:14Z`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Open Vexter PR `#50` remained non-authoritative relative to merged `main`.

## What This Task Did

- Froze the existing transport and handoff observability CI gates as sufficient stop conditions instead of opening another observability lane.
- Fixed Dexter `paper_live` as the first real demo target and kept Mew-X frozen on `sim_live`.
- Kept the public planner boundary at `prepare`, `start`, `status`, `stop`, and `snapshot`.
- Fixed demo order submit, cancel, fill collection, and stop-all fanout as adapter-owned responsibilities behind that unchanged planner boundary.
- Narrowed the next implementation cut to one bounded Dexter-only demo adapter without changing source logic, thresholds, trust semantics, or the comparison baseline.

## Fixed Boundary

Planner-owned:

- immutable plan emission
- correlation and idempotency intent
- `poll_first` reconciliation
- timeout and quarantine classification
- `manual_latched_stop_all`
- normalized `StatusSink` fan-in

Adapter-owned:

- `paper_live` pin and mode validation
- handle and native session/order identity continuity
- demo order submit
- demo order cancel
- demo order status polling
- demo fill collection
- terminal stop confirmation
- normalized failure and stop reason passthrough

Real now:

- Dexter demo-account connectivity on the existing `paper_live` seam
- Dexter demo order submit / cancel / status / fill / stop-all

Still simulated or deferred:

- Mew-X `sim_live`
- cross-source handoff
- funded live trading
- portfolio-split real execution

## First Acceptance Slice

- Dexter-only route
- one active handle and one open position max
- explicit allowlist
- small lot only
- operator-supervised bounded window
- `prepare -> start -> entry/exit -> fill/status reconciliation -> cancel/stop-all -> terminal snapshot`
- no regression on the current CI-gated observability surfaces

## Recommendation Among Next Tasks

### `demo_executor_adapter_implementation`

Recommended because:

- the transport boundary is already fixed at the planner-versus-adapter level
- the repo now has a specific first demo target and acceptance slice
- this is the shortest path to forward-test readiness

### `demo_executor_code_spec`

Not recommended now because:

- another code-spec pass would mostly restate the existing executor transport contract plus this cutover boundary
- the sharper next step is a concrete adapter, not another boundary memo

### `demo_forward_acceptance_pack`

Not recommended now because:

- the acceptance pack becomes meaningful only after the concrete demo adapter exists
- packaging before implementation would mostly rephrase planned surfaces instead of validating them

## Decision

- Outcome: `A`
- Key finding: `pattern_a_demo_executor_boundary_fixed`
- Claim boundary: `pattern_a_demo_executor_cutover_bounded`
- Current task status: `pattern_a_demo_executor_cutover_ready`
- Recommended next step: `demo_executor_adapter_implementation`
- Decision: `demo_executor_adapter_implementation_ready`

## Key Paths

- Current spec: `specs/PATTERN_A_DEMO_EXECUTOR_CUTOVER.md`
- Current implementation plan: `plans/demo_executor_adapter_implementation_plan.md`
- Current proof: `artifacts/proofs/pattern-a-demo-executor-cutover-check.json`
- Current summary: `artifacts/proofs/pattern-a-demo-executor-cutover-summary.md`
- Current handoff: `artifacts/reports/pattern-a-demo-executor-cutover/HANDOFF.md`
- Current bundle target: `artifacts/bundles/pattern-a-demo-executor-cutover.tar.gz`
