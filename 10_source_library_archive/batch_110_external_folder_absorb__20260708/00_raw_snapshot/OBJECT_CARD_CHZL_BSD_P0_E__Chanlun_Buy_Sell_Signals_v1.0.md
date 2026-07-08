# CHZL_BSD_P0_E — 缠论三类买卖点（Buy/Sell Signals）对象卡

> 功能层：P0_E（执行层 — 入场/出场/执行质量）  
> 成熟度：已冻结核心字段  
> 生产者：Kimi（基于 GLM_DELIVERY_07 提取）  
> 来源：缠中说禅 + GLM_DELIVERY_07 + CHZL_ZS 量化公式  
> 状态：已冻结核心字段，待代码实现

---

## 1. 基本定义

缠论三类买卖点是缠中说禅理论体系的核心交易信号，基于中枢（ZS）和背驰（BC）推导而来：

- **1Buy（一买）**：趋势下跌背驰后的第一个买入点，通常对应新笔的起点（分型反转）
- **2Buy（二买）**：1Buy 后回调不破前低的买入点，确认趋势反转
- **3Buy（三买）**：离开中枢后不回到中枢的回踩买入点，确认趋势加速
- **1Sell/2Sell/3Sell**：镜像的卖出信号

---

## 2. 核心概念与字段冻结

### 2.1 基础字段（已冻结）

```text
bsd_id              INT     -- 信号唯一 ID（Auto Inc）
bsd_type            ENUM    -- 买卖点类型：
                              -- '1B' = 一买（趋势反转买入）
                              -- '1S' = 一卖（趋势反转卖出）
                              -- '2B' = 二买（回调不破前低买入）
                              -- '2S' = 二卖（反弹不过前高卖出）
                              -- '3B' = 三买（离开中枢回踩买入）
                              -- '3S' = 三卖（离开中枢反弹卖出）
trigger_price       FLOAT   -- 触发价（信号出现时的价格）
current_bi          OBJECT  -- 当前笔对象 {high, low, direction, index}
zhongshu_zs         OBJECT  -- 关联中枢对象 {zg, zd, zz, state}（可为 NULL）
```

### 2.2 止损字段（已冻结）

```text
stop_loss_price     FLOAT   -- 动态止损价（核心新增）
sl_buffer           FLOAT   -- 止损缓冲（ATR 倍数，默认 0.5~1.0）
sl_logic            ENUM    -- 止损依据：
                              -- 'FRACTAL_BREAK' = 跌破分型低点（1Buy/1Sell）
                              -- 'ZS_REENTRY' = 回到中枢区间（3Buy/3Sell）
                              -- 'PREV_SWING' = 跌破前低/前高（2Buy/2Sell）
is_trailing         BOOL    -- 是否启用追踪止损（3B/3S 推荐 True）
```

### 2.3 计算字段（已冻结）

```text
atr_14              FLOAT   -- 14 日 ATR（用于止损计算）
prev_low            FLOAT   -- 前低（用于 2Buy 止损计算）
prev_high           FLOAT   -- 前高（用于 2Sell 止损计算）
```

### 2.4 A 股适配字段（已冻结）

```text
suspend_merge_logic BOOL    -- 停牌合并逻辑：复牌后 K 线特殊处理
limit_fractal_type  ENUM    -- 涨停板分型处理：
                              -- 'normal' = 正常处理
                              -- 'limit_up_merge' = 涨停板合并为一根 K 线
                              -- 'limit_down_merge' = 跌停板合并为一根 K 线
```

---

## 3. 计算逻辑（伪代码）

### 3.1 止损计算

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
            # 止损设在分型(笔的起点) 下方 + buffer
            stop_price = current_bi.low - (atr_value * 0.5) 
            logic_desc = "FRACTAL_BREAK"
            
        ELIF bsd_type == '2Buy':
            # 2买是回调不破1买 (或前低)
            # 止损设在 1买低点 (前低) 下方
            prev_low = GET_PREV_BI_LOW(current_bi) 
            stop_price = prev_low - (atr_value * 0.2)
            logic_desc = "PREV_SWING"
            
        ELIF bsd_type == '3Buy':
            # 3买是离开中枢回踩不进
            # 止损必须设回中枢内 (ZD 范围内)
            IF zhongshu_zs IS NOT None:
                stop_price = zhongshu_zs.zd - (atr_value * 0.1)
                logic_desc = "ZS_REENTRY"
            ELSE:
                # 无中枢时降级为 2Buy 逻辑
                stop_price = current_bi.low - (atr_value * 0.5)
                logic_desc = "PREV_SWING"

    ELSE:
        # --- 空单止损逻辑 (镜像) ---
        # 1Sell: stop = current_bi.high + (atr * 0.5)
        # 2Sell: stop = prev_high + (atr * 0.2)
        # 3Sell: stop = zhongshu_zs.zg + (atr * 0.1)
        pass

    RETURN {stop_price: stop_price, reason: logic_desc}
```

### 3.2 单元测试

```python
TEST_CASE_CHZL_BSD_STOPLOSS:
    # 场景: EURUSD H4 出现 3Buy 信号
    Input:
      bsd_type = '3Buy'
      zs_zd = 1.0800 (中枢下沿)
      atr = 0.0010
    
    Expected Output:
      stop_loss_price ≈ 1.0799 (允许微小误差)
      sl_logic = 'ZS_REENTRY'
      
    Assertion:
      ASSERT(stop_loss_price < zs_zd) # 止损必须在中枢外部或边缘
