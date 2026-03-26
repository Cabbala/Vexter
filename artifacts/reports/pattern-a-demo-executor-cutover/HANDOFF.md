# Pattern A Demo Executor Cutover Handoff

## Current Status
- outgoing_shift_window: 2026-03-27 Pattern A cutover planning
- incoming_shift_window: next demo adapter implementation lane
- task_state: pattern_a_demo_executor_cutover_ready
- shift_outcome: ready
- current_action: proceed_to_adapter_implementation
- recommended_next_step: demo_executor_adapter_implementation
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: 289eb1bc87a8db9a9801b9b0583a8dbc6b17a5b3
- dexter_main_commit: ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938
- mewx_frozen_commit: dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a
- promoted_baseline: task005-pass-grade-pair-20260325T180027Z
- comparison_source_of_truth: comparison_closed_out

## Proof and Report Pointers
- current_status_report: artifacts/reports/pattern-a-demo-executor-cutover-status.md
- current_report: artifacts/reports/pattern-a-demo-executor-cutover-report.md
- current_proof_summary: artifacts/proofs/pattern-a-demo-executor-cutover-summary.md
- current_proof_json: artifacts/proofs/pattern-a-demo-executor-cutover-check.json
- first_deep_proof_to_open_next: artifacts/proofs/task-007-transport-livepaper-observability-watchdog-ci-gate-check.json
- shortest_proof_trail: status -> report -> summary -> Pattern A proof -> transport watchdog CI gate proof -> handoff watchdog CI gate proof

## Boundary
- planner_owned_surface: prepare/start/status/stop/snapshot plus timeout, quarantine, stop-all, and normalized status fan-in
- adapter_owned_surface: submit/cancel/status/fill/stop-all inside Dexter demo runtime
- handle_identity_chain: plan_id -> handle_id -> native_session_id -> native_order_ids

## Guardrails
- route_mode: single_sleeve
- selected_sleeve_id: dexter_default
- max_active_real_demo_plans: 1
- max_open_positions: 1
- allowlist_required: true
- small_lot_required: true
- operator_supervised_window_required: true
- mewx_overlay_enabled: false

## Abort and Rollback Conditions
- abort_condition_1: pin_or_mode_mismatch
- abort_condition_2: status_or_fill_reconciliation_gap
- abort_condition_3: duplicate_or_ambiguous_handle
- abort_condition_4: unexpected_funded_live_path
- abort_condition_5: cancel_or_stop_all_unconfirmed
- abort_condition_6: quarantine_or_manual_halt_triggered

## Open Questions
- question_1_or_none: choose the concrete demo venue credentials outside the repo before implementation or forward run
- question_2_or_none: choose the initial allowlist symbol set outside the repo before the first supervised window
- question_3_or_none: none

## Next-Shift Priority Checks
- priority_check_1: implement the concrete Dexter demo adapter without changing the existing planner boundary
- priority_check_2_or_none: keep Mew-X on `sim_live` or disabled for the first real demo slice
- priority_check_3_or_none: wire adapter tests before any demo forward acceptance pack is attempted

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- guardrails_explicit: true
- boundary_split_explicit: true
- abort_conditions_explicit: true

This handoff fixes the Pattern A cutover boundary only. It does not collect new evidence, change source logic, or claim funded live readiness.
