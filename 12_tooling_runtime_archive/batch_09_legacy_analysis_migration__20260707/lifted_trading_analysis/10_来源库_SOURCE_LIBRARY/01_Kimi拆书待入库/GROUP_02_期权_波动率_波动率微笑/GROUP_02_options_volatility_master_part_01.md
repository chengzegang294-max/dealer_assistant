# GROUP 02: 期权 + 波动率 + 波动率微笑 — 合并来源库扩展包

> 来源书籍：
> - Hull《期权、期货及其他衍生产品（原书第11版）》(Hull, 2018)
> - McMillan《期权投资策略（原书第5版）》(McMillan, 2012)
> - Sinclair《波动率交易：期权量化交易员指南（原书第2版）》(Sinclair, 2013)
> - Derman & Miller《波动率微笑：宽客大师教你建模》(Derman & Miller, 2016)

> 处理原则：按主题组合并四本书，不按单本书拆分。候选字段量化定义由 Kimi 提出草案，最终字段冻结、落盘、脚本实现由仓库方完成。

---

## 1) 本组总框架：IV/RV、波动率曲面、定价/对冲、PnL归因 的全景图

### 1.1 分层大纲

#### 第一层：波动率基础（Implied vs Realized）

**1.1.1 隐含波动率（IV）**
- **定义**：使BSM模型计算出的期权价格等于市场价格的波动率参数
- **来源**：Hull 第15章; Derman 第8章; Sinclair 第1-2章
- **核心属性**：
  - IV是市场对未来波动率的"预期"+风险溢价（Derman p.155: "隐含波动率通常高于实际波动率，由市场摩擦、对冲成本、未来波动率不确定性导致"）
  - IV是BSM模型下的"错误模型的正确参数"——即使BSM假设不成立，IV作为报价惯例仍具实用价值
  - IV具有多个维度：不同行权价（微笑）、不同期限（期限结构）、不同标的（曲面）

**1.1.2 已实现波动率（RV / Realized Volatility）**
- **定义**：标的资产在过往某段时间内实际表现出的价格波动程度
- **常见度量方法**：
  - 收盘价-收盘价（close-to-close）：`RV = sqrt(252 × Σ r_i²)`，其中`r_i = ln(S_i/S_{i-1})`
  - Parkinson极差（high-low）：利用日内最高最低价，`σ² = (1/4Tln2) × Σ (ln(H_i/L_i))²` — Parkinson (1980)
  - Garman-Klass综合：融合open/high/low/close四价，`σ² = (1/T) × Σ [0.5(ln(H/L))² - (2ln2-1)(ln(C/O))²]`
  - Yang-Zhang综合：融合overnight gap和intraday波动
- **来源**：Sinclair 第1章; Hull 第15.4节

**1.1.3 IV-RV 关系（波动率风险溢价 VRP）**
- **核心发现**：IV > RV 是普遍现象（指数期权尤为显著）
  - S&P 500: VIX（IV）通常比后续实现波动率高2-5个波动率点
  - VRP来源：负偏态风险溢价、离散对冲成本、跳跃风险、需求压力
- **交易含义**：系统性地卖出波动率（如卖出straddle）在统计上具有正期望收益，但尾部风险极大
- **来源**：Derman p.155; Sinclair 第1章; Hull 第19章

#### 第二层：波动率曲面（Volatility Surface）

**1.2.1 波动率微笑（Moneyness维度）**
- **定义**：同一到期日下，不同行权价（或delta）对应的隐含波动率曲线
- **典型形态**：
  - 股票指数：负偏态（左高右低），虚值看跌IV显著高于虚值看涨（Derman 第8章）
  - 个股：近似对称微笑
  - 外汇：近似对称"真微笑"或轻微偏态
- **标准表示方法**：横轴用 delta 而非行权价（Derman p.156: delta标准化使不同期限、不同标的有可比性）

