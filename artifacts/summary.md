# TASK-007-MONITOR-KILLSWITCH-SPEC Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#40` main commit `a4e7a3c74460dc711c3e2897ac31386272e91c27` on `2026-03-26T02:45:48Z`.
- Supporting merged Vexter states remained PR `#39` `a293d6e9260bd092297140bc82469802d6fce115`, PR `#38` `b1ceac48af931db0571a25ea197b1e4e5df52543`, PR `#37` `786221a664637925f790e89af0448fa04832426e`, PR `#36` `8713b9ba8de82accda48526fdff8732531d7b620`, PR `#35` `2bec1badde788ef1c75251af2df17609643720fb`, PR `#34` `981f0977788cffd10de4bf78f14e5b430fbce4c1`, PR `#33` `c6dfaee621e3eea08ceec1cfba7f0fe65a5918fc`, PR `#32` `a214ff04f0662e250b01181551a8963ce8e80dd6`, PR `#31` `0905ec8c991ca6046b13d0c326c3224c49709a2d`, PR `#30` `052de6ccecef1461d2291fb4f0ef5fbf8883d548`, PR `#29` `17af013b0383fd142e15932108c8b4da5447f1f7`, PR `#28` `4df259b90365787ac24085227fcc1b15b63d057d`, PR `#27` `d8149e624b9682e2da55ac4bfcaa30fcaa3d94df`, PR `#26` `9d235176e628e0fcbdcf2182ce83def25f6a6b02`, PR `#25` `727589b40d26c453c2fef78dc5060aa1098c1aad`, PR `#24` `2c8b654fde4b4fcff11f3ecca2e1f4d27ceb610d`, PR `#23` `eaa5acc2f189d5bea5c55f9de059d8e6a8d36091`, PR `#22` `3db6d3e73c4a6d990e0fdf8fba33b31a3a436c5b`, PR `#21` `d7845b665afc912da593f2601e6a3d39524964d0`, PR `#20` `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668`, PR `#19` `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, and PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Task Did

- Started from merged planner/router runtime smoke on PR `#40` and kept the promoted comparison baseline frozen.
- Fixed the source-faithful monitor/kill-switch contract against the already-proven planner/router runtime seam.
- Added contract tests for monitor profile classes, active global halt rejection, Mew-X timeout-tolerant monitoring, immutable per-sleeve monitor binding, and failure-code coverage.
- Added a runtime invalid-transition regression so typed `invalid_status_transition` rollback is exercised directly on the runtime-smoke lane.
- Updated task artifacts and refreshed the proof bundle for TASK-007 monitor/kill-switch spec.

## Monitor/Kill-Switch Surface

- Monitor profiles remain immutable per-plan bindings: `dexter_default` stays `lifecycle_control / dexter_lifecycle_control / sleeve / true`, and `mewx_timeout_guard` stays `timeout_aware / mewx_timeout_tolerant / sleeve / true`.
- Admission gates remain pre-emission and fail closed on config invalidity, pin mismatch, disabled sleeve, budget overflow, or active global halt.
- Timeout envelopes stay source-shaped rather than numerically finalized: Dexter keeps lifecycle-control monitoring, while Mew-X accepts source-native `inactivity_timeout` and quarantines only when the lifecycle exceeds the configured envelope or misses normalized close/shutdown confirmation.
- Quarantine stays sleeve-scoped, global halt stays `manual_latched_stop_all`, and typed failure escalation remains on `FailureCode` / `FailureDetail` / `StatusSnapshot` with source-native reasons as passthrough metadata.
- Validation result: `pytest -q` -> `58 passed`

## Decision

- Outcome: `A`
- Key finding: `monitor_killswitch_contract_fixed`
- Claim boundary: `monitor_killswitch_spec_bounded`
- Current task status: `monitor_killswitch_spec_ready`
- Recommended next step: `planner_router_livepaper_smoke`
- Decision: `planner_router_livepaper_smoke_ready`

## Key Paths

- Monitor/kill-switch report: `artifacts/reports/task-007-monitor-killswitch-spec-report.md`
- Monitor/kill-switch status: `artifacts/reports/task-007-monitor-killswitch-spec-status.md`
- Monitor/kill-switch proof: `artifacts/proofs/task-007-monitor-killswitch-spec-check.json`
- Monitor/kill-switch summary: `artifacts/proofs/task-007-monitor-killswitch-spec-summary.md`
- Monitor/kill-switch prompt pack: `artifacts/reports/task-007-monitor-killswitch-spec`
- Monitor/kill-switch bundle: `artifacts/bundles/task-007-monitor-killswitch-spec.tar.gz`
