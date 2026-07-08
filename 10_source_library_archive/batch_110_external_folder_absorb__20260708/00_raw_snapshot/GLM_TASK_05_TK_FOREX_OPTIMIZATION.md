# GLM 任务指令 05：TK 外汇系统优化 + 缠论交叉映射

> 制作人：Kimi（任务分发）
> 目标：GLM 输出工程级优化文档，补充 TK 系统的量化判据
> 前置条件：
>   - TK 外汇素材已读取：`D:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_TK外汇`
>   - Kimi 初版对象卡：`TK外汇核心概念对象卡_Kimi版_v1.0.md`
>   - CHZL 中枢已完成：`CHZL_ZS_量化公式与互锁视图_v1.0.md`
> 输出要求：伪代码 + 字段冻结表 + 量化判据 + 交叉映射表

---

## 任务概述

Kimi 已经基于 TK 外汇全部素材（第1/8/9集导出 + 吸收结论 + Batch1索引）制作了初版对象卡。现在需要你在此基础上完成三件事：

1. **优化 TK-IB/DB/CB 伪代码** — 补充边界条件和实时失效检测
2. **为 TK-R6/R7/R8 设计精确量化判据** — 从"后续对象入口"推进到"可进入候选组合"
3. **TK 体系与缠论对象卡的交叉映射** — 找出功能重叠和互补关系

---

## 第一部分：TK-IB/DB/CB 伪代码优化

### 背景

Kimi 的初版伪代码已基本可用，但缺少以下边界条件：

1. **IB 被反向突破的实时检测**：
   - 当前代码只计算了 IB 的静态区间，没有实时检测后续 K 线是否反向突破 IB
   - 要求：给出 `CheckIBValid(ib_struct, candles_after)` 函数，一旦 IB 被反向突破，立即设置 `ib_valid = false`

2. **DB 信号的连续性保护**：
   - 当前代码要求 >=3 根连续蜡烛突破 IB，但如果第2根没突破、第3根突破了，是否算 DB？
   - 要求：明确 DB 的定义 —— 是"连续3根都突破"还是"3根内累计突破"？推荐前者（严格）

3. **CB 定位错误的自动校验**：
   - TK 教学强调：学生常把 CB 点位与 IB 开盘价混淆
   - 要求：在代码中加入 `cb_placement_valid` 校验 —— `cb_level != ib_open`，否则标记 `INVALID_CB_PLACEMENT`

4. **多时间框架兼容性**：
   - XBreaking 在 1H 以下周期需要手动加载历史数据（向左拖动图表）
   - 要求：给出 `CheckDataLoaded(candles, min_required=200)` 函数，如果数据不足，返回 `NEED_MORE_DATA`

### 输出格式

```python
# 请完善以下函数

FUNCTION CheckIBValid(ib_struct, candles_after_ib):
    """
    实时检测 IB 是否被反向突破
    输入：ib_struct, 后续 K 线序列
    输出：{is_valid(bool), broken_at_idx(int), broken_price(float)}
    """
    ...

FUNCTION CheckDBContinuity(ib_struct, candles_after_ib):
    """
    检查 DB 信号的连续性
    严格定义：连续 N 根蜡烛都突破 IB（N>=3）
    输出：{db_triggered(bool), continuous_count(int), max_gap_bars(int)}
    """
    ...

FUNCTION ValidateCBPlacement(cb_level, ib_struct):
    """
    校验 CB 点位是否正确（不等于 IB 开盘价）
    输出：{placement_valid(bool), error_type(enum)}
    """
    ...

FUNCTION CheckDataLoaded(candles, min_required=200):
    """
    检查数据是否足够（XBreaking 小周期排障）
    输出：{sufficient(bool), current_count(int), need_load_more(bool)}
    """
    ...
```

---

## 第二部分：TK-R6/R7/R8 精确量化判据

### 背景

这三个对象当前成熟度为"后续对象入口"，需要从模糊的描述推进到可量化的字段。

### TK-R6：IB 回撤阻挡 → TP3 概率增强

当前状态：
- 已有 `tkr6_manual_audit_sheet_v1.tsv`（人工标注样本）
- 已有 5 个状态标签：`touch_only`, `reject_weak`, `reject_clear`, `inside_ib`, `break_through`

要求你给出：

1. **每个标签的精确量化定义**（用价格/影线/实体比例）：
   - `touch_only`：价格触及 IB 区域上沿/下沿，但收盘在区域外（影线触碰）
   - `reject_weak`：价格进入 IB 区域，但收盘在区域内（实体部分在区域内）
   - `reject_clear`：价格进入 IB 区域后，被强力推回，形成长影线 + 收盘远离 IB 区域
   - `inside_ib`：价格完全在 IB 区域内运行（被包含）
   - `break_through`：价格突破 IB 区域（反向突破 = 信号失效）

2. **TP3 概率增强的触发条件**：
   - `reject_clear` → `tp3_probability = enhanced`
   - `reject_weak` → `tp3_probability = normal`
   - `touch_only` → `tp3_probability = reduced`
   - `break_through` → `tp3_probability = invalid`（信号失效）

3. **最小距离口径**：
   - IB 区域附近的价格行为分类阈值（如：进入 IB 区域超过 50% 算 `inside_ib`？）

### TK-R7：AO 背离风险调整标签

当前状态：
- 已有 `tkr7_manual_audit_sheet_v1.tsv`
- 角色：风险调整标签，不做独立硬信号

要求你给出：

1. **AO 背离的量化定义**：
   - AO 参数标准化（建议周期？默认 5/34？）
   - 背离判定：价格新高/新低 + AO 柱状图未新高/新低
   - 输出：`ao_divergence_flag(enum) + ao_divergence_strength(float)`