**1.2.2 波动率期限结构（Term Structure）**
- **定义**：同一行权价（通常ATM）下，不同到期日对应的IV
- **典型形态**：
  - 正常市场：向上倾斜（长期IV > 短期IV）
  - 危机期：向下倾斜（短期IV飙升）
  - Samuelson效应：短期波动率变动更剧烈

**1.2.3 波动率曲面 = 微笑 × 期限结构**
- **完整表示**：Σ(S, t, K, T) — 标的价、时间、行权价、到期日四元函数
- **建模核心矛盾**：BSM假设常数波动率，但市场观察到的是完整曲面 → 需用更复杂模型
- **来源**：Derman 第8-10章; Hull 第27章

#### 第三层：定价模型族

**1.3.1 BSM基准（Hull 第15章; Derman 第1-3章）**
- Black-Scholes-Merton (1973) 闭式解
- 假设：几何布朗运动、常数波动率、无交易费用、连续对冲、无套利
- 局限：微笑/偏态/期限结构均无法解释

**1.3.2 局部波动率模型（Local Volatility）**
- **核心**：σ(S,t) 为标的价和时间的确定性函数
- **代表**：Dupire (1994) 公式 — 从市场曲面反推局部波动率
- **Derman-Kani  implied tree**：离散化的局部波动率实现
- **优点**：完美拟合市场微笑，无套利保证
- **缺点**：波动率动态与真实市场不一致（forward volatility过于平坦）
- **来源**：Derman 第10章; Hull 第27.1节

**1.3.3 随机波动率模型（Stochastic Volatility）**
- **核心**：波动率本身为随机过程
- **代表**：Heston (1993) 模型
  - `dS = μS dt + sqrt(V) S dW₁`
  - `dV = κ(θ-V)dt + ξ sqrt(V) dW₂`
  - `corr(dW₁, dW₂) = ρ`（杠杆效应，ρ < 0）
- **优点**：产生自然偏态，均值回归，与实证吻合
- **缺点**：需数值方法（傅里叶变换），参数校准复杂
- **来源**：Derman 第10章; Hull 第27.2节; Sinclair 第3章

**1.3.4 跳跃-扩散模型（Jump-Diffusion）**
- **核心**：在扩散过程上叠加跳跃
- **代表**：Merton (1976) 模型 — Poisson跳跃 + 对数正态跳跃幅度
- **优点**：解释微笑"峰"（短期深虚值IV极高）
- **缺点**： hedging不完全可能（跳跃不可对冲），参数多
- **来源**：Derman 第10章; Hull 第27.3节

**1.3.5 混合模型（Affine Models）**
- Bates (1996): Heston + 跳跃
- SVJ, SVCJ：更复杂的跳跃-随机波动率组合
- **实用地位**：奇异期权定价的行业标准
- **来源**：Sinclair 第3章

#### 第四层：对冲与PnL归因

**1.4.1 Greeks框架**
- Delta (Δ)：价格一阶敏感度 → 方向对冲
- Gamma (Γ)：价格二阶敏感度 → 凸性/再平衡收益
- Vega (V)：IV敏感度 → 波动率敞口
- Theta (Θ)：时间衰减 → 每日时间损耗
- Rho (ρ)：利率敏感度
- Vanna (∂Delta/∂Vol)：波动率滑移敏感度
- Volga (∂Vega/∂Vol)：Vega凸性
- **来源**：Hull 第19章; Derman 第1-3章; Sinclair 第2章

**1.4.2 PnL归因（Daily P&L Explain / PnL Decomposition）**

标准PnL分解（Derman 第3章; Sinclair 第2章）：

```
Daily P&L = Δ × dS        (Delta PnL)
          + 0.5 × Γ × (dS)²  (Gamma PnL / 凸性收益)
          + V × dΣ           (Vega PnL)
          + Θ × dt           (Theta PnL / 时间衰减)
          + ρ × dr           (Rho PnL)
          + CrossTerms       (Vanna, Volga, etc.)
          + Residual         (未解释部分 → 模型误差/市场摩擦)
```

**关键定理**：在连续对冲、常数波动率假设下，若用IV对冲：

