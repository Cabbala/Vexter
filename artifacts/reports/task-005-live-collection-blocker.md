# TASK-005 Live Collection Blocker

## Checked Scope

- checked at `2026-03-20T21:19:29Z`
- target host: `win-lan` (`DESKTOP-NNC6MPS`)
- fixed runtime root: `C:\Users\bot\quant\Vexter`
- verified latest start point: `origin/main` commit `1b9ace272d63bcc5be8f30aa1e2a2ab03b63304f`
- verified PR state: PR `#6` merged at `2026-03-21T05:46:44+09:00`
- required result: one Dexter package and one Mew-X package from the same live measurement window, followed by `validate`, `derive-metrics`, and `build-pack`

## What Advanced

- The false `entry_rejected.tx_signature` blocker was removed in Vexter's validator and event schema without changing Dexter or Mew-X logic.
- A safe-mode retry kept both frozen sources concurrently active long enough to resolve the old overlap-only blocker.
- The current best matched runtime window is:
  - concurrent runtime start: `2026-03-20T20:58:40.760Z`
  - concurrent runtime end: `2026-03-20T21:01:52.838Z`
  - concurrent runtime duration: `192.078 s`
  - exact event overlap start: `2026-03-20T20:59:55.254Z`
  - exact event overlap end: `2026-03-20T21:01:52.838Z`
  - exact event overlap duration: `117.584 s`
- The concurrent runtime-window packages were rerun through:
  - `scripts/comparison_analysis.py validate`
  - `scripts/comparison_analysis.py derive-metrics`
  - `scripts/comparison_analysis.py build-pack`

## Current Blocker

- The blocker is no longer missing-window alignment.
- The remaining blocker is exact shared-window evidence sufficiency:
  - Dexter runtime-window package `dexter-pass-20260320T205803Z` validates as `partial` with required-event coverage `1 / 12`
    - observed required types: `entry_rejected`
    - missing required types: `candidate_rejected`, `creator_candidate`, `entry_attempt`, `entry_fill`, `entry_signal`, `exit_fill`, `exit_signal`, `mint_observed`, `position_closed`, `run_summary`, `session_update`
    - total events in the matched runtime window: `204818`
    - the frozen Dexter runtime still ran with `0 SOL`, so the shared window never advanced beyond the observe-only safety path
  - Mew-X runtime-window package `mewx-pass-20260320T205803Z` validates as `partial` with required-event coverage `9 / 12`
    - observed required types: `candidate_rejected`, `entry_attempt`, `entry_fill`, `entry_signal`, `exit_fill`, `exit_signal`, `mint_observed`, `position_closed`, `session_update`
    - missing required types: `creator_candidate`, `entry_rejected`, `run_summary`
    - total events in the matched runtime window: `27`
    - Mew-X sim is now close to pass-grade coverage, but the remaining missing types still block comparable winner decisions
- Runtime safety remains unchanged for the next retry:
  - Dexter should stay on `observe_live` or another zero-balance safety path unless a formal paper mode is explicitly confirmed
  - Mew-X should stay on `sim_live` unless a safer paper-equivalent path is approved

## Result

- live Dexter package: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/dexter.validate.json`
- live Mew-X package: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/mewx.validate.json`
- live comparison output directory: `artifacts/reports/task-005-live-pass-grade-runtime-window-comparison`
- comparison pack JSON: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/comparison-pack.json`
- evidence-backed winners / ties recorded: `none`
- blocker state: `partial_live_comparison_blocker`
- `TASK-006` readiness: `blocked`

## Next Unblock Steps

- collect another matched live pair while preserving the current safety constraints
- keep the frozen strategy / execution / instrumentation code unchanged
- provide Dexter with a confirmed formal paper mode or another approved safe path that can emit attempt / fill / exit / run-summary coverage
- gather a Mew-X run whose shared window includes `creator_candidate`, `entry_rejected`, and `run_summary` evidence
- rerun `scripts/comparison_analysis.py validate`, `derive-metrics`, and `build-pack` on that fuller matched pair after those runs exist
