# Live-Paper Observability Operator Runbook

## Purpose

This runbook turns the fixed live-paper observability contract into a bounded operator workflow for the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.
It does not authorize source changes, new evidence collection, or comparison-baseline reopen.

## Fixed Inputs

- Vexter merged `main`: PR `#59`, merge commit `4be21e4e52fbe686e585dea6b573efea759e0933`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- Fixed halt mode: `manual_latched_stop_all`
- Fixed status delivery: `poll_first`

## Operator Meanings

- `omission`: a required field or required surface is missing.
- `drift`: a required field is present but no longer matches the planned source-faithful envelope.
- `partial_visibility`: the lifecycle happened, but the operator-facing surface did not preserve all required detail.

## First-Check Order

1. Start with `artifacts/reports/task-007-livepaper-observability-operator-runbook-status.md`.
   Use it to confirm the current task state, current decision, and current next-step recommendation.
2. Read `artifacts/reports/task-007-livepaper-observability-operator-runbook-report.md`.
   Use it to recover the fixed inputs, bounded scope, lookup order, and escalation rules before opening raw proofs.
3. Read `artifacts/proofs/task-007-livepaper-observability-operator-runbook-summary.md`.
   Use it for the shortest evidence trail and to confirm the frozen pins and next step quickly.
4. Read `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`.
   Use it for exact field names, lifecycle continuity rules, and failure semantics.
5. Read `artifacts/proofs/task-007-livepaper-observability-operator-runbook-check.json`.
   Use it for structured lookup order, surface priority, and machine-readable task result fields.
6. Drill into upstream proofs only after the contract and runbook are clear.
   Read them in this order:
   - `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json`
   - `artifacts/proofs/task-007-livepaper-observability-spec-check.json`
   - `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json`
   - `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-regression-pack-check.json`
   - `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-check.json`

## Failure-Surface Priority

### Priority 0: Containment and halt confidence

Check these first because they determine whether the operator can trust the containment story:

- `manual_stop_all_propagation`
- `quarantine_reason_completeness`
- `snapshot_backed_terminal_detail`
- `normalized_failure_detail_passthrough`

If any of these surfaces fail, keep the plan stopped or quarantined and do not treat the incident as closed.

### Priority 1: Identity and planned-runtime integrity

Check these next because they determine whether the operator can still trust planned-versus-runtime identity:

- `planned_runtime_metadata_drift`
- `handle_lifecycle_continuity`
- `required_observability_field_omission`

If these surfaces fail, do not continue or resume based on downstream summaries alone.

### Priority 2: Visibility quality after containment

Check these after containment and identity are still intact:

- `partial_status_sink_fan_in`
- `ack_history_retention`

If these surfaces fail while containment is still visible, keep the plan contained and inspect more deeply before resuming any workflow.

## Triage Flow

### `omission`

1. Identify the missing surface name from the watchdog CI gate or runbook proof.
2. Compare the missing field against the contract's required field group:
   - handle metadata
   - runtime snapshot detail
   - failed runtime snapshot detail
   - failure envelope
   - nested failure detail
   - rollback snapshot
   - ack-history retention
3. If the missing field is on a halt, quarantine, terminal, or failure surface, treat it as a Priority 0 incident.
4. If the field is missing only from the sink while runtime or terminal snapshots still retain it, reclassify the break as `partial_visibility`.

### `drift`

1. Compare the planned envelope and runtime-visible envelope for:
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
2. Confirm whether `handle_id` and `native_session_id` still remain continuous across handle, runtime, sink, terminal, and failure surfaces.
3. Treat visible-but-mismatched fields as `drift`, even when the runtime appears functionally healthy.

### `partial_visibility`

1. Confirm that the lifecycle progressed and that runtime or terminal surfaces still exist.
2. Check whether the sink or follow-up snapshots lost fields that remain required under the contract.
3. Use raw sink and runtime proofs to localize where the detail disappeared.
4. Keep the plan contained while triaging; `partial_visibility` is not a reason to ignore a containment surface.

## Ack History Interpretation

- `prepare_request_count`, `start_request_count`, and `stop_request_count` must be monotonic.
- Sticky booleans must not collapse from `true` back to `false`.
- If a request count rises above `1`, duplicate-or-terminal visibility must remain visible.
- When counts rise but the corresponding duplicate or terminal flags disappear, treat the break as `partial_visibility` or `omission`.

## Operational Decision Rules

### Manual stop-all

- Treat `manual_latched_stop_all` as a propagation event, not as an isolated plan failure.
- Confirm `halt_mode`, `trigger_plan_id`, `stop_reason`, `stop_requested`, and `stop_confirmed`.
- Confirm reverse-order stop fanout across peer plans before localizing blame to one plan.

### Quarantine

- Treat quarantine as a containment surface, not just a status label.
- Require `quarantine_reason` together with plan identity, monitor identity, executor identity, and ack history.
- If `quarantine_reason` is missing, keep the plan quarantined and escalate as an observability break.

### Terminal snapshot

- Prefer snapshot-backed terminal detail.
- Require `signal=snapshot` before treating a terminal surface as authoritative.
- Use the terminal snapshot as the closing operator record only when required runtime continuity fields and `stop_reason` remain visible.

### Normalized failure detail

- Route first on normalized `code`, `stage`, `plan_id`, and `source`.
- Preserve `source_reason` as passthrough source metadata.
- Use nested `detail` to confirm plan, monitor, executor, transport, and source continuity.
- If `rollback_confirmed` is true, require `rollback_snapshot` before closing the incident.

## Halt, Continue, Inspect

- Halt and escalate when containment surfaces fail, planned/runtime identity drifts, terminal detail is not snapshot-backed, or normalized failure detail loses its identity chain.
- Continue only in a contained state when quarantine reason, stop propagation, terminal snapshot, and failure detail remain visible and coherent.
- Inspect more deeply when the main break is sink fan-in loss or ack-history loss but the containment story is still intact.

## Bounded Non-Goals

- source logic changes in Dexter or Mew-X
- validator rule changes
- comparison baseline reopen
- new evidence collection
- funded live trading
- trust-logic or threshold transplant work
