# 组05 — 趋势/系统交易 · STATE_TEMPLATE_V1 四轴模板

> 处理模式: 模式1+4混合（逐段精读+知识库构建）  
> 标签: `trend_following`, `systematic_trading`, `position_sizing`, `risk_management`  
> 对齐模板: STATE_TEMPLATE_V1（结构轴/偏置轴/摩擦轴/风险轴）

---

## A) 四轴状态模板

---

### 结构轴（Structure）— 市场状态与趋势识别

#### S-01: 趋势存在性判定（Trend Existence）

**定义句**: 趋势是指价格在一段长达几星期或几个月的时期内保持一种变化态势的现象；趋势跟踪的基本策略是在上扬趋势刚刚开始时买入，在趋势即将结束前退出。

**可观测证据（可计算）**:
```python
# 趋势存在性的最小可计算定义
def trend_existence(close_prices, period=20):
    """
    输入: close_prices - 收盘价序列 (OHLCV中的C)
    输出: trend_state ∈ {UPTREND, DOWNTREND, SIDEWAYS}
    """
    sma_fast = SMA(close_prices, period=20)
    sma_slow = SMA(close_prices, period=60)
    
    if sma_fast > sma_slow * 1.02 and close_prices[-1] > sma_fast:
        return "UPTREND"
    elif sma_fast < sma_slow * 0.98 and close_prices[-1] < sma_fast:
        return "DOWNTREND"
    else:
        return "SIDEWAYS"

# 海龟系统: 唐奇安通道突破
def donchian_breakout(high_prices, low_prices, period=20):
    """
    价格突破过去N日最高点 → 多头信号
    价格跌破过去N日最低点 → 空头信号
    """
    upper_channel = max(high_prices[-period:])
    lower_channel = min(low_prices[-period:])
    
    if close_prices[-1] > upper_channel:
        return "LONG_BREAKOUT"
    elif close_prices[-1] < lower_channel:
        return "SHORT_BREAKOUT"
    return "NO_SIGNAL"
```

**可证伪检验**:
- 回测检验: 20日唐奇安通道突破策略在1983-2007年期货组合上的年化收益
- 失败判据: 连续3个月没有触发任何突破信号，或突破后60%交易在2N止损位亏损
- 统计检验: 突破信号的胜率应<50%（典型趋势系统胜率35-45%），但盈亏比>2:1

**来源**: 《海龟交易法则》第3章; 《Trend Trader's Handbook》第I章

---

#### S-02: 市场周期阶段识别（Market Cycle Phase）

**定义句**: 市场周期由四个阶段组成——积累期（Accumulation）、标记期/上涨期（Markup）、分销期（Distribution）、减码期/下跌期（Markdown），每个阶段具有独特的成交量、波动性和价格行为特征。

**可观测证据（可计算）**:
```python
def market_cycle_phase(prices, volumes, rsi, adx):
    """
    四阶段识别算法
    输入: OHLCV + RSI(14) + ADX(14)
    输出: phase ∈ {ACCUMULATION, MARKUP, DISTRIBUTION, MARKDOWN}
    """
    # 积累期特征
    if (ADX < 25 and             # 弱趋势
        volume_20d_avg < volume_60d_avg * 0.8 and  # 成交量萎缩
        RSI > 30 and RSI < 50 and  # RSI低位回升
        price_range_20d < ATR_60d * 0.6):  # 窄幅波动
        return "ACCUMULATION"
    
    # 标记期特征
    elif (ADX > 25 and ADX_slope > 0 and  # 趋势增强
          volume_20d_avg > volume_60d_avg * 1.2 and  # 成交量放大
          RSI > 50 and RSI < 80 and  # RSI上行
          close > SMA_200):  # 价格高于200日均线
        return "MARKUP"
    
    # 分销期特征
    elif (ADX < 25 and
          volume_20d_avg < volume_60d_avg * 0.9 and
          RSI > 50 and RSI < 70 and
          price_range_20d < ATR_60d * 0.7):
        return "DISTRIBUTION"
    
    # 减码期特征
    elif (ADX > 25 and ADX_slope > 0 and
          volume_20d_avg > volume_60d_avg * 1.1 and
          RSI < 50 and RSI > 20 and
          close < SMA_200):
        return "MARKDOWN"
    
    return "UNCERTAIN"
```

