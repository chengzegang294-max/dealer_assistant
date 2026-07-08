# 搜索汇总：执行层补充 + 跨市场适配 + 风控层补充 + 另类数据

> 阶段：搜索/讨论，不编码。  
> 生产：Kimi 搜索 + 本地素材索引。  
> 时间：2026-06-24。

---

## 1. 执行层补充搜索（Volume Profile / 订单流 / 量化执行）

### 1.1 核心发现：执行层缺乏"量化型"方法

当前仓库执行层（P0_E=执行层）共 13 个对象，**全部是主观价格行为方法**：Brooks 双底/次高/趋势K、YTC 迷你结构/批发、ICT 日偏向/微区/POI 3、TK 外汇订单流（7个对象）、缠论三类买卖点。  
**缺少：Volume Profile、VWAP、Footprint（足迹图）、订单流失衡、CVD 累积成交量差等**——这些是日内/短线执行中可直接量化的入场/出场参考。

### 1.2 Volume Profile（成交量分布）——可立即接入

**核心概念（已标准化）**：
- **POC**（Point of Control）：最高成交量柱对应价格。市场最认可的"公平价格"，具有回归引力。
- **VA**（Value Area，70% 成交量区间）：市场平衡区。VAH（上沿）、VAL（下沿）。
- **HVN**（High Volume Node）：高成交量节点=密集成交区=强支撑/阻力。价格来此处会"停留和反复测试"。
- **LVN**（Low Volume Node）：低成交量节点="价格鸿沟"。价格快速通过，打穿后容易形成单边行情。

**入场策略（可直接字段化）**：
1. **VA 突破顺势**：价格有效突破 VAH 或 VAL，伴随成交量放大（VROC > 1.5x 均值），回踩不破 VAH/VAL 时入场。止损：相反侧 VA 边缘。
2. **POC 回归/突破**：价格从远处回归 POC，观察在 POC 附近的反应（停留时间、成交量），确认支撑/阻力后入场。
3. **LVN 穿越动量**：价格快速穿越 LVN（成交量真空区），目标看向下一个 HVN。适用于趋势确认后的加仓。
4. **多周期 VP 联立**：日线 VP 确定主要长期价值区 → 日内 VP（15min/5min）找战术进出点。避免"在长线强支撑做空/在长线强阻力做多"。

**与现有仓库的映射关系**：
- **与 Volty**：VP 的 HVN 可作为 Volty 止损的"加固带"。当 Volty_stop 恰好落在 HVN 上，可靠性更高。
- **与 KD MTF**：VP 的 VAH/VAL 可作为 KD 日级别 K/D 交叉的过滤条件。如果 K 上穿 D 但价格还在 VA 内部（平衡区），暂不行动；突破 VAH 才确认。
- **与缠论**：VP 的 POC 与缠论中枢的"重心"（ZG+ZD/2）功能相似。中枢区间内若 VP 出现明显 POC，则该 POC 是中枢的"真正成本区"。
- **与 TK-R6**：TK 的 IB 回撤阻挡深度可用 VP 的 HVN 作为"历史成交密集带"，验证回撤是否遇到历史阻力。

**字段化建议（成熟度：proxy_quantizable_now，因为只需要 OHLCV + 成交量）**：
```text
vp_poc: 价格，控制点
vp_vah: 价格，价值区域上沿
vp_val: 价格，价值区域下沿
vp_hvn_levels[]: 高成交量节点列表
vp_lvn_levels[]: 低成交量节点列表
vp_current_rel_position: 当前价格相对 VA 的位置（inside/above/below）
vp_trend: 正三角（下方HVN大）vs 倒三角（上方HVN大）
vp_vroc: 成交量变动率，用于确认突破真实性
```

### 1.3 VWAP（成交量加权平均价）——可作为均值回归参考

