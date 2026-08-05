# A5 Cursor 主导 FV gate post third window 下一手讨论包

更新时间：2026-07-19

## 一、当前唯一问题

- 在：
  - `FV_gate_v2_third_window`
    已完成之后
- 当前真正需要 `Cursor`
  统筹的唯一问题是：
  - 下一手是否应围绕：
    - `active underperformance`
      开一个更窄解释层
  - 还是：
    - 切回新的
      `new evidence type`
  - 或：
    - 正式停在当前
      `still_need_evidence`

## 二、当前已完成事实

- `v0 current_best`
  为负
- `v1 adjacent window`
  为正
- `holding_rule_v0`
  已完成
- `cost_sensitivity_v0`
  已完成
- `window_consistency_v0`
  已完成
- `v2 third window`
  已完成

## 三、当前第三窗新事实

- 第三窗正式采用：
  - `20250909 -> 20251212`
- 三窗最新标签为：
  - `cross_window_return_sign_majority_positive__active_sign_majority_negative__still_need_evidence`
- 当前含义是：
  - 绝对收益与 holdout
    出现：
    - `2 正 1 负`
  - 但 active return
    出现：
    - `1 正 2 负`

## 四、当前不允许讨论成什么

- 不允许写成：
  - `financial-valid`
  - `output_passed`
  - `cross_window_consistency_passed`
- 不允许回到：
  - 同窗微调
  - 新持有规则网格
  - 更宽成本带
  - 第四窗默认续抓

## 五、希望 Cursor 回答的问题

1. 当前 `active underperformance`
   是否值得单开一个极窄解释层？
2. 若值得，
   它的最小边界应是什么？
3. 若不值得，
   当前下一手是：
   - 交回新的
     `new evidence type`
   - 还是停在当前
     `still_need_evidence`
4. 当前哪些动作必须列为禁止项？

## 六、Trae 当前已完成部分

- 第三窗候选 A
  失败原因已审计：
  - `688981.SH`
    缺行
- 第三窗候选 B
  已成功跑通：
  - raw daily
  - benchmark
  - returns
  - covariance fresh
  - FV gate scorecard
  - 三窗 summary
- 当前仓内已经不缺：
  - 执行侧证据
- 当前缺的是：
  - 对这个新停点的统筹判断

## 七、一句话口径

- 当前该讨论的不是“还要不要第三窗”，而是“第三窗后 active underperformance 到底值不值得开一个极窄解释层，还是应切回新的 evidence type / 停住”。

## 八、2026-07-19 Cursor 裁决已吸收

- 本轮 `Cursor` 已明确选择：
  - `A`
    即：
    - 先开
      `active underperformance`
      极窄解释层
- 本轮已明确不选：
  - `B`
    - 直接切回新的
      `new evidence type`
  - `C`
    - 现在就停在当前
      `still_need_evidence`
- 当前 `Trae` 已按该裁决正式落地：
  - `A5_FV_gate_active_underperformance_v0解释层页__20260719.md`
  - `fv_gate_active_underperformance_v0_summary_latest.json`
