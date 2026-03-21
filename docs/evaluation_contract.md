# Evaluation Contract

## Goal

Vexter compares Dexter and Mew-X before any integration work begins. This contract freezes the minimum evidence required to judge profitability, operational safety, and replayability on equal terms.

## Comparison Scope

- Candidate generation
- Entry qualification
- Execution quality
- Session management
- Exit quality
- Portfolio and risk handling
- Replayability and observability

## Contract Rules

1. Strategy logic is observed, not changed.
2. Dexter and Mew-X runs must emit the same normalized event types for equivalent decisions.
3. Every comparison run must be attributable to a source repo commit, config snapshot, runtime host, and transport mode.
4. Live measurements and replay measurements must be stored separately, then compared through the same metric catalog.
5. A source is not integration-ready unless its event stream is rich enough to reconstruct candidate selection, entry, session, and exit behavior.
6. Preferred validation mode is paper or sim-safe collection before funded live trading: Mew-X should default to `sim_live`, and Dexter should use explicit `paper_live` now that the formal paper mode is confirmed on merged Dexter `main`.

## Required Run Package

Each measurement run must produce:

- normalized event stream in NDJSON
- metrics summary in JSON
- config snapshot with secrets masked
- human summary in Markdown
- proof manifest pointer to raw logs, DB exports, and replay material

## Required Run Identity

Every run package must carry:

- `run_id`
- `source_system` (`dexter` or `mewx`)
- `source_commit`
- `mode` (`observe_live`, `paper_live`, `trade_live`, `sim_live`, `replay`)
- `transport_mode` (`ws`, `grpc`, `rpc`, `swqos`, or `mixed`)
- `host_role` (`windows_runtime`)
- `runtime_root`
- `started_at_utc`
- `ended_at_utc`

## Profitability Decision Gates

Profitability is only considered confirmed when all of the following are available:

- candidate precision and candidate coverage proxies
- entry latency, fillability, and slippage measurements
- session MFE, MAE, and time-to-peak
- realized vs theoretical exit gap
- stale-position and failed-exit incidence
- capital efficiency under concurrent-session pressure
- replay feasibility with enough state to reproduce the decision path

## Readiness States

- `observe_only`: event coverage is incomplete; no fair comparison yet
- `comparable`: both sources emit the contract and metrics are directly comparable
- `profitable_candidate`: one source or component shows repeatable edge on the catalog
- `integration_ready`: winning component also meets observability, replay, and operational safety requirements
