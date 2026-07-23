# A5 adjusted_position_weight 输出闭合判断页

更新时间：2026-07-16

## 用途

- 把 `adjusted_position_weight` 从“回溯闭合判断层”继续推进到“输出闭合判断层”。
- 这页不是最终组合实现页。
- 这页也不是在宣布最终权重已 ready。
- 这页只负责：
  - 判断当前为什么还不能宣布最终融合输出闭合
  - 固定当前最小闭合条件
  - 作为 `G5` 输出段最后一段的正式判断页

## 当前结论

- `adjusted_position_weight` 当前仍不能写成：
  - `output_closed`
- `adjusted_position_weight` 当前可以写成：
  - `output_closure_under_judgement__not_closed`
- 当前最小回溯链已经具备：
  - `target_weight`
  - `final_size_scalar`
  ->
  - `adjusted_position_weight`
- 但当前仍缺：
  - `target_weight` 的正式输出闭合
  - `final_size_scalar` 与上游降级模式之间的输出边界冻结
  - 最终输出通过条件

## 一、当前字段状态

- 字段名：
  - `adjusted_position_weight`
- 所属层：
  - `portfolio_final_outputs`
- 当前来源状态：
  - `traceability_chain_defined__final_output_not_closed`
- 当前角色：
  - `叠加风险缩放后的最终权重`
- 当前阶段定位：
  - `输出闭合判断层`

## 二、为什么现在进入输出闭合判断

- 原因 1：
  - `target_weight` 已进入：
    - `output_closure_under_judgement__not_closed`
- 原因 2：
  - `adjusted_position_weight` 已不再只是“回溯链已定义”
- 原因 3：
  - 它是组合层最终融合输出，不能长期停在只有回溯关系而没有输出闭合判断的状态

## 三、当前最小闭合条件

- 条件 1：
  - `target_weight` 至少要维持：
    - `output_closure_under_judgement__not_closed`
  - 且不得退回未定义上游输出
- 条件 2：
  - `final_size_scalar` 的核心断言必须保持：
    - `min(kelly_size_scalar, vt_size_scalar, pq_position_max_size, 1.0)`
- 条件 3：
  - 若 `final_size_scalar <= 0.05`
    - 必须 `ABORT`
- 条件 4：
  - 若 `target_weight` 走降级模式
    - 不得把最终结果误写成完整优化器最终输出

## 四、为什么当前仍不能判闭合

- 原因 1：
  - `target_weight` 自身还没通过输出闭合
- 原因 2：
  - 当前只定义了回溯链，没有定义“何时算最终输出通过”
- 原因 3：
  - 降级模式下的最终结果仍不能冒充完整优化器输出
- 因此当前不能写成：
  - `adjusted_position_weight 已可正式运行`
  - `组合层最终权重已闭合`

## 五、当前允许写法

- 允许写成：
  - `adjusted_position_weight 当前已进入输出闭合判断层`
  - `adjusted_position_weight 当前仍未通过输出闭合`
  - `adjusted_position_weight 当前属于 output_closure_under_judgement__not_closed`

## 六、禁止误写

- 禁止写成：
  - `adjusted_position_weight 已 ready`
  - `adjusted_position_weight 已完成最终验收`
  - `组合层最终权重已可直接运行`
  - `G5 已通过`
- 禁止把：
  - 当前输出闭合判断
  写成：
  - 当前已经形成正式最终输出结果

## 七、与上游和整体状态的关系

- 当前这页能解决的是：
  - `adjusted_position_weight` 已不再只是“回溯链已定义”
  - 而是进入了“为什么还不能闭合输出”的判断层
- 当前这页还没有解决：
  - `target_weight` 的正式输出闭合
  - 完整组合层实现

## 八、主负责人裁决

- 当前裁决不是：
  - 把 `adjusted_position_weight` 直接升格为 ready
- 当前裁决是：
  - 允许它进入：
    - `输出闭合判断层`
  - 当前正确状态应写成：
    - `output_closure_under_judgement__not_closed`
- 这一步的价值在于：
  - `G5` 三个输出段现在都已经进入同一层级的闭合判断
  - 主线可以正式写成“输出闭合判断已全段覆盖”

## 九、一句话口径

- 当前 `adjusted_position_weight` 的正确写法是：
  - `output_closure_under_judgement__not_closed`

## 回链

- `A5_adjusted_position_weight_回溯闭合判断页__20260716.md`
- `A5_target_weight_输出闭合判断页__20260716.md`
- `A5_G5_输出闭合判断页__20260716.md`
- `A5_target_weight_最小生成链判断页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
