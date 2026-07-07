# GROUP 03: 组合管理 + 风险模型 + 交易成本 — Part 02
## 3) 约束与现实摩擦

> 换手、交易成本、冲击成本、容量、约束可行性

### 3.1 换手率（Turnover）

#### 3.1.1 换手率定义

```
Turnover = (1/2) × Σ_i |w_i^{new} - w_i^{old}|

纯多头组合简化为：
Turnover = Σ_{w_i^{new}>w_i^{old}} (w_i^{new} - w_i^{old}) = Σ_{w_i^{new}<w_i^{old}} (w_i^{old} - w_i^{new})
```

- **年化换算**: 月换手率 × 12（若每月再平衡），需注意重叠计算问题
- **主动换手率**: 仅计算偏离基准的权重变化
- **来源**: QHS Ch.8 (p.233-236)

#### 3.1.2 被动漂移（Passive Drift）

```
即使不做任何交易，组合权重也会因个股涨跌而自然漂移：

w_i^{drifted} = w_i^{old} × (1 + r_i) / (1 + r_p)

其中 r_p = Σ_i w_i^{old} · r_i = 组合收益

→ 高波动股票权重自然上升，低波动股票权重自然下降
→ 因子暴露也会随价格变动而漂移（如动量因子多头会越发集中在强势股上）
```

- **QHS 发现** (Ch.8, p.234): 纯多头组合的年化被动漂移换手率 ≈ 30-60%
- **含义**: 即使"不交易"，每年也有相当数量的换手
- **来源**: QHS Ch.8 (p.234-236)

#### 3.1.3 换手率与 Alpha 衰减

```
最优换手率的权衡：

Net IR = TC_model × IC × √N × f(rebalance_freq) - c × Turnover

其中：
  f(rebalance_freq) = 再平衡频率对信息捕捉效率的影响
  c = 交易成本系数

QHS 结论 (Ch.8, p.267):
  当信息半衰期 τ 较短时，换手率约束会严重压缩 IR
  当 τ 较长时（如价值因子，τ ≈ 6-12 个月），换手率约束影响较小
```

**常见因子的信息半衰期** (Tortoriello):

| 因子类型 | 信息半衰期 | 建议再平衡频率 |
|---------|-----------|--------------|
| 短期反转 | 1-5 天 | 日度/周度 |
| 动量 | 1-3 个月 | 月度 |
| 质量 | 3-6 个月 | 季度 |
| 价值 | 6-18 个月 | 半年/年度 |
| 低波动 | 6-12 个月 | 半年/年度 |

---

### 3.2 交易成本：机构级精算

#### 3.2.1 交易成本分解（机构级）

```
Total Implementation Cost = Explicit Costs + Implicit Costs

Explicit Costs:
  - 佣金（Commission）: $0.001-0.01/股，取决于经纪商和通道
  - 交易所费用（Exchange fees）: 小额固定
  - 税费: 印花税（中国市场 0.1% 卖方）、资本利得税等

Implicit Costs:
  - 买卖价差（Bid-Ask Spread）: 流动性越好价差越小
    Spread_bps = 2 × (Mid - Bid) / Mid × 10000
  
  - 市场冲击（Market Impact）:
    I = η × σ_daily × (Q / V)^{0.6}
    
    η 典型值（Almgren et al.）:
      - 临时冲击系数: η_temp ≈ 0.5-1.5
      - 永久冲击系数: η_perm ≈ 0.1-0.3
  
  - 机会成本（Opportunity Cost）: 延迟交易导致的价格不利变动
    ≈ 信号衰减速度 × 执行延迟时间
  
  - 择时风险（Timing Risk）: 大宗订单分批执行时的价格波动
```

- **来源**: QHS Ch.12 (p.396-414); N Ch.5 (p.110-117); Almgren et al. (2005)

#### 3.2.2 冲击成本经验公式（Almgren-Chriss-Kruman）

```
ΔP/P = γ · sign(Q) · |Q/V|^δ · σ · √T

常用参数校准（美股大盘股）:
  γ ≈ 0.15 (临时冲击)
  δ ≈ 0.6
  T = 执行时间窗口（日为单位）

中国市场调整:
  γ ≈ 0.2-0.4（流动性较差，冲击更大）
  δ ≈ 0.5-0.7
```

