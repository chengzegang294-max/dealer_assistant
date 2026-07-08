# 缠论全核心概念量化公式（GLM 交付版）

> 制作人：GLM
> 格式化入库：Kimi
> 来源任务：`GLM_TASK_04_CHANLUN_FULL_QUANT_FORMULA.md`
> 交付时间：2026-06-19
> 版本：v1.0
> 状态：工程级交付，可直接交给程序员实现

---

## 交付概览

本方案在已完成的 `CHZL_ZS` (中枢) 基础上，补全了分型、笔、背驰及买卖点的量化逻辑，并提供了完整的字段定义与测试案例。

| 对象 | 原成熟度 | 升级后成熟度 | 关键交付物 |
|------|---------|------------|----------|
| CHZL_FX（分型） | 只读概念 | **已摘公式** | 包含处理算法 + 分型识别 + 强度评分 |
| CHZL_BI（笔） | needs_extra_data | **已摘公式** | 旧笔规则画线算法 + 字段冻结表 |
| CHZL_BC（背驰） | shell_only | **已摘公式** | MACD面积计算 + confidence过滤 |
| CHZL_BSD（买卖点） | shell_only | **known_input_output** | 一/二/三类触发条件 + 止损位 |
| CHZL_ZS（中枢） | 只读概念 | **known_input_output** | 已完成（见单独文件） |

---

## 1. CHZL_FX (分型)：地基构建

分型是缠论的最小原子单位，其核心在于**K线包含处理**后的形态识别。

### 1.1 K线包含处理算法

*目的：消除毛刺，标准化价格序列。*

```python
FUNCTION Process_Inclusion(bars):
    # 输入：原始 OHLC 列表
    # 输出：标准化后的 Bar 列表
    
    processed = []
    
    FOR i FROM 0 TO len(bars)-1:
        curr = bars[i]
        
        IF processed IS EMPTY:
            ADD curr TO processed
            CONTINUE

        prev = processed[-1]
        
        # 1. 判断是否存在包含关系
        is_inclusion = (curr.high <= prev.high AND curr.low >= prev.low) OR \
                       (curr.high >= prev.high AND curr.low <= prev.low)
                       
        IF is_inclusion:
            # 2. 决定趋势方向
            trend_up = True
            IF len(processed) >= 2:
                if processed[-1].close > processed[-2].close:
                    trend_up = True
                else:
                    trend_up = False
            
            # 3. 合并K线
            new_bar = {}
            IF trend_up:
                new_bar.high = MAX(curr.high, prev.high)
                new_bar.low  = MAX(curr.low, prev.low)
            ELSE:
                new_bar.high = MIN(curr.high, prev.high)
                new_bar.low  = MIN(curr.low, prev.low)
            
            new_bar.time = curr.time
            new_bar.close = curr.close
            
            processed[-1] = new_bar
        ELSE:
            ADD curr TO processed
            
    RETURN processed
```

### 1.2 分型识别与强度评分

| 字段 | 内容 |
|------|------|
| **object_id** | CHZL_FX |
| **input_requirement** | 经过包含处理的 OHLC 序列 |
| **logic_pseudo_code** | `IF (Bar[i-1].High > Bar[i].High AND Bar[i-1].Low < Bar[i].Low) THEN TOP_FX`<br>`IF (Bar[i-1].High < Bar[i].High AND Bar[i-1].Low > Bar[i].Low) THEN BOT_FX` |
| **strength_score** | **强/弱**：<br>1. **强顶分型**：中间K线有长上影线，或存在 Gap。<br>2. **弱分型**：三根K线实体极小，呈星线排列。 |
| **output_form** | `{type: enum(TOP/BOT/NONE), index: int, price: float, strength: int}` |

---

## 2. CHZL_BI (笔)：骨架搭建

基于分型序列，构建具有方向性的最小结构单元。

### 2.1 笔的量化公式 (推荐：旧笔规则)