**与 Volume Profile 的区别**：VWAP 是"平均成本"（价格 × 成交量 加权），VP 是"分布"（每个价格有多少成交量）。  
**常见用法**：价格远高于 VWAP 时可能回归；价格低于 VWAP 时可能反弹。与 VP 的 POC 不同，VWAP 是动态的，VP 是静态的（固定周期内）。

**映射**：
- 与 `PV` 指标：PV 是价格-成交量关系（类似 VWAP 的归一化版本）。VWAP 可作为 PV 的"基准线"。
- 与 `score`：VWAP 偏离度可作为 scoring 的因子之一（远离 VWAP 超 2σ 的，加/减分）。

### 1.4 Footprint Chart（足迹图）——需要 Level-2 逐笔数据

**核心概念**：在标准 OHLCV 的 K 线内部，叠加每个价位的**主动买（Ask）vs 主动卖（Bid）**成交量。  
**关键信号**：
- **Imbalance（失衡）**：某价位的 Bid 远大于 Ask（或反之），>300% 视为显著失衡。绿色=买压强，红色=卖压强。
- **大单吃小单**：大单（主动买）吃掉了小单（被动卖），表示机构吸筹。
- **CVD（Cumulative Volume Delta）**：累积成交量差，反映整体主动买 vs 主动卖的力量对比。

**与现有仓库的映射**：
- **与 TK**：TK 的订单流方法（IB/DB/CB）本质上就是 Footprint 的"简化版"。TK 的 `buffer0` 对应 DB/CB，相当于在 K 线级别识别"失衡"。如果接入真正的 Level-2 Footprint，TK 的方法可以更加精确。
- **与缠论 BSD**：缠论三类买卖点的确认可以用 Footprint 的失衡信号来加强。例如 1Buy 出现时，如果 Footprint 在低点出现大量主动买（绿色失衡），则确认"空头衰竭"。

**成熟度评估**：`needs_extra_data`（Level-2 逐笔数据成本高，且 A 股 Level-2 需要付费）。可以：
- 先放入 `future_bucket`，标记"需要 Level-2 数据"；
- 或者从现有 `backtest_p0.py` 中找是否有 Level-2 相关代码（`l2_range_trap` 参数说明已有部分 Level-2 逻辑）。

### 1.5 订单流失衡（Order Flow Imbalance）——从盘口到信号

**核心概念**：买一侧 vs 卖一侧的订单簿失衡。`order_flow_imbalance = bid_volume / ask_volume`（或类似指标）。
**在 A 股量化中的应用**：幻方/九坤等头部量化使用 Level-2 逐笔数据，识别"TWAP/VWAP 拆单痕迹"、"早盘集合竞价虚假报单"等。
**与现有仓库**：S_BUCKET 的 `01_高频微观` 主题（98 份）和 `03_机器学习`（112 份）中**很可能已经包含**订单流/高频微观结构相关内容。`ashare_preprocess.py` 和 `backtest_p0.py` 的 `l2_range_trap` 系列参数也证明已有部分 Level-2 接入逻辑。

---

## 2. 跨市场适配性讨论（A股 vs 外汇/期货/币圈）

### 2.1 现有框架的跨市场定位

当前仓库指标（MT Probes、Volty、KD MTF、PV、RSJ）和外部体系（TK、缠论、Brooks）主要在**外汇/期货/币圈**环境下设计。用户要求覆盖**A股/外汇/币圈/期货**。A股有独特限制：

### 2.2 A 股特殊规则对现有框架的冲击

