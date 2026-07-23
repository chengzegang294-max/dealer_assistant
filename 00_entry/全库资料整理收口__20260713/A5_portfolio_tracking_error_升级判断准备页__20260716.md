# A5 portfolio_tracking_error 升级判断准备页

更新时间：2026-07-16

## 用途

- 把 `portfolio_tracking_error` 从“三项最小缺口均到可判断层”继续推进到“可直接起单点升级判断包”。
- 这页不宣布：
  - `output_passed`
  - `benchmark 风险输出 ready`
  - `covariance_model_id ready`
- 这页只回答：
  - 为什么现在值得起判断
  - 当前唯一该裁的焦点是什么
  - 哪些内容仍禁止误写

## 当前结论

- 当前已经完成：
  - `benchmark` 风险输出最小正式口径页
  - `covariance_model_id` 最小输入层页
  - `降级风险口径可审计样例页`
- 当前正式推进结果是：
  - `portfolio_tracking_error 三项最小缺口均到可判断层`
- 因此当前最顺下一手不再是：
  - 继续补同层条件说明
  - 继续追加样例定义
- 而是：
  - 起 `portfolio_tracking_error` 单点升级判断

## 一、为什么现在值得起判断

- 因为当前已经同时具备：
  - benchmark 风险输出最小正式口径
  - `covariance_model_id` 最小输入层
  - success / failure 降级风险可审计样例
- 这意味着当前已经不再缺：
  - 口径命名
  - 输入层命名
  - 样例层命名

## 二、当前唯一该裁的焦点

- 当前起升级判断时唯一该裁的焦点是：
  - 在 `target_weight = verified_with_degraded_risk__upstream_min_integration_verified__not_output_passed`
  - 且 `covariance_model_id` 仍未闭合
  - 且 `risk_mode = degraded_risk_handling`
  的边界下，
  - `portfolio_tracking_error` 是否已足以从 `pass_conditions_drafted__not_output_passed`
    继续推进到下一档正式升级判断结论

## 三、当前不要再讨论什么

- 当前不要再回到：
  - `benchmark 风险输出最小正式口径` 是否还要改名
- 当前不要再回到：
  - `covariance_model_id` 是否已 ready
- 当前不要展开：
  - 回测
  - 下游 `adjusted_position_weight`
  - 最终组合实现

## 四、当前禁止误写

- 禁止写成：
  - `output_passed`
  - `benchmark 风险输出 ready`
  - `covariance_model_id ready`
- 禁止把：
  - `三项最小缺口均到可判断层`
  - 写成：
    - `正式 tracking error 已通过`

## 五、一句话口径

- 当前 `portfolio_tracking_error` 的最稳正式写法是：
  - `三项最小缺口均到可判断层`
  - `下一手已切到单点升级判断`

## 回链

- `A5_portfolio_tracking_error_benchmark风险输出最小正式口径页__20260716.md`
- `A5_portfolio_tracking_error_covariance最小输入层页__20260716.md`
- `A5_portfolio_tracking_error_降级风险口径可审计样例页__20260716.md`
- `A5_G5_输出升格证据总表__20260716.tsv`
