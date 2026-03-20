# Dexter Event Mapping

## Objective

Freeze the first measurement-ready Dexter instrumentation surface without changing creator scoring, entry logic, or exit logic.

## Event Surface

| Normalized event | Dexter source area | Notes |
| --- | --- | --- |
| `creator_candidate` | `sources/Dexter/Dexter.py` leaderboard refresh via `DexLab/instrumentation.py` | Emits one event per admitted creator and writes a leaderboard snapshot |
| `mint_observed` | `sources/Dexter/Dexter.py` mint match path | Fires when a fresh mint maps to a leaderboard creator |
| `candidate_rejected` | `sources/Dexter/Dexter.py` session admission gates | Captures blacklist, single-lock, and leaderboard-update skips |
| `entry_signal` | `sources/Dexter/Dexter.py` session start | Captures matched creator, trust level projection, and signal latency |
| `entry_attempt` | `sources/Dexter/Dexter.py` buy submission | Captures quote price, reserved balance state, and tx strategy |
| `entry_fill` | `sources/Dexter/Dexter.py` holder-balance or RPC fallback confirmation | Captures fill price, qty, latency, tx signature, and confirmation path |
| `entry_rejected` | `sources/Dexter/Dexter.py` buy skips and confirmation failures | Keeps failed entry reasons attributable after signal time; `tx_signature` is only present when a send path actually produced one |
| `session_update` | `sources/Dexter/Dexter.py` live session loop | Captures price, peak, liquidity, MFE/MAE, composite score, and target step |
| `exit_signal` | `sources/Dexter/Dexter.py` sell trigger path | Captures exit reason plus theoretical peak context |
| `exit_fill` | `sources/Dexter/Dexter.py` sell confirmation | Captures realized price, qty, latency, tx signature, and wallet delta |
| `position_closed` | `sources/Dexter/Dexter.py` post-sell closeout | Captures realized return, MFE, MAE, peak timing, and stale flag |
| `run_summary` | `sources/Dexter/DexLab/instrumentation.py` finalizer | Captures event counts and replayability flag for the run |

## Non-Event Exports

- Masked config snapshot: `sources/Dexter/DexLab/instrumentation.py`
- Leaderboard snapshot: `sources/Dexter/DexLab/instrumentation.py`
- Stagnant-mint replay export on move-to-stagnant: `sources/Dexter/DexLab/market.py`
- Manual replay export command: `python DexLab/instrumentation.py --db-dsn postgres://dexter_user:admin123@127.0.0.1/dexter_db`

## Fixed Windows Outputs

- `C:\Users\bot\quant\Vexter\runtime\dexter\config`
- `C:\Users\bot\quant\Vexter\runtime\dexter\export`
- `C:\Users\bot\quant\Vexter\data\raw\dexter`
- `C:\Users\bot\quant\Vexter\data\logs\dexter`
- `C:\Users\bot\quant\Vexter\data\replays\dexter`
- `C:\Users\bot\quant\Vexter\data\postgres\dexter`

`D:\Quant\Vexter` remains the preferred runtime root if it exists, but the verified fallback stays `C:\Users\bot\quant\Vexter`.
