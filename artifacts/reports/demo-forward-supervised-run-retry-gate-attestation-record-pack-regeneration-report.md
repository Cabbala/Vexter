# Demo Forward Supervised Run Retry Gate Attestation Record Pack Regeneration Report

## Verified GitHub State
- Reverified latest GitHub-visible Vexter `main` at merged PR `#107` merge commit `25f272971acccf22098999405bdeac7fa07d9ba6` on `2026-03-28T18:46:06Z`.
- Dexter stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen Mew-X stayed pinned at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Report timestamp: `2026-03-28T19:11:05Z`.

## Baseline Accepted
- Accepted `supervised_run_retry_gate_attestation_refresh_blocked` as the bounded baseline current source of truth.
- Did not claim retry-gate reopen, retry execution success, funded live access, new external evidence collection success, or any Mew-X seam expansion.
- Promoted one bounded attestation record-pack regeneration lane as the new current source of truth for regenerated face ownership, triggers, inheritance rules, and reviewer-readable pack pointers.
- Kept regeneration consuming the shared canonical outside-repo evidence manifest template, validator, and evidence preflight / compatibility gap surface from the current refresh baseline.
- Kept the canonical manifest honest at `template_only` and the evidence preflight fail-closed while required external evidence remains missing or stale.

## Regeneration Boundary
- Dexter-only real demo slice
- `single_sleeve`
- `dexter_default`
- Dexter `paper_live`
- frozen Mew-X `sim_live`
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded supervised window required
- external credential refs remain outside repo
- operator owner explicit
- venue / connectivity confirmation explicit
- bounded start criteria explicit
- allowlist / symbol / lot-size reconfirmation explicit
- `manual_latched_stop_all` visibility reconfirmation explicit
- terminal snapshot readability reconfirmation explicit
- Mew-X unchanged
- funded live forbidden

## Decision
- Outcome: `FAIL/BLOCKED`
- Decision: `retry_gate_review_blocked_pending_current_attestation_record_pack_regeneration`
- Current lane: `supervised_run_retry_gate_attestation_record_pack_regeneration`
- Recommended next step while blocked: `supervised_run_retry_gate_attestation_refresh`
- Retry-gate pass successor: `supervised_run_retry_gate`
- Runtime validation errors: `[]`

## Regeneration Surfaces
- current status report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-status.md`
- current report: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-report.md`
- current summary: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-summary.md`
- current proof json: `artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration-check.json`
- current handoff: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/HANDOFF.md`
- record-pack regeneration checklist: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_checklist.md`
- record-pack regeneration decision surface: `docs/demo_forward_supervised_run_retry_gate_attestation_record_pack_regeneration_decision_surface.md`
- current sub-agent summary: `artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-record-pack-regeneration/SUBAGENTS.md`

## Canonical External Evidence
- contract spec: `specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_EXTERNAL_EVIDENCE_CONTRACT.md`
- manifest template: `manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json`
- preflight proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json`
- preflight report: `artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md`
- preflight summary: `artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-summary.md`
- gap proof: `artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-check.json`
- gap report: `artifacts/reports/demo-forward-supervised-run-retry-gate-external-evidence-gap-report.md`
- gap summary: `artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-summary.md`
- manifest status: `template_only`
- preflight status: `blocked`
- blocked faces from canonical validator: `external_credential_source_face, venue_ref_face, account_ref_face, connectivity_profile_face, operator_owner_face, bounded_start_criteria_face, allowlist_symbol_lot_reconfirmed, manual_latched_stop_all_visibility_reconfirmed, terminal_snapshot_readability_reconfirmed`
- aggregated blocked reasons: `{"attestors_missing": 9, "bounded_window_missing": 9, "evidence_locator_missing": 9, "fresh_until_missing": 9, "locator_kind_missing": 9, "outside_repo_locator_not_supplied": 9, "template_only_manifest": 9, "verification_timestamp_missing": 9}`
- canonical face-to-manifest map: `artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md` under `Face-To-Manifest And Proof Map`
- template-only false path: `Manifest remains template_only, so retry-gate reopen stays blocked until the bounded supervised window fields are filled once, every blocked face carries a current non-secret reviewable locator, and the canonical preflight returns ready.`
- consistency checks: `{"blocked_face_count_matches_face_rows": true, "blocked_face_names_match_face_rows": true, "blocked_faces_have_manifest_fields_and_operator_input": true, "blocked_reason_counts_match_face_rows": true, "operator_inputs_remaining_match_blocked_faces": true, "template_only_false_path_holds": true}`

## Next Human Pass
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

## Regeneration Findings
- required regeneration faces: `9`
- regeneration rules explicit count: `9`
- per-face manifest field maps explicit count: `9`
- per-face proof path maps explicit count: `9`
- current fresh locator input count: `0`
- freshness inherited cleanly count: `0`
- regenerated face reviewable count: `0`
- blocked regenerated faces: `external_credential_source_face, venue_ref_face, account_ref_face, connectivity_profile_face, operator_owner_face, bounded_start_criteria_face, allowlist_symbol_lot_reconfirmed, manual_latched_stop_all_visibility_reconfirmed, terminal_snapshot_readability_reconfirmed`
- canonical gap blocked faces align with regeneration lane: `yes`
- template-only reopen-ready remains false across canonical preflight and regeneration lane: `yes`

## Honest Regeneration Model
- `PASS` only if refreshed locator rules produce a current, reviewable regenerated record pack sufficient to reopen retry-gate review honestly.
- `FAIL/BLOCKED` if one or more regenerated faces remain missing, stale, ambiguous, or non-reviewable.
- Current result remains `FAIL/BLOCKED` because the canonical manifest is `template_only`, the preflight status remains `blocked`, and the repo still does not point to one current, fresh-enough, reviewable locator per required face, so the regenerated current pack cannot reopen retry-gate review honestly.
