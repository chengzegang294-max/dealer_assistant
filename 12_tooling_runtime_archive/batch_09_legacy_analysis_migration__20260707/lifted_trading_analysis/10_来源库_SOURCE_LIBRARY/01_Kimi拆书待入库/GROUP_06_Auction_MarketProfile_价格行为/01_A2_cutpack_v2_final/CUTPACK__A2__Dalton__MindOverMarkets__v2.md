# A2_CUT__James_Dalton__Mind_over_Markets

## 1. MATERIAL_CARD

| 字段 | 内容 |
|------|------|
| **title** | Mind Over Markets: Power Trading with Market Generated Information |
| **authors** | James F. Dalton, Eric T. Jones, Robert B. Dalton |
| **publisher** | Traders Press, Inc. (1993, repr. 1999) |
| **language** | English + Chinese (bilingual edition) |
| **pages** | 356 |
| **A2_relevance** | Core Market Profile textbook; defines day structures, auction process, value area, TPO logic, initiative vs. responsive |
| **contract_used** | CUT_CONTRACT__Kimi_保留型切割_v2 |
| **source_file** | James Dalton - Mind over Markets 中文.pdf |
| **cut_date** | 2025-06-16 |
| **quantizable_now** | initial balance, value area, POC, day type classification, range extension, TPO count, excess detection, rotation factor |
| **needs_extra_data** | DOM depth, Level II, floor trader intent, pit-specific mechanics, order flow behind single prints |
| **a_share_alignment** | opening auction structure, opening range, intraday rotation, VWAP-like POC proxy |

---

## 2. ROUTING_DECISION

| 决策 | 判定 |
|------|------|
| **保留策略** | 全文保留核心定义与算法；示例与故事性叙述压缩为摘要 |
| **语言处理** | 中英双语保留；英文原文优先，中文译文作为辅助 |
| **quantization_path** | `proxy_quantizable_now` for day structure rules, value area calc, TPO count, rotation factor; `future_bucket` for DOM-dependent nuances |
| **output_form** | RETAINED_EXCERPTS (16+) + FORMULAS_AND_ALGOS + QUANTIZATION_TABLE |
| **A_share_action** | POC 映射到 A 股加权均价/成交量峰值；initial balance 映射到开盘后 N 分钟区间；single prints 映射到集合竞价/开盘后无成交价格区 |

---

## 3. CONTENT_CLUSTERS

### Cluster A: Auction Process Fundamentals (Ch.1-2)
- **核心定义**: auction 是价格发现过程，市场通过拍卖 lower to find buyers / higher to attract sellers
- **关键概念**: trade facilitation, two-sided trade, excess inventory, local vs. other timeframe
- **可量化**: 方向性尝试与失败的量化 = 价格回到 value area 的速率

### Cluster B: Day Timeframe Structure (Ch.2)
- **Day Types**: Normal Day, Normal Variation of a Normal Day, Trend Day, Double-Distribution Trend Day, Nontrend Day, Neutral Day
- **结构语言**: initial balance, range extension, single prints, tails, value area, point of control
- **可量化**: 开盘类型分类、区间扩展判断、日内结构识别

### Cluster C: Advanced Beginner Framework (Ch.3)
- **评估框架**: Other Timeframe Control on extremes / in body of profile
- **活动分类**: Initiative vs. Responsive Activity
- **TPO Count**: 买方/卖方 imbalance 在 value area 内的估计
- **市场状态**: Trending vs. Bracketed Markets

### Cluster D: Competent Day Trading (Ch.4)
- **开盘分类**: Open Within Value / Open Outside Value but Within Range / Open Outside Range
- **方向信念**: Day Timeframe Directional Conviction
- **可视化**: Pattern Recognition, Liquidity Data Bank, High/Low Volume Areas
- **Rotation Factor**: 量化日内旋转方向与强度