```
Theta + 0.5 × Γ × S² × Σ² = 0   (BSM偏微分方程)
```

这意味着 Gamma PnL + Theta PnL = 0（在完美条件下），交易员的实际收益来自**RV > IV**或**RV < IV**。

**1.4.3 对冲方式选择**
- **连续对冲（理论）**：瞬时无风险，需要BSM delta
- **离散对冲（实际）**：产生对冲误差，误差标准差 ∝ 1/sqrt(N)，N为再平衡次数
- **按实际波动率对冲**：PnL终值确定 = V(σ_R) - V(Σ)，但路径中随机波动
- **按隐含波动率对冲**：PnL路径确定（无dZ项），但终值不确定
- **来源**：Derman 第5-6章; Sinclair 第2章

#### 第五层：交易成本与实务调整

**1.5.1 有效波动率（Leland 1985; Derman 第7章）**
- 考虑交易成本比例k、再平衡间隔dt：
  - 多头：`σ_eff = σ × sqrt(1 - sqrt(8/π) × (k/(σ×sqrt(dt))))`
  - 空头：`σ_eff = σ × sqrt(1 + sqrt(8/π) × (k/(σ×sqrt(dt))))`
- **含义**：多头期权价值因交易成本被压缩，空头价值膨胀

**1.5.2 最优对冲频率**
- 对冲频率↑ → 跟踪误差↓ 但交易成本↑
- 存在最优再平衡阈值（如delta变化超过某个阈值时调整，而非定时调整）
- **来源**：Derman 第7章; Sinclair 第2章

---

## 2) 统一公式表

> 每条公式：变量定义 + 使用条件 + 常见误区 +（书名+页码）

### 2.1 Black-Scholes-Merton 核心定价公式

#### FORMULA-01: 欧式看涨期权 BSM 闭式解

```
C = S₀ × N(d₁) × e^(-qT) - K × N(d₂) × e^(-rT)

其中：
d₁ = [ln(S₀/K) + (r - q + σ²/2) × T] / (σ × sqrt(T))
d₂ = d₁ - σ × sqrt(T)
```

- **变量定义**：
  - `S₀`：标的资产当前价格
  - `K`：行权价
  - `T`：距到期年化时间
  - `r`：无风险利率（连续复利）
  - `q`：股息率（连续复利，外汇期权中为 foreign rate）
  - `σ`：波动率（年化）
  - `N(·)`：标准正态累积分布函数

- **使用条件**：
  - 欧式期权（不可提前行权）
  - 标的服从几何布朗运动
  - 波动率和利率在期限内恒定
  - 无交易成本和税收
  - 标的可连续交易/对冲

- **常见误区**：
  - 误用于美式期权（尤其是高股息股票上的看涨期权可能提前行权）
  - 使用错误的年化转换（交易日252 vs 日历日365）
  - 波动率输入使用历史波动率而非隐含波动率（定价时应使用IV）
  - 股息处理：连续q vs 离散股息（大额离散股息需用 escrowed 模型或调整S₀）

- **来源**：Hull 第15章 (p.330-335); Derman 第1章 (p.3-8)

---

#### FORMULA-02: 欧式看跌期权 BSM 闭式解

```
P = K × N(-d₂) × e^(-rT) - S₀ × N(-d₁) × e^(-qT)
```

- **变量定义**：同 FORMULA-01

- **使用条件**：同 FORMULA-01

- **常见误区**：
  - 与看涨公式混淆符号（N(-d₁) 而非 N(d₁)）
  - 美式看跌期权可能提前行权（深度实值时），BSM低估其价值

- **来源**：Hull 第15章 (p.335); Derman 第1章

---

#### FORMULA-03: Put-Call Parity（看跌-看涨平价）

```
C - P = S₀ × e^(-qT) - K × e^(-rT)    (欧式)
```

- **变量定义**：同 FORMULA-01

- **使用条件**：
  - 仅对欧式期权严格成立
  - 美式期权有不等式边界：`S₀ - K ≤ C - P ≤ S₀ - K × e^(-rT)`

