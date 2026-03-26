# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG-RUNTIME

## 1. 目的
最新 GitHub-visible `main` では `TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG` まで完了し、
その結論は
- `executor_transport_livepaper_observability_watchdog_passed`
- `transport_livepaper_observability_watchdog_bounded`
- `recommended next step: transport_livepaper_observability_watchdog_runtime`
で確定している。

したがって次は、新証拠の収集や comparison baseline の再評価ではなく、
**watchdog で定義した drift / omission / partial-visibility 検知が runtime-oriented path でも崩れないことを確認すること**
が正しい次段。

## 2. 現在の source-of-truth
- Latest merged Vexter task state is the watchdog lane reflected in `artifacts/summary.md`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Open Vexter PR `#50` remains non-authoritative relative to merged `main`.

## 3. 固定前提
- promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- comparison source of truth: `comparison_closed_out`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- confirmatory residual overturns promoted baseline: `no`

### 固定 watchdog conclusion
- required observability field omission is watchdog-detected
- handle lifecycle continuity drift is watchdog-detected
- planned-versus-runtime metadata drift is watchdog-detected
- partial status-sink fan-in is watchdog-detected
- ack-history retention loss is watchdog-detected
- quarantine-reason omission is watchdog-detected
- manual stop-all propagation loss is watchdog-detected
- terminal snapshot gaps and normalized failure-detail passthrough loss are watchdog-detected
- remaining risk is runtime-oriented continuity of the watchdog surface, not missing watchdog categories

## 4. このタスクでやること
1. GitHub 上の最新 merged state を確認
2. watchdog outputs を formal baseline として再確認
3. watchdog runtime lane を追加 / 実行
4. 少なくとも以下を検証
   - runtime-oriented follow-up でも required field omission が検知できる
   - handle lifecycle continuity drift と planned/runtime metadata drift が follow-up path でも検知できる
   - partial status-sink fan-in / ack-history truncation / quarantine omission / manual stop-all propagation loss が runtime-oriented経路でも検知できる
   - terminal snapshot gaps と normalized failure-detail passthrough loss が runtime-oriented path でも検知できる
5. tests / summary / context_pack / proof manifest / task ledger / report / handoff bundle を更新
6. 次タスクを
   - `livepaper_observability_spec`
   - `executor_boundary_code_spec`
   - `transport_livepaper_observability_watchdog_regression_pack`
   のどれに切るべきか evidence ベースで提案
7. branch → commit(s) → push → PR作成/更新 → 可能なら merge

## 5. 実務上の狙い
このタスクのゴールは、
**“watchdog がある”状態から“runtime-oriented follow-up でも watchdog が効く”状態へ進めること**。

## 6. 不変条件
- Dexter strategy semantics / trust logic / thresholds は変更しない
- Mew-X source logic は変更しない
- validator rules の再変更はしない
- current frozen source pins は維持
- funded live trading はしない
- comparison baseline は reopen しない
- 新 evidence collection は行わない
- GitHub visible artifacts を source of truth にする
