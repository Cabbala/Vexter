# TASK-005 Live Collection Blocker

## Checked Scope

- checked at `2026-03-20T19:11:55Z`
- target host: `win-lan` (`DESKTOP-NNC6MPS`)
- fixed runtime root: `C:\Users\bot\quant\Vexter`
- verified start point: `origin/main` commit `939642e6d185629f23a04e8e04f9fc7eac62ebc9` and open PR `#5`
- required result: one Dexter package and one Mew-X package from the same live measurement window, followed by `validate`, `derive-metrics`, and `build-pack`

## Resume Probe

- Dexter probe launch: `C:\Users\bot\quant\Vexter\venvs\dexter\Scripts\python.exe Dexter.py`
- Mew-X probe launch: `cargo run --quiet` from `C:\Users\bot\quant\Vexter\sources\Mew-X`
- fixed-root overrides were injected at launch time for `VEXTER_RUNTIME_ROOT` and `VEXTER_OUTPUT_ROOT`; run IDs were pinned for the attempted shared window
- `git`, `python`, `cargo`, `rustc`, `psql`, and PostgreSQL remained available during the probe
- Dexter `HTTP_URL` JSON-RPC `getVersion` probe succeeded and Dexter `WS_URL` accepted a direct WebSocket connection from `win-lan`, so no Dexter-side Helius implementation change is required
- Mew-X repo-root `.env` was missing `RPC_URL` even though the frozen runtime reads that key first; the existing `HTTP_URL` value was copied into `RPC_URL` on `win-lan` without changing source logic, and the rerun reached signer parsing
- checked known env files and default Solana key locations on `win-lan` did not reveal an alternate signing key to substitute automatically
- both source processes still exited before any live NDJSON files or packaged runs appeared under `C:\Users\bot\quant\Vexter\data\raw\{dexter,mewx}` or `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs`

## Exact Blockers

- Dexter: `C:\Users\bot\quant\Vexter\sources\Dexter\.env` key `PRIVATE_KEY` is unusable for startup because it exactly matches the Helius `api-key` already embedded in Dexter `HTTP_URL` / `WS_URL`. The frozen Dexter runtime fails during `base58.b58decode(PRIV_KEY)` with `ValueError: Invalid character '0'`.
- Mew-X: `C:\Users\bot\quant\Vexter\sources\Mew-X\.env` key `PRIVATE_KEY` is unusable for startup because it is a truncated prefix of the Helius `api-key` already embedded in Mew-X `RPC_URL` / `WS_URL`. After `RPC_URL` was restored, the frozen Mew-X runtime panics during Solana keypair parsing with `called Result::unwrap() on an Err value: InvalidChar(48)`.
- Because both sources still fail before event emission, there are still no live NDJSON event files and no packaged runs to feed into Vexter validation or comparison tooling.

## Result

- live Dexter package: `NONE`
- live Mew-X package: `NONE`
- live comparison output directory: `NONE`
- evidence-backed winners / ties recorded: `none`
- blocker state: `exact_signer_env_blocker`
- `TASK-006` readiness: `blocked`

## Unblock Steps

- replace `PRIVATE_KEY` in `C:\Users\bot\quant\Vexter\sources\Dexter\.env` with a valid base58 Solana signing key; the current value is only the Helius URL `api-key`
- replace `PRIVATE_KEY` in `C:\Users\bot\quant\Vexter\sources\Mew-X\.env` with a valid base58 Solana signing key; the current value is only a truncated Helius URL `api-key`
- keep `RPC_URL` populated explicitly in `C:\Users\bot\quant\Vexter\sources\Mew-X\.env` if the file is regenerated
- rerun the frozen Dexter and Mew-X checkouts so they emit matched live raw events under the fixed Vexter root
- collect matched live packages with `scripts/collect_comparison_package.ps1`
- run `scripts/comparison_analysis.py validate`, `derive-metrics`, and `build-pack` only after both live packages exist
