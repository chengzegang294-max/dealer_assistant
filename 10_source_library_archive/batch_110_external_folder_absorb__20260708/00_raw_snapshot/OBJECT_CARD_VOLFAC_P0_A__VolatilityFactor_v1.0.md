# VOLFAC_P0_A — 波动率因子（Volatility Factor）对象卡

> 功能层：P0_A（选股层 / 过滤器）  
> 成熟度：proxy_quantizable_now（只需日收盘价，基础计算）  
> 生产者：Kimi（基于 SBKT_F006 + GLM_DELIVERY_09 提取）  
> 来源：华泰证券《多因子系列 6：单因子测试之波动率类因子》  
> 状态：已冻结核心字段，待代码实现

---

## 1. 基本定义

波动率因子（Volatility Factor）衡量个股价格的波动程度，是**VolTarget_P0_R**的核心输入参数之一。SBKT_F006 通过系统测试，将 8 个波动率因子收缩为 **2 个非冗余核心因子**。

**SBKT_F006 固化结论**：
- 8 个波动率因子 → 7 个高相关 → 收缩为 **1 代表 + hml_r_std_5m（独立信息源）**
- 样本期 3-5 个月最佳，2017/02 后样本外待核
- **核心组合**：`id2_std_3m`（3 个月收益率标准差）+ `hml_r_std_5m`（5 分钟高频波动率）
- 功能定位：选股层过滤器（剔除高特质波动率个股）

---

## 2. 核心概念与字段冻结

### 2.1 基础字段（原始数据输入）

```text
volfac_close_20d[]    ARRAY<FLOAT>   -- 最近 20 日收盘价
volfac_close_60d[]    ARRAY<FLOAT>   -- 最近 60 日收盘价（用于 3 个月标准差）
volfac_high_5m[]      ARRAY<FLOAT>   -- 最近 5 分钟高频最高价（需 Level-2 或 5min 数据）
volfac_low_5m[]       ARRAY<FLOAT>   -- 最近 5 分钟高频最低价
volfac_close_5m[]     ARRAY<FLOAT>   -- 最近 5 分钟高频收盘价
volfac_intraday_high  FLOAT          -- 当日最高价（用于日内已实现波动率）
volfac_intraday_low   FLOAT          -- 当日最低价
```

### 2.2 核心因子字段（已冻结）

```text
volfac_id2_std_3m     FLOAT   -- 3 个月收益率标准差（id2_std_3m）：
                                -- 过去 60 个交易日的日收益率标准差
                                -- 功能：衡量个股中期波动率水平
                                -- 用法：高值 → 高波动个股 → 剔除或降低权重
                                -- 这是 VolTarget 的核心输入参数

volfac_hml_r_std_5m   FLOAT   -- 5 分钟高频波动率（hml_r_std_5m）：
                                -- 基于 5 分钟 high/low 数据的已实现波动率
                                -- 功能：捕捉日内突发波动，与 id2_std_3m 信息源独立
                                -- 用法：高值 → 日内波动异常 → 日内策略暂停开仓
                                -- 需要 Level-2 或 5min 数据，成本较高

volfac_realized_vol_5m  FLOAT   -- 5 分钟已实现波动率（备选）：
                                  -- 计算公式：sqrt(sum(log_return^2) * 252)
                                  -- 基于 5 分钟对数收益率的平方和
```

### 2.3 派生字段（计算后）

```text
volfac_annualized_vol   FLOAT   -- 年化波动率（核心输出）：
                                    -- = id2_std_3m * sqrt(252)
                                    -- 这是 VolTarget 的 vt_current_vol 输入
                                    -- 也是组合风险管理的基准参数

volfac_vol_percentile   FLOAT   -- 波动率历史分位（0-100）：
                                    -- 当前 id2_std_3m 在过去 1 年中的分位排名
                                    -- > 80% = 高波动（历史上很少如此高）
                                    -- < 20% = 低波动（历史上很少如此低）

volfac_vol_regime       ENUM    -- 波动率状态：
                                    -- 'LOW_VOL' = 低波动（< 20% 分位）
                                    -- 'NORMAL_VOL' = 正常波动（20%-80% 分位）
                                    -- 'HIGH_VOL' = 高波动（> 80% 分位）
                                    -- 'EXTREME_VOL' = 极端波动（> 95% 分位）

volfac_vol_trend        ENUM    -- 波动率趋势：
                                    -- 'EXPANDING' = 波动率上升（id2_std_3m 连续 5 日上升）
                                    -- 'CONTRACTING' = 波动率下降（id2_std_3m 连续 5 日下降）
                                    -- 'STABLE' = 波动率稳定（无明显趋势）
```

### 2.4 信号字段（已冻结）

