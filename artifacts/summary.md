# TASK-005 Live Comparison Evidence Summary

## Status

- `TASK-005-live-comparison-evidence` is blocked on branch `codex/task-005-live-comparison-evidence` as of 2026-03-21.
- Start conditions were re-verified from `Cabbala/Vexter` `main` at commit `939642e6d185629f23a04e8e04f9fc7eac62ebc9`.
- Dexter and Mew-X instrumentation remain unchanged; no strategy or execution logic was modified.
- No matched live Dexter / Mew-X packages were available from the fixed Windows runtime, so no live comparison pack or evidence-backed winners / ties were recorded.
- `TASK-006` replay validation cannot begin from this state.

## Collection Evidence

- fixed Windows root `C:\Users\bot\quant\Vexter` exists on `DESKTOP-NNC6MPS`
- `C:\Users\bot\quant\Vexter\data\raw\dexter` and `C:\Users\bot\quant\Vexter\data\raw\mewx` did not contain any NDJSON event files
- `C:\Users\bot\quant\Vexter\runtime\dexter\config`, `C:\Users\bot\quant\Vexter\runtime\dexter\export`, `C:\Users\bot\quant\Vexter\runtime\mewx\config`, and `C:\Users\bot\quant\Vexter\runtime\mewx\export` were empty
- `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs` did not contain any packaged runs
- `git` and `python` were available on `win-lan`, but `cargo`, `rustc`, and `psql` were not detected
- no PostgreSQL process or `127.0.0.1:5432` listener was detected on `win-lan`

## TASK-005 Output State

- live Dexter package path: `NONE`
- live Mew-X package path: `NONE`
- live comparison output directory: `NONE`
- winner / tie decisions: deferred for candidate sourcing, execution, exit quality, and replayability
- blocker evidence: `artifacts/reports/task-005-live-collection-blocker.md`
- structured proof: `artifacts/proofs/task-005-live-collection-check.json`

## Unblock Requirements

- deploy the frozen Dexter and Mew-X source branches onto `win-lan` so they write config, export, raw event, log, and replay artifacts into the fixed Vexter root
- restore the Mew-X runtime prerequisites on `win-lan` (`cargo`, `rustc`, and PostgreSQL reachable from `DB_URL`)
- collect one Dexter run and one Mew-X run from the same live measurement window
- rerun `scripts/collect_comparison_package.ps1` and `scripts/comparison_analysis.py build-pack` once both live packages exist