```python
FUNCTION Detect_Bi(fx_sequence):
    # 输入：CHZL_FX 序列
    # 输出：Bi List
    bi_list = []
    
    i = 0
    WHILE i < len(fx_sequence):
        fx_curr = fx_sequence[i]
        
        IF bi_list IS EMPTY:
             ADD_TO_BI_TEMP(fx_curr)
        ELSE:
            last_bi = bi_list[-1]
            last_fx = last_bi.end_fx
            
            # 规则 1：方向必须相反
            is_opposite = (last_bi.direction == 'UP' AND fx_curr.type == 'TOP') OR \
                          (last_bi.direction == 'DOWN' AND fx_curr.type == 'BOT')
                          
            IF is_opposite:
                # 规则 2：旧笔规则 - 顶底之间必须有独立K线
                kbars_between = COUNT_BARS_BETWEEN(last_fx.index, fx_curr.index)
                
                IF kbars_between >= 2:
                    NEW_BI = {
                        start: last_fx,
                        end: fx_curr,
                        direction: OPPOSITE(last_bi.direction),
                        high: MAX(last_fx.price, fx_curr.price),
                        low: MIN(last_fx.price, fx_curr.price),
                        length_bars: fx_curr.index - last_fx.index
                    }
                    ADD bi_list NEW_BI
        
        i += 1
    RETURN bi_list
```

### 2.2 字段冻结表

| 字段名 | 类型 | 说明 | 枚举值/范围 |
| :--- | :--- | :--- | :--- |
| **bi_id** | INT | 笔的唯一 ID | Auto Inc |
| **direction** | ENUM | 方向 | UP / DOWN |
| **start_idx** | INT | 起始分型索引 | |
| **end_idx** | INT | 结束分型索引 | |
| **start_price** | FLOAT | 起始价 | |
| **end_price** | FLOAT | 结束价 | |
| **high** | FLOAT | 笔内最高价 | |
| **low** | FLOAT | 笔内最低价 | |
| **status** | ENUM | 状态 | CONFIRMED (已成笔), PENDING (未确认/进行中) |

---

## 3. CHZL_BC (背驰)：能量衰竭检测

利用 MACD 面积比较来识别动能不足。

### 3.1 MACD 面积计算与背驰逻辑

```python
FUNCTION Check_Divergence(current_bi, history_bi_list, macd_data):
    # 输入：当前笔，历史笔列表，MACD 数据
    # 输出：bc_flag, confidence
    
    prev_same_dir_bi = FIND_PREV_SAME_DIRECTION_BI(history_bi_list, current_bi.direction)
    
    IF prev_same_dir_bi IS None:
        RETURN {flag: NONE, conf: 0}
        
    area_c = CALC_AREA(macd_data, current_bi.start_idx, current_bi.end_idx)
    area_a = CALC_AREA(macd_data, prev_same_dir_bi.start_idx, prev_same_dir_bi.end_idx)
    
    price_new_high = (current_bi.direction=='UP' AND current_bi.high > prev_same_dir_bi.high)
    price_new_low = (current_bi.direction=='DOWN' AND current_bi.low < prev_same_dir_bi.low)
    
    bc_flag = 'NONE'
    confidence = 0.0
    
    IF current_bi.direction == 'UP':
        IF price_new_high AND area_c < area_a:
            bc_flag = 'TOP_DIVERGENCE'
            confidence = 1 - (area_c / area_a)
    ELSE:
        IF price_new_low AND area_c < area_a:
            bc_flag = 'BOT_DIVERGENCE'
            confidence = 1 - (area_c / area_a)

    # "背了又背" 防护：confidence < 0.30 视为噪音
    IF confidence < 0.30: 
        bc_flag = 'NONE' 
        
    RETURN {flag: bc_flag, conf: confidence}
```

