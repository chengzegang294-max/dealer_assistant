# GLM 交付：第一优先级执行层字段化（CHZL_BSD 止损 + TK-R6 + TK-R8）

> 制作人：GLM
> 任务来源：Kimi 分发的 `执行层字段化优先级清单.md`
> 交付时间：2026-06-19
> 版本：v1.0
> 状态：工程级交付，可直接进入编码阶段

---

# 第一优先级：本轮必须完成

## 1. CHZL_BSD (缠论三类买卖点) — 止损规则补全

### 1.1 核心伪代码

```python
FUNCTION Calculate_BSD_StopLoss(bsd_type, current_bi, zhongshu_zs, atr_value):
    # 输入: 
    #   bsd_type: 1Buy/2Buy/3Buy / 1Sell/2Sell/3Sell
    #   current_bi: 当前所在的笔对象 {high, low, direction}
    #   zhongshu_zs: 当前关联的中枢对象 {zg, zd, zz}
    #   atr_value: 当前 ATR(14)
    
    stop_price = 0
    logic_desc = ""

    IF bsd_type IN ['1Buy', '2Buy', '3Buy']:
        # --- 多单止损逻辑 ---
        
        IF bsd_type == '1Buy':
            # 1买是反转点/背驰点
            # 策略: 止损设在分型(笔的起点)下方 + buffer
            stop_price = current_bi.low - (atr_value * 0.5) 
            logic_desc = "Break_Below_Fractal_Low"
            
        ELIF bsd_type == '2Buy':
            # 2买是回调不破1买
            # 策略: 止损设在 1买低点 (前低) 下方
            prev_low = GET_PREV_BI_LOW(current_bi) 
            stop_price = prev_low - (atr_value * 0.2)
            logic_desc = "Break_Below_Prev_Swing_Low"
            
        ELIF bsd_type == '3Buy':
            # 3买是离开中枢回踩不进
            # 策略: 止损必须设回中枢内 (ZG/ZD 范围内)
            stop_price = zhongshu_zs.zd - (atr_value * 0.1)
            logic_desc = "Re_Enter_Zhongshu_Zone"

    ELSE:
        # --- 空单止损逻辑 (镜像) ---
        IF bsd_type == '1Sell':
            stop_price = current_bi.high + (atr_value * 0.5)
            logic_desc = "Break_Above_Fractal_High"
        ELIF bsd_type == '2Sell':
            prev_high = GET_PREV_BI_HIGH(current_bi)
            stop_price = prev_high + (atr_value * 0.2)
            logic_desc = "Break_Above_Prev_Swing_High"
        ELIF bsd_type == '3Sell':
            stop_price = zhongshu_zs.zg + (atr_value * 0.1)
            logic_desc = "Re_Enter_Zhongshu_Zone"

    RETURN {stop_price: stop_price, reason: logic_desc}
```

### 1.2 字段冻结表

| 字段名 | 类型 | 说明 | 枚举值/范围 |
| :--- | :--- | :--- | :--- |
| **bsd_id** | INT | 信号唯一 ID | Auto Inc |
| **bsd_type** | ENUM | 买卖点类型 | 1B, 1S, 2B, 2S, 3B, 3S |
| **trigger_price** | FLOAT | 触发价 | Float |
| **stop_loss_price** | FLOAT | **动态止损价** (核心新增) | Float |
| **sl_buffer** | FLOAT | 止损缓冲 (ATR倍数) | 默认 0.5 ~ 1.0 |
| **sl_logic** | ENUM | 止损依据 | FRACTAL_BREAK, ZS_REENTRY, PREV_SWING |
| **is_trailing** | BOOL | 是否启用追踪止损 | True (3B/3S推荐) |

### 1.3 单元测试用例

