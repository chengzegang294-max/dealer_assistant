# MFLOW_P0_A — 资金流向因子（Money Flow）对象卡

> 功能层：P0_A（选股层 / 过滤器）  
> 成熟度：proxy_quantizable_now（需要 Wind 资金流向数据，A 股已普及）  
> 生产者：Kimi（基于 SBKT_F014 + GLM_DELIVERY_09 提取）  
> 来源：华泰证券《多因子系列 7：单因子测试之资金流向因子》  
> 状态：已冻结核心字段，待代码实现

---

## 1. 基本定义

资金流向因子（Money Flow）基于 A 股特有的 **委托流数据**（小单/中单/大单/超大单），通过统计主动买入/卖出的力量对比，识别主力资金动向。

**核心洞察**：在 A 股，散户（小单）和机构（大单/超大单）的行为模式截然不同。当 KD MTF 发出买入信号时，如果主力在流出，则信号可能是"诱多"。

**SBKT_F014 固化结论**：
- 50 个 Wind 资金流向因子按 8 类分类 → 后 4 类无效 → 前 4 类有效 → 收缩为 **2 个核心因子**
- 持仓约 10 个交易日，2018/03 后样本外待核
- T+1 开盘信号受限（早盘数据不完整）

---

## 2. 核心概念与字段冻结

### 2.1 基础字段（原始数据输入）

```text
mflow_sellord               FLOAT   -- 主力流出单数（mfd_sellord）：
                                        -- 统计大单+超大单卖出笔数占比
                                        -- 负向因子：值越高，预示主力出逃，后市下跌概率大
                                        -- SBKT_F014 核心结论：多空组合年化收益 42.12%，夏普 4.43
mflow_buyord                FLOAT   -- 主力流入单数（mfd_buyord）：
                                        -- 统计大单+超大单买入笔数占比
                                        -- 正向因子：值越高，主力吸筹，后市上涨概率大
mflow_volinflowrate_open    FLOAT   -- 开盘主力净流入率（mfd_volinflowrate_open_m）：
                                        -- 集合竞价阶段(9:25-9:30)资金净流入占全天比例
                                        -- 反映早盘意图，IC>0 占比 81.05%，IR=0.78
                                        -- 正向因子：早盘抢筹明显 → 当日强势概率高
mflow_total_volume          BIGINT  -- 当日总成交量
mflow_large_sell_amount     FLOAT   -- 大单卖出金额（>100万）
mflow_large_buy_amount      FLOAT   -- 大单买入金额（>100万）
mflow_net_inflow            FLOAT   -- 净流入 = 大单买入金额 - 大单卖出金额
```

### 2.2 派生字段（计算后）

```text
mflow_sellord_ratio         FLOAT   -- 主力流出单数占比 = mflow_sellord / 总成交单数
                                        -- 阈值：> 0.6 视为"主力出逃"，< 0.3 视为"主力吸筹"
mflow_inflow_ratio          FLOAT   -- 净流入占比 = mflow_net_inflow / 总成交额
                                        -- 阈值：> 0.05 视为"显著流入"，< -0.05 视为"显著流出"
mflow_open_intent           ENUM    -- 早盘意图：
                                        -- 'STRONG_BUY' = 开盘净流入率 > 0.10（抢筹）
                                        -- 'MODERATE_BUY' = 0.05 ~ 0.10
                                        -- 'NEUTRAL' = -0.05 ~ 0.05
                                        -- 'MODERATE_SELL' = -0.10 ~ -0.05
                                        -- 'STRONG_SELL' = < -0.10（抛售）
mflow_divergence_score      FLOAT   -- 资金流向背离评分（0.0-1.0）：
                                        -- 价格创新高但 mflow_inflow_ratio 下降 → 背离评分高（危险）
                                        -- 价格创新低但 mflow_inflow_ratio 上升 → 背离评分高（机会）
```

### 2.3 信号字段（已冻结）

```text
mflow_signal_type           ENUM    -- 资金流向信号：
                                        -- 'NONE' = 无信号
                                        -- 'MAIN_FORCE_OUT' = 主力出逃（KD 买入时拒绝入场）
                                        -- 'MAIN_FORCE_IN' = 主力吸筹（增强 KD 买入信号）
                                        -- 'OPEN_RUSH_BUY' = 早盘抢筹（增强突破信号）
                                        -- 'OPEN_DUMP_SELL' = 早盘抛售（减弱做多信号）
                                        -- 'DIVERGENCE_WARN' = 资金流向背离（价格与资金方向相反）
mflow_signal_strength       INT(0-10)   -- 信号强度：
                                        -- 主力流出 + 价格上涨 = 10（最高警告）
                                        -- 主力流入 + 价格下跌 = 8（抄底机会）
                                        -- 早盘抢筹 + 价格突破 = 7（增强信号）
mflow_kd_filter_action      ENUM    -- 对 KD MTF 信号的操作：
                                        -- 'PASS' = 通过，不影响
                                        -- 'ENHANCE' = 增强（主力流入时）
                                        -- 'DOWNGRADE' = 降级（主力流出时）
                                        -- 'BLOCK' = 阻断（主力大幅流出时）
                                        -- 'REVERSE' = 反向（仅用于极端背离时）
```

