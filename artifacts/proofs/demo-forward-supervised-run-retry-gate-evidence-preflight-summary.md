# DEMO-FORWARD-SUPERVISED-RUN-RETRY-GATE-EVIDENCE-PREFLIGHT Summary

- Preflight status: `blocked`
- Manifest status: `template_only`
- Manifest path: `manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json`
- Retry-gate review reopen ready: `no`
- Blocked faces: `external_credential_source_face, venue_ref_face, account_ref_face, connectivity_profile_face, operator_owner_face, bounded_start_criteria_face, allowlist_symbol_lot_reconfirmed, manual_latched_stop_all_visibility_reconfirmed, terminal_snapshot_readability_reconfirmed`
- Aggregated blocked reasons: `attestors_missing=9, bounded_window_missing=9, evidence_locator_missing=9, fresh_until_missing=9, locator_kind_missing=9, outside_repo_locator_not_supplied=9, template_only_manifest=9, verification_timestamp_missing=9`
- Aggregated blocker groups: `missing=63, state=9`
- Canonical preflight command: `python3.12 scripts/run_demo_forward_supervised_run_retry_gate_evidence_preflight.py`

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
