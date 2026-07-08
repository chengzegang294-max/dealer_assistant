# ATRATIO_P0_A — 主动成交占比（Active Trade Ratio）对象卡

> 功能层：P0_A（选股层 / 过滤器）  
> 成熟度：KEEP_AS_LIMITED_CANDIDATE（仅空头/多空策略可用，A 股纯多头受限）  
> 生产者：Kimi（基于 SBKT_F002 + GLM_DELIVERY_09 提取）  
> 来源：华泰证券《多因子系列 5：单因子测试之主动买卖因子》  
> 状态：已冻结核心字段，A 股纯多头场景下标记为 LIMITED_CANDIDATE

---

## 1. 基本定义

主动成交占比（Active Trade Ratio）基于 **逐笔委托流数据**，通过统计 "主动买入" vs "主动卖出" 的订单特征，识别有信息优势的参与者行为。

**核心洞察**：当买单先于卖单提交时，说明买方更积极，可能拥有信息优势。但 SBKT_F002 的测试结果显示：在 A 股纯多头场景下，该因子**无有效区分能力**，只有在能做空时（如 2015 年股指期货）才有效。

**SBKT_F002 固化结论**：
- 主动买入因子：IC>0 占比 62.47%，IR 仅 0.47，无显著优势
- 主动卖出因子：IC<0 占比 72.38%，IR 0.62，显著性不足
- **核心结论**：A 股纯多头场景下，主动成交占比因子无效，仅作为 LIMITED_CANDIDATE 保留
- 使用场景：空头/多空策略（做空时高主动卖出占比 = 卖出信号）

---

## 2. 核心概念与字段冻结

### 2.1 基础字段（原始数据输入，需 Level-2 逐笔数据）

```text
atratio_buy_order_time[]    ARRAY<TIMESTAMP>  -- 买单委托时间（精确到毫秒）
atratio_sell_order_time[]   ARRAY<TIMESTAMP>  -- 卖单委托时间（精确到毫秒）
atratio_buy_vol[]          ARRAY<INT>        -- 每笔主动买入成交量
atratio_sell_vol[]         ARRAY<INT>        -- 每笔主动卖出成交量
atratio_buy_price[]        ARRAY<FLOAT>      -- 每笔主动买入成交价格
atratio_sell_price[]       ARRAY<FLOAT>      -- 每笔主动卖出成交价格
atratio_total_vol          BIGINT            -- 当日总成交量
atratio_total_amount       FLOAT             -- 当日总成交额
```

### 2.2 核心因子字段（已冻结）

```text
atratio_active_buy_ratio    FLOAT   -- 主动买入占比：
                                        -- 主动买入量 / 总成交量
                                        -- SBKT_F002 结论：IC>0 占比 62.47%，但 IR 仅 0.47
                                        -- 在纯多头场景下无显著预测能力

atratio_active_sell_ratio   FLOAT   -- 主动卖出占比：
                                        -- 主动卖出量 / 总成交量
                                        -- SBKT_F002 结论：IC<0 占比 72.38%，但显著性不足
                                        -- 在空头/多空场景下可能有价值

atratio_time_advantage      FLOAT   -- 时间优势因子：
                                        -- 统计买单先于卖单提交的次数占比
                                        -- 核心洞察：买单先于卖单 = 买方信息优势
                                        -- 但因 A 股只能做多，该信息优势无法直接转化为交易信号

atratio_large_order_ratio   FLOAT   -- 大单主动成交占比：
                                        -- 大单（>100万）主动买入 / 大单总成交
                                        -- 与 MFLOW 的主力流入因子高度相关，但信息源独立
```

### 2.3 派生字段（计算后）