---

## 3. 计算逻辑（伪代码）

### 3.1 核心因子计算

```python
def calculate_money_flow_factors(raw_data):
    """
    计算资金流向因子
    
    参数:
        raw_data: DataFrame with [mfd_sellord, mfd_buyord, mfd_volinflowrate_open_m, 
                                     total_volume, large_sell_amount, large_buy_amount,
                                     total_amount, close, open]
    
    返回:
        dict with mflow_* fields
    """
    # 1. 主力流出单数占比
    mflow_sellord_ratio = raw_data['mfd_sellord'] / (raw_data['mfd_sellord'] + raw_data['mfd_buyord'])
    
    # 2. 净流入占比
    mflow_net_inflow = raw_data['large_buy_amount'] - raw_data['large_sell_amount']
    mflow_inflow_ratio = mflow_net_inflow / raw_data['total_amount']
    
    # 3. 早盘意图
    open_rate = raw_data['mfd_volinflowrate_open_m']
    if open_rate > 0.10:
        mflow_open_intent = 'STRONG_BUY'
    elif open_rate > 0.05:
        mflow_open_intent = 'MODERATE_BUY'
    elif open_rate > -0.05:
        mflow_open_intent = 'NEUTRAL'
    elif open_rate > -0.10:
        mflow_open_intent = 'MODERATE_SELL'
    else:
        mflow_open_intent = 'STRONG_SELL'
    
    # 4. 资金流向背离（价格 vs 资金）
    price_change = (raw_data['close'] - raw_data['open']) / raw_data['open']
    if price_change > 0 and mflow_inflow_ratio < 0:
        # 价格上涨但资金流出 → 背离
        mflow_divergence_score = min(1.0, abs(price_change) * 10 + abs(mflow_inflow_ratio) * 5)
    elif price_change < 0 and mflow_inflow_ratio > 0:
        # 价格下跌但资金流入 → 背离（抄底机会）
        mflow_divergence_score = min(1.0, abs(price_change) * 10 + mflow_inflow_ratio * 5)
    else:
        mflow_divergence_score = 0.0
    
    return {
        'mflow_sellord_ratio': round(mflow_sellord_ratio, 4),
        'mflow_inflow_ratio': round(mflow_inflow_ratio, 4),
        'mflow_open_intent': mflow_open_intent,
        'mflow_divergence_score': round(mflow_divergence_score, 4),
    }
```

### 3.2 信号生成

```python
def generate_mflow_signal(factors, kd_signal, price_action):
    """
    基于资金流向生成信号，并决定对 KD MTF 的操作
    
    参数:
        factors: calculate_money_flow_factors 的输出
        kd_signal: KD MTF 当前信号（如 'PERFECT_LONG'）
        price_action: 价格行为（是否创新高/低）
    """
    sellord_ratio = factors['mflow_sellord_ratio']
    inflow_ratio = factors['mflow_inflow_ratio']
    divergence = factors['mflow_divergence_score']
    
    # 默认：不影响 KD 信号
    signal_type = 'NONE'
    signal_strength = 0
    filter_action = 'PASS'
    
    # 1. 主力大幅出逃（危险信号）
    if sellord_ratio > 0.6 and inflow_ratio < -0.05:
        signal_type = 'MAIN_FORCE_OUT'
        signal_strength = 10
        filter_action = 'BLOCK'  # 阻断 KD 买入信号
    
    # 2. 主力吸筹（增强信号）
    elif sellord_ratio < 0.3 and inflow_ratio > 0.05:
        signal_type = 'MAIN_FORCE_IN'
        signal_strength = 8
        if 'LONG' in kd_signal:
            filter_action = 'ENHANCE'
    
    # 3. 早盘抢筹（增强突破）
    elif factors['mflow_open_intent'] == 'STRONG_BUY' and price_action.get('is_breakout'):
        signal_type = 'OPEN_RUSH_BUY'
        signal_strength = 7
        filter_action = 'ENHANCE'
    
    # 4. 资金流向背离
    elif divergence > 0.7:
        signal_type = 'DIVERGENCE_WARN'
        signal_strength = 9
        if 'LONG' in kd_signal and inflow_ratio < 0:
            # KD 看多但资金流出 → 降级为观察
            filter_action = 'DOWNGRADE'
    
    return {
        'mflow_signal_type': signal_type,
        'mflow_signal_strength': signal_strength,
        'mflow_kd_filter_action': filter_action,
    }
```

---

## 4. 与现有指标的互锁逻辑（已冻结）

