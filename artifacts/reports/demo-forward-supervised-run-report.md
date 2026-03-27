# DEMO-FORWARD-SUPERVISED-RUN Report

## Verified Base

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#72`, merge commit `a6ca623b01dbed4191c4be10c2bfe51534025cac`, merged at `2026-03-27T00:32:14Z`.
- Dexter remained pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen Mew-X remained pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What Landed

- Exercised the bounded `prepare / start / status / stop / snapshot` sequence through `DexterDemoExecutorAdapter`.
- Captured entry visibility, fill reconciliation, stop-all visibility, terminal snapshot detail, and handoff continuity as the current source of truth.
- Promoted a fail-closed supervised-run lane that does not fabricate a real-demo completion claim when external prerequisites remain unresolved.
- Kept the public planner boundary unchanged and kept funded live forbidden.

## Supervised Run Boundary

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

## Observed Sequence

1. `prepare` exposed `demo_runtime`, `symbol_allowlist`, `demo_symbol`, `small_lot_order_size`, and `bounded_window_minutes=15`.
2. `start` moved the handle into a bounded running state without widening the planner boundary.
3. `status` surfaced `native_order_status=filled`, `fill_count=1`, and `open_position_lots=0.05`.
4. `stop` preserved stop-all visibility with `stop_all_state=flatten_requested`.
5. `snapshot` preserved terminal detail with `stop_all_state=flatten_confirmed` and `fill_count=2`.

## Outcome

- Outcome: `FAIL/BLOCKED`
- Key finding: `demo_forward_supervised_run_blocked_on_external_prerequisites`
- Claim boundary: `demo_forward_supervised_run_fail_closed`
- Current task state: `demo_forward_supervised_run_blocked`
- Blocker: the repo-visible lane can exercise bounded runtime visibility, but it cannot honestly claim a real Dexter supervised window because external reference resolution, operator ownership, and venue connectivity remain outside the repo and unverified.
- Run timestamp: `2026-03-27T00:51:26Z`

## Required Current Surfaces

- current status report: `artifacts/reports/demo-forward-supervised-run-status.md`
- current report: `artifacts/reports/demo-forward-supervised-run-report.md`
- current summary: `artifacts/proofs/demo-forward-supervised-run-summary.md`
- current proof json: `artifacts/proofs/demo-forward-supervised-run-check.json`
- current handoff: `artifacts/reports/demo-forward-supervised-run/HANDOFF.md`
- supervised run operator follow-up: `docs/demo_forward_supervised_run_operator_follow_up.md`

## Recommendation

- Current task state: `demo_forward_supervised_run_blocked`
- Recommended next step: `supervised_run_retry_readiness`
- Reason: the bounded proof lane is current, but external prerequisites must be resolved outside the repo before a real-demo completion claim can be promoted.