- **来源**: QHS Ch.12 (p.398-405); Almgren et al. (2005)

#### 3.2.3 容量约束（Capacity Constraints）

```
策略容量上限 ≈ (策略目标 Alpha) / (单位规模边际成本增加 50% 时的规模)

规模增加导致成本上升的机制：
  1. 市场冲击随规模线性/超线性增加
  2. 流动性限制使大订单只能分多日执行
  3. 择时风险随持仓规模增加
  4. 小盘股的投资范围收窄

Ding, Martin & Yang (2008) 发现: 
  当 AUM 超过策略容量 50% 时，Alpha 开始出现显著衰减
  衰减模式呈倒 U 型
```

- **来源**: QHS Ch.12 (p.405-414); N Ch.5 (p.119-120)

---

### 3.3 约束可行性分析

#### 3.3.1 约束可行性矩阵

```
判断约束集是否可行：

给定约束 {g_i(w) ≤ 0, h_j(w) = 0}，检查是否存在满足所有约束的 w。

常见不可行场景：
  1. 行业权重下限之和 > 100%
  2. 个股权重上限之和 < 目标集中度
  3. 换手率上限 < 被动漂移所需的最小换手
  4. 多空比率约束与行业中性冲突

解决方法：
  - 松弛次要约束（扩大可行域）
  - 引入松弛变量（允许微小违反，施加惩罚）
  - 分层优化：先求无约束解，再逐步施加约束
```

- **来源**: QHS Ch.11 (p.390-394); N Ch.6 (p.136-150)

#### 3.3.2 Long-Only 约束的信息损失

```
QHS Ch.11 (p.374-379) 分析：

Long-only 约束导致：
  1. 负 Alpha 股票无法做空 → 丧失负向收益来源
  2. 组合必须 100% 投资 → 即使所有股票 Alpha 为负也不能空仓
  3. Transfer Coefficient 通常降至 0.4-0.6

Clarke et al. (2002) 近似：
  TC_longonly ≈ √(2/π) × σ_α / (σ_α + σ_m)
  
  其中 σ_α = Alpha 离散度，σ_m = 市场风险
  
  → 当 Alpha 信号较弱时（σ_α 小），TC 更低
  → 当市场波动大时（σ_m 大），TC 更低
```

- **来源**: QHS Ch.11 (p.374-379)

---

## 4) 可落地字段清单

> 组合层指标：ex-ante risk、factor exposure、turnover、TC、drawdown 控制等

### 4.1 风险类字段

#### FIELD-P01: `exante_tracking_error_pct` — Ex-Ante 跟踪误差（%）

- **定义口径**: `sqrt(w_a' · Σ · w_a) × 100`，其中 w_a = w_p - w_b
- **数据需求**: 组合权重、基准权重、协方差矩阵 Σ（或因子模型参数）
- **计算频率**: 每日（组合权重更新后即时计算）
- **常见陷阱**:
  - 使用样本协方差矩阵时，ex-ante TE 通常低估实际 TE（20-40%偏差）
  - 需用 Ledoit-Wolf 或因子模型压缩后的 Σ 估计
  - 对新兴市场经济体，Σ 估计需使用更长的历史窗口
- **适用边界**: 所有主动管理组合
- **建议分级**: **P0**
- **引用页码**: QHS Ch.2 (p.38-45)

---

#### FIELD-P02: `factor_exposure_{factor_name}` — 因子暴露

- **定义口径**: `b_k = Σ_i w_i · B_{i,k}`，组合在因子 k 上的加权暴露
  - 标准化：`(b_k - mean(B_k)) / std(B_k)`（以横截面 z-score 表示）
- **数据需求**: 组合权重、每只股票的因子暴露值 B_{i,k}
- **计算频率**: 每日
- **常见陷阱**:
  - 因子暴露随时间漂移，需设定偏离阈值触发再平衡
  - 市值因子暴露与行业暴露常有共线性，需正交化
  - 不同数据源对同一因子的定义可能不同（如 Value 可用 B/P 或 E/P）
