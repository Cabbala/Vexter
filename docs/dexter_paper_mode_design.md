# Dexter Minimal Paper-Mode / Paper-Equivalent Design

## Scope And Baseline

This memo answers `DEXTER-PAPER-DESIGN` only. It does not implement the mode yet, does not change Dexter or Mew-X strategy semantics, and does not start `TASK-006`.

The design baseline is:

- `Cabbala/Vexter` latest `origin/main` at `0d4ff2e160feecd4313f0d8ff95d2ff084c5a7ee` (PR `#11`, merged on `2026-03-21`)
- promoted `TASK-005` same-attempt pair `resume-after-pr9-20260321T1737`
- Dexter validation on that pair: `4 / 12`
- Mew-X validation on that pair: `8 / 12`
- current blocker assumption: Dexter coverage stall under safe modes, not another repeated retry loop

To stay source-faithful, the code inspection below uses the source commits pinned by Vexter, not the newer ignored `sources/` checkouts that had already advanced to upstream `main`:

- Dexter pinned commit: `69de8b6ca57ca3d03025d85329c88aa4a167da34`
- Mew-X pinned commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## 1. Dexter Does Not Already Have A Formal Paper Mode

### Historical ingestion and DB observation surface

Dexter has a fully separate historical observation surface:

- `DexLab/wsLogs.py:53-125` subscribes to websocket logs, decodes events, and forwards them into market persistence.
- `DexLab/market.py:141-501` persists mint and swap state, monitors stagnant mints, and supports replay export.
- `DexAI/trust_factor.py:40-243` rebuilds creator scores from persisted stagnant-mint history.

That surface is observational and replay-seeding. It is not an execution simulator.

### Zero-balance observe-only safety path

Dexter also has a safe live path that behaves like observe-only when the wallet cannot fund a buy:

- `Dexter.py:1140-1162` fetches the real wallet balance at startup.
- `Dexter.py:518-536` rejects the buy before `entry_attempt` if `available_balance <= reserved_cost`.

This is not an explicit runtime mode. It is a natural safety outcome from a zero or insufficient real wallet balance.

### Instrumentation mode is metadata only

Dexter instrumentation accepts a mode string, but that string does not drive runtime behavior:

- `DexLab/instrumentation.py:150-163` reads `VEXTER_MODE`, defaulting to `observe_live`.
- `DexLab/instrumentation.py:202-267` and `225-250` only stamp that mode into state and NDJSON envelopes.

No branch in `Dexter.py` reads `self.instrumentation.mode` or `VEXTER_MODE` to swap execution behavior.

### A lower-level simulation seam exists, but Dexter never uses it

The real hidden seam is lower in the send layer:

- `DexLab/pump_fun/pump_swap.py:429-444` implements `_simulate_or_send()`.
- `DexLab/pump_fun/pump_swap.py:446-503` exposes `pump_buy(..., sim=False)`.
- `DexLab/pump_fun/pump_swap.py:565-614` exposes `pump_sell(..., sim=False)`.

If `sim=True`, the code calls `simulate_transaction()` instead of `send_transaction()`.

But the live controller never routes through that seam:

- `Dexter.py:560-567` hard-codes `sim=False` for buys.
- `Dexter.py:645-652` hard-codes `False` for sells.

### Finding

Frozen Dexter contains:

- a historical observation surface
- a zero-balance safety outcome
- a lower-level transaction simulation seam

Frozen Dexter does not contain a formal paper or sim runtime mode that the strategy loop can select end-to-end.

## 2. Smallest Viable Paper-Equivalent Path

The smallest safe path is not "toggle `sim=True` in one place". The upper layer still expects real holder-balance changes and real RPC transaction lookups. The minimal slice therefore has to cut across submission, confirmation, and balance accounting together.

### Recommended insertion points

| Insertion point | Why this is the smallest safe seam | Minimal paper responsibility |
| --- | --- | --- |
| `Dexter.py:498-626` (`buy`) | Centralizes amount sizing, quote basis, reserve accounting, entry-attempt emission, and the call into Pump.fun execution | Add an explicit paper execution branch that reuses the same sizing and quote logic, but never sends a live tx |
| `Dexter.py:827-885` (`monitor_mint_session`) | This is where Dexter currently waits for holder balance or RPC confirmation before it can emit `entry_fill` and continue the session | Add a paper confirmation branch that resolves a synthetic fill immediately from the quote/simulation result |
| `Dexter.py:632-710` (`sell`) | This is where exit fill, wallet balance update, and position closeout still depend on a real tx plus `get_swap_tx()` | Add a paper exit branch that uses the current market snapshot or simulated quote and an internal paper ledger |
| `Dexter.py:80-109`, `110-127`, `1177-1186` | A paper path needs explicit execution mode, synthetic balance state, and reliable finalization metadata | Add explicit paper-mode config and harden run closeout so `run_summary` is reliable |
| `DexLab/pump_fun/pump_swap.py:429-614` | The simulation seam already exists here, but its raw return shape is not enough for the strategy loop | Reuse or slightly wrap it so the upper layer gets quote/simulation metadata without needing a real signature or post-state |
| `DexLab/instrumentation.py:456-760` | The normalized event schema already covers paper entry, session, and exit events | Reuse existing event types; only add paper-specific payload labels and mode naming |