### 4.1 与 KD MTF 的互锁

```text
互锁规则 MFLOW × KD MTF：

1. KD MTF 买入信号时的资金过滤：
   - KD 发出 PERFECT_LONG 且 mflow_signal_type = 'MAIN_FORCE_OUT' → BLOCK（阻断入场）
   - KD 发出 PERFECT_LONG 且 mflow_signal_type = 'MAIN_FORCE_IN' → ENHANCE（信号增强）
   - KD 发出 PERFECT_LONG 且 mflow_signal_type = 'DIVERGENCE_WARN' → DOWNGRADE（降级为观察）

2. KD 极端区与资金流向的共振：
   - kd_week_extreme_zone = 'OVERBOUGHT' + mflow_inflow_ratio > 0.10 → 双重警告，强制减仓
   - kd_week_extreme_zone = 'OVERSOLD' + mflow_inflow_ratio < -0.10 → 双重警告，但可能是抄底机会（需谨慎）

3. 早盘意图与 KD 锁仓：
   - mflow_open_intent = 'STRONG_BUY' 且 lock_signal = 'locked' → 早盘抢筹 + 多周期确认 = 高概率机会
   - mflow_open_intent = 'STRONG_SELL' 且 lock_signal = 'locked' → 早盘抛售 + 多周期确认 = 高概率危险
```

### 4.2 与 Volty 的互锁

```text
互锁规则 MFLOW × VOLTY：

1. 高波动期资金流向：
   - volty_trend_state = 'expansion' + mflow_inflow_ratio > 0.05 → 放量突破 + 资金流入 = 高概率趋势启动
   - volty_trend_state = 'expansion' + mflow_inflow_ratio < -0.05 → 放量下跌 + 资金流出 = 恐慌性抛售

2. 资金流向与 Volty 止损的协同：
   - 若 mflow_signal_type = 'MAIN_FORCE_OUT' 且价格接近 volty_up_stop → 提前触发减仓（不等止损）
```

### 4.3 与 VP 的互锁

```text
互锁规则 MFLOW × VP：

1. VP 突破时的资金确认：
   - VP VA_BREAKOUT_LONG + mflow_inflow_ratio > 0.05 → 突破有资金支撑，信号增强
   - VP VA_BREAKOUT_LONG + mflow_inflow_ratio < -0.05 → 假突破（无资金支撑），信号降级

2. POC 回归时的资金背离：
   - 价格回归 POC + mflow_inflow_ratio > 0 → 资金在 POC 附近吸筹 → 支撑确认
   - 价格回归 POC + mflow_inflow_ratio < 0 → 资金在 POC 附近派发 → 支撑可能失效
```

### 4.4 与缠论 BSD 的互锁

```text
互锁规则 MFLOW × CHZL_BSD：

1. 1Buy 时的资金确认：
   - BSD 1Buy + mflow_inflow_ratio > 0.05 → 背驰反转有资金确认，可靠性高
   - BSD 1Buy + mflow_inflow_ratio < -0.05 → 背驰反转无资金确认，可能是假反转

2. 3Buy 时的资金增强：
   - BSD 3Buy + mflow_open_intent = 'STRONG_BUY' → 离开中枢后早盘抢筹 = 趋势加速确认
```

---

## 5. 失效模式（已冻结）

```text
MFLOW 失效条件：

1. 数据缺失：
   - Wind 资金流向数据缺失（某些小盘股或 ST 股无数据）→ mflow_signal_type = 'NONE'
   - 数据延迟（T+1 公布龙虎榜）→ 仅用于选股层，不用于实时执行层

2. 极端行情：
   - 涨停/跌停时资金流向数据失真（大单被价格限制扭曲）→ 标记为 'market_halt'，不生成信号
   - 连续一字板时无有效成交 → 资金流向数据无意义

3. 大单对倒：
   - 庄家大单对倒制造"主力流入"假象 → 与 VP 的 volume_integrity_score 结合过滤
   - volume_integrity_score < 0.6 时，mflow 信号降级

4. 北向资金 vs 内资割裂：
   - 北向资金流入但内资流出 → 信号冲突，以 mflow（内资）为准（A 股内资主导）
```

---

## 6. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | Wind 资金流向数据（50 个因子）或同花顺/东方财富 Level-1 资金流向 |
| **计算复杂度** | 低（简单统计和比率计算） |
| **实时性能** | 日频更新即可，开盘 9:30 后首笔数据可用 |
| **回测可行性** | 高（Wind 有历史资金流向数据） |
| **A 股落地** | 可直接落地（数据源普及） |
| **外汇/期货/币圈落地** | 不可用（外汇无"主力/散户"概念） |
| **跨周期** | 日频为主，分钟级需付费数据 |

---

> 文件：OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md  
> 生产者：Kimi  
> 状态：已冻结核心字段，待代码实现