- **常见误区**：
  - 对美式期权直接用等式会导致套利机会误判
  - 忽略股息调整（q项）

- **交易应用**：
  - 合成多头：`C - P + K × e^(-rT) ≈ S₀`（合成股票多头）
  - 反转套利（Reversal）：`+C -P -S`（当C-P > S-Ke^(-rT)时）
  - 转换套利（Conversion）：`-C +P +S`（当C-P < S-Ke^(-rT)时）

- **来源**：Hull 第11章 (p.387-389); Derman 第3章

---

### 2.2 Greeks 公式表

#### FORMULA-04: Delta (Δ)

**欧式看涨**：
```
Δ_call = e^(-qT) × N(d₁)
```

**欧式看跌**：
```
Δ_put = e^(-qT) × [N(d₁) - 1] = -e^(-qT) × N(-d₁)
```

- **变量定义**：同 FORMULA-01
- **含义**：标的价变动1单位，期权价格变动Δ单位
- **取值范围**：Call ∈ (0, 1)；Put ∈ (-1, 0)
- **ATM近似**：当S≈K且q=0时，Δ_call ≈ 0.5 + 0.2×σ×sqrt(T)（Derman p.163）
- **常见误区**：
  - 用BSM delta对冲微笑市场时产生偏差（需加入 smile 调整项：∂Σ/∂S）
  - 忽略股息（q）对远期和delta的压缩
- **来源**：Hull 第19章 (p.424-425); Derman 第1章; Sinclair 第2章

---

#### FORMULA-05: Gamma (Γ)

```
Γ = e^(-qT) × N'(d₁) / (S₀ × σ × sqrt(T))

其中 N'(x) = (1/sqrt(2π)) × e^(-x²/2)  (标准正态PDF)
```

- **含义**：标的价变动1单位，delta变动Γ单位
- **关键性质**：
  - Call和Put的Gamma相同
  - ATM期权Gamma最大，深度实值/虚值趋近于0
  - Gamma ∝ 1/σ（低波动率环境Gamma更大）
  - Gamma ∝ 1/sqrt(T)（临近到期Gamma激增）
- **常见误区**：
  - 临近到期的Gamma爆炸需特别关注（Pin risk）
  - 低IV环境下Gamma更大，需更频繁再平衡
- **来源**：Hull 第19章 (p.426); Derman 第1章; Sinclair 第2章

---

#### FORMULA-06: Vega (V)

```
V = S₀ × e^(-qT) × N'(d₁) × sqrt(T)
```

- **含义**：IV变动1个百分点（0.01），期权价格变动V单位
- **关键性质**：
  - Call和Put的Vega相同
  - ATM期权Vega最大（近似 `Vega ≈ S₀ × sqrt(T/(2π))`）
  - Vega ∝ sqrt(T)（长期期权对IV更敏感）
- **常见误区**：
  - 单位混淆：Vega通常以"每1% IV变动"报价，但代码中可能用"每1单位"（需乘以0.01）
  - Vega是线性近似，大IV变动时需考虑Volga
- **来源**：Hull 第19章 (p.427); Derman 第1章; Sinclair 第2章

---

#### FORMULA-07: Theta (Θ)

**欧式看涨**：
```
Θ_call = -S₀ × e^(-qT) × N'(d₁) × σ / (2×sqrt(T)) 
         + q × S₀ × N(d₁) × e^(-qT) 
         - r × K × e^(-rT) × N(d₂)
```

**欧式看跌**：
```
Θ_put = -S₀ × e^(-qT) × N'(d₁) × σ / (2×sqrt(T)) 
        - q × S₀ × N(-d₁) × e^(-qT) 
        + r × K × e^(-rT) × N(-d₂)
```

- **含义**：时间流逝1天（年化1/365），期权价值衰减量
- **关键性质**：
  - Theta通常为负（期权是消耗性资产）
  - ATM期权Theta最大（绝对值）
  - 临近到期Theta加速衰减
  - Theta + 0.5×Γ×S²×σ² = r×Π（组合时间价值衰减）
