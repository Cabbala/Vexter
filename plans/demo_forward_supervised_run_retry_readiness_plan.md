# DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS Plan

## Objective

Promote a bounded `supervised_run_retry_readiness` lane to the repo-visible current source of truth after the blocked supervised run, without widening planner scope or fabricating retry execution success.

## Inputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN.md`
- `artifacts/reports/demo-forward-supervised-run-status.md`
- `artifacts/reports/demo-forward-supervised-run-report.md`
- `artifacts/proofs/demo-forward-supervised-run-check.json`
- `artifacts/reports/demo-forward-supervised-run/HANDOFF.md`
- `docs/demo_forward_supervised_run_operator_follow_up.md`
- `docs/demo_forward_operator_checklist.md`
- `docs/demo_forward_abort_rollback_matrix.md`

## Steps

1. Reverify latest GitHub-visible `main` after PR `#73`.
2. Keep Dexter pinned at merged PR `#3` and keep frozen Mew-X unchanged.
3. Accept `demo_forward_supervised_run_blocked` as the current baseline instead of retrying execution.
4. Promote a retry-readiness spec, status, report, summary, proof, handoff, checklist, and prerequisite matrix as the current source of truth.
5. Fix the external prerequisite gap in bounded terms: what is missing, who confirms it, and what confirmation is enough for retry gate entry.
6. Preserve the planner boundary at `prepare / start / status / stop / snapshot`, keep `poll_first`, and keep `manual_latched_stop_all` planner-owned.
7. Advance the next recommended lane to `supervised_run_retry_gate` unless all external prerequisites are already resolved.

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
- stop-all visibility must be reconfirmed before retry
- Mew-X unchanged
- funded live forbidden
- `manual_latched_stop_all` remains planner-owned

## Required Outputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_READINESS.md`
- `plans/demo_forward_supervised_run_retry_readiness_plan.md`
- `docs/demo_forward_supervised_run_retry_readiness_checklist.md`
- `docs/demo_forward_supervised_run_retry_prerequisite_matrix.md`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness-report.md`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness-status.md`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness/DETAILS.md`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness/MIN_PROMPT.txt`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness/CONTEXT.json`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness/HANDOFF.md`
- `artifacts/reports/demo-forward-supervised-run-retry-readiness/SUBAGENTS.md`
- `artifacts/proofs/demo-forward-supervised-run-retry-readiness-check.json`
- `artifacts/proofs/demo-forward-supervised-run-retry-readiness-summary.md`
- `artifacts/summary.md`
- `artifacts/context_pack.json`
- `artifacts/proof_bundle_manifest.json`
- `artifacts/task_ledger.jsonl`
- `artifacts/bundles/demo-forward-supervised-run-retry-readiness.tar.gz`

## Acceptance

- The blocked supervised run remains the accepted baseline.
- The retry-readiness surface records the bounded prerequisite gap without embedding external secrets.
- The current handoff points directly at checklist and matrix surfaces.
- The next recommended lane advances to `supervised_run_retry_gate` instead of silently retrying execution.
