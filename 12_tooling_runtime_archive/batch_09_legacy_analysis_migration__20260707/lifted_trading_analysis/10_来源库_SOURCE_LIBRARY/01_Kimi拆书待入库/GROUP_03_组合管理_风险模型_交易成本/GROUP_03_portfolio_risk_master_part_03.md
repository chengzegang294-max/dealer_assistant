# GROUP 03: 组合管理 + 风险模型 + 交易成本 — Part 03
## 5) 研究与回测的"组合层偏差清单"

> 幸存者偏差、回填偏差、指数成分变更、前视偏差、挑选基准偏差等，附对策

### 5.1 幸存者偏差（Survivorship Bias）

- **问题描述**: 回测时仅使用当前存活股票的历史数据，排除了已退市/破产股票
- **影响方向**: 系统性高估策略表现（失败者被排除，留下的是赢家）
- **量化影响**: 
  - 美股长周期（1950-2000）价值策略：幸存者偏差可高估年化收益 1.5-2.5%
  - 中国市场：ST/退市股票偏低估值，价值因子回测偏差尤为显著
- **检测方法**: 
  - 比较"含退市"与"不含退市"的回测结果差异
  - 统计退市股票在策略信号中的分布
- **对策**:
  1. 使用包含退市股票的历史数据库（如 CRSP 全历史、万得全A含退市）
  2. 对退市股票假设清算价值（通常为 0 或残余价值）
  3. 在回测中显式标记退市路径：信号产生 → 持有期间退市 → 按退市价结算
- **来源**: QHS Ch.1 (p.8); N Ch.9 (p.197-217)

---

### 5.2 回填偏差 / 前视偏差（Look-Ahead Bias）

- **问题描述**: 在时刻 t 使用了 t+1 或之后才能知道的信息
- **常见场景**:
  - 财务报表数据：3 月 31 日季报在 4 月底才公布，回测中若在 4 月 1 日使用即构成前视
  - 指数成分变更：成分调整在生效日 "T" 执行，但市场通常提前知道
  - 分析师一致预期：实际值在报告期后才逐步更新
- **量化影响**: 可高估信息型因子（如 E/P、ROE）IC 达 30-50%
- **检测方法**:
  - 对每条数据记录 "asof_date"（数据可获取时间）≠ "report_date"（报告期截止日）
  - 检查信号产生时间与数据公开时间的 gap 分布
- **对策**:
  1. 严格使用 "point-in-time" 数据库（如 WRDS 的 CRSP/COMPUSTAT 合并库）
  2. 对财务报表数据施加发布延迟（季度报告 +45 天，年度报告 +90 天）
  3. 建立数据可用性审计日志：每个数据点的首次获取时间戳
- **来源**: QHS Ch.1 (p.8-9); N Ch.8 (p.179-187)

---

### 5.3 指数成分变更偏差（Index Reconstitution Bias）

- **问题描述**: 指数成分股调整前后的价格行为导致策略收益虚高
- **机制**:
  - 被纳入指数的股票在被纳入前上涨（指数基金提前买入预期）
  - 被剔除指数的股票在被剔除前下跌（指数基金提前卖出）
  - 若在回测中按 "当前指数成分" 选股，策略享受了这一价格趋势但不承担调整冲击
- **量化影响**: 
  - S&P 500 纳入效应：被纳入股票在公告日到生效日平均上涨 3-8%
  - 策略若在回测中始终持有当前成分股，年化收益虚高约 0.5-1.5%
- **对策**:
  1. 使用历史指数成分序列（每月/每季度的实际成分）
  2. 避免使用指数成分作为选股池过滤条件
  3. 替代方案：使用全市场股票作为投资域（universe），独立设定流动性筛选条件
- **来源**: N Ch.9 (p.207-210)

---

### 5.4 挑选基准偏差（Benchmark Selection Bias）

- **问题描述**: 选择与策略风格匹配的基准，使 Alpha 显得更大
- **常见手法**:
  - 价值策略用成长股指数做基准（价值因子天然跑赢成长股指数）
  - 小盘策略用大盘指数做基准（小盘溢价使 Alpha 虚高）
  - 行业集中策略用不相关指数做基准
- **检测方法**:
  - 计算策略与多个候选基准的 Beta、R²
  - 检查组合的行业/市值/风格暴露与基准的差异
  - 用 "风格纯化" 基准（如 BARRA 风格指数）做稳健性检验
- **对策**:
  1. 使用与组合实际暴露最匹配的基准（高 R²）
  2. 报告多基准结果（宽基指数 + 风格指数 + 等权指数）
  3. 进行 "纯 Alpha" 检验：将组合收益对多个因子回归，检查残差是否显著
- **来源**: QHS Ch.4 (p.100-108)

---

