# Target Weight Real Input Smoke-Run Card v1

## 用途

- 把 `target_weight` 从模板级 smoke-run 推进到“上游真实输入驱动”的 smoke-run。
- 这张卡不宣布：
  - `output_passed`
- 这张卡只负责：
  - 固定真实输入长什么样
  - 固定要检查什么
  - 固定本轮不能误写成什么

## 当前输入入口

- 真实输入模板：
  - `data/target_weight_real_input_template_v1.json`
- 当前上游假设：
  - `alpha_input_mode = ranked_scores`
  - `alpha_source_type = contract_frozen_proxy`
  - `constraint_set_id = TW_MIN_CONSTRAINT_SET_V1`
  - `risk_handling_mode = degraded_risk_handling`

## 当前 smoke-run 目标

- 目标 1：
  - 不是手写权重结果
  - 而是让“上游真实输入模板”成为后续生成链的正式入口
- 目标 2：
  - 固定 success case 最少需要哪些字段
- 目标 3：
  - 让 failure case 可以对应到真实输入缺口

## success case 最小要求

- 至少要有：
  - `universe_id`
  - `alpha_vector`
  - `constraint_set`
  - `risk_handling_mode`
- 至少要验证：
  - `alpha_vector` 非空
  - `rank` 可追溯
  - 约束字段完整
  - 输出后权重边界可检查

## failure case 最小触发器

- 当前优先触发器：
  - `missing_constraint_set`
  - `empty_alpha_vector`
  - `untraceable_alpha_source`

## 本轮通过后该怎么写

- 允许写成：
  - `真实输入模板已冻结`
  - `真实生成链 smoke-run 输入卡已冻结`
- 不允许写成：
  - `target_weight 已 output_passed`
  - `优化器真实生成链已 fully validated`

## 下一手

- 用这张卡做下一轮：
  - 上游真实输入驱动 success case
  - 上游真实输入驱动 failure case

## 回链

- `runtime_execution_card_v1.md`
- `data/target_weight_real_input_template_v1.json`
- `../../00_entry/全库资料整理收口__20260713/A5_target_weight_最小缺口补齐页__20260716.md`
