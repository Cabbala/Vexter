# Mew-X Source Assessment

## Executive Read

Mew-X is a Rust bot with a richer candidate engine and a much stronger execution substrate than Dexter. It separates candidate sourcing, runtime config, market subscriptions, execution routing, and database state more cleanly, but it still lacks a normalized event stream that would make profitability claims directly comparable.

## File and Function Map

| Concern | Primary Code Path | Assessment |
| --- | --- | --- |
| Entrypoint and runtime wiring | `sources/Mew-X/src/main.rs` | Wires config, databases, creator selection, subscriptions, and refresh loops |
| Candidate source selection | `sources/Mew-X/src/mew/deagle/deagle.rs` | Combines deagles, volume creators, and optional grand chillers |
| Runtime config and modes | `sources/Mew-X/src/mew/config.rs` | Reads env for transport, mode, risk, concurrency, and strategy knobs |
| Session and execution logic | `sources/Mew-X/src/mew/snipe/handler.rs` | Owns mint state, holdings, session loops, and buy/sell operations |
| Transport abstraction | `sources/Mew-X/src/mew/sol_hook/sol.rs` | Exposes websocket, gRPC, RPC, and SWQOS-friendly send paths |
| State databases | `sources/Mew-X/src/mew/sol_hook/goldmine.rs`, `sources/Mew-X/src/mew/sol_hook/vacation.rs` | Separate analytics state from region-awareness state |

## Candidate Source Selection

Candidate generation starts in `main.rs`:

1. `config::get_algo_config()` builds an `AlgoConfig`.
2. `Deagle::algo_choose_creators()` assembles creators from:
   - `Source::VolCreators`
   - `Source::Deagle`
   - optional `Source::GrandChillers`
3. `refresh_creators_loop()` refreshes the candidate set every 60 seconds.
4. `subscribe_*_pump_fun()` matches incoming creates against the current creator list.

This is structurally different from Dexter:

- Dexter creates candidates from historical creator quality only.
- Mew-X combines creator cohorts and can attach explicit source labels.

For Vexter, that means Mew-X must export source label, creator cohort, and refresh diffs as first-class evaluation data.

## Config and Runtime Modes

`config.rs` exposes the runtime controls that matter for comparability:

- transport and connectivity:
  - `RPC_URL`
  - `WS_URL`
  - `GRPC_URL`
  - `GRPC_TOKEN`
  - `USE_GRPC`
- runtime mode:
  - `MODE` (`sim` or `trade`)
  - `MAX_TOKENS_AT_ONCE`
  - `USE_REGIONS`
- snipe controls:
  - buy amount
  - slippage
  - loss and take-profit
  - creator-hold-percent gates
  - txns-in-zero gates
  - inactivity timers
- strategy toggles:
  - ABS
  - dip / MTD
  - DBF

Important consequence: a run summary must capture the config snapshot, because Mew-X behavior can change materially through environment toggles without code changes.

## Transport, Execution, and Route Abstraction

Mew-X has a much richer send path than Dexter:

- `SolHook::subscribe_logs_channel()` and `grpc_subscribe_transactions()` provide WS or Yellowstone gRPC intake.
- `MewSnipe::buy()` can route through:
  - plain RPC send
  - `spray_with_all()` for SWQOS-style multi-endpoint submission
- `MewSnipe::sell()` retries failed sends.
- Market abstraction spans both Pump.fun and PumpSwap.

This is a major comparative advantage, but it also means execution quality cannot be judged without route-level telemetry. Vexter needs per-attempt capture of:

- transport mode
- route family
- fee settings
- signatures
- retry count
- fill latency

## Position and Session Handling

State separation is explicit:

- `holdings` is a `DashMap` keyed by mint and enforces one session per mint.
- `mints` is an `RwLock<HashMap<Pubkey, MewMint>>` containing live market state.
- `start_session()` applies region gating and concurrency gating before spawning a detached task.
- `sim_session()` and `trade_session()` share near-identical profit, inactivity, and creator-sold exit logic.
- `dip_session()` watches migrated PumpSwap pools for later re-entry opportunities.

Main session risk controls:

- `MAX_TOKENS_AT_ONCE`
- regional leader gating through `Vacation`
- creator hold percent checks
- txns-in-zero checks
- loss and take-profit thresholds
- inactivity windows
- creator-sold trigger

## Risk Gates and Notable Edge Cases

What is already strong:

- explicit concurrency cap
- explicit region gating
- buy and sell routing abstraction
- source-aware session starts
- persisted sim snapshots

What remains risky for analysis:

- no normalized record of why a session was rejected
- no structured event for creator refresh diffs
- no explicit distinction between signal time and execution-attempt time
- no full route-attempt log for SWQOS fanout

Two code-level risks should stay visible in the assessment:

- `trade_session()` computes the target market, but the buy call is still hard-coded to `Market::PumpFun`, which may under-measure migrated entry behavior.
- Several CHP and TIZ log messages describe an out-of-range rejection while the predicates read like in-range checks. Instrumentation must capture both raw values and gate outcomes so the real intent is measurable.

## DB and State Separation

Mew-X already separates state into focused stores:

- `Vacation` database:
  - validator location cache for region-aware gating
- `Goldmine` database:
  - `tokens`
  - `dupes`
  - `deagle`
  - `blacklist`
  - `twitters`
  - `sims`
- in-memory runtime state:
  - `mints`
  - `holdings`

This is cleaner than Dexter's split, but replay is still incomplete because `sims` stores the latest snapshot for a mint rather than an event stream of every decision.

## Observability Required Next

Mew-X should emit the following instrumentation before it is compared head-to-head:

- creator refresh snapshot with source labels and diffs
- create-event match and duplicate-reject events
- session gate reject reason with values for concurrency, region, CHP, and TIZ
- entry signal timestamp separate from execution attempt timestamp
- route-level entry attempt telemetry including tx strategy and fee settings
- fill confirmation with signature, latency, and venue
- session checkpoint updates for MFE, MAE, creator behavior, and inactivity windows
- exit signal and exit fill with realized-versus-theoretical gap
- dip-session trigger events for migrated pools

## Assessment Verdict

Mew-X is the stronger candidate-engine and execution-substrate repo, but it still needs normalized instrumentation before its edge can be trusted against Dexter. Its most promising reusable components today are source-labeled candidate generation and the transport abstraction. Its main readiness gap is not capability; it is missing analysis-grade attribution.
