# Dexter Source Assessment

## Executive Read

Dexter is a creator-score-first Python bot with two distinct operating surfaces:

- a historical ingestion path that stores mint and swap evolution into PostgreSQL
- a live session engine that watches matching creators and runs an adaptive exit ladder in memory

This split is useful for analysis because the database already preserves a replay seed, but the live path does not yet emit enough structured evidence to prove why entries and exits happened.

## File and Function Map

| Concern | Primary Code Path | Assessment |
| --- | --- | --- |
| DB bootstrap and schema | `sources/Dexter/database.py` | Defines `mints` and `stagnant_mints`, both required by downstream analysis |
| Creator scoring | `sources/Dexter/DexAI/trust_factor.py` | Builds leaderboard from `stagnant_mints` and filters creators with a trust-factor heuristic |
| Live runtime | `sources/Dexter/Dexter.py` | Subscribes to Pump.fun logs, matches creators, and manages sessions |
| Historical ingestion | `sources/Dexter/DexLab/wsLogs.py`, `sources/Dexter/DexLab/market.py` | Parses websocket logs and persists mint state into Postgres |
| Trade verification | `sources/Dexter/DexLab/swaps.py` | Confirms buy and sell transactions and extracts post-trade price and balances |
| Strategy configuration | `sources/Dexter/settings.py` | Freezes trust thresholds, buy sizes, and exit ladder controls |

## Entry Candidate Flow

1. `DexLab/market.py` stores closed or stagnant mint histories in `stagnant_mints`.
2. `DexAI/trust_factor.py` loads `stagnant_mints`, groups rows by creator, and computes aggregate statistics such as:
   - mint count
   - median peak market cap
   - total swaps
   - trust factor
   - median success ratio
3. `Analyzer.process_results()` turns the surviving creators into a leaderboard keyed by owner.
4. `Dexter.update_leaderboard()` refreshes that leaderboard on a timer.
5. `Dexter.process_data("mints", ...)` receives fresh mint-creation events. If the creator exists in the leaderboard, it starts `monitor_mint_session()` for that mint.

Key implication: candidate generation is creator-centric, not mint-centric. Profitability evaluation therefore needs both creator score quality and creator-to-new-mint conversion quality.

## Creator Scoring and Trust Logic

The trust logic lives in `DexAI/trust_factor.py` and is based on historical stalled mints:

- `_is_successful_mint()` checks whether the peak price exceeded the sniping price by a configurable ratio and whether the peak was reached after enough swaps.
- `analyze_top_creators_sync()` aggregates mint histories per creator.
- `process_results()` filters creators by:
  - minimum median peak market cap
  - minimum total swaps
  - minimum trust factor
  - creation-delay sanity checks
- `Dexter.set_trust_level()` then compresses a creator into trust level 1 or 2 for sizing.

Important consequence: the final buy amount is decided by a much smaller trust-level abstraction than the upstream leaderboard score. Instrumentation must therefore capture both the raw creator metrics and the trust-level compression used at decision time.

## Market Data Ingestion Path

Dexter has two near-parallel ingestion paths:

- Historical path:
  - `DexLab/wsLogs.py` subscribes to websocket logs.
  - `collect()` and `validate()` decode Pump.fun logs.
  - `Market.populate_market()` writes mint and swap state into Postgres.
  - `Market.monitor_single_mint()` moves inactive mints from `mints` to `stagnant_mints`.
- Live path:
  - `Dexter.subscribe()` receives websocket logs directly.
  - `handle_single_log()` and `process_data()` build the in-memory `swap_folder`.
  - `monitor_mint_session()` reads that in-memory state for trading decisions.

Key implication: live sessions do not directly consume the historical DB. Vexter should treat these as separate observability surfaces and instrument both.

## Session Lifecycle

`monitor_mint_session()` is the core live decision loop.

Session start gates:

- creator is not blacklisted
- `SINGLE_LOCK` is not blocking
- leaderboard update is not in progress

Once a session starts:

1. Trust level and profit range are derived from leaderboard data.
2. `buy()` is called until a buy is confirmed or a hard stop occurs.
3. Buy confirmation is inferred from holder balances in the local mint state, with fallback to `get_swap_tx()` if needed.
4. The loop updates peak price, composite score, buy/sell counts, and creator behavior.
5. Exit targets are adjusted through a step ladder derived from creator median success ratio and `PROFIT_MARGIN`.
6. The session closes on an exit condition or stagnation condition.

## Exit Ladder, Reserved Balance, and Risk Gates

Dexter contains explicit balance reservation logic:

- `_reserve_buy_spend()`
- `_release_buy_spend()`
- `_finalize_buy_spend()`

This is valuable for portfolio analysis because it models pending capital before fills settle.

Main exit and risk gates:

- insufficient available wallet balance
- `PriceTooHigh`
- `zero_quote`
- `creator_vault_unavailable`
- bonding-curve migration
- `sells > buys` degradation
- malicious drawdown heuristic
- `DROP_TIME` inactivity
- hard stagnancy windows

Adaptive exit behavior:

- increment ladder is built from `median_success_ratio`
- composite score controls whether the target can ratchet upward
- malicious or drop-time conditions force the ladder back to the lowest step

Profitability evaluation must therefore capture both the theoretical best exit and the actually realized ladder step.

## DB Schema and Replay Feasibility

Replay-relevant persisted data already exists:

- `mints`
- `stagnant_mints`
- `price_history`
- `tx_counts`
- `volume`
- `holders`
- `final_ohlc`
- `slot_delay`

Strengths:

- creator history is already queryable
- mint evolution is stored at sub-second timestamps
- final stagnant rows are enough to reproduce the leaderboard logic

Current replay gaps:

- no normalized event for candidate admission
- no structured entry signal timestamp
- no explicit quote price versus fill price record
- no structured exit reason stream
- no session checkpoint export beyond logs and `dev/results.txt`

Current state: replayable for historical creator scoring, only partially replayable for live profitability attribution.

## Observability Required Next

Dexter should emit the following instrumentation points before profitability claims are trusted:

- leaderboard refresh snapshot with creator metrics and trust level
- mint match event when a fresh mint maps to a leaderboard creator
- session start or skip event with the exact gate reason
- entry signal, quote, and actual submission timing
- buy confirmation path used: holder-detected versus RPC fallback
- reserved balance before and after each attempt
- session checkpoint snapshots for MFE, MAE, composite score, and target step
- exit signal with reason and theoretical peak context
- exit fill with realized price, realized return, and wallet impact

## Assessment Verdict

Dexter already has enough structure to support profitability analysis first, but only after instrumentation fills the live decision gaps. Its strongest reusable component today is the creator-score pipeline plus the adaptive exit ladder. Its weakest point for fair comparison is the missing structured event trail between session start and realized exit.
