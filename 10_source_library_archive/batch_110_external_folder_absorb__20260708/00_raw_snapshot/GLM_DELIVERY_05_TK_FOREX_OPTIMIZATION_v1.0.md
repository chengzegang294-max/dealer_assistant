# GLM 交付：TK 外汇系统优化 + 缠论交叉映射（GLM_TASK_05 回复）

> 制作人：GLM
> 任务来源：Kimi 分发的 `GLM_TASK_05_TK_FOREX_OPTIMIZATION.md`
> 交付时间：2026-06-19
> 版本：v1.0
> 状态：工程级交付，需 Kimi 格式化入库

---

## Part 1: IB/DB/CB 伪代码优化（边界条件与实时检测）

针对 Kimi 初版中较为粗糙的定义，以下是增加了**工程鲁棒性**的版本：

### 1.1 IB (Inside Bar) 实时检测与失效

*目标：解决静态定义无法应对盘中波动的问题。*

```python
FUNCTION Detect_IB_Realtime(current_bar, previous_bars):
    # 输入: 当前未收盘K线(或已收盘), 历史序列
    # 输出: {is_ib: bool, mother_ref: bar_index, status: enum}
    
    mother = previous_bars[-1] # 假设 Mother Bar 是前一根
    
    # 1. 基础包含判定
    is_contained = (current_bar.high <= mother.high) AND (current_bar.low >= mother.low)
    
    IF NOT is_contained:
        RETURN {is_ib: False, status: "INVALID"}
        
    # 2. [新增] 失效检测: 盘中假突破过滤
    # 如果是实时盘，允许极短时间的影线刺穿 (如 < 20% range)，但实体必须在内部
    # 或者采用严格模式: 一旦 High/Mother.High 触发失效标记
    IF current_bar.high > mother.high + SLIPPAGE_BUFFER:
        current_status = "INVALID_TOUCH_HIGH" 
        # 逻辑: 此时 IB 结构被破坏，转为 Potential Breakout Mode
        
    # 3. [新增] 强度评分
    ib_range = mother.high - mother.low
    curr_range = current_bar.high - current_bar.low
    strength_ratio = curr_range / ib_range 
    
    # 如果强度比 < 0.3，视为强收缩 (High Compression)
    
    RETURN {
        is_ib: True, 
        mother_high: mother.high,
        mother_low: mother.low,
        status: current_status,
        compression: strength_ratio
    }
```

### 1.2 DB (Directional Break) 连续性保护

*目的：防止假突破导致的误判。*

```python
FUNCTION Confirm_DB(break_candidate, context):
    # 输入: 突破候选K线, 上下文(前N根)
    # 规则: 必须满足 "动力因子的连续性"
    
    # [新增] 连续性保护机制
    # 条件 A: 收盘价确认 (Conservative)
    # 要求突破K线的 Close 价格必须在 Mother Bar 范围之外
    is_close_confirm = (break_candidate.direction == 'UP' AND break_candidate.close > break_candidate.mother_high)
    
    # 条件 B: 反向无长影线 (Aggressive Filter)
    # 如果向上突破，但上影线极长 (> 70% of total range)，视为拒绝 (Rejection)
    upper_wick = break_candidate.high - MAX(break_candidate.open, break_candidate.close)
    body_size = ABS(break_candidate.open - break_candidate.close)
    is_rejection = (upper_wick > body_size * 2.0) 
    
    IF is_close_confirm AND NOT is_rejection:
        RETURN True # 有效突破
    ELSE:
        RETURN False # 无效突破 (Noise)
```

### 1.3 CB (Closing Break) 定位校验

*目的：确保入场点位于有效区域。*

```python
FUNCTION Validate_CB_Entry(price_entry, ib_structure):
    # [新增] B-Area Qualify Check (R8 前置检查)
    
    # 1. 避免追高/追低 (距离验证)
    distance_from_boundary = ABS(price_entry - ib_structure.boundary_price)
    atr_value = GET_CURRENT_ATR(14)
    
    # 规则: 入场价格不能偏离边界超过 0.5 倍 ATR (防止滑点过大)
    IF distance_from_boundary > (atr_value * 0.5):
        RETURN {valid: False, reason: "SLIPPAGE_TOO_HIGH"}
        
    # 2. 时间校验 (可选)
    # 如果是日内交易，检查是否接近收盘 (如美股最后15分钟不新开仓)
    
    RETURN {valid: True, reason: "OK"}
```

---

## Part 2: R6/R7/R8 精确量化判据

将模糊描述转化为可代码化的阈值：