- **适用边界**: 多因子策略、风险平价策略
- **建议分级**: **P0**
- **引用页码**: QHS Ch.3 (p.60-64)

---

#### FIELD-P03: `pct_contribution_to_risk_{name}` — 风险贡献占比

- **定义口径**: `PCTR_i = w_i · (Σ · w)_i / (w' · Σ · w) × 100%`
- **数据需求**: 组合权重、协方差矩阵
- **计算频率**: 每日
- **常见陷阱**:
  - PCTR 总和 = 100%，但单个股 PCTR 可正可负（对冲头寸为负贡献）
  - 高杠杆组合中，PCTR 可能超过 100%（某些头寸风险贡献 > 100%）
  - 需分别计算因子 PCTR 和个股特异风险 PCTR
- **适用边界**: 所有组合
- **建议分级**: **P0**
- **引用页码**: QHS Ch.3 (p.72-76)

---

#### FIELD-P04: `value_at_risk_95_1d_pct` — 1 日 VaR（95%，%）

- **定义口径**: `VaR = μ_p - z_{0.95} · σ_p`，其中 σ_p = √(w'Σw)
  - 参数法假设正态分布
  - 历史模拟法：取过去 252 日组合收益分布的 5% 分位数
- **数据需求**: 组合权重、Σ（或历史组合收益序列）
- **计算频率**: 每日
- **常见陷阱**:
  - 正态假设低估了尾部风险（实际分布肥尾）
  - 可用 Cornish-Fisher 展开修正偏度/峰度影响
  - 压力测试应作为 VaR 的补充（而非替代）
- **适用边界**: 所有组合
- **建议分级**: **P1**
- **引用页码**: QHS Ch.3 (p.72)

---

#### FIELD-P05: `conditional_var_95_1d_pct` — 条件 VaR / Expected Shortfall（%）

- **定义口径**: `CVaR = E[r_p | r_p < -VaR]`，即损失超过 VaR 时的平均损失
- **数据需求**: 同 VaR
- **计算频率**: 每日
- **常见陷阱**:
  - CVaR 计算需要足够多的极端样本（建议至少 500 日历史数据）
  - 子可加性：CVaR 满足，VaR 不满足（组合 VaR 可能 > 成分 VaR 之和）
- **适用边界**: 风控要求高的组合
- **建议分级**: **P1**
- **引用页码**: QHS Ch.3 (p.72-74)

---

### 4.2 组合结构与效率字段

#### FIELD-P06: `turnover_annualized_pct` — 年化换手率（%）

- **定义口径**: `Σ_month |Turnover_month| × 12`，或日度累加年化
  - 精确公式：`(1/2) × Σ_t Σ_i |w_{i,t} - w_{i,t-1}^{drifted}| × 252/T`
- **数据需求**: 组合权重序列（日度或月度）
- **计算频率**: 月度/季度
- **常见陷阱**:
  - 不区分"主动换手"（再平衡）与"被动换手"（现金流入/流出）
  - 建议拆分为：`turnover_active` + `turnover_passive` + `turnover_flow`
  - IPO/退市/停牌导致的被动换手需单独标记
- **适用边界**: 所有主动策略
- **建议分级**: **P0**
- **引用页码**: QHS Ch.8 (p.233-236)

---

#### FIELD-P07: `transfer_coefficient` — 传递系数

- **定义口径**: `TC = corr(w_unconstrained, w_constrained)`
  - 实际计算：用有约束和无约束优化的权重向量计算 Pearson 相关系数
- **数据需求**: 无约束优化权重、有约束优化权重
- **计算频率**: 月度（或约束变更时）
- **常见陷阱**:
  - TC 接近 0 时数值不稳定（两向量几乎正交）
  - 需确保两次优化使用相同的 Σ 和 α 输入
  - 约束极多时，TC 参考 Clarke et al. 的解析近似
- **适用边界**: 有显著约束的主动策略
- **建议分级**: **P1**
- **引用页码**: QHS Ch.11 (p.379-389)

---

#### FIELD-P08: `information_ratio_annualized` — 信息比率（年化）

- **定义口径**: `IR = (r_p - r_b)_mean / std(r_p - r_b) × √252`
  - 或：`IR = TC × IC × √N`（FLAM 分解）
- **数据需求**: 组合日收益、基准日收益（至少 2 年数据）
- **计算频率**: 月度滚动
- **常见陷阱**:
  - Jobson-Korkie 检验：IR 差异的统计显著性需校正
  - 短期（<2 年）IR 估计误差极大
  - 存活者偏差会高估 IR
- **适用边界**: 所有主动策略
- **建议分级**: **P0**
- **引用页码**: QHS Ch.4 (p.81-94)

---

#### FIELD-P09: `active_share_pct` — 主动份额（%）

- **定义口径**: `Active Share = (1/2) × Σ_i |w_{p,i} - w_{b,i}| × 100`
- **数据需求**: 组合权重、基准权重
- **计算频率**: 月度
- **常见陷阱**:
  - Active Share 与跟踪误差不完全等价（高 AS 可能低 TE，若选股相关性高）
  - Cremers & Petajisto (2009) 分类：
    - AS < 60%： closet indexer
    - 60% ≤ AS < 90%： moderately active
    - AS ≥ 90%： highly active / stock picker
- **适用边界**: 主动管理基金评价
- **建议分级**: **P1**
- **引用页码**: Cremers & Petajisto (2009)

---

### 4.3 交易成本监控字段

#### FIELD-P10: `estimated_tc_bps` — 预估交易成本（基点）

- **定义口径**: 对每个计划交易 Δw_i：
  ```
  TC_i = commission_i + spread_i + η_i × σ_i × |Δw_i × AUM / ADV_i|^{0.6}
  total_TC_bps = Σ_i TC_i / AUM × 10000
  ```
- **数据需求**: 计划交易向量 Δw、各股票 ADV（日均成交额）、波动率 η 冲击系数
- **计算频率**: 每次再平衡前（预交易估计）
- **常见陷阱**:
  - η 系数需定期校准（建议每季度用实际交易数据回归更新）
  - 市场压力期（如 2020 年 3 月）η 可能临时飙升 2-5 倍
  - 暗池/算法交易可降低冲击，模型需区分执行渠道
- **适用边界**: 所有需执行交易的策略
- **建议分级**: **P0**
- **引用页码**: QHS Ch.12 (p.396-405); Almgren et al. (2005)

---

#### FIELD-P11: `realized_tc_bps` — 实现交易成本（基点）

- **定义口径**: `(execution_price - decision_price) / decision_price × 10000 × sign(Δw)`
  - 加权平均：`Σ_i (shares_i × realized_tc_i) / total_shares`
- **数据需求**: 决策时间价格、实际成交均价、成交量
- **计算频率**: 每笔交易/每日/每月汇总
- **常见陷阱**:
  - "决策价格"的定义可能有歧义（信号产生时 vs 订单发出时）
  - 需区分"交易后成本"（post-trade）与"交易前估计"（pre-trade）
  - 收盘价决策的组合，实现 TC 需用次日开盘价作为 benchmark
- **适用边界**: 执行质量监控
- **建议分级**: **P0**
- **引用页码**: QHS Ch.12 (p.414-427)

---

#### FIELD-P12: `tc_slippage_ratio` — 预估/实现 TC 偏差比

- **定义口径**: `realized_tc_bps / estimated_tc_bps`
- **含义**: 
  - 比率 ≈ 1：模型校准良好
  - 比率 >> 1：模型低估成本（市场条件恶化或模型过时）
  - 比率 << 1：模型高估成本（市场条件改善或执行优化有效）
- **建议分级**: **P1**

---

### 4.4 Drawdown 控制字段

#### FIELD-P13: `max_drawdown_pct` — 最大回撤（%）

- **定义口径**: `max_{t} [(peak_t - trough_t) / peak_t × 100]`
  - 从净值高点到低点的最大跌幅
- **数据需求**: 组合净值序列（日度）
- **计算频率**: 每日
- **常见陷阱**:
  - 需区分"绝对回撤"（组合自身）和"相对回撤"（对基准）
  - 最大回撤不是回撤期望，不能用于前瞻性风险控制
  - 不同时间窗口（1 年/3 年/5 年）的最大回撤差异可能很大
- **适用边界**: 所有策略
- **建议分级**: **P0**

---

#### FIELD-P14: `drawdown_current_pct` — 当前回撤（%）

- **定义口径**: `(current_nav - max_nav_since_inception) / max_nav_since_inception × 100`
- **数据需求**: 组合净值
- **计算频率**: 每日
- **建议分级**: **P0**

---

#### FIELD-P15: `drawdown_control_flag` — 回撤控制标志

- **定义口径**: 
  ```
  if current_drawdown > threshold_1: flag = "yellow" (预警)
  if current_drawdown > threshold_2: flag = "orange" (减仓)
  if current_drawdown > threshold_3: flag = "red" (强平)
  ```
  - 阈值建议：threshold_1 = 5%, threshold_2 = 10%, threshold_3 = 15%（根据策略风险特征调整）
- **触发动作**:
  - Yellow: 降低风险暴露至正常水平的 80%
  - Orange: 降至 50%，暂停新增 Alpha 信号
  - Red: 降至 20% 或全部平仓，人工复核
- **建议分级**: **P0**

---

### 4.5 容量与规模字段

#### FIELD-P16: `strategy_capacity_est_usd` — 策略容量估计（USD）

- **定义口径**: 
  ```
  Capacity = min(
    AUM where marginal_alpha_decay = 50%,
    Σ_i (ADV_i × max_single_stock_pct),
    AUM where avg_impact_cost = half_of_expected_alpha
  )
  ```
- **数据需求**: 各股票 ADV、预期 Alpha、冲击系数
- **计算频率**: 月度
- **建议分级**: **P1**

---

#### FIELD-P17: `alpha_decay_slope` — Alpha 衰减斜率

- **定义口径**: 滚动 IR（如 12 月）对时间的回归斜率
  - `negative_slope` 表示 IR 在衰减
- **数据需求**: 组合月度收益、基准月度收益（至少 36 个月）
- **计算频率**: 月度
- **常见陷阱**:
  - 需区分 Alpha 衰减与市场环境变化（如低波动期所有策略表现都差）
  - 建议同时计算"相对于同类策略"的 IR 衰减
- **建议分级**: **P1**

---

### 字段清单汇总表

| 字段编号 | 字段名 | 建议分级 | 数据需求 | 核心用途 |
|---------|--------|---------|---------|---------|
| FIELD-P01 | exante_tracking_error_pct | P0 | 权重+Σ | 风险预算 |
| FIELD-P02 | factor_exposure_{name} | P0 | 权重+因子暴露 | 因子漂移监控 |
| FIELD-P03 | pct_contribution_to_risk | P0 | 权重+Σ | 风险集中度 |
| FIELD-P04 | value_at_risk_95_1d_pct | P1 | 权重+Σ/历史 | 尾部风险 |
| FIELD-P05 | conditional_var_95_1d_pct | P1 | 权重+Σ/历史 | 预期损失 |
| FIELD-P06 | turnover_annualized_pct | P0 | 权重序列 | 换手监控 |
| FIELD-P07 | transfer_coefficient | P1 | 无约束+有约束权重 | 约束效率 |
| FIELD-P08 | information_ratio_annualized | P0 | 收益+基准 | 策略绩效 |
| FIELD-P09 | active_share_pct | P1 | 权重+基准 | 主动程度 |
| FIELD-P10 | estimated_tc_bps | P0 | Δw+ADV+σ | 交易前成本 |
| FIELD-P11 | realized_tc_bps | P0 | 成交数据 | 交易后成本 |
| FIELD-P12 | tc_slippage_ratio | P1 | P10+P11 | 模型校准 |
| FIELD-P13 | max_drawdown_pct | P0 | 净值序列 | 历史极值 |
| FIELD-P14 | drawdown_current_pct | P0 | 净值序列 | 当前风险 |
| FIELD-P15 | drawdown_control_flag | P0 | P14+阈值 | 风控触发 |
| FIELD-P16 | strategy_capacity_est_usd | P1 | ADV+Alpha | 规模管理 |
| FIELD-P17 | alpha_decay_slope | P1 | 月度收益 | 策略健康 |

---

*（第二部分结束，第三部分继续：5) 组合层偏差清单 + 6) 冲突与裁决 + 7) YAML 索引卡）*
