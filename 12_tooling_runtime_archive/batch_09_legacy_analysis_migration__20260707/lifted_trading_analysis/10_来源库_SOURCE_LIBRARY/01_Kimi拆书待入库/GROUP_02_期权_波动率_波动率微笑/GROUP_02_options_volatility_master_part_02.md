# GROUP 02: 期权 + 波动率 + 波动率微笑 — Part 02
## 3) 策略模板库

> 每个策略：入场条件（可判定）/ 调整规则（delta/vega/gamma 目标）/ 风险上限与止损口径 / 数据需求 /（书名+页码）

### 3.1 Long Straddle（买入跨式）

| 维度 | 内容 |
|------|------|
| **构造** | 同时买入同一标的、同一到期日、同一行权价的 ATM 看涨 + ATM 看跌 |
| **入场条件** | (a) IV_Rank < 30%（IV处于历史低位）; (b) 预期即将发生大幅价格变动（事件驱动）; (c) 期限结构Contango显著（远期IV > 近期IV时回避） |
| **Greeks目标** | Delta ≈ 0（中性）; Gamma > 0; Vega > 0; Theta < 0 |
| **调整规则** | (a) Delta偏离±0.1时，用标的股票对冲至中性; (b) 临近到期7天时评估Gamma风险，考虑部分平仓; (c) 事件兑现后立即平仓（避免Theta侵蚀） |
| **风险上限** | 最大损失 = 权利金总计; 止损：当Theta每日侵蚀 > 权利金的5%且3日内无波动时减仓50% |
| **盈利场景** | RV > IV 或价格大幅突破盈亏平衡点（S > K + total_premium 或 S < K - total_premium） |
| **数据需求** | 标的价格、ATM IV、IV_Rank(52周)、IV_TermStructure、Gamma、Theta |
| **来源** | Hull 第12章 (p.427-428); Sinclair 第4章; McMillan 第5章 |

---

### 3.2 Short Straddle（卖出跨式）

| 维度 | 内容 |
|------|------|
| **构造** | 同时卖出同一标的、同一到期日、同一行权价的 ATM 看涨 + ATM 看跌 |
| **入场条件** | (a) IV_Rank > 70%（IV处于历史高位）; (b) 预期标的将窄幅波动; (c) Skew处于正常范围（异常Skew意味着尾部风险定价不足） |
| **Greeks目标** | Delta ≈ 0; Gamma < 0; Vega < 0; Theta > 0 |
| **调整规则** | (a) 严格Delta中性，Delta偏离±0.05即对冲; (b) 标的价格突破盈亏平衡点50%时启动Gamma止损（买入OTM wings对冲）; (c) 临近到期Gamma激增时逐步减仓 |
| **风险上限** | 理论损失无上限; 硬性止损：单日亏损 > 收取权利金的30%时全部平仓; 或设置buy-stop在盈亏平衡点的1.5倍处 |
| **盈利场景** | RV < IV 且价格维持在[K-premium, K+premium]区间内 |
| **数据需求** | 标的价格、ATM IV、IV_Rank、历史RV(20日)、Gamma、Theta、VaR(组合) |
| **来源** | Hull 第12章; Sinclair 第4章; McMillan 第5章 |

---

### 3.3 Long Strangle（买入异价跨式）

| 维度 | 内容 |
|------|------|
| **构造** | 买入OTM看跌（较低行权价K₁）+ 买入OTM看涨（较高行权价K₂），K₁ < S < K₂ |
| **入场条件** | (a) IV_Rank < 30%; (b) 预期大幅波动但方向不确定; (c) 权利金成本比Straddle低（OTM价格更低） |
| **Greeks目标** | Delta ≈ 0（K₁和K₂delta大致抵消）; Gamma > 0（较弱于Straddle）; Vega > 0; Theta < 0（较弱） |
| **调整规则** | (a) Delta偏离±0.15时对冲（Strangle天然Delta偏移较大，阈值放宽）; (b) 标的价格接近K₁或K₂时评估是否转换为Directional策略 |
| **风险上限** | 最大损失 = 权利金总计; 止损同Straddle |
| **盈利场景** | 价格突破K₂+premium 或 跌破K₁-premium |
| **数据需求** | 同Straddle |
| **来源** | Hull 第12章 (p.430-431); McMillan 第5章 |

