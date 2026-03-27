# DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_EXTERNAL_EVIDENCE_CONTRACT

## Goal
Define one canonical non-secret outside-repo evidence intake contract for the remaining retry-gate blockers so refresh and regeneration can consume the same machine-validated truth source while staying fail-closed.

## Boundary
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
- planner boundary remains `prepare / start / status / stop / snapshot`
- `manual_latched_stop_all` remains planner-owned
- funded live forbidden

## Canonical Manifest
- Path: `manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json`
- Kind: `demo_forward_supervised_run_retry_gate_external_evidence_manifest`
- Role: `template` or `evidence`
- Contract is non-secret by construction: it stores only reviewable locator references, timestamps, attestors, and plain-language notes.

## Required Top-Level Fields
- `manifest_kind`
- `schema_version`
- `manifest_role`
- `updated_at`
- `bounded_supervised_window.label`
- `bounded_supervised_window.starts_at`
- `bounded_supervised_window.ends_at`
- `faces`

## Required Face Fields
Every required face must be represented explicitly:
1. `external_credential_source_face`
2. `venue_ref_face`
3. `account_ref_face`
4. `connectivity_profile_face`
5. `operator_owner_face`
6. `bounded_start_criteria_face`
7. `allowlist_symbol_lot_reconfirmed`
8. `manual_latched_stop_all_visibility_reconfirmed`
9. `terminal_snapshot_readability_reconfirmed`

Each face entry carries:
- `provided`
- `attested_by`
- `evidence_locator`
- `locator_kind`
- `verified_at`
- `fresh_until`
- `reviewable_without_secrets`
- `reviewability_note`
- `summary`
- `marker_match_note`
- `operator_input_remaining`

## Validator Output
The canonical validator must answer, per face:
- present?
- current?
- fresh enough?
- reviewable?
- stale?
- why blocked?
- what still needs operator input?

Required gap surfaces:
- machine-readable: `artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-check.json`
- human-readable: `artifacts/reports/demo-forward-supervised-run-retry-gate-external-evidence-gap-report.md`

## Fail-Closed Rule
- `PASS` only if the canonical manifest role is `evidence`, every required face is present, current, fresh enough, reviewable without secrets, and the bounded supervised window is still active enough for retry-gate review.
- `FAIL/BLOCKED` for missing manifests, invalid manifests, template-only manifests, incomplete faces, stale windows, non-reviewable locators, or any ambiguity.

## Refresh / Regeneration Integration
- Refresh consumes the canonical gap output for presence, freshness, and reviewability.
- Regeneration consumes the same canonical gap output for freshness inheritance and regenerated-face reviewability.
- Neither lane may fabricate pass status when the canonical manifest is absent, placeholder-only, incomplete, stale, or non-reviewable.