```

---

## 4. 与现有指标的互锁逻辑（已冻结）

### 4.1 与 KD MTF 的互锁

```text
互锁规则 CHZL_BSD × KD MTF：

1. 方向过滤：
   - 1Buy/2Buy/3Buy 只在 kd_day_signal = 'bullish' 时激活
   - 1Sell/2Sell/3Sell 只在 kd_day_signal = 'bearish' 时激活
   - kd_alignment_tier = 'conflict' → BSD 信号无效

2. 极端区过滤：
   - kd_week_extreme_zone = 'overbought' → 禁止 1Buy/2Buy/3Buy（追高风险）
   - kd_week_extreme_zone = 'oversold' → 禁止 1Sell/2Sell/3Sell（杀跌风险）
   - 但允许 1Buy 在 oversold 区域（趋势反转）

3. 锁仓确认：
   - lock_signal = 'locked' → BSD 信号可执行
   - lock_signal = 'unlocked' → BSD 信号降级为观察
   - lock_signal = 'conflicting' → BSD 信号无效
```

### 4.2 与缠论 ZS/BC 的互锁

```text
互锁规则 CHZL_BSD × CHZL_ZS/BC：

1. 1Buy 必须基于背驰（CHZL_BC）：
   - 1Buy 出现时，必须确认 CHZL_BC 存在（背驰确认）
   - 无背驰的 1Buy → 假信号，禁止交易

2. 2Buy 必须基于中枢（CHZL_ZS）：
   - 2Buy 需要前低（1Buy）不跌破，中枢 ZD 提供支撑参考
   - 2Buy 止损 = prev_low - 0.2×ATR（前低即中枢下沿或附近）

3. 3Buy 必须基于中枢（CHZL_ZS）：
   - 3Buy 需要离开中枢（价格 > ZG）后回踩不进中枢
   - 无中枢时 3Buy 降级为 2Buy 逻辑
   - 3Buy 止损 = ZD - 0.1×ATR（回到中枢即失效）
```

### 4.3 与 VP 的互锁

```text
互锁规则 CHZL_BSD × VP：

1. 1Buy 的理想入场点 = max(1Buy 理论位, 最近的 HVN 下沿)
   - HVN 是历史成交密集区，机构成本区，在此买入更"安全"
2. 2Buy 的理想入场点 = max(2Buy 理论位, POC 附近)
   - POC 是"公平价格"，在此买入成本接近市场平均
3. 3Buy 的理想入场点 = max(3Buy 理论位, VAH 下沿)
   - 3Buy 是突破后回踩，VAH 由阻力变支撑

4. BSD 与 VP 优先级：
   - BSD 提供"结构信号"（什么位置可以买卖），VP 提供"执行价位"（具体什么价格入场/出场）
   - BSD 是战略层，VP 是战术层
```

### 4.4 与 TK 的互锁

```text
互锁规则 CHZL_BSD × TK：

1. 1Buy + TK-R8 ABC 结构有效 → 共振，确认反转
2. 2Buy + TK-R6 TOUCH_BOUNCE → 共振，回调在强支撑处结束
3. 3Buy + TK-R8 qualified → 结构确认，可执行
4. 1Buy + TK-R6 PIERCED → 冲突，结构已破坏，即使背驰出现也谨慎
```

---

## 5. 失效模式（已冻结）

```text
CHZL_BSD 失效条件：

1. 无背驰的 1Buy：
   - 1Buy 必须基于 CHZL_BC 背驰确认，无背驰的 1Buy 是假信号

2. 中枢级别混乱：
   - 中枢级别递归主观，导致 ZG/ZD 计算错误 → 3Buy/3Sell 止损失效

3. A 股特殊失效：
   - 一字涨停板破坏分型连续性 → 笔序列中断
   - 停牌导致笔的时间跨度失真 → 中枢计算错误
   - 连续涨停后出现的 1Sell → 可能是假信号（情绪驱动而非结构反转）
```

---

## 6. A 股特殊适配（已冻结）

```text
A 股 CHZL_BSD 适配规则：

1. 涨停/跌停影响：
   - limit_up = True → 禁止 1Buy/2Buy/3Buy（价格被锁定，无法继续上涨）
   - limit_down = True → 禁止 1Sell/2Sell/3Sell（跌停时无法继续下跌）
   - 涨停/跌停时 BSD 信号标记为 'market_halt'，不执行

2. 一字板分型处理：
   - 一字涨停板（open = close = high）→ 视为特殊分型，不纳入笔序列
   - 使用 limit_fractal_type = 'limit_up_merge' 合并处理

3. 停牌影响：
   - 停牌导致 K 线缺失 → 使用 suspend_merge_logic = True 时，复牌后首根 K 线与停牌前合并计算
   - 防止笔的时间跨度失真

4. T+1 影响：
   - BSD 止损无法当日执行 → 需要预埋止损单
   - 1Buy 风险最大（反转不确定性高），建议仓位最小（Kelly 四分之一）
```

---

> 文件：OBJECT_CARD_CHZL_BSD_P0_E__Chanlun_Buy_Sell_Signals_v1.0.md  
> 生产者：Kimi  
> 状态：已冻结核心字段，待代码实现
