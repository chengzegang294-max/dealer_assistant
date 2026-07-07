# GROUP_05 最小吸收包 v1

更新时间：2026-06-21

## 本次只解决什么

- 把 `GROUP_05_趋势_系统交易` 从“大型方法论书稿集合”收成当前仓库可直接承接的最小吸收层。
- 本轮只产出四件事：
  - 最小状态模板
  - 最小风险规则
  - 最小禁止跑偏规则
  - 仓库映射草案
- 本轮不做：
  - 直接落新字段
  - 直接改回测与策略逻辑
  - 直接把 tick / DOM / 期货展期依赖强塞进当前仓库

## 进入条件

- 已有统一模板文件：
  - `GROUP_05_trend_system_trading_STATE_TEMPLATE.md`
  - `GROUP_05_trend_systematic_trading.md`
- 已有切片正式入口：
  - `01_F1_cutpack_v2_final\README_放这里.md`
- 已有跨组首批吸收清单：
  - `..\GROUP_05_GROUP_06_首批可吸收清单_v1.md`

## 退出条件

- 写清楚首批只吸收哪些状态语言和护栏。
- 写清楚哪些内容先停在解释层，不进入字段或门控。
- 写清楚它与现有仓库 `N01/N02/N03`、研究护栏、来源整理模板的关系。

## 最小状态模板

| 模板块 | 最小内容 | 当前角色 | 当前备注 |
|---|---|---|---|
| `Structure` | `Trend Existence` `Breakout Validity` `Market Cycle Phase` `Volatility Regime` | `DIAG_ONLY_CANDIDATE` | 当前最适合进入状态解释层 |
| `Bias` | `MA Bias` `Momentum Bias` `Crowd Extremity` | `DIAG_ONLY_CANDIDATE` | 更像心理/方向偏置解释，不应直接门控 |
| `Friction` | `Transaction Cost Load` `Liquidity Adequacy` `Rollover Feasibility` | `RESEARCH_GUARDRAIL_CANDIDATE` | 当前用于研究可交易性检查 |
| `Risk` | `Position Size Safety` `Drawdown Controllability` | `RESEARCH_GUARDRAIL_CANDIDATE` | 当前用于风险边界与承受度审计 |

## 最小风险规则

### Step 1：先看市场是不是“值得谈趋势”

- 先判 `Trend Existence`
- 再判 `Breakout Validity`
- 如果两者都不成立：
  - 停在解释层，不继续往趋势策略语言上抬

### Step 2：再看当前环境是否允许放大头寸

- 判 `Volatility Regime`
- 判 `Transaction Cost Load`
- 判 `Liquidity Adequacy`
- 如果波动、成本、流动性三者任一失真：
  - 只保留研究结论，不推进策略建议

### Step 3：最后才谈头寸与衰落

- 判 `Position Size Safety`
- 判 `Drawdown Controllability`
- 当前只接受“先给风控边界，再谈收益预期”

## 最小禁止跑偏规则

- 不把书稿里的主观叙事直接当字段。
- 不把 tick 图、70-tick、OCO、期货展期假设直接映射到当前 A 股或标准 OHLC 仓库。
- 不把 `Tipping Point` 之类主观退出语言直接抬成硬执行规则。
- 不把 `Wyckoff / Volman / 海龟 / 趋势书稿` 的异质规则混成一个新策略。
- 先保留为：
  - 状态模板
  - 研究护栏
  - 风险检查表
- 再决定是否进入任何字段合同或门控层。

## 仓库映射草案

| GROUP_05 内容 | 仓库去向 | 当前层级 | 说明 |
|---|---|---|---|
| `Trend Existence` | `N01/N03` 上位状态解释层 | `DIAG_ONLY_CANDIDATE` | 作为趋势存在性语言，不直接替代现有字段 |
| `Breakout Validity` | `N03` 结构/突破解释层 | `DIAG_ONLY_CANDIDATE` | 更适合做突破质量解释 |
| `Market Cycle Phase` | 周期/阶段语言壳 | `CONDITIONAL_KEEP_CANDIDATE` | 适合研究模板，不宜先字段化 |
| `Volatility Regime` | 风险与环境检查表 | `RESEARCH_GUARDRAIL_CANDIDATE` | 可做 regime 说明，但不默认门控 |
| `Friction` 三项 | 研究护栏 | `RESEARCH_GUARDRAIL_CANDIDATE` | 用于回测与现实可交易性差异审计 |
| `Risk` 两项 | 风险检查表 | `RESEARCH_GUARDRAIL_CANDIDATE` | 用于 size / dd 上限语言 |
| 四轴模板整体 | 拆书统一吸收壳 | `ABSORBED_TEMPLATE` | 先服务来源整理，不直接服务执行层 |

## 当前冻结区

- `70-tick` 图专属 setup 细则：当前不实现。
- `10 pip / 10 pip OCO` 固定止盈止损：当前不迁入仓库。
- `Rollover Feasibility` 的期货合约细节：当前只保留成护栏语言。
- `Trader Effect Density` / COT / CTA AUM：当前超出主线数据依赖。
- `Tipping Point` 主观退出法：当前不字段化。

## 当前结论

- `GROUP_05` 已从“可重开”推进到“最小吸收包已成形”。
- 当前最稳顺序已经固定：
  - 先四轴状态模板
  - 再风险与摩擦护栏
  - 最后才考虑是否有任何对象值得继续下沉
- 本轮完成后，`GROUP_05` 的角色应表述为：
  - `上位状态语言层 + 研究护栏层 + 来源整理模板层`
