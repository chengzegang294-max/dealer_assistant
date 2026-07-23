# A5 target_weight 升格裁决 actual_generation后 第二轮回收记录与主负责人裁决

更新时间：2026-07-16

## 用途

- 吸收 `actual_generation后` 升级判断第二轮更窄追问回包。
- 这页不讨论：
  - 是否足以重开升格裁决
- 这页只讨论：
  - 是否已足以进入更进一步升级判断
  - 若不足，唯一附加条件是什么

## 一、回收总表

| 模型 | 有效性 | 结论 | 一句话原因 | 唯一附加条件/缺口 | 禁止误写提醒 | 备注 |
|---|---|---|---|---|---|---|
| `DeepSeek` | `有效` | `conditional` | 风险模型未闭合致稳健边界未知 | 补降级风险处理稳健边界验证 | 协方差模型未闭合，输出基础不稳固 | 对题且边界清楚 |
| `GPT` | `有效` | `conditional` | 未闭合协方差仍可能是硬门槛 | 确认 `covariance_model_id` 未闭合不阻断升级判断 | 仍处 degraded 风险且协方差未闭合 | 对题且直接命中门槛 |
| `GLM` | `有效` | `yes` | actual generation execution 已完成，满足进入升级判断门槛 | 无 | 当前仍处降级风险处理且协方差未闭合，不能写通过 | 有效，但相对更激进 |
| `Kimi` | `有效` | `conditional` | `covariance_model_id` 仍未闭合，升级判断需附加条件 | `covariance_model_id` 正式可实现口径闭合或降级模式充分性显式确认 | `covariance_model_id` 未闭合且仍为降级风险处理 | 对题，但条件表述较宽 |
| `Qwen` | `无效` | `无回包` | 当前贴回中未见本轮独立回答 | 不适用 | 不适用 | 不计入票面 |

## 二、主负责人裁决

- 当前有效票面是：
  - `3` 票 `conditional`
  - `1` 票 `yes`
  - `1` 票无效
- 当前正式裁决为：
  - `conditional`
- 当前不直接采纳 `GLM yes` 的原因：
  - 它代表的是更激进写法
  - 但多数有效票都把问题收缩到同一个最小边界：
    - `covariance_model_id` 未闭合时，`degraded_risk_handling` 的充分性/稳健边界尚未正式冻结

## 三、唯一附加条件的归一化

- 不同模型虽然写法不同，但当前最小可归一化附加条件只有一条：
  - 正式冻结并验证：
    - 在 `covariance_model_id` 未闭合前提下，
    - `degraded_risk_handling` 的充分性与稳健边界，
    - 且明确该未闭合状态为什么不阻断当前升级判断

## 四、当前先做什么

- 当前先做：
  - 把上面这条唯一附加条件正式落成边界页
  - 不再继续追问同层问题
- 当前暂缓：
  - 直接写成 `yes`
  - 直接推进到 `output_passed`

## 五、一句话口径

- 当前 `actual_generation后` 升级判断的第二轮正式结论是：
  - `conditional`
  - 还差一条附加条件：
    - `degraded_risk_handling` 在 `covariance_model_id` 未闭合时的充分性/稳健边界正式冻结并验证

## 回链

- `A5_target_weight_升格裁决__actual_generation后_第二轮更窄追问稿__20260716.md`
- `A5_target_weight_升格裁决__actual_generation后_多家AI回收记录与主负责人裁决__20260716.md`
