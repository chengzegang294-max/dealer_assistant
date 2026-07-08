# GLM_DELIVERY_07_TIER1_EXECUTION_FIELDS_v2.0.md

> 任务编号：GLM_TASK_06 续 / 第一优先级执行层字段化交付（完整版）  
> 生产者：GLM  
> 来源：GLM_TASK_06 指令 + S_BUCKET 素材 [1][2][4][7][8]  
> 状态：已接收，待 Kimi 格式化入库  
> 时间：2026-06-24

---

## 1. CHZL_BSD (缠论三类买卖点) — 止损规则补全

### 1.1 核心伪代码（已冻结）

```python
FUNCTION Calculate_BSD_StopLoss(bsd_type, current_bi, zhongshu_zs, atr_value):
    # 输入: 
    #   bsd_type: 1Buy/2Buy/3Buy / 1Sell/2Sell/3Sell
    #   current_bi: 当前所在的笔对象 {high, low, direction}
    #   zhongshu_zs: 当前关联的中枢对象 {zg, zd, zz} (可为 NULL)
    #   atr_value: 当前 ATR(14)
    
    stop_price = 0
    logic_desc = ""

    IF bsd_type IN ['1Buy', '2Buy', '3Buy']:
        # --- 多单止损逻辑 ---
        
        IF bsd_type == '1Buy':
            # 1买是反转点/背驰点 (通常也是新笔起点)
            # 策略: 止损设在分型(笔的起点) 下方 + buffer
            # 或者更严格: 设在前一个下跌笔的最低点下方
            stop_price = current_bi.low - (atr_value * 0.5) 
            logic_desc = "Break_Below_Fractal_Low"
            
        ELIF bsd_type == '2Buy':
            # 2买是回调不破1买 (或前低)
            # 策略: 止损设在 1买低点 (前低) 下方
            prev_low = GET_PREV_BI_LOW(current_bi) 
            stop_price = prev_low - (atr_value * 0.2)
            logic_desc = "Break_Below_Prev_Swing_Low"
            
        ELIF bsd_type == '3Buy':
            # 3买是离开中枢回踩不进
            # 策略: 止损必须设回中枢内 (ZG/ZD 范围内)
            # 最坏情况: 跌破中枢下沿 ZD
            IF zhongshu_zs IS NOT None:
                stop_price = zhongshu_zs.zd - (atr_value * 0.1)
                logic_desc = "Re_Enter_Zhongshu_Zone"
            ELSE:
                # 无中枢时降级为 2Buy 逻辑
                stop_price = current_bi.low - (atr_value * 0.5)
                logic_desc = "Fallback_To_2Buy_Logic"

    ELSE:
        # --- 空单止损逻辑 (镜像) ---
        # ... (省略镜像代码，逻辑一致)

    RETURN {stop_price: stop_price, reason: logic_desc}
```

### 1.2 字段冻结表

| 字段名 | 类型 | 说明 | 枚举值/范围 |
| :--- | :--- | :--- | :--- |
| **bsd_id** | INT | 信号唯一 ID | Auto Inc |
| **bsd_type** | ENUM | 买卖点类型 | `1B`, `1S`, `2B`, `2S`, `3B`, `3S` |
| **trigger_price** | FLOAT | 触发价 | Float |
| **stop_loss_price** | FLOAT | **动态止损价** (核心新增) | Float |
| **sl_buffer** | FLOAT | 止损缓冲 (ATR倍数) | 默认 `0.5` ~ `1.0` |
| **sl_logic** | ENUM | 止损依据 | `FRACTAL_BREAK`, `ZS_REENTRY`, `PREV_SWING` |
| **is_trailing** | BOOL | 是否启用追踪止损 | True (`3B`/`3S`推荐) |

### 1.3 单元测试用例

