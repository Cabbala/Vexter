# Demo Forward Supervised Run Retry Gate Attestation Refresh Sub-agent Summaries

## Anscombe
- Confirmed that refresh must become the single current surface atomically across status, report, summary, proof, handoff, checklist, and decision-surface pointers, with record-pack retained only as baseline evidence.
- Recommended keeping the lane observational and fail-closed: the repo may define refresh ownership and freshness rules, but retry-gate review stays blocked until each face points to one current, fresh-enough locator.
- Flagged split-pointer drift as the main risk, so the generator switches repo-level current-task metadata, bundle metadata, and handoff/report pointers together.

## Euler
- Kept the refresh boundary identical to the current bounded envelope: Dexter-only `paper_live`, frozen Mew-X `sim_live`, `single_sleeve`, `dexter_default`, explicit allowlist, small lot, one-plan, one-position, bounded supervision, and funded-live forbidden.
- Confirmed the refresh lane should baseline from attestation record pack rather than attestation audit, and that the row schema should shift to refresh owner, refresh trigger, minimum fresh evidence locator shape, stale condition, and retry-gate usability.
- Found no planner or adapter seam drift: refresh remains docs/proofs/report/script only, with `prepare / start / status / stop / snapshot` and `manual_latched_stop_all` unchanged.

## Parfit
- Scoped the smallest safe change set to one new refresh generator, one focused refresh regression, synchronized current-task assertions in shared tests, and a bundle default-path update.
- Recommended validating the new generator and bundle output first, then running the full pytest suite because many tests pin the repo-level current task, next task, and bundle path.
- Merge readiness depends on an honest blocked result, regenerated refresh artifacts, and a next-step pointer that advances to record-pack regeneration instead of claiming retry-gate reopen.