### Why the seam should not be lower or higher

Too low:

- changing only `pump_buy(..., sim=True)` and `pump_sell(..., sim=True)` does not help because `monitor_mint_session()` still waits for holder-balance or `get_swap_tx()` confirmation (`Dexter.py:827-885`)
- simulation responses do not mutate wallet state or token balances for the controller

Too high:

- trying to solve this in Vexter packaging would only relabel missing evidence after the fact
- the missing events have to originate inside Dexter's runtime control flow

### Recommended paper-equivalent model

The minimal design should introduce an explicit Dexter execution mode such as `paper_live` that:

- keeps the live websocket intake, leaderboard refresh, trust-level projection, and exit ladder unchanged
- never submits a real buy or sell transaction
- never depends on real wallet deltas or `get_swap_tx()` for entry/exit confirmation
- maintains an internal paper cash and position ledger only for event attribution
- writes `mode=paper_live` into the existing NDJSON envelope

That is "paper-equivalent" rather than a perfect simulator. It is enough for comparison evidence because it exercises the same Dexter decision loop against the same live market state while avoiding funded execution.

## 3. Event Coverage Gaps A Minimal Paper Path Could Close

The current promoted pair is missing:

- `candidate_rejected`
- `entry_attempt`
- `entry_fill`
- `exit_fill`
- `exit_signal`
- `position_closed`
- `run_summary`
- `session_update`

### Gap-by-gap assessment

| Missing event | Could minimal paper mode close it? | How | Confidence |
| --- | --- | --- | --- |
| `candidate_rejected` | Conditional only | This event already exists in `monitor_mint_session()` gate rejects (`Dexter.py:735-746`). A paper position could make `single_lock` rejects more likely, but the event still depends on runtime circumstances. Do not promise it every run. | Low |
| `entry_attempt` | Yes | Emit after sizing and quote selection, then route to paper execution instead of the insufficient-balance early return | High |
| `entry_fill` | Yes | Resolve immediate synthetic fill from the paper execution result or quote result and bypass holder/RPC confirmation | High |
| `exit_fill` | Yes | Use current live snapshot or paper sell simulation result, then emit synthetic exit fill with a paper tx label | High |
| `exit_signal` | Yes | Once a paper position exists, the current session loop already reaches the existing exit branches | High |
| `position_closed` | Yes | Current closeout logic already exists after exit fill | High |
| `run_summary` | Yes, but mostly via closeout hardening | The event already exists in `DexLab/instrumentation.py:745-762` and is called in `Dexter.close()` (`Dexter.py:1177-1186`). A paper path helps only if finalization becomes reliable on stop. | Medium |
| `session_update` | Yes | The current loop already emits updates on price changes (`Dexter.py:1021-1038`) once a position gets past the missing fill confirmation stage | High |

### Coverage expectation

A minimal paper path should realistically move Dexter from `4 / 12` to `10 / 12` on eventful runs by adding:

- `entry_attempt`
- `entry_fill`
- `session_update`
- `exit_signal`
- `exit_fill`
- `position_closed`

If closeout reliability is tightened, it can likely reach `11 / 12` by also restoring `run_summary`.

It does not guarantee `12 / 12`, because `candidate_rejected` is conditional rather than structurally mandatory on every run.

That means the paper path materially improves comparison evidence, but it may still leave Vexter's current validator in `partial` on runs where no gate reject occurs.

## 4. What Would And Would Not Be Comparable Versus Mew-X Sim

### Mew-X sim baseline confirmed from source

Mew-X does have an explicit runtime mode split:

- `src/mew/config.rs:128-131` reads `MODE`
- `src/mew/snipe/handler.rs:399-413` routes to `sim_session()` or `trade_session()`

Its sim path is already paper-equivalent:

- `src/mew/snipe/handler.rs:530-555` emits simulated `entry_attempt` and `entry_fill`
- `src/mew/snipe/handler.rs:726-739` emits `session_update`
- `src/mew/snipe/handler.rs:741-761` emits simulated `exit_signal`, `exit_fill`, and `position_closed`
- `src/mew/instrumentation.rs:395-427`, `982-1017` exports session summaries and finalizes with `Drop`

### What a Dexter paper-equivalent path would support

Comparable enough to evaluate:

- candidate sourcing at the decision boundary
- session admission timing
- entry timing versus live market state
- session evolution under the live stream
- exit reason selection
- MFE, MAE, time-to-peak, stale-closeout behavior
- replayability evidence from config, leaderboard, event stream, and replay exports

