# TASK-007 Live-Paper Observability Shift Handoff Watchdog Regression-Pack Report

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#67` main commit `7ab737a306ceca06193044d384e6b17d371838e2` on `2026-03-26T21:34:46Z`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Open Vexter PR `#50` remained non-authoritative relative to merged `main`.

## What This Task Did

- Started from the merged handoff-watchdog-runtime lane on PR `#67` and kept the promoted comparison baseline frozen.
- Added a dedicated handoff-watchdog regression-pack lane so future handoff-facing changes must preserve the fixed watchdog surface across the baseline handoff, runtime follow-up handoff, and current regression-pack handoff.
- Locked required-face omission, pointer shrinkage or ambiguity, implicit carry-over, omission / drift / partial_visibility completeness, manual stop-all visibility, quarantine visibility, terminal snapshot visibility, normalized failure detail visibility, open questions, and next-shift priority checks into durable assertions.
- Preserved the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam without changing source logic, trust logic, thresholds, validator rules, or frozen source pins.

## Validation

- `pytest -q -m livepaper_observability_shift_handoff_watchdog_regression_pack tests/test_planner_router_transport_livepaper_observability_shift_handoff_watchdog_regression_pack.py`
- `25 passed in 0.05s`

## Recommendation Among Next Tasks

### `livepaper_observability_shift_handoff_watchdog_ci_gate`

Recommended next because:

- this task already packages the baseline and runtime handoff-watchdog conclusions into a durable regression surface
- the remaining risk is making that surface run on every handoff-facing change, not discovering a new face
- a dedicated CI gate operationalizes the pack without reopening comparison or changing source logic

### `transport_livepaper_observability_acceptance_pack`

Not recommended now because:

- it would mostly repackage already-fixed operator-facing artifacts instead of increasing regression durability
- the sharper risk-reduction step is an always-on handoff-watchdog CI gate

### `executor_boundary_code_spec`

Not recommended now because:

- no new executor boundary ambiguity surfaced while packaging the handoff watchdog surface
- the remaining work is preserving the existing fixed contract rather than redefining it

## Decision

- Outcome: `A`
- Key finding: `livepaper_observability_shift_handoff_watchdog_regression_pack_durable`
- Claim boundary: `livepaper_observability_shift_handoff_watchdog_regression_pack_bounded`
- Current task status: `livepaper_observability_shift_handoff_watchdog_regression_pack_passed`
- Recommended next step: `livepaper_observability_shift_handoff_watchdog_ci_gate`
- Decision: `livepaper_observability_shift_handoff_watchdog_ci_gate_ready`

## Key Paths

- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- Canonical runbook: `docs/livepaper_observability_operator_runbook.md`
- Canonical checklist: `docs/livepaper_observability_shift_checklist.md`
- Canonical handoff template: `docs/livepaper_observability_shift_handoff_template.md`
- Canonical handoff drill: `docs/livepaper_observability_shift_handoff_drill.md`
- Baseline handoff watchdog proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-check.json`
- Runtime handoff watchdog proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-runtime-check.json`
- Regression-pack handoff: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack/HANDOFF.md`
- Regression-pack report: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-report.md`
- Regression-pack status: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-status.md`
- Regression-pack proof: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-check.json`
- Regression-pack summary: `artifacts/proofs/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack-summary.md`
- Regression-pack prompt pack: `artifacts/reports/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack`
- Regression-pack bundle: `artifacts/bundles/task-007-livepaper-observability-shift-handoff-watchdog-regression-pack.tar.gz`
