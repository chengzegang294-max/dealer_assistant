# T02 候选分支裁决卡 v1

## 对应对象

- `T02`
- `watchlist` 弱候选分支

## 候选定义

- 基线口径：
  - `3% + 连续2日`
- 候选分支：
  - `2.5% + 连续2日 + 排除 G03_震荡`
- 当前只对两组弱候选评估：
  - `low_flow_vol`
  - `growth_tech_low_flow_vol`

## 并排结果

- `low_flow_vol`
  - baseline 密度：`0.3405`
  - looser candidate 密度：`0.3857`
  - filtered candidate 密度：`0.1571`
  - 相对 baseline 变化：`-0.1833`
  - 对 looser candidate 的保留率：`40.7%`
  - 当前判断：过滤后噪声下降明显，但覆盖率掉得过多
- `growth_tech_low_flow_vol`
  - baseline 密度：`0.2833`
  - looser candidate 密度：`0.3333`
  - filtered candidate 密度：`0.1333`
  - 相对 baseline 变化：`-0.1500`
  - 对 looser candidate 的保留率：`40.0%`
  - 当前判断：同样出现“降噪有效，但覆盖掉得太多”

## 当前裁决

- 当前结论：`不升级为微调`
- 当前归类：`继续保留在 watchlist`
- 原因：
  - `排除 G03_震荡` 的确是最有效的第一道过滤
  - 但一旦把它和 baseline 并排，两个弱层的 filtered candidate 密度都明显低于 baseline
  - 当前更像“有价值的观察型候选”，还不是“可接管默认逻辑的微调分支”

## 当前可执行口径

- 全局默认继续使用：
  - `3% + 连续2日`
- 弱候选观察分支继续保留：
  - `2.5% + 连续2日 + 排除 G03_震荡`
- `北向同向` 当前不作为第一道主过滤：
  - 只保留为后续二级加严条件

## 下一步方向

- 如果后续还要继续推进该候选，优先补的不是更松阈值，而是更强确认：
  - 看能否在不明显掉覆盖率的前提下，加上更轻的二级确认
- 当前更现实的升级条件应该是：
  - filtered candidate 覆盖率至少接近 baseline 的 `75%~90%`
  - 同时继续保持明显更低的 `G03` 噪声占比

## 回链

- 候选分支裁决表：
  - `artifacts/t02_candidate_branch/t02_candidate_branch_decision_latest.tsv`
- 候选分支摘要：
  - `artifacts/t02_candidate_branch/t02_candidate_branch_summary_latest.json`
- 确认条件过滤试算：
  - `artifacts/t02_confirmation_filter/t02_confirmation_filter_recommendation_latest.tsv`
- 局部微调建议：
  - `artifacts/t02_local_tuning/t02_local_tuning_recommendation_latest.tsv`
