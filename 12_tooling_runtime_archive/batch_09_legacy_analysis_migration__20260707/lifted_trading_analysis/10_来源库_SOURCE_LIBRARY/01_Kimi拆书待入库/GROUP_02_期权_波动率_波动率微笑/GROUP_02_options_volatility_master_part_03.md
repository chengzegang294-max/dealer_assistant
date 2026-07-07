# GROUP 02: 期权 + 波动率 + 波动率微笑 — Part 03
## 5) 冲突与裁决建议

> 不同书的定义冲突点 + "建议采用的仓库口径" + 理由

---

### 冲突 1: 对冲波动率选择 — 实际波动率 vs 隐含波动率

- **冲突描述**:
  - **Sinclair（第2章）** 主张按实际波动率（Realized Volatility）对冲："若用真实波动率对冲，PnL终值确定，等于理论定价差 V(σ_R) - V(Σ)，路径中波动仅来自离散化"
  - **Derman（第5章）** 与 **Hull（第19章）** 偏向按隐含波动率（Implied Volatility）对冲："按IV对冲时，PnL路径无随机项（无dZ），每日PnL可确定性地由 Gamma × (RV² - IV²) 解释"
  - **实务界分歧**：卖方通常按IV对冲（与客户成交价就是IV），买方通常关注RV（判断IV是否便宜）

- **建议采用的仓库口径**:
  - **采用"双轨制"**：
    1. **运行时用IV对冲**（仓库默认）：因为交易以IV成交，按IV对冲使PnL归因简单（每日PnL = 市场IV变动产生的Vega PnL + Gamma/Theta权衡）
    2. **策略评估时计算RV对冲PnL**：作为"真实盈利能力"的参考，判断策略实质价值
  - **理由**：
    1. IV对冲的PnL路径可解释性强，适合风险管理和归因
    2. 但IV对冲的终值不确定，需RV对冲视角评估策略期望收益
    3. 双轨并行可同时满足风控透明度和策略评估需求
  - **实现**：两个PnL字段：
    - `pnl_iv_hedge`：按IV对冲的日度PnL（用于风控）
    - `pnl_rv_theoretical`：按RV对冲的理论PnL（用于策略评估）

- **引用**：Sinclair 第2章; Derman 第5章 (p.112-116); Hull 第19章

---

### 冲突 2: Delta 定义 — BSM Delta vs Smile-Adjusted Delta

- **冲突描述**:
  - **Hull（第19章）** 使用标准BSM Delta：`Δ = e^(-qT) × N(d₁)` — 忽略波动率微笑
  - **Derman（第2章）** 与 **Sinclair（第2章）** 提出Smile-Adjusted Delta：
    - `Δ_adj = Δ_BSM + Vanna × skew`
    - 即考虑IV随价格变动的调整项（Sticky-Strike vs Sticky-Delta不同假设下调整不同）
  - **冲突核心**：在微笑市场中，标的价格移动时IV也会移动（尤其是沿skew滑动），BSM delta低估了ATM期权的实际delta

- **建议采用的仓库口径**:
  - **P0字段使用BSM Delta**（仓库默认），但增加**Smile-Adjustment指示器**
  - **理由**：
    1. BSM Delta是行业通用标准，跨系统可比
    2. Smile-Adjustment计算依赖Skew模型假设（Sticky-Strike / Sticky-Delta / Sticky-Moneyness），不同假设结果不同
    3. 在skew极端环境（如危机期）启用Smile-Adjustment作为override
  - **实现**：
    - `delta_bsm`：标准BSM delta（P0字段）
    - `delta_smile_adj`：Smile调整后的delta（P1字段，极端环境下参考）
    - `skew_regime`：当前skew状态标记（normal/stressed/extreme），stressed以上启用delta_smile_adj

- **引用**：Hull 第19章 (p.424-425); Derman 第2章 (p.36-39); Sinclair 第2章

---

### 冲突 3: 波动率风险溢价（VRP）的解释与交易

- **冲突描述**:
  - **Sinclair（第1章）** 与 **Derman（p.155）** 确认VRP存在："IV系统性地高于RV，这是期权卖方的风险补偿"
  - **Hull（第19章）** 从风险厌恶角度解释："负偏态（crashophobia）使虚值看跌期权定价高，推升整体IV"
  - **分歧点1**：VRP是否可以被"套利"？Sinclair警告VRP不是free lunch — 卖出volatility的尾部风险极大（如2018年2月VIX飙升）
  - **分歧点2**：VRP的度量口径。不同文献使用不同RV计算方式（close-to-close vs Parkinson vs Yang-Zhang），得到的VRP数值不同

