# TASK-007 Live-Paper Observability Operator Runbook Report

## Scope

This task starts from merged PR `#59` and the completed `TASK-007-LIVEPAPER-OBSERVABILITY-SPEC` lane.
It does not reopen comparison work or change planner/router, Dexter, or Mew-X logic.
It turns the fixed live-paper observability contract into one bounded operator playbook for the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#59`, main commit `4be21e4e52fbe686e585dea6b573efea759e0933`, merged at `2026-03-26T16:54:45Z`
- Open non-authoritative Vexter PR: `#50`, `feat(infra): refresh runtime observability artifacts`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, committed at `2026-03-20T16:05:19Z`

## Fixed Input Surface

- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- Prior lane report: `artifacts/reports/task-007-livepaper-observability-spec-report.md`
- Prior lane proof: `artifacts/proofs/task-007-livepaper-observability-spec-check.json`
- Deep proof sources remain:
  - watchdog CI gate
  - watchdog runtime
  - watchdog regression pack
  - watchdog

## What Landed

### One bounded operator runbook

The operator-facing runbook now lives in `docs/livepaper_observability_operator_runbook.md`.
It does not redefine the contract.
It defines how operators read and use the already-fixed observability surface.

### Two lookup orders

The runbook fixes two separate reading orders.

Artifact entry order:

1. current runbook status
2. current runbook report
3. current runbook proof summary
4. canonical contract
5. current runbook proof JSON

Incident localization order:

1. start with the watchdog CI gate
2. read the failing watchdog surface name before individual snapshots
3. classify the break as `omission`, `drift`, or `partial_visibility`
4. prefer snapshot-backed terminal detail and normalized failure detail over sink snippets for terminal or failed paths
5. confirm peer-plan propagation before treating one plan as isolated under `manual_latched_stop_all`

### Operator meanings and priority

The runbook now fixes the operator-facing meanings without changing source logic:

- `omission`: required evidence disappeared
- `drift`: required evidence stayed visible but no longer matches the planned source-faithful envelope
- `partial_visibility`: lifecycle progression stayed visible but required operator detail no longer did

Priority is now fixed in this order:

1. containment and halt confidence
2. identity and planned-runtime integrity
3. visibility quality after containment

That maps to the named surfaces as:

- containment and halt: `manual_stop_all_propagation`, `quarantine_reason_completeness`, `snapshot_backed_terminal_detail`, `normalized_failure_detail_passthrough`
- identity and planned/runtime integrity: `planned_runtime_metadata_drift`, `handle_lifecycle_continuity`, `required_observability_field_omission`
- visibility quality after containment: `partial_status_sink_fan_in`, `ack_history_retention`

### Bounded operational decisions

The runbook now states how operators should act on the fixed surfaces:

- manual stop-all is a propagation event, not a local failure until peer-plan fanout is confirmed
- quarantine is only complete when `quarantine_reason` remains visible together with plan, monitor, executor, and ack-history continuity
- terminal detail is authoritative only when snapshot-backed
- normalized failure detail routes by normalized `code` and `stage`, but preserves source-native `source_reason` and nested identity detail
- ack-history counts remain monotonic, sticky booleans do not collapse, and duplicate-or-terminal visibility stays required once request counts rise above `1`

### Bounded escalation

The task now fixes when the operator should halt, continue in containment, or inspect more deeply:

- halt when containment surfaces fail or planned/runtime identity drifts
- continue only in a contained state when quarantine, stop propagation, terminal snapshot, and failure detail remain coherent
- inspect more deeply when the main break is sink fan-in loss or ack-history loss but the containment story is still intact

## What Did Not Change

- No planner/router source logic changed.
- No Dexter behavior changed.
- No Mew-X behavior changed.
- No validator rules changed.
- No comparison evidence was recollected.
- No comparison baseline was reopened.

## Tests

- `pytest -q`
- `152 passed`

## Recommendation Among Next Tasks

### `livepaper_observability_shift_checklist`

Recommended next because:

- the contract now fixes what must stay visible
- the runbook now fixes how operators should read and triage that visibility
- the next bounded gap is a short shift-time checklist derived directly from that read order and escalation boundary

### `transport_livepaper_observability_acceptance_pack`

Not next because:

- an acceptance pack would mostly restate the same surfaces before the operator shift procedure is reduced to a concise checklist
- the acceptance pack can become sharper after the shift checklist fixes the minimum pre-shift and during-shift checks

### `executor_boundary_code_spec`

Not next because:

- the executor boundary is already bounded by the earlier transport spec and the watchdog CI gate
- the remaining gap after this task is operator procedure, not code-boundary ambiguity

## Decision

- Outcome: `A`
- Key finding: `livepaper_observability_operator_runbook_fixed`
- Claim boundary: `livepaper_observability_operator_runbook_bounded`
- Current task status: `livepaper_observability_operator_runbook_ready`
- Recommended next step: `livepaper_observability_shift_checklist`
- Decision: `livepaper_observability_shift_checklist_ready`