This is the same comparison layer Mew-X sim already exposes: decision logic against live market movement, not true execution quality.

### What would remain non-comparable

Still not faithfully comparable:

- true execution quality
- true route behavior
- true slippage
- true confirmation latency
- real transaction failure semantics
- real RPC, websocket, ATA, or signature-propagation failure modes

Dexter paper-equivalent would also remain weaker than Mew-X sim on persisted paper-session history until Dexter gains a paper-session export akin to:

- `src/mew/sol_hook/goldmine.rs:98,473` (`Sim` persistence)
- `src/mew/instrumentation.rs:395-427` (session summary export)

### Practical implication

Implementing Dexter paper-equivalent is worthwhile if the goal is:

- fair comparison of candidate conversion and session logic under safe modes

It is not sufficient if the goal is:

- ranking execution transport, venue quality, retry quality, or realized slippage

## 5. Minimum Implementation Slice Worth Doing

### Exact file touch set

If the recommendation is followed, the minimum slice worth doing is:

1. `sources/Dexter/Dexter.py`
2. `sources/Dexter/DexLab/pump_fun/pump_swap.py`
3. `sources/Dexter/DexLab/instrumentation.py`
4. `sources/Dexter/tests/` for paper-path coverage

No Mew-X files are required for this slice.
No Vexter validator or metrics-contract changes are required for the first implementation slice.

### Minimal implementation shape

1. Add explicit Dexter execution-mode configuration

- keep `observe_live` as the default
- add an opt-in paper label such as `paper_live`
- keep instrumentation mode and runtime execution mode aligned, but treat them as real control flow rather than metadata only

2. Add a small paper ledger inside Dexter

- synthetic available SOL
- synthetic reserved buy spend
- synthetic token quantity per active paper position

3. Split buy execution into:

- signal and sizing
- quote or simulation call
- fill confirmation

In live mode, keep the current behavior.
In paper mode, stop after quote or simulation and synthesize the fill.

4. Split sell execution into:

- exit signal
- execution call
- fill confirmation and ledger update

In live mode, keep the current behavior.
In paper mode, synthesize exit fill from the live market snapshot or simulation result.

5. Harden closeout

- keep `Dexter.close()` finalization
- add a reliable process-exit fallback such as `atexit` registration or equivalent guard
- do not rely on forced process termination for `run_summary`

### Reuse versus new contract

No new normalized event types are required.

Reuse:

- `entry_attempt`
- `entry_rejected`
- `entry_fill`
- `session_update`
- `exit_signal`
- `exit_fill`
- `position_closed`
- `run_summary`

Only payload labels need paper-specific values, for example:

- `mode=paper_live`
- `tx_strategy=paper_quote` or `paper_simulation`
- `confirmation_path=paper_fill`
- synthetic signatures such as `paper-entry:<mint>` and `paper-exit:<mint>`

### Safety constraints

The implementation should preserve these rules:

- default remains `observe_live`
- paper mode must be explicit and opt-in
- paper mode must never call a live send path
- paper mode must never call `get_swap_tx()` for confirmation
- paper mode must never mutate or depend on the real wallet balance
- candidate selection, trust-level projection, exit ladder math, and gate predicates must remain unchanged

### Rollback conditions

The paper path should fail closed if:

- quote or simulation output is empty or invalid
- the paper ledger would go negative
- a required live snapshot is missing
- closeout cannot reliably emit state and summary artifacts

In those cases, the mode should reuse the existing `entry_rejected` event or abort the session cleanly rather than silently fabricating more evidence.

### Proof expectations

A successful first paper-equivalent slice should prove:

- Dexter emits `entry_attempt`, `entry_fill`, `session_update`, `exit_signal`, `exit_fill`, and `position_closed` on a safe same-window run
- all such events carry `mode=paper_live`
- no live signatures or live wallet deltas are required
- the matched comparison with Mew-X sim improves from the current `4 / 12` baseline

The design should not promise:

- a guaranteed `candidate_rejected` on every run
- a guaranteed `12 / 12` validator pass without a gate reject
- any execution-quality claim

## Decision

### Recommendation

Proceed to implementation.

### Why

Repeated `TASK-005` retries already established the safe observe-only ceiling:

- same-attempt packaging was repaired
- exact event overlap was recovered
- Dexter still plateaued at `4 / 12`

The missing comparison signal is now concentrated in Dexter's execution-confirmation path, not in Vexter retry orchestration.

Frozen Dexter already has the raw ingredients for a minimal paper-equivalent path:

- a simulation seam in the send layer
- a normalized instrumentation contract
- a live session loop that already emits exit and session events once fills exist

That combination makes `DEXTER-PAPER-IMPLEMENT` the next task worth doing.

### Non-goals for the implementation follow-up

The follow-up should not:

- change creator scoring
- change entry thresholds
- change exit ladder thresholds
- change Mew-X
- change Vexter comparison rules
- start `TASK-006`
