# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE

## 1. Purpose
Promote the locked watchdog, watchdog-runtime, and watchdog-regression-pack observability surface into an always-on CI gate on the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.

## 2. Fixed Inputs
- Latest merged Vexter `main`: PR `#57` commit `8368b545c3ef3c32db9843ac7e958528902fe67c`
- Dexter merged `main`: PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`

## 3. Required Gate Surfaces
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
- `livepaper_observability_spec`
