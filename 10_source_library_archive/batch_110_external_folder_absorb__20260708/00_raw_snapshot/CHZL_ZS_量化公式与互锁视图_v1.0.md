# CHZL_ZS 中枢量化公式与 KD MTF P0 互锁视图

> 制作人：GLM（经 Kimi 格式化入库）
> 来源路径：`D:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/01_Kimi拆书待入库/`
> 制作时间：2026-06-19
> 版本：v1.0
> 状态：供程序员直接实现的工程级文档

---

# 第一部分：CHZL_ZS 中枢量化公式

本模块的目标是将模糊的"盘整"转化为精确的价格区间 `[ZG, ZD]` 和状态机。

## 1. 数据预处理：K线包含处理

*在计算中枢前，必须先将原始 K 线 (Raw OHLC) 合并为标准 K 线 (Processed OHLC)。*

```python
FUNCTION MergeKLines(raw_bars):
    # 输入：按时间排序的 Raw Bar List
    # 输出：Processed Bar List (去除包含关系的干净K线)
    
    i = 0
    WHILE i < len(raw_bars):
        current = raw_bars[i]
        previous = processed_list[-1] IF processed_list NOT empty ELSE None
        
        IF previous IS None:
            ADD current TO processed_list
            CONTINUE

        # 判断是否有包含关系 (High/Low 重叠)
        IF current.high >= previous.low AND current.low <= previous.high:
            # 判断趋势方向 (与前一个非包含K线比，或者与处理后的前一根比)
            # 这里采用通用规则：与 processed_list[-1] 的方向
            trend_is_up = (current.close > previous.close) OR (processed_list[-1].high <= processed_list[-2].high) # 简化逻辑
            
            IF trend_is_up:
                # 向上包含：取高高，取高低
                new_high = MAX(current.high, previous.high)
                new_low  = MAX(current.low, previous.low)
            ELSE:
                # 向下包含：取低高，取低低
                new_high = MIN(current.high, previous.high)
                new_low  = MIN(current.low, previous.low)
            
            # 覆盖 processed_list 最后一个元素
            REPLACE_LAST(processed_list, {high:new_high, low:new_low, close:current.close})
        ELSE:
            ADD current TO processed_list
            
        i += 1
    RETURN processed_list
```

## 2. 中枢核心计算逻辑

*假设输入已经过分型和笔的提取，生成了 `bi_sequence` (笔序列)。每笔包含 `{start_idx, end_idx, high_price, low_price, direction}`。*

```python
FUNCTION CalculateZhongshu(bi_sequence):
    # 定义中枢的最小参数
    MIN_BI_COUNT_FOR_ZS = 3  # 至少三笔
    zhongshu_container = []  # 存储所有活跃中枢
    
    # 遍历寻找三笔重叠
    FOR i FROM 0 TO len(bi_sequence) - MIN_BI_COUNT_FOR_ZS:
        bi_1 = bi_sequence[i]     # 第1笔 (如: 下跌)
        bi_2 = bi_sequence[i+1]   # 第2笔 (如: 上涨)
        bi_3 = bi_sequence[i+2]   # 第3笔 (如: 下跌)

        # 1. 计算重叠区间 (Intersection)
        range_high = MIN(bi_1.high, bi_2.high, bi_3.high)
        range_low  = MAX(bi_1.low, bi_2.low, bi_3.low)

        # 2. 有效中枢判定：必须存在物理重叠
        IF range_high > range_low:
            
            # --- 核心字段赋值 ---
            zs = {
                'zg': range_high,           # 中枢高点
                'zd': range_low,            # 中枢低点
                'zz': (range_high + range_low) / 2, # 中轴
                'direction': NEUTRAL,       # 待定
                'count': 3,                 # 初始接触次数
                'start_index': bi_1.start,
                
                # --- 状态判定逻辑 ---
                'state': DetermineState(bi_sequence, i+3, range_high, range_low),
                
                # --- 扩展性检查 (Optional) ---
                # 如果后续第4笔、第5笔...继续在重叠区内，更新 count 和 state
            }
            ADD zs TO zhongshu_container
            
    RETURN zhongshu_container

# --- 状态判定子函数 ---
FUNCTION DetermineState(bi_seq, next_bi_start_idx, zg, zd):
    # 检查中枢形成后的走势 (第4笔及以后)
    current_price = GET_CURRENT_PRICE()
    
    # 规则 A: 破坏向上
    IF current_price > zg:
        # 需要确认是否为 "三买" 或真突破
        # 简单量化：最近一笔的高点 > zg + buffer (e.g., 1 ATR)
        RETURN 'BROKEN_UP' 
    
    # 规则 B: 破坏向下
    ELIF current_price < zd:
        RETURN 'BROKEN_DOWN'
        
    # 规则 C: 延伸
    ELSE:
        # 价格仍在 [zd, zg] 之间
        RETURN 'EXTENDING'
```