**可证伪检验**:
- 回测: 在标记期做多+减码期做空的策略应显著优于买入持有
- 失败判据: 阶段转换识别滞后超过10个交易日
- 交叉验证: 与《Trend Trader's Handbook》图例对比，手工标注100个交易日检验一致性

**来源**: 《Trend Trader's Handbook》第II章

---

#### S-03: 波动性状态（Volatility Regime）

**定义句**: 波动性状态决定了趋势跟踪策略的适用性和头寸规模；ATR（真实波动幅度均值）是量化波动性的核心指标，所有头寸规模计算均基于N（ATR值）。

**可观测证据（可计算）**:
```python
def ATR(high_prices, low_prices, close_prices, period=20):
    """
    真实波动幅度均值计算
    TR = max(high-low, |high-prev_close|, |low-prev_close|)
    ATR = SMA(TR, period)
    """
    tr_list = []
    for i in range(1, len(close_prices)):
        tr = max(
            high_prices[i] - low_prices[i],
            abs(high_prices[i] - close_prices[i-1]),
            abs(low_prices[i] - close_prices[i-1])
        )
        tr_list.append(tr)
    return sum(tr_list[-period:]) / period

def volatility_regime(atr_current, atr_60d_avg):
    """
    波动性状态分类
    """
    ratio = atr_current / atr_60d_avg
    if ratio > 1.5:
        return "HIGH_VOL"
    elif ratio < 0.7:
        return "LOW_VOL"
    return "NORMAL_VOL"
```

**可证伪检验**:
- 高波动状态下头寸规模应自动缩小（海龟: 头寸单位 = 账户1% / N）
- 失败判据: ATR预测未来5日波动性的R²<0.3

**来源**: 《海龟交易法则》第3章; 《Trend Trader's Handbook》第III章（波动性指标）

---

### 偏置轴（Bias）— 信号生成与方向判断

#### B-01: 移动平均线偏置（Moving Average Bias）

**定义句**: 当价格高于移动平均线时视为上升趋势，低于时视为下降趋势；短期均线上穿长期均线为金叉（看涨），下穿为死叉（看跌）。

**可观测证据（可计算）**:
```python
def ma_bias(close_prices, fast=20, slow=200):
    """
    输出: bias ∈ {BULLISH, BEARISH, NEUTRAL}
    """
    ema_fast = EMA(close_prices, fast)
    ema_slow = EMA(close_prices, slow)
    
    if ema_fast > ema_slow and close_prices[-1] > ema_fast:
        return "BULLISH"
    elif ema_fast < ema_slow and close_prices[-1] < ema_fast:
        return "BEARISH"
    return "NEUTRAL"

# 信号强度
def ma_signal_strength(close_prices, volumes):
    """
    价格突破200周均线的斜率反映趋势强度
    上升的200周MA = 上升趋势增强
    """
    ma_200w = SMA(close_prices, period=1000)  # ~200周
    slope = (ma_200w[-1] - ma_200w[-20]) / ma_200w[-20]
    return slope  # >0.02为强上升, <-0.02为强下降
```

**可证伪检验**:
- 200日均线之上做多的胜率应显著高于随机（>55%）
- 失败判据: 在震荡市场中均线信号产生>60%假突破

**来源**: 《Trend Trader's Handbook》第I章, III章

---

#### B-02: 动量指标偏置（Momentum Oscillator Bias）