```text
volfac_filter_action    ENUM    -- 对选股/交易的操作：
                                    -- 'PASS' = 通过，不影响
                                    -- 'REDUCE_WEIGHT' = 降低权重（高波动时）
                                    -- 'EXCLUDE' = 剔除（极端波动时）
                                    -- 'INCREASE_WEIGHT' = 增加权重（低波动时，需结合趋势）

volfac_r8_qualify       BOOL    -- 日内 R8 资格判定：
                                    -- True = 日内波动率正常，允许 TK 策略开仓
                                    -- False = 日内波动率过高（hml_r_std_5m > 阈值），暂停开仓
```

### 2.5 标准输出字段（对象卡统一接口）

所有对象卡必须输出以下统一字段，供上层策略引擎消费：

```text
object_id               STRING  -- 对象卡唯一标识：'VOLFAC_P0_A'
signal_type             ENUM    -- 信号类型：'FILTER'（本卡为过滤器，非方向性信号）
signal_strength         INT     -- 信号强度：-2~+2 离散等级
                                    -- +2 = 强烈建议增加权重（LOW_VOL + STABLE/CONTRACTING）
                                    -- +1 = 建议增加权重（LOW_VOL）
                                    --  0 = 中性（NORMAL_VOL）
                                    -- -1 = 建议降低权重（HIGH_VOL）
                                    -- -2 = 强烈建议剔除（EXTREME_VOL）
confidence              FLOAT   -- 置信度：0.0~1.0
                                    -- 基于数据完整性和历史回测稳定性
                                    -- 1.0 = 数据完整，历史表现稳定
                                    -- <0.5 = 数据缺失或新股，标记为不可靠
lock_status             ENUM    -- 锁定状态：'UNLOCKED' / 'LOCKED'
                                    -- 'UNLOCKED' = 可自由调整
                                    -- 'LOCKED' = 波动率趋势稳定时锁定当前判断
filter_action           ENUM    -- 过滤动作：映射自 volfac_filter_action
                                    -- 'PASS' / 'REDUCE_WEIGHT' / 'EXCLUDE' / 'INCREASE_WEIGHT'
risk_action             ENUM    -- 风险动作：'NONE' / 'HALT_DAY_TRADE' / 'REDUCE_POSITION'
                                    -- 'HALT_DAY_TRADE' = hml_r_std_5m 过高，暂停日内
                                    -- 'REDUCE_POSITION' = EXTREME_VOL 时建议降仓
                                    -- 'NONE' = 无特殊风险动作
size_scalar             FLOAT   -- 仓位缩放系数：0.0~2.0
                                    -- 映射规则：
                                    --   EXTREME_VOL → 0.2
                                    --   HIGH_VOL → 0.5
                                    --   NORMAL_VOL → 1.0
                                    --   LOW_VOL + EXPANDING → 0.8（潜在波动上升）
                                    --   LOW_VOL + STABLE/CONTRACTING → 1.2~1.5
```

**输出字段映射关系**：

| 标准字段 | VOLFAC 内部字段 | 计算/映射逻辑 |
|---------|----------------|--------------|
| object_id | 固定 | `'VOLFAC_P0_A'` |
| signal_type | 固定 | `'FILTER'` |
| signal_strength | volfac_vol_regime + volfac_vol_trend | 见上表映射 |
| confidence | 数据完整性 | 60日数据完整=1.0，<40日=0.3 |
| lock_status | volfac_vol_trend | STABLE 且连续3期同状态 → LOCKED |
| filter_action | volfac_filter_action | 直接映射 |
| risk_action | volfac_hml_r_std_5m + volfac_vol_regime | hml>阈值→HALT_DAY_TRADE；EXTREME→REDUCE_POSITION |
| size_scalar | volfac_vol_regime + volfac_vol_trend | 见上表映射 |
```

```text
volfac_filter_action    ENUM    -- 对选股/交易的操作：
                                    -- 'PASS' = 通过，不影响
                                    -- 'REDUCE_WEIGHT' = 降低权重（高波动时）
                                    -- 'EXCLUDE' = 剔除（极端波动时）
                                    -- 'INCREASE_WEIGHT' = 增加权重（低波动时，需结合趋势）

volfac_r8_qualify       BOOL    -- 日内 R8 资格判定：
                                    -- True = 日内波动率正常，允许 TK 策略开仓
                                    -- False = 日内波动率过高（hml_r_std_5m > 阈值），暂停开仓