2. **与 KD MTF P0 的联合规则**：
   - `kd_week_extreme_zone = overbought` + `ao_divergence = present` → 降低仓位 50%
   - `kd_day_signal = cross_up` + `ao_divergence = present` → 延迟入场（等待确认）

3. **"背了又背"防护**：
   - AO 背离后价格继续加速的过滤条件（如：背离后 3 根 K 线内未反转，取消背离标记）

### TK-R8：B 区域 Qualify 壳

当前状态：
- 已有 `tkr8_manual_audit_sheet_v1.tsv`
- 角色：ABC/B 位挂单的 qualify 条件

要求你给出：

1. **ABC 结构有效性判定**：
   - A → B → C 的波浪比例（如：B 回撤占 AB 段的 38.2%-61.8%）
   - C 点必须创新高/低（否则结构失效）
   - 输出：`abc_valid(bool) + abc_ratio(float)`

2. **B 区域的有效性判定**：
   - B 区域深度：回撤不超过 AB 段的 61.8%（斐波那契回撤）
   - B 区域时间：不超过 AB 段时间的 50%
   - 输出：`b_zone_qualify(bool) + b_zone_depth_ratio(float)`

3. **结构失效的最小条件**：
   - C 点未创新高/低 → `structure_break = true`
   - B 区域后价格继续反向穿透 → `continuation_lost = true`
   - 输出：`structure_status(enum: valid/broken/extending)`

### 输出格式

```python
# TK-R6
FUNCTION ClassifyIBRetest(price_action, ib_struct):
    """
    分类 IB 回撤行为
    输出：{retest_status(enum), tp3_probability(enum), confidence(float)}
    """
    ...

# TK-R7
FUNCTION DetectAODivergence(prices, ao_values, lookback=10):
    """
    检测 AO 背离
    输出：{divergence_flag(enum), strength(float), expiration_bars(int)}
    """
    ...

# TK-R8
FUNCTION ValidateABCStructure(a_point, b_point, c_point):
    """
    验证 ABC 结构有效性
    输出：{abc_valid(bool), abc_ratio(float), b_zone_qualify(bool)}
    """
    ...

# 字段冻结表
TK_R6:
  - ib_retest_status: enum(touch_only, reject_weak, reject_clear, inside_ib, break_through)
  - tp3_probability: enum(enhanced, normal, reduced, invalid)
  - reject_strength: float(0-1)
  
TK_R7:
  - ao_divergence_flag: enum(present, absent, fading)
  - ao_divergence_strength: float(0-1)
  - risk_adjust_action: enum(reduce_50pct, delay_entry, hold, exit)
  
TK_R8:
  - abc_valid: bool
  - abc_ratio: float  # B回撤占AB的比例
  - b_zone_qualify: bool
  - structure_status: enum(valid, broken, extending)
```

---

## 第三部分：TK 体系与缠论对象卡的交叉映射

### 要求

找出 TK 外汇系统（IB/DB/CB/TP3/R6/R7/R8）与缠论对象卡（CHZL_FX/BI/ZS/BC/BSD）之间的功能重叠和互补关系。

### 输出格式

```markdown
| TK 对象 | 缠论对应概念 | 关系类型 | 说明 |
|---------|------------|---------|------|
| TK-IB | CHZL_ZS（中枢） | 互补 | IB 区域 ≈ 中枢的 ZG/ZD 边界；IB 被反向突破 ≈ 中枢破坏 |
| TK-DB | CHZL_BSD-3Buy/3Sell | 重叠 | DB 信号 ≈ 第三类买卖点（突破后不回踩） |
| TK-CB | CHZL_BSD-1Buy/1Sell | 重叠 | CB 信号 ≈ 第一类买卖点（背驰点突破） |
| TK-R6 | CHZL_ZS（中枢延伸） | 互补 | IB 回撤阻挡 ≈ 中枢 ZG/ZD 的支撑阻力测试 |
| TK-R7 | CHZL_BC（背驰） | 重叠 | AO 背离 ≈ MACD 面积背驰（都是能量衰竭信号） |
| TK-R8 | CHZL_BI（笔结构） | 互补 | ABC 结构 ≈ 笔的序列（A=顶分型，B=底分型，C=顶分型） |
| TK-TP3 | CHZL_ZS（中枢离开段） | 互补 | TP3 延伸 ≈ 中枢离开段的预期目标 |

### 互锁建议

1. **当 TK-CB 触发时，检查 CHZL_BC**：
   - 如果 TK-CB = true 且 CHZL_BC = divergence_top → 降低仓位（双重反转信号）
   
2. **当 CHZL_BSD-3Buy 触发时，检查 TK-DB**：
   - 如果两者同时触发 → 高置信度入场
   
3. **当 TK-R7（AO 背离）触发时，检查 CHZL_BC**：
   - 如果两者同时背离 → 强制减仓或离场
```

---

## 约束条件

1. **只输出伪代码和公式**，不要写完整的 Python/MQL4/TradingView 代码
2. **所有条件必须用价格比较**（> < =）、计数（count >= N）或比例（ratio > 0.382），不能用"感觉""大概""可能"
3. **明确标注新旧笔规则**：TK-IB/DB/CB 中 IB 的定义必须与缠论的分型/笔定义兼容（或明确说明差异）
4. **TK-R6/R7/R8 必须从"后续对象入口"推进到"可进入候选组合"**，必须有明确的阈值和触发条件

---

## 输出文件命名建议

`GLM_TASK_05_TK_FOREX_OPTIMIZATION_v1.0.md`

请按上述3个部分组织文档，每个部分有独立的伪代码、字段冻结表和测试断言。