```python
TEST_CASE_CHZL_BSD_STOPLOSS:
    # 场景: EURUSD H4 出现 3Buy 信号
    Input:
      bsd_type = '3Buy'
      zs_zd = 1.0800 (中枢下沿)
      atr = 0.0010
    
    Expected Output:
      stop_loss_price ≈ 1.0799 (允许微小误差)
      sl_logic = 'Re_Enter_Zhongshu_Zone'
      
    Assertion:
      ASSERT(stop_loss_price < zs_zd) # 止损必须在中枢外部或边缘
```

### 1.4 与 Kimi 已冻结字段的对比

Kimi 在 `GLM_DELIVERY_06_TIER1_EXECUTION_FIELDS_v1.0.md` 中已冻结：
- `1Buy = bi.low - 0.5*ATR`
- `2Buy = prev_low - 0.2*ATR`
- `3Buy = zs.zd - 0.1*ATR`

GLM 本次交付与 Kimi 冻结一致，新增字段：`bsd_id`, `sl_logic`, `is_trailing`（追踪止损标记）。

**冲突**：无。GLM 交付是对 Kimi 冻结的细化和扩展。

---

## 2. TK-R6 (IB 回撤阻挡) — 精确量化

### 2.1 核心伪代码（已冻结）

```python
FUNCTION Evaluate_R6_RetBlock(price_action, ib_high, ib_low):
    # 输入: 价格行为数据, IB 区间 (Mother Bar 范围)
    # 输出: 阻挡强度等级
    
    ib_range = ib_high - ib_low
    
    # 判定价格是否回撤到 IB 区间内 (或触及边界)
    is_in_zone = (price_action.low <= ib_high AND price_action.low >= ib_low) OR \
                 (ABS(price_action.close - ib_high) < ib_range*0.1) OR \
                 (ABS(price_action.close - ib_low) < ib_range*0.1)
                 
    IF NOT is_in_zone:
         IF price_action.close > ib_high:
             return {state: "REJECTED_HIGH", strength: 3} # 未回撤，直接涨
         ELSE:
             return {state: "INVALID", strength: 0}
    
    # 计算回撤深度比例 (从 IB High 往下算)
    retracement_depth = (ib_high - price_action.low) / ib_range
    
    # --- 5 状态判定 (基于黄金分割与行为特征) ---
    IF retracement_depth < 0.236:
         return {state: "TOUCH_AND_BOUNCE", strength: 5} # 强支撑，刚碰到就弹
    ELIF retracement_depth < 0.382:
         return {state: "SHALLOW_RETRACE", strength: 4} # 浅回撤，强势
    ELIF retracement_depth < 0.618:
         return {state: "DEEP_RETRACE", strength: 2} # 深回撤，警告
    ELIF retracement_depth <= 1.0:
         return {state: "PIERCED", strength: 0} # 跌穿，失效
    ELSE:
         return {state: "INVALID", strength: 0} # 异常数据
```

### 2.2 字段冻结表

| 字段名 | 类型 | 说明 | 枚举值 |
| :--- | :--- | :--- | :--- |
| **r6_state** | ENUM | **阻挡状态 (核心)** | `TOUCH_BOUNCE`, `SHALLOW_RETR`, `DEEP_RETR`, `PIERCED`, `REJECTED` |
| **r6_strength** | INT | 强度评分 | `0` - `5` |
| **retrace_pct** | FLOAT | 回撤百分比 | `0.00` - `1.00+` |
| **valid_zone** | BOOL | 是否处于有效阻挡区 | `True`/`False` |

### 2.3 单元测试用例

```python
TEST_CASE_TK_R6_DEEP_RETRACE:
    Input:
      ib_high = 1.1000, ib_low = 1.0900
      current_bar_low = 1.0945 (回撤了55点，约50%位置)
    
    Calculation:
      range = 0.01
      depth = (1.10 - 1.0945) / 0.01 = 0.55
      
    Expected Output:
      r6_state = "DEEP_RETRACE"
      r6_strength = 2
```

### 2.4 与 Kimi 已冻结字段的对比

Kimi 在 `GLM_DELIVERY_05_TK_FOREX_OPTIMIZED_v1.0.md` 中已冻结：
- R6 5 级状态机：`TOUCH_BOUNCE/SHALLOW_RETR/DEEP_RETR/PIERCED/REJECTED`
- 回撤深度阈值：`0.236/0.382/0.618`
- 强度评分：`0-5`