- **常见误区**：
  - 符号约定：Theta通常报负数，但有的系统报正数表示"每日衰减的绝对值"
  - 周末效应：期权市场在周末不交易但Theta仍衰减
- **来源**：Hull 第19章 (p.427-428); Derman 第1章

---

#### FORMULA-08: Vanna 与 Volga

```
Vanna = ∂Δ/∂σ = ∂V/∂S = -e^(-qT) × N'(d₁) × d₂ / σ
Volga = ∂V/∂σ = V × d₁ × d₂ / σ
```

- **Vanna含义**：IV变动对Delta的影响（或标的价格变动对Vega的影响）
  - ATM时Vanna≈0（d₁≈0时Vanna变号）
  - 决定skew exposure：Vanna大意味着delta对IV移动敏感
  
- **Volga含义**：Vega对IV的敏感度（Vega凸性）
  - ATM时Volga为负（d₁×d₂ < 0）
  - 决定vol-of-vol exposure

- **应用**：奇异期权定价（Vanna-Volga方法）
  ```
  Price = BSM + p_Skew × Vanna + p_Smile × Volga
  ```

- **来源**：Derman 第2章; Sinclair 第3章

---

### 2.3 对冲与 PnL 分解公式

#### FORMULA-09: 离散对冲 PnL 分解（Derman框架）

```
PnL(t, t+δt) = Δ × δS                 (Delta PnL)
              + 0.5 × Γ × (δS)²        (Gamma/Convexity PnL)
              + V × δΣ                 (Vega PnL)
              + Θ × δt                 (Theta PnL)
              + O((δS)³, (δΣ)²)        (高阶项)
```

- **使用条件**：
  - 期权组合按BSM Greeks计量
  - 短期内（δt较小）的PnL归因
  - 适用于任何 Greeks-based 风险管理系统

- **关键定理 — Gamma-Theta权衡**：
  ```
  E[Gamma PnL] + Theta PnL ≈ 0.5 × Γ × S² × (RV² - IV²) × δt
  ```
  当 RV = IV 时，期望PnL为零；RV > IV 时多头Gamma获利。

- **来源**：Derman 第3章 (p.49-52); Sinclair 第2章

---

#### FORMULA-10: 按隐含波动率对冲的瞬时 PnL

```
dPnL = 0.5 × Γ × S² × (σ_R² - Σ²) × dt + V × dΣ + Slippage
```

- **含义**：
  - 若按隐含波动率Σ对冲，且实际波动率为σ_R：
    - σ_R > Σ → 多头Gamma策略盈利（Gamma Scalping）
    - σ_R < Σ → 空头Gamma策略盈利（Theta Harvesting）
  - IV变动产生Vega PnL
  - 离散对冲产生Slippage（对冲误差）

- **来源**：Derman 第5章 (p.112-116); Sinclair 第2章

---

#### FORMULA-11: 对冲误差（离散再平衡）

```
σ_HE ≈ σ × sqrt(π/4N) × PortfolioValue

或更精确：
σ_HE ≈ sqrt(π/8) × V × σ / sqrt(N)    (N次再平衡的标准差)
```

- **含义**：
  - 对冲误差标准差 ∝ 1/sqrt(N)
  - 对冲频率增加4倍 → 误差减半
  - 使用实际波动率对冲时，误差仅来自离散化
  - 使用错误波动率对冲时，误差额外增加系统性偏差

- **来源**：Derman 第6章 (p.130-136)

---

### 2.4 波动率曲面参数化

#### FORMULA-12: SVI 参数化（Stochastic Volatility Inspired）

```
σ²_BS(k) = a + b × [ρ × (k - m) + sqrt((k - m)² + σ²_J)]

其中：
k = ln(K/F)    (log-moneyness，F为远期价格)
a, b, ρ, m, σ_J 为5个参数
```

- **参数含义**：
  - `a`：整体水平（整体IV²）
  - `b`：曲率/展开程度
  - `ρ`：偏态（ρ < 0 为负偏态，对应股票指数）
  - `m`：平移（ATM位置）
  - `σ_J`：曲率控制（微笑"开口"大小）

