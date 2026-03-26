# Live-Paper Observability Shift Handoff Template

## Purpose

This template turns the fixed live-paper observability contract, operator runbook, and shift checklist into one bounded outgoing and incoming handoff record for the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.
It does not authorize source changes, new evidence collection, comparison-baseline reopen, or funded live trading.

## Fixed Inputs

- Vexter merged `main`: PR `#62`, merge commit `3b595faacf316aca89655b6e1ffcf7568478763e`
- Latest merged checklist lane: PR `#61`, merge commit `991efd2566dc0a51121c5c36e806fd0a215bcea6`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- Canonical runbook: `docs/livepaper_observability_operator_runbook.md`
- Canonical checklist: `docs/livepaper_observability_shift_checklist.md`
- Fixed halt mode: `manual_latched_stop_all`
- Fixed status delivery: `poll_first`

## Artifact Entry Order

1. Start with `artifacts/reports/task-007-livepaper-observability-shift-handoff-template-status.md`.
   Use it to confirm the current lane state, fixed inputs, and next-step recommendation before filling or reading a handoff.
2. Read `artifacts/reports/task-007-livepaper-observability-shift-handoff-template-report.md`.
   Use it to recover the bounded handoff faces, completion rules, and next-task recommendation.
3. Read `artifacts/proofs/task-007-livepaper-observability-shift-handoff-template-summary.md`.
   Use it for the shortest evidence trail and the current recommendation.
4. Read `docs/livepaper_observability_shift_handoff_template.md`.
   Use it for the canonical handoff shape and copyable template body.
5. Read `artifacts/proofs/task-007-livepaper-observability-shift-handoff-template-check.json`.
   Use it for the machine-readable handoff faces, completeness rules, and task result fields.

## Required Handoff Faces

### 1. Current status

Always record:

- current task status
- shift outcome: `contained`, `escalated`, or `closed`
- current action: `halt`, `quarantine`, or `continue`
- active broken surface, or `none`
- current recommended next step
- fixed status delivery confirmation: `poll_first`
- fixed seam and pins confirmation
- promoted baseline and comparison source-of-truth confirmation

### 2. Proof and report pointers

Always record:

- current status report path
- current report path
- current proof summary path
- current proof JSON path
- first deep proof to open next
- shortest proof trail used for the outgoing decision

### 3. `omission` / `drift` / `partial_visibility`

Always record each meaning explicitly:

- present: `true` or `false`
- short summary, or `none`
- exact broken surface or `none`

Do not collapse this into one vague incident note.

### 4. Manual stop-all and quarantine state

Always record:

- whether `manual_latched_stop_all` is visible
- `halt_mode`, `trigger_plan_id`, and `stop_reason`, or `none`
- whether peer-plan propagation is confirmed
- whether quarantine is active
- `quarantine_reason`, or `none`
- whether plan, monitor, executor, and ack-history continuity stay visible

### 5. Terminal snapshot state

Always record:

- whether a terminal snapshot is present
- the terminal snapshot pointer, or `none`
- whether `signal=snapshot` is visible
- whether `stop_reason` stays visible

### 6. Normalized failure detail state

Always record:

- whether normalized failure detail is present
- the failure-detail pointer, or `none`
- whether `code`, `stage`, `plan_id`, `source`, and passthrough `source_reason` remain visible
- whether the nested identity chain remains coherent
- whether `rollback_snapshot` is present when `rollback_confirmed=true`

### 7. Open questions

Always record unresolved questions explicitly.
If none remain, write `none`.

### 8. Next-shift priority checks

Always record the first checks for the incoming operator.
These should be the smallest high-signal confirmations, not a full rerun.

### 9. Bounded completeness criteria

Treat the handoff as incomplete if any required face is blank, implied, or replaced by "same as before."

Minimum completion rules are fixed now:

- every required face is filled or explicitly marked `none`
- current status agrees with the current checklist status, report, and proof trail
- proof/report pointers are present and openable
- `omission`, `drift`, and `partial_visibility` are each recorded explicitly
- manual stop-all, quarantine, terminal snapshot, and normalized failure detail are each recorded explicitly, even when absent
- open questions and next-shift priority checks are explicit, not implied

## Copyable Template

```md
# Live-Paper Observability Shift Handoff

## Current Status
- outgoing_shift_window:
- incoming_shift_window:
- task_state:
- shift_outcome: contained | escalated | closed
- current_action: halt | quarantine | continue
- active_broken_surface_or_none:
- recommended_next_step:
- status_delivery: poll_first
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- vexter_main_commit:
- dexter_main_commit:
- mewx_frozen_commit:
- promoted_baseline:
- comparison_source_of_truth:

## Proof and Report Pointers
- current_status_report:
- current_report:
- current_proof_summary:
- current_proof_json:
- first_deep_proof_to_open_next:
- shortest_proof_trail:

## Observability Classification
- omission_present:
- omission_summary_or_none:
- drift_present:
- drift_summary_or_none:
- partial_visibility_present:
- partial_visibility_summary_or_none:
- exact_broken_surface_or_none:

## Manual Stop-All and Quarantine
- manual_stop_all_visible:
- halt_mode_or_none:
- trigger_plan_id_or_none:
- stop_reason_or_none:
- peer_plan_propagation_confirmed:
- quarantine_active:
- quarantine_reason_or_none:
- continuity_check:

## Terminal Snapshot
- terminal_snapshot_present:
- terminal_snapshot_pointer_or_none:
- snapshot_signal_visible:
- terminal_stop_reason_visible:

## Normalized Failure Detail
- normalized_failure_detail_present:
- failure_detail_pointer_or_none:
- normalized_identity_chain_coherent:
- source_reason_visible:
- rollback_snapshot_required_and_present_or_none:

## Open Questions
- question_1_or_none:
- question_2_or_none:
- question_3_or_none:

## Next-Shift Priority Checks
- priority_check_1:
- priority_check_2_or_none:
- priority_check_3_or_none:

## Completeness Check
- every_required_face_filled_or_none:
- status_matches_current_checklist_artifacts:
- proof_and_report_pointers_checked:
- omission_drift_partial_visibility_explicit:
- containment_and_failure_faces_explicit:
- open_questions_and_next_checks_explicit:
```

## Bounded Non-Goals

- Dexter or Mew-X source logic changes
- validator-rule changes
- comparison-baseline reopen
- new evidence collection
- funded live trading
- transport-boundary or trust-logic redesign
