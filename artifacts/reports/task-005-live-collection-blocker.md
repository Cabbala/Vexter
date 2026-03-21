# TASK-005 Live Collection Blocker

## Checked Scope

- checked at `2026-03-20T22:52:22Z`
- target host: `win-lan` (`DESKTOP-NNC6MPS`)
- fixed runtime root: `C:\Users\bot\quant\Vexter`
- verified latest start point: `origin/main` commit `d005528a236360b3cb67c78b3a61a6710be410a2`
- verified PR state: PR `#8` merged at `2026-03-21T07:33:45+09:00`
- required result: one fresh Dexter package and one fresh Mew-X package from the same attempt, followed by `validate`, `derive-metrics`, and `build-pack`

## What Advanced

- The immediate `dexter_startup_rate_limit_blocker` was mitigated on a fresh PR `#8` recollection run using Vexter-side controls only:
  - configured `60 s` Dexter prestart quiet
  - configured `90 s` wsLogs readiness wait
  - configured `20 s` wsLogs settle window
  - configured `5 s` startup delay before Dexter main
  - configured `4` max startup attempts with `90 s` retry backoff
- The matched-pair helper now also records structured startup timing / `HTTP 429` evidence, hardens Windows collector setup over `ssh`, and can package full event streams when timestamp-window filtering is unavailable.
- Fresh same-attempt label: `resume-after-pr8-20260321T0743`
- Observed startup timing from Windows log creation / first raw-event evidence:
  - `Mew-X` logs created at `2026-03-20T22:42:10Z`
  - `Mew-X` first raw event at `2026-03-20T22:42:23.102Z`
  - `Dexter wsLogs` logs created at `2026-03-20T22:42:23Z`
  - `Dexter` logs created at `2026-03-20T22:42:53Z`
  - `Dexter` first raw event at `2026-03-20T22:42:56.215162Z`
- `Dexter` startup wallet-balance `HTTP 429` attempts on the successful run: `0`
- `Dexter wsLogs` stderr still contained `6` `HTTP 429` lines before recovery, and `Dexter` main stderr still contained `1` websocket `HTTP 429` line after startup, but both no longer prevented raw-package formation.

## Fresh Same-Attempt Outputs

- Fresh matched measurement window:
  - concurrent runtime start: `2026-03-20T22:42:23.102Z`
  - concurrent runtime end: `2026-03-20T22:44:53.527477Z`
  - concurrent runtime duration: `150.425 s`
  - exact event overlap start: `2026-03-20T22:42:56.215162Z`
  - exact event overlap end: `2026-03-20T22:44:27.240Z`
  - exact event overlap duration: `91.024 s`
- Fresh package paths:
  - Dexter package dir: `artifacts/tmp/winlan-packages-resume-after-pr8-20260321T0743/dexter-resume-after-pr8-20260321T0743`
  - Mew-X package dir: `artifacts/tmp/winlan-packages-resume-after-pr8-20260321T0743/mewx-resume-after-pr8-20260321T0743`
  - Dexter validation JSON: `artifacts/proofs/task-005-live-resume-after-pr8-20260321T0743-results/dexter.validate.json`
  - Mew-X validation JSON: `artifacts/proofs/task-005-live-resume-after-pr8-20260321T0743-results/mewx.validate.json`
  - fresh comparison output dir: `artifacts/reports/task-005-live-resume-after-pr8-20260321T0743-comparison`
  - fresh comparison pack JSON: `artifacts/proofs/task-005-live-resume-after-pr8-20260321T0743-results/comparison-pack.json`
- Fresh validation results:
  - Dexter: `partial`, `4 / 12` required event types, `107078` total events
    - observed: `creator_candidate`, `entry_rejected`, `entry_signal`, `mint_observed`
  - Mew-X: `partial`, `8 / 12` required event types, `26` total events
    - observed: `entry_attempt`, `entry_fill`, `entry_signal`, `exit_fill`, `exit_signal`, `mint_observed`, `position_closed`, `session_update`

## Baseline Comparison

- Prior baseline remained:
  - label: `pass-20260320T205803Z`
  - Dexter validation: `partial`, `1 / 12`
  - Mew-X validation: `partial`, `9 / 12`
  - comparison output dir: `artifacts/reports/task-005-live-pass-grade-runtime-window-comparison`
- Fresh same-attempt pair versus prior baseline:
  - Dexter improved from `1 / 12` to `4 / 12`
  - Mew-X moved from `9 / 12` to `8 / 12`
  - same-attempt packaging on latest `main` now exists and was rebuilt through `validate`, `derive-metrics`, and `build-pack`
  - comparison winners / ties still remain deferred

## Current Blocker

- The task is no longer blocked by fresh Dexter startup wallet-balance `HTTP 429`.
- The current blocker is now partial matched-pair coverage on the fresh same-attempt package:
  - Dexter still lacks `candidate_rejected`, `entry_attempt`, `entry_fill`, `exit_fill`, `exit_signal`, `position_closed`, `run_summary`, and `session_update`
  - Mew-X still lacks `candidate_rejected`, `creator_candidate`, `entry_rejected`, and `run_summary`
  - the fresh Mew-X package still lacks a `session_summary` export pointer in `run_metadata.json`
- Because the fresh pair remains partial, no comparison area becomes decisive enough to advance replay validation or TASK-006.

## Result

- latest fresh Dexter package: `artifacts/proofs/task-005-live-resume-after-pr8-20260321T0743-results/dexter.validate.json`
- latest fresh Mew-X package: `artifacts/proofs/task-005-live-resume-after-pr8-20260321T0743-results/mewx.validate.json`
- latest fresh comparison output: `artifacts/reports/task-005-live-resume-after-pr8-20260321T0743-comparison`
- winner / tie decisions: deferred
- blocker state: `partial_live_comparison_blocker`
- `TASK-006` readiness: `blocked`
