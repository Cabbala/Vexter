# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-EXTERNAL-EVIDENCE-GAP Summary

- Manifest status: `template_only`
- Manifest path: `manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json`
- Required faces: `9`
- Present/current/reviewable: `0` / `0` / `0`
- Blocked faces: `external_credential_source_face, venue_ref_face, account_ref_face, connectivity_profile_face, operator_owner_face, bounded_start_criteria_face, allowlist_symbol_lot_reconfirmed, manual_latched_stop_all_visibility_reconfirmed, terminal_snapshot_readability_reconfirmed`
- Retry-gate review reopen ready: `no`
- Window fields to fill: `bounded_supervised_window.label, bounded_supervised_window.starts_at, bounded_supervised_window.ends_at`
- Canonical preflight command: `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py`
- Legacy gap command: `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py`
- Canonical face-to-manifest and proof map: `artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md`
- Next operator step: fill the bounded window once, fill each blocked face honestly, keep manifest_role at `template` until the canonical preflight returns `ready`, then rerun the canonical preflight and the refresh/regeneration surfaces.

## Next Human Pass Checklist
- Hold rule: Keep manifest_role at template while any bounded-window field or blocked face field is still missing, stale, non-reviewable, or otherwise preflight-blocked.
- Reopen false-path: Manifest remains template_only, so retry-gate reopen stays blocked until the bounded supervised window fields are filled once, every blocked face carries a current non-secret reviewable locator, and the canonical preflight returns ready.
- Fill bounded-window fields once: `bounded_supervised_window.label, bounded_supervised_window.starts_at, bounded_supervised_window.ends_at`
- `external_credential_source_face` -> fill `provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note`; blockers `state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing`; operator input: Provide one current non-secret locator that confirms which Dexter paper-live credential source was resolved for the bounded supervised window.
- `venue_ref_face` -> fill `provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note`; blockers `state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing`; operator input: Provide one current non-secret locator that ties the repo-visible venue marker to the exact Dexter demo venue for the bounded supervised window.
- `account_ref_face` -> fill `provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note`; blockers `state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing`; operator input: Provide one current non-secret locator that shows which Dexter paper-live demo account the bounded supervised window is bound to.
- `connectivity_profile_face` -> fill `provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note`; blockers `state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing`; operator input: Provide one current non-secret locator that shows the intended connectivity profile was checked for venue/account reachability inside the bounded supervised window.
- `operator_owner_face` -> fill `provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note`; blockers `state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing`; operator input: Name one explicit operator owner and provide one reviewable non-secret locator that shows ownership for the bounded supervised window.
- `bounded_start_criteria_face` -> fill `provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note`; blockers `state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing`; operator input: Provide one current non-secret locator that fixes the bounded start window plus the go/no-go and abort owners for the next supervised retry attempt.
- `allowlist_symbol_lot_reconfirmed` -> fill `provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note`; blockers `state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing`; operator input: Provide one current non-secret locator that reconfirms the allowlist, default symbol, lot size, one-position cap, and bounded window guardrails for the next supervised attempt.
- `manual_latched_stop_all_visibility_reconfirmed` -> fill `provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note`; blockers `state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing`; operator input: Provide one current non-secret locator that freshly reconfirms `manual_latched_stop_all` visibility for the bounded supervised window.
- `terminal_snapshot_readability_reconfirmed` -> fill `provided, attested_by, evidence_locator, locator_kind, verified_at, fresh_until, reviewable_without_secrets, reviewability_note`; blockers `state=template_only_manifest; missing=outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing`; operator input: Provide one current non-secret locator that freshly reconfirms terminal snapshot readability for the bounded supervised window.
- Rerun in order: `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py`
- Rerun in order: `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_refresh.py`
- Rerun in order: `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration.py`
- Optional legacy compatibility rerun: `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_external_evidence_gap.py`

## Consistency Checks
- `blocked_face_count_matches_face_rows`: `yes`
- `blocked_face_names_match_face_rows`: `yes`
- `blocked_reason_counts_match_face_rows`: `yes`
- `operator_inputs_remaining_match_blocked_faces`: `yes`
- `blocked_faces_have_manifest_fields_and_operator_input`: `yes`
- `template_only_false_path_holds`: `yes`

## Operator Inputs Remaining
- `external_credential_source_face: Provide one current non-secret locator that confirms which Dexter paper-live credential source was resolved for the bounded supervised window.`
- `venue_ref_face: Provide one current non-secret locator that ties the repo-visible venue marker to the exact Dexter demo venue for the bounded supervised window.`
- `account_ref_face: Provide one current non-secret locator that shows which Dexter paper-live demo account the bounded supervised window is bound to.`
- `connectivity_profile_face: Provide one current non-secret locator that shows the intended connectivity profile was checked for venue/account reachability inside the bounded supervised window.`
- `operator_owner_face: Name one explicit operator owner and provide one reviewable non-secret locator that shows ownership for the bounded supervised window.`
- `bounded_start_criteria_face: Provide one current non-secret locator that fixes the bounded start window plus the go/no-go and abort owners for the next supervised retry attempt.`
- `allowlist_symbol_lot_reconfirmed: Provide one current non-secret locator that reconfirms the allowlist, default symbol, lot size, one-position cap, and bounded window guardrails for the next supervised attempt.`
- `manual_latched_stop_all_visibility_reconfirmed: Provide one current non-secret locator that freshly reconfirms `manual_latched_stop_all` visibility for the bounded supervised window.`
- `terminal_snapshot_readability_reconfirmed: Provide one current non-secret locator that freshly reconfirms terminal snapshot readability for the bounded supervised window.`