---

### 3.4 Bull Call Spread（牛市看涨价差）

| 维度 | 内容 |
|------|------|
| **构造** | 买入较低行权价K₁看涨 + 卖出较高行权价K₂看涨（K₁ < K₂） |
| **入场条件** | (a) 看涨标的但涨幅有限; (b) 降低买入ATM看涨的成本; (c) 期限斜率正常（不远期升水异常） |
| **Greeks目标** | Delta > 0; Gamma 符号取决于S位置（S≈K₁时Gamma>0，S≈K₂时Gamma<0）; Vega ≈ 0（近似Vega中性）; Theta ≈ 0 |
| **调整规则** | (a) 价格突破K₂时考虑将卖出腿向上roll（锁定利润）; (b) 价格跌破K₁-10%时止损; (c) 临近到期S≈K₂时关注Pin Risk |
| **风险上限** | 最大损失 = K₁期权价格 - K₂期权收入 = 净权利金支出; 止损：亏损达到净支出的50% |
| **盈利场景** | S_T > K₁ + net_premium; 最大盈利 = K₂ - K₁ - net_premium |
| **数据需求** | 标的价格、不同行权价IV（smile数据）、净权利金、Breakeven |
| **来源** | Hull 第12章 (p.415-417); McMillan 第3章; Sinclair 第5章 |

---

### 3.5 Bear Put Spread（熊市看跌价差）

| 维度 | 内容 |
|------|------|
| **构造** | 买入较高行权价K₂看跌 + 卖出较低行权价K₁看跌（K₁ < K₂） |
| **入场条件** | (a) 看跌标的但跌幅有限; (b) Put Skew极端负值时买入OTM put更贵，此策略可部分对冲Skew成本 |
| **Greeks目标** | Delta < 0; 其余同Bull Spread |
| **调整规则** | 对称于Bull Call Spread |
| **风险上限** | 最大损失 = 净权利金支出 |
| **盈利场景** | S_T < K₂ - net_premium; 最大盈利 = K₂ - K₁ - net_premium |
| **数据需求** | 同Bull Spread |
| **来源** | Hull 第12章 (p.417-418); McMillan 第3章 |

---

### 3.6 Short Iron Condor（卖出铁鹰）

| 维度 | 内容 |
|------|------|
| **构造** | 卖出Put Spread(K₁/K₂) + 卖出Call Spread(K₃/K₄)，K₁<K₂<K₃<K₄，且K₂、K₃为近ATM |
| **入场条件** | (a) IV_Rank > 50%; (b) 预期标的在[K₂, K₃]区间盘整; (c) 距离到期至少30天（留有Theta衰减空间）; (d) 盈亏比 > 1:2（收取权利金:最大风险） |
| **Greeks目标** | Delta ≈ 0; Gamma < 0; Vega < 0; Theta > 0（主要收益来源） |
| **调整规则** | (a) Delta偏离±0.1时对冲; (b) 价格突破K₂或K₃时，将受威胁的一侧向内roll（如价格↑突破K₃，将Call Spread向上平移）; (c) 临近到期7天强制减仓50% |
| **风险上限** | 最大风险 = (K₂-K₁) - net_credit 或 (K₄-K₃) - net_credit（取较大值）; 硬性止损：净亏损 > 最大风险的50%时全部平仓 |
| **盈利场景** | S_T ∈ [K₂, K₃] 区间 |
| **数据需求** | 标的价格、4个行权价IV、IV_Rank、IV_Percentile、各腿Greeks、组合Greeks |
| **来源** | McMillan 第4章; Sinclair 第4章 |

---

### 3.7 Calendar Spread（日历价差 / 时间价差）