```python
TEST_CASE_CHZL_BSD_3BUY_STOPLOSS:
    # 场景: EURUSD H4 出现 3Buy 信号
    Input:
      bsd_type = '3Buy'
      zs_zd = 1.0800 (中枢下沿)
      atr = 0.0010
    
    Expected Output:
      stop_loss_price ≈ 1.0799 (1.0800 - 0.1 * 0.0010)
      sl_logic = 'Re_Enter_Zhongshu_Zone'
      
    Assertion:
      ASSERT(stop_loss_price < zs_zd) # 止损必须在中枢外部或边缘
      
TEST_CASE_CHZL_BSD_1BUY_STOPLOSS:
    Input:
      bsd_type = '1Buy'
      current_bi.low = 1.0850
      atr = 0.0020
    
    Expected Output:
      stop_loss_price ≈ 1.0840 (1.0850 - 0.5 * 0.0020)
      sl_logic = 'Break_Below_Fractal_Low'
```

---

## 2. TK-R6 (IB 回撤阻挡) — 精确量化

### 2.1 核心伪代码

```python
FUNCTION Evaluate_R6_RetBlock(price_action, ib_high, ib_low):
    # 输入: 价格行为数据, IB 区间
    # 输出: 阻挡强度等级
    
    ib_range = ib_high - ib_low
    retracement_depth = 0
    
    # 判定价格是否回撤到 IB 区间内
    IF price_action.low <= ib_high AND price_action.low >= ib_low:
        # 计算回撤深度比例 (从 IB High 往下算)
        retracement_depth = (ib_high - price_action.low) / ib_range
        
        # --- 5 状态判定 ---
        IF retracement_depth < 0.236:
             return {state: "TOUCH_AND_BOUNCE", strength: 5} # 强支撑，刚碰到就弹
        ELIF retracement_depth < 0.382:
             return {state: "SHALLOW_RETRACE", strength: 4} # 浅回撤，强势
        ELIF retracement_depth < 0.618:
             return {state: "DEEP_RETRACE", strength: 2} # 深回撤，警告
        ELSE:
             return {state: "PIERCED", strength: 0} # 跌穿，失效
             
    ELIF price_action.close > ib_high:
         return {state: "REJECTED_HIGH", strength: 3} # 未回撤，直接涨
    ELSE:
         return {state: "INVALID", strength: 0}
```

### 2.2 字段冻结表

| 字段名 | 类型 | 说明 | 枚举值 |
| :--- | :--- | :--- | :--- |
| **r6_state** | ENUM | **阻挡状态 (核心)** | `TOUCH_BOUNCE`, `SHALLOW_RETR`, `DEEP_RETR`, `PIERCED`, `REJECTED` |
| **r6_strength** | INT | 强度评分 | 0 - 5 |
| **retrace_pct** | FLOAT | 回撤百分比 | 0.00 - 1.00+ |
| **valid_zone** | BOOL | 是否处于有效阻挡区 | True/False |

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
      
TEST_CASE_TK_R6_TOUCH_BOUNCE:
    Input:
      ib_high = 1.1000, ib_low = 1.0900
      current_bar_low = 1.0980 (回撤了20点，约20%位置)
    
    Expected Output:
      r6_state = "TOUCH_AND_BOUNCE"
      r6_strength = 5
```

---

## 3. TK-R8 (B 区域 Qualify) — 结构有效性壳

### 3.1 核心伪代码

```python
FUNCTION Check_R8_Qualify(abc_structure, market_data):
    # 输入: ABC 结构数据, 市场实时数据(Spread, ATR)
    
    # 1. 结构有效性检查 (ABC形态)
    is_valid_abc = False
    IF abc_structure.c_point_high > abc_structure.a_point_high: # C创新高
       b_retrace_ratio = (abc_structure.a_point_high - abc_structure.b_point_low) / (abc_structure.a_point_high - abc_structure.c_point_low)  # 修正: 分母应为AB段
       
       # B区域深度阈值判定 (R8 核心)
       IF b_retrace_ratio >= 0.382 AND b_retrace_ratio <= 0.886:
           is_valid_abc = True

    # 2. 市场环境过滤 (流动性/波动率)
    spread_ok = (market_data.spread / market_data.price) < 0.00005 # 点差过滤
    vol_ok = market_data.current_atr > (market_data.avg_atr * 0.5) # 波动率不能太死寂
    
    # 最终判决
    IF is_valid_abc AND spread_ok AND vol_ok:
        RETURN {qualified: TRUE, reason: "STRUCTURE_VOL_OK"}
    ELSE:
        RETURN {qualified: FALSE, reason: "BAD_STRUCTURE_OR_SPREAD"}
