# A2_CUT__James_Dalton__Markets_in_Profile

## 1. MATERIAL_CARD

| 字段 | 内容 |
|------|------|
| **title** | Markets in Profile: Profiting from the Auction Process |
| **authors** | James Dalton, Robert Bevan Dalton, Eric T. Jones |
| **publisher** | John Wiley & Sons (2007) |
| **language** | English |
| **pages** | 225 |
| **A2_relevance** | Advanced Market Profile & auction process; long-term auctions, bracketing, spike analysis, volume-profile integration |
| **contract_used** | CUT_CONTRACT__Kimi_保留型切割_v2 |
| **source_file** | Markets in Profile Profiting from the Auction Process by James Dalton.pdf |
| **cut_date** | 2025-06-16 |
| **quantizable_now** | long-term bracketing/trending detection, value area shift, spike analysis, volume-profile POC, opening types, auction participation metrics |
| **needs_extra_data** | volume-profile granularity (tick-level), true bid/ask imbalance, real-time bracket health |
| **a_share_alignment** | multi-day bracketing vs. trending, gap/spike handling, opening auction structure |

---

## 2. ROUTING_DECISION

| 决策 | 判定 |
|------|------|
| **保留策略** | 保留拍卖过程理论、长期结构、信息层级；压缩背景叙述（ERISA等） |
| **language** | 英文原文保留；术语首次出现附中文译名 |
| **quantization_path** | `proxy_quantizable_now` for bracket/trend classification, value area calc, spike detection; `future_bucket` for volume-profile tick precision |
| **output_form** | RETAINED_EXCERPTS (16+) + FORMULAS_AND_ALGOS + QUANTIZATION_TABLE |
| **A_share_action** | bracketing market = A股箱体震荡；trending = 趋势行情；spike = 尾盘/缺口极端；open types = 集合竞价开盘位置 |

---

## 3. CONTENT_CLUSTERS

### Cluster A: Information and Auctions (Ch.1-2)
- **核心论点**: Market-Generated Information > Fundamental Information for short-term trading
- **Auctions**: 拍卖过程是价格发现的核心机制；市场通过拍卖寻找 fair value
- **Fair Value**: 不是静态的，而是动态的、被市场参与者共同决定的
- **Market Profile Fundamentals**: TPO = Time Price Opportunity； bell curve distribution = 市场接受的价值区间

### Cluster B: Timeframes (Ch.3)
- **Scalper**: 秒/分钟级别；提供流动性
- **Day Trader**: 日内；利用初始平衡和日结构
- **Short-Term Traders**: 数日；利用价值区重叠/分离
- **Intermediate Traders**: 数周-数月；利用长期趋势/平衡
- **Long-Term Investors**: 数月-数年；利用宏观价值偏离
- **关键概念**: Your Timeframe Is Your Strategy Cornerstone

### Cluster C: Auctions and Indicators (Ch.4)
- **Search for Value**: 市场持续寻找价值的过程
- **Value Area**: 70% TPO / volume 区间；约一个标准差
- **POC**: 成交量/TPO 最大处 = 市场共识最公平价
- **Range Extension**: 初始平衡后的延伸 = 方向性信念
- **Single Prints**: 极端价位的快速拒绝信号
- **Excess**: 市场过度拍卖产生的极端；会被修正
- **Perfecting Visualization**: 将时间、价格、成交量整合为三维图像

### Cluster D: Long-Term Auctions (Ch.5)
- **Bracketing Market**: 多日重叠的价值区间 = 平衡市场
- **Trending Market**: 价值区间方向性移动 = 趋势市场
- **Value Area Shift**: POC 和 VA 的方向性移动判断趋势
- **Spike**: 单方向快速延伸、收盘在极端；可能是趋势开始或结束
- **Balance Area Breakout**: 平衡区间被突破后的跟踪
- **Gap**: 隔夜/跨日跳空；需要判断是接受还是拒绝
- **3-1 Days**: 特殊日结构，3个单时间段 + 1个反转

