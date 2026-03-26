# TASK-007-TRANSPORT-RUNTIME-SMOKE

## 1. 目的
`TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-IMPLEMENTATION` で実装済みになった handle-based executor transport が、runtime-like 状態遷移・idempotency・reconciliation・rollback semantics まで bounded に成立していることを smoke で示す。

## 2. 現在の source-of-truth
- Latest merged Vexter task: PR `#44`
- Dexter main pinned: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` (PR `#3`)
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## 3. 固定前提
- promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- comparison source of truth: `comparison_closed_out`
- promoted live winner mode: `derived`
- promoted replay winner mode: `derived`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- confirmatory residual overturns promoted baseline: `no`

### 固定 transport conclusion
- `PlanStore` is pre-runtime immutable batch persistence only
- `ExecutorRegistry` is in-process adapter lookup only
- `ExecutorAdapter` concretely owns handle allocation, idempotency, source-faithful mode selection, stop confirmation, and poll-first reconciliation
- `StatusSink` is normalized runtime fan-in only
- `prepare` is the only full-plan command
- `handle_id` is the stable runtime identity
- `start/status/stop/snapshot` address the same handle
- reverse-order rollback stop fanout, planner stop-reason preservation, and no cross-source handoff remain fixed
- implementation stays bounded to in-memory adapter-owned runtimes; external wire choice, subprocess topology, and numeric timing constants remain deferred

## 4. このタスクでやること
1. GitHub 上の最新 merged state を確認
2. 実装済み transport implementation outputs を formal baseline として再確認
3. transport runtime smoke を追加 / 実行
4. 少なくとも以下を検証
   - handle-based runtime progression across `prepare/start/status/stop/snapshot`
   - duplicate `prepare/start/stop` が idempotent に扱われる
   - poll-first reconciliation が `status()` と `snapshot()` fallback で bounded に成立する
   - transport-originated failure が normalized `FailureDetail` / `StatusSnapshot` に落ちる
   - reverse-order rollback stop fanout が active handles に対して完了する
5. source-faithful Dexter `paper_live` / Mew-X `sim_live` stub seams で evidence 化
6. tests / summary / context_pack / proof manifest / task ledger / report / handoff bundle を更新
7. 次タスクを
   - `livepaper_observability_spec`
   - `executor_boundary_code_spec`
   - `transport_livepaper_smoke`
   のどれに切るべきか evidence ベースで提案

## 5. 実務上の狙い
このタスクのゴールは、transport contract が spec と実装の両方で整っただけでなく、runtime-like にも破綻していないことを確認すること。

## 6. 不変条件
- Dexter strategy semantics / trust logic / thresholds は変更しない
- Mew-X source logic は変更しない
- validator rules の再変更はしない
- current frozen source pins は維持
- funded live trading はしない
- comparison baseline は reopen しない
- 新 evidence collection は行わない
