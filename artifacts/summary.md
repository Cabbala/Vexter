# TASK-001 Source Assessment Summary

## Outcome

- Verified that `main` and `codex/task-000-bootstrap` both point to commit `6d22d22e37a77e2e15c6211d32c125c8c4a2c151`.
- Assessed Dexter and Mew-X at the file and function level before any integration-bot implementation.
- Added the shared evaluation contract, normalized event schema, metrics catalog, comparison template, and per-source instrumentation plans.
- Verified the Windows runtime root through `ssh win-lan` and fixed a concrete separation plan for runtime, logs, raw events, replay material, and DB volumes.

## Key Findings

- Dexter already has useful replay seed data in PostgreSQL, but its live decision path is under-instrumented.
- Mew-X has the stronger candidate and execution substrate, but it still lacks analysis-grade event attribution.
- Profitability confirmation requires normalized evidence for candidate precision, entry latency, slippage, session excursions, realized-vs-theoretical exit gap, stale-position risk, and capital efficiency.

## Key Artifacts

- `docs/evaluation_contract.md`
- `docs/normalized_event_schema.md`
- `docs/metrics_catalog.md`
- `docs/comparison_matrix_template.md`
- `docs/dexter_source_assessment.md`
- `docs/mewx_source_assessment.md`
- `plans/dexter_instrumentation_plan.md`
- `plans/mewx_instrumentation_plan.md`
- `plans/integration_readiness_plan.md`
- `artifacts/context_pack.json`
- `artifacts/proof_bundle_manifest.json`

## Git Visibility

- GitHub repo: `https://github.com/Cabbala/Vexter`
- Working branch: `codex/task-001-source-assessment`
