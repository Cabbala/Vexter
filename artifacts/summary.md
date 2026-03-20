# TASK-005 Live Comparison Evidence Summary

## Status

- `TASK-005-live-comparison-evidence` remains blocked in `dexter_startup_rate_limit_blocker` state on branch `codex/task-005-resume-after-pr7` as of `2026-03-20T22:17:49Z`.
- Start conditions were re-verified from `Cabbala/Vexter` latest `main` commit `4752182af91c2353491741bf36cf9a82d9655575`; PR `#7` was confirmed merged on `2026-03-21T06:44:14+09:00`.
- Dexter and Mew-X strategy, execution, and instrumentation logic remain unchanged.
- Sub-agent tooling was not exposed in this session, so repo and runtime inspection were completed locally.

## Collection Results

- `scripts/collect_matched_live_pair.py` was hardened without touching frozen source logic:
  - `Mew-X` now prewarms before Dexter startup
  - direct `mew.exe` launch is preferred over `cargo run`
  - the collection window closes after graceful shutdown instead of before it
  - Dexter startup can retry with backoff when the raw stream stays empty
- Historical raw inspection on `win-lan` still proves the last successful Dexter run (`dexter-pass-20260320T205803Z`) contains startup `creator_candidate`, `mint_observed`, and `entry_signal` before the old exact-overlap cutoff, so the prior `1 / 12` window remained partly a collection-timing loss and not just missing Dexter instrumentation.
- Three fresh safe-mode recollection attempts were run after PR `#7`. No new matched pair could be packaged because Dexter never created a fresh raw NDJSON stream.
- The latest fresh `Mew-X` sim retry, `mewx-resume-final-20260321T0714`, produced `41` raw events from `2026-03-20T22:14:55.210Z` to `2026-03-20T22:16:18.740Z` across `9 / 12` required event types:
  - `candidate_rejected`
  - `entry_attempt`
  - `entry_fill`
  - `entry_signal`
  - `exit_fill`
  - `exit_signal`
  - `mint_observed`
  - `position_closed`
  - `session_update`
- Dexter startup failed before its first raw event on every final retry attempt. `Dexter.py` exited with Helius `HTTP 429` during wallet balance fetch across four backoff attempts, while `DexLab/wsLogs.py` recovered from initial websocket `HTTP 429` rejects and resumed observing new mints.
- Because no fresh Dexter raw stream existed, `validate`, `derive-metrics`, and `build-pack` could not be rerun on a new matched pair. The best known matched-window outputs therefore remain the prior `dexter-pass-20260320T205803Z` / `mewx-pass-20260320T205803Z` artifacts.

## Output State

- best known live Dexter package path: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/dexter.validate.json`
- best known live Mew-X package path: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/mewx.validate.json`
- best known live comparison output directory: `artifacts/reports/task-005-live-pass-grade-runtime-window-comparison`
- best known comparison pack JSON: `artifacts/proofs/task-005-live-pass-grade-runtime-window-results/comparison-pack.json`
- new matched live package pair collected in this session: `none`
- winner / tie decisions: deferred for candidate sourcing, execution quality, exit quality, and replayability

## Current Narrowed Blocker

- The old `entry_rejected.tx_signature` payload blocker remains resolved in Vexter, and the old overlap-alignment blocker remains resolved in the last valid matched window.
- The immediate blocker is now `dexter_startup_rate_limit_blocker`, not generic shared-window packaging logic:
  - Dexter must still stay on the zero-balance `observe_live` path, but it now fails before first event because Helius returns `HTTP 429` during wallet balance fetch on startup.
  - `DexLab/wsLogs.py` can recover after initial websocket `HTTP 429`, so the fresh blocker is narrower than a full Windows runtime outage.
  - Fresh `Mew-X` sim evidence improved to `41` events, but it remains unpaired and still lacks `creator_candidate`, `entry_rejected`, and `run_summary`.
- `TASK-006` remains blocked until Dexter can complete a safe startup without `HTTP 429`, a fresh matched pair exists, and `validate`, `derive-metrics`, and `build-pack` can be rerun on that pair.
