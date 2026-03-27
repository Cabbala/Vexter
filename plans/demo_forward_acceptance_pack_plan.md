# Demo Forward Acceptance Pack Plan

## Goal

Fix the minimum bounded acceptance, operator, proof, and handoff surfaces required to start the first Dexter-only supervised forward demo run without changing the planner boundary or reopening source logic.

## Scope

- keep the public planner boundary at `prepare / start / status / stop / snapshot`
- treat `DexterDemoExecutorAdapter` as the implemented base
- define current acceptance artifacts as repo-visible source of truth
- define operator and abort expectations without handling secrets or executing a real run

## Work Items

1. Fix the acceptance boundary to Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, one active real demo plan, one open position max, explicit allowlist, small lot, and bounded operator supervision.
2. Add a current spec, current report, current status, proof summary, proof json, handoff, operator checklist, and abort / rollback matrix for the forward-demo slice.
3. Keep Mew-X unchanged on frozen `sim_live` and keep funded live forbidden.
4. Reuse the current proof and handoff surfaces already established for transport and shift-handoff observability instead of inventing a new reporting shape.
5. Advance the next recommended lane from `demo_executor_adapter_implementation` to `demo_forward_supervised_run`.

## Acceptance Sequence To Fix

- `prepare`
- `start`
- entry visibility
- order status / fill reconciliation
- cancel or stop-all visibility
- terminal snapshot
- normalized failure detail / handoff continuity

## Operator Requirements

- validate external credential references before the window opens
- confirm symbol allowlist and small lot remain bounded
- confirm `manual_latched_stop_all` can be used immediately
- confirm terminal snapshot and proof surfaces remain visible before handoff

## Non-Goals

- no supervised run execution yet
- no funded live introduction
- no Mew-X real-demo path
- no planner API change
- no Dexter or Mew-X source logic rewrite
- no comparison-baseline reopen

## Exit Criteria

- current source of truth points at the acceptance pack artifacts
- operator checklist and abort / rollback matrix are explicit
- next recommended task is `demo_forward_supervised_run`
- pytest and bounded regression checks are green
