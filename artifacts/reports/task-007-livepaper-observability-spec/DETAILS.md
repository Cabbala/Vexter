# TASK-007-LIVEPAPER-OBSERVABILITY-SPEC

## 1. Purpose

Convert the already-CI-gated live-paper observability surface into one operator-facing bounded spec for the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.

## 2. Fixed Inputs

- Latest merged Vexter `main`: PR `#58` commit `10e23faa2a2428abae8206df963889392840919c`
- Dexter merged `main`: PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`

## 3. Mandatory Contract Surfaces

- immutable handoff metadata continuity
- handle lifecycle continuity
- planned/runtime metadata continuity
- status sink fan-in
- ack-history retention
- quarantine reason completeness
- reverse-order `manual_latched_stop_all` propagation
- snapshot-backed terminal detail
- normalized failure-detail passthrough

## 4. Constraints

- no source logic changes
- no validator rule changes
- no comparison baseline reopen
- no new evidence collection
- keep source-faithful Dexter `paper_live` / Mew-X `sim_live` seam

## 5. Recommended Next Task

- `livepaper_observability_operator_runbook`