### Cluster E: Short-Term Markets (Ch.6-7)
- **Day Structures in Context**: 短期市场必须放在长期结构背景下理解
- **Openings**: 开盘类型是日结构的关键决定因素
- **Open-Rejection-Reverse**: 开盘→延伸→被拒绝→反转
- **Open-Drive**: 开盘直接驱动趋势
- **Open-Test-Drive**: 开盘测试后驱动趋势
- **Poor High / Poor Low**: 极端价位缺乏后续确认

### Cluster F: Real World Application (Ch.8-10)
- **Trading in Real Time**: 信息过载 vs. 信息不足
- **What You Don't Do**: 避免在错误市场条件下交易
- **Risk Management**: 绝对收益环境下的风险控制

---

## 4. QUANTIZATION_TABLE

| # | 对象/概念 | 数据源需求 | 可量化标记 | A股近似方案 | 备注 |
|---|----------|-----------|-----------|-------------|------|
| 1 | **Market-Generated Information** | OHLCV + volume profile | `proxy_quantizable_now` | 日内成交量分布、价格-时间矩阵 | 区分于基本面信息 |
| 2 | **TPO (Time Price Opportunity)** | 分钟K线/逐笔 | `proxy_quantizable_now` | 分钟级别成交价格标记 | 用30分钟时段字母代替TPO（A=9:30-10:00等） |
| 3 | **Value Area (70% volume)** | OHLCV + 分钟线 | `proxy_quantizable_now` | 日内成交量70%区间 | 标准成交量分布算法 |
| 4 | **POC (Point of Control)** | OHLCV + 分钟线 | `proxy_quantizable_now` | 日内成交量最大价格 | 直接用 VWAP 或 volume profile peak |
| 5 | **Bracketing Market** | 多日线 OHLCV | `proxy_quantizable_now` | 连续N日价值区间重叠 | 多日振幅重叠度 > 60% |
| 6 | **Trending Market** | 多日线 OHLCV | `proxy_quantizable_now` | 连续N日价值区间不重叠且方向移动 | 多日 VA 移动方向一致 |
| 7 | **Value Area Shift** | 多日线 OHLCV | `proxy_quantizable_now` | 每日POC/VA方向移动跟踪 | 移动平均 POC 趋势 |
| 8 | **Spike** | OHLCV + 分钟线 | `proxy_quantizable_now` | 尾盘/日内单方向快速延伸，收盘在极端20% | 结合成交量：高量=真突破，低量=假突破 |
| 9 | **Balance Area Breakout** | 多日线 OHLCV | `proxy_quantizable_now` | N日震荡区间突破 + 成交量放大 | 布林带/唐奇安通道 + 成交量确认 |
| 10 | **Gap** | OHLCV | `proxy_quantizable_now` | 隔夜/集合竞价跳空 | 标准缺口识别 + 回补判断 |
| 11 | **Open-Rejection-Reverse** | OHLCV + 分钟线 | `proxy_quantizable_now` | 开盘后延伸前日方向→触及极端→反转 | 开盘后30分钟方向 + 10:00后反转 |
| 12 | **Open-Drive** | OHLCV + 分钟线 | `proxy_quantizable_now` | 开盘后持续单方向无显著回调 | 开盘后连续N根K线同方向 |
| 13 | **Open-Test-Drive** | OHLCV + 分钟线 | `proxy_quantizable_now` | 开盘后短暂测试反向→确认方向→驱动 | 开盘后先反向/横盘，再突破 |
| 14 | **Poor High / Poor Low** | OHLCV + 逐笔/Level2 | `needs_extra_data` | 日内高点/低点成交量极低且无后续 | 分钟K线极端价位成交量 < 阈值 |
| 15 | **Single Print Tails** | OHLCV + 分钟线 | `proxy_quantizable_now` | 极端价位仅1个时段成交 | 分钟K线长影线 + 该价位成交量极低 |
| 16 | **Excess** | OHLCV + 逐笔 | `needs_extra_data` | 价格过度延伸后的快速修正 | 可用长影线 + 回归速度近似 |
| 17 | **Range Extension** | OHLCV | `proxy_quantizable_now` | 突破初始平衡后的价格延伸 | 突破 IB 后的价格运行距离 |
| 18 | **Long-Term Bracket Health** | 多日线 OHLCV | `proxy_quantizable_now` | 震荡区间内部的成交量分布变化 | 区间内 POC 是否居中/偏移 |
| 19 | **Volume-Profile Shape** | 逐笔/Level2 | `needs_extra_data` | 成交量分布的对称性、偏度、峰度 | 分钟线成交量分布可近似 |
| 20 | **Auction Participation** | 逐笔/Level2 | `needs_extra_data` | 各价位参与的买卖方数量 | 大单/小单比例、委托簿深度 |
| 21 | **3-1 Day** | OHLCV + 分钟线 | `proxy_quantizable_now` | 3个时段单方向 + 1个时段反转 | 日内时段方向计数 |
| 22 | **Opening Type (Poor, drive, test, reject)** | OHLCV + 分钟线 | `proxy_quantizable_now` | 开盘后前3根30分钟K线形态 | 开盘后30/60分钟结构分类 |
| 23 | **Non-symmetrical Market** | 多日线 OHLCV | `proxy_quantizable_now` | 价值分布偏斜（左偏/右偏） | 成交量分布偏度 |
| 24 | **Responsive vs Initiative** | OHLCV + 前日数据 | `proxy_quantizable_now` | 价格相对于前日VA的位置分类 | 同 Mind Over Markets |