```

---

## 3. 计算逻辑（伪代码）

### 3.1 核心因子计算

```python
def calculate_volatility_factors(close_60d, close_5m=None, high_5m=None, low_5m=None):
    """
    计算波动率因子
    
    参数:
        close_60d: 最近 60 日收盘价列表
        close_5m: 最近 5 分钟收盘价列表（可选，需 Level-2）
        high_5m: 最近 5 分钟最高价列表（可选）
        low_5m: 最近 5 分钟最低价列表（可选）
    
    返回:
        dict with volfac_* fields
    """
    import numpy as np
    
    # 1. id2_std_3m: 3 个月收益率标准差
    log_returns = np.log(np.array(close_60d[1:]) / np.array(close_60d[:-1]))
    id2_std_3m = np.std(log_returns)
    
    # 2. 年化波动率
    volfac_annualized_vol = id2_std_3m * np.sqrt(252)
    
    # 3. 历史分位（需要至少 1 年历史数据）
    historical_vol = []  # 过去 1 年的 id2_std_3m 滚动值
    volfac_vol_percentile = percentile(id2_std_3m, historical_vol)
    
    # 4. 波动率状态
    if volfac_vol_percentile > 95:
        volfac_vol_regime = 'EXTREME_VOL'
    elif volfac_vol_percentile > 80:
        volfac_vol_regime = 'HIGH_VOL'
    elif volfac_vol_percentile < 20:
        volfac_vol_regime = 'LOW_VOL'
    else:
        volfac_vol_regime = 'NORMAL_VOL'
    
    # 5. 波动率趋势（简单线性回归）
    recent_vol = [id2_std_3m] + historical_vol[-4:]  # 最近 5 期
    slope = np.polyfit(range(5), recent_vol, 1)[0]
    if slope > 0.001:
        volfac_vol_trend = 'EXPANDING'
    elif slope < -0.001:
        volfac_vol_trend = 'CONTRACTING'
    else:
        volfac_vol_trend = 'STABLE'
    
    # 6. hml_r_std_5m: 5 分钟高频波动率（需 5min 数据）
    volfac_hml_r_std_5m = None
    if close_5m is not None and high_5m is not None and low_5m is not None:
        # 5 分钟已实现波动率
        log_returns_5m = np.log(np.array(close_5m[1:]) / np.array(close_5m[:-1]))
        volfac_hml_r_std_5m = np.std(log_returns_5m) * np.sqrt(48 * 252)  # 48 个 5min/日，年化
    
    return {
        'volfac_id2_std_3m': round(id2_std_3m, 6),
        'volfac_annualized_vol': round(volfac_annualized_vol, 4),
        'volfac_vol_percentile': round(volfac_vol_percentile, 2),
        'volfac_vol_regime': volfac_vol_regime,
        'volfac_vol_trend': volfac_vol_trend,
        'volfac_hml_r_std_5m': round(volfac_hml_r_std_5m, 6) if volfac_hml_r_std_5m else None,
    }
```

### 3.2 过滤决策

```python
def apply_volatility_filter(vol_factors, strategy_type='swing'):
    """
    基于波动率因子对选股/交易进行过滤
    
    参数:
        vol_factors: calculate_volatility_factors 的输出
        strategy_type: 'swing'（波段）/ 'day_trade'（日内）/ 'trend'（趋势）
    
    返回:
        dict with filter_action and r8_qualify
    """
    regime = vol_factors['volfac_vol_regime']
    trend = vol_factors['volfac_vol_trend']
    hml_5m = vol_factors.get('volfac_hml_r_std_5m')
    
    # 默认
    filter_action = 'PASS'
    r8_qualify = True
    
    # 波段策略（日线级别）
    if strategy_type == 'swing':
        if regime == 'EXTREME_VOL':
            filter_action = 'EXCLUDE'  # 极端波动个股不纳入选股池
        elif regime == 'HIGH_VOL':
            filter_action = 'REDUCE_WEIGHT'  # 高波动降低权重
        elif regime == 'LOW_VOL' and trend == 'EXPANDING':
            # 低波动但正在扩大 → 可能是波动率即将上升的转折点
            filter_action = 'PASS'  # 保持观察
    
    # 日内策略（需 5min 数据）
    elif strategy_type == 'day_trade':
        if hml_5m and hml_5m > 0.05:  # 5 分钟波动率阈值
            r8_qualify = False  # 日内波动过高，暂停开仓
        if regime == 'EXTREME_VOL':
            filter_action = 'EXCLUDE'
    
    # 趋势策略
    elif strategy_type == 'trend':
        # 趋势策略偏好低波动但趋势明确的个股
        if regime == 'LOW_VOL' and trend == 'STABLE':
            filter_action = 'INCREASE_WEIGHT'  # 低波动稳定 = 理想趋势标的
        elif regime == 'HIGH_VOL':
            filter_action = 'REDUCE_WEIGHT'  # 高波动趋势股 = 风险大
    
    return {
        'volfac_filter_action': filter_action,
        'volfac_r8_qualify': r8_qualify,
    }
```

---

## 4. 与现有指标的互锁逻辑（已冻结）

### 4.1 与 VOLTARGET 的互锁

```text
互锁规则 VOLFAC × VOLTARGET：

