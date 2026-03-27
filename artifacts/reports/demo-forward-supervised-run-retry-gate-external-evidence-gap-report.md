# Demo Forward Supervised Run Retry Gate External Evidence Gap Report

## Canonical Contract
- Contract spec: `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_EXTERNAL_EVIDENCE_CONTRACT.md`
- Canonical manifest: `manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json`
- Manifest status: `template_only`
- Manifest role: `template`
- Generated at: `2026-03-27T20:43:13Z`
- Retry-gate review reopen ready: `no`

## Summary
- Required faces: `9`
- Present faces: `0`
- Current faces: `0`
- Reviewable faces: `0`
- Stale faces: `0`
- Blocked faces: `external_credential_source_face, venue_ref_face, account_ref_face, connectivity_profile_face, operator_owner_face, bounded_start_criteria_face, allowlist_symbol_lot_reconfirmed, manual_latched_stop_all_visibility_reconfirmed, terminal_snapshot_readability_reconfirmed`

## Face Status

| Face | Repo-visible marker | Present | Current | Fresh enough | Reviewable | Blocked reasons | Operator input still needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `external_credential_source_face` | `external_reference` | `no` | `no` | `no` | `no` | template_only_manifest, outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing | Provide one current non-secret locator that confirms which Dexter paper-live credential source was resolved for the bounded supervised window. |
| `venue_ref_face` | `dexter_paper_live_demo_venue` | `no` | `no` | `no` | `no` | template_only_manifest, outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing | Provide one current non-secret locator that ties the repo-visible venue marker to the exact Dexter demo venue for the bounded supervised window. |
| `account_ref_face` | `dexter_paper_live_demo_account` | `no` | `no` | `no` | `no` | template_only_manifest, outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing | Provide one current non-secret locator that shows which Dexter paper-live demo account the bounded supervised window is bound to. |
| `connectivity_profile_face` | `dexter_paper_live_demo_connectivity` | `no` | `no` | `no` | `no` | template_only_manifest, outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing | Provide one current non-secret locator that shows the intended connectivity profile was checked for venue/account reachability inside the bounded supervised window. |
| `operator_owner_face` | `unconfirmed_outside_repo` | `no` | `no` | `no` | `no` | template_only_manifest, outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing | Name one explicit operator owner and provide one reviewable non-secret locator that shows ownership for the bounded supervised window. |
| `bounded_start_criteria_face` | `{"bounded_window_minutes": 15, "halt_mode": "manual_latched_stop_all", "status_delivery": "poll_first"}` | `no` | `no` | `no` | `no` | template_only_manifest, outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing | Provide one current non-secret locator that fixes the bounded start window plus the go/no-go and abort owners for the next supervised retry attempt. |
| `allowlist_symbol_lot_reconfirmed` | `{"allowed_symbols": ["BONK/USDC"], "bounded_window_minutes": 15, "default_symbol": "BONK/USDC", "max_open_positions": 1, "max_order_size_lots": "0.05", "order_size_lots": "0.05"}` | `no` | `no` | `no` | `no` | template_only_manifest, outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing | Provide one current non-secret locator that reconfirms the allowlist, default symbol, lot size, one-position cap, and bounded window guardrails for the next supervised attempt. |
| `manual_latched_stop_all_visibility_reconfirmed` | `baseline_stop_all_state=flatten_confirmed` | `no` | `no` | `no` | `no` | template_only_manifest, outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing | Provide one current non-secret locator that freshly reconfirms `manual_latched_stop_all` visibility for the bounded supervised window. |
| `terminal_snapshot_readability_reconfirmed` | `baseline_terminal_snapshot_readable=true` | `no` | `no` | `no` | `no` | template_only_manifest, outside_repo_locator_not_supplied, attestors_missing, evidence_locator_missing, locator_kind_missing, verification_timestamp_missing, fresh_until_missing, bounded_window_missing | Provide one current non-secret locator that freshly reconfirms terminal snapshot readability for the bounded supervised window. |

## Validation Errors
- none

The gap report stays fail-closed. It does not claim current external evidence exists unless the canonical manifest is marked `evidence`, every required face is present, current, and reviewable, and the manifest remains non-secret by construction.
