# Demo Forward Supervised Run

This document fixes the bounded supervised forward-demo lane after the acceptance pack became the repo-visible current source of truth.

## Verified Base

- Latest merged Vexter `main`: PR `#72`, merge commit `a6ca623b01dbed4191c4be10c2bfe51534025cac`, merged at `2026-03-27T00:32:14Z`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Acceptance pack source of truth: `specs/DEMO_FORWARD_ACCEPTANCE_PACK.md`
- Demo adapter source of truth: `vexter/planner_router/transport.py`

## Purpose

The shortest next lane is the bounded supervised Dexter-only forward run. This task must either complete the required visibility surface inside the supervised window or fail closed without fabricating a live-demo success claim.

## Planner Boundary Remains Fixed

The public planner surface remains:

- `prepare`
- `start`
- `status`
- `stop`
- `snapshot`

Planner ownership remains unchanged:

- immutable plan emission
- `poll_first` reconciliation
- `manual_latched_stop_all`
- quarantine classification
- normalized failure detail fan-in

Adapter-owned runtime detail remains unchanged:

- source-native demo submit
- source-native cancel
- order status polling
- fill collection
- stop-all fanout and terminal snapshot detail

## Supervised Run Boundary

The bounded supervised run remains:

- Dexter-only real demo slice
- Dexter `paper_live` only
- frozen Mew-X `sim_live` only
- `single_sleeve` route only
- `dexter_default` sleeve only
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded operator-supervised window required
- Mew-X overlay disabled / unchanged
- funded live forbidden

## Required Current Surfaces

The repo must expose the following as current source of truth:

- current status report
- current report
- current summary
- current proof json
- current handoff
- supervised run operator follow-up
- next recommended step

## Required Sequence

The required supervised sequence is:

1. `prepare`
2. `start`
3. entry visibility
4. order status / fill reconciliation
5. stop or stop-all visibility
6. terminal snapshot
7. normalized failure detail and handoff continuity
8. supervised window outcome

## Required Outcome Handling

The supervised lane must hold one of these honest outcomes:

- PASS: bounded supervised run completed with required visibility
- FAIL/BLOCKED: external references, credentials, operator attestation, venue connectivity, or bounded abort conditions prevented a real-demo completion claim

If the real-demo claim is blocked, the proof must still show:

- the bounded planner and adapter sequence remained source-faithful
- the exact external prerequisite gap that prevented the live claim
- the current report, proof, summary, and handoff pointers
- the next minimal retry lane

## Abort And Rollback Conditions

Abort or rollback remains mandatory on:

- pin mismatch
- mode mismatch
- status or fill reconciliation gap
- duplicate or ambiguous handle
- unexpected funded live path
- cancel or stop-all unconfirmed
- quarantine or manual halt triggered
- terminal snapshot visibility lost

## Out Of Scope

- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no portfolio split
- no comparison baseline reopen
- no Dexter or Mew-X source logic rewrite

## Recommended Next Task

`supervised_run_retry_readiness`

This supervised lane may fail closed. The next task after a blocked run is the smallest retry-readiness cut that resolves external prerequisites without widening scope.
