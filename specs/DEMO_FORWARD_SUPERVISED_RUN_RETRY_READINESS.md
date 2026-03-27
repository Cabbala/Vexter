# Demo Forward Supervised Run Retry Readiness

This document fixes the bounded retry-readiness lane after `DEMO-FORWARD-SUPERVISED-RUN` fail-closed on unresolved external prerequisites.

## Verified Base

- Latest merged Vexter `main`: PR `#73`, merge commit `aea530368fc5b59b87dd08a38c2629392ea8d706`, merged at `2026-03-27T00:56:46Z`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Blocked baseline source of truth: `specs/DEMO_FORWARD_SUPERVISED_RUN.md`
- Blocked baseline proof: `artifacts/proofs/demo-forward-supervised-run-check.json`

## Purpose

The shortest next lane is not another blind supervised retry. It is fixing the operator-visible retry-readiness surface so the external prerequisite gap stays bounded, current, and reviewable before any retry gate or retry execution is attempted.

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

## Retry Readiness Boundary

The bounded retry-readiness lane remains:

- Dexter-only real demo slice
- Dexter `paper_live`
- frozen Mew-X `sim_live`
- `single_sleeve`
- `dexter_default`
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded supervised window required
- external credential refs remain outside repo
- operator owner must be explicit
- venue / connectivity confirmation must be explicit
- allowlist / symbol / lot-size reconfirmation must be explicit
- stop-all visibility must be reconfirmed before retry
- Mew-X unchanged
- funded live forbidden

## Required Current Surfaces

The repo must expose the following as current source of truth:

- current status report
- current report
- current summary
- current proof json
- current handoff
- retry readiness checklist
- retry prerequisite matrix
- next recommended step

## External Prerequisite Model

The bounded prerequisite model must keep these faces explicit:

- `DEXTER_DEMO_CREDENTIAL_SOURCE`
- `DEXTER_DEMO_VENUE_REF`
- `DEXTER_DEMO_ACCOUNT_REF`
- `DEXTER_DEMO_CONNECTIVITY_PROFILE`
- named operator owner
- bounded supervised-window start criteria
- allowlist / symbol / lot-size reconfirmation
- stop-all visibility reconfirmation

The repo may name these prerequisite faces, but it must not embed the external credentials or venue/account secrets themselves.

## Honest Outcome Model

The retry-readiness lane must hold one of these honest outcomes:

- PASS: retry prerequisites are explicitly satisfied enough to attempt the next bounded retry lane
- FAIL/BLOCKED: one or more external prerequisites remain unresolved

If the readiness lane is blocked, the proof must still show:

- the blocked supervised run remains the accepted baseline
- the exact missing prerequisite faces
- who must confirm each face
- what confirmation is sufficient to enter the retry gate
- the next minimal retry lane

## Next-Step Boundary

The next recommended lane must be one of:

- `supervised_run_retry_execution`
- `supervised_run_retry_gate`

When external prerequisites remain unresolved, the next smallest honest lane is `supervised_run_retry_gate`.

## Out Of Scope

- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no portfolio split
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success

## Recommended Next Task

`supervised_run_retry_gate`

This readiness lane fixes the current prerequisite surface only. It does not claim that the next retry may start until the gate inputs are explicitly confirmed.
