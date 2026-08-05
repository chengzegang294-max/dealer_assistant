# A5 FV gate window consistency v0 后续方向 多AI前情提要与裁决框架

更新时间：2026-07-19

## TASK

- 讨论：在 `window_consistency_v0`
  已正式落成
  `cross_window_sign_divergence__still_need_evidence`
  后，
  当前下一手最合理的是：
  - 补第三日历窗
  - 先停在当前 `still_need_evidence`
  - 还是存在更窄但不越界的替代动作

## BACKGROUND

- 当前 `FV gate v0`
  已完成：
  - `current_best`
  - `tuning_frozen`
- 当前 `FV_gate_v1_sample_boundary`
  已完成：
  - 相邻窗复验
  - 标签：
    - `sample_boundary_reproduced__still_need_evidence`
- 当前 `cost_sensitivity_v0`
  已完成：
  - `5 / 15 / 25 bps`
    小成本带
  - 标签：
    - `cost_band_stable__still_need_evidence`
- 当前 `holding_rule_v0`
  已完成：
  - `20 trade days`
    单一预声明再平衡对照
  - 标签：
    - `holding_rule_stable__still_need_evidence`
- 当前 `window_consistency_v0`
  又已完成：
  - `v0 current_best window`
    对照
    `v1 adjacent window`
  - 标签：
    - `cross_window_sign_divergence__still_need_evidence`
- 当前核心事实是：
  - 同一冻结合同在：
    - `20260401 -> 20260630`
    - `20251215 -> 20260331`
    上出现收益主字段符号分歧

## KNOWN_CONSTRAINTS

- 当前不允许写成：
  - `financial-valid`
  - `output_passed`
  - `cross_window_consistency_passed`
- 当前不允许回到：
  - 同窗微调 `final_size_scalar`
  - 同窗微调 `rank-decay`
  - `breakout`
  - 严过滤
- 当前不允许默认直接展开：
  - 第三类 `new evidence type`
  - 冲击模型
  - 稳健性全家桶
  - 完整回测平台
- 当前必须承认：
  - `sample_boundary_reproduced`
    仍成立
  - 但 `cross_window_sign_divergence`
    也已成立

## DISCUSSION_SCOPE

- 本轮允许讨论：
  - 下一手是否先补第三日历窗
  - 是否应停在当前
    `still_need_evidence`
  - 是否存在比“第三日历窗”更窄、
    但比“原地停住”更有信息价值的动作
  - 若继续推进，
    停点与停止规则怎么写
- 本轮不要展开：
  - 新信号
  - 新排序
  - 新持有规则网格
  - 更宽成本带
  - 冲击模型细节
  - UI / 产品壳 / 发布门禁

## FREE_GUESS_RANGE

- 允许你合理判断：
  - `cross_window_sign_divergence`
    更像是：
    - 样本偶发
    - 日历窗 regime 差异
    - 当前合同尚不足以宣称稳定
  - 当前最值钱的下一手应偏向：
    - 补证据
    - 停止扩线
    - 还是更窄的复核动作
- 若缺证据必须写：
  - `NEED_EVIDENCE`

## EXPECTED_OUTPUT

- 请至少给出：
  - `保守 / 平衡 / 激进`
    三种方案
- 每种方案至少说明：
  - 核心思路
  - 适用条件
  - 优点
  - 风险
  - `NEED_EVIDENCE`
  - 当前最小下一步
  - 停止规则
- 最后请给出：
  - 你最推荐的方案
  - 为什么不推荐另外两个
