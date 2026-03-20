# TASK-005 Live Collection Blocker

## Checked Scope

- checked at `2026-03-20T22:17:49Z`
- target host: `win-lan` (`DESKTOP-NNC6MPS`)
- fixed runtime root: `C:\Users\bot\quant\Vexter`
- verified latest start point: `origin/main` commit `4752182af91c2353491741bf36cf9a82d9655575`
- verified PR state: PR `#7` merged at `2026-03-21T06:44:14+09:00`
- required result: one Dexter package and one Mew-X package from the same live measurement window, followed by `validate`, `derive-metrics`, and `build-pack`

## What Advanced

- The false `entry_rejected.tx_signature` blocker remains removed in Vexter's validator and event schema without changing Dexter or Mew-X logic.
- The matched-pair helper now:
  - prewarms `Mew-X` before launching Dexter
  - prefers `mew.exe` over `cargo run`
  - records the measurement end after graceful shutdown
  - retries Dexter startup with backoff when the raw stream stays empty
- The best already-proven matched runtime window is still:
  - concurrent runtime start: `2026-03-20T20:58:40.760Z`
  - concurrent runtime end: `2026-03-20T21:01:52.838Z`
  - concurrent runtime duration: `192.078 s`
  - exact event overlap start: `2026-03-20T20:59:55.254Z`
  - exact event overlap end: `2026-03-20T21:01:52.838Z`
  - exact event overlap duration: `117.584 s`
- The prior concurrent runtime-window packages remain the last pair rerun through:
  - `scripts/comparison_analysis.py validate`
  - `scripts/comparison_analysis.py derive-metrics`
  - `scripts/comparison_analysis.py build-pack`
- Three fresh safe-mode retries were attempted after PR `#7`.
- The latest fresh `Mew-X` sim run, `mewx-resume-final-20260321T0714`, produced `41` raw events from `2026-03-20T22:14:55.210Z` to `2026-03-20T22:16:18.740Z` with event counts:
  - `candidate_rejected`: `1`
  - `entry_attempt`: `4`
  - `entry_fill`: `4`
  - `entry_signal`: `4`
  - `exit_fill`: `4`
  - `exit_signal`: `4`
  - `mint_observed`: `6`
  - `position_closed`: `4`
  - `session_update`: `10`

## Current Blocker

- The blocker is no longer generic window alignment.
- The immediate blocker is fresh Dexter startup under current Helius limits:
  - `Dexter.py` exited before its first raw event on every final retry attempt:
    - `dexter-resume-final-20260321T0714`
    - `dexter_retry_2-resume-final-20260321T0714`
    - `dexter_retry_3-resume-final-20260321T0714`
    - `dexter_retry_4-resume-final-20260321T0714`
  - repeated failure: `HTTP 429: {"jsonrpc":"2.0","error":{"code":-32429,"message":"rate limited"}}`
  - failed call site: wallet balance fetch during zero-balance `observe_live` startup
  - fresh Dexter raw NDJSON path created: `none`
- `DexLab/wsLogs.py` also saw initial websocket `HTTP 429`, but unlike `Dexter.py` it later re-subscribed, observed new mints, and kept running.
- Fresh `Mew-X` sim evidence improved materially, but it remains unpaired because no same-attempt Dexter raw stream exists.
- The older exact shared-window evidence blocker is still unresolved in the last valid pair:
  - prior Dexter runtime-window package `dexter-pass-20260320T205803Z` remains `partial` at `1 / 12`
  - prior Mew-X runtime-window package `mewx-pass-20260320T205803Z` remains `partial` at `9 / 12`
- Runtime safety remains unchanged for the next retry:
  - Dexter should stay on `observe_live` or another zero-balance safety path unless a formal paper mode is explicitly confirmed
  - Mew-X should stay on `sim_live` unless a safer paper-equivalent path is approved

## Result

- latest fresh Dexter package: `none`
- latest fresh Mew-X raw event file: `C:\Users\bot\quant\Vexter\data\raw\mewx\mewx-resume-final-20260321T0714.ndjson`
- prior best Dexter package: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/dexter.validate.json`
- prior best Mew-X package: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/mewx.validate.json`
- prior comparison output directory: `artifacts/reports/task-005-live-pass-grade-runtime-window-comparison`
- prior comparison pack JSON: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/comparison-pack.json`
- evidence-backed winners / ties recorded: `none`
- blocker state: `dexter_startup_rate_limit_blocker`
- `TASK-006` readiness: `blocked`

## Next Unblock Steps

- collect another matched live pair while preserving the current safety constraints
- keep the frozen strategy / execution / instrumentation code unchanged
- remove or wait out the current Dexter-side Helius `HTTP 429` rate limit so `observe_live` startup can complete its wallet balance fetch and create a raw NDJSON stream
- keep `Mew-X` on `sim_live` and reuse the hardened prewarm / graceful-stop helper for the next retry
- rerun `scripts/comparison_analysis.py validate`, `derive-metrics`, and `build-pack` only after a same-attempt Dexter raw package and Mew-X raw package both exist
