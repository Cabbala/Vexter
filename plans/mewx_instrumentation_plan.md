# Mew-X Instrumentation Plan

## Objective

Instrument Mew-X so Vexter can compare candidate sourcing, transport quality, session quality, and exit quality against Dexter with the same contract.

## Principles

- keep candidate logic observational
- keep WS and gRPC paths behaviorally identical
- record route-level execution decisions
- preserve separation between Goldmine, Vacation, and runtime state

## Capture Points

1. Candidate sourcing
   - files:
     - `sources/Mew-X/src/main.rs`
     - `sources/Mew-X/src/mew/deagle/deagle.rs`
   - emit:
     - `creator_candidate`
   - capture:
     - candidate source label
     - ranking inputs
     - creator counts per source
     - refresh diffs

2. Mint observation and session admission
   - file: `sources/Mew-X/src/mew/snipe/handler.rs`
   - emit:
     - `mint_observed`
     - `entry_signal`
     - `candidate_rejected`
   - capture:
     - create event metadata
     - duplicate detection result
     - region gate result
     - concurrency cap result
     - source label

3. Entry execution
   - files:
     - `sources/Mew-X/src/mew/snipe/handler.rs`
     - `sources/Mew-X/src/mew/sol_hook/sol.rs`
   - emit:
     - `entry_attempt`
     - `entry_fill`
     - `entry_rejected`
   - capture:
     - tx strategy
     - transport path
     - route family
     - fee and tip settings
     - retries
     - signature and fill latency

4. Session checkpoints
   - file: `sources/Mew-X/src/mew/snipe/handler.rs`
   - emit:
     - `session_update`
   - capture:
     - current price
     - highest price
     - creator hold state
     - txns in zero and txns in n
     - MFE and MAE
     - inactivity timer status

5. Exit execution
   - file: `sources/Mew-X/src/mew/snipe/handler.rs`
   - emit:
     - `exit_signal`
     - `exit_fill`
     - `position_closed`
   - capture:
     - exit reason
     - realized price
     - theoretical peak
     - realized-versus-peak gap

6. Dip and migration tracking
   - file: `sources/Mew-X/src/mew/snipe/handler.rs`
   - emit:
     - `mint_observed`
     - `session_update`
   - capture:
     - migration detection
     - dip trigger
     - re-entry start conditions

## Windows Output Layout

- runtime config and exporter state:
  - `C:\Users\bot\quant\Vexter\runtime\mewx\config`
  - `C:\Users\bot\quant\Vexter\runtime\mewx\export`
- raw normalized events:
  - `C:\Users\bot\quant\Vexter\data\raw\mewx`
- logs:
  - `C:\Users\bot\quant\Vexter\data\logs\mewx`
- replay material:
  - `C:\Users\bot\quant\Vexter\data\replays\mewx`
- DB exports:
  - `C:\Users\bot\quant\Vexter\data\postgres\mewx`

## Handoff to Next Task

The next Mew-X task should implement:

- a normalized event writer shared by WS and gRPC handlers
- route-attempt telemetry for RPC and SWQOS sends
- periodic export of candidate refresh snapshots and sim summaries