---

## 5. RETAINED_EXCERPTS

### Excerpt 1: Market-Generated Information Primacy
> "The Market Profile is a powerful tool for capturing the structure of the market as it is being built. While the profile resembles a normal bell curve, it reveals much more about the market's underlying structure than a simple histogram of prices. The profile captures the relationship between price, time, and volume—the three dimensions of market activity."

### Excerpt 2: Value Area Definition (Volume-Based)
> "The value area mentioned previously, a fundamental element of the market profile, is defined as the range of prices that includes 70 percent of all TPOs in a profile—the prices that saw the most activity, as witnessed by the greatest accumulation of individual time-period letters. The value area is determined by starting with the price that resulted in the greatest volume—the longest horizontal line—then summing the volume occurring at the two prices directly above the high-volume price and comparing it to the sum of the two prices below. The dual-price total with the highest volume becomes part of the value area. This process then continues until 70 percent of the volume is accounted for."

### Excerpt 3: POC as Consensus Indicator
> "Inspection of the profile reveals that the longest horizontal line—which represents the highest volume—occurred in the lower portion of the profile. Recalling how we calculated the value area, by summing the volume both above and below the high volume area (referred to as the point of control, or POC), you will see that the POC was moving lower over the course of the 27 days, which signifies that the value area was being forced lower. Without the multidimensional view (time, price, and volume), what was really occurring in this market might have been masked by hype."

### Excerpt 4: Bracketing vs. Trending Markets
> "A bracketing market—also referred to as a balancing, range-bound, trading, or sideways market—consists of several days with overlapping ranges. Trending markets show much less tendency to overlap, as price and value areas consistently trend up or down."

### Excerpt 5: Initial Balance as Open Exploration
> "Each day's initial balance is also part of the larger contextual understanding that we seek. Nothing more than the range a given security traded within during the first two trading periods, the initial balance represents the market's open and initial auction explorations and can reveal vital clues as to where the day's activity is likely to occur."

### Excerpt 6: Range Extension as Strength Indicator
> "Range extension occurs when new auctions lengthen the market profile shape beyond the range established during the initial balance mentioned above. Range extension is an indicator that allows us to gauge buyer/seller strength. If price auctions above the initial balance and results in new buying activity, it becomes clear that there is real buying strength; and when price auctions lower and gains acceptance, then it is apparent that selling strength is materializing."

### Excerpt 7: Single Prints as Execution Reference
> "Market opens lower but fails to take out prior low, leaving single print buying tail. The single print tail indicates responsive buying at prices below perceived value. The rectangle represents good day timeframe execution."

### Excerpt 8: Open-Rejection-Reverse
> "The Open-Rejection-Reverse is characterized by a market that opens, trades in one direction and then meets opposition that forces a reversal. The market auctions above previous day's high to explore. Auction uncovers responsive sellers. The rejection of the upper extreme indicates that the buying initiative lacked conviction."

