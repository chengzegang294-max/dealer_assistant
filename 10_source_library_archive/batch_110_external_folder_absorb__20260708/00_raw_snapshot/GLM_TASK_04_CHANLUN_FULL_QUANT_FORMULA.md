# GLM 任务指令 04：缠论剩余核心概念量化公式 + KD MTF P0 完整字段映射

> 制作人：Kimi（任务分发）
> 目标：GLM 输出工程级文档，可直接交给程序员实现
> 前置条件：CHZL_ZS（中枢）已完成，见 `CHZL_ZS_量化公式与互锁视图_v1.0.md`
> 输出要求：伪代码 + 字段冻结表 + 最小测试数据集

---

## 任务概述

缠论中枢（CHZL_ZS）的量化公式和与 KD MTF P0 的互锁视图已经完成。现在需要你继续推进缠论剩余的**4个核心概念**，从"地基"到"应用"依次完成：

1. **CHZL_FX（分型）** — 地基，必须先冻结
2. **CHZL_BI（笔）** — 基于分型，是中枢的前提
3. **CHZL_BC（背驰）** — 基于中枢+MACD面积，是买卖点的预警
4. **CHZL_BSD（三类买卖点）** — 基于中枢+背驰，是最终执行触发器

注意：CHZL_XD（线段）本次不处理，标注为 `shell_only`，说明原因即可。

---

## 第一部分：CHZL_FX（分型）量化公式

### 要求

分型是缠论的**最小原子单位**。没有正确的分型，就没有正确的笔，也就没有正确的中枢。

请给出：

1. **K线包含处理算法**（MergeKLines）的完整伪代码
   - 输入：Raw OHLC 序列
   - 输出：Processed OHLC 序列（无包含关系）
   - 规则：
     - 向上趋势（当前K线高点 >= 前一根高点）：向上包含 → 取高高、取高低
     - 向下趋势（当前K线低点 <= 前一根低点）：向下包含 → 取低高、取低低
     - 趋势判断：与前一根处理后的K线比较 close 或 high/low

2. **顶底分型识别算法**
   - 输入：Processed K线序列
   - 输出：`enum {top_fractal, bottom_fractal, none}` + `strength_score(0-1)`
   - 规则：
     - 顶分型：中间K线高点最高，且中间K线低点也最高（三根K线，中间最高）
     - 底分型：中间K线低点最低，且中间K线高点也最低（三根K线，中间最低）
     - 强度评分：考虑是否有缺口（gapped）/ 影线长度比例

3. **常见边界条件处理**
   - 连续两根K线都满足分型条件，取哪一个？
   - 分型出现后，后续K线破坏分型（如顶分型后创新高），如何处理？

### 输出格式

```python
# 伪代码格式，可直接给程序员
FUNCTION MergeKLines(raw_bars):
    ...
    
FUNCTION IdentifyFractals(processed_bars):
    ...
    
# 字段冻结表
CHZL_FX:
  - fx_type: enum(top, bottom, none)
  - fx_strength: float(0-1)
  - fx_high: float  # 顶分型高点 / 底分型低点
  - fx_confirm: bool  # 是否被后续K线确认（未被破坏）
  - fx_idx: int  # 分型所在K线索引
```

---

## 第二部分：CHZL_BI（笔）量化公式

### 要求

笔是缠论的**最小结构单位**。一笔 = 一个顶分型 + 一个底分型（或反之），中间至少有一根独立K线。

请给出：

1. **画线算法**
   - 输入：分型序列（CHZL_FX 输出）
   - 输出：`struct {start_idx, end_idx, direction(up/down), length_bars, high, low}`
   - 规则：
     - 顶分型 → 底分型 = 向下笔
     - 底分型 → 顶分型 = 向上笔
     - 两个分型之间**至少有一根独立K线**（旧笔规则）
     - 如果两个分型之间没有独立K线，则合并或跳过

2. **笔的破坏判定**
   - 规则：反向笔突破前一笔的极值（如向下笔跌破前向上笔的低点）
   - 输出：`is_broken(bool) + broken_at_idx(int)`