```text
atratio_signal_valid        BOOL    -- 信号是否有效：
                                        -- True = 数据完整，可生成信号
                                        -- False = 数据缺失或纯多头场景，信号无效

atratio_short_qualify       BOOL    -- 是否可用于做空策略：
                                        -- True = 当前市场环境允许做空（如有股指期货权限）
                                        -- False = 纯多头环境，因子不可用

atratio_composite_score     FLOAT   -- 综合评分（-1.0 到 +1.0）：
                                        -- 综合主动买入/卖出/时间优势
                                        -- +1.0 = 极强主动买入（纯多头场景：中性，不交易）
                                        -- -1.0 = 极强主动卖出（纯多头场景：中性，不交易）
                                        -- 仅在 atratio_short_qualify = True 时有效
```

### 2.4 信号字段（已冻结，A 股纯多头下标记为 LIMITED）

```text
atratio_signal_type         ENUM    -- 主动成交信号：
                                        -- 'NONE' = 无信号（纯多头默认）
                                        -- 'STRONG_ACTIVE_BUY' = 强烈主动买入（仅多空策略可用）
                                        -- 'STRONG_ACTIVE_SELL' = 强烈主动卖出（仅空头/多空策略可用）
                                        -- 'TIME_ADVANTAGE_BUY' = 时间优势买入（信息优势方在买方）
                                        -- 'TIME_ADVANTAGE_SELL' = 时间优势卖出（信息优势方在卖方）

atratio_kd_filter_action    ENUM    -- 对 KD MTF 信号的操作：
                                        -- 'PASS' = 通过（默认，纯多头场景）
                                        -- 'BLOCK_BUY' = 阻断买入（强烈主动卖出时，仅做空可用）
                                        -- 'ENHANCE_SHORT' = 增强做空信号（强烈主动卖出时）
```

### 2.5 标准输出字段（对象卡统一接口）

所有对象卡必须输出以下统一字段，供上层策略引擎消费：

```text
object_id               STRING  -- 对象卡唯一标识：'ATRATIO_P0_A'
signal_type             ENUM    -- 信号类型：
                                    -- 'NONE' = A 股纯多头场景默认（因子无效）
                                    -- 'STRONG_ACTIVE_BUY' = 强烈主动买入（仅多空策略）
                                    -- 'STRONG_ACTIVE_SELL' = 强烈主动卖出（仅多空策略）
                                    -- 'TIME_ADVANTAGE_BUY' = 时间优势买入
                                    -- 'TIME_ADVANTAGE_SELL' = 时间优势卖出
signal_strength         INT     -- 信号强度：-2~+2 离散等级
                                    -- 基于 atratio_composite_score 映射：
                                    --   +2 = score > 0.8
                                    --   +1 = score > 0.5
                                    --    0 = |score| <= 0.5 或无信号
                                    --   -1 = score < -0.5
                                    --   -2 = score < -0.8
                                    -- A 股纯多头下固定为 0
confidence              FLOAT   -- 置信度：0.0~1.0
                                    -- A 股纯多头下固定为 0.0（因子无效）
                                    -- 多空环境下基于数据质量：Level-2完整=1.0，部分缺失=0.5
lock_status             ENUM    -- 锁定状态：'UNLOCKED' / 'LOCKED'
                                    -- A 股纯多头下固定为 'UNLOCKED'
filter_action           ENUM    -- 过滤动作：'PASS' / 'BLOCK_BUY'
                                    -- A 股纯多头下固定为 'PASS'
                                    -- 多空环境下：STRONG_ACTIVE_SELL → BLOCK_BUY
risk_action             ENUM    -- 风险动作：'NONE'
                                    -- A 股纯多头下固定为 'NONE'
size_scalar             FLOAT   -- 仓位缩放系数：0.0~1.0
                                    -- A 股纯多头下固定为 1.0（不缩放）
                                    -- 多空环境下可映射为 0.5~1.0
```

**A 股纯多头场景输出固定值**：