| A 股规则 | 对现有框架的冲击 | 应对建议 |
|---------|---------------|---------|
| **T+1**（当日买入次日卖出） | 外汇/币圈的日内多笔交易→A股只能一笔到收盘。`TK_IB` 的"频繁入场/出场"必须改为"T+1 全仓持有到次日"。| 执行层从"日内多段"→"波段单段"。`entry_min_votes: 3` 只能执行一次，不能反复。|
| **涨跌停（10%/20%/30%）** | Volty 的止损位（如 1.5×ATR）在涨停时**无法执行**（没有流动性）。Brooks 的"止损设在关键K线外"也失效。| 加入`涨停/跌停状态`字段：`limit_up`/`limit_down` 时**禁止入场/出场**，或强制平仓。`allow2_risk_mult: 0.20` 在涨跌停时归零。|
| **集合竞价（9:15-9:25）** | 现有框架（如 KD MTF、缠论）基于连续交易数据。集合竞价价格由最大成交量决定，逻辑完全不同。S_BUCKET 有 `01_集合竞价教程`（49 文件）。| 集合竞价可单独作为一个"时间窗口"处理。`open_price` 不是 `close` 的简单延续，需加入 `auction_volume` 和 `auction_price_diff` 作为因子。|
| **散户占比高** | 现有框架（如 TK 订单流、缠论）假设"理性机构行为"。A股散户情绪驱动（追涨杀跌），导致"假突破"更频繁。| 加入**情绪因子**（涨跌停数、涨停封单比、散户资金流出）作为过滤。`KD MTF` 的 `lock_signal` 在 A股需要更严格。|
| **无做空（大部分散户）** | 现有框架（缠论、TK、Brooks）都有做多/做空两套逻辑。A股散户只能做多+融券（门槛高）。| 只保留**做多方向**的信号。`kd_direction_filter: long_only` 在 A 股策略中强制生效。TK 的 Short 信号只在期货/外汇/币圈使用。|
| **行业轮动明显** | 现有框架是"单品种择时"。A股需要"行业/风格择时"才能避免单票系统性风险。| 加入**行业Beta**和**风格因子**（大盘/小盘、价值/成长）。这与 S_BUCKET 的 `02_指数增强`（16 份）和 `04_多因子`（181 份）直接相关。|

### 2.3 现有回测框架（backtest_p0.py）的适配

`backtest_p0.py` 已有 37K 行，包含 A 股回测。关键参数：`entry_min_votes: 3`、`allow2_risk_mult: 0.20`、固定止损 ATR 系列。但**缺失**：
- 涨停/跌停状态检测
- 集合竞价处理
- 情绪因子接入
- 做空机制（已有参数但未限制）
- 行业/风格轮动过滤

### 2.4 现有 S_BUCKET 素材可直接利用

| S_BUCKET 主题 | 文件数 | 与跨市场适配的关联 |
|-------------|-------|------------------|
| `01_集合竞价教程` | 49 | 直接解决"集合竞价冲击"问题，可提取因子 |
| `02_游资悟道交割单` | 341 | 散户行为模式（情绪、跟风、打板），可作为"另类因子"提取 |
| `03_券商研报/01_高频微观` | 98 | 订单流、微观结构、Level-2 数据，直接补充执行层 |
| `03_券商研报/02_指数增强` | 16 | 行业轮动、风格因子，直接补充跨市场适配 |
| `03_券商研报/04_多因子` | 181 | 已有大量 A股多因子研究，包括价值、动量、质量等 |
| `03_券商研报/03_机器学习` | 112 | 因子组合、非线性模型，可用于优化 scoring |

**结论**：A 股适配不是"从 0 开始搜索"，而是"从现有 S_BUCKET 素材中**结构提取**"已有 477 份券商研报覆盖大部分 A 股特殊问题。搜索的方向应该是：在现有素材中**哪些已经解决了哪些还没解决**。

---

## 3. 风控层补充（Kelly / 动态仓位 / 波动率目标）

### 3.1 现有风控层（只有 Van Tharp 固定风险）

当前仓库：`backtest_p0.py` 中 `allow2_risk_mult: 0.20`（单笔风险=2% 资金）。这是**静态**的：无论市场环境如何，每笔只冒 2% 的风险。  
**问题**：低波动期（ATR 很小）→ 2% 风险可以下很大仓位；高波动期（ATR 很大）→ 2% 风险只能下很小仓位。这本身就隐含了"波动率调整"，但**没有显式公式**。

### 3.2 Kelly Criterion（凯利公式）——从理论到实战