3. **新旧笔规则选择**
   - 旧笔：顶底分型之间必须有独立K线（严格，推荐）
   - 新笔：允许共用K线（宽松）
   - 请明确推荐**旧笔**，并说明原因（稳定性优先）

### 输出格式

```python
FUNCTION DrawBiLines(fractal_sequence, use_old_rule=True):
    ...
    
FUNCTION CheckBiBroken(current_bi, next_bi):
    ...
    
# 字段冻结表
CHZL_BI:
  - bi_direction: enum(up, down)
  - bi_start_idx: int
  - bi_end_idx: int
  - bi_high: float
  - bi_low: float
  - bi_length_bars: int
  - bi_is_broken: bool
  - bi_broken_at_idx: int
```

---

## 第三部分：CHZL_BC（背驰）量化公式

### 要求

背驰是缠论的**能量衰竭信号**。基于中枢（CHZL_ZS）+ MACD 柱状图面积比较。

请给出：

1. **MACD 面积计算**
   - 输入：价格序列 + MACD 参数（默认 12/26/9）
   - 输出：`macd_area_a(float)` + `macd_area_c(float)` + `bc_flag(enum)`
   - 规则：
     - a 段：进入中枢前的同向笔对应的 MACD 面积
     - c 段：离开中枢后的同向笔对应的 MACD 面积
     - 顶背驰：价格创新高，MACD 面积 c < a
     - 底背驰：价格创新低，MACD 面积 c < a

2. **背驰确认条件**
   - 价格必须创新高/低（突破中枢后）
   - MACD 面积必须缩小
   - 输出 `confidence(0-1)`，基于面积缩小比例

3. **"背了又背"防护**
   - 说明：小级别频繁假背驰的过滤方法
   - 建议：只在日线及以上级别判断背驰，或要求面积缩小比例 > 30%

### 输出格式

```python
FUNCTION CalculateMacdArea(prices, macd_params=(12,26,9), segment_start, segment_end):
    ...
    
FUNCTION DetectBeichi(zhongshu_struct, bi_sequence):
    ...
    
# 字段冻结表
CHZL_BC:
  - bc_flag: enum(divergence_top, divergence_bottom, none)
  - bc_area_a: float
  - bc_area_c: float
  - bc_ratio: float  # c/a 的比值，越小越可靠
  - bc_confidence: float(0-1)
  - bc_level: enum(day, 4h, 1h)  # 建议只在大级别使用
```

---

## 第四部分：CHZL_BSD（三类买卖点）量化公式

### 要求

三类买卖点是缠论的**执行触发器**。基于中枢（CHZL_ZS）+ 背驰（CHZL_BC）+ 回踩动作。

请给出：

1. **第一类买卖点**
   - 定义：背驰点（中枢离开后，背驰确认）
   - 输入：CHZL_BC 输出 + 价格
   - 输出：`buy1_trigger(bool) + price_level(float)`

2. **第二类买卖点**
   - 定义：第一类后，回踩不破前极值（不破中枢 ZG/ZD）
   - 输入：CHZL_ZS + 价格回踩位置
   - 输出：`buy2_trigger(bool) + price_level(float)`

3. **第三类买卖点**
   - 定义：离开中枢后，回踩不回到中枢内部（ZG/ZD 之间）
   - 输入：CHZL_ZS + 价格回踩位置
   - 输出：`buy3_trigger(bool) + price_level(float)`

4. **止损规则**
   - 第一类止损：前一笔极值
   - 第二类止损：中枢 ZG/ZD
   - 第三类止损：中枢 ZG/ZD（或 ZZ 中轴）

### 输出格式

```python
FUNCTION DetectBuySellPoints(zhongshu, beichi, price, bi_sequence):
    ...
    
# 字段冻结表
CHZL_BSD:
  - bsd_type: enum(1buy, 2buy, 3buy, 1sell, 2sell, 3sell, none)
  - bsd_trigger_price: float
  - bsd_stop_loss: float
  - bsd_confidence: float(0-1)
```

---

## 第五部分：CHZL 全体系与 KD MTF P0 完整字段映射

### 要求

不是规则描述，是**SQL/伪代码级别的字段映射**。给出一段可以直接让程序员写的代码：

