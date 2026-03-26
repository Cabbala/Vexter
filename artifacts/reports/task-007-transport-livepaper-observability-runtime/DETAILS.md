# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-RUNTIME

## 1. 目的
最新 GitHub-visible `main` では `TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-SMOKE` まで完了し、
その結論は
- `executor_transport_livepaper_observability_smoke_passed`
- `transport_livepaper_observability_smoke_bounded`
- `recommended next step: transport_livepaper_observability_runtime`
で確定している。

したがって次は、新証拠の収集や comparison baseline の再評価ではなく、
**実装済み executor transport の live-paper observability surface が runtime-oriented path でも崩れないことを確認すること**
が正しい次段。

## 2. 現在の source-of-truth
- Latest merged Vexter task: PR `#48`
- Supporting merged Vexter states:
  - PR `#47`: transport_livepaper_observability_smoke
  - PR `#46`: transport_livepaper_smoke
  - PR `#45`: transport_runtime_smoke
  - PR `#44`: planner_router_executor_transport_implementation
  - PR `#43`: planner_router_executor_transport_spec
  - PR `#42`: planner_router_livepaper_smoke
  - PR `#41`: monitor_killswitch_spec
  - PR `#40`: planner_router_runtime_smoke
  - PR `#39`: planner_router_integration_smoke
  - PR `#38`: planner_router_code_implementation
  - PR `#37`: concrete_planner_router_code_spec
  - PR `#36`: concrete_planner_router_implementation_spec
  - PR `#35`: planner_router_interface_spec
  - PR `#34`: implementation_planning
  - PR `#33`: execution_planning
  - PR `#32`: strategy_planning
  - PR `#31`: risk_containment_vs_exit_capture
  - PR `#30`: execution_timing_vs_retention
  - PR `#29`: candidate_generation_vs_quality
  - PR `#28`: downstream_research_intake
  - PR `#27`: research_handoff / comparison_closeout continuation
  - PR `#26`: comparison_closeout
  - PR `#25`: downstream comparative analysis
  - PR `#24`: replay surface fix
  - PR `#23`: replay gap analysis
  - PR `#22`: replay deepening
  - PR `#21`: replay validation intake
  - PR `#20`: validator rule implementation
  - PR `#19`: validator rule review
  - PR `#18`: validator contract audit
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

### 固定 observability conclusion
- immutable handoff metadata is traceable from planner-owned `planned` storage into prepared live-paper handles and the shared status sink
- handle lifecycle, first-vs-duplicate ack metadata, quarantine reason, manual halt propagation, and snapshot-backed terminal detail remain visible end to end
- normalized `status_timeout` failure detail preserves source reason passthrough plus source-faithful rollback snapshot context
- remaining risk is runtime-oriented observability continuity, not basic transport coherence

## 4. このタスクでやること
1. GitHub 上の最新 merged state を確認
2. transport live-paper observability smoke outputs を formal baseline として再確認
3. observability runtime lane を追加 / 実行
4. 少なくとも以下を検証
   - immutable handoff metadata が runtime-oriented path を通じても trace continuity を保つ
   - handle lifecycle と status sink snapshots が runtime progression 全体で一貫する
   - first-vs-duplicate ack visibility が runtime follow-up 後も保持される
   - quarantine reason / manual stop-all propagation / snapshot terminal detail が runtime-like 継続経路でも end-to-end で観測可能
   - normalized failure detail が runtime-oriented path でも source-faithful passthrough を保つ
5. tests / summary / context_pack / proof manifest / task ledger / report / handoff bundle を更新
6. 次タスクを
   - `livepaper_observability_spec`
   - `executor_boundary_code_spec`
   - `transport_livepaper_observability_hardening`
   のどれに切るべきか evidence ベースで提案
7. branch → commit(s) → push → PR作成/更新 → 可能なら merge

## 5. 実務上の狙い
このタスクのゴールは、
**live-paper seam で観測可能だった transport metadata / status / failure / stop information が runtime-oriented path でも崩れないことを確認すること**。

## 6. 不変条件
- Dexter strategy semantics / trust logic / thresholds は変更しない
- Mew-X source logic は変更しない
- validator rules の再変更はしない
- current frozen source pins は維持
- funded live trading はしない
- comparison baseline は reopen しない
- 新 evidence collection は行わない
- GitHub visible artifacts を source of truth にする
