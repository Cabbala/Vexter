# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-REGRESSION-PACK

## 1. Purpose
Freeze the watchdog and watchdog-runtime drift / omission / partial-visibility surface into durable regression coverage on top of the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.

## 2. Fixed Inputs
- Latest merged Vexter `main`: PR `#56` commit `cc8996e0204b7dd149ebce85f1988d7a3abf90cd`
- Dexter merged `main`: PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`

## 3. Required Regression Surfaces
- immutable handoff metadata continuity
- handle lifecycle continuity
- planned/runtime metadata drift detection
- status sink fan-in detection
- ack-history retention
- quarantine reason completeness
- reverse-order `manual_latched_stop_all` propagation
- snapshot-backed terminal detail completeness
- normalized failure-detail passthrough

## 4. Constraints
- no source logic changes
- no validator rule changes
- no comparison baseline reopen
- no new evidence collection
- keep source-faithful Dexter `paper_live` / Mew-X `sim_live` seam

## 5. Recommended Next Task
- `transport_livepaper_observability_watchdog_ci_gate`
