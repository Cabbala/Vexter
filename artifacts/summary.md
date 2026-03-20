# TASK-005 Live Comparison Evidence Summary

## Status

- `TASK-005-live-comparison-evidence` is now in `partial_live_comparison_blocker` state on branch `codex/task-005-live-comparison-evidence` as of `2026-03-20T19:46:59Z`.
- Start conditions were re-verified from `Cabbala/Vexter` `main` at commit `939642e6d185629f23a04e8e04f9fc7eac62ebc9` and open PR `#5`.
- Dexter and Mew-X strategy, execution, and instrumentation logic remain unchanged.
- The Windows repo-root `.env` blocker was cleared on `win-lan`: Dexter values were unquoted, Mew-X now uses explicit `RPC_URL`, a valid base58 signer, a working `DB_URL`, and parser-safe env formatting.
- Live smoke packages were collected from `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs` and revalidated on the Mac control plane with the Vexter comparison tooling.
- `validate`, `derive-metrics`, and `build-pack` now run end-to-end, but both packages still validate as `partial`, so winner / tie calls remain deferred and `TASK-006` stays blocked.

## Collection Results

- Dexter smoke run `dexter-smoke-20260320T193452Z` emitted raw NDJSON, config, leaderboard export, and replay evidence after seeding `stagnant_mints` via `DexLab\wsLogs.py`.
- Dexter package validation remains `partial`: observed required event coverage is `4 / 12`, and the frozen runtime emitted `43741` `entry_rejected` payloads without `tx_signature`, while no live fill / exit / run-summary events were captured under the zero-balance safety signer.
- Mew-X smoke run `mewx-smoke-20260320T193850Z` emitted raw NDJSON, config, candidate snapshots, state export, and session summary after the parser-safe `REGIONS` fix.
- Mew-X package validation remains `partial`: observed required event coverage is `8 / 12`; missing required event types are `creator_candidate`, `candidate_rejected`, `entry_rejected`, and `run_summary`.
- Cross-platform package handling was tightened in this repo so Windows-authored package paths now validate cleanly on Mac, and the collector now points Dexter replay and Mew-X session-summary exports at concrete files.

## Output State

- live Dexter package path: `artifacts/proofs/task-005-live-smoke-results/dexter.validate.json`
- live Mew-X package path: `artifacts/proofs/task-005-live-smoke-results/mewx.validate.json`
- live comparison output directory: `artifacts/reports/task-005-live-smoke-comparison`
- comparison pack JSON: `artifacts/proofs/task-005-live-smoke-results/comparison-pack.json`
- winner / tie decisions: deferred for candidate sourcing, execution quality, exit quality, and replayability pending a matched comparable live window

## Current Narrowed Blocker

- The exact signer / RPC env blocker is resolved.
- The remaining blocker is evidence quality, not startup: current smoke packages are not a matched comparable pair from the same live window and both remain `partial`.
- Dexter's safe observe-only run proved env/network recovery, but it did not produce `entry_attempt`, `entry_fill`, `exit_signal`, `exit_fill`, `position_closed`, `run_summary`, or `session_update` coverage needed for a comparable pass package.
- Mew-X now reaches full `sim_live` session closure, but this smoke run was collected from a later non-matched window and still lacks `creator_candidate`, `candidate_rejected`, `entry_rejected`, and `run_summary`.