- **约束条件**（无套利）：
  - b ≥ 0, σ_J > 0
  - a + b×σ_J×sqrt(1-ρ²) ≥ 0
  - 需验证日历套利和蝶式套利条件

- **来源**：Gatheral (2004); Sinclair 第3章; Derman 第8章

---

#### FORMULA-13: Heston 模型特征函数

```
φ(u) = exp(A(u,T) + B(u,T) × V₀ + iu × ln(S₀))

其中：
A(u,T) = r×u×i×T + (κ×θ/ξ²) × [(κ-ρξui-d)×T - 2×ln((1-g×e^(-dT))/(1-g))]
B(u,T) = (κ-ρξui-d)/(ξ²) × (1-e^(-dT))/(1-g×e^(-dT))
d = sqrt((ρξui-κ)² + ξ²×(ui+u²))
g = (κ-ρξui-d)/(κ-ρξui+d)
```

- **参数含义**：
  - `V₀`：当前瞬时方差
  - `κ`：方差均值回归速度
  - `θ`：长期方差均值
  - `ξ`：波动率的波动率（vol of vol）
  - `ρ`：价格-方差相关系数（通常<0）

- **使用条件**：
  - Feller条件：2κθ > ξ² 保证方差不触及0
  - 需用傅里叶逆变换或Cosine方法数值积分求期权价格

- **来源**：Heston (1993); Sinclair 第3章; Derman 第10章

---

### 2.5 已实现波动率计算

#### FORMULA-14: Close-to-Close 实现波动率

```
RV_cc = sqrt(252 × Σᵢ₌₁ᴺ (ln(Sᵢ/Sᵢ₋₁))²)
```

- **使用条件**：日度数据，N个交易日
- **偏差**：忽略隔夜跳空、日内信息
- **来源**：Sinclair 第1章; Hull 第15.4节

---

#### FORMULA-15: Parkinson 实现波动率

```
RV_pk = sqrt(252/(4×N×ln2) × Σᵢ₌₁ᴺ (ln(Hᵢ/Lᵢ))²)
```

- **变量**：Hᵢ=日高, Lᵢ=日低
- **优点**：利用日内信息，效率约为close-to-close的5倍
- **偏差**：连续取样假设下高估（约+10%），低采样时偏差更大
- **来源**：Parkinson (1980); Sinclair 第1章

---

#### FORMULA-16: Garman-Klass 实现波动率

```
RV_gk = sqrt(252/N × Σᵢ₌₁ᴺ [0.5×(ln(Hᵢ/Lᵢ))² - (2ln2-1)×(ln(Cᵢ/Oᵢ))²])
```

- **变量**：Oᵢ=开盘价, Cᵢ=收盘价
- **优点**：效率最高（约为close-to-close的8倍）
- **缺点**：对开盘价误差敏感
- **来源**：Garman & Klass (1980); Sinclair 第1章

---

#### FORMULA-17: Yang-Zhang 实现波动率

```
RV_yz = sqrt(252 × (σₒ² + k×σ_c² + (1-k)×σ_rs²))

其中：
σₒ² = 1/(N-1) × Σ(ln(Oᵢ/Cᵢ₋₁) - μₒ)²    (overnight)
σ_c² = 1/(N-1) × Σ(ln(Cᵢ/Oᵢ) - μ_c)²      (open-to-close)
σ_rs² = 1/N × Σ[(ln(Hᵢ/Cᵢ)×ln(Hᵢ/Oᵢ) + ln(Lᵢ/Cᵢ)×ln(Lᵢ/Oᵢ))]  (Rogers-Satchell)
k = 0.34 / (1.34 + (N+1)/(N-1))
```

- **优点**：无漂移假设，综合隔夜和日内信息
- **推荐**：作为标准实现波动率度量
- **来源**：Yang & Zhang (2000); Sinclair 第1章

---

*（第一部分结束，第二部分将继续：3) 策略模板库 + 4) 波动率建模条目）*