1. VOLFAC 是 VOLTARGET 的核心输入：
   - volfac_annualized_vol → vt_current_vol（VOLTARGET 的当前波动率）
   - volfac_vol_regime → vt_vol_regime（波动率状态映射）
   - volfac_vol_trend → vt_vol_regime 的趋势判断

2. 波动率状态联动：
   - volfac_vol_regime = 'LOW_VOL' → VOLTARGET scalar 可 > 1.0（允许加仓）
   - volfac_vol_regime = 'HIGH_VOL' → VOLTARGET scalar < 1.0（强制降仓）
   - volfac_vol_regime = 'EXTREME_VOL' → VOLTARGET scalar = 0.2（极度保守）

3. 小盘股分层处理：
   - 小盘股（<50亿）的 volfac_annualized_vol 通常 > 50%
   - 小盘股 VOLTARGET target_vol 应提高到 20%（而非默认 10%）
   - 大盘股（>500亿）target_vol 保持 10%
```

### 4.2 与 Volty 的互锁

```text
互锁规则 VOLFAC × VOLTY：

1. Volty 的 ATR 与 VOLFAC 的协同：
   - volty_trend_state = 'expansion' 且 volfac_vol_regime = 'HIGH_VOL' → 双重确认高波动，强制降仓
   - volty_trend_state = 'contraction' 且 volfac_vol_regime = 'LOW_VOL' → 双重确认低波动，允许加仓

2. Volty 翻转与波动率状态：
   - volty_flip_signal = 'bullish_flip' 且 volfac_vol_trend = 'EXPANDING' → 翻转发生在波动扩张期，可能是假翻转
   - volty_flip_signal = 'bullish_flip' 且 volfac_vol_trend = 'CONTRACTING' → 翻转发生在波动收缩期，更可靠
```

### 4.3 与 KD MTF 的互锁

```text
互锁规则 VOLFAC × KD MTF：

1. 高波动期 KD 信号降级：
   - volfac_vol_regime = 'EXTREME_VOL' → 所有 KD 信号强度 -2（高波动噪音大）
   - volfac_vol_regime = 'HIGH_VOL' → lock_signal 要求更严格（只接受 'strong' 对齐）

2. 低波动期 KD 信号升级：
   - volfac_vol_regime = 'LOW_VOL' → KD 信号强度 +1（低波动期信号更可靠）
   - 但 volfac_vol_trend = 'EXPANDING' 时，即使低波动也不升级（可能即将变高波动）
```

### 4.4 与选股层的互锁

```text
互锁规则 VOLFAC × 选股：

1. 选股池波动率分层：
   - 高波动池（volfac_vol_regime = 'HIGH_VOL'）→ 只用于短线/日内策略
   - 中波动池（volfac_vol_regime = 'NORMAL_VOL'）→ 用于波段策略
   - 低波动池（volfac_vol_regime = 'LOW_VOL'）→ 用于趋势/配置策略

2. 与 MFLOW 的协同：
   - 高波动 + 主力流出（MFLOW）→ 双重危险，剔除
   - 低波动 + 主力流入（MFLOW）→ 理想标的，增加权重
```

---

## 5. 失效模式（已冻结）

```text
VOLFAC 失效条件：

1. 数据不足：
   - 60 日收盘价不足 40 个 → id2_std_3m 不可靠，标记为 'insufficient_data'
   - 5 分钟数据缺失 → hml_r_std_5m 为 NULL，不影响 id2_std_3m

2. 连续涨跌停 ATR 失真：
   - 连续涨停/跌停导致 high-low 压缩 → 日收益率标准差被低估
   - 应对：使用 VOLTARGET 的 limit_atr_corrector（剔除涨跌停日）

3. 历史分位数据不足：
   - 新股上市不足 1 年 → 历史分位计算不准
   - 应对：新股使用行业平均波动率作为参考基准

4. 小盘股特殊性：
   - 小盘股（<50亿）波动率天然高，不适用于与大盘股统一阈值
   - 应对：按市值分层处理（大盘股/中盘股/小盘股分别计算分位）
```

---

## 6. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | 日收盘价（已有）+ 可选 5 分钟数据（需 Level-2） |
| **计算复杂度** | 极低（标准差 + 百分位计算） |
| **实时性能** | 日频更新即可，每交易日收盘后计算一次 |
| **回测可行性** | 极高（仅需历史收盘价） |
| **A 股落地** | 可直接落地（id2_std_3m 只需日收盘价） |
| **外汇/期货/币圈落地** | 直接可用（跨市场通用） |
| **跨周期** | 日频（3 个月）+ 可选 5 分钟高频 |

---

> 文件：OBJECT_CARD_VOLFAC_P0_A__VolatilityFactor_v1.0.md  
> 生产者：Kimi  
> 状态：已冻结核心字段，待代码实现
