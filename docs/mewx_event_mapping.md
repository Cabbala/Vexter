# Mew-X Event Mapping

## Objective

Freeze the first measurement-ready Mew-X instrumentation surface without changing creator selection, entry rules, or exit rules.

## Event Surface

| Normalized event | Mew-X source area | Notes |
| --- | --- | --- |
| `creator_candidate` | `sources/Mew-X/src/main.rs`, `sources/Mew-X/src/mew/deagle/deagle.rs` | Emits source-labeled creator admissions from Deagle, volume creators, and grand chillers plus refresh additions |
| `mint_observed` | `sources/Mew-X/src/mew/snipe/handler.rs` | Fires for Pump.fun creates and migrated PumpSwap dip-watch starts with create metadata and source attribution when present |
| `candidate_rejected` | `sources/Mew-X/src/mew/snipe/handler.rs` | Captures duplicate-token, region, concurrency, CHP, and TIZ rejects without changing admission logic |
| `entry_signal` | `sources/Mew-X/src/mew/snipe/handler.rs` | Captures admitted session starts for creator matches, ABS, DBF, and dip re-entry paths |
| `entry_attempt` | `sources/Mew-X/src/mew/snipe/handler.rs` | Captures route family, tx strategy, transport path, fee/tip settings, and expected output for simulated and live attempts |
| `entry_fill` | `sources/Mew-X/src/mew/snipe/handler.rs` | Captures simulated fills and live transport acknowledgements with signature, latency, and wallet snapshot |
| `entry_rejected` | `sources/Mew-X/src/mew/snipe/handler.rs` | Keeps failed entry attempts attributable when the outbound transport send fails |
| `session_update` | `sources/Mew-X/src/mew/snipe/handler.rs` | Captures price, peak, creator state, txns-in-zero / txns-in-n, MFE/MAE, migration, and dip-trigger checkpoints |
| `exit_signal` | `sources/Mew-X/src/mew/snipe/handler.rs` | Captures loss, take-profit, inactivity, recent-profit collapse, creator-sold, and guard exits |
| `exit_fill` | `sources/Mew-X/src/mew/snipe/handler.rs` | Captures simulated exits and live sell transport acknowledgements with signature and latency |
| `position_closed` | `sources/Mew-X/src/mew/snipe/handler.rs` | Captures realized return, MFE, MAE, time-to-peak, session duration, and stale-session flag |
| `run_summary` | `sources/Mew-X/src/mew/instrumentation.rs` | Captures run-level counts and replayability once the process finalizes |

## Non-Event Exports

- Masked config snapshot: `sources/Mew-X/src/mew/instrumentation.rs`
- Candidate refresh snapshots: `sources/Mew-X/src/mew/instrumentation.rs`
- Session summaries: `sources/Mew-X/src/mew/instrumentation.rs`

## Fixed Windows Outputs

- `C:\Users\bot\quant\Vexter\runtime\mewx\config`
- `C:\Users\bot\quant\Vexter\runtime\mewx\export`
- `C:\Users\bot\quant\Vexter\data\raw\mewx`
- `C:\Users\bot\quant\Vexter\data\logs\mewx`
- `C:\Users\bot\quant\Vexter\data\replays\mewx`
- `C:\Users\bot\quant\Vexter\data\postgres\mewx`

`D:\Quant\Vexter` remains the preferred runtime root if it exists, but the verified fallback stays `C:\Users\bot\quant\Vexter`.

## Notes

- Live entry and exit fills are transport-ack based so the instrumentation remains observational and does not add confirmation gating to the strategy loop.
- Dexter instrumentation remains frozen; this mapping is the Mew-X counterpart only.
