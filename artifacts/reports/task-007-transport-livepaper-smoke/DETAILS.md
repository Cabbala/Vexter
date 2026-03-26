# TASK-007-TRANSPORT-LIVEPAPER-SMOKE

## 1. 目的
最新 GitHub-visible `main` では `TASK-007-TRANSPORT-RUNTIME-SMOKE` まで完了し、
その結論は
- `executor_transport_runtime_smoke_passed`
- `transport_runtime_smoke_bounded`
- `recommended next step: transport_livepaper_smoke`
で確定している。

したがって次は、新証拠の収集や comparison baseline の再評価ではなく、
**実装済み executor transport が live-paper shaped seams でも bounded に成立していることを smoke で示すこと**
が正しい次段。

## 2. 現在の source-of-truth
- Latest merged Vexter task: PR `#45`
- Supporting merged Vexter states:
  - PR `#44`: transport_runtime_smoke
  - PR `#43`: planner_router_executor_transport_implementation
  - PR `#42`: planner_router_executor_transport_spec
  - PR `#41`: planner_router_livepaper_smoke
  - PR `#40`: monitor_killswitch_spec
  - PR `#39`: planner_router_runtime_smoke
  - PR `#38`: planner_router_integration_smoke
  - PR `#37`: planner_router_code_implementation
  - PR `#36`: concrete_planner_router_code_spec
  - PR `#35`: concrete_planner_router_implementation_spec
  - PR `#34`: planner_router_interface_spec
  - PR `#33`: implementation_planning
  - PR `#32`: execution_planning
  - PR `#31`: strategy_planning
  - PR `#30`: risk_containment_vs_exit_capture
  - PR `#29`: execution_timing_vs_retention
  - PR `#28`: candidate_generation_vs_quality
  - PR `#27`: downstream_research_intake
  - PR `#26`: research_handoff / comparison_closeout continuation
  - PR `#25`: comparison_closeout
  - PR `#24`: downstream comparative analysis
  - PR `#23`: replay surface fix
  - PR `#22`: replay gap analysis
  - PR `#21`: replay deepening
  - PR `#20`: replay validation intake
  - PR `#19`: validator rule implementation
  - PR `#18`: validator rule review
  - PR `#17`: structural gap closeout
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
2. 実装済み planner/router modules / transport runtime smoke outputs を formal baseline として再確認
3. transport live-paper smoke を追加 / 実行
4. 少なくとも以下を検証
   - live-paper shaped request が immutable plan handoff と source-faithful Dexter `paper_live` / Mew-X `sim_live` executor selectionへ結び付く
   - handle-based transport が live-paper seam でも `prepare/start/status/stop/snapshot` を通じて維持される
   - poll-first reconciliation と snapshot-backed stop confirmation が live-paper seam でも bounded に成立する
   - manual stop-all propagation と quarantine / stop semantics が live-paper active handles に対して成立する
   - transport-originated failure normalization が live-paper path でも保たれる
5. tests / summary / context_pack / proof manifest / task ledger / report / handoff bundle を更新
6. 次タスクを
   - `livepaper_observability_spec`
   - `executor_boundary_code_spec`
   - `transport_livepaper_observability_smoke`
   のどれに切るべきか evidence ベースで提案
7. branch → commit(s) → push → PR作成/更新 → 可能なら merge

## 5. 実務上の狙い
このタスクのゴールは、
**transport contract と transport 実装が runtime-like だけでなく live-paper shaped 運用 seam でも破綻していないことを確認すること**。

主に欲しいもの:
- live-paper transport smoke
- end-to-end handoff and stop confirmation evidence
- observability / boundary code spec 次段へ進む bounded confidence

## 6. 不変条件
- Dexter strategy semantics / trust logic / thresholds は変更しない
- Mew-X source logic は変更しない
- validator rules の再変更はしない
- current frozen source pins は維持
- funded live trading はしない
- comparison baseline は reopen しない
- 新 evidence collection は行わない
- GitHub visible artifacts を source of truth にする