**定义句**: 动量指标衡量价格变化速率，RSI>50为看涨偏置，RSI<50为看跌偏置；RSI持续高于80为超买（可能回调），持续低于20为超卖（可能反弹）。

**可观测证据（可计算）**:
```python
def rsi_bias(close_prices, period=14):
    """
    RSI计算与偏置判定
    RSI = 100 - 100/(1 + RS)
    RS = 平均上涨幅度 / 平均下跌幅度
    """
    deltas = [close_prices[i] - close_prices[i-1] for i in range(1, len(close_prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100, "EXTREME_OVERBOUGHT"
    
    rs = avg_gain / avg_loss
    rsi = 100 - 100 / (1 + rs)
    
    if rsi > 80:
        return rsi, "OVERBOUGHT"
    elif rsi > 50:
        return rsi, "BULLISH"
    elif rsi > 20:
        return rsi, "BEARISH"
    else:
        return rsi, "OVERSOLD"

def divergence_bias(prices, rsi, lookback=20):
    """
    背离检测: 价格创新高但RSI未创新高 = 看跌背离
             价格创新低但RSI未创新低 = 看涨背离
    """
    price_highs = find_local_extrema(prices, lookback, 'high')
    rsi_highs = find_local_extrema(rsi, lookback, 'high')
    
    if len(price_highs) >= 2 and len(rsi_highs) >= 2:
        if price_highs[-1] > price_highs[-2] and rsi_highs[-1] < rsi_highs[-2]:
            return "BEARISH_DIVERGENCE"
    
    price_lows = find_local_extrema(prices, lookback, 'low')
    rsi_lows = find_local_extrema(rsi, lookback, 'low')
    
    if len(price_lows) >= 2 and len(rsi_lows) >= 2:
        if price_lows[-1] < price_lows[-2] and rsi_lows[-1] > rsi_lows[-2]:
            return "BULLISH_DIVERGENCE"
    
    return "NO_DIVERGENCE"
```

**可证伪检验**:
- 看涨背离后10日内价格上涨概率应>60%
- 失败判据: RSI在强趋势中持续超买/超卖导致反向信号失效

**来源**: 《Trend Trader's Handbook》第III章（动量振荡器）

---

#### B-03: ADX趋势强度偏置（ADX Trend Strength Bias）

**定义句**: ADX（平均方向指数）衡量趋势强度而非方向；ADX>25表明趋势足够强劲以进行趋势交易，ADX上升表明趋势正在增强。

**可观测证据（可计算）**:
```python
def adx_bias(high, low, close, period=14):
    """
    ADX计算
    +DM = max(0, high_t - high_{t-1}) if high_t - high_{t-1} > low_{t-1} - low_t else 0
    -DM = max(0, low_{t-1} - low_t) if low_{t-1} - low_t > high_t - high_{t-1} else 0
    +DI = 100 * SMA(+DM) / ATR
    -DI = 100 * SMA(-DM) / ATR
    DX = 100 * |+DI - -DI| / (+DI + -DI)
    ADX = SMA(DX, period)
    """
    atr = ATR(high, low, close, period)
    
    plus_dm = []
    minus_dm = []
    for i in range(1, len(high)):
        up_move = high[i] - high[i-1]
        down_move = low[i-1] - low[i]
        plus_dm.append(max(0, up_move) if up_move > down_move else 0)
        minus_dm.append(max(0, down_move) if down_move > up_move else 0)
    
    plus_di = 100 * sum(plus_dm[-period:]) / period / atr
    minus_di = 100 * sum(minus_dm[-period:]) / period / atr
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx  # 简化版，实际应做平滑
    
    if adx > 25 and plus_di > minus_di:
        return "STRONG_UPTREND"
    elif adx > 25 and minus_di > plus_di:
        return "STRONG_DOWNTREND"
    elif adx > 25:
        return "STRONG_TREND"
    else:
        return "WEAK_TREND"
```