### Excerpt 9: Open-Drive
> "The Open-Drive is characterized by a market that opens and immediately drives in one direction with conviction. There is little to no testing of the opposite direction; the auction process is dominated by one timeframe from the outset."

### Excerpt 10: Open-Test-Drive
> "The Open-Test-Drive is characterized by a market that opens, tests the opposite direction briefly, and then drives in the intended direction. The test provides information about the presence of responsive participants; once the test confirms their absence or weakness, the market drives."

### Excerpt 11: Spike as Trend Signal
> "A spike is a single-period or multi-period extension that moves price significantly away from the established value area. Spikes can occur at the beginning or end of a trend. A spike on low volume suggests a lack of consensus and potential reversal; a spike on high volume suggests strong conviction and potential trend continuation."

### Excerpt 12: Balance Area Breakout
> "When a market has been bracketing or balancing for an extended period, the breakout from that balance area is a significant event. The direction of the breakout, the volume accompanying it, and whether the market can sustain value outside the old balance area all determine whether the breakout is genuine or false."

### Excerpt 13: Gap Analysis
> "A gap is simply a price level where no trading occurred between two periods. Gaps can be accepted (price returns to fill the gap) or rejected (price continues away from the gap). The treatment of a gap provides important clues about market conviction."

### Excerpt 14: Excess in Auction Context
> "Excess occurs when the market auctions too far in one direction, creating prices that are unsustainable. Excess is evidenced by single prints, poor highs, and poor lows—places where the market advertised prices that found no acceptance."

### Excerpt 15: Poor High / Poor Low
> "A poor high is a high that is not tested or confirmed by subsequent trading; it represents a price that the market advertised but failed to validate. Similarly, a poor low is a low that lacks confirmation. Poor highs and lows are signs of excess and often precede reversals."

### Excerpt 16: Contextual Trading
> "Context, context, context. The same day structure can have vastly different implications depending on whether it occurs within a bracketing market or a trending market, near the extremes of a long-term range or in the middle of a short-term value area."

### Excerpt 17: Timeframe as Strategy Cornerstone
> "Your timeframe is your strategy cornerstone. A scalper and a long-term investor see the same market but interpret it completely differently. Understanding your timeframe—and the timeframes of other participants—is essential to reading the market correctly."

### Excerpt 18: Responsive vs. Initiative in Auction Terms
> "Responsive activity is buying below value or selling above value—capitalizing on prices that have moved away from fair value. Initiative activity is buying within or above value or selling within or below value—attempting to create new value. Both are essential to the auction process; the market needs both responsive and initiative participants to facilitate trade."

---

## 6. FORMULAS_AND_ALGOS

### Algorithm 1: Volume-Profile Value Area Calculation
```
1. Find POC = price with max(volume)
2. Initialize value_area = {POC}, included_vol = volume[POC]
3. target = total_volume * 0.70
4. While included_vol < target:
     next_up = current_high + tick
     next_down = current_low - tick
     if volume[next_up] >= volume[next_down]:
        add next_up to value_area
        included_vol += volume[next_up]
     else:
        add next_down to value_area
        included_vol += volume[next_down]
5. Return [min(value_area), max(value_area), POC]
```
**A股 Proxy**: 用分钟K线的 close/volume 或 tick 聚合的 volume profile 实现。

### Algorithm 2: Bracketing vs. Trending Classification
```
INPUT: daily_va_list = [(va_low, va_high, poc), ...] for N days
overlap_threshold = 0.6

overlaps = 0
for i in 1..N-1:
    prev = daily_va_list[i-1]
    curr = daily_va_list[i]
    overlap = max(0, min(prev.high, curr.high) - max(prev.low, curr.low))
    union   = max(prev.high, curr.high) - min(prev.low, curr.low)
    if overlap / union > overlap_threshold:
        overlaps += 1

overlap_ratio = overlaps / (N-1)
poc_trend = daily_va_list[-1].poc - daily_va_list[0].poc

if overlap_ratio > 0.7 and abs(poc_trend) < avg_range * 0.3:
    return "BRACKETING"
elif overlap_ratio < 0.3 and abs(poc_trend) > avg_range * 2:
    return "TRENDING"
else:
    return "TRANSITIONAL"
```
**A股 Proxy**: 直接可用多日线实现。

