# Dexter Instrumentation Plan

## Objective

Add observational instrumentation to Dexter so Vexter can measure candidate quality, entry quality, session dynamics, and exit quality without changing strategy behavior.

## Principles

- do not modify trust logic or exit logic
- emit normalized events beside existing behavior
- preserve local logs and DB writes
- make replay extraction possible from Windows runtime outputs

## Capture Points

1. Leaderboard generation
   - file: `sources/Dexter/DexAI/trust_factor.py`
   - emit:
     - `creator_candidate`
     - leaderboard snapshot metadata
   - capture:
     - creator metrics
     - trust factor
     - performance score
     - trust level projection

2. Mint match and session admission
   - file: `sources/Dexter/Dexter.py`
   - emit:
     - `mint_observed`
     - `entry_signal`
     - `candidate_rejected`
   - capture:
     - matched creator
     - mint and bonding curve
     - skip reason for blacklist, single-lock, or update lock

3. Entry execution
   - files:
     - `sources/Dexter/Dexter.py`
     - `sources/Dexter/DexLab/swaps.py`
   - emit:
     - `entry_attempt`
     - `entry_fill`
     - `entry_rejected`
   - capture:
     - quote price
     - reserved balance
     - available balance
     - retry path
     - tx signature
     - fill latency
     - creator-vault and migration errors

4. Session checkpoints
   - file: `sources/Dexter/Dexter.py`
   - emit:
     - `session_update`
   - capture:
     - current price
     - peak price
     - MFE and MAE
     - composite score
     - buys and sells
     - target ladder step
     - malicious and drop-time flags

5. Exit execution
   - file: `sources/Dexter/Dexter.py`
   - emit:
     - `exit_signal`
     - `exit_fill`
     - `position_closed`
   - capture:
     - exit reason
     - theoretical best price
     - realized price
     - realized return
     - wallet delta

6. Historical replay extraction
   - file: `sources/Dexter/DexLab/market.py`
   - export:
     - raw price history
     - final stagnant rows
     - mint age and slot-delay context

## Windows Output Layout

- runtime config and exporter state:
  - `C:\Users\bot\quant\Vexter\runtime\dexter\config`
  - `C:\Users\bot\quant\Vexter\runtime\dexter\export`
- raw normalized events:
  - `C:\Users\bot\quant\Vexter\data\raw\dexter`
- logs:
  - `C:\Users\bot\quant\Vexter\data\logs\dexter`
- replay material:
  - `C:\Users\bot\quant\Vexter\data\replays\dexter`
- DB exports:
  - `C:\Users\bot\quant\Vexter\data\postgres\dexter`

## Handoff to Next Task

The next Dexter task should implement a lightweight event writer and an extraction command that can export:

- NDJSON event stream
- masked config snapshot
- leaderboard snapshot
- stagnant-mint replay export
