# TASK-005 Live Comparison Evidence Summary

## Status

- `TASK-005-live-comparison-evidence` remains blocked in `partial_live_comparison_blocker` state on branch `codex/task-005-resume-after-pr8` as of `2026-03-20T22:52:22Z`.
- Start conditions were re-verified from `Cabbala/Vexter` latest `main` commit `d005528a236360b3cb67c78b3a61a6710be410a2`; PR `#8` was confirmed merged at `2026-03-21T07:33:45+09:00`.
- Dexter and Mew-X strategy, execution, and instrumentation logic remain unchanged.
- Sub-agents `Chandrasekhar` and `Tesla` were launched for sidecar inspection while the main thread handled the helper changes, recollection run, and artifact rebuild.

## Fresh Same-Attempt Result

- Vexter-side startup mitigation succeeded without touching frozen source logic:
  - configured Dexter-side quiet/cooldown knobs: `60 s` prestart quiet, `90 s` wsLogs readiness wait, `20 s` wsLogs settle, `5 s` startup delay, `4` max startup attempts, `90 s` retry backoff
  - helper packaging was hardened so the Windows collector can fall back to full-stream copy when exact timestamp filtering is unavailable
  - Windows `ssh` collector setup was hardened to avoid shell-quoting failures during remote package creation
- Fresh same-attempt label: `resume-after-pr8-20260321T0743`
- Observed launch and readiness evidence:
  - `Mew-X` logs created at `2026-03-20T22:42:10Z`; first raw event at `2026-03-20T22:42:23.102Z`
  - `Dexter wsLogs` logs created at `2026-03-20T22:42:23Z`; stderr still captured `6` `HTTP 429` lines before recovery
  - `Dexter` logs created at `2026-03-20T22:42:53Z`; first raw event arrived at `2026-03-20T22:42:56.215162Z`
  - Dexter startup wallet-balance `HTTP 429` attempts on the successful run: `0`
  - Dexter main stderr still captured `1` websocket `HTTP 429` line after startup, but the raw stream stayed live
- Fresh matched measurement window:
  - concurrent runtime start: `2026-03-20T22:42:23.102Z`
  - concurrent runtime end: `2026-03-20T22:44:53.527477Z`
  - concurrent runtime duration: `150.425 s`
  - exact event overlap start: `2026-03-20T22:42:56.215162Z`
  - exact event overlap end: `2026-03-20T22:44:27.240Z`
  - exact event overlap duration: `91.024 s`
- Fresh package outputs:
  - Dexter package dir: `artifacts/tmp/winlan-packages-resume-after-pr8-20260321T0743/dexter-resume-after-pr8-20260321T0743`
  - Mew-X package dir: `artifacts/tmp/winlan-packages-resume-after-pr8-20260321T0743/mewx-resume-after-pr8-20260321T0743`
  - comparison output dir: `artifacts/reports/task-005-live-resume-after-pr8-20260321T0743-comparison`
  - comparison pack JSON: `artifacts/proofs/task-005-live-resume-after-pr8-20260321T0743-results/comparison-pack.json`
- Fresh validation coverage:
  - Dexter: `partial`, `4 / 12` required event types, `107078` total events
  - Mew-X: `partial`, `8 / 12` required event types, `26` total events
- `validate`, `derive-metrics`, and `build-pack` were rerun successfully on the fresh same-attempt pair.

## Baseline Comparison

- Prior best runtime-window baseline remained:
  - label: `pass-20260320T205803Z`
  - Dexter: `1 / 12` required event types
  - Mew-X: `9 / 12` required event types
  - exact overlap duration: `117.584 s`
- Fresh same-attempt comparison versus baseline:
  - Dexter improved from `1 / 12` to `4 / 12`
  - Mew-X moved from `9 / 12` to `8 / 12`
  - same-attempt packaging now exists on latest `main` and is GitHub-visible
  - no comparison area becomes decisively attributable enough yet to unlock TASK-006

## Current Blocker

- `TASK-005` is no longer blocked on `dexter_startup_rate_limit_blocker`; the fresh run cleared Dexter startup far enough to produce a raw NDJSON stream and a packaged same-attempt pair.
- `TASK-005` is now blocked on partial matched-pair coverage:
  - Dexter still lacks `candidate_rejected`, `entry_attempt`, `entry_fill`, `exit_fill`, `exit_signal`, `position_closed`, `run_summary`, and `session_update`
  - Mew-X still lacks `candidate_rejected`, `creator_candidate`, `entry_rejected`, and `run_summary`
  - the fresh Mew-X package still lacks a `session_summary` export pointer
- Winner / tie decisions remain deferred for candidate sourcing, execution quality, exit quality, and replayability.
- `TASK-006` remains blocked until a matched pair supports fuller event coverage and non-deferred comparison decisions.