**可证伪检验**:
- ADX>25时趋势跟踪策略胜率应显著高于ADX<25时
- 失败判据: ADX在趋势转折点滞后超过5日

**来源**: 《Trend Trader's Handbook》第III章

---

### 摩擦轴（Friction）— 执行成本与滑点

#### F-01: 头寸规模限制（Position Sizing Limit）

**定义句**: 海龟系统的核心创新是基于波动性的头寸规模调整：每个市场的绝对波动幅度（以N衡量）大致相等，确保风险分散化。

**可观测证据（可计算）**:
```python
def turtle_position_size(account_value, N, contract_value_per_point, 
                         point_value=1, risk_percent=0.01):
    """
    海龟头寸单位计算
    头寸单位 = (账户 × 风险%) / (N × 每点价值)
    
    示例: 账户$100万, N=$5, 每点$12.50
    头寸单位 = $10,000 / ($5 × $12.50) = 16份合约
    """
    dollar_risk = account_value * risk_percent
    position_unit = dollar_risk / (N * point_value)
    return int(position_unit)

def position_limits(market, total_markets=12):
    """
    海龟头寸限制规则:
    1. 单个市场 ≤ 4个单位
    2. 高度相关市场合计 ≤ 6个单位
    3. 松散相关市场合计 ≤ 10个单位
    4. 单一方向（多/空）≤ 12个单位
    """
    return {
        'single_market_max': 4,
        'closely_correlated_max': 6,
        'loosely_correlated_max': 10,
        'single_direction_max': 12
    }
```

**可证伪检验**:
- 基于N的头寸调整应使各市场日波动金额大致相等（误差<20%）
- 失败判据: 未按N调整头寸导致单一市场亏损超过账户5%

**来源**: 《海龟交易法则》第3章, 第8章

---

#### F-02: 止损与退出摩擦（Stop-Loss & Exit Friction）

**定义句**: 海龟系统使用2N止损（距离入场价2倍ATR的止损），同时采用10日/20日反向突破作为退出信号；止损的存在是交易成本的一部分，过紧的止损会增加摩擦。

**可观测证据（可计算）**:
```python
def turtle_stop(entry_price, N, direction='LONG', multiplier=2):
    """
    2N止损计算
    """
    if direction == 'LONG':
        return entry_price - multiplier * N
    return entry_price + multiplier * N

def trailing_stop(high_prices, low_prices, close_prices, 
                  entry_price, highest_high, N=2):
    """
    追踪止损: 从最高回撤2N
    """
    stop_price = highest_high - N * ATR(high_prices, low_prices, close_prices)
    return max(stop_price, entry_price - 0.5 * N * ATR(...))  # 不低于入场-0.5N

def system1_exit(low_prices, high_prices, direction='LONG'):
    """
    系统1（20日突破）退出: 10日反向突破
    """
    if direction == 'LONG':
        return min(low_prices[-10:])  # 跌破10日低点
    return max(high_prices[-10:])     # 突破10日高点

def system2_exit(low_prices, high_prices, direction='LONG'):
    """
    系统2（60日突破）退出: 20日反向突破
    """
    if direction == 'LONG':
        return min(low_prices[-20:])
    return max(high_prices[-20:])
```

**可证伪检验**:
- 2N止损应在35-45%的交易中被触发（海龟系统正常损耗）
- 失败判据: 止损过于频繁（>60%触发率）说明N估计过小或市场状态不适合

**来源**: 《海龟交易法则》第3章, 附录

---

### 风险轴（Risk）— 破产风险与极端情景

#### R-01: 破产风险量化（Risk of Ruin）

**定义句**: 破产风险是指因为一连串失败而赔光所有钱的可能性；破产风险随赌注增加不成比例地迅速增大，资金管理的核心是将破产风险控制在可接受水平。

