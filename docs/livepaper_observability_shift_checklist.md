# Live-Paper Observability Shift Checklist

## Purpose

This checklist turns the fixed live-paper observability contract and operator runbook into one bounded shift-by-shift procedure for the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.
It does not authorize source changes, new evidence collection, comparison-baseline reopen, or funded live trading.

## Fixed Inputs

- Vexter merged `main`: PR `#60`, merge commit `ec46f051b41c3e140db09e808ef54e4d6e3d33ac`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- Canonical runbook: `docs/livepaper_observability_operator_runbook.md`
- Fixed halt mode: `manual_latched_stop_all`
- Fixed status delivery: `poll_first`

## Artifact Entry Order

1. Start with `artifacts/reports/task-007-livepaper-observability-shift-checklist-status.md`.
   Use it to confirm the current lane state, current decision, and current next-step recommendation before opening deeper evidence.
2. Read `artifacts/reports/task-007-livepaper-observability-shift-checklist-report.md`.
   Use it to recover the fixed inputs, shift phases, lookup order, and decision mapping.
3. Read `artifacts/proofs/task-007-livepaper-observability-shift-checklist-summary.md`.
   Use it for the shortest evidence trail and the current recommendation.
4. Read `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`.
   Use it for exact field names, continuity requirements, and failure semantics.
5. Read `artifacts/proofs/task-007-livepaper-observability-shift-checklist-check.json`.
   Use it for the machine-readable checklist shape, action mapping, and task result fields.
6. Open upstream proofs only after the checklist context is clear.
   Read them in this order:
   - `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json`
   - `artifacts/proofs/task-007-livepaper-observability-spec-check.json`
   - `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json`
   - `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-regression-pack-check.json`
   - `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-check.json`

## Pre-Shift Checklist

1. Confirm the fixed pins and frozen task inputs from the checklist status, report, and summary.
   - Required matches: Vexter PR `#60`, Dexter PR `#3`, frozen Mew-X commit, promoted baseline, `comparison_closed_out`, `manual_latched_stop_all`, and `poll_first`.
   - If those artifacts disagree, do not start the shift as normal. Halt the shift start and escalate before opening deeper proofs.
2. Confirm the operator vocabulary remains fixed now:
   - `omission`
   - `drift`
   - `partial_visibility`
3. Confirm the active bounded surface set is still the same nine watchdog surfaces from the contract and runbook.
4. Confirm the first deep proof remains the watchdog CI gate, not individual snapshots.
5. Confirm containment-first priority before any sink-quality review:
   - `manual_stop_all_propagation`
   - `quarantine_reason_completeness`
   - `snapshot_backed_terminal_detail`
   - `normalized_failure_detail_passthrough`
6. Confirm the source-faithful seam is still Dexter `paper_live` with frozen Mew-X `sim_live`.

## During-Shift Periodic Checks

1. Start from the currently failing watchdog surface name before drilling into snapshots.
2. Check containment-first surfaces before identity or sink quality.
   - If `manual_latched_stop_all` is visible, confirm `halt_mode`, `trigger_plan_id`, `stop_reason`, `stop_requested`, and `stop_confirmed`, then confirm reverse-order stop fanout across peer plans.
   - If quarantine is visible, require `quarantine_reason` together with plan, monitor, executor, and ack-history continuity.
   - For terminal or failed paths, prefer snapshot-backed terminal detail and normalized failure detail over sink snippets.
3. Check identity continuity on `handle_id` and `native_session_id` across handle, runtime, sink, terminal, and failure surfaces.
4. Check planned-versus-runtime integrity for the fixed planned envelope fields:
   - `transport_version`
   - `entrypoint`
   - `execution_mode`
   - `startup_method`
   - `status_delivery`
   - `plan_batch_id`
   - `objective_profile_id`
   - `source`
   - `selected_sleeve_id`
   - `monitor_profile_id`
   - `timeout_envelope_class`
   - `quarantine_scope`
   - `global_halt_participation`
   - `executor_profile_id`
   - `pinned_commit`
5. Check ack history on every visible lifecycle surface.
   - `prepare_request_count`, `start_request_count`, and `stop_request_count` must remain monotonic.
   - Sticky booleans must not collapse from `true` back to `false`.
   - If a request count rises above `1`, duplicate-or-terminal visibility must remain visible.
6. Check sink fan-in only after containment and identity are still coherent.
   - If sink detail loses fields that remain visible in runtime or terminal snapshots, treat that loss as `partial_visibility`, not a clean incident close.

## Incident Branching

### `omission`

1. Name the missing surface or field from the watchdog CI gate or the checklist proof.
2. Compare it against the contract field groups:
   - handle metadata
   - runtime snapshot detail
   - failed runtime snapshot detail
   - failure envelope
   - nested failure detail
   - rollback snapshot
   - ack-history retention
3. If the missing field is on a halt, quarantine, terminal, or failure surface, map it directly to `halt`.
4. If the field is missing only from the sink while runtime or terminal surfaces still retain it, reclassify the break as `partial_visibility` and map it to `quarantine`.

### `drift`

1. Compare the planned envelope with the runtime-visible envelope for every planned-runtime anchor field.
2. Confirm `handle_id` and `native_session_id` still remain continuous across handle, runtime, sink, terminal, and failure surfaces.
3. Treat any visible-but-mismatched planned field or identity chain as `drift`.
4. Map `drift` directly to `halt`. Do not resume based on downstream summaries alone.

### `partial_visibility`

1. Confirm the lifecycle progressed and that runtime or terminal surfaces still exist.
2. Localize where the detail disappeared by comparing runtime and sink proofs.
3. Keep the plan contained while triaging.
4. Map `partial_visibility` to `quarantine` by default.
5. `continue` is allowed only in a contained state when quarantine reason, stop propagation, snapshot-backed terminal detail, and normalized failure detail remain coherent.

## Halt, Quarantine, Continue

- `halt`
  - containment surfaces fail
  - planned/runtime identity drifts
  - terminal detail is not snapshot-backed
  - normalized failure detail loses identity continuity
  - shift-start fixed inputs disagree across status, report, or proof
- `quarantine`
  - sink-only omission is reclassified as `partial_visibility`
  - ack-history detail becomes incomplete while containment remains intact
  - sink fan-in loses required detail while runtime and terminal still retain it
  - `quarantine_reason` is missing or peer-plan stop propagation is not yet visible
- `continue`
  - only after status, report, summary, contract, and proof stay aligned
  - only when no unresolved `omission` or `drift` remains
  - only in contained state if the incident is still open; record this explicitly as continuing in containment rather than closing the incident

## End-of-Shift Checklist

1. Re-open the current checklist status, report, proof summary, and proof JSON in that order.
2. Record the shift outcome as one of:
   - `contained`
   - `escalated`
   - `closed`
3. Record the exact broken surface and classification, if any:
   - surface name
   - `omission`, `drift`, or `partial_visibility`
   - `halt`, `quarantine`, or `continue`
4. Record the shortest proof trail that supports the shift decision.
5. Record the next reader entry point:
   - current status path
   - current report path
   - first deep proof to open next if the incident remains active
6. Confirm no new evidence collection, source changes, validator-rule changes, or comparison-baseline reopen happened during the shift.
7. Hand off unresolved incidents with the pinned commits, promoted baseline, containment state, and next proof entry point unchanged.

## Bounded Non-Goals

- Dexter or Mew-X source logic changes
- validator-rule changes
- comparison-baseline reopen
- new evidence collection
- funded live trading
- trust-logic, threshold, or transport-boundary redesign
