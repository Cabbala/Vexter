# Demo Forward Supervised Run Retry Gate

This document fixes the bounded retry-gate lane after `DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS` made the external prerequisite gap current and reviewable.

## Verified Base

- Latest merged Vexter `main`: PR `#74`, merge commit `d06856cecf42c336af05902a1d932468c5d280b0`, merged at `2026-03-27T01:20:35Z`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Retry-readiness baseline proof: `artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json`

## Purpose

The shortest next lane is not retry execution. It is fixing one bounded retry gate that decides, fail-closed, whether the repo-visible and externally confirmed inputs are explicit enough to let `supervised_run_retry_execution` begin.

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

## Retry Gate Boundary

The bounded retry-gate lane remains:

- Dexter-only real demo slice
- `single_sleeve`
- `dexter_default`
- Dexter `paper_live`
- frozen Mew-X `sim_live`
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded supervised window required
- external credential refs remain outside repo
- operator owner must be explicit
- venue / connectivity confirmation must be explicit
- bounded start criteria must be explicit
- allowlist / symbol / lot-size reconfirmation must be explicit
- `manual_latched_stop_all` visibility must be reconfirmed
- terminal snapshot readability must be reconfirmed
- Mew-X unchanged
- funded live forbidden

## Required Current Surfaces

The repo must expose the following as current source of truth:

- current status report
- current report
- current summary
- current proof json
- current handoff
- retry gate checklist
- retry gate decision surface
- next recommended step

## Honest Gate Model

The bounded retry gate must hold one of these honest outcomes:

- PASS: the gate inputs are explicit enough to enter `supervised_run_retry_execution`
- FAIL/BLOCKED: one or more gate inputs remain unresolved, so retry execution does not begin

The repo may name external references and confirmations, but it must not embed credentials, secrets, or fabricated pass evidence.

## Gate Input Model

The gate decision surface must include at least:

- external credential source face explicit
- venue ref face explicit
- account ref face explicit
- connectivity profile face explicit
- operator owner face explicit
- bounded start criteria explicit
- allowlist / symbol / lot-size reconfirmed
- `manual_latched_stop_all` visibility reconfirmed
- terminal snapshot readability reconfirmed

## Next-Step Boundary

- While blocked, the current lane remains `supervised_run_retry_gate`.
- Only after every gate input is explicit enough may the next recommended lane advance to `supervised_run_retry_execution`.

## Out Of Scope

- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no portfolio split
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success
