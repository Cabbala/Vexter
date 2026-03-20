# TASK-005 Live Collection Blocker

## Checked Scope

- checked at `2026-03-20T19:46:59Z`
- target host: `win-lan` (`DESKTOP-NNC6MPS`)
- fixed runtime root: `C:\Users\bot\quant\Vexter`
- verified start point: `origin/main` commit `939642e6d185629f23a04e8e04f9fc7eac62ebc9` and open PR `#5`
- required result: one Dexter package and one Mew-X package from the same live measurement window, followed by `validate`, `derive-metrics`, and `build-pack`

## What Advanced

- Dexter `.env` is now parser-safe on `win-lan`: `PRIVATE_KEY`, `HTTP_URL`, and `WS_URL` are unquoted and load cleanly.
- Mew-X `.env` is now parser-safe on `win-lan`: `RPC_URL` / `WS_URL` are clean ASCII endpoints, `DB_URL` resolves to `postgres://postgres:admin123@127.0.0.1:5432`, the explicit signer is valid base58, and `REGIONS` was rewritten to a space-free form so dotenv stops truncating the later `ALGO_*` values.
- A safe Dexter smoke path was recovered without touching frozen source logic:
  - `DexLab\wsLogs.py` repopulated `stagnant_mints`
  - `Dexter.py` emitted raw NDJSON, config, leaderboard export, and replay artifacts under the fixed Vexter root
- A safe Mew-X smoke path was recovered without touching frozen source logic:
  - `cargo run --quiet` with `MODE=sim` emitted raw NDJSON, config, candidate snapshots, state export, and a session summary under the fixed Vexter root
- Windows collector output and Mac validator input are now cross-platform compatible from this repo: relative package paths are normalized and required replay / session-summary pointers resolve correctly.
- Smoke packages were collected, transferred to the Mac control plane, validated, metricized, and assembled into a comparison pack.

## Current Blocker

- The blocker is no longer exact signer startup failure.
- The remaining blocker is evidence quality: the available smoke packages are `partial` and not a matched comparable pair from the same live measurement window.
- Dexter package `dexter-smoke-20260320T193452Z` validates as `partial` with required-event coverage `4 / 12`.
  - Observed required types: `creator_candidate`, `mint_observed`, `entry_signal`, `entry_rejected`
  - Missing required types: `candidate_rejected`, `entry_attempt`, `entry_fill`, `exit_signal`, `exit_fill`, `position_closed`, `run_summary`, `session_update`
  - The frozen Dexter runtime emitted `43741` `entry_rejected` events without `tx_signature`, and the zero-balance safety signer never advanced to fill / exit coverage.
- Mew-X package `mewx-smoke-20260320T193850Z` validates as `partial` with required-event coverage `8 / 12`.
  - Observed required types: `mint_observed`, `entry_signal`, `entry_attempt`, `entry_fill`, `session_update`, `exit_signal`, `exit_fill`, `position_closed`
  - Missing required types: `creator_candidate`, `candidate_rejected`, `entry_rejected`, `run_summary`
  - This smoke run reached a complete `sim_live` session closeout, but it was collected from a later non-matched window.

## Result

- live Dexter package: `artifacts/proofs/task-005-live-smoke-results/dexter.validate.json`
- live Mew-X package: `artifacts/proofs/task-005-live-smoke-results/mewx.validate.json`
- live comparison output directory: `artifacts/reports/task-005-live-smoke-comparison`
- evidence-backed winners / ties recorded: `none`
- blocker state: `partial_live_comparison_blocker`
- `TASK-006` readiness: `blocked`

## Next Unblock Steps

- collect one Dexter run and one Mew-X run from the same measurement window
- keep the frozen strategy / execution / instrumentation code unchanged
- gather a Dexter run that reaches comparable execution coverage rather than observe-only rejection coverage
- gather a Mew-X run from that same shared window so `validate` can move both packages beyond `partial`
- rerun `scripts/comparison_analysis.py validate`, `derive-metrics`, and `build-pack` on the matched package pair after those fuller runs exist