### 5.5 数据挖掘偏差 / 过度拟合（Data Mining Bias）

- **问题描述**: 测试过多因子/参数组合后偶然发现"显著"结果
- **White (2000) Reality Check**:
  ```
  若独立测试 K 个策略，至少一个达到显著性水平 α 的概率：
  P(至少一个假阳性) = 1 - (1 - α)^K
  
  K=20, α=5%:  P = 64%
  K=100, α=5%: P = 99.4%
  ```
- **对策**:
  1.  Bonferroni 校正：调整后的 α' = α / K
  2.  样本外测试：70% 数据训练 + 30% 数据验证，且只做一次验证
  3.  交叉验证：滚动窗口回测，避免特定时间段的偶然性
  4.  经济学直觉：每个因子需有坚实的经济理论基础（非纯统计发现）
  5.  简化法则：参数越少、模型越简单，越不容易过拟合
- **来源**: N Ch.11 (p.266-270)

---

### 5.6 交易成本低估偏差（Transaction Cost Underestimation）

- **问题描述**: 回测中使用过低的交易成本假设
- **常见低估来源**:
  - 仅使用佣金，忽略冲击成本
  - 使用线性成本模型而非二次型
  - 对流动性差的小盘股使用大盘股的冲击系数
  - 忽略市场冲击的 "冰山效应"（大单拆小单执行，累计冲击 > 单次小单冲击）
- **量化影响**: 高频策略（月换手 > 100%）的成本低估可达年化 5-15%
- **对策**:
  1. 使用机构级交易成本模型（如 ITG、Barra 的模型）
  2. 保守估计：回测中使用实际成本的 1.5-2 倍作为安全垫
  3. 对每笔模拟交易计算实际冲击：`impact = η × σ × (Q/V)^{0.6}`
  4. 区分交易场所：主板的冲击 < 创业板/科创板 < 新三板
- **来源**: QHS Ch.12 (p.414-427); N Ch.5 (p.119-124)

---

### 5.7 容量幻觉偏差（Capacity Illusion Bias）

- **问题描述**: 小规模回测的高收益无法在大规模资金下复现
- **机制**:
  - 回测中假设所有股票都可以按收盘价无冲击成交
  - 实际中，小盘股日均成交额仅数百万，无法承载大资金
  - 策略从 1 亿扩展到 10 亿时，小盘股持仓比例被迫下降，策略特征改变
- **对策**:
  1. 回测中加入容量约束：`position_i ≤ liquidity_ratio × ADV_i`
  2. 分规模回测：1 亿 / 5 亿 / 10 亿 / 50 亿分别回测
  3. 流动性分层：按 ADV 分 quintile，分别评估各层容量上限
  4. 滑点递增模型：规模越大，单位冲击成本越高
- **来源**: QHS Ch.12 (p.405-414)

---

### 5.8 组合层偏差检查清单（Checklist）

回测启动前必须逐项确认：

| # | 检查项 | 通过标准 | 数据来源要求 |
|---|--------|---------|------------|
| 1 | 数据含退市股票？ | 退市股数量 / 总历史股票数 > 5% | CRSP/万得全A |
| 2 | 财务报表已加发布延迟？ | 季报 +45天，年报 +90天 | Point-in-time 库 |
| 3 | 指数成分使用历史序列？ | 非使用当前成分快照 | 指数提供商历史成分 |
| 4 | 基准选择有依据？ | 策略与基准 R² > 0.7 | BARRA 归因 |
| 5 | 测试策略数量有记录？ | K 已知，Bonferroni 校正已做 | 研究日志 |
| 6 | 样本外测试已完成？ | 至少 30% 数据未用于调参 | 回测框架 |
| 7 | 冲击成本按二次模型计算？ | η 系数有校准来源 | 交易数据回归 |
| 8 | 容量约束已纳入回测？ | 最大单票持仓 ≤ 5% ADV | ADV 数据 |
| 9 | 换手率估计与模型频率一致？ | 实际换手在目标 ±20% 内 | 权重序列 |
| 10 | 收益归因可追溯到因子？ | 月度归因 R² > 0.5 | BARRA/自建模型 |

---

## 6) 冲突与裁决建议

### 冲突 1: 风险模型架构选择 — 基本面因子 vs 统计因子 vs 宏观因子

- **冲突描述**:
  - **QHS Ch.3 (p.54-64)** 偏好基本面因子模型（BARRA 型）：因子有经济解释，暴露稳定
  - **N Ch.4 (p.96-106)** 指出统计因子（PCA）的优势：适应性更强，可能捕获未知风险源
  - **宏观因子模型**（Ross APT）：理论优雅但因子收益预测困难

