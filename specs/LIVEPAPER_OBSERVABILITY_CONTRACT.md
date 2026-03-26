# Live-Paper Observability Contract

## Purpose

This document is the bounded operator-facing contract for executor transport observability on the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.
It does not introduce new runtime behavior.
It codifies the surfaces already locked by:

- `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-check.json`
- `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-runtime-check.json`
- `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-regression-pack-check.json`
- `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json`

## Fixed Inputs

- Vexter merged `main`: PR `#58`, merge commit `10e23faa2a2428abae8206df963889392840919c`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Global halt mode: `manual_latched_stop_all`
- Status delivery model: `poll_first`

## Canonical Surfaces

The live-paper observability contract is bounded to these nine watchdog surfaces:

- `required_observability_field_omission`
- `handle_lifecycle_continuity`
- `planned_runtime_metadata_drift`
- `partial_status_sink_fan_in`
- `ack_history_retention`
- `quarantine_reason_completeness`
- `manual_stop_all_propagation`
- `snapshot_backed_terminal_detail`
- `normalized_failure_detail_passthrough`

## Required Fields

### Handle metadata

Every prepared handle must keep these required keys visible in `DispatchHandle.native_handle`:

- `transport_version`, `handle_id`, `ack_state`, `entrypoint`, `executor_profile_id`, `pinned_commit`, `status_delivery`, `prepared_at_utc`
- `native_session_id`, `execution_mode`, `startup_method`, `plan_batch_id`, `objective_profile_id`, `source`, `selected_sleeve_id`
- `monitor_profile_id`, `timeout_envelope_class`, `quarantine_scope`, `global_halt_participation`
- `prepare_ack_state`, `prepare_accepted_once`, `prepare_duplicate_seen`, `prepare_request_count`
- `start_ack_state`, `start_accepted_once`, `start_duplicate_seen`, `start_terminal_seen`, `start_request_count`
- `stop_ack_state`, `stop_accepted_once`, `stop_duplicate_seen`, `stop_terminal_seen`, `stop_request_count`
- `last_reported_status`

### Runtime snapshot detail

Every runtime `StatusSnapshot.detail` must keep these required keys visible:

- `handle_id`, `native_session_id`, `transport_version`, `signal`, `prepared_at_utc`
- `entrypoint`, `execution_mode`, `startup_method`, `status_delivery`, `ack_state`
- `plan_batch_id`, `objective_profile_id`, `source`, `selected_sleeve_id`
- `monitor_profile_id`, `timeout_envelope_class`, `quarantine_scope`, `global_halt_participation`
- `executor_profile_id`, `pinned_commit`
- `prepare_ack_state`, `prepare_accepted_once`, `prepare_duplicate_seen`, `prepare_request_count`
- `start_ack_state`, `start_accepted_once`, `start_duplicate_seen`, `start_terminal_seen`, `start_request_count`
- `stop_ack_state`, `stop_accepted_once`, `stop_duplicate_seen`, `stop_terminal_seen`, `stop_request_count`
- `last_reported_status`

For `running`, `quarantined`, `stopping`, `stopped`, and `failed` snapshots, lifecycle visibility fields must also remain visible:

- `sequence`
- `poll_counter`
- `snapshot_counter`
- `executor_status`
- `started`
- `stop_requested`
- `stop_confirmed`
- `duplicate`

### Failure and rollback detail

A failed runtime snapshot must also carry:

- `failure_code`
- `stage`
- `rollback_confirmed`
- `rollback_confirmation_source`
- `rollback_snapshot`

The normalized `FailureDetail` envelope must carry:

- `code`
- `stage`
- `plan_id`
- `source`
- `source_reason`
- `detail`

The nested failure `detail` mapping must carry:

- `plan_id`
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
- `entrypoint`
- `execution_mode`
- `startup_method`
- `handle_id`
- `transport_version`

When `rollback_confirmed` is true, `rollback_snapshot` must at least carry:

- `execution_mode`
- `monitor_profile_id`
- `executor_profile_id`
- `pinned_commit`
- `stop_reason`

### Ack-history retention

The latest visible detail across handle, runtime snapshots, terminal snapshot, and failure detail must retain:

- `prepare_ack_state`, `prepare_accepted_once`, `prepare_duplicate_seen`, `prepare_request_count`
- `start_ack_state`, `start_accepted_once`, `start_duplicate_seen`, `start_terminal_seen`, `start_request_count`
- `stop_ack_state`, `stop_accepted_once`, `stop_duplicate_seen`, `stop_terminal_seen`, `stop_request_count`

Ack-history rules are fixed now:

