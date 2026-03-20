# TASK-005 Live Collection Blocker

## Checked Scope

- checked at `2026-03-20T18:00:16Z`
- target host: `win-lan` (`DESKTOP-NNC6MPS`)
- fixed runtime root: `C:\Users\bot\quant\Vexter`
- required result: one Dexter package and one Mew-X package from the same live measurement window

## What Was Recovered

- `cargo`, `rustc`, and `psql` are now available on `win-lan`
- PostgreSQL 17.9 is restored and listening on `127.0.0.1:5432`
- frozen Dexter and Mew-X source checkouts now exist under `C:\Users\bot\quant\Vexter\sources`
- Dexter dependencies were restored in `C:\Users\bot\quant\Vexter\venvs\dexter`
- Dexter database bootstrap completed successfully against the restored PostgreSQL instance
- repo-root env injection points are now documented and templated for both Dexter and Mew-X

## Remaining Blockers

- `C:\Users\bot\quant\Vexter\data\raw\dexter`: no NDJSON event files yet
- `C:\Users\bot\quant\Vexter\data\raw\mewx`: no NDJSON event files yet
- `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs`: no packaged runs present yet
- Dexter still requires user-populated secrets at `C:\Users\bot\quant\Vexter\sources\Dexter\.env`
- Mew-X still requires user-populated secrets at `C:\Users\bot\quant\Vexter\sources\Mew-X\.env`
- a fresh Mew-X launch now reaches config validation and fails at `PRIVATE_KEY is invalid / not set`

## Result

- live Dexter package: `NONE`
- live Mew-X package: `NONE`
- live comparison output directory: `NONE`
- evidence-backed winners / ties recorded: `none`
- blocker state: `narrowed_blocker`
- `TASK-006` readiness: `blocked`

## Unblock Steps

- populate the repo-root `.env` files using `templates/windows_runtime/dexter.env.example` and `templates/windows_runtime/mewx.env.example`
- run the frozen Dexter and Mew-X checkouts so they emit matched live raw events under the fixed Vexter root
- collect matched live packages with `scripts/collect_comparison_package.ps1`
- rerun `scripts/comparison_analysis.py build-pack` only after both live packages exist