| 维度 | 内容 |
|------|------|
| **构造** | 卖出近月ATM期权 + 买入远月ATM同类型期权（行权价相同） |
| **入场条件** | (a) 期限结构陡峭（近月IV显著高于远月IV，即Backwardation）; (b) 预期标的短期内窄幅波动但长期有方向; (c) 事件（如财报）将在近月到期后出现 |
| **Greeks目标** | 近月到期时：Delta ≈ 0; Gamma < 0（近月Gamma主导）; Vega > 0（远月Vega主导）; Theta > 0（近月Theta更大） |
| **调整规则** | (a) 近月到期前7天评估是否提前平仓（避免Pin Risk）; (b) 近月到期后保留远月腿并可选择添加方向性leg; (c) 标的大幅偏离行权价时，考虑将远月腿向新ATM roll |
| **风险上限** | 最大损失 = 净权利金支出（因远月期权价格 > 近月）; 止损：亏损 = 净支出的50% |
| **盈利场景** | 近月到期时S ≈ K（近月期权价值归零，远月仍保留时间价值） |
| **数据需求** | 标的价格、近月/远月ATM IV、期限结构斜率、各腿Greeks |
| **来源** | Hull 第12章 (p.424); Sinclair 第5章; McMillan 第4章 |

---

### 3.8 Covered Call（备兑看涨 / 备兑写）

| 维度 | 内容 |
|------|------|
| **构造** | 持有标的股票多头 + 卖出ATM/OTM看涨期权 |
| **入场条件** | (a) 持有标的并预期短期上涨空间有限; (b) IV处于高位（Call premium高）; (c) 目标行权价 ≥ 目标卖出价位 |
| **Greeks目标** | Delta > 0（但 < 1，因卖出call）; Gamma < 0; Vega < 0; Theta > 0 |
| **调整规则** | (a) 标的大幅上涨突破行权价时：可选择被指派交割（锁定收益）或向上roll call; (b) 标的大幅下跌时：buy back call降低下行敞口（或向下roll） |
| **风险上限** | 下行风险同持有股票（最大损失 = S₀ - call_premium）; 上行被Cap在行权价 |
| **盈利场景** | S_T ≤ K + call_premium; 最大盈利 = K - S₀ + call_premium |
| **数据需求** | 标的价格、标的持有成本、OTM/ATM Call IV、股息日期（除息前可能提前行权） |
| **来源** | Hull 第12章 (p.413); McMillan 第2章 |

---

### 3.9 Risk Reversal（风险逆转）

| 维度 | 内容 |
|------|------|
| **构造** | 卖出OTM看跌（Delta ≈ -0.25）+ 买入OTM看涨（Delta ≈ +0.25），净权利金 ≈ 0 |
| **入场条件** | (a) 强烈看涨且认为下行风险有限; (b) Call Skew相对Put Skew异常便宜（25-delta risk reversal报价为负值时利好）; (c) 合成Forward价格与现货差异显著 |
| **Greeks目标** | Delta > 0（约+0.5）; Gamma ≈ 0（近似）; Vega ≈ 0（近似）; Theta ≈ 0（近似） |
| **调整规则** | (a) 价格如期上涨后可卖出更高行权价的Call形成Spread锁定利润; (b) 价格反向跌破Put行权价时评估是否止损或转换为 naked put |
| **风险上限** | 下行风险理论上至S→0; 止损：S < Put行权价 × 0.9时全部平仓 |
| **盈利场景** | 价格上涨（与持有股票方向一致，但几乎零成本） |
| **数据需求** | 标的价格、25-delta Call/Put IV、Risk Reversal报价、Skew度量 |
| **来源** | Sinclair 第4章; McMillan 第3章; Derman 第8章 |

---

### 3.10 Butterfly Spread（蝶式价差）