- **建议采用的仓库口径**:
  - **主模型：基本面因子模型**（P0），辅之以统计因子的残差分析（P1）
  - **理由**:
    1. 基本面因子的经济可解释性是风控和合规的核心要求
    2. 统计因子作为"未知风险探测器"，用于识别主模型未覆盖的风险源
    3. 宏观因子用于情景分析（stress test），不进入日常风险预算
  - **实现架构**:
    ```
    日常风险预算:  基本面因子模型 (BARRA-type)
    异常检测:      PCA 残差分析 ( Top 3 主成分监控 )
    压力测试:      宏观因子冲击 ( 利率+100bp, 信用利差+200bp 等 )
    ```

---

### 冲突 2: 协方差矩阵估计 — 样本协方差 vs 因子模型 vs 压缩估计

- **冲突描述**:
  - **样本协方差**: 无模型风险，但 N>T 时奇异，估计误差大
  - **因子模型**: 大幅降低参数，但遗漏因子导致结构化风险低估
  - **Ledoit-Wolf 压缩**: 向恒等相关收缩，稳健但可能过度平滑

- **建议采用的仓库口径**:
  - **日常使用：多因子模型**（BARRA 型）
  - **备用方案：Ledoit-Wolf 压缩估计**（当因子模型未覆盖资产时）
  - **理由**:
    1. 因子模型对机构级股票数量（500-3000）是工程上的唯一可行方案
    2. Ledoit-Wolf 作为 fallback，用于新上市股票或数据不足的股票
    3. 样本协方差仅在 N << T 的子集上用于校验

---

### 冲突 3: 换手率最优频率 — 高频再平衡 vs 低频再平衡

- **冲突描述**:
  - **QHS Ch.8 (p.257-267)** 推导了信息半衰期与最优换手率的理论关系
  - **N Ch.3 (p.72)** 指出过度交易增加成本且不改善信号质量
  - **Tortoriello** 提供了不同因子的经验半衰期数据

- **建议采用的仓库口径**:
  - **按因子分层设定再平衡频率**，而非统一频率
  - **默认频率矩阵**:

| 因子类型 | 再平衡频率 | 月换手预算 | 来源 |
|---------|-----------|-----------|------|
| 短期反转 | 日度/周度 | 200-400% | QHS Ch.8 |
| 动量 | 月度 | 50-100% | Tortoriello |
| 质量/价值 | 季度/半年度 | 20-50% | Tortoriello |
| 低波动 | 半年度/年度 | 10-30% | QHS Ch.8 |

---

### 冲突 4: 交易成本模型复杂度 — 常数/线性/二次型

- **冲突描述**:
  - **N Ch.5 (p.117-124)** 比较了四种模型的复杂度与精度
  - **QHS Ch.12 (p.398-405)** 使用二次型冲击模型
  - **实务中** 许多机构仍使用线性近似（计算简便）

- **建议采用的仓库口径**:
  - **预估阶段：分段线性模型**（计算快，足够用于优化器）
  - **事后分析：二次型模型**（精确归因，用于模型校准）
  - **理由**: 分段线性在优化器中足够且计算效率高；二次型用于校准和报告

---

### 冲突 5: Long-Only vs Long-Short 架构

- **冲突描述**:
  - **QHS Ch.11 (p.374-379)** 详细分析了 Long-Only 的信息损失（TC ≈ 0.4-0.6）
  - **N Ch.4 (p.98)** 强调市场中性架构的风控优势
  - **中国市场**: 融券成本高、券源有限，纯 Long-Short 难以实现

- **建议采用的仓库口径**:
  - **中国市场**: Long-Only + 行业中性 + 风格中性（尽可能接近市场中性）
  - **海外市场（美股）**: 130/30 或纯 Long-Short（若成本可控）
  - **理由**: 中国市场融券成本（8-10% 年化）使 Long-Short 策略的做空端几乎无利可图，Long-Only + 严格中性化是务实的替代方案

---

## 7) YAML 索引卡

