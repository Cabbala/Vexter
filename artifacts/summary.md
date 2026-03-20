# TASK-005 Live Comparison Evidence Summary

## Status

- `TASK-005-live-comparison-evidence` is now in `subsecond_overlap_partial_blocker` state on branch `codex/task-005-resume-matched-window` as of `2026-03-20T20:30:28Z`.
- Start conditions were re-verified from `Cabbala/Vexter` latest `main` commit `9d7190ef3590ee80592115c73ff1bcec10cb1475`; PR `#5` was confirmed merged on `2026-03-20T20:08:22Z`.
- Dexter and Mew-X strategy, execution, and instrumentation logic remain unchanged.
- Sub-agents were launched for parallel GitHub / runbook inspection while the main thread handled Windows collection retries and evidence closeout.

## Collection Results

- A first resume retry surfaced a transient Dexter startup instability on `win-lan`: Helius returned `HTTP 429` during wallet-balance fetch before live events started.
- A second Dexter retry succeeded on run `dexter-window-20260320T202100Z` and emitted `157023` live events from `2026-03-20T20:21:09.930245Z` to `2026-03-20T20:23:51.718358Z`.
  Dexter stayed zero-balance observe-only throughout that run: `creator_candidate=57`, `mint_observed=1`, `entry_signal=1`, `entry_rejected=156964`, with no fill / exit / run-summary coverage.
- The latest usable Mew-X live run was `mewx-desktop-nnc6mps-20260320T201918Z`, which emitted `11` live events from `2026-03-20T20:20:09.062Z` to `2026-03-20T20:21:10.211Z`.
  Its full-run event mix was `mint_observed=4`, `entry_signal=2`, `entry_attempt=2`, `entry_rejected=2`, `candidate_rejected=1`.
- The exact shared live slice between those runs was `2026-03-20T20:21:09.930245Z` -> `2026-03-20T20:21:10.211Z`, a `281 ms` overlap.
- Exact-overlap packages were built from that shared slice and rerun through `validate`, `derive-metrics`, and `build-pack`.
- Dexter overlap package `dexter-window-20260320T202100Z` validated as `partial` with required-event coverage `1 / 12`; only `creator_candidate` was observed inside the shared slice.
- Mew-X overlap package `mewx-desktop-nnc6mps-20260320T201918Z` validated as `partial` with required-event coverage `1 / 12`; only `entry_rejected` was observed inside the shared slice, and that payload still omitted `tx_signature`.

## Output State

- live Dexter package path: `artifacts/proofs/task-005-live-overlap-results/dexter.validate.json`
- live Mew-X package path: `artifacts/proofs/task-005-live-overlap-results/mewx.validate.json`
- live comparison output directory: `artifacts/reports/task-005-live-overlap-comparison`
- comparison pack JSON: `artifacts/proofs/task-005-live-overlap-results/comparison-pack.json`
- winner / tie decisions: deferred for candidate sourcing, execution quality, exit quality, and replayability

## Current Narrowed Blocker

- The old `not from the same live measurement window` blocker is resolved only at overlap level: a shared live slice now exists.
- The remaining blocker is evidence sufficiency:
  - the shared slice is only `281 ms`, so it is not a fair comparable live window
  - Dexter still ran with `0 SOL`, so the overlap package never advanced beyond `creator_candidate`
  - Mew-X contributed only one overlapping `entry_rejected` event, and that payload still lacks `tx_signature`
- `TASK-006` remains blocked until a fuller matched live window produces materially richer overlap coverage.