- **建议采用的仓库口径**:
  - **VRP作为P1诊断字段**，不进入P0交易信号
  - **VRP计算采用Yang-Zhang RV**作为标准
  - **理由**：
    1. YZ RV无漂移假设、综合隔夜和日内信息，是最稳健的RV度量
    2. VRP仅表示统计上的溢价存在，不构成交易信号（需结合skew、term structure综合判断）
    3. 设置VRP监控预警：当VRP < 0（IV < RV）时标记为`vol_premium_inverted`，提示卖出volatility策略风险升高
  - **实现**：
    ```python
    vrp = iv_30d - rv_yz_20d  # 30天IV vs 20天YZ RV
    vrp_percentile = percentile(vrp, lookback=252)  # 52周百分位
    signal = 'sell_vol' if vrp_percentile > 80 else 'neutral' if vrp_percentile > 20 else 'caution'
    ```

- **引用**：Sinclair 第1章; Derman p.155; Hull 第19章

---

### 冲突 4: Theta 符号约定

- **冲突描述**:
  - **Hull（第19章）** Theta通常报负数（表示时间流逝导致价值减少）
  - **部分交易系统** Theta报正数（表示"每日衰减的绝对值"）
  - **Sinclair（第2章）** 使用 `Θ = ∂V/∂t`（偏导定义，通常为负），但在PnL分解中写为 `PnL_Theta = Θ × δt`

- **建议采用的仓库口径**:
  - **Theta统一报负数**（遵循Hull学术规范和大部分卖方系统惯例）
  - **新增字段`theta_daily_decay`** = abs(Θ) / 365（便于直观理解"每天衰减多少"）
  - **理由**：
    1. 负Theta与偏微分方程的数学约定一致（∂V/∂t）
    2. 防止跨系统对接时的符号混乱
    3. `theta_daily_decay`给交易员直观的每日损耗数字

- **引用**：Hull 第19章 (p.427-428); Sinclair 第2章

---

### 冲突 5: 离散股息处理 — 连续q vs Escrowed模型

- **冲突描述**:
  - **Hull（第15.3节）** 对小额股息使用连续股息率q：`C = S₀e^(-qT)N(d₁) - Ke^(-rT)N(d₂)`
  - **Derman（第1章）** 与实务界对大额离散股息使用Escrowed模型：
    - `S₀' = S₀ - PV(Dividends)`（标的价格减去股息现值）
    - 用S₀'代入BSM公式（设q=0）
  - **冲突**：连续q模型隐含"股息连续均匀支付"假设，与大多数股票的季度/半年度离散股息现实不符

- **建议采用的仓库口径**:
  - **分场景处理**：
    1. **指数期权**（股息分散）：使用连续q（从指数点计算隐含dividend yield）
    2. **个股期权**（离散大额股息）：使用Escrowed模型（扣除PV(Dividends)）
    3. **外汇期权**：连续q = foreign risk-free rate（Hull 第17章）
  - **理由**：
    1. 指数的股息近似连续，误差可接受
    2. 个股的离散股息（尤其高额特别股息）对深度实值期权定价影响显著
    3. 外汇期权的q即 foreign rate，是模型原生设定
  - **实现**：
    - 字段`dividend_model`：continuous / escrowed / discrete_tree
    - 大额股息（>S×2%）自动切换escrowed模型并发出alert

- **引用**：Hull 第15.3节; Derman 第1章; Hull 第17章（外汇期权）

---

### 冲突 6: 美式期权定价 — BSM外推 vs 数值方法

- **冲突描述**:
  - **Hull（第15.12节）** 指出：美式看涨在r>q时不应提前行权，但高股息股票上可能最优提前行权；美式看跌始终有提前行权可能
  - **Derman（第3章）** 在讨论PnL归因时主要使用欧式框架，因美式期权的非线性行权边界使PnL分解复杂化
  - **McMillan（第5章）** 大量讨论美式期权的早期行权条件和调整

- **建议采用的仓库口径**:
  - **定价层**：美式期权用二叉树/PIDE数值方法定价（Hull 第13/21章）
  - **Greeks层**：用BSM Greeks作为近似（仓库默认），但标注`american_adjustment_needed`标志
  - **理由**：
    1. 二叉树计算成本高，不适合高频Greeks更新
    2. 对大多数轻度虚值/平值期权，提前行权溢价很小，BSM近似足够
    3. 深度实值时（尤其是put）启用数值方法override
  - **触发条件**：
    ```python
    if option_type == 'american_call' and div_yield > risk_free_rate * 0.5:
        use_bin_tree = True
    if option_type == 'american_put' and moneyness < 0.85:
        use_bin_tree = True
    ```

- **引用**：Hull 第13章, 第15.12节, 第21章; Derman 第3章; McMillan 第5章

---

### 冲突 7: 波动率模型选择 — 局部波动率 vs 随机波动率

