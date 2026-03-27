# Demo Forward Supervised Run Retry Gate Attestation Refresh Sub-agent Summaries

## Anscombe
- Confirmed PR `#86` / merge commit `2be10c663f8d5f441defeea5f506108d1aae25c3` is latest merged `main`, while repo-level current pointers still point at regeneration, so refresh has to be re-promoted atomically from that newer baseline.
- Flagged summary, context, manifest, ledger, README, bundle path/source, and handoff continuity as the minimum pointer set that must move together so refresh becomes current and regeneration returns to the blocked next step.
- Called out partial flips as the main correctness risk because stale pre-PR `#86` refresh metadata, duplicated refresh clauses, or lingering regeneration-current flags would make the handoff internally inconsistent.

## Euler
- Confirmed no architecture drift: the planner boundary stays `prepare / start / status / stop / snapshot`, `manual_latched_stop_all` stays planner-owned, Dexter remains `paper_live`, and frozen Mew-X remains `sim_live`.
- Kept the fail-closed split crisp: refresh owns freshness, owner, trigger, locator-shape, and staleness while regeneration owns regenerated-face derivation and reviewability, and both keep `supervised_run_retry_gate` as pass successor only.
- Recommended only light wording normalization so refresh remains auditable without widening scope or implying retry execution success.

## Parfit
- Scoped the minimal file set to the refresh generator, current-pointer tests, `build_proof_bundle.sh`, and a refresh-side closeout exporter so the final tarball can be generated reproducibly.
- Recommended regenerating refresh artifacts from the generator first, then validating focused current-pointer regressions before widening to the shared pytest suite.
- Merge readiness depends on exact agreement across summary, context, manifest, ledger, README, refresh bundle path/source, and PR `#86` metadata on branch `codex/attestation-refresh-repromotion-after-pr86`.