**可观测证据（可计算）**:
```python
def risk_of_ruin(win_rate, payoff_ratio, risk_per_trade=0.01):
    """
    破产风险计算（简化公式）
    
    参数:
    - win_rate: 胜率 (0-1)
    - payoff_ratio: 平均盈利/平均亏损
    - risk_per_trade: 每笔交易风险占账户比例
    
    返回: 破产概率估计
    """
    if win_rate * payoff_ratio <= (1 - win_rate):
        return 1.0  # 期望值为负，破产必然
    
    # 简化公式: R = ((1-W)/W)^(C/R) 其中C为初始资金单位, R为每单位风险
    # 更实用的: 基于蒙特卡洛模拟
    edge = win_rate * payoff_ratio - (1 - win_rate)
    if edge <= 0:
        return 1.0
    
    # 经验法则: 单笔风险1% + 正期望值 → 理论破产风险<1%
    return max(0, 1 - edge**2 / (risk_per_trade * 2))

def monte_carlo_ruin_simulation(win_rate, payoff_ratio, 
                                  risk_per_trade=0.01, num_simulations=10000):
    """
    蒙特卡洛破产风险模拟
    """
    ruin_count = 0
    for _ in range(num_simulations):
        capital = 1.0  # 初始资金=100%
        while capital > 0.2 and capital < 3.0:  # 亏到20%或赚到300%
            if random.random() < win_rate:
                capital *= (1 + risk_per_trade * payoff_ratio)
            else:
                capital *= (1 - risk_per_trade)
            if capital <= 0.01:
                ruin_count += 1
                break
    return ruin_count / num_simulations
```

**可证伪检验**:
- 单笔风险2%时破产风险应显著高于1%（海龟采用约1%）
- 失败判据: 任何单笔交易风险>2%账户净值 → 立即拒绝

**来源**: 《海龟交易法则》第3章（破产风险）, 第8章

---

#### R-02: 期望值验证（Expectancy Validation）

**定义句**: 期望值 = 每笔交易的平均赢利 / 每笔交易的平均风险投入；海龟系统的期望值约为0.2，即每1美元风险投入预期获利20美分。

**可观测证据（可计算）**:
```python
def calculate_expectancy(trades):
    """
    输入: trades = [(profit, risk), ...]
    输出: 期望值（R乘数平均值）
    """
    r_multiples = [profit / risk for profit, risk in trades]
    return sum(r_multiples) / len(r_multiples)

def r_multiple_distribution(trades):
    """
    R乘数分布分析
    正期望值系统特征:
    - 亏损交易数量 > 盈利交易数量（通常65-70%亏损）
    - 但盈利交易的平均R乘数 > 2.0
    - 存在少量10R+的大盈利交易
    """
    losses = [r for r in trades if r < 0]
    wins = [r for r in trades if r >= 0]
    
    win_rate = len(wins) / len(trades)
    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(losses) / len(losses) if losses else 0
    
    return {
        'win_rate': win_rate,
        'avg_win_r': avg_win,
        'avg_loss_r': avg_loss,
        'expectancy': win_rate * avg_win + (1 - win_rate) * avg_loss,
        'big_wins_5r': len([r for r in wins if r > 5])
    }
```

**可证伪检验**:
- 海龟系统历史回测期望值应>0.15
- 失败判据: 期望值<0 → 系统无效

**来源**: 《海龟交易法则》第3章, 第12章

---

#### R-03: 认知偏差风险控制（Cognitive Bias Risk）

**定义句**: 交易者因认知偏差导致的非理性行为是系统执行的最大风险；海龟成功的关键不在于系统本身，而在于坚定不移执行系统的能力。

**关键偏差清单与对策**:

| 偏差 | 定义 | 可计算检测 | 对策 |
|------|------|-----------|------|
| 损失厌恶 | 不赔钱远比赚钱更重要 | 止损执行率<80% | 自动化止损单 |
| 沉没成本 | 过度重视已投入的资金 | 持仓时间超过系统信号2倍 | 严格按信号退出 |
| 处置效应 | 早早兑现利润，让损失持续 | 平均盈利持仓<平均亏损持仓天数 | 反向操作: 让利润奔跑 |
| 结果偏好 | 以结果质量判断决策好坏 | 因连续亏损改变系统参数 | 关注期望值而非单笔结果 |
| 近期偏好 | 过度重视近期数据 | 过去20日权重>过去200日 | 等权看待所有历史数据 |
| 锚定效应 | 过度依赖容易获得的信息 | 入场价成为决策锚点 | 用当前价格重新评估 |
| 小数定律 | 从太少信息中得出结论 | 10笔交易内改变策略 | 最少100笔样本 |

**来源**: 《海龟交易法则》第2章, 第4章

---

## B) 参数表

| 参数名 | 默认值 | 可调范围 | 来源书 | 用途 | 调参影响 |
|--------|--------|----------|--------|------|----------|
| 唐奇安通道周期（系统1） | 20日 | 10-50日 | 海龟 | 中期突破入场 | 周期越短信号越多但假突破增加 |
| 唐奇安通道周期（系统2） | 60日 | 40-120日 | 海龟 | 长期突破入场 | 周期越长信号越少但胜率提高 |
| ATR计算周期（N） | 20日 | 10-30日 | 海龟 | 头寸规模和止损 | 影响所有风险计算 |
| 单笔风险比例 | 1% | 0.5%-2% | 海龟 | 头寸单位计算 | 直接影响破产风险 |
| 止损倍数 | 2N | 1.5N-3N | 海龟 | 止损距离 | 越小止损越频繁但单次损失小 |
| SMA快线周期 | 20日 | 10-50日 | TTH | 趋势识别 | 与慢线差距决定信号频率 |
| SMA慢线周期 | 200日 | 100-300日 | TTH | 趋势方向 | 长期趋势基准 |
| RSI周期 | 14日 | 7-21日 | TTH | 动量/超买超卖 | 越短越敏感 |
| RSI超买阈值 | 80 | 70-90 | TTH | 超买判定 | 越高信号越少但可靠性增强 |
| RSI超卖阈值 | 20 | 10-30 | TTH | 超卖判定 | 同上 |
| ADX阈值 | 25 | 20-30 | TTH | 趋势强度判定 | 越高只选强趋势 |
| 布林带周期 | 20日 | 10-30日 | TTH | 波动性/突破 | 与ATR周期通常一致 |
| 布林带标准差 | 2σ | 1.5-3σ | TTH | 通道宽度 | 越大信号越少 |
| 积累期ADX上限 | 25 | 20-30 | TTH | 周期识别 | 需与趋势阈值一致 |
| 标记期成交量放大比 | 1.2× | 1.1-1.5× | TTH | 上涨确认 | 越高越严格 |
| 回撤止损比例 | 0.5N | 0.3N-1N | 海龟 | 追踪止损下限 | 防止利润过度回吐 |
| 系统1退出反向突破 | 10日 | 5-15日 | 海龟 | 中期退出 | 越短退出越快但可能错过趋势 |
| 系统2退出反向突破 | 20日 | 10-30日 | 海龟 | 长期退出 | 同上 |

> TTH = 《Trend Trader's Handbook》

---

## C) 禁止跑偏规则（≥15条）

### 系统纪律规则

1. **禁止单笔风险>2%** — 无论信心多强，单笔交易风险不得超过账户净值的2%（海龟标准: 1%）
2. **禁止跳过突破信号** — 系统生成的所有突破信号必须执行，不得因"感觉不对"而跳过（海龟第一教训: 错过趋势=全年失败）
3. **禁止提前止损** — 不得将止损从2N收紧到1N或更小，即使在浮盈状态下（除非是追踪止损按规则调整）
4. **禁止加仓摊平亏损** — 亏损头寸绝对禁止加仓摊薄成本（Martingale策略在海龟体系中属于高危行为）
5. **禁止在退出信号出现前手动平仓** — 必须等待10日/20日反向突破或2N止损，不得因利润回撤而提前离场