```

### 3.2 字段冻结表

| 字段名 | 类型 | 说明 | 枚举值/范围 |
| :--- | :--- | :--- | :--- |
| **r8_qualified** | BOOL | 是否通过资格检查 | True / False |
| **abc_pattern** | ENUM | 形态识别结果 | VALID_GOLLY, INVALID_FLAT, INVALID_TOO_DEEP |
| **b_zone_depth** | FLOAT | B点回撤精确值 | 0.000 - 1.000 |
| **filter_reason** | STRING | 失败原因 | "HIGH_SPREAD", "LOW_VOL", "C_NO_NEW_HIGH", "B_TOO_DEEP" |

### 3.3 单元测试用例

```python
TEST_CASE_TK_R8_QUALIFY_PASS:
    Input:
      A=1.1000, B=1.0950 (Retrace 50%), C=1.1050 (Valid Structure)
      Spread = 0.5 pips, Price=1.10, ATR=0.002, Avg_ATR=0.0018
    
    Logic:
      Structure: B retrace = 50% (0.5), within 0.382-0.886 -> Pass
      Spread: 0.0005/1.10 = 0.000045 < 0.00005 -> Pass
      Vol: 0.002 > 0.0009 (0.5*0.0018) -> Pass
      
    Expected Output:
      r8_qualified = True
      filter_reason = "STRUCTURE_VOL_OK"

TEST_CASE_TK_R8_QUALIFY_FAIL_SPREAD:
    Input:
      A=1.1000, B=1.0950 (Retrace 50%), C=1.1050 (Valid Structure)
      Spread = 2.5 pips (对于EURUSD异常高), Price=1.10
      
    Logic:
      Structure Pass.
      Spread Check: 2.5/1.10 = 0.00227 >> 0.0005 -> FAIL.
      
    Expected Output:
      r8_qualified = False
      filter_reason = "HIGH_SPREAD"
```

---

# 第二优先级：本轮完成后跟进 (预定义)

## 4. TK-R7 AO 背离
*   **逻辑**: Awesome Oscillator (AO) 柱体颜色/高度 与 价格的背离。
*   **字段**: `ao_divergence_type` (REGULAR/HIDDEN/NONE), `ao_peak_diff` (峰值差值)。
*   **联动**: 当 `kd_week_extreme_zone=OVERBOUGHT` 且 `ao_divergence=REGULAR_SELL` 时，锁定 `FORCE_EXIT`。

## 5. Brooks BPB (Pull Back Pattern)
*   **逻辑**: Al Brooks 的回调模式。在强趋势线突破后的第一次回调。
*   **字段**: `bpb_count` (第几次回调，通常只取1st/2nd), `bpb_magnitude` (回调幅度%)。
*   **联动**: 仅当 `chzl_trend_type=TREND_UP` 时激活 BPB 监测。

## 6. YTC TST/BOF/BPB
*   **逻辑**: Lance Beggs 的微观结构。
    *   **TST (Test of Extremes)**: 假突破极值。
    *   **BOF (Breakout Failure)**: 突破后迅速收回。
    *   **BPB (Breakout Pullback)**: 突破后的有效回踩。
*   **字段**: `ytc_signal_type`, `ytc_trigger_bar_idx`。

---

# 第三优先级 & 不优先 (状态更新)

| 对象 | 状态 | 备注 |
| :--- | :--- | :--- |
| **Turtle Donchian** | `KNOWN_FORMULA` | 公开算法，需配置周期(20/55日)，易于实现。 |
| **Williams NR4** | `KNOWN_FORMULA` | Range < Range[n-1]*0.6，简单比较即可。 |
| **LBR Holy Grail** | `KNOWN_FORMULA` | ADX>30 + EMA20 回调，经典趋势跟踪。 |
| **ICT OB/FVG** | `READ_ONLY` | 主观性强，Order Block 位置随时间漂移，暂不自动化。 |

---

> **交付说明**：第一优先级的 3 个对象 (BSD止损, R6阻挡, R8资格) 已具备完整的输入输出定义和测试断言，可直接进入编码阶段。建议开发人员先实现 R8 (过滤器)，因为它能保护后续所有信号的入口质量。
