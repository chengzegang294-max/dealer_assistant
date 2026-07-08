# MTF-SEB 交易系统框架 v0.1

## 全称

**Multi-Timeframe Structure-Energy-Band Trading System**
多周期结构-能量-波段交易系统

---

## 设计声明

- 本框架**不改动**任何现有指标的字段定义、计算公式或角色定位。
- 本框架只给每个指标分配**体系角色**和**互锁条件**。
- 本框架保持以下边界不变：
  - `XBreaking` 仍保持 `NEED_PROBE / DIAG`，不升级为硬信号。
  - `PV Corr` / `RSJ` 仍保持 `DIAG_ONLY`，不直接生成交易信号。
  - `Volty` 仍保持 `RISK / EXIT / DIAG`，不单独作为入场条件。
  - `KD MTF P0` 仍是唯一可输出方向偏好的指标层。
- 本框架的"缺失"是有意设计：不存在的指标用 `NEED_PROBE` 占位，不强补。

---

## 核心思想来源

| 来源 | 核心思想 | 在本框架中的映射 |
|------|---------|----------------|
| **ICT (Inner Circle Trader)** | Market Structure + Liquidity Sweep + Kill Zone | 结构层：多周期方向判定 + 时间窗口过滤 |
| **Al Brooks** | 价格行为三书：Trend/Range/Reversal 结构 | 结构层：趋势/震荡/反转状态机 |
| **Lance Beggs (YTC)** | TST/BOF/BPB 三层框架 + 陷阱交易者 | 执行层：突破-回测-确认结构 |
| **Andreas Clenow** | 趋势跟踪 + ATR 波动率过滤 + 严格仓位管理 | 能量层：ATR 波动率状态 + 仓位缩放 |
| **Adam Grimes** | 市场结构 + 价格波动分析 | 结构层：结构有效性判定 |

---

## 五层架构