| 维度 | 内容 |
|------|------|
| **构造** | 买入低行权价K₁ + 卖出2倍中间行权价K₂ + 买入高行权价K₃，K₂=(K₁+K₃)/2 |
| **入场条件** | (a) 预期价格将稳定在K₂附近; (b) 隐含波动率曲面中间行权价处"过度弯曲"（可被统计套利利用）; (c) 即将到期时Gamma风险可控 |
| **Greeks目标** | 在K₂处：Delta=0, Gamma极大正, Vega极小; 整体Vega≈0 |
| **调整规则** | (a) 此策略一旦建立极少调整（成本已锁定）; (b) 标的价格偏离K₂超过(K₃-K₁)/4时考虑止损; (c) 临近到期如S≈K₂则持有至到期获取最大收益 |
| **风险上限** | 最大损失 = 净权利金支出（有限且预先确定） |
| **盈利场景** | S_T ≈ K₂; 最大盈利 = K₂-K₁ - net_premium |
| **数据需求** | 标的价格、三个行权价IV、曲面曲率（Fly报价） |
| **来源** | Hull 第12章 (p.420-423); McMillan 第4章 |

---

### 策略模板汇总矩阵

| 策略 | 方向性 | IV看法 | 最大损失 | 最大盈利 | 主要收益来源 | 复杂度 |
|------|--------|--------|---------|---------|------------|--------|
| Long Straddle | 中性 | 做多IV | 权利金 | ∞ | Gamma Scalping | 低 |
| Short Straddle | 中性 | 做空IV | ∞ | 权利金 | Theta | 中 |
| Long Strangle | 中性 | 做多IV | 权利金 | ∞ | Gamma Scalping | 低 |
| Bull Call Spread | 看多 | 中性 | 净支出 | K₂-K₁-净支出 | 方向+IV | 低 |
| Bear Put Spread | 看空 | 中性 | 净支出 | K₂-K₁-净支出 | 方向+IV | 低 |
| Short Iron Condor | 中性 | 做空IV |  wings宽-净收入 | 净收入 | Theta | 中 |
| Calendar Spread | 中性 | 做空期限结构 | 净支出 | 有限 | Theta+Vega | 中 |
| Covered Call | 看多 | 做空IV | S₀-premium | K-S₀+premium | Theta+方向 | 低 |
| Risk Reversal | 强烈看多 | 中性 | 下行∞ | ∞ | 方向 | 低 |
| Butterfly | 中性 | 做空曲面曲率 | 净支出 | 有限 | Gamma收敛 | 中 |

---

## 4) 波动率建模条目

> 微笑/偏度/期限结构/曲面拟合方法：适用场景、限制条件、校准步骤（伪代码级）

### 4.1 波动率微笑描述方法

#### 4.1.1 Delta表示法（Derman推荐）

**方法**：以期权Delta（而非行权价）作为横轴来表示IV

```
x-axis: Δ = N(d₁)  (Call Delta ∈ (0,1) 或 Put Delta ∈ (-1,0))
y-axis: Σ(Δ)       (对应delta的IV)
```

**优点**：
- Delta标准化使不同期限、不同标的可比
- 25-delta Risk Reversal = IV(Δ=0.25 Call) - IV(Δ=-0.25 Put) → 偏态度量
- 25-delta Butterfly/Strangle = [IV(Δ=0.25) + IV(Δ=-0.25)]/2 - IV(ATM) → 曲率度量

**标准市场报价惯例**（Derman p.156-158）：
- ATM Vol（50-delta IV）
- 25-delta Risk Reversal (RR25)
- 25-delta Butterfly (BF25) 或 25-delta Strangle

**来源**：Derman 第8章 (p.155-158)

---

#### 4.1.2 Moneyness表示法

**方法**：以ln(K/F)或K/S作为横轴

```
x-axis: m = ln(K/F)  (log-moneyness)
y-axis: Σ(m, T)      (隐含波动率曲面)
```

**适用场景**：局部波动率模型（Dupire公式需要连续moneyness函数）
**局限**：不同期限的ATM位置不同，不易直观比较

**来源**：Derman 第8章; Sinclair 第3章

---

### 4.2 波动率曲面参数化方法

#### 4.2.1 SVI参数化（推荐用于外推与插值）

**适用场景**：
- 需要平滑拟合市场IV报价
- 需要外推到无报价行权价的IV
- 需要快速计算Greeks（解析导数可得）

