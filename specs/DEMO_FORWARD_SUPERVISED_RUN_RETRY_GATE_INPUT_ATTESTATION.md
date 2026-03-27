# Demo Forward Supervised Run Retry Gate Input Attestation

This document fixes the bounded retry-gate input-attestation lane after `DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE` made the unresolved gate inputs current and reviewable.

## Verified Base

- Latest merged Vexter `main`: PR `#75`, merge commit `b9e556ffc57592190fdffbcabf61ab168b8ed467`, merged at `2026-03-27T01:50:11Z`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Retry-gate baseline proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`

## Purpose

The shortest next lane is not retry execution. It is fixing one bounded retry-gate input-attestation lane that records, fail-closed, who attests each required gate face, what is being attested, the minimum evidence shape, and when the attestation becomes stale.

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

## Attestation Boundary

The bounded retry-gate input-attestation lane remains:

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
- operator owner explicit
- venue / connectivity confirmation explicit
- bounded start criteria explicit
- allowlist / symbol / lot-size reconfirmation explicit
- `manual_latched_stop_all` visibility reconfirmation explicit
- terminal snapshot readability reconfirmation explicit
- Mew-X unchanged
- funded live forbidden

## Required Current Surfaces

The repo must expose the following as current source of truth:

- current status report
- current report
- current summary
- current proof json
- current handoff
- gate input attestation checklist
- gate input attestation decision surface
- next recommended step

## Honest Attestation Model

The bounded attestation lane must hold one of these honest outcomes:

- PASS: the required gate-input attestation faces are explicit enough to reopen retry-gate review
- FAIL/BLOCKED: one or more attestation faces remain unresolved, stale, or not explicit enough to reopen retry-gate review

The repo may name external references, attesters, timestamps, and evidence shapes, but it must not embed credentials, secrets, or fabricated pass evidence.

## Attestation Face Model

The current attestation decision surface must include at least:

- credential source face
- venue ref face
- account ref face
- connectivity profile face
- operator owner face
- bounded start criteria face
- allowlist / symbol / lot-size reconfirmation face
- `manual_latched_stop_all` visibility face
- terminal snapshot readability face

Each face must make explicit:

- who attests
- what is being attested
- minimal evidence shape
- when the attestation is stale

## Next-Step Boundary

- While blocked, the current lane remains `supervised_run_retry_gate_input_attestation`.
- Only after every required attestation face is explicit enough may the next recommended lane advance to `supervised_run_retry_execution`.
- That pass means gate review can honestly reopen without hidden assumptions; it does not fabricate a completed retry execution.

## Out Of Scope

- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no portfolio split
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success