| 对象 ID | 名称 | 量化公式 / 判据 | 触发条件 | 输出字段 |
| :--- | :--- | :--- | :--- | :--- |
| **TK_R06** | **IB 回撤阻挡**<br>(Retracement Block) | **Price Action Proximity**<br>`dist_to_level = ABS(Current_Price - IB_Boundary)`<br>`threshold = IB_Range * 0.236` (黄金分割回调位) | 当 `dist_to_level < threshold` 且 出现 **Pinbar** 或 **Engulfing** 反向K线时触发。 | `r6_signal`: ENUM[STRONG_HOLD, WEAK_HOLD, PIERCED] |
| **TK_R07** | **AO 背离**<br>(Momentum Divergence) | **Awesome Oscillator (AO) Slope**<br>计算最近 2 根 AO 柱体的面积差。<br>`Delta_AO = AO[n] - AO[n-2]`<br>`Delta_Price = Price[n] - Price[n-2]` | **顶背离**: Price Up && AO_Down && AO_Color_Red<br>**底背离**: Price Down && AO_Up && AO_Color_Green | `r7_flag`: BOOL<br>`r7_strength`: FLOAT (Area Diff %) |
| **TK_R08** | **B 区域资格**<br>(Zone Qualify) | **Volatility & Spread Filter**<br>`Spread_Pct = (Ask - Bid) / Mid`<br>`ATR_Ratio = Current_ATR / Avg_ATR_20` | **准入条件**:<br>1. `Spread_Pct < 0.05` (点差正常)<br>2. `ATR_Ratio < 1.5` (非极端波动)<br>3. `Time_In_Session == True` (交易时段内) | `r8_pass`: BOOL |

---

## Part 3: TK × 缠论 (CHZL) 交叉映射

找出两套体系的对应关系，实现功能复用。

### 3.1 功能重叠与冲突对照表

| 维度 | TK 体系 (微观/行为) | 缠论体系 (几何/结构) | **互锁建议** |
| :--- | :--- | :--- | :--- |
| **最小单元** | **IB (Inside Bar)**<br>定义: 波动率收缩 | **CHZL_FX (分型)**<br>定义: 顶底几何形态 | **互补**: 用缠论的"包含处理"来清洗数据，再用 TK 的 IB 逻辑寻找爆发点。 |
| **趋势启动** | **CB (Closing Break)**<br>定义: 收盘价突破区间 | **CHZL_BI (笔破坏)**<br>定义: 反向分型突破原笔极值 | **替代**: 在日内级别 (1H/4H)，CB 比"笔破坏"更灵敏，建议用 **CB 替代** 小级别的笔破坏信号。 |
| **阻力支撑** | **Mother Bar Boundary**<br>定义: IB 前一根的高低点 | **CHZL_ZS (中枢)**<br>定义: 价格密集重叠区 | **融合**: 只有当 TK 的 CB 方向与 **离开中枢 (ZS State=BROKEN)** 方向一致时，才视为高胜率信号。 |
| **能量确认** | **AO Divergence (R7)**<br>基于均线摆动 | **CHZL_BC (MACD Area)**<br>基于面积比较 | **冗余验证**: 同时满足 R7 和 CHZL_BC 时，置信度 * 1.5；若两者冲突，放弃交易 (NOISE)。 |

### 3.2 推荐的融合策略: "中枢内的 IB"

这是一个具体的实战策略组合：
1.  **环境 (Context)**: 缠论显示 `chzl_zs_state = EXTENDING` (处于中枢震荡中)。
2.  ** Setup (设置)**: 在中枢上沿 (`zg`) 附近出现了一个 **TK_IB** (Inside Bar)。这意味着市场在中枢边界犹豫。
3.  **Trigger (触发)**: 价格向下 **CB (Closing Break)** IB 的下沿，且方向是 **回到中枢内部** (回归均值)。
4.  **结论**: 这是一个完美的"中枢高抛低吸"信号，由 TK 提供精确入场，由缠论提供宏观背景。

---

## 附录：成熟度映射对照（GLM 标签 → 仓库标准）

| GLM 标签 | 仓库标准成熟度 | 含义 |
| :--- | :--- | :--- |
| `KNOWN_IO` | known_input_output | 输入输出已定义，接口明确 |
| `VERIFIED_V1` | known_input_output | 已通过 v1.0 断言测试 |
| `CANDIDATE_COMBO` | 可进入候选组合 | 已量化完成，可放入候选组合测试 |
| `PENDING_OPTIMIZATION` | 已摘公式 | 伪代码已完成，正在优化参数敏感度 |
| `CORE_ENGINE` | 可进入候选组合 | 核心引擎，runtime-ready |
| `Production Ready` | 可进入候选组合 | 已通过测试，可进入生产环境 |

---

> **交付说明**：以上内容完成了 TK 体系的工程化升级 并同步了全局状态表。现在系统中，XBreaking 已经就绪，而 TK_R6/R7/R8 正式进入开发队列。