```
┌─────────────────────────────────────────────────────────────┐
│  审计层 (Audit)                                             │
│  indicator_audit → 回测归因 + 参数校准 + 绩效审查           │
├─────────────────────────────────────────────────────────────┤
│  风控层 (Risk Guard)                                        │
│  RSJ + Volty Stop Distance → 异常过滤 + 止损锚定          │
├─────────────────────────────────────────────────────────────┤
│  执行层 (Execution)                                         │
│  XBreaking → 结构突破触发（NEED_PROBE 占位）                │
├─────────────────────────────────────────────────────────────┤
│  能量层 (Energy)                                            │
│  Volty + PV Corr → 波动率状态 + 量价确认                     │
├─────────────────────────────────────────────────────────────┤
│  结构层 (Structure)                                         │
│  KD MTF P0 → 多周期方向判定 + 一致性分级                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 第一层：结构层（Structure）

### 指标：KD MTF P0

**体系角色**：`STRUCTURE_FILTER` —— 回答"现在是什么市场状态，该往哪个方向看"

### 决策逻辑

| 条件组合 | 结果 | 说明 |
|---------|------|------|
| `kd_alignment_tier = s` + `kd_direction_filter = long_preferred` | **LONG_BIAS** | 三周期共振多头，可寻找做多机会 |
| `kd_alignment_tier = s` + `kd_direction_filter = short_preferred` | **SHORT_BIAS** | 三周期共振空头，可寻找做空机会 |
| `kd_alignment_tier = b` | **WAIT** | 部分确认，等待 4H 确认或回调 |
| `kd_alignment_tier = conflict` | **NO_TRADE** | 周期冲突，观望 |
| `kd_week_extreme_zone = overbought` + `long_preferred` | **LONG_BIAS_WITH_CAUTION** | 多头但周线超买，等回调或缩量 |
| `kd_week_extreme_zone = oversold` + `short_preferred` | **SHORT_BIAS_WITH_CAUTION** | 空头但周线超卖，等反弹或缩量 |

### 时间框架映射（按市场）

| 市场 | 结构层周期 | 说明 |
|------|-----------|------|
| **A股** | 周线 → 日线 → 60分钟 | T+1 限制，日线定方向，60分钟找结构 |
| **外汇** | 日线 → 4H → 1H | 24H 连续，4H 为主结构，1H 为执行参考 |
| **币圈** | 日线 → 4H → 1H | 7×24，高波动，日线过滤噪音 |
| **期货** | 日线 → 4H → 1H | 换月跳空注意，日线定方向 |

### 外部参考映射

- **ICT**：`kd_alignment_tier = s` 对应 "三周期结构对齐"（HTF trend + ITF structure + LTF entry）
- **Al Brooks**：`kd_week_extreme_zone` 对应超买/超卖区的 "Always In" 偏向反转
- **YTC**：`conflict` 对应框架边界不明确，不交易

---

## 第二层：能量层（Energy）

### 子层 2A：波动率状态 —— Volty

**体系角色**：`ENERGY_FILTER` —— 回答"当前波动率是否适合交易"

### 决策逻辑

| 条件 | 结果 | 说明 |
|------|------|------|
| `volty_stop_distance_atr_bucket = tight` | **ENERGY_LOW** | 波动率压缩，可能即将突破，观望或缩小仓位 |
| `volty_stop_distance_atr_bucket = medium` | **ENERGY_NORMAL** | 正常波动，可正常交易 |
| `volty_stop_distance_atr_bucket = wide` | **ENERGY_HIGH** | 波动率扩张，风险增大，减仓或观望 |
| `volty_trend_state` 与 `KD方向` 一致 | **ENERGY_CONFIRM** | 通道方向与结构方向一致 |
| `volty_trend_state` 与 `KD方向` 冲突 | **ENERGY_CONFLICT** | 通道方向与结构方向冲突，观望 |

### 外部参考映射

- **Clenow**：`volty_stop_distance_atr` 直接对应 ATR 波动率仓位缩放逻辑
- **ICT**：`tight` 对应 "低波动压缩期"，常有突破前奏

### 子层 2B：量价确认 —— PV Corr

**体系角色**：`ENERGY_CONFIRM` —— 回答"价格运动是否得到成交量确认"

### 决策逻辑

| 条件 | 结果 | 说明 |
|------|------|------|
| `pv_pressure_bias = up_confirm` + `LONG_BIAS` | **VOLUME_CONFIRM** | 多头量价共振，能量确认 |
| `pv_pressure_bias = down_confirm` + `SHORT_BIAS` | **VOLUME_CONFIRM** | 空头量价共振，能量确认 |
| `pv_pressure_bias = mixed` (diverge) | **VOLUME_WARN** | 量价背离，警告 |
| `pv_extreme_flag = price_up_volume_down` + `LONG_BIAS` | **VOLUME_REJECTION** | 价涨量缩，多头危险 |
| `pv_extreme_flag = price_down_volume_up` + `SHORT_BIAS` | **VOLUME_REJECTION** | 价跌量增，空头危险 |

### 约束

- `PV Corr` 仍为 `DIAG_ONLY`，本框架只把它作为**能量层过滤条件**，不直接生成入场信号。
- 当 `VOLUME_REJECTION` 时，结构层信号降级为 `WAIT`。

---

## 第三层：执行层（Execution）

### 指标：XBreaking

**体系角色**：`EXECUTION_TRIGGER` —— 回答"具体结构突破点在哪里"

### 当前状态

- `XBreaking` 仍为 `NEED_PROBE / DIAG`。
- 当前框架只定义**占位规则**：当 `XBreaking` 的 buffer 语义确认后，它应该承担以下角色。

### 占位规则（待 XBreaking 语义确认后激活）

| 前置条件 | 触发条件 | 动作 |
|---------|---------|------|
| `STRUCTURE_FILTER = LONG_BIAS` + `ENERGY_FILTER = ENERGY_NORMAL` | `XBreaking` 确认向上突破结构 | **LONG_ENTRY** |
| `STRUCTURE_FILTER = SHORT_BIAS` + `ENERGY_FILTER = ENERGY_NORMAL` | `XBreaking` 确认向下突破结构 | **SHORT_ENTRY** |
| `ENERGY_FILTER = ENERGY_LOW` | `XBreaking` 任何方向突破 | **WAIT** 或 **缩小仓位** |
| `ENERGY_FILTER = ENERGY_HIGH` | `XBreaking` 任何方向突破 | **WAIT** 或 **减仓** |

### 外部参考映射

- **YTC**：`XBreaking` 对应 `BOF` (Breakout Failure) 或 `BPB` (Breakout Pullback) 的确认点
- **ICT**：`XBreaking` 对应 Liquidity Sweep 后的结构突破
- **Al Brooks**：`XBreaking` 对应 Breakout Pullback 后的趋势延续确认

### 当前执行替代方案

在 `XBreaking` 语义未确认前，执行层退化为**手动结构观察**：
- 在结构层方向明确 + 能量层正常时，等待价格突破前高/前低或回调确认后手动入场。
- 这对应于 Al Brooks 的 "limit order entry on pullback" 或 YTC 的 "wholesale entry"。

---

## 第四层：风控层（Risk Guard）

### 子层 4A：情绪极端 —— RSJ

**体系角色**：`RISK_FILTER` —— 回答"当前市场情绪是否处于极端状态"

### 决策逻辑

| 条件 | 结果 | 说明 |
|------|------|------|
| `rsj_state = warm` + `rsj_extreme_flag = extreme_high` | **RISK_EXTREME_EUPHORIA** | 极端乐观，新多头仓位暂停，已有仓位收紧止损 |
| `rsj_state = cold` + `rsj_extreme_flag = extreme_low` | **RISK_EXTREME_FEAR** | 极端恐慌，反向机会但需确认，新仓位缩小 |
| `rsj_timing_bias = risk_on` + 结构层无信号 | **RISK_CONTEXT_OK** | 环境允许交易，但需等待结构 |
| `rsj_timing_bias = risk_off` | **RISK_CONTEXT_BAD** | 环境不利，全系统暂停或减仓 |

### 约束

- `RSJ` 仍为 `DIAG_ONLY`，本框架只把它作为**全局风险开关**，不直接平仓。
- 当 `RISK_EXTREME_EUPHORIA` 或 `RISK_CONTEXT_BAD` 时，所有新入场信号降级为 `WAIT`。

### 子层 4B：止损锚定 —— Volty Stop

**体系角色**：`STOP_ANCHOR` —— 回答"具体止损位置在哪里"

### 决策逻辑

| 仓位方向 | 止损位置 | 说明 |
|---------|---------|------|
| 多头 | `volty_up_stop` | 动态上移，跟踪止损 |
| 空头 | `volty_dn_stop` | 动态下移，跟踪止损 |
| `volty_stop_distance_atr` 过大 | **缩小仓位** | 按 Clenow 的 ATR 仓位缩放 |
| `volty_flip_signal` 触发 | **考虑平仓/反转** | 趋势可能翻转 |

### 外部参考映射

- **Clenow**：ATR 直接用于仓位缩放（risk per trade = fixed % / ATR）
- **YTC**：结构止损位于 swing high/low 外侧

---

## 第五层：审计层（Audit）

### 指标：indicator_audit

**体系角色**：`PERFORMANCE_AUDIT` —— 回答"这个体系是否有效"

### 审计清单

| 审计项 | 检查内容 | 频率 |
|-------|---------|------|
| 结构层命中率 | `kd_alignment_tier = s` 后价格是否沿方向运动 | 每周 |
| 能量层过滤效果 | `ENERGY_LOW` 或 `VOLUME_REJECTION` 是否避开亏损 | 每月 |
| 执行层延迟 | `XBreaking` 确认点 vs 实际最优入场点差异 | 每批次 |
| 风控层保护 | `RSJ` 极端信号前是否触发大额回撤 | 每月 |
| 整体盈亏比 | 平均盈利/平均亏损 > 1.5 | 每月 |
| 最大回撤 | 连续亏损次数 < 5 次且回撤 < 10% | 每月 |

---

## 完整决策流程（示例：外汇 4H/1H）

```
Step 1: 结构层判定
├─ 日线 KD: 周线 = up, 日线 = up, 4H = up
├─ → kd_alignment_tier = s, kd_direction_filter = long_preferred
├─ → STRUCTURE_FILTER = LONG_BIAS
│
Step 2: 能量层确认
├─ Volty: volty_trend_state = up, stop_distance = medium
├─ → ENERGY_FILTER = ENERGY_NORMAL
├─ PV Corr: pv_pressure_bias = up_confirm
├─ → VOLUME_CONFIRM
│
Step 3: 风控层检查
├─ RSJ: rsj_state = neutral, rsj_extreme_flag = none
├─ → RISK_CONTEXT_OK
│
Step 4: 执行层等待
├─ XBreaking (占位): 等待 1H 结构突破确认
├─ 或手动: 等待价格回调至 4H 支撑位 + 1H 确认阳线
│
Step 5: 入场
├─ 执行 LONG_ENTRY
├─ 止损: volty_up_stop 或结构前低外侧
├─ 仓位: 按 ATR 缩放，volty_stop_distance_atr 正常 = 标准仓位
│
Step 6: 持仓监控
├─ 每根 4H bar close: 检查 volty_up_stop 是否上移
├─ 每日: 检查 RSJ 是否进入 extreme_high
├─ 若 RSJ = extreme_high: 收紧止损或部分平仓
│
Step 7: 出场
├─ 目标位: 前高/结构阻力位
├─ 止损位: volty_up_stop 被触及
├─ 或: XBreaking 反向信号确认（未来）
```

---

## 市场适配表

| 维度 | A股 | 外汇 | 币圈 | 期货 |
|------|-----|------|------|------|
| **结构层主周期** | 日线/周线 | 4H/日线 | 日线/4H | 日线/4H |
| **执行层次周期** | 60分钟 | 1H/15分钟 | 1H/15分钟 | 1H/15分钟 |
| **Volty 参数** | Kv=2.5, ATR=20 | Kv=2.0, ATR=14 | Kv=3.0, ATR=20 | Kv=2.0, ATR=14 |
| **PV Corr 窗口** | 20 日 | 20 根 bar | 20 根 bar | 20 根 bar |
| **RSJ 窗口** | 20 日 | 20 根 bar | 20 根 bar | 20 根 bar |
| **特殊处理** | 涨跌停过滤 | 重大新闻日暂停 | 插针检测 | 换月跳空过滤 |
| **仓位缩放** | 低杠杆 | 中等杠杆 | 低杠杆 | 合约倍数 |
| **RSJ 极端处理** | 全部暂停 | 避开 NFP/央行决议 | 避开重大事件 | 避开交割周 |

---

## 与现有仓库的对接

### 已存在指标的位置映射

| 指标 | 当前仓库位置 | 框架角色 | 当前状态 |
|------|------------|---------|---------|
| KD MTF P0 | `01_active_objects/dy_r1_kd_mtf_p0/` | 结构层 | FIELD_READY |
| Volty | `02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/` | 能量层+风控层 | FIELD_READY |
| XBreaking | `02_runtime/mt_indicator_probes/batch_01_volty_xbreaking/` | 执行层 | NEED_PROBE |
| PV Corr | `legacy_analysis/12_工具运行时_TOOLING_RUNTIME/pv_corr_state_p0_v1/` | 能量层 | DIAG_ONLY |
| RSJ | `legacy_analysis/12_工具运行时_TOOLING_RUNTIME/rsj_state_p0_v1/` | 风控层 | DIAG_ONLY |

### 下一步推进建议

1. **短期（XBreaking 语义确认前）**
   - 用 KD MTF + Volty + RSJ 构建 "最小可运行体系"
   - 执行层退化为手动：结构明确 + 能量正常 + 风险可控 → 手动等结构突破
   - 这对应 Al Brooks / YTC 的 "pullback entry" 模式

2. **中期（XBreaking 语义确认后）**
   - 补全执行层自动触发
   - 构建 `indicator_audit` 回测框架
   - 测试四市场的参数鲁棒性

3. **长期**
   - 从 F1 (外汇) 的已有 CUTPACK 中提取更多结构判定规则
   - 从 F2 (微观结构) 中提取订单流确认逻辑
   - 从 A2 (市场轮廓) 中提取价值区域过滤

---

## 外部参考精读清单

### 必读（与框架直接相关）

| 来源 | 内容 | 与框架的对应 |
|------|------|------------|
| **ICT** | Market Structure + Kill Zone | 结构层多周期对齐 + 时间窗口过滤 |
| **Al Brooks** | Trading Price Action Trends | 结构层趋势判定 + 回测框架 |
| **YTC (Lance Beggs)** | TST/BOF/BPB 框架 | 执行层突破-回测结构 |
| **Clenow** | Following the Trend | 能量层 ATR 过滤 + 仓位管理 |

### 选读（深化特定层）

| 来源 | 内容 | 对应层 |
|------|------|--------|
| **Adam Grimes** | The Art and Science of Technical Analysis | 结构层深化 |
| **Kris Verma** | Kelly Criterion + 统计优势 | 风控层仓位管理 |
| **Jim Dalton** | Market Profile | 结构层价值区域（你的 A2 已切割） |

---

## 版本记录

- v0.1 (2026-07-06): 初版框架，基于现有指标字段定义 + 外部参考映射
- 下一步: 确认 XBreaking buffer 语义，或退化为手动执行层

---

## 一句话总结

> **结构定方向（KD MTF），能量定条件（Volty + PV），风控定生死（RSJ + Volty Stop），执行等突破（XBreaking / 手动）。**