### 3.2 字段冻结表

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| **bc_flag** | ENUM | divergence_top, divergence_bottom, none |
| **bc_area_a** | FLOAT | a 段 MACD 面积 |
| **bc_area_c** | FLOAT | c 段 MACD 面积 |
| **bc_ratio** | FLOAT | c/a 比值 |
| **bc_confidence** | FLOAT | 0-1，confidence < 0.30 过滤 |
| **bc_level** | ENUM | 建议只在大级别使用（day, 4h） |

---

## 4. CHZL_BSD (三类买卖点)：执行触发器

基于中枢(ZS)、笔(BI)和背驰(BC)的综合决策点。

### 4.1 买卖点判定逻辑

| 类型 | 定义 | 触发条件 | 止损位 |
| :--- | :--- | :--- | :--- |
| **1Buy / 1Sell** | 转折点 | `chzl_bc_flag == BOT_DIVERGENCE` (或 TOP)<br>AND `bi_direction` 发生反转 | 分型极端值外侧 |
| **2Buy / 2Sell** | 回调不破 | `price_retraces_to_prev_fx_area`<br>AND `NOT_breaking_prev_extreme`<br>AND `kd_signal_supports` | 前 1Buy 低点下方 |
| **3Buy / 3Sell** | 离开中枢回踩 | `price_leaves_zs` (Break Out)<br>AND `price_returns_to_zs_edge_but_not_enter`<br>AND `zs_state == BROKEN_UP/DOWN` | 中枢内部边缘 (ZG/ZD) |

### 4.2 字段冻结表

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| **bsd_type** | ENUM | 1B, 1S, 2B, 2S, 3B, 3S, NONE |
| **trigger_price** | FLOAT | 触发入场价 |
| **stop_loss_price** | FLOAT | 建议止损价 |
| **validity** | BOOL | 是否依然有效 |

---

## 5. 完整字段映射与 SQL 视图

### 5.1 融合视图设计

```sql
CREATE VIEW v_chanlun_kd_lock AS
SELECT 
    t.date,
    t.close,
    -- 1. KD MTF P0 原始字段
    t.kd_week_bias,
    t.kd_day_signal,
    t.kd_alignment_tier,
    t.kd_direction_filter,
    
    -- 2. 缠论结构字段
    fx.type AS fx_type,
    bi.direction AS bi_direction,
    zs.zg, zs.zd, zs.zz, zs.state AS zs_state,
    
    -- 3. 能量与信号
    bc.flag AS bc_flag,
    bsd.type AS bsd_type,
    
    -- 4. 最终互锁信号
    CASE 
        -- Rule 1: 结构破坏优先
        WHEN zs.state IN ('BROKEN_DOWN') AND bsd.type = '3S' THEN 'PERFECT_SHORT'
        WHEN zs.state IN ('BROKEN_UP') AND bsd.type = '3B' THEN 'PERFECT_LONG'
        
        -- Rule 2: 背驰共振
        WHEN t.kd_week_extreme_zone = 'OVERBOUGHT' AND bc.flag = 'TOP_DIVERGENCE' THEN 'FORCE_EXIT_SHORT'
        WHEN t.kd_week_extreme_zone = 'OVERSOLD' AND bc.flag = 'BOT_DIVERGENCE' THEN 'FORCE_EXIT_LONG'
        
        -- Rule 3: 常规信号
        WHEN t.kd_alignment_tier = 's' AND bsd.type IN ('2B', '3B') THEN 'LONG_SIGNAL'
        WHEN t.kd_alignment_tier = 's' AND bsd.type IN ('2S', '3S') THEN 'SHORT_SIGNAL'
        
        -- Rule 4: 噪音过滤
        WHEN t.kd_alignment_tier IN ('conflict', 'b') AND zs.state = 'EXTENDING' THEN 'NOISE_IGNORE'
        
        ELSE 'NEUTRAL'
    END AS lock_signal

FROM ohlc_data t
LEFT JOIN chanlun_fx fx ON t.date = fx.date
LEFT JOIN chanlun_bi bi ON t.date BETWEEN bi.start_date AND bi.end_date
LEFT JOIN chanlun_zs zs ON t.date BETWEEN zs.start_date AND zs.end_date
LEFT JOIN chanlun_bc bc ON bi.id = bc.bi_id
LEFT JOIN chanlun_bsd bsd ON bi.id = bsd.bi_id;
```