```python
# A 股纯多头：ATRATIO 因子无效，输出统一格式的"空信号"
ashare_long_only_output = {
    'object_id': 'ATRATIO_P0_A',
    'signal_type': 'NONE',
    'signal_strength': 0,
    'confidence': 0.0,
    'lock_status': 'UNLOCKED',
    'filter_action': 'PASS',
    'risk_action': 'NONE',
    'size_scalar': 1.0,
    'atratio_signal_valid': False,
    'note': 'A 股纯多头场景下 ATRATIO 因子无效（SBKT_F002 结论）'
}
```

**多空环境输出映射**：

| 标准字段 | ATRATIO 内部字段 | 计算/映射逻辑 |
|---------|----------------|--------------|
| object_id | 固定 | `'ATRATIO_P0_A'` |
| signal_type | atratio_signal_type | 直接映射 |
| signal_strength | atratio_composite_score | score>0.8→+2, >0.5→+1, <-0.5→-1, <-0.8→-2 |
| confidence | 数据完整性 | Level-2完整=1.0，部分缺失=0.5 |
| lock_status | 固定 | `'UNLOCKED'` |
| filter_action | atratio_kd_filter_action | PASS / BLOCK_BUY |
| risk_action | 固定 | `'NONE'` |
| size_scalar | atratio_composite_score | \|score\|>0.7 → 0.5，否则 1.0 |
```

```text
atratio_signal_type         ENUM    -- 主动成交信号：
                                        -- 'NONE' = 无信号（纯多头默认）
                                        -- 'STRONG_ACTIVE_BUY' = 强烈主动买入（仅多空策略可用）
                                        -- 'STRONG_ACTIVE_SELL' = 强烈主动卖出（仅空头/多空策略可用）
                                        -- 'TIME_ADVANTAGE_BUY' = 时间优势买入（信息优势方在买方）
                                        -- 'TIME_ADVANTAGE_SELL' = 时间优势卖出（信息优势方在卖方）

atratio_kd_filter_action    ENUM    -- 对 KD MTF 信号的操作：
                                        -- 'PASS' = 通过（默认，纯多头场景）
                                        -- 'BLOCK_BUY' = 阻断买入（强烈主动卖出时，仅做空可用）
                                        -- 'ENHANCE_SHORT' = 增强做空信号（强烈主动卖出时）
```

---

## 3. 计算逻辑（伪代码）

### 3.1 核心因子计算（需 Level-2 逐笔数据）

```python
def calculate_active_trade_ratio(tick_data, market_type='ashare_long_only'):
    """
    计算主动成交占比因子
    
    参数:
        tick_data: DataFrame with [buy_order_time, sell_order_time, buy_vol, sell_vol, 
                                     buy_price, sell_price, total_vol, total_amount]
        market_type: 'ashare_long_only'（A 股纯多头）/ 'ashare_long_short'（A 股多空）/
                     'forex'（外汇）/ 'futures'（期货）
    
    返回:
        dict with atratio_* fields
    """
    # 1. 主动买入占比
    atratio_active_buy_ratio = tick_data['buy_vol'].sum() / tick_data['total_vol']
    
    # 2. 主动卖出占比
    atratio_active_sell_ratio = tick_data['sell_vol'].sum() / tick_data['total_vol']
    
    # 3. 时间优势因子（买单先于卖单提交的次数占比）
    buy_first_count = (tick_data['buy_order_time'] < tick_data['sell_order_time']).sum()
    atratio_time_advantage = buy_first_count / len(tick_data)
    
    # 4. 大单主动成交占比（>100万）
    large_buy = tick_data[tick_data['buy_vol'] * tick_data['buy_price'] > 1_000_000]
    large_sell = tick_data[tick_data['sell_vol'] * tick_data['sell_price'] > 1_000_000]
    atratio_large_order_ratio = (large_buy['buy_vol'].sum() - large_sell['sell_vol'].sum()) / \
                                 (large_buy['buy_vol'].sum() + large_sell['sell_vol'].sum())
    
    # 5. 综合评分（仅在多空环境下有效）
    atratio_composite_score = 0.0
    atratio_short_qualify = (market_type in ['ashare_long_short', 'forex', 'futures'])
    
    if atratio_short_qualify:
        atratio_composite_score = (
            atratio_active_buy_ratio * 0.3 +
            (1 - atratio_active_sell_ratio) * 0.3 +  # 主动卖出少 = 买入优势
            atratio_time_advantage * 0.2 +
            atratio_large_order_ratio * 0.2
        ) * 2 - 1  # 映射到 [-1, +1]
    
    # 6. 信号类型（纯多头下默认 NONE）
    atratio_signal_type = 'NONE'
    if atratio_short_qualify:
        if atratio_composite_score > 0.7:
            atratio_signal_type = 'STRONG_ACTIVE_BUY'
        elif atratio_composite_score < -0.7:
            atratio_signal_type = 'STRONG_ACTIVE_SELL'
    
    return {
        'atratio_active_buy_ratio': round(atratio_active_buy_ratio, 4),
        'atratio_active_sell_ratio': round(atratio_active_sell_ratio, 4),
        'atratio_time_advantage': round(atratio_time_advantage, 4),
        'atratio_large_order_ratio': round(atratio_large_order_ratio, 4),
        'atratio_composite_score': round(atratio_composite_score, 4),
        'atratio_short_qualify': atratio_short_qualify,
        'atratio_signal_type': atratio_signal_type,
        'atratio_signal_valid': (atratio_short_qualify and abs(atratio_composite_score) > 0.5),
    }