### Cluster E: Long-Term Trading (Ch.4 Sec.II)
- **长期拍卖**: Attempted Direction, Directional Performance, Auction Rotations
- **特殊形态**: 3-1 Days, Neutral-Extreme Days, Spikes, Balance Area Breakouts, Gaps
- **Value-Area Rule**: 跨日 value area 重叠/非重叠判断趋势/平衡

### Cluster F: Proficient Trading (Ch.5)
- **结果方程**: Market Understanding × (Self-Understanding + Strategy) = Results
- **全脑交易者**: 左脑(分析) + 右脑(直觉)

---

## 4. QUANTIZATION_TABLE

| # | 对象/概念 | 数据源需求 | 可量化标记 | A股近似方案 | 备注 |
|---|----------|-----------|-----------|-------------|------|
| 1 | **initial balance** | OHLCV + session calendar | `proxy_quantizable_now` | 开盘后30分钟/60分钟最高最低区间 | 原文定义为A+B periods（约2个30min） |
| 2 | **value area (70% TPO)** | OHLCV + 分钟K线 | `proxy_quantizable_now` | 日内成交量分布70%区间 | 可用 VWAP + volume profile 近似；标准差 proxy |
| 3 | **point of control (POC)** | OHLCV + 分钟K线 | `proxy_quantizable_now` | 日内成交量最大价格/加权均价 | 直接映射为日内 VWAP 或成交量峰值价 |
| 4 | **range extension** | OHLCV + session calendar | `proxy_quantizable_now` | 价格突破 initial balance 后的延伸幅度 | 突破初始区间后的上下轨延伸 |
| 5 | **single prints (tails)** | OHLCV + 逐笔 or Level2 | `needs_extra_data` | 某分钟/某时段无成交价格区间 | 无逐笔时可用分钟K线缺失价格近似 |
| 6 | **TPO count** | TPO数据 or 分钟K线 | `proxy_quantizable_now` | 分钟K线数量分布 | 用分钟级别成交笔数代替 TPO 字母 |
| 7 | **rotation factor** | OHLCV + 分钟K线 | `proxy_quantizable_now` | 逐分钟高低点方向累加 | 原文算法：+1/-1/0 逐 period 判断 |
| 8 | **Normal Day** | OHLCV + session calendar | `proxy_quantizable_now` | 日内振幅适中、有双向成交、收盘在区间中部 | 可用日内波动率 + 成交量分布偏度判断 |
| 9 | **Trend Day** | OHLCV + session calendar | `proxy_quantizable_now` | 单边趋势、开盘在区间一端、收盘在另一端 | 日内趋势强度指标 + 开盘/收盘位置 |
| 10 | **Double-Distribution Trend Day** | OHLCV + 分钟K线 | `proxy_quantizable_now` | 两个成交量聚集区 + 中间低成交稀疏区 | 双峰分布识别（volume profile 双峰） |
| 11 | **Neutral Day** | OHLCV + session calendar | `proxy_quantizable_now` | 收盘在区间内中部、双向范围扩展 | 收盘位置在日内中位数附近 |
| 12 | **Nontrend Day** | OHLCV + session calendar | `proxy_quantizable_now` | 窄幅区间、无方向信念、成交量低 | 日内波动率低 + 成交量萎缩 |
| 13 | **Initiative Activity** | OHLCV + 前日 value area | `proxy_quantizable_now` | 价格在前日/近期 value area 之外成交 | 突破前日 70% 成交量区间 |
| 14 | **Responsive Activity** | OHLCV + 前日 value area | `proxy_quantizable_now` | 价格远离前日/近期 value area 后回归 | 触及前日区间外后返回 |
| 15 | **excess (tails)** | OHLCV + 逐笔/Level2 | `needs_extra_data` | 极端价格快速被拒绝、无持续成交 | 分钟K线长影线 + 该价位成交量极低 |
| 16 | **auction failure** | OHLCV + 分钟K线 | `proxy_quantizable_now` | 价格突破后无跟随、迅速返回 value area | 假突破识别：突破后 N 分钟返回 |
| 17 | **other timeframe control** | DOM + 订单簿 | `needs_extra_data` | 大资金/机构在关键价位的持续介入 | 需 Level2 或主力资金流数据 |
| 18 | **opening type (Within/Outside Value/Range)** | OHLCV + 前日数据 | `proxy_quantizable_now` | 今日开盘价相对于前日 value area / range 的位置 | 直接用前日收盘价/振幅区间判断 |
| 19 | **gap** | OHLCV + session calendar | `proxy_quantizable_now` | 隔夜/集合竞价跳空缺口 | 标准 OHLC 数据即可 |
| 20 | **balance area breakout** | OHLCV + 多日线 | `proxy_quantizable_now` | 多日震荡区间突破 | 用 N 日最高价/最低价区间 |
| 21 | **spike** | OHLCV + 分钟K线 | `proxy_quantizable_now` | 尾部快速单向延伸、收盘在极端 | 尾盘冲刺/跳水的形态量化 |
| 22 | **long-term value area shift** | OHLCV + 多日线 | `proxy_quantizable_now` | 多日 POC 移动方向 | 多日 VWAP 移动趋势 |

