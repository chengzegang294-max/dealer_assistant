# A5 adjusted_position_weight final_size_scalar 降级样例页

更新时间：2026-07-16

## 用途

- 把 `adjusted_position_weight` 当前第一缺口压成正式一页。
- 这页不宣布：
  - `adjusted_position_weight output_passed`
  - `final_size_scalar runtime_ready`
- 这页只负责：
  - 冻结 `final_size_scalar` 在降级模式下的最小可审计样例口径
  - 写清哪些字段必须保留
  - 给后续最终融合 failure 样例页提供统一入口

## 当前结论

- 当前 `adjusted_position_weight` 仍不能写成：
  - `output_passed`
- 当前可以正式写成：
  - `final_size_scalar` 降级样例已冻结
- 当前最小样例口径的含义不是：
  - 风险缩放链已完整实跑
- 当前最小样例口径的含义是：
  - 已可明确 `adjusted_position_weight` 在降级模式下，最小需要怎样记录 `final_size_scalar`

## 一、success 样例最小结构

- success 样例至少必须带：
  - `target_weight_status`
  - `final_size_scalar`
  - `final_size_scalar_method`
  - `degrade_flags`
  - `adjusted_position_weight_formula = target_weight * final_size_scalar`
  - `audit_note`
- success 样例当前必须守住：
  - `final_size_scalar = min(kelly_size_scalar, vt_size_scalar, pq_position_max_size, 1.0)`
  - 若来自降级模式，必须显式展开 `degrade_flags`

## 二、failure 样例最小结构

- failure 样例至少必须带：
  - `final_size_scalar = null`
  - `abort_reason`
  - `degrade_flags`
  - `audit_note`
- failure 样例推荐触发器至少覆盖：
  - `final_size_scalar <= 0.05`
  - 缺少 `target_weight`
  - 缺少任一核心缩放输入

## 三、当前允许写法

- 允许写成：
  - `final_size_scalar` 已具备降级模式下的最小可审计样例
  - 当前缩放链仍属于规则冻结与样例冻结层
- 禁止写成：
  - `final_size_scalar 已完成运行闭合`
  - `最终权重缩放链已 ready`

## 四、主负责人裁决

- 当前不做：
  - `adjusted_position_weight` 升级判断
  - runtime 缩放实现
- 当前正式裁决是：
  - 允许把 `final_size_scalar` 降级样例视为已冻结
  - 下一手切到：
    - `最终融合 failure / abort_reason 样例`

## 五、一句话口径

- 当前 `adjusted_position_weight` 已先补齐：
  - `final_size_scalar` 降级样例
- 但当前仍未到：
  - `output_passed`

## 回链

- `A5_adjusted_position_weight_升级判断准备页__20260716.md`
- `A5_adjusted_position_weight_最小通过条件页__20260716.md`
- `A5_实现阻塞项拆解表__20260716.tsv`
