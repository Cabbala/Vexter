# Demo Forward Supervised Run Retry Gate Attestation Refresh Handoff

## Current Status
- outgoing_shift_window: 2026-03-28T15:24:50Z attestation-refresh lane
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
- vexter_main_commit: 4df9837e630e175af3b06f99f79fce2689822bd0
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
- canonical_external_evidence_contract: specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_EXTERNAL_EVIDENCE_CONTRACT.md
- canonical_external_evidence_manifest: manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json
- canonical_external_evidence_preflight_report: artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md
- canonical_external_evidence_preflight_proof: artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json
- canonical_external_evidence_preflight_summary: artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-summary.md
- canonical_external_evidence_gap_report: artifacts/reports/demo-forward-supervised-run-retry-gate-external-evidence-gap-report.md
- canonical_external_evidence_gap_proof: artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-check.json
- canonical_external_evidence_gap_summary: artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-summary.md
- canonical_external_evidence_manifest_status: template_only
- baseline_status_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md
- baseline_report: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md
- baseline_proof_json: artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json
- baseline_handoff: artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md

## Canonical Evidence Intake Handoff
- bounded_window_fields_to_fill_once: bounded_supervised_window.label, bounded_supervised_window.starts_at, bounded_supervised_window.ends_at
- per_blocked_face_fields_to_fill: provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note
- canonical_face_to_manifest_map: artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md
- canonical_machine_preflight_proof: artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json
- canonical_legacy_gap_report: artifacts/reports/demo-forward-supervised-run-retry-gate-external-evidence-gap-report.md
- proof_surfaces_to_rerun_after_manifest_update: artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json, artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md, artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-summary.md, artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-check.json, artifacts/reports/demo-forward-supervised-run-retry-gate-external-evidence-gap-report.md, artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-summary.md, artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json, artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md, artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json, artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md
- evidence_preflight_status: blocked
- evidence_preflight_aggregated_blocked_reasons: {"attestors_missing": 9, "bounded_window_missing": 9, "evidence_locator_missing": 9, "fresh_until_missing": 9, "locator_kind_missing": 9, "outside_repo_locator_not_supplied": 9, "template_only_manifest": 9, "verification_timestamp_missing": 9}
- template_only_false_path: Manifest remains template_only, so retry-gate reopen stays blocked until the bounded supervised window fields are filled once, every blocked face carries a current non-secret reviewable locator, and the canonical preflight returns ready.
- evidence_preflight_consistency_checks: {"blocked_face_count_matches_face_rows": true, "blocked_face_names_match_face_rows": true, "blocked_faces_have_manifest_fields_and_operator_input": true, "blocked_reason_counts_match_face_rows": true, "operator_inputs_remaining_match_blocked_faces": true, "template_only_false_path_holds": true}
- rerun_gap_and_lane_commands:
  - python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py
  - python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py
  - python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py

## Next Human Pass Checklist
- Keep manifest_role at template: Keep manifest_role at template while any bounded-window field or blocked face field is still missing, stale, non-reviewable, or otherwise preflight-blocked.
- Template-only false path: Manifest remains template_only, so retry-gate reopen stays blocked until the bounded supervised window fields are filled once, every blocked face carries a current non-secret reviewable locator, and the canonical preflight returns ready.
- Fill bounded window once: bounded_supervised_window.label, bounded_supervised_window.starts_at, bounded_supervised_window.ends_at
- external_credential_source_face: fill provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note; blockers state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing; operator input Provide one current non-secret locator that confirms which Dexter paper-live credential source was resolved for the bounded supervised window.
- venue_ref_face: fill provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note; blockers state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing; operator input Provide one current non-secret locator that ties the repo-visible venue marker to the exact Dexter demo venue for the bounded supervised window.
- account_ref_face: fill provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note; blockers state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing; operator input Provide one current non-secret locator that shows which Dexter paper-live demo account the bounded supervised window is bound to.
- connectivity_profile_face: fill provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note; blockers state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing; operator input Provide one current non-secret locator that shows the intended connectivity profile was checked for venue/account reachability inside the bounded supervised window.
- operator_owner_face: fill provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note; blockers state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing; operator input Name one explicit operator owner and provide one reviewable non-secret locator that shows ownership for the bounded supervised window.
- bounded_start_criteria_face: fill provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note; blockers state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing; operator input Provide one current non-secret locator that fixes the bounded start window plus the go/no-go and abort owners for the next supervised retry attempt.
- allowlist_symbol_lot_reconfirmed: fill provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note; blockers state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing; operator input Provide one current non-secret locator that reconfirms the allowlist, default symbol, lot size, one-position cap, and bounded window guardrails for the next supervised attempt.
- manual_latched_stop_all_visibility_reconfirmed: fill provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note; blockers state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing; operator input Provide one current non-secret locator that freshly reconfirms `manual_latched_stop_all` visibility for the bounded supervised window.
- terminal_snapshot_readability_reconfirmed: fill provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note; blockers state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing; operator input Provide one current non-secret locator that freshly reconfirms terminal snapshot readability for the bounded supervised window.
- Rerun in order: python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py -> python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py -> python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py
- Optional legacy compatibility rerun: python3.12 scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py

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
- question_1_or_none: who will replace the template manifest with current evidence locators for each required face without exposing secrets
- question_2_or_none: which refreshed evidence locator should seed the next record-pack regeneration rerun for venue, account, and connectivity faces
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