---

## 5. RETAINED_EXCERPTS

### Excerpt 1: Initial Balance Definition
> "The price range resulting from market activity during the first two time periods (the first hour) for most commodities is called the initial balance (slightly longer in the S&P). The initial balance represents the period of time in which the locals attempt to find a range where two-sided trade can take place—a range where both the buyer and seller agree to conduct trade."

### Excerpt 2: Value Area Definition
> "The area where 70 percent of the day's business is conducted (roughly one standard deviation) is called the value area. This is logical, for the middle part of the bell curve is where most activity occurs and indicates two-sided trade took place in the day timeframe. If both buyer and seller are actively participating in an area, then that area is accepted as value by both parties."

### Excerpt 3: Point of Control Definition
> "The longest line of TPOs closest to the center of the range is called the point of control. This is the price where the most activity occurred during the day, and it is therefore the fairest price in the day timeframe. The greatest amount of time was spent trading at that price, signifying greatest value."

### Excerpt 4: Single Print Buying Tail
> "The single 'K' TPOs at the lower extreme of the Profile are called a single-print buying tail. This is an important reference point, for it indicates that the other timeframe buyer responded strongly to price advertised below value, rejecting price out of the lower range in one time period (K). Competition among buyers for contracts causes price to move quickly."

### Excerpt 5: Range Extension
> "Any movement in price beyond the initial balance set up by the local in the first hour of trading is called range extension, and signifies that something has changed because of other timeframe buyer or seller presence. The local is not responsible for any major moves in the market. It is the other timeframe that can move price substantially."

### Excerpt 6: Normal Day Characteristics
> "A Normal day is characterized by a wide initial balance and no directional conviction. The other timeframe buyer and seller are both present, but neither are dominant enough to extend the range. The initial balance is not upset throughout the day. In Treasury bonds, the initial balance was established in A and B periods—well over a point wide. Other timeframe sellers entered on the upper extreme because price auctioned too high, creating a strong single-print selling tail, while other timeframe buyers entered on the lower extreme as price auctioned too low, creating a single print buying tail. Price spent the rest of the day auctioning within the extremes."

### Excerpt 7: Trend Day Dynamics
> "There are two types of Trend days: the 'standard' Trend day and the Double-Distribution Trend day. The most important feature of a standard Trend day is the high level of directional confidence that is evident throughout the day. The other timeframe buyer or seller remains in control of the auction process virtually from the day's open to its close."

### Excerpt 8: Double-Distribution Trend Day
> "A very small initial balance is the first indication of a potential Double-Distribution Trend day. Again, the more narrow the base, the easier it is to overwhelm this area and auction quickly to a new level. The other timeframe seller extends the range down in F and G periods. Lower prices are accepted as value forms below the original value area in a new distribution, separated by single TPO price prints. The single prints separating the two distributions become an important reference point near the end of the day. If price auctions back into the single prints during the latter time periods, in effect making them double prints, something has changed, and the second distribution is no longer accepted as value."