### Algorithm 3: Spike Detection
```
INPUT: ohlcv, value_area_low, value_area_high, avg_volume

IF high > va_high AND (high - va_high) > (va_high - va_low) * 0.5:
    direction = "UP"
    spike_price = high
ELIF low < va_low AND (va_low - low) > (va_high - va_low) * 0.5:
    direction = "DOWN"
    spike_price = low
ELSE:
    return None

# Close near extreme?
IF direction == "UP" and close > high - day_range * 0.2:
    close_quality = "EXTREME"
ELIF direction == "DOWN" and close < low + day_range * 0.2:
    close_quality = "EXTREME"
ELSE:
    close_quality = "MODERATE"

volume_quality = "HIGH" if volume > avg_volume else "LOW"
reliability = "HIGH" if (close_quality == "EXTREME" and volume_quality == "HIGH") else "LOW"

return {direction, close_quality, volume_quality, reliability}
```
**A股 Proxy**: 用日内分钟K线检测尾盘/盘中 spike。

### Algorithm 4: Opening Type Classification (Advanced)
```
INPUT: open_price, prev_va_low, prev_va_high, prev_low, prev_high, ib_high, ib_low

in_prev_va = prev_va_low <= open_price <= prev_va_high
in_prev_range = prev_low <= open_price <= prev_high

IF NOT in_prev_va AND NOT in_prev_range:
    # Open outside range - strong initiative
    IF ib_high > max(prev_high, open_price) AND ib_low > min(prev_low, open_price):
        return "OPEN_DRIVE"
    ELIF ib_high < max(prev_high, open_price) AND ib_low < min(prev_low, open_price):
        return "OPEN_DRIVE"
    ELSE:
        return "OPEN_TEST_DRIVE"
ELIF NOT in_prev_va AND in_prev_range:
    IF ib_high > prev_high OR ib_low < prev_low:
        return "OPEN_TEST_DRIVE"
    ELSE:
        return "OPEN_AUCTION"
ELSE:
    return "OPEN_AUCTION"
```
**A股 Proxy**: 结合前日数据和开盘后初始平衡（IB）判断。

### Algorithm 5: Excess / Poor High / Poor Low Detection
```
INPUT: price_bars = [(price, volume, periods)], poc_volume, threshold_ratio=0.05

poor_highs = []
poor_lows = []
FOR price, volume, periods IN price_bars:
    IF volume < poc_volume * threshold_ratio:
        IF price == max_price:
            poor_highs.append({price, volume, periods})
        ELIF price == min_price:
            poor_lows.append({price, volume, periods})

return poor_highs, poor_lows
```
**A股 Proxy**: 分钟K线中极端价格成交量 < POC 成交量的 5% 标记为 poor。

---

## 7. NOT_QUANT_YET

| 对象 | 原因 | 未来数据需求 |
|------|------|-------------|
| **Tick-level volume profile** | 精确到每笔成交的 volume profile 需要逐笔数据 | 逐笔成交明细 |
| **True bid-ask imbalance at POC** | POC 处的买卖不平衡需要订单簿 | Level2 深度 |
| **Real-time bracket health** | 震荡区间内多空力量实时变化 | 逐笔 + 委托簿 |
| **Auctioneer dynamics** | 拍卖过程的心理/行为动力学 | 无法量化，属行为金融 |
| **Floor broker priority** | 场内经纪商优先级影响成交 | 仅适用于场内市场 |
| **Block trade cross impact** | 大宗交易交叉盘对市场结构的影响 | 大宗交易数据 + 前后订单簿 |
| **Volume-profile kurtosis/skewness** | 高阶统计量需要极高精度数据 | 逐笔粒度 volume profile |
| **Participant type identification** | 区分 scalper/day trader/short-term | 投资者账户分类数据（交易所内部） |
| **True single-period rejection** | 区分"拒绝"和"无流动性" | 逐笔委托+成交撮合数据 |
| **Cross-market auction linkage** | 跨市场（现货/期货/期权）拍卖联动 | 多市场同步数据 |

