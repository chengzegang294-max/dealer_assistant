# A5 adjusted_position_weight 最终融合 failure 样例页

更新时间：2026-07-18

## 用途

- 把 `adjusted_position_weight` 当前第二关键缺口压成正式一页。
- 这页不宣布：
  - `adjusted_position_weight output_passed`
  - `最终融合输出 ready`
- 这页只负责：
  - 冻结最终融合 failure / `abort_reason` 的最小样例口径
  - 写清什么情况必须中止
  - 说明补完后下一手为何应切到单点升级判断准备

## 当前结论

- 当前 `adjusted_position_weight` 仍只能写成：
  - `pass_conditions_drafted__not_output_passed`
- 当前可以正式写成：
  - 最终融合 failure 样例已冻结
- 这意味着当前已不再缺：
  - failure / `abort_reason` 的命名骨架

## 一、最小 failure 结构

- failure 样例至少必须带：
  - `adjusted_position_weight = null`
  - `target_weight_status`
  - `final_size_scalar`
  - `degrade_flags`
  - `abort_reason`
  - `audit_note`

## 二、推荐的最小 abort_reason 家族

- 推荐至少覆盖：
  - `missing_target_weight`
  - `invalid_final_size_scalar`
  - `final_size_scalar_below_abort_threshold`
  - `upstream_target_weight_not_consumable`
  - `degraded_chain_not_allowed_for_final_output`

## 三、当前必须中止的情况

- 一旦出现以下任一条，当前最终融合必须中止：
  - `target_weight` 不可消费
  - `final_size_scalar <= 0.05`
  - 降级链未显式展开 `degrade_flags`
  - 输出文字把降级链写成正式优化器最终输出

## 四、当前允许写法

- 允许写成：
  - 最终融合 failure / `abort_reason` 样例已冻结
  - `adjusted_position_weight` 当前已具备最小失败追溯骨架
- 禁止写成：
  - 最终融合已可正式运行
  - failure 样例已等于通过证据

## 五、主负责人裁决

- 当前不做：
  - 最终融合输出通过裁决
  - runtime 最终权重实现
- 当前正式裁决是：
  - 允许把最终融合 failure 样例视为已冻结
  - 当前下一手切到：
    - `adjusted_position_weight` 单点升级判断准备收口

## 六、一句话口径

- 当前 `adjusted_position_weight` 已继续补齐：
  - `最终融合 failure / abort_reason 样例`
- 但当前仍未到：
  - `正式最终输出通过`

## 六点五、2026-07-18 执行验证复位

- 本轮已新增真实 runtime 入口：
  - `02_runtime/a5_g5_adjusted_position_weight_validation/`
- 本轮已实际执行：
  - success generation
  - failure generation
- 本轮复跑确认：
  - `adjusted_position_weight = target_weight * final_size_scalar`
  - `gross_adjusted_weight = 0.240344`
  - `observed_abort_reason = final_size_scalar_below_abort_threshold`
- 这次执行新增证明的是：
  - 最终融合公式已进入 hard 证据层
  - failure `abort_reason` 已进入可复现层
- 这次执行不新增宣称：
  - `output_passed`
  - `组合层最终权重 ready`

## 回链

- `A5_adjusted_position_weight_升级判断准备页__20260716.md`
- `A5_adjusted_position_weight_final_size_scalar降级样例页__20260716.md`
- `A5_adjusted_position_weight_actual_generation_execution页__20260718.md`
- `A5_adjusted_position_weight_最小通过条件页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
