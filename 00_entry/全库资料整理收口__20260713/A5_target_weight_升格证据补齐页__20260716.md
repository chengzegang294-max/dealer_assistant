# A5 target_weight 升格证据补齐页

更新时间：2026-07-16

## 用途

- 作为 `target_weight` 冲击 `output_passed` 的第一手执行物。
- 这页不宣布已经通过。
- 这页只负责把三类最值钱的升格证据先补齐到可审计层：
  - `constraint_set` 最小正式形式
  - 可审计权重样例
  - 失败样例与 `abort_reason`

## 当前结论

- 当前 `target_weight` 仍只能写成：
  - `pass_conditions_frozen__not_output_passed`
- 但当前已经不是：
  - 纯口头要求补证据
- 当前已经推进到：
  - `第一手升格证据补齐已启动`

## 一、constraint_set 最小正式形式

- 当前最小正式形式固定包含：
  - `weight_lower_bound`
  - `weight_upper_bound`
  - `long_only_flag`
  - `turnover_limit`
- 当前允许作为最小通过证据的约束集合样式：

```json
{
  "constraint_set_id": "TW_MIN_CONSTRAINT_SET_V1",
  "weight_lower_bound": 0.0,
  "weight_upper_bound": 0.10,
  "long_only_flag": true,
  "turnover_limit": 0.25,
  "notes": [
    "single_name_cap_applied",
    "long_only_enforced",
    "turnover_control_enabled"
  ]
}
```

- 当前这份正式形式回答的是：
  - `最小约束集合长什么样`
- 当前还没有回答：
  - `全部优化器细节已闭合`

## 二、可审计权重样例

- 当前允许作为最小可审计权重样例的结构：

```json
{
  "sample_id": "TW_AUDIT_SAMPLE_V1",
  "risk_handling_mode": "degraded_risk_handling",
  "input_assumption": {
    "alpha_input_mode": "ranked_scores",
    "constraint_set_id": "TW_MIN_CONSTRAINT_SET_V1"
  },
  "weights": [
    { "ticker": "000001.SZ", "target_weight": 0.08 },
    { "ticker": "600519.SH", "target_weight": 0.10 },
    { "ticker": "300750.SZ", "target_weight": 0.06 }
  ],
  "checks": {
    "non_empty": true,
    "within_bounds": true,
    "weight_sum_traceable": true
  },
  "degrade_flags": [
    "risk_model_not_formalized__use_degraded_risk_handling"
  ],
  "abort_reason": ""
}
```

- 这份样例当前只证明：
  - 权重结构可读
  - 单项边界可验
  - 降级口径可显式带出
- 这份样例当前不证明：
  - 正式优化器输出已通过

## 三、失败样例与 abort_reason

- 当前允许作为最小失败样例的结构：

```json
{
  "sample_id": "TW_FAIL_SAMPLE_V1",
  "input_assumption": {
    "alpha_input_mode": "untraceable_proxy",
    "constraint_set_id": ""
  },
  "weights": [],
  "checks": {
    "non_empty": false,
    "within_bounds": false,
    "weight_sum_traceable": false
  },
  "degrade_flags": [],
  "abort_reason": "missing_constraint_set_or_untraceable_alpha_input"
}
```

- 当前这份失败样例回答的是：
  - 什么情况下必须中止
  - `abort_reason` 如何显式写出
- 当前这份失败样例不等于：
  - 所有失败场景都已枚举完毕

## 四、当前已补齐了什么

- 已补齐：
  - `constraint_set` 的最小正式形式
  - 可审计权重样例
  - 失败样例与 `abort_reason`
- 当前仍未补齐：
  - 更强的正式风险模型口径
  - 更完整的多样本族
  - 正式优化器实现

## 五、当前状态更新

- 当前 `target_weight` 不应升格为：
  - `output_passed`
- 但当前应明确升级口径为：
  - `第一手升格证据已补齐`
- 当前下一步不再是：
  - 继续抽象讨论证据要什么
- 当前下一步应是：
  - 判断这批证据是否足以支持一次新的升格裁决

## 六、禁止误写

- 禁止写成：
  - `target_weight 已正式通过`
  - `正式优化器输出已闭合`
  - `covariance_model_id 已 ready`
- 禁止把：
  - `降级风险口径下的样例`
  写成：
  - `正式协方差路线已完成`

## 七、一句话口径

- 当前 `target_weight` 已经从：
  - `通过条件已冻结`
- 继续推进到：
  - `第一手升格证据已补齐`
- 但当前仍只能写成：
  - `pass_conditions_frozen__not_output_passed`

## 回链

- `A5_target_weight_通过后仍需证据清单页__20260716.md`
- `A5_G5_输出升格顺序裁决页__20260716.md`
- `A5_G5_输出升格证据总表__20260716.tsv`
- `A5_实现阻塞项拆解表__20260716.tsv`