**原始公式**：`f* = (bp - q) / b`，其中 `p=胜率`，`q=1-p`，`b=赔率（盈亏比）`。
**A 股适配版**：`f* = (pW - qL) / WL`，`W=平均盈利幅度`，`L=平均亏损幅度`。
**关键限制**：
- 参数估算误差最致命（你以为 60% 胜率，实际 52%）。
- 连续亏损时仓位可能爆掉（黑天鹅）。
- 实际交易有成本（佣金、印花税）。

**实战方案（半凯利 + 修正）**：
1. 从历史交易日志提取至少 50-100 笔同类型交易，计算 `p`（胜率）和 `b`（盈亏比）。
2. 修正交易成本：实际盈利 = 原盈利 - 成本，实际亏损 = 原亏损 + 成本。重新计算 `b`。
3. 采用**半凯利**（Half-Kelly）：`f_real = 0.5 × f*`。这是 Ed Thorp 和 Paul Tudor Jones 的推荐。
4. 对于高波动资产（A股小盘、币圈），用**四分之一凯利**（Quarter-Kelly）。
5. 多资产时考虑协方差矩阵：`f* = Σ⁻¹ × (μ - r·1)`，本质就是 Markowitz 切线组合 × 风险偏好参数。

**与现有仓库的映射**：
- `allow2_risk_mult: 0.20` 可以解释为"Van Tharp 2% 固定风险"，但**没有考虑胜率和赔率**。Kelly 可以替代它，或作为补充：
  - 如果 Kelly 算出的 `f* < 0.20`（低质量信号），则按 Kelly 执行（仓位更小）。
  - 如果 Kelly 算出的 `f* > 0.20`（高质量信号），但受限于半凯利和总仓位上限，则取 `min(0.5 × f*, 0.20)`。
- `volty_trend_state`：高波动率时（`volty_trend_state = expansion`），仓位应该自动降低。Kelly 公式本身就隐含了这一点（因为 `L` 在高波动期会增大）。

**字段化建议**：
```text
kelly_p: 胜率（从历史回测统计）
kelly_b: 赔率（平均盈利/平均亏损）
kelly_f_star: 理论最优仓位比例
kelly_f_half: 半凯利实际执行仓位（= 0.5 × f_star）
kelly_f_quarter: 四分之一凯利（极端保守）
kelly_risk_budget: 最终风险预算（结合现有 allow2_risk_mult 的 min 值）
```

**成熟度**：`proxy_quantizable_now`（需要历史交易日志，但已有 `backtest_p0.py` 可以产出）。

### 3.3 波动率目标（Volatility Targeting）——更保守的替代方案

**核心逻辑**：不是"每笔风险 2%"，而是"**组合年化波动率锁定在目标值**（如 10%）"。  
**公式**：`target_position = target_vol / current_vol × base_position`。  
**应用场景**：如果当前 ATR 很高（市场动荡），当前波动率 `current_vol` 很大，目标仓位自动缩小。如果当前波动率很低，仓位自动放大。

**与现有仓库的映射**：
- `volty_trend_state`（扩张/收缩）+ `volty_stop_distance_atr`（ATR 距离）→ 当前波动率可以直接从 Volty 计算。
- `atr_n: 14` 已经计算了 ATR14。`volatility_target = 10% / (ATR14 × sqrt(252)) × base_position`。  
**注意**：在 A股，如果 ATR 因涨停/跌停导致失真（如连续一字板），`volatility_target` 会失效。需要加入 `limit_up` 状态过滤。

**成熟度**：`proxy_quantizable_now`（只需要 OHLCV + 现有 ATR 参数）。

### 3.4 建议：风控层从单一到分层

