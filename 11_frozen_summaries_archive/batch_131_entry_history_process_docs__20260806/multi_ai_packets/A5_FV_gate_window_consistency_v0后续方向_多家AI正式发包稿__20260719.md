# A5 FV gate window consistency v0 后续方向 多家AI正式发包稿

【TEXT PAYLOAD START】
你现在参与的是一个多AI讨论，不是自由闲聊。

你现在只能回答一个新题，不许回到旧题。

【旧题（已裁定，禁止再答）】
1. 是否继续同窗微调 `final_size_scalar` / `rank-decay`：已裁定 `no`
2. 是否进入第二个 `new evidence type`：已裁定 `yes`，且 `holding_rule_v0` 已完成
3. `window_consistency_v0` 是否需要正式落盘：已完成，当前标签为 `cross_window_sign_divergence__still_need_evidence`

【新题（你必须回答的唯一问题）】
在 `window_consistency_v0` 已确认
`cross_window_sign_divergence__still_need_evidence`
后，
当前下一手最合理的是：
- 补第三日历窗
- 先停在当前 `still_need_evidence`
- 还是存在更窄但不越界的替代动作

你必须至少给出三种方案：
- 保守
- 平衡
- 激进

【已知背景】
- 当前 `FV gate v0` 已完成：
  - `current_best`
  - `tuning_frozen`
- 当前 `FV_gate_v1_sample_boundary` 已完成：
  - `sample_boundary_reproduced__still_need_evidence`
- 当前 `cost_sensitivity_v0` 已完成：
  - `cost_band_stable__still_need_evidence`
- 当前 `holding_rule_v0` 已完成：
  - `holding_rule_stable__still_need_evidence`
- 当前 `window_consistency_v0` 已完成：
  - `cross_window_sign_divergence__still_need_evidence`
- 当前跨窗对照的核心事实是：
  - `v0 current_best window`
    - `net total_return = -0.00947495`
    - `holdout net total_return = -0.00291711`
    - `net active_total_return = -0.12843922`
    - `net max_drawdown = -0.01794461`
  - `v1 adjacent window`
    - `net total_return = 0.00197364`
    - `holdout net total_return = 0.00485478`
    - `net active_total_return = 0.03054991`
    - `net max_drawdown = -0.00983588`

【硬约束】
- 当前不能写成：
  - `financial-valid`
  - `output_passed`
  - `cross_window_consistency_passed`
- 当前不能回到：
  - 同窗微调 `final_size_scalar`
  - 同窗微调 `rank-decay`
  - `breakout`
  - 严过滤
- 当前不能默认直接展开：
  - 第三类 `new evidence type`
  - 冲击模型
  - 稳健性全家桶
  - 完整回测平台

【本轮允许讨论】
- 第三日历窗是否是当前最值钱的补证动作
- 是否应先停在当前 `still_need_evidence`
- 是否存在比“第三日历窗”更窄但仍有信息价值的动作
- 每种方案对应的停止规则

【本轮禁止展开】
- 不要讨论新信号
- 不要讨论新排序
- 不要讨论新持有规则网格
- 不要讨论更宽成本带
- 不要讨论 UI / 产品壳 / 发布门禁
- 不要把“你更喜欢什么”写成“已证明什么”

【OUTPUT CONTRACT】
1. 结论摘要
2. 三种方案对比（保守 / 平衡 / 激进）
3. 最推荐方案
4. 当前最小下一步
5. 停止规则

【额外要求】
- 每种方案都必须说明：
  - 适用条件
  - 优点
  - 风险
  - `NEED_EVIDENCE`
- 如果你主张补第三日历窗，请说明：
  - 为什么它比第三类 `new evidence type` 更优先
- 如果你主张先停在当前，请说明：
  - 为什么继续补不会显著增加信息价值
- 如果你主张更窄替代动作，请说明：
  - 为什么它不属于变相扩线
【TEXT PAYLOAD END】