```sql
-- 缠论数据表
CREATE TABLE chzl_data (
    date TIMESTAMP,
    fx_type ENUM('top','bottom','none'),
    bi_direction ENUM('up','down'),
    zs_state ENUM('building','extending','broken_up','broken_down'),
    bc_flag ENUM('divergence_top','divergence_bottom','none'),
    bsd_type ENUM('1buy','2buy','3buy','1sell','2sell','3sell','none'),
    -- ... 其他字段
);

-- KD MTF P0 数据表（已有）
-- CREATE TABLE kdmft_p0_data (...);

-- 融合视图
CREATE VIEW trade_signal AS
SELECT 
    k.date,
    k.kd_week_bias,
    k.kd_day_signal,
    k.kd_alignment_tier,
    k.kd_direction_filter,
    k.kd_week_extreme_zone,
    c.fx_type,
    c.bi_direction,
    c.zs_state,
    c.bc_flag,
    c.bsd_type,
    
    -- 融合信号
    CASE 
        -- 最高优先级：结构破坏
        WHEN c.zs_state = 'broken_down' AND k.kd_direction_filter != 'short_preferred' THEN 'FORCE_EXIT'
        WHEN c.zs_state = 'broken_up' AND k.kd_direction_filter != 'long_preferred' THEN 'FORCE_EXIT'
        
        -- 次高优先级：极端区+背驰
        WHEN k.kd_week_extreme_zone = 'overbought' AND c.bc_flag = 'divergence_top' THEN 'PERFECT_SHORT'
        WHEN k.kd_week_extreme_zone = 'oversold' AND c.bc_flag = 'divergence_bottom' THEN 'PERFECT_LONG'
        
        -- 常规：共振+结构
        WHEN k.kd_alignment_tier = 's' AND c.bsd_type IN ('2buy', '3buy') AND k.kd_direction_filter = 'long_preferred' THEN 'PERFECT_LONG'
        WHEN k.kd_alignment_tier = 's' AND c.bsd_type IN ('2sell', '3sell') AND k.kd_direction_filter = 'short_preferred' THEN 'PERFECT_SHORT'
        
        -- 噪音
        WHEN k.kd_alignment_tier IN ('conflict','b') AND c.zs_state IN ('building','extending') THEN 'NOISE_IGNORE'
        
        ELSE 'NEUTRAL'
    END AS lock_signal
FROM kdmft_p0_data k
LEFT JOIN chzl_data c ON k.date = c.date;
```

请完善上述 SQL，补充：
1. 所有 CHZL 字段的完整定义（包括 FX、BI、ZS、BC、BSD）
2. `lock_signal` 的所有分支条件（不要有遗漏）
3. 索引建议（哪些字段需要联合索引？）

---

## 第六部分：最小可测试数据集（MTS）

### 要求

提供一个 **EURUSD H4** 或 **某A股日线** 的模拟数据集（20-30根K线），覆盖以下场景：

1. **分型形成**：连续3-5根K线形成顶分型
2. **笔形成**：顶分型 → 底分型 = 向下笔
3. **中枢形成**：3笔重叠（上-下-上）
4. **背驰**：价格创新高，MACD面积缩小
5. **三类买卖点**：至少各出现一次

每根K线标注：
- 价格（OHLC）
- 预期 FX 输出
- 预期 BI 输出
- 预期 ZS 输出
- 预期 BC 输出
- 预期 BSD 输出
- 预期 lock_signal（与 KD MTF P0 融合后）

---

## 约束条件

1. **只输出伪代码和公式**，不要写完整的 Python/MQL4/TradingView 代码
2. **所有条件必须用价格比较**（> < =）、计数（count >= N）或状态枚举，不能用"感觉""大概""可能"
3. **如果某个条件确实无法量化**（如"分型的级别"），标注为 `UNQUANTIZABLE` 并说明原因
4. **明确推荐旧笔规则**（顶底分型之间必须有独立K线）
5. **背驰只建议在大级别使用**（日线/4H），小级别标注为 `UNRELIABLE`

---

## 输出文件命名建议

`GLM_TASK_04_CHANLUN_FULL_QUANT_FORMULA_v1.0.md`

请按上述6个部分组织文档，每个部分有独立的伪代码、字段冻结表和测试断言。
