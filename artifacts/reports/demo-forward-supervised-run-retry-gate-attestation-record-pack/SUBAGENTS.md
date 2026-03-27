# Demo Forward Supervised Run Retry Gate Attestation Record Pack Sub-agent Summaries

## Anscombe
- Confirmed the minimum safe change is a new attestation-record-pack lane beside attestation audit, with one atomic current-pointer switch across status, report, proof, summary, handoff, checklist, and decision-surface paths.
- Recommended fail-closed wording that stays observational: the repo may define each record face clearly, but retry-gate review remains blocked until every face points to a current, timestamped, reviewable record locator.
- Flagged the main consistency risks as baseline-hop drift, split current pointers, and mixed record-pack naming; the new pack should baseline from attestation audit and become the single current source of truth once written.

## Euler
- Kept the record-pack boundary aligned with the accepted audit boundary: Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, explicit allowlist, small lot, one-plan, one-position, bounded supervision, and funded-live forbidden.
- Confirmed the same nine required faces must remain unchanged and that the lane should stay docs-and-proof only, without planner or adapter seam drift.
- Reviewed the state split and emphasized that `prepare / start / status / stop / snapshot` remains fixed, `manual_latched_stop_all` stays planner-owned, and Mew-X remains unchanged while the record pack stays fail-closed.

## Parfit
- Scoped the smallest safe change set to one new proof generator, one focused record-pack test, README and default-bundle updates, generated artifact refreshes, and the shared tests that pin the current supervised-run lane.
- Recommended validating with the new generator plus focused supervised-run and bootstrap/compatibility pytest coverage, then full `pytest -q`, because several shared tests key off the repo-level current task, bundle path, and next-task state.
- Merge readiness depends on a clean record-pack pointer switch, regenerated tarball output, updated GitHub main metadata, and a blocked decision that does not claim retry-gate reopen or retry execution success.
