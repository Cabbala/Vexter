# TASK-008 Details

## Objective

Audit whether upstream `FLOCK4H/Dexter` `v3.0.1` can be adopted into the Dexter implementation currently pinned by Vexter without breaking Vexter's bounded seam, planner/runtime invariants, replay assumptions, or fail-closed demo path.

## Inputs Used

- attached audit bundle task brief
- Vexter local repo state
- `Cabbala/Dexter` pinned commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- upstream `FLOCK4H/Dexter` tag `v3.0.1` commit `1a31624906114150b4f05a0f8103af0ad383ebe7`
- Vexter planner/router specs, scripts, manifests, and watchdog code that assert the current seam

## Method

1. Verified the Vexter pin and the exact files that encode Dexter ownership, mode, env, stop-all, and proof expectations.
2. Fetched the fork and upstream tag directly from GitHub and compared them tree-to-tree.
3. Classified each changed path against Vexter's bounded seam.
4. Mapped exact Vexter touchpoints that would need change if the source pin moved.
5. Recommended the smallest safe path that preserves current invariants.

## Limitation

The task brief requested named sub-agents. Interactive sub-agent spawning was not available for this run, so the Anscombe / Euler / Parfit lenses were executed in the main thread and captured in `subagent_summary.md`.