### Excerpt 9: Neutral Day
> "A Neutral day is characterized by a lack of directional conviction. Both the other timeframe buyer and seller extend the range, but neither is dominant. The market closes in the middle of the range, signifying a balance between buyer and seller."

### Excerpt 10: Nontrend Day
> "A Nontrend day is characterized by little market participation and no confidence. The initial range is narrow. However, the market fails to extend the range in either direction, and the day remains in a very tight range."

### Excerpt 11: Initiative vs. Responsive Activity
> "Initiative buying is any buying activity occurring within or above the previous day's value area. Conversely, initiative selling is any selling activity occurring within or below the previous day's value area. Responsive buying is buying that occurs below the previous day's value area, as buyers respond to price advertised below value. Responsive selling is selling that occurs above the previous day's value area, as sellers respond to price advertised above value."

### Excerpt 12: TPO Count Methodology
> "The 'TPO count' is found by isolating the point of control (the longest line closest to the center of the range), summing all the TPOs above it and comparing that number to the total number of TPOs below it. Single print tails are excluded from the count, because their implications are clear and have already been considered when examining activity on the extremes. The total TPO figure above the point of control represents other timeframe traders willing to sell and stay short above value, while total TPOs below the point of control represent other timeframe traders willing to buy and stay long below value. The resulting ratio is an estimate for buyer/seller imbalance in the value area."

### Excerpt 13: Excess Definition
> "To achieve its primary goal of trade facilitation, the market auctions lower to find buyers and higher to attract sellers. Ideally, the market finds a value range where both the other timeframe buyer and seller perceive price to be fair so that two-sided trade can take place. However, the market is effective, not efficient. Consequently, in its attempt to generate trade with all participants, the market occasionally creates excess by auctioning too far in a given direction."

### Excerpt 14: Price × Time = Value
> "Without considering time, there is no way to judge value, and trading becomes a 50-50 gamble on price movement. In the day timeframe, time validates price. The areas of the Market Profile's bell curve showing the greatest depth indicate the prices where trading spent the most time, thus establishing value for that day (price × time = value)."

### Excerpt 15: Auction Failure
> "Auction failure occurs when price breaks away from value but fails to sustain the move, quickly returning to the value area. This is a sign that the initiating activity lacked conviction and that responsive activity is dominant."

### Excerpt 16: The Results Equation
> "The Results Equation: Market Understanding × (Self-Understanding + Strategy) = Results. Understanding the market is only one part of the equation; without self-understanding and a coherent strategy, even the best market analysis will not produce profitable results."

### Excerpt 17: Open Types Classification
> "Open Within Value: The market opens within the previous day's value area, suggesting continuity and balance. Open Outside of Value but Within Range: The market opens outside the previous day's value area but within the previous day's range, suggesting a potential test of value. Open Outside of Range: The market opens outside the previous day's range, suggesting a strong initiative move and potential trend day."

### Excerpt 18: Long-Term Value Area Rule
> "When daily value areas overlap, the market is in balance. When value areas do not overlap and shift directionally, the market is trending. The Value-Area Rule: monitor whether consecutive days' value areas overlap or separate to determine long-term market condition."

---

## 6. FORMULAS_AND_ALGOS

### Formula 1: Value Area Calculation (TPO Method)
1. Identify the price with the greatest number of TPOs (Point of Control)
2. Sum TPOs at POC + 2 prices above vs. POC + 2 prices below
3. Add the side with higher total to the value area
4. Continue until ~70% of total TPOs are included
5. Result: [Value Area Low, Value Area High]
**A股 Proxy**: 用分钟K线成交量分布代替 TPO；从成交量最大价开始，向上下两侧累加，直到覆盖约70%成交量。

