# Windows Runtime Recovery

## Goal

Recover only the TASK-005 Windows runtime surface on `win-lan` so Dexter and Mew-X can be launched from their frozen branches and write into the fixed Vexter root without changing strategy, execution, or instrumentation logic.

## Fixed Paths

- Windows root: `C:\Users\bot\quant\Vexter`
- Dexter checkout: `C:\Users\bot\quant\Vexter\sources\Dexter`
- Mew-X checkout: `C:\Users\bot\quant\Vexter\sources\Mew-X`
- Dexter Python venv: `C:\Users\bot\quant\Vexter\venvs\dexter`
- PostgreSQL client: `C:\Users\bot\quant\Vexter\tools\postgresql-17.9\pgsql\bin\psql.exe`
- PostgreSQL data dir: `C:\Users\bot\quant\Vexter\data\postgres\portable17`
- PostgreSQL log: `C:\Users\bot\quant\Vexter\data\logs\postgresql-17.log`

## Recovery Entry Point

Run [scripts/recover_windows_runtime.sh](/Users/cabbala/Documents/vexter/task005-live-comparison-evidence/scripts/recover_windows_runtime.sh) from the Mac control plane. It restores:

- PostgreSQL 17.9 from the official EDB Windows binaries zip
- `Google.Protobuf` so `protoc.exe` and the bundled protobuf includes are present on `win-lan`
- `dexter_db`, `goldmine`, and `vacation` on `127.0.0.1:5432`
- detached frozen source checkouts for Dexter and Mew-X
- Dexter's Python venv and database bootstrap
- user-scope `PROTOC`, `PROTOC_INCLUDE`, and `INSTALL_DIR` so a new PowerShell session can build and launch the frozen Mew-X checkout until it hits repo-root `.env` validation

## Env Injection Points

Edit these files directly on `win-lan`:

- Dexter: `C:\Users\bot\quant\Vexter\sources\Dexter\.env`
- Mew-X: `C:\Users\bot\quant\Vexter\sources\Mew-X\.env`

Reference templates live in:

- [templates/windows_runtime/dexter.env.example](/Users/cabbala/Documents/vexter/task005-live-comparison-evidence/templates/windows_runtime/dexter.env.example)
- [templates/windows_runtime/mewx.env.example](/Users/cabbala/Documents/vexter/task005-live-comparison-evidence/templates/windows_runtime/mewx.env.example)

Formatting rules for both files:

- do not wrap values in `"` quotes
- do not append inline `# comments` after assignments
- keep one `KEY=value` assignment per line

### Dexter

Dexter reads only the repo-root `.env` through `DexLab/common_.py`.

Populate:

- `PRIVATE_KEY`
- `HTTP_URL`
- `WS_URL`

Optional but recommended for package naming and fixed-root output:

- `VEXTER_RUNTIME_ROOT`
- `VEXTER_OUTPUT_ROOT`
- `VEXTER_MODE`
- `VEXTER_TRANSPORT_MODE`
- `VEXTER_RUN_ID`

Dexter does not need a second secret-bearing config file for this recovery path. Its DB DSN remains hardcoded to `postgres://dexter_user:admin123@127.0.0.1/dexter_db`.

Do not paste the Helius URL `api-key` UUID into `PRIVATE_KEY`. Dexter expects a valid base58 Solana signing key there, not the RPC credential already embedded in `HTTP_URL` / `WS_URL`.

### Mew-X

Mew-X reads the repo-root `.env` via `dotenv()` in `src/mew/config.rs`.

Populate at minimum:

- `RPC_URL`
- `WS_URL`
- `PRIVATE_KEY`
- `DB_URL`

`DB_URL` is the local PostgreSQL listener recovered on `win-lan`, not a Helius endpoint. For this workspace the expected DSN is `postgres://postgres:admin123@127.0.0.1:5432`.

If an older local note or copied `.env` only contains `HTTP_URL`, duplicate that same HTTP endpoint into `RPC_URL` before launching. Mew-X reads `RPC_URL` and does not consume `HTTP_URL` from `src/mew/config.rs`.

Keep repo-root `.env` values unquoted on Windows for this recovery path, and avoid inline `#` comments after values. The recovered Mew-X dotenv parsing proved sensitive to formatting, and `REGIONS` should stay space-free if enabled, for example:

- `REGIONS=Germany,Netherlands,UnitedKingdom`

Documented optional / conditional keys for live collection:

- `GRPC_URL`
- `GRPC_TOKEN`
- `USE_GRPC`
- `MODE`
- `MAX_TOKENS_AT_ONCE`
- `TX_STRAT`
- `NONCE_ACCOUNT`
- `NEXTBLOCK_KEY`
- `ZERO_SLOT_KEY`
- `TEMPORAL_KEY`
- `BLOX_KEY`
- `TIP_SOL`
- `PRIORITY_FEE_LVL`

Mew-X's Rust dependency tree also needs `sh.exe` on `PATH` for `protobuf-src`. Recovery injects:

- `C:\Program Files\Git\bin`

Do not prepend `C:\Program Files\Git\usr\bin`; on this host it shadows the MSVC linker with Git's `link.exe`.

Recovery also persists these user-scope environment variables from the installed `Google.Protobuf` package:

- `PROTOC`
- `PROTOC_INCLUDE`
- `INSTALL_DIR`

With those values present, a fresh `cargo run --quiet` on `C:\Users\bot\quant\Vexter\sources\Mew-X` reaches signer parsing. Do not paste the Helius URL `api-key` value into `PRIVATE_KEY`; Mew-X expects a valid base58 Solana signing key there and will panic during `solana-keypair` parsing if the RPC credential is reused.

## Expected Output Roots

Once the user-owned `.env` files are populated and the frozen repos are launched, these paths must stop being empty:

- `C:\Users\bot\quant\Vexter\data\raw\dexter`
- `C:\Users\bot\quant\Vexter\data\raw\mewx`
- `C:\Users\bot\quant\Vexter\runtime\dexter\config`
- `C:\Users\bot\quant\Vexter\runtime\dexter\export`
- `C:\Users\bot\quant\Vexter\runtime\mewx\config`
- `C:\Users\bot\quant\Vexter\runtime\mewx\export`
- `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs`

## Current Narrowed Blocker

Runtime prerequisites, DB reachability, frozen checkouts, Mew-X protobuf build prerequisites, and exact signer/env formatting are now recovered without touching source logic. The current narrowed blocker is no longer startup:

- Dexter and Mew-X both emit smoke-run artifacts under the fixed Vexter root.
- `validate`, `derive-metrics`, and `build-pack` now complete on those smoke packages.
- Both packages still validate as `partial`, and they were not collected from the same live measurement window.

The next unblock requirement is a matched live window with fuller comparable coverage, especially on Dexter:

- collect one Dexter run and one Mew-X run from the same live measurement window
- preserve frozen Dexter and Mew-X strategy, execution, and instrumentation logic
- gather a Dexter run with more than observe-only rejection coverage
- rerun `validate`, `derive-metrics`, and `build-pack` on that matched package pair
