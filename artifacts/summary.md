# TASK-005 Live Comparison Evidence Summary

## Status

- `TASK-005-live-comparison-evidence` remains in `partial_live_comparison_blocker` state on branch `codex/task-005-pass-grade-pair` as of `2026-03-20T21:19:29Z`.
- Start conditions were re-verified from `Cabbala/Vexter` latest `main` commit `1b9ace272d63bcc5be8f30aa1e2a2ab03b63304f`; PR `#6` was confirmed merged on `2026-03-21T05:46:44+09:00`.
- Dexter and Mew-X strategy, execution, and instrumentation logic remain unchanged.
- Sub-agents `Socrates` and `Locke` were launched for parallel runbook / blocker inspection while the main thread handled Windows collection retries, contract fixes, and evidence closeout.

## Collection Results

- The validator contract was corrected so `entry_rejected.tx_signature` is optional when transport or balance guards never returned a signature. This removes the old payload false-negative without changing Dexter or Mew-X logic.
- A fresh safe-mode collection kept both frozen sources concurrently active from `2026-03-20T20:58:40.760Z` to `2026-03-20T21:01:52.838Z`.
- Exact event overlap inside that runtime window was `2026-03-20T20:59:55.254Z` -> `2026-03-20T21:01:52.838Z` (`117.584s`), which resolves the old `281 ms` overlap blocker.
- The concurrent runtime-window packages were rerun through `validate`, `derive-metrics`, and `build-pack` on the Mac control plane.
- Dexter runtime-window package `dexter-pass-20260320T205803Z` validates as `partial` with required-event coverage `1 / 12`.
  It contributes `204818` `entry_rejected` events inside the shared runtime window and remains on the zero-balance observe-only path.
- Mew-X runtime-window package `mewx-pass-20260320T205803Z` validates as `partial` with required-event coverage `9 / 12`.
  It contributes `27` events in the same window, including `candidate_rejected`, `entry_attempt`, `entry_fill`, `entry_signal`, `exit_fill`, `exit_signal`, `mint_observed`, `position_closed`, and `session_update`, but still misses `creator_candidate`, `entry_rejected`, and `run_summary`.

## Output State

- live Dexter package path: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/dexter.validate.json`
- live Mew-X package path: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/mewx.validate.json`
- live comparison output directory: `artifacts/reports/task-005-live-pass-grade-runtime-window-comparison`
- comparison pack JSON: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/comparison-pack.json`
- winner / tie decisions: deferred for candidate sourcing, execution quality, exit quality, and replayability

## Current Narrowed Blocker

- The old `entry_rejected.tx_signature` payload blocker is resolved in Vexter, and the same-window comparison is no longer a `281 ms` overlap artifact.
- The remaining blocker is exact shared-window evidence sufficiency:
  - Dexter still runs on the zero-balance safety path, so the shared window collapses to `entry_rejected` only and never reaches attempt / fill / exit / run-summary coverage.
  - Mew-X is now close to pass grade at `9 / 12`, but it still lacks `creator_candidate`, `entry_rejected`, and graceful `run_summary` evidence in that same matched window.
  - Dexter should stay on `observe_live` unless a formal paper mode is confirmed, and Mew-X should stay on `sim_live` for the next retry.
- `TASK-006` remains blocked until a fuller matched live window produces materially richer overlap coverage.
