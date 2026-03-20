# Vexter Detailed Analysis and Development Plan

## Phase 0 - Bootstrap the mothership
Create `Cabbala/Vexter` and local Mac control folder `~/Projects/Vexter`.
Set up docs/specs/scripts/artifacts layout.
Add Windows runtime bootstrap scripts and placeholders.

## Phase 1 - Environment discovery and runtime placement
From Mac control plane, use `ssh win-lan` to:
- discover best Windows workspace root
- create Vexter runtime directories
- prepare Docker-compatible workspace skeleton
- document chosen paths in committed manifests

Suggested Windows layout:
- `Vexter/runtime/dexter/`
- `Vexter/runtime/mewx/`
- `Vexter/runtime/unified/`
- `Vexter/data/postgres/`
- `Vexter/data/logs/`
- `Vexter/data/replays/`
- `Vexter/data/raw/`

## Phase 2 - Dexter deep source assessment
Assess:
- setup/runtime assumptions
- DB schema and init flow
- websocket / Helius ingestion path
- leaderboard/trust-factor creation path
- session monitoring / exit logic
- what needs instrumentation for profitability analysis

Expected strong modules:
- creator scoring / trust factor
- session adaptive exit
- reserved balance logic

## Phase 3 - Mew-X deep source assessment
Assess:
- Rust build/runtime assumptions
- transport / gRPC / websocket modes
- creator source selection and filters
- execution substrate and risk controls
- what needs instrumentation for profitability analysis

Expected strong modules:
- candidate source diversity
- execution and transport abstraction
- portfolio-level caps and pre-entry filters

## Phase 4 - Comparison tooling
Build report generators that compare Dexter and Mew-X outputs using the common analysis contract.

## Phase 5 - Integration spec
Only after evidence is available, write minimal integration spec:
- Mew-X substrate + Dexter creator scoring + Dexter adaptive exit + shared normalized telemetry

## Phase 6 - Minimal unified implementation
Implement only winning components inside Vexter.
