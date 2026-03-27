# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE Plan

## Objective

Promote a bounded `supervised_run_retry_gate` lane to the repo-visible current source of truth after retry readiness, without widening planner scope or fabricating retry execution success.

## Inputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md`
- `docs/demo_forward_supervised_run_retry_readiness_checklist.md`
- `docs/demo_forward_supervised_run_retry_prerequisite_matrix.md`

## Steps

1. Reverify latest GitHub-visible `main` after PR `#74`.
2. Keep Dexter pinned at merged PR `#3` and keep frozen Mew-X unchanged.
3. Accept `supervised_run_retry_readiness_blocked` as the current baseline instead of retrying execution.
4. Promote a retry-gate spec, status, report, summary, proof, handoff, checklist, and decision surface as the current source of truth.
5. Fix one bounded gate decision surface that makes every required gate input explicit and fail-closed.
6. Preserve the planner boundary at `prepare / start / status / stop / snapshot`, keep `poll_first`, and keep `manual_latched_stop_all` planner-owned.
7. Keep the current lane blocked unless every gate input is explicit enough to enter `supervised_run_retry_execution`.

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
- operator owner must be explicit
- venue / connectivity confirmation must be explicit
- bounded start criteria must be explicit
- `manual_latched_stop_all` visibility must be reconfirmed
- terminal snapshot readability must be reconfirmed
- Mew-X unchanged
- funded live forbidden

## Required Outputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE.md`
- `plans/demo_forward_supervised_run_retry_gate_plan.md`
- `docs/demo_forward_supervised_run_retry_gate_checklist.md`
- `docs/demo_forward_supervised_run_retry_gate_decision_surface.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-report.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/DETAILS.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/MIN_PROMPT.txt`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/CONTEXT.json`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/HANDOFF.md`
- `artifacts/reports/demo-forward-supervised-run-retry-gate/SUBAGENTS.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-check.json`
- `artifacts/proofs/demo-forward-supervised-run-retry-gate-summary.md`
- `artifacts/summary.md`
- `artifacts/context_pack.json`
- `artifacts/proof_bundle_manifest.json`
- `artifacts/task_ledger.jsonl`
- `artifacts/bundles/demo-forward-supervised-run-retry-gate.tar.gz`

## Acceptance

- Retry readiness remains the accepted baseline.
- The retry-gate surface records every required gate input without embedding external secrets.
- The current handoff points directly at checklist and decision-surface artifacts.
- The current lane remains `FAIL/BLOCKED` until retry execution is honestly permitted.
