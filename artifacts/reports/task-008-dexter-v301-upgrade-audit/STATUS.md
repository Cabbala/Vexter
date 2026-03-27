# TASK-008 Dexter v3.0.1 Upgrade Audit Status

- decision: `selective_cherry_pick_only`
- full_upgrade_safe: `no`
- merge_base: `none`
- changed_paths: `36`
- primary_breakers:
  - fork-only `paper_live` and `VEXTER_*` contract removed upstream
  - fork-only NDJSON / replay instrumentation removed upstream
  - upstream control plane owns `.env`, operator state, and runtime snapshots
  - upstream strategy/scoring semantics drift from the frozen comparison baseline
  - upstream tag has no Dexter `tests/` tree
- safest_now:
  - docs / packaging / helper leaf files only
- next_action:
  - use a compatibility branch from `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
  - keep `paper_live`, fork instrumentation, and current tests intact
  - evaluate parser / market / export ideas only behind the current seam