---

## 6. MTS 最小可测试数据集 (EURUSD H4)

### 场景设置
*   **资产**: EURUSD
*   **周期**: H4
*   **初始状态**: 下跌趋势中

### 数据流推演表

| 时间 | OHLC (模拟) | CHZL_FX (分型) | CHZL_BI (笔) | CHZL_ZS (中枢) | CHZL_BC (背驰) | CHZL_BSD (买卖点) | Lock Signal (KD=假设共振) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1-T3 | 下跌... | 无 | Bi_1 (Down) | N/A | N/A | N/A | NEUTRAL |
| T4 | 大阳线 | **BOT_FX (底分型)** | Bi_1 End | N/A | N/A | N/A | WATCH |
| T5-T7 | 上涨回调 | 无 | Bi_2 (Up) Start | N/A | N/A | N/A | NEUTRAL |
| T8 | 下跌停顿 | **TOP_FX (顶分型)** | Bi_2 End | N/A | N/A | N/A | NEUTRAL |
| T9-T11 | 再次下跌 | 无 | Bi_3 (Down) | **ZS 形成**<br>ZG=T8.High<br>ZD=T6.Low | N/A | N/A | NOISE_IGNORE (中枢内) |
| T12 | **关键K线** | **BOT_FX (底分型)**<br>(T12.Low > T9.Low) | Bi_3 End | ZS Extending | **BOT_DIVERGENCE**<br>(MACD绿柱缩小) | **2Buy / 类3Buy**<br>(回踩不破ZD) | **PERFECT_LONG**<br>(背驰+中枢支撑+KD金叉) |
| T13-T15 | 暴涨突破 | 无 | Bi_4 (Up) | **BROKEN_UP**<br>(突破ZG) | N/A | **3Buy 确认** | PERFECT_LONG (加仓) |

### 测试断言

1. **断言 1 (分型)**: 在 T12 处，系统必须识别出一个有效的 `BOT_FX`，且该分型的 Low 点高于 T9 的 Low 点（构成类二买结构）。
2. **断言 2 (中枢)**: 在 T11 结束时，`chzl_zhongshu_state` 应为 `EXTENDING`，且 `count` >= 3。
3. **断言 3 (背驰)**: 在 T12 处，虽然价格可能未创 T3 新低（盘整背驰），但 MACD 面积必须显著小于 Bi_1 段面积，触发 `bc_flag`。
4. **断言 4 (互锁)**: 只有当 T12 出现 `BOT_DIVERGENCE` 且 `kd_day_signal=CROSS_UP` 时，才允许输出 `PERFECT_LONG`。否则应为 `NOISE_IGNORE`。

---

## 7. 工程实现优先级建议

```
Phase 1: FX (分型) — 地基，必须先冻结
    ↓
Phase 2: BI (笔) — 基于 FX，是中枢的前提
    ↓
Phase 3: ZS (中枢) — 基于 BI，已完成（见 CHZL_ZS 文件）
    ↓
Phase 4: BC (背驰) — 基于 ZS + MACD
    ↓
Phase 5: BSD (买卖点) — 基于 ZS + BC + 回踩动作
    ↓
Phase 6: SQL VIEW (融合视图) — 最终交付
```

---

> **交付说明**：以上内容涵盖了从底层原子（分型）到顶层决策（Lock Signal）的全部逻辑。建议开发顺序为：FX -> BI -> ZS -> BC -> BSD -> VIEW。
