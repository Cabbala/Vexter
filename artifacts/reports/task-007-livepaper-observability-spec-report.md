# TASK-007 Live-Paper Observability Spec Report

## Scope

This task starts from merged PR `#58` and the completed `TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-CI-GATE` lane.
It keeps the promoted comparison baseline frozen and asks one bounded contract question:

- Given the already-CI-gated watchdog surface, what single operator-facing live-paper observability contract can be fixed now without reopening comparison work, changing source logic, or recollecting evidence?

The task stays intentionally narrow:

- no new evidence collection
- no Dexter or Mew-X source changes
- no validator-rule changes
- no comparison baseline reopen
- no executor transport redesign
- only live-paper observability contract definition, contract tests, and refreshed task artifacts/bundle

## Verified GitHub State

- Latest merged Vexter `main`: PR `#58`, main commit `10e23faa2a2428abae8206df963889392840919c`, merged at `2026-03-26T16:29:07Z`
- Open non-authoritative Vexter PR: `#50`, `feat(infra): refresh runtime observability artifacts`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Prior lane source of truth: `artifacts/reports/task-007-transport-livepaper-observability-watchdog-ci-gate-report.md`
- Prior lane proof: `artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json`
- Existing watchdog suite proofs stay authoritative for runtime visibility and failure mapping
- Source-faithful seam remains Dexter `paper_live` and frozen Mew-X `sim_live`

Facts preserved from the watchdog lane:

- live winner mode: `derived`
- replay winner mode: `derived`
- stable scored split: Dexter `6`, Mew-X `4`, tie `2`
- default execution anchor: `Dexter`
- selective option source: `Mew-X`
- public status lifecycle stays `planned -> starting -> running -> quarantined -> stopping -> stopped|failed`
- global halt mode stays `manual_latched_stop_all`

## What Landed

### One bounded observability contract

The contract is now fixed in `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`.
It is not a new runtime lane.
It is the operator-facing definition of the already-proven surface enforced by:

- watchdog
- watchdog-runtime
- watchdog-regression-pack
- watchdog CI gate

### Required surfaces

The live-paper observability surface remains bounded to these nine faces:

- `required_observability_field_omission`
- `handle_lifecycle_continuity`
- `planned_runtime_metadata_drift`
- `partial_status_sink_fan_in`
- `ack_history_retention`
- `quarantine_reason_completeness`
- `manual_stop_all_propagation`
- `snapshot_backed_terminal_detail`
- `normalized_failure_detail_passthrough`

### Required fields

The contract now names the exact required field groups for:

- handle metadata
- runtime snapshot detail
- failed runtime snapshot detail
- normalized failure envelopes
- nested failure passthrough detail
- rollback snapshots
- ack-history retention, monotonic counts, sticky flags, and duplicate visibility

The fixed consequence is explicit:

- immutable handoff metadata must remain visible past prepare
- handle identifiers must stay continuous across handle, runtime, sink, terminal, and failure surfaces
- planned metadata must still match runtime metadata on the source-faithful seam
- sink fan-in must remain lossless relative to runtime snapshots

### Lifecycle semantics

The contract now states operator-visible lifecycle rules instead of leaving them implicit in tests:

- `handle_id` and `native_session_id` are the continuity identifiers
- `transport_version`, `entrypoint`, `execution_mode`, `startup_method`, `status_delivery`, plan identity, monitor identity, and executor identity stay anchored to the planned envelope
- `poll_confirmed_by_push` and `push_promoted` are valid reconciliation outcomes, but they may not drop required fields
- quarantine must keep `quarantine_reason`
- manual stop-all must keep `halt_mode=manual_latched_stop_all`, `stop_reason`, `trigger_plan_id`, and peer-plan propagation visibility
- terminal detail is valid only when backed by `signal=snapshot`

### Failure reporting

The operator-facing meanings are fixed now:

- `omission`: required evidence is missing
- `drift`: required evidence exists but no longer matches the planned source-faithful envelope
- `partial_visibility`: lifecycle progressed, but the operator surface lost required detail

Normalized failure passthrough remains bounded:

- planner-owned `code` and `stage` stay normalized
- source-native `source_reason` remains passthrough metadata
- rollback-confirmed failures must keep a rollback snapshot with source-faithful monitor and executor identity

### Proof and report outputs

The contract now fixes the required outputs for this lane:

- canonical spec file
- report
- status summary
- prompt pack
- machine-readable proof
- proof summary
- bundle

## What Did Not Change

- No planner/router source logic changed.
- No Dexter or Mew-X behavior changed.
- No validator rules changed.
- No comparison evidence was recollected.
- No CI or watchdog surface was reopened or redefined beyond documentation of the existing contract.

## Tests

Contract coverage now includes:

- `tests/test_planner_router_transport_livepaper_observability_spec_contract.py`
- `tests/test_planner_router_transport_livepaper_observability_watchdog_runtime.py`
- `tests/test_bootstrap_layout.py`

Validation run on this branch:

- `pytest -q`
- `149 passed`

## Recommendation Among Next Tasks

### `livepaper_observability_operator_runbook`

Recommended next because:

- the contract is now fixed, but operators still need a consistent playbook for reading CI gate and watchdog failures
- the highest-value follow-up is turning field-level contract language into stepwise triage and escalation guidance
- that work can reuse the bounded spec directly without reopening runtime behavior

### `transport_livepaper_observability_acceptance_pack`

Not next because:

- an acceptance pack would mostly restate the same surface before the operator workflow is clarified
- the acceptance pack can become sharper after the runbook fixes how operators interpret each contract breach

### `executor_boundary_code_spec`

Not next because:

- the executor transport boundary is already bounded by the earlier executor transport spec plus the watchdog CI gate
- this task surfaced an interpretation gap, not a boundary-ownership gap

## Decision

- Outcome: `A`
- Key finding: `livepaper_observability_contract_fixed`
- Claim boundary: `livepaper_observability_spec_bounded`
- Current task status: `livepaper_observability_spec_ready`
- Recommended next step: `livepaper_observability_operator_runbook`
- Decision: `livepaper_observability_operator_runbook_ready`