```

### 3.2 过滤决策（A 股纯多头场景）

```python
def apply_atratio_filter(factors, kd_signal, market_type='ashare_long_only'):
    """
    A 股纯多头场景下的过滤决策
    
    核心逻辑：
    - 纯多头下，主动卖出信号无法做空 → 只能阻断买入
    - 但 SBKT_F002 显示阻断买入的有效性不足（IR 仅 0.47）
    - 因此：纯多头下，ATRATIO 不生成任何信号，只作为观察指标
    """
    
    if market_type == 'ashare_long_only':
        # 纯多头：ATRATIO 无效，不干预任何信号
        return {
            'atratio_kd_filter_action': 'PASS',
            'atratio_signal_valid': False,
            'note': 'A 股纯多头场景下，ATRATIO 因子无效（SBKT_F002 结论）',
        }
    
    # 多空/空头场景
    if factors['atratio_signal_type'] == 'STRONG_ACTIVE_SELL':
        return {
            'atratio_kd_filter_action': 'BLOCK_BUY',
            'atratio_signal_valid': True,
            'note': '强烈主动卖出，阻断买入信号',
        }
    elif factors['atratio_signal_type'] == 'STRONG_ACTIVE_BUY':
        return {
            'atratio_kd_filter_action': 'ENHANCE_SHORT',  # 增强做空（反向）
            'atratio_signal_valid': True,
            'note': '强烈主动买入但信号为做空方向（反向增强）',
        }
    
    return {
        'atratio_kd_filter_action': 'PASS',
        'atratio_signal_valid': False,
    }
```

---

## 4. 与现有指标的互锁逻辑（已冻结）

### 4.1 与 KD MTF 的互锁（A 股纯多头）

```text
互锁规则 ATRATIO × KD MTF（A 股纯多头）：

1. 纯多头场景下 ATRATIO 不干预 KD 信号：
   - atratio_signal_valid = False → 无论 KD 发出什么信号，ATRATIO 都不干预
   - atratio_kd_filter_action = 'PASS'（默认）

2. 多空场景下的互锁（未来扩展）：
   - KD PERFECT_LONG + atratio_signal_type = 'STRONG_ACTIVE_SELL' → BLOCK_BUY（阻断买入）
   - KD PERFECT_SHORT + atratio_signal_type = 'STRONG_ACTIVE_BUY' → ENHANCE_SHORT（增强做空）