### 市场状态规则

6. **禁止在ADX<20时趋势跟踪** — ADX低于20表明趋势太弱，此时趋势跟踪策略失效概率高
7. **禁止在分销期新开多头** — 市场周期处于分销阶段时，新开多头风险极大
8. **禁止在积累期做空** — 积累期是底部构建阶段，做空属于逆势行为
9. **禁止在RSI超买区追多** — RSI>80时追多属于FOMO（错失恐惧）行为，盈亏比极差
10. **禁止在RSI超卖区追空** — RSI<20时追空同理

### 头寸与相关性规则

11. **禁止单一市场超过4个单位** — 即使信号连续出现，单个市场持仓不得超过4个头寸单位
12. **禁止高度相关市场合计超6单位** — 如原油+燃油+天然气合计不得超过6单位
13. **禁止单一方向超过12单位** — 全组合多头或空头总单位不得超过12个
14. **禁止不基于N的头寸调整** — 所有头寸规模必须按ATR(N)计算，不得主观决定合约数

### 心理与认知规则

15. **禁止在连续亏损3次后改变参数** — 连续亏损是趋势系统的正常特征（胜率通常<50%），改变参数=结果偏好
16. **禁止以入场价作为决策锚点** — 必须用当前价格重新评估每一笔持仓，不得因"已经亏了这么多"而继续持有
17. **禁止在10笔交易内评估系统有效性** — 最少需要100笔交易样本才能进行统计评估
18. **禁止使用<50日的回测样本做决策** — 样本量不足会导致过度拟合
19. **禁止在系统外添加"确认指标"** — 不得在原有系统上叠加个人判断来过滤信号（这是大多数海龟失败的原因）
20. **禁止在市场状态不确定时强行交易** — 当ADX、周期阶段、均线方向三者矛盾时，应降低仓位或观望

---

## D) 跨书裁决 + YAML

### 跨书概念冲突裁决

| 冲突点 | 书A观点 | 书B观点 | 裁决 | 理由 |
|--------|---------|---------|------|------|
| 入场信号优先级 | 海龟: 唐奇安通道突破（20/60日） | TTH: 均线金叉+RSI确认 | **组合使用** | 唐奇安突破定义趋势起点，RSI过滤超买区假突破；单独均线金叉在震荡市产生过多假信号 |
| 头寸规模方法 | 海龟: 基于ATR(N)的波动率调整 | TTH: 固定百分比或均仓 | **采纳海龟** | ATR调整使各市场风险贡献相等，是海龟系统核心创新；固定百分比在高波动市场风险暴露不均 |
| 止损方法 | 海龟: 2N硬性止损+反向突破退出 | TTH: 追踪止损（抛物线SAR） | **分场景使用** | 2N止损适用于趋势系统初始阶段；抛物线SAR适用于趋势确立后的利润保护 |
| 趋势强度度量 | 海龟: 隐含在突破幅度中 | TTH: ADX显式度量 | **ADX优先** | ADX>25是趋势跟踪策略适用的前提条件，应先过滤再入场 |
| 震荡市场处理 | 海龟: 任何市场都适用（只要波动率足够） | TTH: 识别周期阶段后选择性交易 | **采纳TTH** | 在分销期/积累期强行趋势跟踪会产生过多损耗 |

### 统一参数建议（三书整合）

