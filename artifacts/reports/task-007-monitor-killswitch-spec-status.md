# TASK-007 Monitor Kill-Switch Spec Status

## Verified Start

- Vexter `origin/main` verified at PR `#40` commit `a4e7a3c74460dc711c3e2897ac31386272e91c27`
- Dexter `main` verified at PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X verified at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Current Result

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior lane source state: `planner_router_runtime_smoke_passed`
- Monitor profiles are fixed as immutable per-plan bindings with the committed `dexter_default` and `mewx_timeout_guard` class tuples preserved
- Admission gates stay pre-emission and fail closed on config invalidity, pin mismatch, disabled sleeve, budget overflow, or active global halt
- Timeout envelopes stay source-shaped classes with numeric heartbeat, retry, and timeout values deferred
- Quarantine remains sleeve-scoped; current participating profiles can escalate into reverse-order stop-all rollback without enabling cross-source handoff
- Global halt remains `manual_latched_stop_all`: freeze new planning plus source-native stop requests only
- Typed failure escalation stays on `FailureCode`, `FailureDetail`, and `StatusSnapshot`, with source-native reasons carried as passthrough metadata
- Validation: `pytest -q` -> `58 passed`

## Decision

- Current task: `monitor_killswitch_spec_ready`
- Key finding: `monitor_killswitch_contract_fixed`
- Claim boundary: `monitor_killswitch_spec_bounded`
- Recommended next step: `planner_router_livepaper_smoke`
- Decision: `planner_router_livepaper_smoke_ready`

The planner/router control plane now has a source-faithful monitor/killswitch contract anchored to the already-proven runtime seam. The shortest next cut is live-paper smoke using these fixed quarantine and halt semantics, not another boundary-only restatement.
