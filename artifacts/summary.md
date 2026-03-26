# TASK-007-LIVEPAPER-OBSERVABILITY-SPEC Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#58` main commit `10e23faa2a2428abae8206df963889392840919c` on `2026-03-26T16:29:07Z`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Open Vexter PR `#50` (`feat(infra): refresh runtime observability artifacts`) remained non-authoritative relative to merged `main`.

## What This Task Did

- Treated the watchdog CI gate, watchdog, watchdog-runtime, and watchdog-regression-pack outputs as the formal live-paper observability baseline without reopening comparison work.
- Wrote one bounded observability contract for the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam in `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`.
- Fixed required fields, lifecycle continuity, failure-reporting semantics, proof outputs, and operator-facing interpretation around immutable handoff metadata, handle continuity, planned/runtime metadata continuity, status sink fan-in, ack-history retention, quarantine completeness, manual stop-all propagation, snapshot-backed terminal detail, and normalized failure-detail passthrough.
- Refreshed tests, summary, context pack, proof manifest, task ledger, report, proof output, and handoff bundle without changing planner/router source logic or collecting new evidence.

## Fixed Observability Contract

- The live-paper observability surface remains bounded to the nine watchdog faces already enforced in CI.
- The required field sets are now explicit for handle metadata, runtime snapshots, failed runtime snapshots, normalized failure envelopes, rollback snapshots, and ack-history retention.
- Operator interpretation is now fixed: `omission` means required evidence disappeared, `drift` means planned-versus-runtime identity or metadata no longer match, and `partial_visibility` means the lifecycle happened but the operator-facing surface lost required detail.

## Decision

- Outcome: `A`
- Key finding: `livepaper_observability_contract_fixed`
- Claim boundary: `livepaper_observability_spec_bounded`
- Current task status: `livepaper_observability_spec_ready`
- Recommended next step: `livepaper_observability_operator_runbook`
- Decision: `livepaper_observability_operator_runbook_ready`

## Key Paths

- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- Live-paper observability spec report: `artifacts/reports/task-007-livepaper-observability-spec-report.md`
- Live-paper observability spec status: `artifacts/reports/task-007-livepaper-observability-spec-status.md`
- Live-paper observability spec proof: `artifacts/proofs/task-007-livepaper-observability-spec-check.json`
- Live-paper observability spec summary: `artifacts/proofs/task-007-livepaper-observability-spec-summary.md`
- Live-paper observability spec prompt pack: `artifacts/reports/task-007-livepaper-observability-spec`
- Live-paper observability spec bundle: `artifacts/bundles/task-007-livepaper-observability-spec.tar.gz`
