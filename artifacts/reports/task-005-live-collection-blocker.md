# TASK-005 Live Collection Blocker

## Checked Scope

- checked at `2026-03-20T17:01:21Z`
- target host: `win-lan` (`DESKTOP-NNC6MPS`)
- fixed runtime root: `C:\Users\bot\quant\Vexter`
- required result: one Dexter package and one Mew-X package from the same live measurement window

## What Was Found

- `C:\Users\bot\quant\Vexter\data\raw\dexter`: no NDJSON event files
- `C:\Users\bot\quant\Vexter\data\raw\mewx`: no NDJSON event files
- `C:\Users\bot\quant\Vexter\runtime\dexter\config`: empty
- `C:\Users\bot\quant\Vexter\runtime\dexter\export`: empty
- `C:\Users\bot\quant\Vexter\runtime\mewx\config`: empty
- `C:\Users\bot\quant\Vexter\runtime\mewx\export`: empty
- `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs`: no packaged runs present
- `git` and `python` are available on `win-lan`
- `cargo`, `rustc`, and `psql` are not available on `win-lan`
- no PostgreSQL process or `127.0.0.1:5432` listener was detected on `win-lan`

## Result

- live Dexter package: `NONE`
- live Mew-X package: `NONE`
- live comparison output directory: `NONE`
- evidence-backed winners / ties recorded: `none`
- `TASK-006` readiness: `blocked`

## Unblock Steps

- provision the frozen Dexter and Mew-X source branches on `win-lan`
- restore config, export, raw event, replay, and log outputs under the fixed Vexter root
- restore the Mew-X runtime prerequisites on `win-lan` (`cargo`, `rustc`, and PostgreSQL reachable from `DB_URL`)
- collect matched live packages with `scripts/collect_comparison_package.ps1`
- rerun `scripts/comparison_analysis.py build-pack` only after both live packages exist
