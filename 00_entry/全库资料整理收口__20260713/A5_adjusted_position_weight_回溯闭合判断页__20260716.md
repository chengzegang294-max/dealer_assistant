# A5 adjusted_position_weight 回溯闭合判断页

更新时间：2026-07-16

## 用途

- 把 `adjusted_position_weight` 从纯阻塞态，推进到“回溯闭合可判断”层。
- 这页不是最终权重实现页。
- 这页也不是在宣布最终权重已可直接运行。
- 这页只负责：
  - 冻结当前最小回溯链
  - 写清中止条件、允许写法与禁止误写
  - 作为 `G5` 主链当前最后一段的正式判断页

## 当前结论

- `adjusted_position_weight` 当前仍不能写成：
  - `final_output_ready`
- `adjusted_position_weight` 当前可以写成：
  - `traceability_chain_defined__final_output_not_closed`
- 当前最小回溯链已经明确：
  - `adjusted_position_weight = target_weight * final_size_scalar`
- 但只要以下任一项未闭合：
  - `target_weight`
  - `final_size_scalar`
  - `target_weight` 上游降级口径
  当前都不能写成最终输出已通过

## 一、当前字段状态

- 字段名：
  - `adjusted_position_weight`
- 所属层：
  - `portfolio_final_outputs`
- 当前来源状态：
  - `blocked_by_target_weight`
- 当前角色：
  - `叠加风险缩放后的最终权重`
- 当前阻塞位置：
  - `G5 / final_output`

## 二、为什么现在进入判断页

- 原因 1：
  - `target_weight` 已进入最小生成链判断
- 原因 2：
  - `final_size_scalar` 的回溯断言已经冻结：
    - `min(kelly_size_scalar, vt_size_scalar, pq_position_max_size, 1.0)`
- 原因 3：
  - `adjusted_position_weight` 是组合层最后一个明确挂在阻塞表上的最终融合输出

## 三、当前最小回溯链

- 当前允许写成的最小回溯链是：
  - `target_weight`
  - `final_size_scalar`
  ->
  - `adjusted_position_weight`

### 解释

- 这条链当前只说明：
  - 最终权重必须能从目标权重与风险缩放标量反推
- 这不意味着：
  - 目标权重已闭合
  - 风险缩放已全链实跑
  - 当前已有正式最终权重输出

## 四、当前最小断言

- 断言 1：
  - `adjusted_position_weight` 必须满足：
    - `target_weight * final_size_scalar`
- 断言 2：
  - 若 `target_weight` 仍是：
    - `generation_chain_defined__output_not_closed`
  - 则 `adjusted_position_weight` 只能保留为：
    - `final_output_not_closed`
- 断言 3：
  - 若 `final_size_scalar <= 0.05`
    - 必须 `ABORT`
- 断言 4：
  - 若 `target_weight` 走的是降级生成模式
    - 不得伪装成完整优化器最终输出

## 五、当前允许写法

- 允许写成：
  - `adjusted_position_weight 当前最小回溯链已定义`
  - `adjusted_position_weight 当前仍未闭合正式最终输出`
  - `adjusted_position_weight 当前属于 traceability_chain_defined__final_output_not_closed`

## 六、禁止误写

- 禁止写成：
  - `adjusted_position_weight 已可正式运行`
  - `adjusted_position_weight 已完成最终验收`
  - `组合层最终权重已闭合`
- 禁止把：
  - 回溯链定义
  写成：
  - 实际已跑通的最终输出

## 七、与上游的关系

- 当前这页能解决的是：
  - `adjusted_position_weight` 不再只是纯文字阻塞项
  - 组合层最终融合输出已有明确回溯口径
- 当前这页还没有解决：
  - `target_weight` 正式数值输出
  - `portfolio_tracking_error` 正式风险输出
  - 组合层完整实现

## 八、主负责人裁决

- 当前裁决不是：
  - 把 `adjusted_position_weight` 升格为已闭合最终输出
- 当前裁决是：
  - 允许它进入：
    - `回溯闭合判断层`
  - 当前正确状态应写成：
    - `traceability_chain_defined__final_output_not_closed`
- 这一步的价值在于：
  - `G5` 主链已经能从输入一路讲到最终融合输出
  - 但仍守住“不直接开实现”的边界

## 九、一句话口径

- 当前 `adjusted_position_weight` 的正确写法是：
  - `traceability_chain_defined__final_output_not_closed`

## 回链

- `A_REQ_003_最小验收口径__20260715.md`
- `A5_target_weight_最小生成链判断页__20260716.md`
- `A5_最小对象卡草案__20260715.md`
- `A5_统一验收断言表__20260715.tsv`
- `A5_实现阻塞项拆解表__20260716.tsv`
