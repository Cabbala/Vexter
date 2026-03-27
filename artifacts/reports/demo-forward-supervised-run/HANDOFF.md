# Demo Forward Supervised Run Handoff

## Current Status
- outgoing_shift_window: 2026-03-27T00:51:26Z bounded supervised run lane
- incoming_shift_window: external prerequisite resolution and retry readiness
- task_state: demo_forward_supervised_run_blocked
- shift_outcome: blocked
- current_action: hold_real_demo_claim_until_external_resolution
- recommended_next_step: supervised_run_retry_readiness
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: a6ca623b01dbed4191c4be10c2bfe51534025cac
- dexter_main_commit: ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938
- mewx_frozen_commit: dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a
- prior_acceptance_lane: demo_forward_acceptance_pack_ready
- comparison_source_of_truth: comparison_closed_out

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-supervised-run-status.md
- current_report: artifacts/reports/demo-forward-supervised-run-report.md
- current_proof_summary: artifacts/proofs/demo-forward-supervised-run-summary.md
- current_proof_json: artifacts/proofs/demo-forward-supervised-run-check.json
- current_operator_follow_up: docs/demo_forward_supervised_run_operator_follow_up.md
- current_operator_checklist: docs/demo_forward_operator_checklist.md
- current_abort_rollback_matrix: docs/demo_forward_abort_rollback_matrix.md
- acceptance_pack_report: artifacts/reports/demo-forward-acceptance-pack-report.md
- acceptance_pack_proof_json: artifacts/proofs/demo-forward-acceptance-pack-check.json

## Observed Sequence
- supervised_step_1: prepare
- supervised_step_2: start
- supervised_step_3: entry_visibility
- supervised_step_4: order_status_and_fill_reconciliation
- supervised_step_5: stop_or_stop_all_visibility
- supervised_step_6: terminal_snapshot
- supervised_step_7: normalized_failure_detail_and_handoff_continuity
- supervised_step_8: supervised_window_outcome
- observed_handle_id: dexter_main_pinned:demo-forward-supervised-run:batch:0:dexter_default
- observed_native_order_status: filled
- observed_stop_all_state: flatten_confirmed

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

## External Readiness
- credential_source_visible_in_repo: false
- venue_ref_visible_in_repo: false
- account_ref_visible_in_repo: false
- connectivity_profile_visible_in_repo: false
- operator_owner_named_outside_repo: false
- supervised_window_start_confirmed_outside_repo: false
- venue_connectivity_confirmed_outside_repo: false
- real_demo_completion_claim_allowed: false

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
- question_1_or_none: who owns the named supervised window outside the repo
- question_2_or_none: when the bounded supervised window opens outside the repo
- question_3_or_none: which external venue/account/connectivity references are confirmed live outside the repo

## Next-Shift Priority Checks
- priority_check_1: resolve external credential and connectivity references outside the repo before retry
- priority_check_2: keep the lane Dexter-only and funded-live-forbidden
- priority_check_3: preserve `manual_latched_stop_all` and terminal snapshot visibility during the retry

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- operator_follow_up_pointer_checked: true
- guardrails_explicit: true
- supervised_sequence_explicit: true
- blocked_claim_boundary_explicit: true

This handoff promotes the bounded supervised run lane only. It does not claim a completed real-demo window, introduce funded live, or reopen source logic.