```

### 4.2 与 MFLOW 的互锁

```text
互锁规则 ATRATIO × MFLOW：

1. 信息互补：
   - MFLOW 基于大单统计（资金流向）
   - ATRATIO 基于逐笔委托时间（信息优势）
   - 两者信息源独立，理论上可互补

2. A 股纯多头下的协同：
   - MFLOW 有效（主力流出可阻断买入）
   - ATRATIO 无效（主动卖出无法做空）
   - 实际使用：只使用 MFLOW，ATRATIO 仅作为观察指标

3. 未来多空场景下的协同：
   - MFLOW 主力流出 + ATRATIO 强烈主动卖出 → 双重确认做空信号
   - MFLOW 主力流入 + ATRATIO 强烈主动买入 → 双重确认做多信号
```

### 4.3 与 VOLFAC 的互锁

```text
互锁规则 ATRATIO × VOLFAC：

1. 高波动期信息质量：
   - volfac_vol_regime = 'EXTREME_VOL' → 逐笔数据噪音大，ATRATIO 信号降级
   - volfac_vol_regime = 'LOW_VOL' → 逐笔数据质量高，ATRATIO 信号更可靠

2. 日内策略的协同：
   - hml_r_std_5m（5分钟波动率）高 → ATRATIO 的逐笔数据可能失真
   - 建议在 volfac_r8_qualify = True（日内波动正常）时，才使用 ATRATIO
```

---

## 5. 失效模式（已冻结）

```text
ATRATIO 失效条件：

1. A 股纯多头限制（核心失效）：
   - 市场类型 = 'ashare_long_only' → ATRATIO 因子无效
   - 原因：SBKT_F002 显示纯多头下 IC 不显著，无法产生有效信号
   - 应对：标记为 LIMITED_CANDIDATE，仅记录数据，不生成交易信号

2. 数据缺失（Level-2 依赖）：
   - 无逐笔委托数据 → 无法计算时间优势因子
   - 无逐笔成交数据 → 无法计算主动买入/卖出占比
   - 应对：atratio_signal_valid = False，不生成信号

3. 极端行情：
   - 涨停/跌停时逐笔数据失真（封单/撤单行为异常）
   - 连续一字板时无有效逐笔成交
   - 应对：标记为 'market_halt'，不生成信号

4. 大单对倒：
   - 庄家通过大单对倒制造"主动买入"假象
   - 与 MFLOW 和 VP 的 volume_integrity_score 结合过滤
   - volume_integrity_score < 0.6 时，ATRATIO 信号降级
```

---

## 6. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | Level-2 逐笔委托/成交数据（需付费） |
| **计算复杂度** | 中（逐笔数据量大，需高效处理） |
| **实时性能** | 需实时逐笔数据，延迟要求 < 100ms |
| **回测可行性** | 中（需历史 Level-2 数据，成本高） |
| **A 股纯多头落地** | **不可落地**（SBKT_F002 结论：无效） |
| **A 股多空落地** | 理论上可落地（需股指期货权限） |
| **外汇/期货落地** | 可直接落地（天然多空市场） |
| **跨周期** | 日内为主（逐笔数据日频无意义） |

---

## 7. 与其他市场对比

| 市场 | 可用性 | 原因 |
|------|--------|------|
| A 股纯多头 | ❌ 不可用 | SBKT_F002 显示纯多头下无效 |
| A 股多空 | ⚠️ 理论上可用 | 需股指期货权限，未实测 |
| 外汇 | ✅ 可用 | 天然多空，双向交易 |
| 期货 | ✅ 可用 | 天然多空，双向交易 |
| 币圈 | ✅ 可用 | 天然多空，双向交易 |

---

> 文件：OBJECT_CARD_ATRATIO_P0_A__ActiveTradeRatio_v1.0.md  
> 生产者：Kimi  
> 状态：已冻结核心字段，A 股纯多头标记为 LIMITED_CANDIDATE，外汇/期货/币圈可用
