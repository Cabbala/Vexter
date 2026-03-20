# TASK-005 Live Comparison Evidence Summary

## Status

- `TASK-005-live-comparison-evidence` is now in `exact_env_key_blocker` state on branch `codex/task-005-live-comparison-evidence` as of 2026-03-21.
- Start conditions were re-verified from `Cabbala/Vexter` `main` at commit `939642e6d185629f23a04e8e04f9fc7eac62ebc9` and the open work-branch PR `#5`.
- Dexter and Mew-X strategy, execution, and instrumentation logic remain unchanged; this work only resumed live collection from the recovered Windows runtime and captured the next narrower blocker with sanitized evidence.
- The 2026-03-20T18:48:13Z resume probe launched the frozen Dexter and Mew-X Windows checkouts with fixed-root overrides. Dexter's Helius HTTP and WebSocket endpoints both responded successfully from `win-lan`, but both sources still exited before emitting raw events or packaged runs.
- No matched live Dexter / Mew-X packages have been collected yet, so no validator output, derived metrics, live comparison pack, or evidence-backed winners / ties were recorded.
- `TASK-006` replay validation cannot begin from this state.

## Resume Probe Evidence

- fixed Windows root `C:\Users\bot\quant\Vexter` still exists on `DESKTOP-NNC6MPS`
- `git`, `python`, `cargo`, `rustc`, and `psql` remain available on `win-lan`
- PostgreSQL is still running and listening on `127.0.0.1:5432`
- frozen Dexter and Mew-X source checkouts remain pinned at the TASK-002 / TASK-003 commits
- repo-root `.env` files now exist at the documented Dexter and Mew-X Windows injection points
- Dexter `HTTP_URL` and `WS_URL` are now non-empty and no longer placeholder-like
- Dexter Helius probes succeeded from `win-lan`: JSON-RPC `getVersion` returned a result and a direct WebSocket connection opened successfully
- live launch overrides were injected at process start for `VEXTER_RUNTIME_ROOT` / `VEXTER_OUTPUT_ROOT` and source-specific run IDs
- `C:\Users\bot\quant\Vexter\data\raw\dexter`, `C:\Users\bot\quant\Vexter\data\raw\mewx`, and `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs` remained empty after the probe; temporary Dexter probe export/log artifacts were cleaned after the blocker was captured

## Exact Blocker

- Dexter startup now fails at `C:\Users\bot\quant\Vexter\sources\Dexter\.env` `PRIVATE_KEY`: the configured value contains the invalid base58 character `0`, so the frozen runtime aborts during key parsing before collection starts
- Mew-X startup now fails at `C:\Users\bot\quant\Vexter\sources\Mew-X\.env` `PRIVATE_KEY`: Solana keypair parsing aborts on an invalid base58 character before collection starts
- because both sources exit during keypair parsing, live package collection cannot begin, so `validate`, `derive-metrics`, and `build-pack` remain blocked on exact env-key correction rather than on generic runtime recovery

## TASK-005 Output State

- live Dexter package path: `NONE`
- live Mew-X package path: `NONE`
- live comparison output directory: `NONE`
- winner / tie decisions: deferred for candidate sourcing, execution, exit quality, and replayability
- runtime recovery evidence: `artifacts/reports/task-005-windows-runtime-recovery.md`
- exact blocker evidence: `artifacts/reports/task-005-live-collection-blocker.md`