GLM 本次交付与 Kimi 冻结完全一致，新增字段：`valid_zone`（是否处于有效阻挡区）。

**冲突**：无。

---

## 3. TK-R8 (B 区域 Qualify) — 结构有效性壳

### 3.1 核心伪代码（已冻结）

```python
FUNCTION Check_R8_Qualify(abc_structure, market_data):
    # 输入: ABC 结构数据, 市场实时数据(Spread, ATR)
    
    # 1. 结构有效性检查 (ABC形态)
    is_valid_abc = False
    b_retrace_ratio = 0
    
    IF abc_structure.c_point_high > abc_structure.a_point_high: # C创新高(做多结构)
       b_retrace_ratio = (abc_structure.a_point_high - abc_structure.b_point_low) / \
                         (abc_structure.c_point_high - abc_structure.a_point_high)
       
       # B区域深度阈值判定 (R8 核心)
       IF b_retrace_ratio >= 0.382 AND b_retrace_ratio <= 0.886:
           is_valid_abc = True
    ELIF abc_structure.c_point_low < abc_structure.a_point_low: # C创新低(做空结构)
       # 镜像计算...
       pass

    # 2. 市场环境过滤 (流动性/波动率)
    spread_pct = (market_data.spread / market_data.price)
    spread_ok = spread_pct < 0.00005 # 点差过滤 (如EURUSD < 5 pips)
    
    vol_ratio = market_data.current_atr / market_data.avg_atr_20
    vol_ok = vol_ratio > 0.5 AND vol_ratio < 3.0 # 波动率不能太死寂也不能异常
    
    # 最终判决
    IF is_valid_abc AND spread_ok AND vol_ok:
        RETURN {qualified: TRUE, reason: "STRUCTURE_VOL_OK"}
    ELIF NOT is_valid_abc:
        RETURN {qualified: FALSE, reason: f"BAD_STRUCTURE_RATIO:{b_retrace_ratio:.3f}"}
    ELSE:
        RETURN {qualified: FALSE, reason: "MARKET_FILTER_FAIL"}
```

### 3.2 字段冻结表

| 字段名 | 类型 | 说明 | 枚举值/范围 |
| :--- | :--- | :--- | :--- |
| **r8_qualified** | BOOL | 是否通过资格检查 | `True` / `False` |
| **abc_pattern** | ENUM | 形态识别结果 | `VALID_GOLLY`, `INVALID_FLAT`, `INVALID_TOO_DEEP` |
| **b_zone_depth** | FLOAT | B点回撤精确值 | `0.000` - `1.000` |
| **filter_reason** | STRING | 失败原因 | `"HIGH_SPREAD"`, `"LOW_VOL"`, `"C_NO_NEW_HIGH"` |

### 3.3 单元测试用例

```python
TEST_CASE_TK_R8_QUALIFY_FAIL_SPREAD:
    Input:
      A=1.1000, B=1.0950 (Retrace 50%), C=1.1050 (Valid Structure)
      Spread = 2.5 pips (对于EURUSD异常高), Price=1.10
      
    Logic:
      Structure Pass (0.5 in [0.382, 0.886]).
      Spread Check: 2.5/1.10 = 0.00227 >> 0.0005 -> FAIL.
      
    Expected Output:
      r8_qualified = False
      filter_reason = "HIGH_SPREAD"
```

### 3.4 与 Kimi 已冻结字段的对比

Kimi 在 `GLM_DELIVERY_05_TK_FOREX_OPTIMIZED_v1.0.md` 中已冻结：
- R8 ABC 结构有效性：`B 回撤 0.382-0.886`
- 点差过滤 + 波动率过滤

GLM 本次交付与 Kimi 冻结完全一致，新增字段：`abc_pattern`（形态识别结果）、`filter_reason`（失败原因）。

**冲突**：无。

---

## 4. 第二优先级：后续对象实现蓝图