**限制条件**：
- 仅描述单一到期日的微笑
- 需每个到期日单独拟合
- 需验证无套利条件

**校准步骤（伪代码）**：

```python
def calibrate_svi(market_strikes, market_ivs, F, T):
    """
    输入: 市场行权价列表, 市场IV列表, 远期价格, 到期时间
    输出: SVI 5参数 (a, b, ρ, m, σ_J)
    """
    # Step 1: 转换为log-moneyness
    k = [ln(K/F) for K in market_strikes]
    
    # Step 2: IV平方（SVI拟合方差）
    w = [iv**2 * T for iv in market_ivs]  # total variance
    
    # Step 3: 定义目标函数
    def objective(params):
        a, b, rho, m, sigma = params
        # 无套利约束检查
        if b < 0 or sigma <= 0:
            return 1e10
        # 蝶式套利检查
        if a + b*sigma*sqrt(1-rho**2) < 0:
            return 1e10
        
        w_model = [a + b*(rho*(ki-m) + sqrt((ki-m)**2 + sigma**2)) 
                   for ki in k]
        return sum((wi - wmi)**2 for wi, wmi in zip(w, w_model))
    
    # Step 4: 优化
    from scipy.optimize import minimize
    result = minimize(objective, x0=[0.01, 0.1, -0.5, 0, 0.1],
                      method='L-BFGS-B')
    return result.x
```

**来源**：Gatheral (2004); Sinclair 第3章

---

#### 4.2.2 SSVI（Surface SVI）参数化

**适用场景**：一次性拟合整个曲面，保证期限结构一致性

**限制条件**：
- 参数较少（每个到期日只有θ_t，全局参数ρ和η）
- 可能无法完美拟合所有到期日的微笑

**核心公式**：
```
SSVI(k, θ_t) = (θ_t/2) × (1 + ρ×φ×k + sqrt((φ×k + ρ)² + 1 - ρ²))

其中：
θ_t = ATM total variance at time t
φ = η/θ_t^α  ( η, α 为全局参数, α ∈ [0.5, 1] )
```

**校准步骤**：
1. 对每个到期日拟合ATM total variance θ_t
2. 全局优化ρ和η使所有到期日的蝶式/风险逆转误差最小
3. 验证日历套利条件：∂w/∂t ≥ 0 且 ∂²(SSVI)/∂k∂t 一致

**来源**：Gatheral & Jacquier (2014); Sinclair 第3章

---

#### 4.2.3 三次样条插值（Cubic Spline）

**适用场景**：
- 快速、精确的局部插值
- 不需要参数化外推

**限制条件**：
- 外推不稳定
- 需要足够密的行权价数据
- 可能引入蝶式套利

**校准步骤**：
```python
def calibrate_spline(market_strikes, market_ivs):
    from scipy.interpolate import CubicSpline
    # 直接拟合IV-smile（或total variance）
    cs = CubicSpline(market_strikes, market_ivs)
    
    # 必须检查：插值后无蝶式套利
    # 条件：∂²(IV²×T)/∂K² ≥ 0 （局部方差非负）
    test_strikes = np.linspace(min_K, max_K, 1000)
    for K in test_strikes:
        second_deriv = cs.derivative(2)(K)
        if second_deriv < 0 and abs(second_deriv) > tol:
            raise ValueError("蝶式套利 detected")
    return cs
```

**来源**：Hull 第27章; Sinclair 第3章

---

### 4.3 期限结构建模

#### 4.3.1 直接线性/样条插值

**方法**：对同一moneyness（通常是ATM）的不同到期日IV进行插值

```
Σ(T) = Interp({(T₁, Σ₁), (T₂, Σ₂), ...})
```

**限制**：
- 需外推到非常短期限（<1个月）时不可靠
- 危机时期期限结构形状剧变，插值可能失效

**来源**：Sinclair 第3章

---

#### 4.3.2 因子模型

**方法**：将期限结构分解为因子

```
Σ(T) = Level + Slope × f(T) + Curvature × g(T) + ε(T)
```

