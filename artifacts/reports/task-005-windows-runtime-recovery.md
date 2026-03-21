# TASK-005 Windows Runtime Recovery

## Verified Scope

- verified at `2026-03-21T11:01:05Z`
- target host: `win-lan` (`DESKTOP-NNC6MPS`)
- fixed runtime root: `C:\Users\bot\quant\Vexter`
- control branch: `codex/task-005-paper-validation`
- start point rechecked from `origin/main` commit `379f55a50dbfd91968ba643e2fbfe5e73fad8392` after merged PR `#12` and PR `#13`

## Recovered Runtime Prerequisites

- `cargo 1.94.0 (85eff7c80 2026-01-15)` is available on `win-lan`
- `rustc 1.94.0 (4a4ef493e 2026-03-02)` is available on `win-lan`
- `psql (PostgreSQL) 17.9` is available on `win-lan`
- `Google.Protobuf` is installed and provides `protoc.exe` plus protobuf includes on `win-lan`
- PostgreSQL 17.9 is listening on `127.0.0.1:5432`
- runtime directories, raw-data roots, replay roots, unified report roots, source roots, tools, downloads, and virtualenv roots exist under the fixed Windows root

## Restored Checkouts

- Dexter checkout: `C:\Users\bot\quant\Vexter\sources\Dexter` at merged `main` `5dc1036c499af5f14f06d08ad0fa96aa36228c96`
- Mew-X checkout: `C:\Users\bot\quant\Vexter\sources\Mew-X` at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Dexter virtualenv: `C:\Users\bot\quant\Vexter\venvs\dexter`
- Dexter database bootstrap completed successfully against local PostgreSQL
- confirmed databases: `dexter_db`, `goldmine`, `vacation`

## Env Injection Points

- Dexter reads `C:\Users\bot\quant\Vexter\sources\Dexter\.env`
- Dexter required keys: `PRIVATE_KEY`, `HTTP_URL`, `WS_URL`
- TASK-005 paper validation mode: `VEXTER_MODE=paper_live`
- Mew-X reads `C:\Users\bot\quant\Vexter\sources\Mew-X\.env`
- Mew-X required keys: `RPC_URL`, `WS_URL`, `PRIVATE_KEY`, `DB_URL`
- TASK-005 Mew-X mode: `MODE=sim`

## Output Roots Ready For Collection

- Dexter raw events: `C:\Users\bot\quant\Vexter\data\raw\dexter`
- Mew-X raw events: `C:\Users\bot\quant\Vexter\data\raw\mewx`
- unified comparison input root: `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs`
- unified runtime reports: `C:\Users\bot\quant\Vexter\runtime\unified\reports`

## Current Runtime Conclusion

- runtime recovery status: `ready_for_task_005_paper_validation`
- fresh paper/sim matched packages collected: `2`
- remaining blocker is no longer environment recovery; it is Dexter `paper_live` staying creator-only on fresh matched pairs
- `TASK-006` readiness: `blocked`
