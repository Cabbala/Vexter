# TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-SPEC Summary

- Started from merged live-paper smoke on PR `#42` without reopening comparison work or changing frozen source logic.
- Fixed transport ownership across `PlanStore`, `ExecutorRegistry`, `ExecutorAdapter`, and `StatusSink`.
- Fixed one bounded process model: one in-process planner/router plus one long-lived executor runtime per `executor_profile_id`.
- Fixed handle-based request/response envelopes, mandatory idempotent `prepare/start/stop`, ack/failure normalization, stop confirmation, and poll-first status reconciliation.
- Kept wire choice, auth, host placement, and numeric timeout/retry/poll constants deferred.
- Validation result: `./scripts/build_proof_bundle.sh` and `pytest -q` -> `64 passed`