**因子解释**：
- Level（水平因子）：整体IV水平，对应VIX
- Slope（斜率因子）：短期vs长期，对应期限结构斜率
- Curvature（曲率因子）：中期凸性

**来源**：Sinclair 第3章; Derman 第8章

---

### 4.4 完整曲面建模流程（伪代码级）

```python
class VolatilitySurface:
    """
    完整波动率曲面建模与校准流程
    """
    
    def __init__(self, spot, forwards, discount_curve, 
                 dividend_curve, market_data):
        """
        market_data: dict[T] = list of (strike, iv, call_put_flag)
        """
        self.S = spot
        self.F = forwards  # dict[T] = forward price
        self.r = discount_curve
        self.q = dividend_curve
        self.raw = market_data
        
    def step1_clean_data(self):
        """数据清洗与标准化"""
        for T, quotes in self.raw.items():
            # 转换为统一delta表示
            for strike, iv, cp in quotes:
                F = self.F[T]
                delta = bsm_delta(self.S, strike, T, 
                                  self.r(T), self.q(T), iv, cp)
                k = log(strike / F)
                self.standardized[T].append((delta, k, iv))
    
    def step2_fit_smile_per_tenor(self):
        """对每个到期日拟合SVI微笑"""
        self.svi_params = {}
        for T in self.standardized:
            ks = [x[1] for x in self.standardized[T]]
            ivs = [x[2] for x in self.standardized[T]]
            self.svi_params[T] = calibrate_svi(ks, ivs, self.F[T], T)
    
    def step3_interpolate_term_structure(self):
        """期限结构插值（对SVI参数逐参数插值）"""
        tenors = sorted(self.svi_params.keys())
        for param in ['a', 'b', 'rho', 'm', 'sigma']:
            values = [self.svi_params[T][param] for T in tenors]
            self.param_interp[param] = CubicSpline(tenors, values)
    
    def step4_no_arbitrage_check(self):
        """无套利验证"""
        # 4a. 蝶式套利：∂²(C)/∂K² ≥ 0 → 概率密度非负
        for T in self.all_tenors:
            for K in test_strike_grid:
                price = self.price_vanilla(K, T, 'call')
                # 有限差分近似二阶导
                if butterfly_density < 0:
                    raise ValueError(f"蝶式套利: T={T}, K={K}")
        
        # 4b. 日历套利：同一K的不同T不应倒挂
        for K in test_strike_grid:
            for i in range(len(tenors)-1):
                T1, T2 = tenors[i], tenors[i+1]
                var1 = self.get_total_var(K, T1)
                var2 = self.get_total_var(K, T2)
                assert var2 >= var1, f"日历套利: K={K}, T1={T1}, T2={T2}"
    
    def get_iv(self, K, T):
        """查询任意(K,T)的IV"""
        if T in self.svi_params:
            a,b,r,m,s = self.svi_params[T]
        else:
            # 插值SVI参数
            a = self.param_interp['a'](T)
            b = self.param_interp['b'](T)
            r = self.param_interp['rho'](T)
            m = self.param_interp['m'](T)
            s = self.param_interp['sigma'](T)
        
        k = log(K / self.F[T])
        var = a + b * (r*(k-m) + sqrt((k-m)**2 + s**2))
        return sqrt(var / T)
```

---

### 4.5 模型选择决策树

```
需要拟合市场微笑？
  ├── 否 → 使用BSM + 单一IV（简单场景）
  └── 是 → 需要解释微笑动态？
            ├── 否 → 局部波动率（Dupire）— 完美拟合但错误动态
            │         └── 适用：障碍期权、奇异期权定价（需correct hedge）
            └── 是 → 需要闭式解？
                      ├── 是 → Heston + Fourier
                      │         └── 适用：快速定价、Greeks计算
                      └── 否 → 混合模型（Heston+Jump）
                                └── 适用：短期OTM微笑峰、VIX产品
```

**来源**：综合 Derman 第10章; Sinclair 第3章; Hull 第27章

---

*（第二部分结束，第三部分将继续：5) 冲突与裁决 + 6) YAML索引卡）*
