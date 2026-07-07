# TK-R7 AO 背离风险调整标签 后续对象定义入口 v1

## 作用

- 把 `TK-R7 = AO divergence 风险调整标签` 从综合整理稿里的“可重开结论”推进成更明确的后续对象入口。
- 当前目标不是把 `AO` 变成独立硬信号，而是先固定：
  - 它在 `TK` 主线里扮演什么角色
  - 最小输入
  - 最小输出
  - 与现有 `IB/DB/CB + Fib` 主线的关系
  - 当前边界

## 当前定位

- 层级：
  - `TK` 后续对象层
- 当前角色：
  - `risk_adjust_label_entry`
- 不是：
  - 当前独立策略
  - 当前 entry gate
  - 当前已量化完成对象

## 来源锚点

- 主要来源：
  - `20231219TK外汇交易系统学习资料整理(6)_导出.md`
  - `20231219TK外汇交易系统学习资料整理(6)_吸收结论_v1.md`
- 当前已固定可引用语义：
  - `AO` 更偏动量/背离参考
  - 更适合作为风险调整与转向概率补充
  - 不适合作为单独硬信号

## 为什么要单独开 TK-R7

- 新综合整理稿没有把 `AO` 写成新的主信号源。
- 它补的是：
  - 当主信号已出现时，如何用背离来调整风险感知
  - 如何把“继续延伸”与“衰竭/转向概率上升”区分开
- 因而 `TK-R7` 的价值不在于替代现有信号，而在于：
  - 作为风险修正标签
  - 作为解释层
  - 作为后续 trade commentary / diag-only 的补充对象

## 最小语义

- 当前保守写法：
  - 当主信号或结构已成立后，若 `AO` 背离出现，则把它记为“风险调整 / 转向概率补充”标签。
- 当前不写成：
  - `AO divergence = 必做反手`
  - `AO divergence = 独立入场信号`
  - `AO` 单独决定 `TP3` 或主结构是否成立

## 最小输入

- 主信号上下文：
  - `IB / DB / CB / ABC / B zone` 中至少一个上下文已成立
- `AO` 基础值：
  - 至少能判断当前是否出现多/空背离
- 价格上下文：
  - 当前价格是延续中、回撤中，还是接近目标区
- 可选辅助：
  - `TP1 / TP2 / TP3`
  - `IB retest / rejection`

## 最小输出

- `ao_divergence_present`
  - 当前是否有背离
- `ao_divergence_side`
  - `bullish / bearish / none`
- `ao_risk_adjust_note`
  - 当前属于：
    - `no_divergence`
    - `divergence_watch`
    - `divergence_against_main_signal`

## 当前建议的派生输出

- `ao_divergence_strength_bucket`
  - 背离强度分桶
- `ao_vs_tp_context`
  - 背离发生在靠近 `TP1/TP2/TP3` 的哪个阶段
- `ao_trend_exhaustion_bias`
  - 是否倾向提示延伸衰竭

## 与现有 TK 主线的关系

- 当前更稳的关系是：
  - `TK-R7` 不替代 `IB / DB / CB`
  - `TK-R7` 不替代 `Fib TP3`
  - `TK-R7` 也不替代 `TK-R6 / TK-R8`
  - 它更像主结构之后的风险调整标签
- 当前更适合放在：
  - 风险修正层
  - 解释层
  - 诊断标签层
- 当前不适合直接放在：
  - 独立 entry gate
  - 硬门控

## 最小验收定义

- 有一份对象语义文档：
  - 说明它是 risk-adjust label，而不是独立信号
- 有一份最小输入/输出合同：
  - 至少把 `divergence present / side / adjust note` 说清
- 有一份 proof-of-mapping 的证据表（可审计）：
  - `12_工具运行时_TOOLING_RUNTIME\TK_R7\tkr7_manual_audit_sheet_v1.tsv`
- 有一份可复现的汇总产物（可审计）：
  - `12_工具运行时_TOOLING_RUNTIME\TK_R7\tkr7_manual_audit_summary_v1.md`
- 有一份当前角色裁决：
  - `DIAG_ONLY_OBJECT_CANDIDATE`
  - 或 `risk_adjust_label_entry`

## 当前 gaps

- `AO 背离` 的精确判据仍未冻结。
- 当前还没有统一样本去判断：
  - 背离出现后
  - 对主信号胜率、`TP3` 到达率或回撤风险
  - 是否真的有稳定影响。
- 当前不应把教学语义直接写成统计显著性结论。

## 当前裁决

- `TK-R7` 是新综合整理稿里第三优先的新增对象。
- 当前应把它固定为：
  - `TK` 后续对象层中的风险调整标签入口
  - 主结构成立后的解释/修正对象
- 同时继续保持边界：
  - 不直接升级成硬门控
  - 不直接升级成独立策略
  - 不宣称已完成量化验证

## 下一步

- 若继续推进同一条线，优先顺序应为：
  - 先补 `AO divergence` 的最小判据草案
  - 再补与 `TP1/TP2/TP3` 的位置关系标签
  - 再决定是否值得开 `TK-R7` 的 proof-of-mapping 或诊断壳