### Formula 2: TPO Count (Buyer/Seller Imbalance)
1. Isolate POC (longest line closest to center of range)
2. Sum all TPOs above POC = SELLING_TPOs
3. Sum all TPOs below POC = BUYING_TPOs
4. Exclude single-print tails from count
5. Ratio = SELLING_TPOs / BUYING_TPOs
6. Interpretation:
   - Ratio > 1.2: Seller imbalance in value area
   - Ratio < 0.8: Buyer imbalance in value area
   - Ratio ~1.0: Balanced
**A股 Proxy**: 用分钟级别成交量在 POC 上方/下方的分布比例代替 TPO 比例。

### Formula 3: Rotation Factor
For each period (e.g., 30min):
  IF current_period_high > previous_period_high AND current_period_low > previous_period_low:
    score = +1  (higher rotation)
  ELIF current_period_high < previous_period_high AND current_period_low < previous_period_low:
    score = -1  (lower rotation)
  ELSE:
    score = 0   (overlapping / neutral)

Daily Rotation Factor = sum of all period scores

Interpretation:
  RF > 0: Market rotating higher (upside control)
  RF < 0: Market rotating lower (downside control)
  RF = 0: Balanced rotation
**A股 Proxy**: 用30分钟或60分钟K线直接计算。

### Formula 4: Day Type Classification Algorithm
INPUT: initial_balance_range, total_day_range, close_position, range_extension_direction, volume_profile_shape

IF total_day_range < 1.2 * initial_balance_range:
    IF close_position in middle_50%:
        TYPE = "Neutral Day"
    ELSE:
        TYPE = "Normal Day" (or Normal Variation)
ELIF range_extension_single_direction AND close_near_extreme:
    IF volume_profile_bimodal AND single_prints_separate_distributions:
        TYPE = "Double-Distribution Trend Day"
    ELSE:
        TYPE = "Trend Day"
ELIF total_day_range < 0.8 * avg_daily_range AND volume_low:
    TYPE = "Nontrend Day"
ELSE:
    TYPE = "Normal Variation Day"
**A股 Proxy**: 完全可用 OHLCV + 前日数据实现。

### Formula 5: Opening Type Classification
INPUT: open_price, prev_day_value_area_low, prev_day_value_area_high, prev_day_range_low, prev_day_range_high

IF prev_day_value_area_low <= open_price <= prev_day_value_area_high:
    TYPE = "Open_Within_Value"
ELIF prev_day_range_low <= open_price <= prev_day_range_high:
    TYPE = "Open_Outside_Value_Within_Range"
ELSE:
    TYPE = "Open_Outside_Range"
**A股 Proxy**: 直接用前日数据判断。

### Formula 6: Excess Detection (Tail Identification)
INPUT: price_bars, volume_profile

FOR each extreme price in top/bottom 5% of range:
    IF time_spent_at_price <= 1 period AND price_quickly_reverses:
        excess_score = high
        TYPE = "single_print_tail" (buying or selling)
    ELSE:
        excess_score = low

FOR each price level:
    IF volume_at_price < 5% of POC_volume AND price_at_extreme:
        excess_score = high
**A股 Proxy**: 分钟K线中，某价格仅出现1分钟且快速反转，标记为 excess/tail。

---

## 7. NOT_QUANT_YET