- `prepare_request_count`, `start_request_count`, and `stop_request_count` are monotonic.
- Sticky booleans never collapse from `true` back to `false`.
- If a request count rises above `1`, duplicate-or-terminal visibility must remain visible.
- Duplicate visibility requirements are:
  - `prepare_request_count` -> `prepare_duplicate_seen`
  - `start_request_count` -> `start_duplicate_seen` or `start_terminal_seen`
  - `stop_request_count` -> `stop_duplicate_seen` or `stop_terminal_seen`

## Lifecycle Semantics

### Status surface

The public lifecycle remains:

- `planned`
- `starting`
- `running`
- `quarantined`
- `stopping`
- `stopped`
- `failed`

### Identity continuity

The following identity fields must stay continuous across handle, runtime snapshots, sink snapshots, terminal snapshot, nested failure detail, and rollback snapshot:

- `handle_id`
- `native_session_id`

### Planned-runtime continuity

The watchdog surface treats the planned envelope as authoritative for these fields:

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

Drift on those fields is a contract failure even if the runtime appears functionally healthy.

### Status sink fan-in

The status sink is a required fan-in view, not a best-effort mirror.

Rules fixed now:

- sink sequence must match the runtime sequence exactly by `plan_id`, normalized `status`, `source_reason`, and `signal`
- sink detail must not omit required runtime keys that remain visible in the runtime snapshot
- `poll_confirmed_by_push` is a valid reconciliation decision
- `push_promoted` is a valid reconciliation decision when the pushed status is the stronger valid state

### Quarantine

For every quarantined runtime surface:

- `quarantine_reason` must stay visible either on the runtime detail or the promoted push detail
- the same surface must retain plan, monitor, executor, and ack-history continuity

### Manual stop-all

When manual stop-all is visible, the normalized semantics are fixed now:

- `halt_mode` must be `manual_latched_stop_all`
- propagation remains reverse-order stop fanout across active plans
- `stop_reason` must stay visible
- `trigger_plan_id` must stay visible
- `stop_requested` and `stop_confirmed` must stay visible on terminal failure paths

### Terminal detail

Operator-facing terminal detail is snapshot-backed only.

Rules fixed now:

- terminal detail must be present for plans with runtime observations
- terminal detail must carry the runtime required fields
- terminal detail `signal` must be `snapshot`
- terminal detail must retain `stop_reason`

## Failure Reporting Semantics

The watchdog finding severities are fixed now:

- `omission`: a required field or required surface is missing
- `drift`: a required field is present but no longer matches the planned source-faithful envelope
- `partial_visibility`: the lifecycle happened, but the operator-facing surface did not preserve all required detail

Normalized failure passthrough rules are fixed now:

- planner-owned `code` and `stage` remain normalized
- source-native `source_reason` remains passthrough metadata
- failure detail may add rollback evidence, but it may not rewrite source-strategy semantics
- a rollback-confirmed failure must surface `rollback_snapshot`

## Proof and Report Outputs

A complete live-paper observability spec handoff consists of:

- `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- `artifacts/reports/task-007-livepaper-observability-spec-report.md`
- `artifacts/reports/task-007-livepaper-observability-spec-status.md`
- `artifacts/reports/task-007-livepaper-observability-spec/DETAILS.md`
- `artifacts/reports/task-007-livepaper-observability-spec/MIN_PROMPT.txt`
- `artifacts/reports/task-007-livepaper-observability-spec/CONTEXT.json`
- `artifacts/proofs/task-007-livepaper-observability-spec-check.json`
- `artifacts/proofs/task-007-livepaper-observability-spec-summary.md`
- `artifacts/bundles/task-007-livepaper-observability-spec.tar.gz`

## Operator-Facing Interpretation

Use the contract in this order:

1. Start with the watchdog CI gate. If it is green, the required surface is still present in standard validation.
2. Read the failing watchdog surface name before reading individual snapshots. The surface name is the shortest explanation of what visibility contract broke.
3. Treat `omission` as missing evidence, `drift` as mismatched identity or metadata, and `partial_visibility` as an incomplete operator surface.
4. For terminal or failure triage, prefer snapshot-backed terminal detail and normalized failure detail over ad hoc sink snippets.
5. For stop-all incidents, confirm peer-plan propagation before treating a single-plan failure as isolated.

## Bounded Troubleshooting Expectations

This contract is intentionally bounded.
It does not authorize:

- source logic changes in Dexter or Mew-X
- validator rule changes
- comparison baseline reopen
- funded live trading
- threshold transplant
- trust-logic transplant
- new evidence collection in place of reading the fixed proof outputs

The operator response expected from this contract is limited to visibility triage:

- confirm which watchdog surface failed
- confirm whether the failure is omission, drift, or partial visibility
- identify the first surface where required fields stopped being continuous
- hand off source or transport remediation only after the visibility break is localized