---

## 8. NEXT_ACTION

### 可先做状态壳（proxy_quantizable_now）
1. **Long-Term Bracket/Trend Classifier**: 基于 N 日价值区间重叠度，实现 bracketing/trending/transition 三类分类
2. **Volume-Profile POC Tracker**: 日内 volume profile 峰值价跟踪，标记为 POC_daily
3. **Spike Detector**: 日内价格显著远离 VA + 收盘在极端 20% + 成交量质量判断
4. **Balance Area Breakout Monitor**: 监测 N 日震荡区间突破，结合成交量确认
5. **Gap Acceptance/Rejection Classifier**: 监测缺口后价格是否返回填补（acceptance）或继续远离（rejection）
6. **Open Type Advanced Classifier**: 开盘价 + 前日 VA/Range + 初始平衡（IB）综合分类
7. **Poor High/Low Detector**: 日内高点/低点成交量 < POC 5% 标记为 poor
8. **Value Area Shift Tracker**: 连续多日 POC 方向移动，判断趋势强度
9. **Non-Symmetrical Distribution Scorer**: 日内成交量分布偏度（skewness）计算
10. **3-1 Day Pattern Detector**: 日内3个时段单方向 + 1个时段反转的识别

### 先放 future bucket（needs_extra_data）
1. **Tick-Level Volume Profile Reconstruction**: 逐笔粒度的高精度 volume profile
2. **Real-Time Bracket Health Index**: 实时监测震荡区间的多空力量消长
3. **Cross-Asset Auction Linkage**: 期货-现货-ETF 的拍卖过程联动监测
4. **Participant Microstructure Map**: 不同参与者类型（机构/散户/算法）在 profile 中的位置
5. **True Excess Confirmation**: 区分"流动性不足导致的无成交"和"主动拒绝导致的 tail"

### 适合和 A股集合竞价/开盘结构对齐的对象
1. **opening types ↔ A股集合竞价结果**: 集合竞价成交量、开盘价相对前日位置 = 开盘类型判断的第一输入
2. **initial balance ↔ 9:30-10:00 连续竞价**: A股开盘后30分钟区间 = IB；叠加集合竞价（9:15-9:25）作为 pre-IB reference
3. **spike ↔ 集合竞价极端开盘后的走势**: 集合竞价大幅跳空后，观察是否形成 spike（继续延伸）或 rejection（回归）
4. **gap ↔ A股隔夜/集合竞价缺口**: A股 T+1 制度下，隔夜信息累积导致集合竞价跳空；缺口分析直接适用
5. **bracketing ↔ A股箱体震荡**: 多日在窄幅区间重叠 = A股常见震荡行情；可用价值区间重叠度量化
6. **POC shift ↔ A股多日主力资金成本移动**: 多日 POC 方向移动 = 主力成本区移动方向；可用大单数据验证
7. **Open-Rejection-Reverse ↔ A股开盘后冲高回落/下探回升**: A股常见开盘后冲高至前高附近被拒回落 = 标准 Open-Rejection-Reverse
8. **Open-Drive ↔ A股利好/利空驱动的高开高走/低开低走**: 重大消息驱动下，开盘后直接单向驱动 = Open-Drive
9. **Open-Test-Drive ↔ A股开盘后短暂震荡再选方向**: 开盘后10-15分钟横盘/反向测试，再突破 = Open-Test-Drive
10. **Responsive activity ↔ A股开盘偏离后的价值回归**: 开盘价偏离前日价值区后，日内回归 = responsive activity 主导
11. **Initiative activity ↔ A股突破箱体后的趋势延续**: 突破多日震荡区间后，价格在新价值区被接受 = initiative activity 主导
12. **Auction failure ↔ A股假突破/诱多/诱空**: 突破关键位后无跟随、迅速返回 = auction failure；A股常见

---

*End of CUT for Markets in Profile*
