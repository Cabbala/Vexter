# TASK-007-MONITOR-KILLSWITCH-SPEC Summary

- Started from merged planner/router runtime smoke on PR `#40` without reopening comparison work or changing frozen source logic.
- Fixed the source-faithful monitor profile, admission gate, timeout envelope, quarantine scope, global halt, and typed failure-escalation contract.
- Added contract tests for active global halt, Mew-X timeout-tolerant monitoring, immutable per-sleeve monitor binding, and failure-code coverage.
- Added a runtime invalid-transition regression so typed `invalid_status_transition` rollback is directly exercised on the runtime-smoke lane.
- Kept numeric heartbeat, retry, timeout, and escalation thresholds deferred as bounded defaults.
- Validation result: `pytest -q` -> `58 passed`