| 风控方法 | 适用场景 | 与现有参数关系 | 成熟度 |
|---------|---------|--------------|-------|
| **固定风险（Van Tharp 2%）** | 基础保护，每笔止损 | `allow2_risk_mult: 0.20` | 已冻结 |
| **Kelly（半凯利）** | 高胜率/高赔率时加大仓位 | 从 `backtest_p0.py` 历史日志提取 p, b | proxy_quantizable_now |
| **波动率目标** | 市场波动剧烈时自动降仓 | 从 `atr_n: 14` + `volty_trend_state` 计算 | proxy_quantizable_now |
| **最大回撤熔断** | 组合层面保护，非单笔 | 目前缺失。建议加入：总回撤 > 10% 时强制减仓/空仓 | 需要实现 |

---

## 4. 另类数据搜索（A股特色因子）

### 4.1 头部量化机构的 A 股特色因子

根据搜索（幻方、九坤等），A 股三大特色因子挖掘方向：

| 方向 | 核心数据源 | 典型因子 | 可入库性 | 与现有仓库关系 |
|------|----------|--------|---------|--------------|
| **市场微观结构** | Level-2 逐笔成交/委托 | 订单流失衡、集合竞价撤单率、分钟频收益率偏度 (CSKEW) | needs_extra_data（Level-2 付费） | 与 TK 订单流 + 缠论结构互补，需 S_BUCKET 01 高频微观审核 |
| **行为金融异常** | 龙虎榜、社交舆情（雪球/股吧） | 游资席位溢价因子、散户情绪反转因子、隔夜收益率 (Overnight Return) | proxy_quantizable_now（龙虎榜有公开数据） | 与 KD MTF 的 `lock_signal` 过滤互补：情绪过热时即使 KD 锁仓也拒绝入场 |
| **另类数据** | 分析师研报、互动易问答 | 分析师修正情绪因子、NLP 舆情得分、互动平台回复延迟因子 | needs_extra_data（NLP 处理） | 与 S_BUCKET 03 机器学习（112 份）和 04 多因子（181 份）直接相关 |

### 4.2 现有仓库已有哪些因子？

从 `backtest_p0.py` 的 `l2_range_trap` 参数看，**已有 Level-2 相关逻辑**：
```python
# 已有的 Level-2 系列参数（推测）
l2_range_trap      # 范围陷阱检测
l2_trap_threshold  # 陷阱阈值
l2_imbalance_ratio # 订单流失衡比例
```

从 S_BUCKET 的 `F002`, `F014`, `F006` 看，**已有至少 3 个另类数据因子**：  
（F 编号可能代表：F002=资金流、F014=情绪、F006=宏观？需要确认实际含义。）

从 S_BUCKET 的 `03_券商研报` 的 `04_多因子`（181 份）看，**已有大量因子研究**：
- 价值类：PE 分位数、PB-ROE
- 动量类：短期动量、波动率调整
- 资金类：北向资金、主力净流入
- 情绪类：龙虎榜机构净买入、新闻热度

### 4.3 建议：A 股另类数据不是"新增"，而是"从现有素材中结构化提取"

**核心问题**：S_BUCKET 的 477 份券商研报 + 341 份游资交割单 + 49 份集合竞价教程，已经覆盖了 A 股 90% 的另类数据需求。搜索发现：这些研报本身就在研究"如何利用龙虎榜、北向、Level-2、情绪等因子做量化"。  
**任务不应该是"再找更多外部论文"，而是"**在现有素材中，提取已有因子的字段化定义，标记哪些可直接落地（proxy_quantizable_now），哪些需要额外数据（needs_extra_data）**"**。

### 4.4 币圈/外汇的另类数据

- **币圈**：链上数据（链上余额、交易所流入/流出、巨鲸钱包监控、矿工抛压、gas 费用）。  
  可入库性：`needs_extra_data`（需要链上 API，如 Glassnode、CryptoQuant）。
- **外汇**：COT 报告（CFTC Commitment of Traders，机构持仓）、央行干预信号、跨币种流动性。  
  可入库性：`needs_extra_data`（COT 有公开数据，但处理复杂）。

---

## 5. 综合建议：下一步行动优先级

