# Demo Forward Supervised Run Retry Gate Attestation Record Pack Checklist

## Required Runtime Markers
- `DEXTER_DEMO_CREDENTIAL_SOURCE`
- `DEXTER_DEMO_VENUE_REF`
- `DEXTER_DEMO_ACCOUNT_REF`
- `DEXTER_DEMO_CONNECTIVITY_PROFILE`
- `DEXTER_DEMO_ALLOWED_SYMBOLS`
- `DEXTER_DEMO_DEFAULT_SYMBOL`
- `DEXTER_DEMO_ORDER_SIZE_LOTS`
- `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`
- `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`
- `DEXTER_DEMO_WINDOW_MINUTES=15`
- `manual_latched_stop_all`
- terminal snapshot readability
- funded live forbidden

## Review Steps
1. Start at `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-status.md`.
2. Review `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-report.md`.
3. Review `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-check.json`.
4. Carry continuity from `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack/HANDOFF.md`.
5. Use `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_decision_surface.md` as the single attestation record-pack decision surface.
6. Keep one record-pack row per required face: credential source, venue ref, account ref, connectivity profile, operator owner, bounded start criteria, allowlist / symbol / lot reconfirmation, `manual_latched_stop_all` visibility, and terminal snapshot readability.
7. For every row, confirm who owns the record, the minimum evidence locator shape, the freshness requirement, the stale condition, and what makes the record reviewable enough are explicit.
8. For every row, record whether a current bounded-window record locator is present without embedding secret material.
9. Hold the lane at `FAIL/BLOCKED` until every required face is current, fresh, and reviewable enough.

## Record Faces
| Record face | Who owns the record | Minimum evidence locator shape | Freshness requirement | Stale condition | Reviewable enough when |
| --- | --- | --- | --- | --- | --- |
| `external_credential_source_face` | `named_operator_owner_outside_repo` | attestor name, reference label only, bounded window, verification timestamp, and a plain-language confirmation that the referenced credential source was resolved outside repo | one current bounded-window record locator with a verification timestamp must be present and refreshed before the credential reference changes or the bounded supervised window rolls forward | the credential reference changes or the bounded supervised window rolls forward | the repo can point to a current attestation record for this face without exposing secret material |
| `venue_ref_face` | `named_operator_owner_plus_venue_owner_outside_repo` | attestor names, venue reference label, bounded window, verification timestamp, and explicit match confirmation between the marker and the intended venue | one current bounded-window record locator with a verification timestamp must be present and refreshed before the venue reference changes, venue routing changes, or the supervised window is rescheduled | the venue reference changes, venue routing changes, or the supervised window is rescheduled | the venue attestation is current, explicit, and reviewable without requiring the reviewer to infer the mapping |
| `account_ref_face` | `named_operator_owner_outside_repo` | attestor name, account reference label, bounded window, verification timestamp, and a statement that the external account binding was checked outside repo | one current bounded-window record locator with a verification timestamp must be present and refreshed before the account reference changes or a different demo account is selected for the window | the account reference changes or a different demo account is selected for the window | the account attestation makes the intended demo account explicit enough to reopen gate review |
| `connectivity_profile_face` | `named_operator_owner_plus_connectivity_owner_outside_repo` | attestor names, connectivity profile label, verification timestamp, bounded window, and a short reachability result | one current bounded-window record locator with a verification timestamp must be present and refreshed before network routing changes, connectivity profile changes, or the verification timestamp is outside the current window | network routing changes, connectivity profile changes, or the verification timestamp is outside the current window | the connectivity attestation is current enough that a gate reviewer can treat reachability as explicitly checked |
| `operator_owner_face` | `demo_operator_lead_outside_repo` | owner name or handle, verification timestamp, window label, and explicit ownership statement | one current bounded-window record locator with a verification timestamp must be present and refreshed before the named owner changes or the supervised window changes | the named owner changes or the supervised window changes | the owner attestation is explicit enough that gate recheck does not rely on unnamed responsibility |
| `bounded_start_criteria_face` | `named_operator_owner_outside_repo` | planned start window, bounded window minutes, go/no-go owner, abort owner, verification timestamp, and explicit stop condition note | one current bounded-window record locator with a verification timestamp must be present and refreshed before the scheduled window moves or ownership for go/no-go or abort changes | the scheduled window moves or ownership for go/no-go or abort changes | the bounded-start attestation makes timing and ownership explicit enough to reopen gate review |
| `allowlist_symbol_lot_reconfirmed` | `named_operator_owner_outside_repo` | attestor name, verification timestamp, allowlist values, lot-size values, position cap, and a plain-language reconfirmation note | one current bounded-window record locator with a verification timestamp must be present and refreshed before any guardrail value changes or the supervised window moves | any guardrail value changes or the supervised window moves | the guardrail attestation is current enough that gate recheck can treat the bounded demo envelope as explicitly reconfirmed |
| `manual_latched_stop_all_visibility_reconfirmed` | `named_operator_owner_outside_repo` | attestor name, verification timestamp, referenced stop-all surface, and a plain-language visibility confirmation | one current bounded-window record locator with a verification timestamp must be present and refreshed before the stop-all surface changes or the window advances without reconfirmation | the stop-all surface changes or the window advances without reconfirmation | the stop-all visibility attestation is current enough to reopen gate review without assuming prior visibility still holds |
| `terminal_snapshot_readability_reconfirmed` | `named_operator_owner_outside_repo` | attestor name, verification timestamp, referenced snapshot surface, and a short readability confirmation | one current bounded-window record locator with a verification timestamp must be present and refreshed before the snapshot format changes or the supervised window advances without reconfirmation | the snapshot format changes or the supervised window advances without reconfirmation | the snapshot-readability attestation is current enough that a gate reviewer can rely on terminal visibility without inference |