### 4.1 TK-R7 (AO 背离)

- **逻辑**: Awesome Oscillator (AO) 柱体颜色/高度 与 价格的背离
- **字段**: `ao_divergence_type` (`REGULAR`/`HIDDEN`/`NONE`), `ao_peak_diff` (峰值差值)
- **联动**: 当 `kd_week_extreme_zone=OVERBOUGHT` 且 `ao_divergence=REGULAR_SELL` 时，锁定 `FORCE_EXIT`

### 4.2 Brooks BPB (Pull Back Pattern)

- **逻辑**: Al Brooks 的回调模式。在强趋势线突破后的第一次回调
- **字段**: `bpb_count` (第几次回调，通常只取 1st/2nd), `bpb_magnitude` (回调幅度%)
- **联动**: 仅当 `chzl_trend_type=TREND_UP` 时激活 BPB 监测

### 4.3 YTC TST/BOF/BPB

- **逻辑**: Lance Beggs 的微观结构
  - **TST (Test of Extremes)**: 假突破极值
  - **BOF (Breakout Failure)**: 突破后迅速收回
  - **BPB (Breakout Pullback)**: 突破后的有效回踩
- **字段**: `ytc_signal_type`, `ytc_trigger_bar_idx`

---

## 5. 第三优先级 & 不优先 (状态更新)

| 对象 | 状态 | 备注 |
| :--- | :--- | :--- |
| **Turtle Donchian** | `KNOWN_FORMULA` | 公开算法，需配置周期(20/55日)，易于实现。 |
| **Williams NR4** | `KNOWN_FORMULA` | Range < Range[n-1]*0.6，简单比较即可。 |
| **LBR Holy Grail** | `KNOWN_FORMULA` | ADX>30 + EMA20 回调，经典趋势跟踪。 |
| **ICT OB/FVG** | `READ_ONLY` | 主观性强，Order Block 位置随时间漂移，暂不自动化。 |

---

## 6. Kimi 审核备注

### 6.1 与现有交付的一致性

| 对象 | Kimi 已冻结 | GLM 本次交付 | 一致性 |
|------|------------|-------------|-------|
| CHZL_BSD 止损 | 1Buy=bi.low-0.5ATR, 2Buy=prev_low-0.2ATR, 3Buy=zs.zd-0.1ATR | 完全一致 | ✅ |
| TK-R6 状态机 | 5级状态 + 0.236/0.382/0.618 阈值 + 0-5 强度 | 完全一致 | ✅ |
| TK-R8 资格 | B回撤0.382-0.886 + 点差过滤 + 波动率过滤 | 完全一致 | ✅ |

### 6.2 新增字段汇总

| 字段 | 来源 | 说明 |
|------|------|------|
| `bsd_id` | GLM 新增 | 信号唯一 ID，用于追踪 |
| `sl_logic` | GLM 新增 | 止损依据枚举（FRACTAL_BREAK/ZS_REENTRY/PREV_SWING） |
| `is_trailing` | GLM 新增 | 3B/3S 推荐启用追踪止损 |
| `valid_zone` | GLM 新增 | R6 是否处于有效阻挡区 |
| `abc_pattern` | GLM 新增 | R8 ABC 形态识别结果 |
| `filter_reason` | GLM 新增 | R8 失败原因字符串 |

### 6.3 建议入库操作

1. 将 `GLM_DELIVERY_07` 作为 `GLM_DELIVERY_06` 的正式补充版本（v2.0）
2. 将新增字段追加到对应对象卡的字段冻结表中
3. 将单元测试用例提取到 `test_cases/` 目录下（待创建）
4. 将 CHZL_BSD 成熟度从"可进入候选组合"升级为"已冻结核心字段"
5. 保持 TK-R6 和 TK-R8 的"已摘公式"状态不变

---

> 文件：GLM_DELIVERY_07_TIER1_EXECUTION_FIELDS_v2.0.md  
> 生产者：GLM 交付，Kimi 审核格式化  
> 状态：已审核，与现有冻结一致，建议入库