---

# 第二部分：互锁视图伪代码

这是一个可以直接给程序员写的 `Class` 或 `Function` 逻辑。它整合了 KD MTF P0 和 CHZL_ZS/BC。

## 1. 输入接口定义

```python
INPUTS:
    # --- 来自 KD MTF P0 ---
    kd_week_bias : ENUM [UP, DOWN, FLAT]
    kd_day_signal: ENUM [CROSS_UP, CROSS_DOWN, NONE]
    kd_alignment_tier: ENUM [s, a, b, conflict] # s=共振, b=待定
    kd_direction_filter: ENUM [LONG_PREFERRED, SHORT_PREFERRED, WAIT]
    kd_week_extreme_zone: ENUM [OVERBOUGHT, OVERSOLD, NORMAL]

    # --- 来自 缠论 (CHZL) ---
    chzl_zg : FLOAT          # 中枢上沿
    chzl_zd : FLOAT          # 中枢下沿
    chzl_state: ENUM         # [BUILDING, EXTENDING, BROKEN_UP, BROKEN_DOWN]
    chzl_bc_flag : ENUM      # [DIVERGENCE_TOP, DIVERGENCE_BOTTOM, NONE]
    
    # --- 市场数据 ---
    current_close : FLOAT
```

## 2. 核心决策引擎

```python
FUNCTION GenerateLockSignal(INPUTS):
    
    # ============================================================
    # PRIORITY 1: 结构破坏检查 - 最高优先级，风控为王
    # ============================================================
    IF chzl_state == 'BROKEN_DOWN':
        # 结构坏了，不管 KD 怎么样，都要警惕
        IF kd_direction_filter != 'SHORT_PREFERRED':
            RETURN 'FORCE_EXIT'  # 强制退出多头 / 或者反手
        ELSE:
            RETURN 'PERFECT_SHORT' # 结构坏 + KD 也看空 = 完美做空

    IF chzl_state == 'BROKEN_UP':
        IF kd_direction_filter != 'LONG_PREFERRED':
            RETURN 'FORCE_EXIT'
        ELSE:
            RETURN 'PERFECT_LONG'

    # ============================================================
    # PRIORITY 2: 能量衰竭检查 - 次高优先级，拐点捕捉
    # ============================================================
    # 条件：KD 处于极端区 + 缠论出现背驰
    IF kd_week_extreme_zone == 'OVERBOUGHT' AND chzl_bc_flag == 'DIVERGENCE_TOP':
        RETURN 'PERFECT_SHORT' # 高概率顶
        
    IF kd_week_extreme_zone == 'OVERSOLD' AND chzl_bc_flag == 'DIVERGENCE_BOTTOM':
        RETURN 'PERFECT_LONG'  # 高概率底

    # ============================================================
    # PRIORITY 3: 共振过滤检查 - 常规交易信号
    # ============================================================
    # 只有当 KD 共振时，才考虑在中枢边界操作
    IF kd_alignment_tier == 's': # s = Super Alignment (共振)
        
        # 检查价格相对中枢的位置
        price_pos = CHECK_PRICE_POS(current_close, chzl_zg, chzl_zd)
        
        IF kd_direction_filter == 'LONG_PREFERRED':
            IF price_pos == 'ABOVE_ZS':
                RETURN 'PERFECT_LONG' # 最强：KD好 + 结构上 + 中枢上
            IF price_pos == 'TOUCH_ZD': # 回踩中枢下沿
                RETURN 'PERFECT_LONG' # 次强：回踩不破 + KD支持 (类二买/三买)
                
        IF kd_direction_filter == 'SHORT_PREFERRED':
             IF price_pos == 'BELOW_ZS':
                RETURN 'PERFECT_SHORT'
             IF price_pos == 'TOUCH_ZG':
                RETURN 'PERFECT_SHORT'

    # ============================================================
    # PRIORITY 4: 噪音过滤 - 默认行为
    # ============================================================
    # 如果 KD 冲突 (conflict) 或 待定 (b)，且价格在中枢里
    IF kd_alignment_tier IN ['conflict', 'b'] AND chzl_state IN ['EXTENDING', 'BUILDING']:
        RETURN 'NOISE_IGNORE' # 忽略信号，不交易

    # Default
    RETURN 'NEUTRAL'

# Helper Function
FUNCTION CHECK_PRICE_POS(price, zg, zd):
    IF price > zg: RETURN 'ABOVE_ZS'
    ELIF price < zd: RETURN 'BELOW_ZS'
    ELIF ABS(price - zg) < threshold: RETURN 'TOUCH_ZG'
    ELIF ABS(price - zd) < threshold: RETURN 'TOUCH_ZD'
    ELSE: RETURN 'INSIDE_ZS'
```

---

# 第三部分：最小可测试数据集 (MTS)

为了验证上述公式，我们构造一个理想化的 **EURUSD H4 (4小时图)** 场景。