| 对象 | 原因 | 未来数据需求 |
|------|------|-------------|
| **Floor trader / local inventory dynamics** | 依赖于场内交易员持仓和库存平衡，A股无场内本地交易员 | 主力资金流、席位数据、Level2 逐笔 |
| **Single-print true rejection vs. thin market** | 无法区分是"主动拒绝"还是"流动性不足无成交" | 逐笔数据 + 订单簿深度 |
| **Other timeframe participant intent** | 需要识别谁在买/卖（机构/散户/算法） | 席位数据、资金流向、大单拆分识别 |
| **Pit-specific mechanics** | 场内喊价、手势、经纪商优先级 | 仅适用于期货/期权场内市场 |
| **Real-time DOM imbalance** | 实时订单簿倾斜度 | Level2 完整订单簿 |
| **Spike quality (low vs. high volume)** | 需要区分"低量假突破"和"高量真突破" | 分钟/逐笔成交量 + 订单簿变化 |
| **True auction facilitation quality** | 需要衡量"交易促进效率" | 需要市场结构微观数据 |
| **Liquidity Data Bank (LDB)** | 原书依赖 CBOT 的 LDB 数据 | A股无直接等价物；可用逐笔委托+成交近似 |
| **Chinese text translation accuracy** | 部分中文翻译有歧义（如"初始余额"应为"初始平衡"） | 需对照英文原文校验术语 |

---

## 8. NEXT_ACTION

### 可先做状态壳（proxy_quantizable_now）
1. **Day Type Classifier**: 基于 OHLCV + 前日数据，实现 Normal/Trend/Neutral/Nontrend/Double-Distribution 分类器
2. **Initial Balance Calculator**: 开盘后30/60分钟区间计算，标记为 IB_high / IB_low
3. **Value Area / POC Calculator**: 用成交量分布（volume profile）计算日内 70% 区间和成交量峰值价
4. **Opening Type Classifier**: 今日开盘价 vs. 前日 value area / range 的三类分类
5. **Rotation Factor Tracker**: 逐30/60分钟K线计算 +1/-1/0 累加
6. **TPO Count Proxy**: 用分钟成交量在 POC 上方/下方比例近似买方/卖方 imbalance
7. **Excess / Tail Detector**: 分钟K线极端价格快速反转 + 该价位低成交量 标记为 tail
8. **Range Extension Monitor**: 价格突破 IB 后，跟踪延伸幅度和方向
9. **Auction Failure Detector**: 价格突破 value area 后 N 分钟内返回，标记为 auction failure
10. **Initiative/Responsive Classifier**: 基于价格相对于前日 value area 的位置分类

### 先放 future bucket（needs_extra_data）
1. **True DOM Imbalance Scanner**: 需要 Level2 订单簿实时倾斜度
2. **Single Print True Intent Parser**: 需要逐笔数据区分"拒绝"vs"无成交"
3. **Other Timeframe Control Identifier**: 需要识别机构大单/主力资金流
4. **Liquidity Data Bank Reconstruction**: 需要逐笔委托+成交数据重建流动性视图
5. **Market Facilitation Quality Index**: 需要衡量市场促进交易的效率（类似 Market Facilitation Index 但更细）

### 适合和 A股集合竞价/开盘结构对齐的对象
1. **initial balance ↔ 开盘后N分钟区间**: A股 9:30-10:00 的连续竞价区间 = initial balance proxy；可叠加 9:15-9:25 集合竞价结果作为 pre-opening reference
2. **POC ↔ 早盘成交量峰值价**: A股 10:00 前成交量最大价 = 日内 early POC；可结合 VWAP
3. **opening type ↔ 集合竞价开盘位置**: 开盘价相对于前日收盘价/振幅的位置 = Open Within/Outside Value/Range 的直接映射
4. **single prints ↔ 集合竞价/开盘后无成交价格区**: A股集合竞价中的无成交跳空、开盘后某价位无成交 = single print 类似物
5. **excess / tails ↔ 竞价极端价后的快速回归**: 集合竞价极端价格开盘后迅速回归 = tail rejection 现象
6. **responsive activity ↔ 开盘价偏离前日价值后的回归**: A股开盘后若价格远离前日价值区间，观察是否有 responsive 回归力量
7. **auction failure ↔ 假突破**: A股开盘后突破前高/前低但无跟随、迅速返回 = day timeframe auction failure
8. **value area shift ↔ 多日价值区间移动**: A股连续多日 POC / 70% 区间方向性移动 = 长期趋势/平衡判断

---

*End of CUT for Mind Over Markets*


