# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-INPUT-ATTESTATION Plan

## Objective

Promote a bounded `supervised_run_retry_gate_input_attestation` lane to the repo-visible current source of truth after retry gate, without widening planner scope or fabricating retry execution success.

## Inputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-report.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md`
- `docs/demo_forward_supervised_run_retry_gate_checklist.md`
- `docs/demo_forward_supervised_run_retry_gate_decision_surface.md`

## Steps

1. Reverify latest GitHub-visible `main` after PR `#75`.
2. Keep Dexter pinned at merged PR `#3` and keep frozen Mew-X unchanged.
3. Accept `supervised_run_retry_gate_blocked` as the current baseline instead of retrying execution.
4. Promote an input-attestation spec, status, report, summary, proof, handoff, checklist, and decision surface as the current source of truth.
5. Fix one bounded attestation surface that makes every required gate face explicit with who attests, what is being attested, minimal evidence shape, and stale boundary.
6. Preserve the planner boundary at `prepare / start / status / stop / snapshot`, keep `poll_first`, and keep `manual_latched_stop_all` planner-owned.
7. Keep the current lane blocked unless every required attestation face is explicit enough to reopen retry-gate review.

## Guardrails

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
- operator owner explicit
- venue / connectivity confirmation explicit
- bounded start criteria explicit
- `manual_latched_stop_all` visibility reconfirmation explicit
- terminal snapshot readability reconfirmation explicit
- Mew-X unchanged
- funded live forbidden

## Required Outputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md`
- `plans/demo_forward_supervised_run_retry_gate_input_attestation_plan.md`
- `docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md`
- `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/DETAILS.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/MIN_PROMPT.txt`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/CONTEXT.json`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/SUBAGENTS.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-summary.md`
- `artifacts/summary.md`
- `artifacts/context_pack.json`
- `artifacts/proof_bundle_manifest.json`
- `artifacts/task_ledger.jsonl`
- `artifacts/bundles/demo-forward-supervised-run-retry-gate-input-attestation.tar.gz`

## Acceptance

- Retry gate remains the accepted baseline.
- The input-attestation surface records every required gate face without embedding external secrets.
- The current handoff points directly at checklist and decision-surface artifacts.
- The current lane remains `FAIL/BLOCKED` until retry execution can honestly be reconsidered from explicit attestation faces.
