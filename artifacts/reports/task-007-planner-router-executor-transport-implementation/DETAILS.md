# TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-IMPLEMENTATION

## 1. 目的
`TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-SPEC` で固定した transport contract を、source-faithful な Dexter `paper_live` / Mew-X `sim_live` seam のまま Vexter 実装へ落とし込む。

## 2. 現在の source-of-truth
- Latest merged Vexter task: PR `#43`
- Dexter main pinned: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` (PR `#3`)
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## 3. 固定前提
- promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- comparison source of truth: `comparison_closed_out`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- confirmatory residual overturns promoted baseline: `no`

## 4. このタスクでやること
1. GitHub 上の最新 merged state を確認
2. spec の ownership / envelope / idempotency / stop-confirmation / reconciliation を実装へ反映
3. `ExecutorAdapter` / `ExecutorRegistry` / `PlanStore` / `StatusSink` の concrete bounded 実装を追加
4. `dispatch_state_machine` を transport-aware rollback / failure propagation へ更新
5. tests を追加 / 更新
6. summary / context_pack / proof manifest / task ledger / report / handoff bundle を更新
7. 次タスクを `transport_runtime_smoke` / `livepaper_observability_spec` / `executor_boundary_code_spec` から evidence ベースで提案

## 5. 実務上の狙い
このタスクのゴールは、planner/router control plane と source-faithful executor seams を、bounded だが実行可能な transport 実装で接続すること。

## 6. 不変条件
- Dexter strategy semantics / trust logic / thresholds は変更しない
- Mew-X source logic は変更しない
- validator rules の再変更はしない
- current frozen source pins は維持
- funded live trading はしない
- comparison baseline は reopen しない
- 新 evidence collection は行わない
