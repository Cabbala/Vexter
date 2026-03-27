# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-ATTESTATION-AUDIT Plan

## Objective

Promote a bounded `supervised_run_retry_gate_attestation_audit` lane to the repo-visible current source of truth after retry-gate input attestation, without widening planner scope or fabricating retry-gate reopen or retry execution success.

## Inputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_INPUT_ATTESTATION.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation-report.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-input-attestation-check.json`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-input-attestation/HANDOFF.md`
- `docs/demo_forward_supervised_run_retry_gate_input_attestation_checklist.md`
- `docs/demo_forward_supervised_run_retry_gate_input_attestation_decision_surface.md`

## Steps

1. Reverify latest GitHub-visible `main` after PR `#76`.
2. Keep Dexter pinned at merged PR `#3` and keep frozen Mew-X unchanged.
3. Accept `supervised_run_retry_gate_input_attestation_blocked` as the current baseline instead of reopening retry-gate review or retrying execution.
4. Promote an attestation-audit spec, status, report, summary, proof, handoff, checklist, and decision surface as the current source of truth.
5. Re-audit every required face for definition completeness, stale-rule completeness, and whether the face is currently auditable enough to reopen retry-gate review.
6. Preserve the planner boundary at `prepare / start / status / stop / snapshot`, keep `poll_first`, and keep `manual_latched_stop_all` planner-owned.
7. Keep the current lane blocked unless every required attestation face is explicit, non-stale, and auditable enough to reopen retry-gate review.

## Guardrails

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

## Required Outputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_AUDIT.md`
- `plans/demo_forward_supervised_run_retry_gate_attestation_audit_plan.md`
- `docs/demo_forward_supervised_run_retry_gate_attestation_audit_checklist.md`
- `docs/demo_forward_supervised_run_retry_gate_attestation_audit_decision_surface.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-report.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/DETAILS.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/MIN_PROMPT.txt`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/CONTEXT.json`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/HANDOFF.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-audit/SUBAGENTS.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-check.json`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-audit-summary.md`
- `artifacts/summary.md`
- `artifacts/context_pack.json`
- `artifacts/proof_bundle_manifest.json`
- `artifacts/task_ledger.jsonl`
- `artifacts/bundles/demo-forward-supervised-run-retry-gate-attestation-audit.tar.gz`

## Acceptance

- Retry-gate input attestation remains the accepted baseline.
- The attestation-audit surface records completeness, stale conditions, and auditable-enough conditions for every required face without embedding external secrets.
- The current handoff points directly at checklist and decision-surface artifacts.
- The current lane remains `FAIL/BLOCKED` until retry-gate review can honestly be reconsidered from current, non-stale, auditable attestation faces.
