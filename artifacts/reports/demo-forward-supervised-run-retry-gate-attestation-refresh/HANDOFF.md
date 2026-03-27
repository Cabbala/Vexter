# Demo Forward Supervised Run Retry Gate Attestation Refresh Handoff

## Current Status
- outgoing_shift_window: 2026-03-27T13:11:43Z attestation-refresh lane
- incoming_shift_window: fresh locator collection and record-pack regeneration
- task_state: supervised_run_retry_gate_attestation_refresh_blocked
- shift_outcome: blocked
- current_action: hold_retry_gate_review_until_attestation_refresh_is_current_and_record_pack_can_be_regenerated
- current_lane: supervised_run_retry_gate_attestation_refresh
- recommended_next_step_while_blocked: supervised_run_retry_gate_attestation_record_pack_regeneration
- refresh_pass_successor: supervised_run_retry_gate
- status_delivery: poll_first
- halt_mode: manual_latched_stop_all
- source_faithful_seam: Dexter `paper_live` / frozen Mew-X `sim_live`
- first_demo_target: Dexter `paper_live`
- real_execution_leg: Dexter only
- simulated_leg_or_none: Mew-X `sim_live`
- vexter_main_commit: abf5a5659a1a6a1918af18c57978ec10ef2d33d6
- dexter_main_commit: ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938
- mewx_frozen_commit: dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a
- baseline_attestation_record_pack_regeneration_task_state: supervised_run_retry_gate_attestation_record_pack_regeneration_blocked

## Proof And Report Pointers
- current_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-status.md
- current_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh-report.md
- current_proof_summary: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-summary.md
- current_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json
- current_attestation_refresh_checklist: docs/demo_forward_supervised_run_retry_gate_attestation_refresh_checklist.md
- current_attestation_refresh_decision_surface: docs/demo_forward_supervised_run_retry_gate_attestation_refresh_decision_surface.md
- current_subagent_summary: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/SUBAGENTS.md
- baseline_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md
- baseline_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md
- baseline_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json
- baseline_handoff: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md

## Guardrails
- route_mode: single_sleeve
- selected_sleeve_id: dexter_default
- max_active_real_demo_plans: 1
- max_open_positions: 1
- allowlist_required: true
- allowlist_symbols: BONK/USDC
- demo_symbol: BONK/USDC
- small_lot_required: true
- small_lot_order_size: 0.05
- bounded_window_minutes: 15
- operator_supervised_window_required: true
- external_credential_refs_outside_repo: true
- operator_owner_explicit_required: true
- venue_connectivity_confirmation_required: true
- manual_latched_stop_all_visibility_reconfirmation_required: true
- terminal_snapshot_readability_reconfirmation_required: true
- mewx_overlay_enabled: false
- funded_live_allowed: false

## Refresh Faces
- external_credential_source_face: refresh_rule_complete=true, current_fresh_evidence_locator_present=false, current_evidence_fresh_enough=false, usable_now=false, refresh_owner=named_operator_owner_outside_repo
- venue_ref_face: refresh_rule_complete=true, current_fresh_evidence_locator_present=false, current_evidence_fresh_enough=false, usable_now=false, refresh_owner=named_operator_owner_plus_venue_owner_outside_repo
- account_ref_face: refresh_rule_complete=true, current_fresh_evidence_locator_present=false, current_evidence_fresh_enough=false, usable_now=false, refresh_owner=named_operator_owner_outside_repo
- connectivity_profile_face: refresh_rule_complete=true, current_fresh_evidence_locator_present=false, current_evidence_fresh_enough=false, usable_now=false, refresh_owner=named_operator_owner_plus_connectivity_owner_outside_repo
- operator_owner_face: refresh_rule_complete=true, current_fresh_evidence_locator_present=false, current_evidence_fresh_enough=false, usable_now=false, refresh_owner=demo_operator_lead_outside_repo
- bounded_start_criteria_face: refresh_rule_complete=true, current_fresh_evidence_locator_present=false, current_evidence_fresh_enough=false, usable_now=false, refresh_owner=named_operator_owner_outside_repo
- allowlist_symbol_lot_reconfirmed: refresh_rule_complete=true, current_fresh_evidence_locator_present=false, current_evidence_fresh_enough=false, usable_now=false, refresh_owner=named_operator_owner_outside_repo
- manual_latched_stop_all_visibility_reconfirmed: refresh_rule_complete=true, current_fresh_evidence_locator_present=false, current_evidence_fresh_enough=false, usable_now=false, refresh_owner=named_operator_owner_outside_repo
- terminal_snapshot_readability_reconfirmed: refresh_rule_complete=true, current_fresh_evidence_locator_present=false, current_evidence_fresh_enough=false, usable_now=false, refresh_owner=named_operator_owner_outside_repo

## Open Questions
- question_1_or_none: who will publish one current bounded-window locator for each required face without exposing secrets
- question_2_or_none: which refreshed regenerated locator should seed the next record-pack regeneration rerun for venue, account, and connectivity faces
- question_3_or_none: who timestamps the bounded start window and operator owner for the next retry-gate recheck
- question_4_or_none: has `manual_latched_stop_all` visibility been freshly reconfirmed for the current bounded window
- question_5_or_none: has terminal snapshot readability been freshly reconfirmed for the current bounded window

## Next-Shift Priority Checks
- priority_check_1: keep the current lane blocked unless every face has a current, fresh-enough bounded-window locator and freshness check
- priority_check_2: recommend `supervised_run_retry_gate_attestation_record_pack_regeneration` while blocked so the current record-pack regeneration can be rerun, and expose `supervised_run_retry_gate` only as the pass successor
- priority_check_3: preserve Dexter-only `paper_live`, `single_sleeve`, `dexter_default`, small-lot, one-position, `manual_latched_stop_all`, and funded-live-forbidden guardrails

## Completeness Check
- every_required_face_filled_or_none: true
- status_matches_current_artifacts: true
- proof_and_report_pointers_checked: true
- checklist_pointer_checked: true
- decision_surface_pointer_checked: true
- subagent_summary_pointer_checked: true
- blocked_claim_boundary_explicit: true

This handoff promotes the bounded attestation refresh lane only. It does not claim regenerated record-pack success, reopened retry gate, completed retry execution, funded live access, or any Mew-X seam expansion.
