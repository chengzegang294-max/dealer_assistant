# GLM 搜索任务指令（可复制给 GLM）

## 任务目标

请帮我搜索并补充更多知名交易系统的"功能层组件"，按统一格式输出。我已经完成了一部分（见下方"已覆盖体系"），请你补充：
- 你没有搜过的、我没有覆盖的体系
- 同一个交易者的不同体系（如 ICT 的多个模型）
- 学术/半学术级别的量化策略
- 中文交易社区有影响力的体系

## 输出格式（必须严格遵守）

每个体系按以下格式输出：

```markdown
### [编号] [体系名] — [创始人/来源]

| 维度 | 内容 |
|------|------|
| **体系名** | [名称] |
| **结构层** | [用什么判断趋势/方向/状态，200字以内] |
| **能量层** | [用什么过滤波动/确认信号，200字以内] |
| **执行层** | [用什么触发入场，200字以内] |
| **风控层** | [用什么止损/仓位/极端状态过滤，200字以内] |
| **适合市场** | [股票/外汇/期货/加密货币/多资产] |
| **时间框架** | [日线/4H/1H/日内/月线等] |
| **成熟度** | [学术级/半学术级/社区级/工具级] |
| **核心参考来源** | [书名/论文名/YouTube频道/博客，附URL] |
```

## 已覆盖体系（请跳过这些，不要再搜）

1. **ICT (Inner Circle Trader)** — Michael J. Huddleston
2. **Adam Grimes** — The Art and Science of Technical Analysis
3. **Andreas Clenow** — Following the Trend
4. **Rob Hoffman** — Hoffman System Indicator
5. **Al Brooks** — Price Action Trading (Trends/Ranges/Reversals)
6. **Lance Beggs (YTC)** — YTC Price Action Trader
7. **Mentfx** — Liquidity + Structure
8. **Meb Faber** — GTAA / Ivy Portfolio / Trend Following
9. **Kris Verma** — Statistical Edge + Kelly Criterion
10. **Jim Dalton** — Market Profile / Auction Market Theory
11. **Multiple Time Frame Trading** — 通用方法论

## 建议搜索方向（至少覆盖这些，也可补充更多）

### 方向 A：价格行为/订单流深化
- **Mark Douglas** — Trading in the Zone（交易心理，但影响体系设计）
- **Peter Steidlmayer** — Market Profile 原始开发者（Jim Dalton 之前）
- **J. Peter Steidlmayer** — Capital Flow 概念
- **Richard Wyckoff** — Wyckoff Method（机构吸筹/派发的原始框架）
- **Tom Williams** — Volume Spread Analysis (VSA)
- **Noel Aranas** — Order Flow / Footprint Chart 体系

### 方向 B：量化/系统化策略
- **Turtle Trading** — Richard Dennis & William Eckhardt
- **Dual Momentum** — Gary Antonacci
- **Relative Strength Momentum** — Jegadeesh & Titman (学术)
- **Factor Investing** — Fama-French 多因子
- **AQR** — Cliff Asness 的 Value/Momentum 组合
- **Renaissance Technologies** — Medallion Fund 的公开方法论（如有）
- **Kaufman Adaptive Moving Average (KAMA)** — Perry Kaufman
- **Daryl Guppy** — Multiple Moving Average (GMMA)
- **Larry Williams** — %R + 季节性交易
- **Linda Raschke** — 日内动量策略

### 方向 C：波段/趋势中文体系
- **缠论** — 缠中说禅（中文独特体系，级别/中枢/背驰）
- **道氏理论** — Charles Dow（经典但仍有价值）
- **艾略特波浪** — Elliott Wave（Ralph Elliott）
- **江恩理论** — W.D. Gann（时间周期/几何角度）
- **海龟交易法则** — 中文社区大量实现
- **冯柳** — 高毅资产（逆向投资/弱者体系，中文知名）
- **徐翔** — 涨停敢死队（超短模式，但可提取结构特征）
- **asking/炒股养家** — 游资心法（情绪周期/题材轮动）

### 方向 D：风控/仓位管理专门体系
- **Van Tharp** — Position Sizing / R-Multiple
- **Ralph Vince** — Optimal f / Kelly Criterion 变体
- **Ed Seykota** — Trend Following + 交易心理学
- **Bill Eckhardt** — Turtle 风控体系
- **Nassim Taleb** — Black Swan / Antifragile（对尾部风险的处理）

### 方向 E：日内/高频微观结构
- **Larry Harris** — Trading and Exchanges（你已有 F2 CUTPACK）
- **Ananth Madhavan** — Market Microstructure（学术）
- **Pine Script 社区策略** — TradingView 高排名策略（如 London Breakout, NY Reversal）
- **Sam Seiden** — Supply and Demand 交易（与 Order Block 类似）
- **Steve Mauro** — Beat the Market Maker（BTMM）

## 搜索注意事项

1. **优先英文源**：YouTube、博客、论文、书籍
2. **中文源可选**：如果某个体系在中文社区影响力大（如缠论、游资心法），也请包含
3. **不要只给概念**：每个维度必须能说出**具体方法**（如"用 ATR"比"用波动率"更具体）
4. **成熟度要诚实**：如果某个体系只有 YouTube 视频没有书/论文，标"社区级"；如果有书有回测，标"半学术级"；如果有论文被引用，标"学术级"
5. **来源要附 URL**：如果找到具体文章/视频/论文，请附 URL

## 输出要求

- 至少补充 **10 个新体系**
- 按功能层拆解，不要只写"这是趋势跟踪体系"
- 如果某个体系在某层没有明确方法，写"未明确"或"主观判断"
- 最后附一段**总结**：这些新体系与我已有的指标（KD MTF、Volty、PV Corr、RSJ、XBreaking）有什么互补关系

---

## 一句话记忆

> 不是"介绍这个体系"，而是"这个体系在结构层用什么、能量层用什么、执行层用什么、风控层用什么"。