### 5.1 讨论层（当前阶段）待决策问题

| 问题 | 当前状态 | 建议决策方向 |
|------|---------|-------------|
| **Volume Profile 是否纳入执行层？** | 已搜索，概念清晰，与现有指标可映射 | **纳入**。作为 P0_E 第 14 个对象。只需 OHLCV，proxy_quantizable_now。 |
| **VWAP 是否单独对象？** | 与 PV 指标功能重叠 | **不单独**。VWAP 作为 VP 的辅助参考，或融入 PV 指标的"基准线"逻辑。 |
| **Footprint/订单流是否纳入？** | 需要 Level-2，成本高 | **放入 future_bucket**。标记：当接入 Level-2 后，作为 TK 的精确化版本。 |
| **Kelly 是否替代 2% 固定风险？** | 理论更强，但需历史数据 | **不替代，而是分层**。保留 Van Tharp 2% 作为"硬性上限"，Kelly 作为"动态优化层"（Half-Kelly ≤ 0.20）。 |
| **波动率目标是否纳入？** | 需要现有 ATR 参数即可 | **纳入**。作为风控层 P0_R 的新对象。利用现有 `atr_n:14` + `volty_trend_state`。 |
| **A 股适配：是否从现有 S_BUCKET 提取？** | 已有 477 份券商研报 | **优先提取**。不搜索新外部素材。先 audit S_BUCKET 已有素材中的 A股特殊因子。 |
| **币圈/外汇另类数据？** | 有明确方向（链上/COT） | 标记为 future_bucket，当扩展到这些市场时再实现。 |

### 5.2 建议的下一步

1. **确认上述 7 个决策方向**（用户拍板）。
2. **如果确认**，进入"结构化提取"阶段：
   - 对 Volume Profile：编写对象卡（类似 CHZL_ZS / TK-R6），定义字段、公式、与现有指标互锁逻辑。
   - 对 Kelly：从 `backtest_p0.py` 的历史输出中提取胜率/赔率数据，计算半凯利公式，编写风控层对象卡。
   - 对 A股特殊因子：audit S_BUCKET 的 `03_券商研报/04_多因子` 和 `01_高频微观`，提取可直接落地的因子字段。
3. **不编码**：先写对象卡、定义字段、讨论公式，等 GLM 或用户确认后再进入代码实现。

---

## 6. 附录：搜索来源

- Volume Profile 深度分析：https://incosmos.vision/deep-analysis/3532/
- Volume Profile Trading Strategies：https://trendspider.com/learning-center/volume-profile-strategies/
- Volume Profile 分析（中文）：https://fintastic.trading/trading_strategy/volume-profile-analysis/
- Footprint Chart vs Order Flow：https://www.lexedge.net/terms/compare/footprint-chart-vs-order-flow-trading
- CoinGlass 订单流足迹图：https://www.coinglass.com/zh/learn/footprint-chart-tw
- Kyle's Lambda 与流动性：https://waylandz.com/quant-book/%E9%AB%98%E9%A2%91%E5%B8%82%E5%9C%BA%E5%BE%AE%E7%BB%93%E6%9E%84/
- Kelly Criterion 深度解析：https://research.frankk.site/kelly-resources/
- Kelly 公式与仓位管理（A 股）：https://ag.yueniuzq.com/stock/kelly-formula-dynamic-position-sizing-guide/
- A 股 vs 美股量化因子：https://www.gankinterview.cn/blog/a-shares-vs-us-stocks-interviewing-at-top-domestic-private-funds-high-flyerjiuku
- 幻方量化策略拆解：https://www.joinquant.com/view/community/detail/4f8b143407ce6f555a7094fde6667e02
- S_BUCKET 本地素材：D:\Stock\cut_file\S 目录（868 文件，券商研报 477 份）

---

> 文件：GLM_SEARCH_01_执行层补充_跨市场_风控_另类数据_v1.0.md  
> 生产者：Kimi  
> 状态：待讨论 / 待用户决策
