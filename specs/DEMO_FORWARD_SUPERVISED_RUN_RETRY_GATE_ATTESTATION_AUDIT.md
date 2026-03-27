# Demo Forward Supervised Run Retry Gate Attestation Audit

This document fixes the bounded retry-gate attestation-audit lane after `DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION` made the required attestation faces explicit at the definition level.

## Verified Base

- Latest merged Vexter `main`: PR `#76`, merge commit `56dedfe86bf9f6252d1099775fa9506d7259e0da`, merged at `2026-03-27T07:27:42Z`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Input-attestation baseline proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`

## Purpose

The shortest next lane is still not retry execution. It is fixing one bounded retry-gate attestation-audit lane that re-audits the current attestation faces for completeness, stale conditions, and whether each face is auditable enough to reopen retry-gate review.

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

## Attestation Audit Boundary

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
- attestation audit checklist
- attestation audit decision surface
- next recommended step

## Honest Audit Model

The bounded audit lane must hold one of these honest outcomes:

- PASS: the required attestation faces are explicit, non-stale, auditable, and sufficient to reopen retry-gate review
- FAIL/BLOCKED: one or more attestation faces remain incomplete, stale, ambiguous, or not auditable enough to reopen retry-gate review

The repo may name external references, attesters, timestamps, and evidence shapes, but it must not embed credentials, secrets, or fabricated gate-pass evidence.

## Required Audit Faces

The current attestation-audit decision surface must include at least:

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
- what makes the face auditable enough

## Next-Step Boundary

- While blocked, the current lane remains `supervised_run_retry_gate_attestation_audit`.
- Only after every required attestation face is explicit, non-stale, and auditable enough may the next recommended lane advance to `supervised_run_retry_gate`.
- That pass only reopens retry-gate review; it does not claim retry execution success.

## Out Of Scope

- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no portfolio split
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success
