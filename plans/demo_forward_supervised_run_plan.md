# DEMO-FORWARD-SUPERVISED-RUN Plan

## Objective

Promote a bounded `demo_forward_supervised_run` lane to the repo-visible current source of truth after the forward acceptance pack, without changing planner boundaries or fabricating a live-demo completion claim.

## Inputs

- `specs/DEMO_FORWARD_ACCEPTANCE_PACK.md`
- `plans/demo_forward_acceptance_pack_plan.md`
- `docs/demo_forward_operator_checklist.md`
- `docs/demo_forward_abort_rollback_matrix.md`
- `vexter/planner_router/transport.py`
- `tests/test_planner_router_executor_transport_implementation.py`

## Steps

1. Reverify latest GitHub-visible `main` after PR `#72`.
2. Keep Dexter pinned at merged PR `#3` and keep frozen Mew-X unchanged.
3. Exercise the bounded source-faithful sequence at `prepare / start / status / stop / snapshot`.
4. Record entry visibility, order status, fill reconciliation, stop-all visibility, terminal snapshot detail, and normalized failure continuity.
5. Fail closed on the real-demo claim unless external references, credentials, operator ownership, and venue connectivity are all confirmed outside the repo.
6. Promote current status, report, summary, proof json, handoff, and operator follow-up surfaces to the repo-visible current source of truth.
7. Advance the next recommended lane to `supervised_run_retry_readiness`.

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
- bounded operator-supervised window required
- funded live forbidden
- `manual_latched_stop_all` remains planner-owned

## Required Outputs

- `specs/DEMO_FORWARD_SUPERVISED_RUN.md`
- `plans/demo_forward_supervised_run_plan.md`
- `docs/demo_forward_supervised_run_operator_follow_up.md`
- `scripts/run_demo_forward_supervised_run.py`
- `artifacts/reports/demo-forward-supervised-run-report.md`
- `artifacts/reports/demo-forward-supervised-run-status.md`
- `artifacts/reports/demo-forward-supervised-run/DETAILS.md`
- `artifacts/reports/demo-forward-supervised-run/MIN_PROMPT.txt`
- `artifacts/reports/demo-forward-supervised-run/CONTEXT.json`
- `artifacts/reports/demo-forward-supervised-run/HANDOFF.md`
- `artifacts/proofs/demo-forward-supervised-run-check.json`
- `artifacts/proofs/demo-forward-supervised-run-summary.md`
- `artifacts/summary.md`
- `artifacts/context_pack.json`
- `artifacts/proof_bundle_manifest.json`
- `artifacts/task_ledger.jsonl`
- `artifacts/bundles/demo-forward-supervised-run.tar.gz`

## Acceptance

- The supervised run surface records the bounded sequence and preserves `poll_first`.
- The current proof is honest about `PASS` vs `FAIL/BLOCKED`.
- If blocked, the proof names the missing external prerequisites explicitly.
- The current handoff is continuous enough for the next operator to retry without reopening baseline work.