```yaml
group_id: GROUP_03
theme: 组合管理 + 风险模型 + 交易成本
source_books:
  - id: QHS_2007
    title: "Quantitative Equity Portfolio Management"
    author: Edward E. Qian, Ronald H. Hua, Eric H. Sorensen
    lang: en
    key_chapters: >
      Ch.2(Portfolio Theory/Mean-Variance), Ch.3(Risk Models/APT/Factor Models),
      Ch.4(Alpha Evaluation/IC/IR), Ch.5(Quant Factors),
      Ch.7(Multifactor Alpha Models), Ch.8(Turnover/Optimal Rebalancing),
      Ch.11(Constraints/IR Loss), Ch.12(Transaction Costs/Optimal Trading)
    page_range_note: "全书约450页，核心 Ch.2-3, 7-8, 11-12 (p.23-434)"
    
  - id: Tortoriello_2012
    title: "量化投资策略 如何实现超额收益Alpha"
    author: Tortoriello (托托里罗)
    lang: zh-CN (translated)
    key_chapters: "因子定义与回测、Alpha衰减、多因子组合"
    page_range_note: "全书约400页，核心因子定义与IC测试部分"
    
  - id: Ding_2012
    title: "量化投资 策略与技术 修订版"
    author: 丁鹏
    lang: zh-CN
    key_chapters: "量化选股、资产配置、程序化交易、高频交易"
    page_range_note: "全书约500页，中国市场量化实务"
    
  - id: Narang_2009
    title: "打开量化投资的黑箱"
    author: Rishi K. Narang
    lang: zh-CN (translated)
    key_chapters: >
      Ch.3(Alpha Models), Ch.4(Risk Models), Ch.5(Transaction Cost Models),
      Ch.6(Portfolio Construction), Ch.7(Execution), Ch.8(Data), Ch.9(Research)
    page_range_note: "全书约300页，核心 Ch.3-9 (p.42-217)"

worth_re_reading:
  - book: QHS_2007
    chapters: [2, 3, 7, 8, 11, 12]
    reason: >
      组合优化数学基础、风险模型架构、多因子Alpha组合、
      换手率最优控制、约束对IR的影响、交易成本与执行算法。
      这是本组的理论基石。
      
  - book: Narang_2009
    chapters: [4, 5, 6, 7]
    reason: >
      风险控制模型实务、交易成本四层模型、投资组合构建方法、
      执行算法与基础设施。补充QHS的工程实现层面。

tags:
  - portfolio_optimization
  - risk_model
  - transaction_cost
  - mean_variance_optimization
  - factor_model
  - tracking_error
  - information_ratio
  - transfer_coefficient
  - turnover
  - market_impact
  - black_litterman
  - long_only_constraint
  - capacity_constraint
  - drawdown_control
  - survivorship_bias
  - look_ahead_bias
  - data_mining_bias
  - backtest_bias
  - variance_risk_contribution
  - rebalancing
  - execution_cost

key_formula_count: 14
formula_categories:
  covariance_estimation: [FORMULA-01, FORMULA-02]
  factor_models: [FORMULA-02, FORMULA-03]
  tracking_error: [FORMULA-04, FORMULA-05]
  risk_contribution: [FORMULA-06, FORMULA-07, FORMULA-08]
  optimization: [FORMULA-09, FORMULA-10, FORMULA-11]
  turnover: [FORMULA-12]
  constraint_impact: [FORMULA-13]
  multifactor_alpha: [FORMULA-14]

field_count: 17
p0_fields: [FIELD-P01, FIELD-P02, FIELD-P03, FIELD-P06, FIELD-P08, FIELD-P10, FIELD-P11, FIELD-P13, FIELD-P14, FIELD-P15]
p1_fields: [FIELD-P04, FIELD-P05, FIELD-P07, FIELD-P09, FIELD-P12, FIELD-P16, FIELD-P17]

bias_checklist_count: 8
bias_items:
  - survivorship_bias
  - look_ahead_bias
  - index_reconstitution_bias
  - benchmark_selection_bias
  - data_mining_bias
  - transaction_cost_underestimation
  - capacity_illusion_bias

conflict_resolutions:
  - 风险模型架构: 基本面因子(P0) + PCA残差(P1) + 宏观压力测试
  - 协方差估计: 多因子模型主用 + Ledoit-Wolf备用
  - 换手率频率: 按因子分层（反转日度/动量月度/价值季度）
  - 成本模型: 分段线性(优化器) + 二次型(事后校准)
  - Long架构: 中国Long-Only+中性 / 海外130/30或Long-Short

pipeline_steps:
  - Alpha模型
  - 风险模型
  - 约束条件
  - 交易成本模型
  - 投资组合优化
  - 再平衡执行
  - 组合监控

output_files:
  - GROUP_03_portfolio_risk_master_part_01.md  # Pipeline + 风险模型公式
  - GROUP_03_portfolio_risk_master_part_02.md  # 约束摩擦 + 字段清单
  - GROUP_03_portfolio_risk_master_part_03.md  # 偏差清单 + 冲突裁决 + YAML
```

---

> 最终输出必须是 Markdown 正文，可直接保存为 .md 文件。
> 本组内容已按主题合并四本书，未按单本书拆分为多篇读书笔记。
> Kimi 提出了七步组合构建 Pipeline、14 个核心公式（含变量定义/使用条件/常见陷阱/页码引用）、
> 17 个可落地字段（P0=10, P1=7）、8 项组合层偏差检查清单（含对策）、
> 5 项跨书冲突裁决建议。
> **最终字段冻结、落盘、脚本实现由仓库方完成。**