- **冲突描述**:
  - **Derman（第10章）** 局部波动率（Dupire）完美拟合市场微笑、无套利，但"forward volatility的动态与真实市场不符"（forward smile过于平坦）
  - **Sinclair（第3章）** Heston随机波动率产生自然的偏态和均值回归，但参数校准复杂，且无法完美拟合短期深虚值微笑
  - **Hull（第27章）** 讨论混合模型（SVJ、SVCJ），但指出参数过多导致过拟合风险

- **建议采用的仓库口径**:
  - **分层使用**：
    | 场景 | 推荐模型 | 理由 |
    |------|---------|------|
    | 香草期权定价+Greeks | BSM + IV曲面插值 | 简单、快速、市场一致 |
    | 障碍/亚式/回望等奇异期权 | 局部波动率（Dupire） | 无套利、完美拟合 |
    | 波动率衍生品（VIX期权等） | Heston/Bates | 需要正确的vol动态 |
    | 短期OTM峰解释 | Merton Jump-Diffusion | 跳跃解释微笑峰 |
    | 综合交易台 | BSM + SVI曲面 + Heston备用 | 快速+灵活+深度 |
  - **理由**：
    1. 不同模型有不同优势领域，不存在"最佳通用模型"
    2. 仓库应支持多模型并行，按产品类型路由
    3. BSM + IV曲面是运行时的黄金标准（简单、透明、市场一致）

- **引用**：Derman 第10章; Sinclair 第3章; Hull 第27章

---

### 冲突 8: 已实现波动率计算 — 哪种方法为标准

- **冲突描述**:
  - **Sinclair（第1章）** 推荐Yang-Zhang："综合考虑了隔夜跳空和日内波动，无漂移假设"
  - **Hull（第15.4节）** 主要使用close-to-close："简单、数据需求最低"
  - **Derman（第3章）** 讨论Parkinson和Garman-Klass的效率增益

- **建议采用的仓库口径**:
  - **标准RV使用Yang-Zhang**
  - **同时保留close-to-close RV用于长期历史对比**
  - **理由**：
    1. YZ效率最高（约为CC的8倍），且无漂移偏差
    2. CC RV是行业标准，便于与历史数据和外部系统对比
    3. 两者差异可指示"隔夜信息占比"（YZ >> CC时说明隔夜跳空主导）
  - **实现**：
    - `rv_yang_zhang_20d`：P0字段（标准RV）
    - `rv_close_20d`：P1字段（历史对比）
    - `overnight_ratio` = 1 - (CC RV)²/(YZ RV)²（隔夜信息占比，diag字段）

- **引用**：Sinclair 第1章; Hull 第15.4节; Derman 第3章

---

## 6) YAML 索引卡

