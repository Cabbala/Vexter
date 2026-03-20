# TASK-005 Windows Runtime Recovery

## Verified Scope

- verified at `2026-03-20T18:00:16Z`
- target host: `win-lan` (`DESKTOP-NNC6MPS`)
- fixed runtime root: `C:\Users\bot\quant\Vexter`
- control branch: `codex/task-005-live-comparison-evidence`
- start point rechecked from `origin/main` commit `939642e6d185629f23a04e8e04f9fc7eac62ebc9` and open PR `#5`

## Recovered Runtime Prerequisites

- `cargo 1.94.0 (85eff7c80 2026-01-15)` is available on `win-lan`
- `rustc 1.94.0 (4a4ef493e 2026-03-02)` is available on `win-lan`
- `psql (PostgreSQL) 17.9` is available on `win-lan`
- `Google.Protobuf` is installed and provides `protoc.exe` plus protobuf includes on `win-lan`
- PostgreSQL 17.9 was restored from the official EDB binaries zip and is listening on `127.0.0.1:5432`
- PostgreSQL data directory: `C:\Users\bot\quant\Vexter\data\postgres\portable17`
- PostgreSQL log path: `C:\Users\bot\quant\Vexter\data\logs\postgresql-17.log`
- runtime directories, raw-data roots, replay roots, unified report roots, source roots, tools, downloads, and virtualenv roots now exist under the fixed Windows root

## Restored Frozen Checkouts

- Dexter checkout: `C:\Users\bot\quant\Vexter\sources\Dexter` at `69de8b6ca57ca3d03025d85329c88aa4a167da34`
- Mew-X checkout: `C:\Users\bot\quant\Vexter\sources\Mew-X` at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Dexter virtualenv: `C:\Users\bot\quant\Vexter\venvs\dexter`
- Dexter database bootstrap completed successfully against local PostgreSQL
- created / confirmed databases: `dexter_db`, `goldmine`, `vacation`

## Env Injection Points

- Dexter reads `C:\Users\bot\quant\Vexter\sources\Dexter\.env`
- Dexter required keys: `PRIVATE_KEY`, `HTTP_URL`, `WS_URL`
- Mew-X reads `C:\Users\bot\quant\Vexter\sources\Mew-X\.env`
- Mew-X required keys: `RPC_URL`, `WS_URL`, `PRIVATE_KEY`, `DB_URL`
- recovery also persists `PROTOC`, `PROTOC_INCLUDE`, and `INSTALL_DIR` so a fresh PowerShell session can compile and launch Mew-X on Windows
- example env files were added under `templates/windows_runtime/`

## Output Roots Ready For Live Collection

- Dexter raw events: `C:\Users\bot\quant\Vexter\data\raw\dexter`
- Mew-X raw events: `C:\Users\bot\quant\Vexter\data\raw\mewx`
- unified comparison input root: `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs`
- unified runtime reports: `C:\Users\bot\quant\Vexter\runtime\unified\reports`

## Narrowed Blocker

- Dexter runtime recovery is complete enough to collect a live package once its repo-root `.env` is populated
- a fresh `cargo run --quiet` from `C:\Users\bot\quant\Vexter\sources\Mew-X` now reaches config validation and fails at `PRIVATE_KEY is invalid / not set`
- matched live package collection is now blocked only on user-populated repo-root `.env` files and the first shared live observation window
- no Dexter or Mew-X strategy, execution, or instrumentation logic was changed during this recovery work

## Result

- runtime recovery status: `narrowed_blocker`
- matched live packages collected: `0`
- `TASK-006` readiness: `blocked`
