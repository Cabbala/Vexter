# TASK-005 Live Comparison Evidence Summary

## Status

- `TASK-005-live-comparison-evidence` is now in `narrowed_blocker` state on branch `codex/task-005-live-comparison-evidence` as of 2026-03-21.
- Start conditions were re-verified from `Cabbala/Vexter` `main` at commit `939642e6d185629f23a04e8e04f9fc7eac62ebc9` and the open work-branch PR `#5`.
- Dexter and Mew-X strategy, execution, and instrumentation logic remain unchanged; this work only recovers the Windows runtime, clarifies env injection points, and restores live-package collection prerequisites.
- No matched live Dexter / Mew-X packages have been collected yet, so no live comparison pack or evidence-backed winners / ties were recorded.
- `TASK-006` replay validation cannot begin from this state.

## Recovery Evidence

- fixed Windows root `C:\Users\bot\quant\Vexter` exists on `DESKTOP-NNC6MPS`
- `cargo`, `rustc`, and `psql` are now available on `win-lan`
- `Google.Protobuf` plus user-scope `PROTOC`, `PROTOC_INCLUDE`, and `INSTALL_DIR` are now available on `win-lan`
- PostgreSQL 17.9 is restored and listening on `127.0.0.1:5432`
- frozen Dexter and Mew-X source checkouts are restored at the pinned commits used by TASK-002 and TASK-003
- Dexter dependencies and local database bootstrap were restored successfully
- documented repo-root env injection points now exist for Dexter and Mew-X under their Windows source checkouts
- a fresh Mew-X launch now reaches repo-root env validation and fails at `PRIVATE_KEY is invalid / not set`

## Remaining Blocker

- user-populated `.env` files are still required at `C:\Users\bot\quant\Vexter\sources\Dexter\.env` and `C:\Users\bot\quant\Vexter\sources\Mew-X\.env`
- `C:\Users\bot\quant\Vexter\data\raw\dexter` and `C:\Users\bot\quant\Vexter\data\raw\mewx` still contain no live NDJSON event files
- `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs` still contains no packaged runs

## TASK-005 Output State

- live Dexter package path: `NONE`
- live Mew-X package path: `NONE`
- live comparison output directory: `NONE`
- winner / tie decisions: deferred for candidate sourcing, execution, exit quality, and replayability
- runtime recovery evidence: `artifacts/reports/task-005-windows-runtime-recovery.md`
- collection blocker evidence: `artifacts/reports/task-005-live-collection-blocker.md`