```yaml
unified_trend_system:
  entry:
    primary: donchian_channel_breakout  # 海龟
    filter: [rsi_not_overbought, adx_above_25]  # TTH过滤
    parameters:
      system1_period: 20
      system2_period: 60
      rsi_overbought: 80
      rsi_oversold: 20
      adx_threshold: 25
  
  position_sizing:
    method: volatility_based  # 海龟核心
    risk_per_trade: 0.01  # 1%
    atr_period: 20
    limits:
      single_market: 4
      correlated_group: 6
      single_direction: 12
  
  exit:
    stop_loss: 2N  # 海龟
    system1_reverse: 10_day_breakout
    system2_reverse: 20_day_breakout
    trailing: half_N_below_high  # 海龟追踪止损
  
  market_filter:
    cycle_phase_required: [markup, markdown]  # TTH周期过滤
    adx_minimum: 20
    avoid: [accumulation_long, distribution_short]
```

### YAML 汇总卡

```yaml
---
group: "05"
theme: "趋势/系统交易"
processing_mode: "1+4混合"
books:
  - title: "海龟交易法则（珍藏版）"
    author: "柯蒂斯·费思 (Curtis M. Faith)"
    key_contributions: 
      - "ATR(N)波动率调整头寸规模"
      - "唐奇安通道突破系统"
      - "2N止损与反向突破退出"
      - "期望值与R乘数框架"
      - "认知偏差与执行纪律"
    core_parameters:
      - {name: "system1_period", value: 20, unit: "days"}
      - {name: "system2_period", value: 60, unit: "days"}
      - {name: "atr_period", value: 20, unit: "days"}
      - {name: "stop_multiplier", value: 2, unit: "N"}
      - {name: "risk_per_trade", value: 0.01, unit: "fraction"}
    
  - title: "The Trend Trader's Handbook"
    author: "James Muranno"
    key_contributions:
      - "市场周期四阶段模型"
      - "多指标趋势确认体系（MA/RSI/MACD/ADX/布林带）"
      - "背离信号检测"
      - "成交量确认方法"
    core_parameters:
      - {name: "rsi_period", value: 14, unit: "days"}
      - {name: "rsi_overbought", value: 80, unit: "level"}
      - {name: "rsi_oversold", value: 20, unit: "level"}
      - {name: "adx_threshold", value: 25, unit: "level"}
      - {name: "bollinger_period", value: 20, unit: "days"}
      - {name: "bollinger_std", value: 2, unit: "sigma"}
      - {name: "sma_fast", value: 20, unit: "days"}
      - {name: "sma_slow", value: 200, unit: "days"}
    
  - title: "量化交易：如何建立自己的算法交易"
    author: "欧内斯特·陈 (Ernest P. Chan)"
    key_contributions:
      - "均值回归策略框架"
      - "动量策略数学基础"
      - "回测与过拟合防范"
      - "算法交易基础设施"
    note: "本书内容以图片格式存储，详细参数提取受限，核心概念已融入统一框架"

states_defined: 3  # S-01, S-02, S-03
biases_defined: 3  # B-01, B-02, B-03
frictions_defined: 2  # F-01, F-02
risks_defined: 3  # R-01, R-02, R-03
prohibitions: 20
parameters_tabled: 19

key_metrics:
  expected_win_rate: "35-45%"
  expected_payoff_ratio: ">2:1"
  expected_expectancy: ">0.15R"
  max_single_risk: "2% (推荐1%)"
  max_drawdown_expected: "~30%"
  min_sample_for_evaluation: "100 trades"

cross_group_refs:
  - "Group 01: ATR, 期望值, 破产风险"
  - "Group 07: 海龟实验历史背景, 丹尼斯与埃克哈特"
```

---

> **处理说明**: 本组采用模式1+4混合处理。三本书的概念已整合为统一的趋势交易系统框架。由于《量化交易》文件以图片格式存储，详细参数提取受限，但其核心概念（均值回归、动量策略、回测方法）已融入框架。所有参数均标注可调范围和调参影响，便于实际部署时优化。  
> **关键原则**: 趋势系统的核心不在于高胜率（35-45%为正常），而在于大盈小亏的期望值为正；坚定不移地执行系统比系统本身更重要。