```yaml
group_id: GROUP_02
theme: 期权 + 波动率 + 波动率微笑
source_books:
  - id: Hull_2018
    title: "期权、期货及其他衍生产品（原书第11版）"
    author: John C. Hull
    lang: zh-CN (translated)
    key_chapters: >
      第10章(期权市场机制), 第11章(股票期权性质), 第12章(期权交易策略),
      第13章(二叉树模型), 第15章(BSM模型), 第19章(Greeks/波动率度量),
      第21章(数值方法), 第27章(波动率微笑/奇异期权)
    page_range_note: "全书约900页，核心章节10-27 (p.340-700)"
    
  - id: McMillan_2012
    title: "期权投资策略（原书第5版）"
    author: Lawrence G. McMillan
    lang: zh-CN (translated)
    key_chapters: >
      第2章(期权基础), 第3章(价差策略), 第4章(组合策略),
      第5章(高级策略/波动率交易), 第6章(风险管理/止损)
    page_range_note: "全书约700页，核心策略章节2-6 (p.50-500)"
    
  - id: Sinclair_2013
    title: "波动率交易：期权量化交易员指南（原书第2版）"
    author: Euan Sinclair
    lang: zh-CN (translated)
    key_chapters: >
      第1章(波动率基础/RV计算), 第2章(风险管理/Greeks/PnL归因),
      第3章(波动率曲面/模型校准), 第4章(方向性策略/Straddle/Strangle),
      第5章(高级策略/Calendar/Condor)
    page_range_note: "全书约300页，全部为核心内容"
    
  - id: Derman_Miller_2016
    title: "波动率微笑：宽客大师教你建模"
    author: Emanuel Derman, Michael B. Miller
    lang: zh-CN (translated)
    key_chapters: >
      第1-3章(BSM回顾/Greegs/HedgingPnL),
      第4章(离散Hedging效应), 第5章(Hedging策略选择),
      第6章(交易成本/Leland), 第7章(做市/Hedging),
      第8章(波动率微笑描述), 第9章(跳跃扩散/局部波动率),
      第10章(模型综述/校准), 第11章(隐含分布), 第12章(静态复制)
    page_range_note: "全书约350页，全部为核心内容，第1-8章尤为精华"

worth_re_reading:
  - book: Derman_Miller_2016
    chapters: [1, 2, 3, 5, 7, 8]
    reason: >
      Greeks精确推导、Hedging PnL归因框架、Smile描述方法（delta表示法）、
      交易成本对定价的影响。这些是波动率交易实务的理论基石。
      
  - book: Sinclair_2013
    chapters: [1, 2, 3]
    reason: >
      波动率度量方法对比（YZ vs CC vs GK vs Parkinson）、
      Greeks管理/Risk Budgeting/PnL归因、曲面参数化（SVI/SSVI）。
      直接对应可落地字段定义。
      
  - book: Hull_2018
    chapters: [12, 13, 15, 19, 27]
    reason: >
      策略构造与盈亏分析、二叉树数值方法、BSM定价、
      Greeks完整公式、波动率微笑与曲面建模。
      行业标准参考书。
      
  - book: McMillan_2012
    chapters: [3, 4, 5]
    reason: >
      策略调整规则、止损方法、事件驱动交易。
      补充Sinclair/Hull中策略执行层面的细节。

tags:
  - options_pricing
  - volatility
  - hedging
  - pnl_attribution
  - black_scholes
  - greeks
  - implied_volatility
  - realized_volatility
  - volatility_surface
  - svi_parameterization
  - heston_model
  - local_volatility
  - jump_diffusion
  - variance_risk_premium
  - straddle
  - strangle
  - iron_condor
  - calendar_spread
  - butterfly
  - risk_reversal
  - covered_call
  - smile_skew
  - term_structure
  - delta_hedging
  - gamma_scalping
  - vega_trading
  - theta_harvesting
  - pin_risk
  - american_option
  - discrete_dividend
  - transaction_cost

key_formula_count: 17
formula_categories:
  bsm_pricing: [FORMULA-01, FORMULA-02, FORMULA-03]
  greeks: [FORMULA-04, FORMULA-05, FORMULA-06, FORMULA-07, FORMULA-08]
  hedging_pnl: [FORMULA-09, FORMULA-10, FORMULA-11]
  surface_param: [FORMULA-12, FORMULA-13]
  realized_vol: [FORMULA-14, FORMULA-15, FORMULA-16, FORMULA-17]

strategy_templates:
  - Long Straddle
  - Short Straddle
  - Long Strangle
  - Bull Call Spread
  - Bear Put Spread
  - Short Iron Condor
  - Calendar Spread
  - Covered Call
  - Risk Reversal
  - Butterfly Spread

conflict_resolutions:
  - 对冲波动率选择: 双轨制(IV对冲运行, RV对冲评估)
  - Delta定义: BSM Delta(P0) + Smile-Adjusted(P1_override)
  - VRP交易: P1诊断字段, 不进入P0信号
  - Theta符号: 统一负数 + daily_decay辅助字段
  - 股息处理: 指数用continuous_q, 个股用escrowed
  - 美式期权: BSM近似(P0) + bin_tree_override(深度实值)
  - 模型选择: 分层路由(BSM+SVI标准, Dupile/Heston按场景)
  - RV计算: Yang-Zhang标准 + Close-Close历史对比

conflict_count: 8
formula_count: 17
strategy_count: 10
model_families:
  - BSM_Baseline
  - Local_Volatility_Dupire
  - Stochastic_Volatility_Heston
  - Jump_Diffusion_Merton
  - Mixed_Affine_Bates
  - SVI_Surface

data_requirements_summary:
  Level_1: [标的价格, ATM_IV, 期限结构]
  Level_2: [完整微笑(多行权价IV), Greeks]
  Tick: [逐笔期权成交, 标的价格]
  Historical: [标的OHLC(计算RV), 无风险利率, 股息日历]
  Model_Calibration: [SVI参数, Heston参数, 局部波动率曲面]

output_files:
  - GROUP_02_options_volatility_master_part_01.md  # 总框架 + 公式表
  - GROUP_02_options_volatility_master_part_02.md  # 策略模板库 + 波动率建模
  - GROUP_02_options_volatility_master_part_03.md  # 冲突裁决 + YAML索引卡
```

---

> 最终输出必须是 Markdown 正文，可直接保存为 .md 文件。
> 本组内容已按主题合并四本书，未按单本书拆分为多篇读书笔记。
> Kimi 提出了 17 个公式条目（含变量定义/使用条件/常见误区/页码引用）、
> 10 个策略模板（含入场条件/调整规则/风险上限/数据需求）、
> 5 个波动率建模方法（含适用场景/限制条件/校准伪代码）、
> 8 项冲突裁决建议。
> **最终字段冻结、落盘、脚本实现由仓库方完成。**