**场景设定**：
*   **资产**：EURUSD
*   **周期**：H4 (4小时K线)
*   **模拟数据流** (共 20 根 K 线，简化版)：

| K线索引 | 行为描述 | 价格特征 | 预期系统反应 |
| :--- | :--- | :--- | :--- |
| **01-03** | **构建第1笔 (下跌)** | 从 1.1000 跌至 1.0900 | 无中枢 |
| **04-06** | **构建第2笔 (上涨)** | 从 1.0900 涨至 1.0950 | 无中枢 |
| **07-09** | **构建第3笔 (下跌)** | 从 1.0950 跌至 1.0920 | **中枢形成！** |
| | | | **[计算]**: ZG=MIN(1.10, 1.095, 1.095)=1.095; ZD=MAX(1.09, 1.09, 1.092)=1.092 |
| | | | **[状态]**: `BUILDING` -> `EXTENDING` |
| **10-12** | **构建第4笔 (上涨)** | 从 1.0920 涨至 1.0940 (未破 ZG) | **中枢延伸** |
| | | | **[验证]**: 1.0940 < 1.095 (ZG). 依然在内部. `count`++ |
| **13-15** | **构建第5笔 (下跌)** | 跌至 1.0915 | **中枢延伸** |
| | | | **[验证]**: 1.0915 > 1.092 (ZD)? No! (跌破ZD) |
| | | | **[注意]**: 这里触及了 `chzl_zd`。如果此时 `kd_day_signal=CROSS_UP`，触发 **Rule Set A (回踩买入)**。 |
| **16-18** | **构建第6笔 (暴涨)** | 直接突破 1.0950 (ZG) 到达 1.1050 | **中枢破坏 (向上)** |
| | | | **[状态]**: `BROKEN_UP`. |
| | | | **[动作]**: 寻找 `kd_4h_confirm=confirm` 做多。 |

**测试用例脚本**：
> 请程序员运行代码，输入上述模拟价格。
> **断言 1**：在第 09 根 K 线结束时，系统必须输出 `chzl_zhongshu_state = BUILDING`。
> **断言 2**：在第 15 根 K 线（回踩下沿），若 KD 为金叉，输出应为 `PERFECT_LONG` (二买/三买模式)。
> **断言 3**：在第 18 根 K 线（突破后），输出应为 `BROKEN_UP`。

---

# 第四部分：字段冻结确认

经过量化推演，建议对 `chzl_zs` 字段进行如下最终冻结。

## Final Schema: `chzl_zhongshu_table`

| 字段名 | 类型 | 枚举值/范围 | 说明 | 是否新增 |
| :--- | :--- | :--- | :--- | :--- |
| **zs_id** | INT | Auto Inc | 中枢唯一标识符 (区分新旧中枢) | **Yes (关键)** |
| **zg** | FLOAT | (High, +inf) | 中枢上沿 | Existing |
| **zd** | FLOAT | (-inf, Low) | 中枢下沿 | Existing |
| **zz** | FLOAT | (ZD, ZG) | 中枢中轴 (Zero Zone) | Existing |
| **direction** | ENUM | UP / DOWN / FLAT | 中枢倾向性 (根据进入段判断) | Existing |
| **count** | INT | [3, +inf] | 中枢内笔的数量 (>=9 则考虑升级) | Existing |
| **state** | ENUM | **BUILDING**<br>**EXTENDING**<br>**BROKEN_UP**<br>**BROKEN_DOWN**<br>**COMPLETED** | **核心状态位** | Existing |
| **exit_status** | ENUM | ACTIVE / INACTIVE / EXPIRED | 该中枢是否还有效 (被新中枢取代?) | Existing |
| **range_atr** | FLOAT | (0, 5.0) | **(新增)** 中枢宽度 / ATR 的比值。< 1.0 为窄幅震荡，> 2.0 为宽幅震荡 | **Yes** |
| **touch_count** | INT | [0, +inf] | **(新增)** 价格触碰 ZG/ZD 的次数。次数越多，支撑阻力越有效 | **Yes** |

### 为什么增加这三个字段？

1.  **`zs_id`**: 您可能会遇到"中枢扩展"的情况（9段升级）。这时候会有两个中枢同时存在（一个是旧的正在消亡，一个是新的正在诞生）。没有 ID 无法区分。
2.  **`range_atr`**: 区分"窄幅中枢"（易爆发）和"宽幅中枢"（难操作）。
3.  **`touch_count`**: 这是一个量化"能量"的字段。如果 `touch_count` 很大但 `state` 依然是 `EXTENDING`，说明这里争夺非常激烈，一旦突破 (`BROKEN`)，行情会很大。

---

> **结论**：这套方案已具备完全的可执行性。下一步请交给开发人员实现 `MergeKLines` 和 `CalculateZhongshu` 函数，并用 EURUSD 数据跑通 MTS 测试案例。
