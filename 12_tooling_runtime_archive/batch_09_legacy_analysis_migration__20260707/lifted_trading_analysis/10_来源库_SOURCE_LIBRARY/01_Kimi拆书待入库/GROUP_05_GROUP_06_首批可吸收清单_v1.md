# GROUP_05 + GROUP_06 首批可吸收清单 v1

## 目的

- 把 `01_Kimi拆书待入库` 中最贴近当前仓库的两组材料，先从“待入库”推进到“可吸收清单”。
- 当前只做：
  - 通用对象
  - 状态模板
  - 禁止跑偏规则
  - 仓库映射
- 当前不做：
  - 直接落字段
  - 直接改 CSV 合约
  - 直接开新策略实现

## 当前选择这两组的原因

- `GROUP_05_趋势_系统交易`
  - 已有 `STATE_TEMPLATE` 风格，和当前仓库的状态模板语言最接近。
- `GROUP_06_Auction_MarketProfile_价格行为`
  - 已有统一对象定义与最小可实现定义，和 `N02 / 结构标签 / 价格行为对象化` 最接近。

## GROUP_05 可吸收项

### A1. 四轴状态模板

- 来源：
  - `GROUP_05_trend_system_trading_STATE_TEMPLATE.md`
- 当前可吸收内容：
  - `结构轴 / 偏置轴 / 摩擦轴 / 风险轴`
- 仓库价值：
  - 可作为跨来源书稿的统一整理壳
  - 让后续“方法论书稿”不再只是长文摘要，而有固定结构
- 当前角色：
  - `已吸收到整理模板候选`

### A2. 趋势存在性 / 突破有效性 / 市场周期 / 波动率状态

- 来源：
  - `GROUP_05_trend_system_trading_STATE_TEMPLATE.md`
  - `GROUP_05_trend_systematic_trading.md`
- 当前可吸收内容：
  - `Trend Existence`
  - `Breakout Validity`
  - `Market Cycle Phase`
  - `Volatility Regime`
- 仓库价值：
  - 可作为 `N01/N03` 之外的上位状态语言
  - 更适合放进“状态模板/解释层/研究 checklist”
- 当前角色：
  - `可重开（模板级，不是字段级）`

### A3. 摩擦轴与风险轴

- 来源：
  - `GROUP_05_trend_system_trading_STATE_TEMPLATE.md`
- 当前可吸收内容：
  - `Transaction Cost Load`
  - `Liquidity Adequacy`
  - `Rollover Feasibility`
- 仓库价值：
  - 可补当前研究口径里较弱的执行摩擦与可交易性检查
  - 适合先进入通用研究护栏
- 当前角色：
  - `可重开（研究护栏候选）`

### A4. 禁止跑偏规则

- 当前可吸收内容：
  - 先定义状态/证据/证伪，再谈策略有效性
  - 不把书稿里的主观叙述直接当字段
  - 先保留为模板/解释层，再决定是否进入硬门控
- 仓库价值：
  - 和当前 `全量吃透 -> 四分流 -> 1-2 个重开项` 的流程一致
- 当前角色：
  - `已吸收到方法护栏`

## GROUP_06 可吸收项

### B1. 统一对象定义

- 来源：
  - `GROUP_06_market_profile_price_action_DEFINITIONS.md`
  - `GROUP_06_market_profile_price_action.md`
- 当前可吸收内容：
  - `TPO`
  - `Initial Balance`
  - `Value Area`
  - `POC`
  - `Balance vs Imbalance`
  - `Day Type`
- 仓库价值：
  - 对 `N02` 与后续结构定义层最有帮助
  - 适合先做“对象定义库”，不是立即做全实现
- 当前角色：
  - `可重开（对象定义层）`

### B2. 价格行为最小可实现定义

- 来源：
  - `GROUP_06_market_profile_price_action.md`
- 当前可吸收内容：
  - `Trend Bar / Doji`
  - `Signal Bar`
  - 上下文敏感判定
- 仓库价值：
  - 对 `N03` 的结构/信号定义很有帮助
  - 但当前应停在定义层，不要提前把 Brooks 语言硬量化成主线字段
- 当前角色：
  - `future bucket（定义保留，暂不首批实现）`

### B3. N02 对接价值

- 当前可吸收内容：
  - `Initial Balance`
  - `Value Area`
  - `Balance/Imbalance`
  - `Day Type`
- 仓库价值：
  - 可作为 `N02` 后续从 OR 扩展到 IB / auction context 的自然上游来源
- 当前角色：
  - `可重开（N02 后续候选）`

## 当前四分流

### 已吸收

- 四轴状态模板作为整理壳
- 统一对象定义作为对象库壳
- “先定义/证据/证伪，再决定是否实现”的方法护栏

### 可重开

- `G56-R1`：四轴状态模板正式并入书稿吸收流程
- `G56-R2`：Auction / Market Profile 对象定义库（先 `IB / VA / POC / Day Type`）

### future bucket

- Brooks 价格行为信号条目做字段化
- TPO 全量精细实现（需要更细数据与更多工程时间）

### 仅来源库保留

- 书中大量案例叙事
- 纯主观解盘语言
- 页码与估计页码仍需回原书复核的部分

## 建议顺序

- 先做 `G56-R1`：
  - 把四轴状态模板固化成后续拆书统一吸收壳
- 再做 `G56-R2`：
  - 先只吸收 `IB / VA / POC / Day Type` 的对象定义
- 暂不做：
  - 直接编码
  - 直接主线落字段
  - 直接策略化
