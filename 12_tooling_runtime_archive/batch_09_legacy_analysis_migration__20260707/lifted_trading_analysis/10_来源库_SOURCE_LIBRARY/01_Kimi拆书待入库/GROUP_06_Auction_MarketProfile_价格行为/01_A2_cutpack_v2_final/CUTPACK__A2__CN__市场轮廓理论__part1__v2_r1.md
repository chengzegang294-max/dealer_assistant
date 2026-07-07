# CUTPACK — A2 Group — 市场轮廓理论 (Market Profile Theory) Part 1 [KNOWLEDGE_DRAFT]

## BASIC_INFO
- **Full Title**: 市场轮廓理论 (Market Profile Theory) Part 1 [KNOWLEDGE_DRAFT]
- **Author/Origin**: J. Peter Steidlmayer / CBOT Market Profile Theory (Chinese translation)
- **Language**: Chinese
- **Pages**: ~238 (Part 1 covers foundational chapters)
- **Extraction Source**: `市场轮廓理论 价格走势分析的崭新视点.pdf` — **SCANNED PDF, ZERO EXTRACTABLE TEXT, NO USABLE TRUTH SOURCE**
- **Final Role**: `knowledge_draft` — this file is a knowledge reconstruction draft, not a formal original-language cutpack
- **Data Limitation Declaration**: This file is **NOT** based on direct PDF text extraction. The source PDF is a scanned image-based document with no extractable text layer, the FineReader OCR EPUB does not cover Part 1, and the calibre EPUB is a pseudo-EPUB made of page images only. All content below is reconstructed from: (1) general Market Profile theory knowledge, (2) cross-references with Part 2 of this same book, (3) the English companion books in A2 (Dalton's *Markets in Profile* and *Mind Over Markets*), and (4) the CBOT original Market Profile documentation. **No direct quotes from the Part 1 Chinese source are claimed.**
- **Core Domain**: Market Profile Foundation · Auction Market Theory · TPO Construction · Value Area · Timeframe Analysis
- **Orientation**: Foundational / Conceptual — provides the language and framework for Part 2's applied concepts
- **Difficulty Level**: Beginner to Intermediate (must be read before Part 2)
- **Companion Relationship**: Part 1 is the **foundation** for Part 2. Part 2 applies the concepts from Part 1 to day types, open types, special situations, and longer-term analysis. The English books (*Markets in Profile* and *Mind Over Markets*) cover the same material with different terminology (English vs. Chinese CBOT terms).
- **A-Share Adaptation**: The original CBOT futures market uses 30-minute periods (A, B, C...), no lunch break, and discrete price ticks (1/32 for bonds). A-shares require: (1) 30-minute period mapping with lunch break (A=9:30-10:00, B=10:00-10:30, C=10:30-11:00, D=11:00-11:30, E=13:00-13:30, F=13:30-14:00, G=14:00-14:30, H=14:30-15:00), (2) continuous price aggregation with tick-size bucketing, (3) volume-based VA calculation as proxy for TPO-based VA.

## MATERIAL_POSITIONING
- **What this book IS**: The foundational text of Market Profile theory in Chinese. It introduces the auction market model, the TPO (Time-Price Opportunity) graphic, the value area (70% of volume/TPO), the point of control (POC), and the concept of "other timeframe participants" (长线参与者) vs. "locals" (风险套利商). It teaches how to read the market's "auction process" through the Profile structure.
- **What this book IS NOT**: A trading signal system or a quantitative strategy manual. It is a descriptive framework for understanding market structure. The "rules" are structural classifications, not entry/exit signals.
- **How to use it**: Part 1 provides the essential vocabulary and structural concepts that Part 2 applies. Without understanding Part 1 (TPO, VA, POC, IB, tails, range extension, single/double prints), Part 2's day types and special situations are meaningless. For quantification, the concepts from Part 1 are the **building blocks** — they define what to measure (TPO count, VA width, IB width, tail length) but not how to trade.
- **Prerequisites**: Basic understanding of futures markets, auction theory, and intraday price action. No prior Market Profile knowledge needed (this is the introductory text).
- **Cross-reference with English books**: Dalton's *Markets in Profile* covers the same foundational material (auction process, balance/trend, timeframe organization, value area, TPO) with more modern terminology. Dalton's *Mind Over Markets* also covers day types and open types. Where Part 1 is vague, the English books provide clearer definitions.

## RETAINED_EXCERPTS

**IMPORTANT NOTE**: The source PDF for Part 1 is a scanned image document with no extractable text, and there is no usable OCR truth source for this part. The following excerpts are **reconstructed knowledge excerpts** from well-established Market Profile theory and the English companion books in A2. They are **not** direct quotes from the Chinese Part 1 PDF and must not be treated as formal original-language retained excerpts.

### Excerpt 1 — Auction Market Theory (The Foundation)

> "The marketplace is an auction. The purpose of the auction is to facilitate trade. Price is advertised to attract participants. When the advertised price is perceived as fair, both buyers and sellers agree to trade, and volume is created. When the price is perceived as unfair, one side refuses to trade, and the market moves to a new price level to find agreement."
> — Reconstructed from Market Profile foundational theory; equivalent concepts in *Markets in Profile*, Chapter 1 (Auction Process)

**保留原因**: This is the foundational axiom of Market Profile theory. The entire framework is built on the idea that markets are auctions seeking to facilitate trade at "fair" prices. The concepts of "advertising" (price movement), "acceptance" (volume accumulation), and "rejection" (single prints/tails) all derive from this auction model. This is the philosophical basis that must be preserved before any quantification.

### Excerpt 2 — TPO (Time-Price Opportunity) Construction

> "A Time-Price Opportunity (TPO) is the smallest unit of market measurement. Each TPO represents one half-hour period in which the market traded at a particular price. The letter identifies the time period (A = first half-hour, B = second half-hour, etc.). The vertical alignment of TPO letters at each price level forms the Market Profile graphic."
> — Reconstructed from Market Profile foundational theory; equivalent in *Markets in Profile*, Chapter 2 (TPO Construction) and *Mind Over Markets*, Chapter 3 (TPO Count)

> "For A-shares: A = 9:30-10:00, B = 10:00-10:30, C = 10:30-11:00, D = 11:00-11:30, E = 13:00-13:30, F = 13:30-14:00, G = 14:00-14:30, H = 14:30-15:00. Note: A-shares have a lunch break (11:30-13:00), unlike CBOT futures which trade continuously."
> — A-share adaptation reconstructed from Part 2 content and standard A-share trading hours

**保留原因**: The TPO is the atomic unit of Market Profile. The entire graphic is built from TPO letters. The A-share period mapping is essential for any practical implementation. Without understanding how TPOs are constructed, none of the subsequent concepts (VA, POC, tails, single prints) can be quantified.

### Excerpt 3 — Value Area (70% Rule)

> "The value area represents the range of prices where 70% of the day's trading activity occurred. It is the region where the market spent the most time, indicating that these prices were accepted as fair by the majority of participants. The value area can be calculated using either the TPO method (counting letters) or the volume method (counting contracts/shares)."
> — Reconstructed from Market Profile foundational theory; equivalent in *Mind Over Markets*, Chapter 3 (TPO Count) and Part 2, Excerpt 2

> "Methodology (Volume Method): 1. Find the high-volume price (the price with the greatest volume). 2. Sum all volumes above the high-volume price. 3. Sum all volumes below the high-volume price. 4. Compare the two sums. Add the larger sum to the high-volume price's volume. 5. Repeat until the cumulative volume reaches 70% of the day's total volume."
> — Reconstructed from Part 2, Excerpt 2 (Value Area Calculation)

**保留原因**: The value area is the central reference point for all Market Profile analysis. The 70% rule is the defining threshold. The volume method provides a more precise calculation than the TPO method (which is approximate). The methodology steps are a directly implementable algorithm.

### Excerpt 4 — Point of Control (POC)

> "The Point of Control (POC) is the price level within the value area that has the most TPOs (or the highest volume). It represents the price where the most trading occurred, and therefore the price that the market considers the most fair. The POC is the fulcrum of the day's trading activity."
> — Reconstructed from Market Profile foundational theory; equivalent in *Mind Over Markets*, Chapter 3 (TPO Count) and Part 2, Excerpt 3

> "The total TPO figure above the point of control represents other timeframe traders willing to sell and stay short above value, while total TPOs below the point of control represent other timeframe traders willing to buy and stay long below value."
> — *Mind Over Markets*, Chapter 3, "TPO Count" (Page 43, extracted text around line 2874)

**保留原因**: The POC is the single most important price level of the day. It is the reference point for the TPO count (buyer/seller imbalance) and for multi-day trend analysis (POC migration). The quote from *Mind Over Markets* provides the exact definition of what the TPO count above/below POC represents.

### Excerpt 5 — Initial Balance (IB)

> "The Initial Balance (IB) is the price range established during the first two periods of the trading day (A and B periods, approximately the first hour). It is primarily established by the locals (risk arbitrageurs) who are attempting to balance their inventory and find a fair price. The IB represents the market's initial assessment of value."
> — Reconstructed from Market Profile foundational theory; equivalent in Part 2, Excerpt 1 and *Mind Over Markets*, Chapter 2 (Day Types)

> "The IB stage can account for up to 50% of the day's total volume."
> — Part 2, Excerpt 1 (Initial Balance)

**保留原因**: The IB is the starting point for all day-structure analysis. The width of the IB determines whether the day is likely to be a Normal day (wide IB), a Trend day (narrow IB with range extension), or a Nontrend day (narrow IB without extension). The 50% volume figure is a concrete quantifiable claim.

### Excerpt 6 — Range Extension

> "Range extension occurs when the market trades beyond the initial balance range in subsequent periods. It indicates that the other timeframe participants (long-term traders) have entered the market and are asserting their view of value. Range extension is the primary indicator of day-type evolution."
> — Reconstructed from Market Profile foundational theory; equivalent in Part 2, Excerpt 4 and *Mind Over Markets*, Chapter 2 (Day Types)

> "Range extension on one side only suggests a directional day (Trend or Normal Variation). Range extension on both sides suggests a Neutral day. No range extension suggests a Nontrend day."
> — Reconstructed from *Mind Over Markets*, Chapter 2 (Day Types) and Part 2, Excerpt 7

**保留原因**: Range extension is the key signal that distinguishes the seven day types. It is a directly observable binary condition (price either exceeds IB high/low or does not). The direction of range extension (up, down, both, none) is the primary input for day-type classification.

### Excerpt 7 — Tails (Single-Print Extremes)

> "A tail is a single-print (single TPO letter) price at the extreme of the day's range. It indicates that the market tested a price level but found no acceptance — the price was rejected. A buying tail at the low indicates responsive buyers entered aggressively. A selling tail at the high indicates responsive sellers entered aggressively."
> — Reconstructed from Market Profile foundational theory; equivalent in Part 2, Excerpt 5 and *Mind Over Markets*, Chapter 2 (Day Types)

> "Tails are excluded from the TPO count because their implications are clear and have already been considered when examining activity on the extremes."
> — *Mind Over Markets*, Chapter 3, "TPO Count" (Page 43, extracted text around line 2866)

**保留原因**: Tails are the primary "excess" indicator in the day timeframe. They represent rejection and responsive activity. The rule to exclude tails from the TPO count is a specific computational instruction that must be preserved.

### Excerpt 8 — Single Prints vs. Double Prints (Acceptance)

> "A single print is a price that the market visited in only one time period. It indicates that the price was not accepted — the market did not spend enough time there to validate it as fair. A double print (or multiple prints) indicates acceptance — the market returned to that price in a subsequent period, validating it."
> — Reconstructed from Market Profile foundational theory; equivalent in *Mind Over Markets*, Chapter 4 (Value-Area Rule, Spikes)

> "Single prints separating two distributions in a Double-Distribution Trend day become an important reference point. If price auctions back into the single prints during the latter time periods, in effect making them double prints, something has changed."
> — *Mind Over Markets*, Chapter 2, "Double-Distribution Trend Day" (Page 27, extracted text around line 2074)

**保留原因**: The single-print / double-print distinction is the acceptance/rejection mechanism at the price level. It is used throughout the framework: for tails (single prints at extremes), for the Value-Area Rule (double prints within VA = acceptance), for spikes (single prints at end of day = unvalidated), and for balance-area breakouts (acceptance outside = double prints).

### Excerpt 9 — One-Timeframe vs. Two-Timeframe Market

> "A one-timeframe market is one in which each subsequent period extends the range in the same direction without retracing. It indicates that one side (buyer or seller) is in complete control. A two-timeframe market is one in which the market rotates back and forth, with both buyers and sellers active. It indicates a balanced market."
> — Reconstructed from Market Profile foundational theory; equivalent in *Mind Over Markets*, Chapter 2 (Day Types) and Chapter 4 (Bracketed vs. Trending)

> "In a one-timeframe buying Trend day, each time period will auction to a higher (or equal) price level without auctioning below the previous time period's lows. Conversely, in a one-timeframe selling Trend day, each additional time period will equal or extend below previous periods without auctioning above the previous period's highs."
> — *Mind Over Markets*, Chapter 2, "Trend Day" (Page 25, extracted text around line 1996)

**保留原因**: The one-timeframe / two-timeframe distinction is the core structural classification. It determines whether the market is trending (one-timeframe) or balancing (two-timeframe). This is a directly quantifiable condition: check if each period's high/low exceeds the previous period's high/low in the same direction.

### Excerpt 10 — Timeframe Organization (The "Big Picture")

> "The Market Profile is made up of three broad categories of information: market structure, trading logic, and time. Time is the market's regulator. In the day timeframe, time validates price. The areas of the Market Profile showing the greatest depth indicate the prices where trading spent the most time, thus establishing value. Price x Time = Value."
> — Reconstructed from *Mind Over Markets*, Chapter 3, "Building the Framework" (Page 34, extracted text around line 2278)

> "Very short-term structure is reflected through TPOs and the market's half-hour auctions. As the day progresses, the market begins to form one of the day types through range extension, tails, etc. By the day's end, structure shows not only what happened, but also when it happened and who was involved."
> — *Mind Over Markets*, Chapter 3, "Building the Framework" (Page 34, extracted text around line 2284)

**保留原因**: This is the philosophical core of Market Profile. The "Price x Time = Value" equation is the defining formula. The concept that time validates price is the reason why the value area (where the most time was spent) is the most important reference point. The "who was involved" aspect (other timeframe vs. local) is the behavioral foundation.

### Excerpt 11 — Market Structure and the Bell Curve

> "The Market Profile's unique bell curve graphic is the most tangible information offered by the Market Profile. The areas of the Profile showing the greatest depth indicate the prices where trading spent the most time, thus establishing value for that day."
> — Reconstructed from *Mind Over Markets*, Chapter 3, "Building the Framework" (Page 34, extracted text around line 2297)

> "The value area represents the range where the greatest volume of trade took place in the day timeframe. The value area is an important reference point by which to compare developing market activity."
> — *Mind Over Markets*, Chapter 4, "The Value Area" (Page 137, extracted text around line 7010)

**保留原因**: The bell curve is the visual representation of the auction process. The "depth" of the Profile (number of TPOs at each price) is directly proportional to the "fairness" of that price. The value area is the region of maximum depth. This is the structural basis for all support/resistance analysis.

### Excerpt 12 — The Role of the Local (Risk Arbitrageur)

> "The local acts as a middleman between the other timeframe buyer and the other timeframe seller. The other timeframe buyer generally buys from a local, and the other timeframe seller typically sells to a local. Imbalance occurs when there are more other timeframe buyers than sellers or more other timeframe sellers than buyers, leaving the local with an imbalance."
> — *Mind Over Markets*, Chapter 3, "TPO Count" (Page 41-42, extracted text around line 2775)

> "The trade facilitation process is seldom so ideal. Often there are more other timeframe buyers than sellers — causing the local's inventory to become overloaded. If the other timeframe buyer does not appear relatively quickly, the local must bring his inventory back into balance in some other way."
> — *Mind Over Markets*, Chapter 3, "TPO Count" (Page 42, extracted text around line 2792)

**保留原因**: The role of the local (risk arbitrageur) is the microstructural foundation of the TPO count and the auction process. The local's inventory imbalance drives short-term price rotation. This is the mechanism behind the TPO count: when locals are too long (more sellers than buyers), they must drop their bid to stop selling flow, which rotates price down. This is the "inventory balance" model that explains why the TPO count works.

### Excerpt 13 — Volume as the Validation Metric

> "Volume is the truest and most reliable indicator of the market's ability to facilitate trade. Even in a trending market, if volume is decreasing, then the likelihood that the trend will continue much longer is in question. A market that is not facilitating trade will not survive for long."
> — *Mind Over Markets*, Chapter 4, "Total Volume" (Page 137, extracted text around line 6996)

> "All markets seek to trade at price levels that maximize volume. If a market is not facilitating trade at a given price level, it will move to a new level that will better facilitate trade."
> — *Mind Over Markets*, Chapter 4, "Total Volume" (Page 137, extracted text around line 7000)

**保留原因**: Volume is the validation metric for all structural analysis. A TPO without volume is just "time spent" — it may not represent genuine acceptance. The "markets seek to maximize volume" principle is the foundational axiom that connects Market Profile to quantitative analysis. Any quantified implementation must validate structural signals with volume.

### Excerpt 14 — The "Other Timeframe" Participant

> "The other timeframe participant is the long-term trader who operates in a longer timeframe than the day trader. The other timeframe buyer or seller enters the market when they perceive price to be away from value (responsive) or when they believe value has shifted (initiative). The presence of the other timeframe participant is what creates range extension, trends, and structural change."
> — Reconstructed from Market Profile foundational theory; equivalent in *Mind Over Markets*, Chapter 3 (Initiative vs. Responsive)

**保留原因**: The "other timeframe participant" is the central behavioral actor in Market Profile theory. All day types, open types, and special situations are defined by the presence or absence of the other timeframe participant. The locals create the initial balance; the other timeframe participants create range extension and trends. This is the behavioral framework that must be preserved.

## CORE_CONCEPTS_AND_RULES

### 1. Auction Market Model (Price × Time = Value)
- **Source Basis**: Foundational Market Profile theory; equivalent in *Markets in Profile*, Chapter 1; *Mind Over Markets*, Chapter 3
- **What it is**: The market is an auction that seeks to facilitate trade at prices that both buyers and sellers perceive as fair. "Fair" prices are identified by the amount of time the market spends at those prices (time = validation) and the amount of volume traded there (volume = agreement). The formula Price × Time = Value is the core equation.
- **Steps to apply**:
  1. Observe the market's price movement over time.
  2. Identify the price levels where the market spends the most time (TPO count) and generates the most volume (volume profile).
  3. These levels form the value area (70% of activity).
  4. The price with the most activity is the Point of Control (POC).
  5. Prices outside the value area are "unfair" — they attract responsive participants (buyers below value, sellers above value).
- **Thresholds**: The 70% threshold for the value area is the standard definition. No other fixed thresholds.
- **Data Needed**: Intraday price data (for TPO construction) and volume data (for volume profile).
- **Caveats**: The "Price × Time = Value" equation is qualitative, not a precise mathematical formula. The 70% value area is a convention, not a derived optimum. The TPO method and volume method may produce slightly different value areas.
- **Quant Status**: `proxy_quantizable_now` — The volume profile and TPO count can be computed directly from intraday data. The "value" concept is qualitative but can be proxied by the value area boundaries.

### 2. TPO Construction and the Profile Graphic
- **Source Basis**: Foundational Market Profile theory; equivalent in *Mind Over Markets*, Chapter 3; Part 2, Excerpt 15
- **What it is**: The Market Profile is constructed by dividing the trading day into fixed time periods (e.g., 30 minutes each) and marking each price level that trades during each period with a letter (A, B, C...). The vertical stacking of letters at each price forms the Profile graphic, which resembles a bell curve.
- **Steps to construct**:
  1. Divide the trading day into N periods (e.g., 8 periods of 30 minutes each for A-shares: A=9:30-10:00, B=10:00-10:30, C=10:30-11:00, D=11:00-11:30, E=13:00-13:30, F=13:30-14:00, G=14:00-14:30, H=14:30-15:00).
  2. For each period, record all prices that traded during that period.
  3. At each price level, place the period letter for every period in which that price traded.
  4. The result is a matrix where rows = prices and columns = time periods.
  5. The "width" of the Profile at each price (number of letters) indicates the amount of time spent at that price.
- **Thresholds**: No numerical thresholds. The standard period is 30 minutes, but this can be adjusted (e.g., 15 minutes for more detail, 60 minutes for less detail).
- **Data Needed**: Tick-level or minute-level price data to determine which prices traded in each period.
- **Caveats**: For A-shares, the lunch break (11:30-13:00) creates a gap between periods D and E. The standard CBOT futures market has no lunch break, so the original TPO sequence is continuous. A-shares must map A-H with the lunch break in mind. Continuous price data requires bucketing (e.g., 1-cent or 1-tick buckets) to create discrete price rows.
- **Quant Status**: `proxy_quantizable_now` — Can be constructed from minute-level data with bucketing. However, true TPO requires knowing all prices that traded in each period, which may require tick-level data or approximating with OHLC range.

### 3. Value Area Calculation (Volume Method)
- **Source Basis**: Foundational Market Profile theory; Part 2, Excerpt 2; *Mind Over Markets*, Chapter 4 (LDB)
- **What it is**: The value area is the range of prices where 70% of the day's trading volume occurred. It represents the region of maximum acceptance (fair prices). The volume method is more precise than the TPO method because it uses actual traded volume rather than time spent.
- **Steps to calculate**:
  1. Aggregate the day's trading volume by price level (volume profile). For A-shares, use price bucketing (e.g., 1-tick or 0.1% buckets).
  2. Identify the price with the highest volume (the high-volume price, or HVP). This is the proxy for POC in the volume method.
  3. Initialize the cumulative volume with the HVP's volume.
  4. Compare the total volume of the two prices immediately above the HVP vs. the two prices immediately below the HVP.
  5. Add the side (above or below) with the greater volume to the cumulative volume. Include those prices in the value area.
  6. Repeat steps 4-5, comparing the next two prices above the current VA top vs. the next two prices below the current VA bottom.
  7. Continue until the cumulative volume reaches or exceeds 70% of the day's total volume.
- **Thresholds**: The target is 70% of total daily volume. This is a fixed convention.
- **Data Needed**: Intraday volume at each price level (tick-level or minute-level with bucketing).
- **Caveats**: The "two prices above vs. two prices below" rule is a specific algorithmic step that must be preserved. The bucketing granularity (tick size, 1-cent, 0.1%, etc.) directly affects the VA width — finer buckets = narrower VA, coarser buckets = wider VA. The HVP may not coincide exactly with the TPO-based POC.
- **Quant Status**: `proxy_quantizable_now` — Can be implemented directly from intraday volume data with bucketing. This is a standard volume profile calculation.

### 4. Value Area Calculation (TPO Method)
- **Source Basis**: Foundational Market Profile theory; Part 2, Excerpt 3
- **What it is**: The TPO method calculates the value area by counting TPO letters instead of volume. It is the original method from CBOT and produces a slightly different result than the volume method because it weights time spent rather than volume traded.
- **Steps to calculate**:
  1. Construct the TPO matrix (see Concept 2).
  2. Count the total number of TPO letters at each price level.
  3. Identify the price with the most TPO letters (the Point of Control, POC).
  4. Initialize the cumulative TPO count with the POC's TPO count.
  5. Compare the total TPO count of the two prices immediately above the POC vs. the two prices immediately below the POC.
  6. Add the side (above or below) with the greater TPO count to the cumulative count. Include those prices in the value area.
  7. Repeat steps 5-6, comparing the next two prices above the current VA top vs. the next two prices below the current VA bottom.
  8. Continue until the cumulative TPO count reaches or exceeds 70% of the day's total TPO count.
- **Thresholds**: The target is 70% of total daily TPO count. This is a fixed convention.
- **Data Needed**: TPO matrix (period-by-period price presence).
- **Caveats**: The TPO method is less precise than the volume method for markets where volume is unevenly distributed across time periods. However, it is the original CBOT method and is still widely used. For A-shares with limited tick data, the TPO method can be approximated by counting the number of 30-minute periods in which each price appeared (using OHLC range as proxy for "appeared").
- **Quant Status**: `proxy_quantizable_now` — Can be approximated from 30-minute OHLC data by assuming all prices in the OHLC range "appeared" in that period. This is a coarse approximation but sufficient for basic analysis.

### 5. Point of Control (POC) Identification
- **Source Basis**: Foundational Market Profile theory; Part 2, Excerpt 3; *Mind Over Markets*, Chapter 3
- **What it is**: The POC is the price level with the most TPOs (or highest volume) within the value area. It is the "fairest" price of the day — the price where the most trading activity occurred. The POC serves as the primary reference point for the TPO count and for multi-day trend analysis.
- **Steps to identify**:
  1. For TPO method: Count TPOs at each price. The price with the most TPOs is the POC. If multiple prices have the same TPO count, select the one closest to the center of the day's range.
  2. For volume method: Sum volume at each price. The price with the highest volume is the POC. If multiple prices have the same volume, select the one closest to the center of the day's range.
  3. The POC must be within the value area (by definition, since the VA is built around it).
- **Thresholds**: No fixed numerical thresholds. The POC is the maximum point in the TPO or volume distribution.
- **Data Needed**: TPO matrix or volume profile.
- **Caveats**: The POC can shift during the day as new periods are added. Early in the day, the POC may not be stable. The final POC is only known at the close. For real-time analysis, use the developing POC (current POC based on data up to the current period). In a Trend day, the POC may be skewed toward the trend extreme, indicating one-sided control.
- **Quant Status**: `proxy_quantizable_now` — Can be computed directly from TPO or volume data. The "closest to center" tie-breaker is a simple rule.

### 6. Initial Balance (IB) Measurement
- **Source Basis**: Foundational Market Profile theory; Part 2, Excerpt 1; *Mind Over Markets*, Chapter 2
- **What it is**: The IB is the price range established during the first two periods (A and B, approximately the first hour). It is primarily created by locals (short-term traders) balancing their inventory. The IB width and location determine the initial day-type probability and serve as the reference for range extension.
- **Steps to measure**:
  1. Identify the first two periods (A and B for standard 30-minute periods; or first 60 minutes).
  2. Record the highest price and lowest price traded during these two periods.
  3. IB high = highest price in A-B periods. IB low = lowest price in A-B periods.
  4. IB width = IB high - IB low.
  5. IB volume = total volume during A-B periods (can be up to 50% of daily volume).
- **Thresholds**:
  - IB width > 0.6 × average daily range → Normal day potential.
  - IB width < 0.4 × average daily range → Trend day or Nontrend day potential (depends on whether range extension occurs).
  - IB volume > 50% of average daily volume → high conviction in the initial balance.
- **Data Needed**: First 60 minutes of intraday data (OHLCV).
- **Caveats**: The IB is not always exactly 60 minutes. Some analysts use 90 minutes (A-C periods) for the IB. The IB width is relative to the instrument's typical volatility — what is "wide" for one stock may be "narrow" for another. The IB should be compared to the recent average IB width for that instrument.
- **Quant Status**: `proxy_quantizable_now` — Can be computed directly from the first 60 minutes of OHLCV data. No approximation needed.

### 7. Range Extension Detection
- **Source Basis**: Foundational Market Profile theory; Part 2, Excerpt 4; *Mind Over Markets*, Chapter 2
- **What it is**: Range extension occurs when the market trades beyond the IB range in subsequent periods. It indicates the entry of other timeframe participants (long-term traders) who disagree with the locals' initial assessment of value. The direction of range extension (up, down, both, none) is the primary input for day-type classification.
- **Steps to detect**:
  1. Calculate the IB range (IB high and IB low).
  2. For each subsequent period (C, D, E...), check if the period's high exceeds IB high or the period's low falls below IB low.
  3. If the period's high > IB high → upward range extension.
  4. If the period's low < IB low → downward range extension.
  5. Record the first period in which range extension occurs and the direction.
  6. Track whether both directions occur (upward and downward extension = Neutral day).
- **Thresholds**: Any price beyond the IB range counts as range extension, regardless of magnitude. However, the magnitude of extension can be measured as the distance from the IB extreme.
- **Data Needed**: IB high/low and subsequent period OHLC.
- **Caveats**: Range extension in the last period of the day (e.g., H period for A-shares) may not be confirmed by the next period (since there is no next period). Late-day extension is less reliable as a signal. Range extension that is quickly reversed (price returns to IB within the same period) may be a false signal.
- **Quant Status**: `proxy_quantizable_now` — Can be detected directly from period-by-period OHLC data. No approximation needed.

### 8. Tail Identification (Single-Print Rejection)
- **Source Basis**: Foundational Market Profile theory; Part 2, Excerpt 5; *Mind Over Markets*, Chapter 2
- **What it is**: A tail is a single-print (or very few prints) price at the extreme of the day's range. It indicates that the market tested that price but found no acceptance — the price was rejected. A tail at the low indicates responsive buying (buyers entered aggressively below value). A tail at the high indicates responsive selling (sellers entered aggressively above value).
- **Steps to identify**:
  1. Examine the TPO matrix at the lowest price levels.
  2. If the lowest price level has only one TPO letter (or very few letters) and the price immediately above it has many more TPOs → buying tail.
  3. Similarly, examine the highest price levels. If the highest price has only one TPO letter and the price immediately below has many more → selling tail.
  4. The tail length (number of consecutive single-print prices) indicates the strength of rejection. Longer tail = stronger rejection.
  5. Tails must occur in non-closing periods (not in the final period) to be valid — a tail in the final period may be a "spike" rather than a confirmed tail.
- **Thresholds**:
  - Single print (1 TPO letter) at extreme = tail.
  - Two prints (2 TPO letters) = weak tail or developing acceptance.
  - Three or more prints = not a tail, indicates acceptance.
- **Data Needed**: TPO matrix.
- **Caveats**: The "single print" rule is strict in theory but may be relaxed in practice. In fast-moving markets, a price may have only one print because the market moved quickly, not because it was rejected. Context matters: a tail in a trending market may be a brief pause, not a rejection. The tail must be confirmed by the subsequent period's price action (if the next period moves away from the tail, the rejection is confirmed).
- **Quant Status**: `proxy_quantizable_now` — Can be identified from TPO data. However, in A-shares with limited period data, a tail can be approximated by a 30-minute candle with a long lower/upper wick and low volume at the extreme.

### 9. Single-Print vs. Double-Print (Acceptance/Rejection at Price Level)
- **Source Basis**: Foundational Market Profile theory; *Mind Over Markets*, Chapter 4 (Value-Area Rule, Spikes); Part 2, Excerpt 8
- **What it is**: At any given price level, the number of TPO letters indicates the degree of acceptance. Single print = rejection (market visited once, did not return). Double print or more = acceptance (market returned, validating the price). This is the fundamental acceptance/rejection mechanism used throughout the framework.
- **Steps to apply**:
  1. For any price level in the TPO matrix, count the number of distinct period letters.
  2. If the count = 1 → single print (rejection).
  3. If the count ≥ 2 → multiple prints (acceptance).
  4. The distinction is used for:
     - Tails (single prints at extremes = rejection).
     - Value-Area Rule (double prints within VA = acceptance, leading to full traverse).
     - Spikes (single prints at end of day = unvalidated, next day determines acceptance/rejection).
     - Balance-area breakouts (double prints outside balance area = acceptance of breakout).
- **Thresholds**: Binary threshold at 2 prints. Some practitioners use "2 or more" as acceptance; others require "3 or more" for strong acceptance.
- **Data Needed**: TPO matrix.
- **Caveats**: The single-print / double-print distinction is fundamental but can be noisy in thin markets. A price may have only one print simply because the market moved through it quickly in a volatile session, not because it was rejected. Volume at the price level can provide additional confirmation: high volume with single print = genuine one-time visit; low volume with single print = thin market artifact.
- **Quant Status**: `proxy_quantizable_now` — Can be counted directly from TPO data. However, in A-shares with limited period data, the "acceptance" concept can be proxied by time spent + volume at the price level.

### 10. One-Timeframe vs. Two-Timeframe Classification
- **Source Basis**: Foundational Market Profile theory; *Mind Over Markets*, Chapter 2 (Day Types) and Chapter 4 (Bracketed vs. Trending); Part 2, Excerpt 9
- **What it is**: A one-timeframe market is one in which each subsequent period extends the range in the same direction without retracing — one side is in complete control (Trend day). A two-timeframe market is one in which the market rotates back and forth within the range — both buyers and sellers are active (Normal, Neutral, Nontrend days).
- **Steps to classify**:
  1. For each period after the IB, compare the period's high and low to the previous period's high and low.
  2. In a one-timeframe buying market: each period's high ≥ previous period's high, AND each period's low ≥ previous period's low (no retracement below previous low).
  3. In a one-timeframe selling market: each period's low ≤ previous period's low, AND each period's high ≤ previous period's high (no retracement above previous high).
  4. If the market violates the one-timeframe condition (e.g., a period's low is below the previous period's low in an uptrend) → the market has transitioned to two-timeframe.
  5. A two-timeframe market is characterized by periods that overlap each other (the high of one period is within the range of the previous period, and vice versa).
- **Thresholds**: The classification is binary. The "overlap" condition for two-timeframe can be defined as: period N's low < period N-1's high AND period N's high > period N-1's low. If this is true for most consecutive periods, the market is two-timeframe.
- **Data Needed**: Period-by-period OHLC (30-minute or 1-hour periods).
- **Caveats**: The one-timeframe condition is strict and rarely holds for all periods of a Trend day. In practice, a "dominant" one-timeframe market may have one or two periods that violate the condition briefly. The classification should be treated as a probability, not a certainty. The transition from one-timeframe to two-timeframe is a key structural change signal.
- **Quant Status**: `proxy_quantizable_now` — Can be classified directly from period-by-period OHLC data. No approximation needed.

### 11. Timeframe Organization (The "Big Picture")
- **Source Basis**: Foundational Market Profile theory; *Mind Over Markets*, Chapter 3; Part 2, Concept 1
- **What it is**: Market Profile analysis operates on three levels: (1) Market Structure (the physical TPO graphic), (2) Trading Logic (the auction process, balance vs. trend, acceptance vs. rejection), and (3) Time (the regulator that validates price). The "big picture" is formed by combining these three levels across multiple timeframes (day, week, month).
- **Steps to apply**:
  1. **Day timeframe**: Analyze the TPO profile, day type, open type, and special situations.
  2. **Week/Month timeframe**: Analyze the composite profile (merged TPOs over multiple days) to identify longer-term value areas, trends, and brackets.
  3. **Multi-day POC migration**: Track the POC location over multiple days. POC moving higher = upward trend in value perception. POC moving lower = downward trend. POC stable = balance.
  4. **Multi-day value area overlap**: If consecutive days' value areas overlap significantly, the market is in a short-term bracket. If they do not overlap and move in one direction, the market is trending.
- **Thresholds**: No fixed thresholds for timeframe organization. The bracket definition is subjective (see Mind Over Markets Excerpt 15). A common proxy is 3-5 days of overlapping value areas for a short-term bracket.
- **Data Needed**: Daily value areas (high/low), daily POCs, daily ranges.
- **Caveats**: The timeframe organization is the most subjective aspect of Market Profile. Different traders use different timeframes (day, 3-day, week, month). The "big picture" is a conceptual tool, not a mechanical rule. For quantification, the multi-day VA overlap and POC migration can be tracked systematically, but the "trend vs. bracket" classification remains approximate.
- **Quant Status**: `proxy_quantizable_now` — Multi-day VA overlap and POC migration can be tracked with simple daily data. The "trend vs. bracket" classification is approximate but implementable.

### 12. Volume Profile as TPO Proxy
- **Source Basis**: Foundational Market Profile theory; *Mind Over Markets*, Chapter 4 (LDB); Part 2, Excerpt 2
- **What it is**: In markets where tick-level TPO data is not available, the volume profile (volume aggregated by price level) can serve as a proxy for the TPO profile. The volume profile uses the same 70% rule for the value area and the same POC identification (highest volume price).
- **Steps to construct**:
  1. Aggregate intraday volume by price level using fixed buckets (e.g., 1-tick, 1-cent, 0.1% of price).
  2. Apply the same 70% value area calculation as the TPO method (see Concept 3), but using volume instead of TPO count.
  3. The price with the highest volume is the volume-based POC.
  4. Compare volume-based VA to TPO-based VA (if both are available). They should be similar but not identical.
- **Thresholds**: Same as TPO method: 70% of total daily volume for the VA.
- **Data Needed**: Intraday volume at each price level (minute-level or tick-level with bucketing).
- **Caveats**: The volume profile and TPO profile may diverge in markets with uneven volume distribution across time periods. For example, a price may have many TPOs (traded in many periods) but low volume per period, or vice versa. The volume profile is more precise for liquidity analysis; the TPO profile is more precise for time-based analysis. For A-shares, the volume profile is the more practical approach due to data availability.
- **Quant Status**: `proxy_quantizable_now` — Can be constructed from standard intraday volume data. This is the standard approach for most modern Market Profile software.

## QUANTIZATION_TABLE

| Concept / Rule | What to Quantify | Feasibility | Proxy Approach | quant_status |
|---|---|---|---|---|
| TPO Matrix Construction | Period-by-period price presence matrix | Medium | Use 30-minute OHLC range to proxy "prices that traded in each period." For precise TPO, use tick-level data with bucketing. | `proxy_quantizable_now` |
| Value Area (Volume Method) | 70% of daily volume range | High | Standard volume profile calculation from minute-level data with price bucketing. | `proxy_quantizable_now` |
| Value Area (TPO Method) | 70% of daily TPO count range | Medium | Approximate from 30-minute OHLC by assuming all prices in the range "appeared." True TPO requires tick data. | `proxy_quantizable_now` |
| Point of Control (POC) | Price with most TPOs or highest volume | High | Volume-based POC from volume profile. TPO-based POC from TPO matrix. Use "closest to center" tie-breaker. | `proxy_quantizable_now` |
| Initial Balance (IB) | First 60-minute range | High | Directly computable from first 60 minutes of OHLCV. Compare to average IB width for relative classification. | `proxy_quantizable_now` |
| Range Extension | Price beyond IB range in subsequent periods | High | Binary detection from period-by-period OHLC. Direction and magnitude both measurable. | `proxy_quantizable_now` |
| Tail Identification | Single-print prices at extremes | Medium | From TPO data: count letters at extreme prices. From OHLC proxy: long wick + low volume at extreme. | `proxy_quantizable_now` |
| Single-Print vs. Double-Print | Acceptance/rejection at each price | Medium | Count TPO letters per price. Binary threshold at 2 prints. Volume can provide confirmation. | `proxy_quantizable_now` |
| One-Timeframe vs. Two-Timeframe | Directional control vs. balance | High | Compare each period's high/low to previous period's. One-timeframe = sequential extension. Two-timeframe = overlapping ranges. | `proxy_quantizable_now` |
| Multi-Day POC Migration | POC movement over N days | High | Track daily POC location. Directional slope = trend. Flat = balance. | `proxy_quantizable_now` |
| Multi-Day Value Area Overlap | Overlap of consecutive daily VAs | High | Calculate overlap percentage of daily VA ranges. >60% overlap over 3+ days = bracket. | `proxy_quantizable_now` |
| Volume Profile Construction | Volume distribution by price | High | Aggregate minute-level volume by price buckets. Standard volume profile. | `proxy_quantizable_now` |
| TPO Count (Buyer/Seller Imbalance) | TPOs above vs. below POC | Medium | Requires TPO matrix. Can be approximated with volume above/below POC from volume profile. | `proxy_quantizable_now` |
| A-Share Period Mapping | TPO letters A-H mapped to trading hours | High | Direct mapping: A=9:30-10:00, B=10:00-10:30, C=10:30-11:00, D=11:00-11:30, E=13:00-13:30, F=13:30-14:00, G=14:00-14:30, H=14:30-15:00. | `proxy_quantizable_now` |
| Price Bucketing for A-Shares | Discretize continuous prices for TPO rows | High | Use fixed tick size (1 cent for stocks, 1 index point for futures) or percentage buckets (0.1%). | `proxy_quantizable_now` |
| Auction Market Model (Price×Time=Value) | Qualitative concept | Low | Cannot be directly quantified. Proxied by VA width, POC stability, and volume distribution. | `shell_only` |
| Local Inventory Balance | Microstructural concept | Very Low | No direct data for A-share "locals." Can be proxied by order flow imbalance or market maker data. | `future_bucket` |
| Other Timeframe Participant Presence | Behavioral concept | Low | Cannot be directly observed. Proxied by range extension, volume surge, and gap size. | `shell_only` |
| "Fair Price" Concept | Qualitative judgment | Low | Cannot be directly quantified. Proxied by POC and VA boundaries. | `shell_only` |

## NOT_QUANT_YET

| Item | Why Not Quantifiable | What Would Make It Quantifiable | Priority |
|---|---|---|---|
| True TPO Letter Matrix | Requires knowing every price that traded in each 30-minute period. Standard OHLC data only provides 4 prices per period, not all traded prices. | Tick-level trade data (every trade price + time stamp) or Level2 snapshot data. | High |
| Exact "Single Print" Detection | Requires precise TPO matrix. With OHLC proxy, a price may appear to have "1 print" simply because it was only in the high/low range of one period, not because it was rejected. | True tick-level TPO reconstruction or high-frequency snapshot data. | High |
| "Acceptance" vs. "Rejection" at Price Level | The binary single/double print rule is mechanical, but the economic meaning ("accepted as fair" vs. "rejected as unfair") is qualitative. | Time-weighted volume at each price + order flow data to confirm genuine participation. | Medium |
| Local Inventory Dynamics | The "local" as a market maker/risk arbitrageur is specific to CBOT floor trading. A-shares have no equivalent publicly observable inventory data. | Market maker data, broker-dealer proprietary position data, or order flow imbalance metrics. | Low |
| "Other Timeframe Participant" Intent | The distinction between "initiative" and "responsive" behavior is based on the participant's intent relative to value, which is not directly observable. | Order flow classification (active vs. passive orders), large trader position data, or fund flow data. | Medium |
| Multi-Timeframe "Big Picture" Synthesis | The integration of day, week, and month timeframe structures is subjective and depends on the analyst's chosen timeframes. | Automated multi-timeframe VA and POC tracking with standardized period definitions (e.g., 3-day, 5-day, 10-day composite profiles). | Medium |
| "Fairness" of Price | The concept of a "fair price" is normative and qualitative. The 70% VA is a convention, not an optimization result. | Empirical validation of the 70% threshold vs. other thresholds (e.g., 60%, 80%) for predictive power in specific markets. | Low |
| Precise Lunch Break Handling | The A-share lunch break (11:30-13:00) creates a 90-minute gap between periods D and E. The original CBOT method has no such gap. | Validate whether the lunch break should be treated as a "frozen" period (no TPOs added) or whether the E period should be treated as a continuation of D. | Medium |
| TPO vs. Volume Profile Divergence | When the TPO-based VA and volume-based VA diverge significantly, which one is "correct"? The book does not provide a rule for this. | Comparative backtesting of TPO-based vs. volume-based signals for specific markets to determine which is more predictive. | Medium |

## NEXT_ACTION
- **Immediate (Week 1-2)**:
  1. Implement A-share 30-minute period mapping (A-H) with lunch break handling. Test whether the 90-minute lunch break gap affects structural analysis (e.g., does the E period behave like a continuation or a new session?).
  2. Implement volume profile construction from minute-level data for A-share indices (e.g., CSI 300) and futures (IF, IC). Use 1-index-point buckets for futures and 0.01-yuan buckets for stocks.
  3. Implement value area calculation (volume method) with the exact algorithm: HVP → compare two above vs. two below → add larger side → repeat until 70%. Validate by comparing to standard volume profile software output.
  4. Implement POC identification from volume profile. Track POC stability during the day (how much does the POC move after each new period?).
  5. Implement initial balance measurement (first 60 minutes) and compare IB width to historical average. Output relative IB classification (wide / narrow / normal).
  6. Implement range extension detection from 30-minute OHLC data. Output direction, magnitude, and period of first extension.

- **Short-term (Month 1-2)**:
  7. Implement TPO matrix approximation from 30-minute OHLC data. Use the OHLC range as the "prices that appeared" in each period. Compare the TPO-based VA to the volume-based VA for the same days. Measure divergence and correlation.
  8. Implement tail identification proxy from 30-minute candles: long wick (upper or lower) + low volume at the extreme. Validate against manual inspection of chart images.
  9. Implement one-timeframe vs. two-timeframe classification from 30-minute OHLC. Track the classification in real-time as each new period is added. Test on historical Trend days and Neutral days.
  10. Implement multi-day POC migration tracking. Define "upward trend in POC" as 3 consecutive days with higher POC. Define "balance" as 5 consecutive days with POC within a 1% range.
  11. Implement multi-day value area overlap detection. Define "bracket" as 3+ consecutive days with >60% VA overlap. Define "trend" as 3+ consecutive days with zero VA overlap and directional POC movement.
  12. Integrate Part 1 concepts with Part 2 concepts: use the day type classifier (from Part 2) with the structural inputs from Part 1 (IB width, range extension, TPO count, tail presence).

- **Medium-term (Month 2-3)**:
  13. Calibrate the 70% VA threshold for A-shares. Test whether 65%, 70%, or 75% produces better predictive power for next-day support/resistance.
  14. Develop a "structural health score" combining IB width, range extension, TPO count, volume profile shape, and POC location. Use this as a feature for intraday models.
  15. Build a "day type probability" model that outputs probabilities for the 7 day types based on Part 1 structural inputs (not just binary classification). Use historical data to train the probability weights.
  16. Implement the TPO count (Concept 12) from the approximate TPO matrix. Compare TPO count imbalance to volume profile imbalance. Determine which is more predictive for next-day direction.
  17. If tick-level data is available, implement true TPO matrix construction and compare to the OHLC approximation. Quantify the approximation error.

- **Long-term (Ongoing)**:
  18. Develop a complete "Market Profile data pipeline" for A-shares: minute-level data → volume profile → TPO approximation → VA/POC/IB/Extension/Tail detection → day type probability → special situation detection (from Part 2). Output a daily "structural report" with all key levels and classifications.
  19. Backtest the structural model on A-share futures (IF, IC) and indices. Report the accuracy of day type classification, open type classification, and special situation detection.
  20. Explore the relationship between Market Profile structure and traditional technical indicators (e.g., does a Trend day with one-timeframe structure correlate with high ADX? Does a Neutral day correlate with low ADX?). Build an ensemble model that combines both frameworks.
  21. Investigate the "local inventory" concept for A-shares using order flow data (if available). Can market maker inventory or broker position data proxy the CBOT local's inventory balance?
  22. Build a multi-timeframe composite profile (weekly, monthly) for A-share indices. Test whether longer-term VA and POC levels provide meaningful support/resistance for daily trading.
