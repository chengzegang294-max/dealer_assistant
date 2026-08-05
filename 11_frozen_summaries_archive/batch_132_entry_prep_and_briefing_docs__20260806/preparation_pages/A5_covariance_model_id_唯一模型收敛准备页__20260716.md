# A5 covariance_model_id 唯一模型收敛准备页

更新时间：2026-07-16

## 用途

- 在 `minimum_stability_checked__not_ready` 后，
  把下一手正式收缩到“唯一模型收敛准备”。
- 这页不直接定稿唯一模型。
- 这页只负责：
  - 说明为什么现在可以开始讨论唯一模型收敛
  - 冻结唯一模型收敛至少要满足什么
  - 说明当前不应提前写成什么

## 当前结论

- 当前 `covariance_model_id` 已完成：
  - `benchmark_relative_sample_covariance` 的 current / adjacent 两窗口 fresh-run
  - `minimum_stability_checked__not_ready`
- 当前最顺下一手不是：
  - 直接写成 `ready`
  - 回头重新开 provider 讨论
  - 立刻把三段输出全部重判
- 当前最顺下一手是：
  - 判断 `benchmark_relative_sample_covariance`
    是否已足以从“候选家族第一顺位”继续收敛为“唯一活动实现候选”

## 一、当前为什么能进入这一步

- 当前已不再只有：
  - 单次 first fresh-run
- 当前已补齐：
  - 相邻窗口 second fresh-run
  - 最小稳定性检查 `passed`
- 因此当前已经具备：
  - 讨论“是否继续保留其它候选家族”的最低证据基础

## 二、唯一模型收敛至少要看什么

- 至少看：
  - 当前单家族是否连续两窗口都能稳定产出 PSD 矩阵
  - 当前是否仍存在必须立刻并跑 `shrinkage / factor-implied` 的硬理由
  - 当前下游三段输出是否仍明确依赖“多候选并存”
  - 当前保留其它候选家族，是为了真实 NEED_EVIDENCE，还是只是旧口径残留

## 三、当前暂缓

- 暂缓：
  - 直接写 `unique_model_frozen`
  - 直接写 `risk_model_ready`
  - 直接解除三段输出的 `not_output_passed`

## 四、主负责人裁决

- 当前先做什么：
  - 把下一手正式切到唯一模型收敛判断准备
- 当前为什么先做这个：
  - 因为 stability 已补到最小可判断层，
    现在最值钱的不是继续机械加窗口，
    而是判断其它候选家族是否还必须保留
- 当前不做什么：
  - 不因为两窗口通过就直接把风险模型写成 ready

## 五、一句话口径

- 当前 `covariance_model_id` 的下一手已切到：
  - `唯一模型收敛准备`
- 当前这页的准备职责已完成，
  当前主线已继续推进到：
  - `sole_implementation_candidate_frozen__not_ready`

## 回链

- `A5_covariance_model_id_最小稳定性检查执行页__20260716.md`
- `A5_covariance_model_id_唯一模型收敛主负责人裁决页__20260716.md`
- `A5_covariance_model_id_唯一模型定稿准备页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
