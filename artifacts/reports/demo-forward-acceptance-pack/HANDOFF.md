# Demo Forward Acceptance Pack Handoff

## Current Status
- outgoing_shift_window: 2026-03-27 demo forward acceptance pack
- incoming_shift_window: supervised Dexter-only forward demo run
- task_state: demo_forward_acceptance_pack_ready
- shift_outcome: ready
- current_action: hold_until_supervised_window_opens
- recommended_next_step: demo_forward_supervised_run
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: 5c1feb2561da7b16a17c5d03b71ff2bf895e20e4
- dexter_main_commit: ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938
- mewx_frozen_commit: dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a
- prior_adapter_lane: demo_executor_adapter_implemented
- comparison_source_of_truth: comparison_closed_out

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-acceptance-pack-status.md
- current_report: artifacts/reports/demo-forward-acceptance-pack-report.md
- current_proof_summary: artifacts/proofs/demo-forward-acceptance-pack-summary.md
- current_proof_json: artifacts/proofs/demo-forward-acceptance-pack-check.json
- current_operator_checklist: docs/demo_forward_operator_checklist.md
- current_abort_rollback_matrix: docs/demo_forward_abort_rollback_matrix.md
- adapter_report: artifacts/reports/demo-executor-adapter-implementation-report.md
- adapter_proof_json: artifacts/proofs/demo-executor-adapter-implementation-check.json

## Acceptance Sequence
- acceptance_step_1: prepare
- acceptance_step_2: start
- acceptance_step_3: entry_visibility
- acceptance_step_4: order_status_and_fill_reconciliation
- acceptance_step_5: cancel_or_stop_all_visibility
- acceptance_step_6: terminal_snapshot
- acceptance_step_7: normalized_failure_detail_and_handoff_continuity

## Guardrails
- route_mode: single_sleeve
- selected_sleeve_id: dexter_default
- max_active_real_demo_plans: 1
- max_open_positions: 1
- allowlist_required: true
- small_lot_required: true
- operator_supervised_window_required: true
- mewx_overlay_enabled: false
- funded_live_allowed: false

## Abort And Rollback Conditions
- abort_condition_1: pin_mismatch
- abort_condition_2: mode_mismatch
- abort_condition_3: status_or_fill_reconciliation_gap
- abort_condition_4: duplicate_or_ambiguous_handle
- abort_condition_5: unexpected_funded_live_path
- abort_condition_6: cancel_or_stop_all_unconfirmed
- abort_condition_7: quarantine_or_manual_halt_triggered
- abort_condition_8: terminal_snapshot_visibility_lost

## Open Questions
- question_1_or_none: choose the explicit supervised-window start time outside the repo
- question_2_or_none: choose the initial allowlist symbol set outside the repo
- question_3_or_none: assign the named operator owner for the first supervised window outside the repo

## Next-Shift Priority Checks
- priority_check_1: confirm external credential references are resolved before `prepare`
- priority_check_2: confirm the window remains Dexter-only and funded-live-forbidden
- priority_check_3: confirm `manual_latched_stop_all` and terminal snapshot visibility remain explicit during the supervised run

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- operator_checklist_pointer_checked: true
- abort_matrix_pointer_checked: true
- guardrails_explicit: true
- acceptance_sequence_explicit: true
- abort_conditions_explicit: true

This handoff fixes the bounded acceptance pack only. It does not start the supervised window, introduce funded live, or reopen source logic.
