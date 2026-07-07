# CUTPACK — A2 Group — Dalton: Mind Over Markets (2nd Edition)

## BASIC_INFO
- **Full Title**: Mind Over Markets: Power Trading with Market Generated Information (2nd Edition)
- **Author**: James F. Dalton
- **Publisher**: Traders Press (2nd Edition)
- **Pages**: 356
- **Language**: English (Bilingual EN/CN text extracted from PDF)
- **Extraction Source**: `extracted_MindOverMarkets.txt` (356 pages, mixed EN/CN layout, partially corrupted due to PDF extraction artifacts)
- **Cross Check Source**: none (no EPUB available)
- **PDF Role**: `main_text_source`
- **Core Domain**: Market Profile · Day Structure · Timeframe Control · Auction Market Theory
- **Orientation**: Intraday / Day-Timeframe · Longer-Term Bracket/Trend Analysis
- **Difficulty Level**: Intermediate (requires prior Market Profile/TPO basics)
- **Key Chapters for Quants**: Chapter 2 (Day Types), Chapter 3 (TPO Count, Initiative/Responsive), Chapter 4 (Open Types, Special Situations, Range Estimation, Bracket/Trend, LDB)
- **Companion Relationship**: Part 2 of the Chinese "Market Profile Theory" book (市场轮廓理论) covers the same applied concepts (day types, open types, special situations) but with Chinese market terminology.
- **Source Audit Note**: Main text is built from PDF text-layer extraction, not from EPUB/OCR backfill.

## MATERIAL_POSITIONING
- **What this book IS**: A tactical day-trading manual that teaches how to read the "auction process" through Market Profile structure. It provides mechanical rules for identifying high-probability setups (3-1 days, Neutral-Extreme, Value-Area Rule, spikes, balance-area breakouts, gaps) and estimating daily range potential from the opening.
- **What this book IS NOT**: A systematic quantitative strategy book. It contains anecdotal statistics from limited studies (e.g., Treasury bonds 1986-1987) but no rigorous backtesting, no Sharpe ratios, no portfolio construction. The "LDB" (Liquidity Data Bank) concepts are specific to CBOT futures and not directly available for most A-share instruments.
- **How to use it**: Extract the structural classification rules (day types, open types, initiative/responsive) as conditional logic for intraday models. The "Special Situations" provide confluence criteria. The range estimation rules can be used as volatility/expectation inputs. The LDB concepts (volume dispersion, Cti figures) can be proxied with intraday volume profile data.
- **Prerequisites**: Understanding of TPO construction, Value Area (70% of volume), Point of Control (POC), Initial Balance (first hour), range extension, single/double prints, tails. (These are covered in Part 1 of the Chinese book or in Markets in Profile.)

## RETAINED_EXCERPTS

### Excerpt 1 — Day Types and Directional Conviction

> "The result is a gradually ascending line from lowest conviction to highest; from a Nontrend day to a Trend day. Again, the labels we have given the day types are not carved in stone, but are used only for learning purposes. What should become clear is that by monitoring a day's conviction very early in the trading session, traders can quickly begin to understand and visualize how the day will develop."
> — Chapter 2, "Day Type Summary" (Page 43, extracted text around line 2167)

**保留原因**: This establishes the core taxonomy of day types (Nontrend → Normal → Normal Variation → Trend) as a spectrum of directional conviction. The day type is not an arbitrary label but a function of observable structural elements (initial balance width, range extension presence, TPO count, tails). This is the foundational framework for any intraday structural model.

### Excerpt 2 — TPO Count as Imbalance Measurement

> "The TPO count provides a means of measuring the activity of the other timeframe within the body of the day's Profile. Specifically, the TPO count measures the level of imbalance (when such an imbalance exists) between the other timeframe participant and the day timeframe (mostly local) trader."
> — Chapter 3, "TPO Count" (Page 41, extracted text around line 2763)

> "For example, a ratio of 32/24 breaks down to 32 selling TPOs above the point of control, and 24 buying TPOs below. Note that a value area is not specifically calculated. Rather, the methodology of the TPO count, i.e., single-print rejections are not counted, implies value."
> — Chapter 3, "TPO Count" (Page 43, extracted text around line 2877)

**保留原因**: The TPO count is the only "mechanical" quantitative tool in the book that can be computed directly from the Profile. It provides a ratio of buyer/seller dominance within the value area. The instruction to exclude single-print tails from the count is a specific computational rule that must be preserved.

### Excerpt 3 — Initiative vs Responsive Activity

> "Initiative buying is any buying activity occurring within or above the previous day's value area. Conversely, initiative selling is any selling activity that takes place within or below the previous day's value area. Initiative activity indicates strong conviction on the part of the other timeframe."
> — Chapter 3, "Initiative versus Responsive Activity" (Page 46, extracted text around line 3028)

> "Responsive activity is the obverse of initiative activity. Buyers respond to price below value, and sellers respond to price above value."
> — Chapter 3, "Initiative versus Responsive Activity" (Page 46, extracted text around line 3033)

**保留原因**: This is the core behavioral classification used throughout the book. It divides all market activity into four categories based on the relationship to the previous day's value area. This classification is used to interpret tails, range extension, TPO count, and open types. It is the primary "state variable" for any Market Profile-based trading logic.

### Excerpt 4 — Open-Drive (Strongest Open Type)

> "The strongest and most definitive type of open is the Open-Drive. An Open-Drive is generally caused by other timeframe participants who have made their market decisions before the opening bell. The market opens and aggressively auctions in one direction. Fueled by strong other timeframe activity, price never returns to trade back through the opening range."
> — Chapter 4, "Open-Drive" (Page 63, extracted text around line 3863)

> "In the majority of cases, the extreme left behind after an Open-Drive will hold for the entire day."
> — Chapter 4, "Open-Drive" (Page 63, extracted text around line 3874)

> "Open-Drive activity sends clear signals to the trader regarding the type of day to expect—a Trend or Normal Variation day."
> — Chapter 4, "Open-Drive" (Page 65, extracted text around line 3922)

**保留原因**: The Open-Drive is the most reliable open type for predicting day structure. The rule that "the extreme will hold for the entire day" is a high-conviction mechanical statement. If the extreme is violated (price returns through the opening range), it signals a structural change. This provides a clear binary rule for model building.

### Excerpt 5 — Open-Test-Drive (Second Most Reliable)

> "An Open-Test-Drive is similar to an Open-Drive, except that the market lacks the initial confidence necessary to drive immediately after the opening bell. During this type of open, the market generally opens and tests beyond a known reference point (previous day's high or low, bracket top or bottom, etc.) to make sure there is no new business to be done in that direction. The market then reverses and auctions swiftly back through the open."
> — Chapter 4, "Open-Test-Drive" (Page 65, extracted text around line 3935)

> "The strategy for Open-Test-Drive days is similar to that of the Open-Drive, with the understanding that the tested extreme has a slightly lower probability of holding."
> — Chapter 4, "Open-Test-Drive" (Page 67, extracted text around line 4037)

**保留原因**: The Open-Test-Drive provides a mechanical entry rule: wait for the test of a known reference point, then trade in the direction of the reversal. The "tested extreme has a slightly lower probability of holding" is a quantifiable probabilistic distinction from Open-Drive.

### Excerpt 6 — Open-Rejection-Reverse (Lower Conviction)

> "The Open-Rejection-Reverse is characterized by a market that opens, trades in one direction, and then meets opposite activity strong enough to reverse price and return it back through the opening range. An Open-Rejection-Reverse type of open is less convinced of its direction when compared to the Open-Drive and Open-Test-Drive. Because of the lower level of directional conviction, initial extremes generally hold less than half of the time."
> — Chapter 4, "Open-Rejection-Reverse" (Page 68, extracted text around line 4092)

> "The key to trading an Open-Rejection-Reverse type of day is patience."
> — Chapter 4, "Open-Rejection-Reverse" (Page 68, extracted text around line 4119)

**保留原因**: The explicit probability statement "initial extremes generally hold less than half of the time" is a rare quantified claim in the book. This directly implies that the initial extreme is not a reliable reference point, and the day is likely to be two-sided (Normal, Normal Variation, or Neutral).

### Excerpt 7 — Open-Auction (In Range vs Out of Range)

> "An Open-Auction in range generally sets the stage for a Nontrend, Normal, or Neutral type of day. The low market conviction suggests that any extreme established early on has a low probability of holding throughout the day."
> — Chapter 4, "Open-Auction In Range" (Page 70, extracted text around line 4200)

> "However, it is evident in the two examples that an Open-Auction outside of range has the potential to be a big day, while an Open-Auction within value usually lacks conviction. This is evidenced in the fact that March 22 developed into a Selling Trend day, while June 30 resulted in a narrow Normal Variation day."
> — Chapter 4, "Open-Auction Out Of Range" (Page 74, extracted text around line 4311)

**保留原因**: The critical distinction between Open-Auction in range (low conviction, range-bound day) and Open-Auction out of range (potential for big day, Double-Distribution Trend) is a key conditional rule. The opening's relationship to the previous day's range is an early filter for day-type prediction.

### Excerpt 8 — Range Estimation Rules

> "In short, the greatest risk and opportunity arise when a market opens outside of the previous day's range. This indicates that the market is out of balance. When a market opens out of balance, the potential for a dynamic move in either direction is high. Conversely, a market that opens and is accepted (auctions for at least one hour) within the previous day's value area embodies lower risk, but also less opportunity."
> — Chapter 4, "Opening's Relationship to Previous Day" (Page 74, extracted text around line 4341)

> "If you are confident that one of the day's extremes will hold, to estimate the day's range potential you simply superimpose the length of the previous day's range from that extreme."
> — Chapter 4, "Range Estimation" (Page 76, extracted text around line 4476)

> "Allow roughly 10 percent in either direction, recognizing that this is just an estimate, not a prediction."
> — Chapter 4, "Range Estimation" (Page 76, extracted text around line 4494)

**保留原因**: These are the only explicit mechanical rules for estimating daily range potential. They provide a quantitative framework: use previous day's range length as a baseline, adjust for opening location (in value = similar range; out of range = unlimited), and apply a ±10% tolerance. This is directly usable as a volatility expectation model.

### Excerpt 9 — 3-1 Day Statistics (Special Situation)

> "In 94 percent of the days following a 3-1 day, the market traded at prices better than the previous day's value area during the first 90 minutes of trading (higher on 3-1 buying days and lower on 3-1 selling days)."
> — Chapter 4, "3-1 Days" (Page 275, extracted text around line 12488)

> "Some 59 percent of the days following a 3-1 day closed at prices better than the previous day's value area, while only 3 percent closed worse. In all, 97 percent of the days following a 3-1 day closed within or better than the previous day's value area."
> — Chapter 4, "3-1 Days" (Page 275, extracted text around line 12498)

**保留原因**: These are the only rigorously quantified statistics in the book (from a limited Treasury bond study, 1986-1987). The 94% / 97% figures provide a concrete probability base for a 3-1 day follow-through strategy. However, the caveat "derived from one market studied over a limited period of time" must be preserved.

### Excerpt 10 — Neutral-Extreme Day Statistics

> "In 92 percent of the cases studied, the market traded within or above the previous day's value area during the initial 90 minutes of trade. Sixty-four percent of the time this activity occurred above the value area during a Neutral day closing on the highs, or below the value area on a Neutral day closing on the lows."
> — Chapter 4, "Neutral-Extreme Days" (Page 277, extracted text around line 12604)

**保留原因**: The Neutral-Extreme day provides a mechanical rule: if the market closes on the extreme of a Neutral day, the next day is likely to open in the direction of the close. The 92% / 64% figures provide a statistical basis, though from the same limited study.

### Excerpt 11 — Value-Area Rule

> "If the market opens outside the value area on the following day, then the previous day's value area has been rejected by other timeframe participants. Due to the presence of the other timeframe participants who caused the initial rejection, the top of the previous day's value area generally provides support against price probes back down into value, and the bottom of the value area will offer resistance against auction attempts to the upside. However, if price should be accepted (double TPO prints) within the previous day's value area, there is a good possibility that the market will auction completely through that value area."
> — Chapter 4, "Value-Area Rule" (Page 278, extracted text around line 12662)

**保留原因**: The Value-Area Rule provides a mechanical support/resistance rule for the previous day's value area boundaries. The condition "double TPO prints" (acceptance) is the trigger for expecting a full traverse. This is a directly quantifiable rule based on TPO structure.

### Excerpt 12 — Spike Acceptance/Rejection

> "A market that opens within a spike created during the previous day indicates confirmation of that area. The price spike is also accepted if the following day opens beyond the spike—above a buying spike or below a selling spike."
> — Chapter 4, "Spikes" (Page 281, extracted text around line 12815)

> "Conversely, a spike is rejected if the subsequent trading session opens in the opposite direction from the spike."
> — Chapter 4, "Spikes" (Page 281, extracted text around line 12825)

**保留原因**: Spikes provide a clear binary acceptance/rejection framework based on the next day's opening location relative to the spike. This is a directly quantifiable rule for overnight gap analysis.

### Excerpt 13 — Balance-Area Breakout Strategy

> "Balance area break-out strategy is straightforward—go with the break-out. Thus, if price is accepted outside the balance area, place trades in the direction of the new activity."
> — Chapter 4, "Balance-Area Break-outs" (Page 288, extracted text around line 13019)

> "A balance area break-out is a trade you 'almost have to do.' Risk is minimal and profit potential is very high."
> — Chapter 4, "Balance-Area Break-outs" (Page 292, extracted text around line 13102)

**保留原因**: The balance-area breakout is presented as a mechanical "must-do" trade. The rule "go with the breakout" is a simple directional signal. The risk management rule (place stops a few ticks inside the breakout point) is a concrete execution rule.

### Excerpt 14 — Gap Trading Rule

> "The Special Situation rule for trading gaps is to trade with the initiative activity that caused the gap, placing stops at the point where a price rotation would effectively erase the gap by trading completely through it."
> — Chapter 4, "Gaps" (Page 293, extracted text around line 13181)

> "In the day timeframe, if a gap is going to be retraced (filled) by responsive participants, the rejection will usually fill the gap within the first hour. The longer a gap holds, the greater the probability of its continuation."
> — Chapter 4, "Gaps" (Page 293, extracted text around line 13177)

**保留原因**: The gap trading rule provides a mechanical entry (trade with the gap) and stop-loss (gap erasure point). The "first hour" rule for gap filling is a quantifiable time-based condition. This is directly usable for overnight gap strategies.

### Excerpt 15 — Bracketed Market Rules

> "Rule 1: All trades in a bracketed market should be placed responsively."
> — Chapter 4, "Trade Location in a Bracketed Market" (Page 220, extracted text around line 10660)

> "Rule 2: Markets generally test the bracket extreme more than once. Over a large sample size, the market will return to test the bracket extreme on the average of three to five times before moving to new levels with confidence."
> — Chapter 4, "Trade Location in a Bracketed Market" (Page 224, extracted text around line 10757)

> "Rule 3: Markets fluctuate within bracketed regions. A market generally will not auction from one extreme of a bracket to the other in a 'beeline.' Rather, price fluctuates within the balanced area: from top to middle, middle to top, middle to bottom, etc."
> — Chapter 4, "Trade Location in a Bracketed Market" (Page 224, extracted text around line 10765)

> "Rule 4: Monitor activity near the bracket extremes for acceptance/rejection."
> — Chapter 4, "Trade Location in a Bracketed Market" (Page 224, extracted text around line 10771)

**保留原因**: These four rules provide a complete mechanical framework for trading range-bound markets. The "3-5 tests" rule (Rule 2) is a rare quantified claim about bracket behavior. The responsive-only rule (Rule 1) is a clear positional constraint. These rules are directly translatable to mean-reversion models.

### Excerpt 16 — Trend Monitoring via Volume

> "One useful way to monitor a trend for signs of continuation and/or slowing by comparing activity on up days against activity occurring on down days. While in an up trend, for example, determine which way each individual trading session is attempting to go. Then, compare the volume generated on down days versus the up days. If a trend is strong, up days should exhibit greater trade facilitation by generating higher volume than down days. When volume begins to increase on days against the trend, then the trend is aging and may soon begin to balance, or enter a bracket."
> — Chapter 4, "Monitoring Trends for Continuation" (Page 227, extracted text around line 10930)

**保留原因**: This provides a volume-based trend health indicator. The rule "up days should generate higher volume than down days" in an uptrend is a standard quantitative condition. The aging signal (volume increasing on counter-trend days) is a trend exhaustion warning.

### Excerpt 17 — Volume as Trade Facilitation Indicator

> "Volume is the truest and most reliable indicator of the market's ability to facilitate trade. Even in a trending market, if volume is decreasing, then the likelihood that the trend will continue much longer is in question. A market that is not facilitating trade will not survive for long."
> — Chapter 4, "Total Volume" (Page 137, extracted text around line 6996)

> "All markets seek to trade at price levels that maximize volume. If a market is not facilitating trade at a given price level, it will move to a new level that will better facilitate trade."
> — Chapter 4, "Total Volume" (Page 137, extracted text around line 7000)

**保留原因**: This establishes volume as the primary validation metric for all Market Profile structure. The concept that "markets seek to maximize volume" is the foundational axiom of Market Profile theory. Any quantitative implementation must validate structural signals with volume confirmation.

## CORE_CONCEPTS_AND_RULES

### 1. Day Type Classification (Spectrum of Directional Conviction)
- **Source Basis**: Chapter 2, "Day Types" (Pages 20-43)
- **What it is**: Six day types ordered by directional conviction: Nontrend (lowest) → Neutral → Normal → Normal Variation → Double-Distribution Trend → Trend (highest). Each type is determined by observable structural elements: initial balance width, range extension direction, TPO count, tail presence, and whether the market is one-timeframe or two-timeframe.
- **Steps to classify**:
  1. Measure initial balance width (first 1-2 hours / A-B periods). Wide = Normal day potential; Narrow = Trend or Nontrend potential.
  2. Check for range extension. One-sided extension = Trend/Normal Variation; Both-sided = Neutral; None = Nontrend.
  3. Check TPO count direction. Favors one side = directional day; Balanced = Neutral/Nontrend.
  4. Check for tails. Single-print tails at extremes indicate responsive activity (excess).
  5. Check if each subsequent period auctions beyond the previous period's extreme (one-timeframe) or rotates within the range (two-timeframe).
- **Thresholds**:
  - Initial balance > 1.5x average of last 5 days → Normal day potential.
  - Initial balance < 0.5x average of last 5 days → Trend day potential (if range extension occurs) or Nontrend (if no extension).
  - Range extension in first 3 periods → Trend or Normal Variation.
  - Range extension on both sides → Neutral day.
  - No range extension in first 5 periods → Nontrend day.
- **Data Needed**: TPO data (30-min or 1-hour periods), previous day's value area and range.
- **Caveats**: Day types are not mutually exclusive and can evolve. A Nontrend can become a Trend if news arrives. A Normal Variation can become a Neutral if the other timeframe enters on both sides. Classification should be updated period-by-period.
- **Quant Status**: `proxy_quantizable_now` — can be implemented as a multi-factor classification model using intraday OHLC + TPO data.

### 2. TPO Count (Buyer/Seller Imbalance within Value Area)
- **Source Basis**: Chapter 3, "TPO Count" (Pages 41-45)
- **What it is**: A ratio measuring the imbalance between buyers and sellers within the developing value area. Computed by isolating the Point of Control (POC), summing TPOs above it (sellers) and below it (buyers), and comparing.
- **Steps**:
  1. Identify the Point of Control (longest TPO line closest to center of range).
  2. Sum all TPOs above POC (selling TPOs).
  3. Sum all TPOs below POC (buying TPOs).
  4. Exclude single-print tails from the count (they are already accounted for as excess).
  5. Compare the ratio (e.g., 32/24 = 32 selling vs 24 buying).
- **Thresholds**:
  - Ratio > 60/40 → significant imbalance, expect directional follow-through.
  - Ratio > 70/30 → strong imbalance, often provides momentum into the next day.
  - Ratio approaching 50/50 → balance, expect rotational trade.
- **Data Needed**: TPO profile data (30-min periods), real-time updating.
- **Caveats**: The TPO count is only valid for two-timeframe (rotational) markets. In a one-timeframe Trend day, the TPO count is distorted and not useful. The count must be monitored over time (e.g., Profile A → Profile B → Final Profile) to see how the imbalance evolves.
- **Quant Status**: `proxy_quantizable_now` — can be computed directly from TPO data. Requires real-time TPO construction.

### 3. Initiative vs Responsive Activity (Four-Category Classification)
- **Source Basis**: Chapter 3, "Initiative versus Responsive Activity" (Pages 46-49)
- **What it is**: A behavioral classification of all market activity based on the relationship to the previous day's value area. Initiative = activity within/above/below value (strong conviction). Responsive = activity below/above value (opportunistic).
- **The four types**:
  1. **Initiative Buying**: Buying within or above previous day's value area.
  2. **Initiative Selling**: Selling within or below previous day's value area.
  3. **Responsive Buying**: Buying below previous day's value area.
  4. **Responsive Selling**: Selling above previous day's value area.
- **Steps to classify**:
  1. Determine the previous day's value area (high and low boundaries).
  2. For each new price level or range extension, compare to the previous day's value area.
  3. Classify the activity as initiative or responsive based on the location.
  4. Classify the day as a whole: if the value area forms above the previous day's value area → initiative buying; below → initiative selling; overlapping → responsive on both sides.
- **Thresholds**: No numerical thresholds; classification is binary based on location relative to previous day's value area.
- **Data Needed**: Previous day's value area (high/low boundaries), current price action.
- **Caveats**: The distinction between initiative and responsive is not always clean. A responsive buying tail is also initiative selling range extension (the same activity viewed from both sides). The classification depends on which participant is perceived as the aggressor. In the middle of the value area, activity is considered initiative (agreeing with recent value) but with less conviction than initiative outside the value area.
- **Quant Status**: `proxy_quantizable_now` — can be implemented as a binary classification based on previous day's value area boundaries.

### 4. Open Type Classification (Four Types)
- **Source Basis**: Chapter 4, "Opening Types" (Pages 63-74)
- **What it is**: Four types of opening activity that indicate the level of directional conviction and predict the likely day type. The open type is determined by the first 1-3 periods of trading.
- **The four types**:
  1. **Open-Drive**: Market opens and aggressively auctions in one direction without returning to the opening range. Highest conviction. Predicts Trend or Normal Variation day. The initial extreme holds for the entire day in the majority of cases.
  2. **Open-Test-Drive**: Market opens, tests beyond a known reference point, then reverses and auctions swiftly back through the open. Second highest conviction. Predicts Trend or Normal Variation day. The tested extreme has slightly lower probability of holding than Open-Drive.
  3. **Open-Rejection-Reverse**: Market opens, trades in one direction, then meets opposite activity strong enough to reverse price back through the opening range. Lower conviction. Predicts Normal, Normal Variation, or Neutral day. Initial extremes hold less than half the time.
  4. **Open-Auction**: Market opens with no apparent conviction, auctioning above and below the opening range. Lowest conviction. Subdivided into:
     - **Open-Auction In Range**: Opens within previous day's range. Predicts Nontrend, Normal, or Neutral day.
     - **Open-Auction Out of Range**: Opens outside previous day's range. Predicts potential for big day (Double-Distribution Trend).
- **Steps to classify**:
  1. Observe the first 1-2 periods (A-B) after the open.
  2. Check if price returns to the opening range after the initial move.
  3. Check if the market tests a known reference point (previous day's high/low, bracket extreme) before driving.
  4. Check if the market opens within or outside the previous day's range.
  5. Classify based on the observed pattern.
- **Thresholds**: Classification is pattern-based, not numerical. The key binary test is: does price return to the opening range within the first 2 periods? Yes = Open-Rejection-Reverse or Open-Auction; No = Open-Drive or Open-Test-Drive.
- **Data Needed**: Opening price, first 1-2 periods' price action, previous day's range and value area, known bracket extremes.
- **Caveats**: The open type is not always clear in the first 2 periods. Some days start as Open-Auction and evolve into Open-Test-Drive. The classification should be treated as a probability, not a certainty. The textbook examples are rare; most opens are messy.
- **Quant Status**: `proxy_quantizable_now` — can be implemented as a rule-based classifier using the first 1-2 periods' OHLC relative to opening range and previous day's range.

### 5. Opening/Previous Day Relationship & Range Estimation
- **Source Basis**: Chapter 4, "Opening's Relationship to Previous Day" (Pages 74-87)
- **What it is**: A framework for estimating the day's potential range and risk/opportunity based on where the market opens relative to the previous day's value area and range. Three relationships: (1) Open within value, (2) Open outside value but within range, (3) Open outside range.
- **Steps**:
  1. Determine the previous day's value area (high/low) and range (high/low).
  2. Determine the opening price and observe the first 1-2 periods.
  3. Classify the opening into one of three relationships:
     - **Open within value**: If accepted (builds double TPOs within value for at least 1 hour), the market is in balance. Range estimate = previous day's range length, superimposed from the held extreme. Allow ±10%.
     - **Open outside value but within range**: Market is slightly out of balance. Range estimate = similar to previous day but overlapping to one side. Risk slightly higher than open within value.
     - **Open outside range**: Market is out of balance. Range potential is unlimited in the direction of the breakout. If accepted, expect Trend day. If rejected back into range, expect dynamic move in opposite direction.
  4. As the day develops, update the estimate if early extremes are erased or confirmed.
- **Thresholds**:
  - "Auctions for at least one hour" within value = acceptance.
  - "Double TPO prints" within value = acceptance.
  - Price returns to opening range = open type is not Open-Drive.
  - Price breaks beyond previous day's range = breakout, range unlimited.
- **Data Needed**: Previous day's value area and range, opening price, first 1-2 periods' TPO data.
- **Caveats**: The range estimation is a rough guideline, not a prediction. The ±10% tolerance is explicitly stated as approximate. The method works best when the market is in balance (open within value). When out of balance, the range is intentionally unbounded.
- **Quant Status**: `proxy_quantizable_now` — can be implemented as a volatility expectation model. The "previous day's range" is a simple input. The acceptance/rejection condition requires TPO data.

### 6. 3-1 Day (Special Situation)
- **Source Basis**: Chapter 4, "3-1 Days" (Pages 273-277)
- **What it is**: A high-probability day structure where three factors (tail, TPO count, range extension) all point in the same direction. A 3-1 buying day shows initiative buying tail, initiative buying TPOs, and initiative buying range extension. The following day has high probability of continuing in the same direction.
- **Steps to identify**:
  1. Check for initiative tail in the direction of the trend (buying tail for up, selling tail for down).
  2. Check TPO count favors the same direction (e.g., more buying TPOs below POC for a 3-1 buying day).
  3. Check range extension in the same direction.
  4. All three must align. If any one is missing or responsive, it is not a 3-1 day.
- **Thresholds** (from limited Treasury bond study, 1986-1987):
  - 94% of following days traded "better than" previous day's value area in first 90 minutes.
  - 97% of following days closed "within or better than" previous day's value area.
  - 59% of following days closed "better than" previous day's value area.
  - 0% closed "worse" in first 90 minutes; 3% closed "worse" by end of day.
- **Data Needed**: TPO profile, tail identification, TPO count, range extension direction.
- **Caveats**: The statistics are from a single market (Treasury bonds) over a limited period (1986-1987). Other markets behave differently. The 3-1 day is rare. The "2I-1R" day (responsive tail instead of initiative tail) has lower reliability (71% / 82% / 18% worse).
- **Quant Status**: `proxy_quantizable_now` — can be identified from TPO data. The follow-through statistics can be used as priors but must be re-estimated for each market.

### 7. Neutral-Extreme Day (Special Situation)
- **Source Basis**: Chapter 4, "Neutral-Extreme Days" (Pages 277-278)
- **What it is**: A Neutral day (range extension on both sides of initial balance, indicating two-sided activity) that closes on one of the day's extremes. The "victor" (buyer or seller) is identified by the close location, and the following day is likely to open in the direction of the close.
- **Steps to identify**:
  1. Identify a Neutral day: both-sided range extension (buyer and seller both extend the range).
  2. Check the close location: near the middle = Neutral-center (no victor); near the high = buyer has higher conviction; near the low = seller has higher conviction.
  3. If close is on the extreme, classify as Neutral-Extreme.
- **Thresholds** (from limited Treasury bond study, 1986-1987):
  - 92% of following days traded within or above previous day's value area in first 90 minutes.
  - 64% of following days traded "better than" previous day's value area in first 90 minutes (when close was on high).
  - 73% of following days closed "within or better than" previous day's value area.
  - 45% of following days closed "better than" previous day's value area.
  - 27% closed "worse" by end of day.
- **Data Needed**: Daily TPO profile, close location, range extension on both sides.
- **Caveats**: Same limited study as 3-1 days. The Neutral-Extreme is less reliable than the 3-1 day. The statistics are for Treasury bonds only.
- **Quant Status**: `proxy_quantizable_now` — can be identified from daily TPO data. The follow-through statistics can be used as priors but must be re-estimated.

### 8. Value-Area Rule (Special Situation)
- **Source Basis**: Chapter 4, "Value-Area Rule" (Pages 278-279)
- **What it is**: A rule for trading when the market opens outside the previous day's value area and then re-enters it. The previous day's value area boundaries act as support/resistance, but if the market builds double TPOs (acceptance) within the value area, it will likely auction completely through.
- **Steps**:
  1. Market opens outside previous day's value area (rejection of that value area).
  2. Price returns toward the value area.
  3. If price is rejected at the boundary (no double TPOs) → the boundary holds as support/resistance.
  4. If price builds double TPOs within the value area → the market will likely traverse the entire value area.
  5. Monitor the close after traversing: close on the high = strength; close on the low = weakness.
- **Thresholds**: "Double TPO prints" within the value area = acceptance. No specific numerical thresholds for distance from value or value area width, but the book notes that narrower value areas are more easily traversed.
- **Data Needed**: Previous day's value area boundaries, current TPO data for acceptance/rejection detection.
- **Caveats**: The Value-Area Rule does not suggest blindly buying every pierce of the value area. The overall market direction, distance from value, and value area width must be evaluated. The rule is most reliable when the market opens close to the value area (in relative balance) and the value area is narrow.
- **Quant Status**: `proxy_quantizable_now` — can be implemented as a support/resistance breakout model using TPO acceptance data.

### 9. Spike Analysis (Special Situation)
- **Source Basis**: Chapter 4, "Spikes" (Pages 280-288)
- **What it is**: A spike is created when price trends swiftly away from established value in the last few periods of the day, creating a single-print range (low TPO count) at the extreme. The next day's opening location relative to the spike determines acceptance or rejection.
- **Steps to identify**:
  1. Identify a spike: a swift move away from value in the last 1-2 periods, creating a single-print range (no TPO accumulation).
  2. Determine the spike's range (from the top of the breakout period to the day's extreme).
  3. Observe the next day's opening:
     - Open within the spike → acceptance (market balancing within the spike's range). Use spike length for range estimation.
     - Open beyond the spike (above buying spike, below selling spike) → acceptance (continuation).
     - Open in the opposite direction from the spike → rejection.
- **Thresholds**: Spike identification is visual/TPO-based. The key condition is single-print (no TPO accumulation) in the last 1-2 periods. Range estimation uses spike length instead of previous day's full range when the open is within the spike.
- **Data Needed**: TPO profile for spike day, next day's opening price.
- **Caveats**: Spikes are only valid reference points for the first price probe into the spike. If the market returns multiple times in the same period, the spike extreme will likely be auctioned through. The spike's extremes provide support/resistance for alert traders.
- **Quant Status**: `proxy_quantizable_now` — can be identified from TPO data. The acceptance/rejection logic is directly quantifiable.

### 10. Balance-Area Breakout (Special Situation)
- **Source Basis**: Chapter 4, "Balance-Area Break-outs" (Pages 288-292)
- **What it is**: A breakout from a balance area (bracket) where the market has been trading with overlapping value for several days. The breakout is confirmed when price is accepted outside the balance area. The strategy is to trade with the breakout.
- **Steps**:
  1. Identify a balance area: multiple days of overlapping value (number of days depends on timeframe; could be 3 days for swing traders, 8 days for intermediate term, months for long-term).
  2. Identify the balance area boundaries (high and low).
  3. Monitor for a break below the low or above the high.
  4. If price is accepted outside the balance area (no immediate rejection, builds value outside) → trade with the breakout direction.
  5. Place stops a few ticks inside the balance area (a return into the balance area indicates rejection).
- **Thresholds**: "Accepted outside" means price does not return to the balance area within the same day or the next few periods. The exact number of days for "overlapping value" is timeframe-dependent (not fixed).
- **Data Needed**: Multiple days' value areas for overlap detection, current price action for breakout detection.
- **Caveats**: Breakouts can be false (rejected back into the balance area). The market sometimes "rocks" one way and breaks out the opposite direction. The key is to wait for acceptance, not just a price probe. The balance area definition is subjective and timeframe-dependent.
- **Quant Status**: `proxy_quantizable_now` — can be implemented as a breakout model using multi-day value area overlap. Requires defining "overlapping value" as a numerical threshold (e.g., 70% overlap of value areas over N days).

### 11. Gap Analysis (Special Situation)
- **Source Basis**: Chapter 4, "Gaps" (Pages 292-299)
- **What it is**: A gap is an opening outside the previous day's range, indicating a market out of balance. Gaps are classified as break-away (early trend), acceleration (within trend), or exhaustion (end of trend). The gap trading rule is to trade with the gap and place stops at the gap erasure point.
- **Steps**:
  1. Identify a gap: opening price is outside the previous day's range.
  2. Classify the gap type (break-away, acceleration, exhaustion) based on trend context. This is qualitative but can be proxied by trend strength indicators.
  3. Trade with the gap direction (initiative activity).
  4. Place stop at the gap erasure point (where price would trade completely back through the gap).
  5. Monitor the first hour: if the gap is going to be filled by responsive participants, it usually happens within the first hour.
  6. The longer the gap holds, the greater the probability of continuation.
- **Thresholds**: "Filled within the first hour" is a time-based threshold. The gap erasure point is the previous day's extreme (for a gap down, the erasure point is the previous day's low; for a gap up, the previous day's high).
- **Data Needed**: Opening price, previous day's range (high/low), first hour's price action.
- **Caveats**: Not all gaps are ideal. Extreme gaps (far from previous day's range) may invite responsive activity and temporary reversal. The gap type (break-away, acceleration, exhaustion) is subjective and requires trend context. The "first hour" rule is a guideline, not a certainty.
- **Quant Status**: `proxy_quantizable_now` — can be implemented as an overnight gap strategy. The gap type classification requires trend strength indicators (e.g., ADX, moving average slope).

### 12. Bracketed vs Trending Markets (Longer-Term Structure)
- **Source Basis**: Chapter 4, "Brackets" and "Trends" (Pages 220-233)
- **What it is**: Markets spend approximately 70% of the time in brackets (trading ranges) and 30% in trends. The transition from bracket to trend is marked by the initiative participant exerting more control. The transition from trend to bracket is marked by the responsive participant creating excess at the trend extreme.
- **Steps to identify bracket**:
  1. Look for multiple days of overlapping value areas (number of days depends on timeframe).
  2. Define bracket extremes using either value-area tops/bottoms or price extremes (excess).
  3. Trade responsively: buy near the bottom, sell near the top, avoid the middle.
  4. Monitor for 3-5 tests of each extreme before a breakout.
  5. Monitor for acceptance/rejection at extremes.
- **Steps to identify trend**:
  1. Look for consecutive days of non-overlapping value areas in one direction.
  2. Look for initiative activity (gaps, tails, range extension) confirming the direction.
  3. Trade with the trend (initiative). Early entry is difficult but necessary.
  4. Monitor volume: up days should have higher volume than down days in an uptrend.
  5. Look for responsive excess at the trend extreme as a warning of trend end.
- **Thresholds**:
  - 70% of time in brackets / 30% in trends (approximate).
  - 3-5 tests of bracket extreme before breakout.
  - Volume on up days > volume on down days in uptrend (trend strength).
  - Volume increasing on counter-trend days = trend aging.
- **Data Needed**: Multi-day value areas, volume data, gap/tail/range extension data.
- **Caveats**: The bracket/trend definition is timeframe-dependent. A long-term trader may see a 6-month bracket; a swing trader may see a 1-month bracket; a day trader may see a 6-day bracket. There is no universal definition. The 70/30 split is an approximate rule of thumb.
- **Quant Status**: `proxy_quantizable_now` — can be proxied with multi-day value area overlap detection and volume comparison. The timeframe dependency makes it non-universal.

### 13. Liquidity Data Bank (LDB) Volume Dispersion
- **Source Basis**: Chapter 4, "LDB" (Pages 137-140)
- **What it is**: The LDB provides volume-based measures of market activity. Key measures include: total volume (trend health), value area (70% of volume), dispersion of volume (buyer/seller imbalance within value area), Cti figures (participant identification), and high-volume concentrations (support/resistance).
- **Steps for dispersion of volume**:
  1. Find the high-volume price (within the value area).
  2. Sum all volume percentages above the high-volume price.
  3. Sum all volume percentages below the high-volume price.
  4. Divide the high-volume price's percentage by two and add to both sides.
  5. Compare the two sides. Higher volume below = buyer dominance; higher volume above = seller dominance.
- **Thresholds**: No fixed numerical thresholds for imbalance. The book notes that "when one side of the value area contains substantially higher volume, the imbalance usually carries over into the following day."
- **Data Needed**: Intraday volume at each price level (tick-level or price-level volume), value area boundaries.
- **Caveats**: The LDB is specific to CBOT futures and not available for most markets. The concepts can be proxied with intraday volume profile data, but the exact Cti figures (commercial, local, etc.) are not replicable without exchange data. The dispersion analysis is only valid for two-timeframe markets; Trend days distort it.
- **Quant Status**: `needs_extra_data` — requires tick-level volume data and exchange participant classification (not available for most A-share markets). Can be proxied with intraday volume profile but not directly.

### 14. Composite Days (Quick Directional Assessment)
- **Source Basis**: Chapter 4, "Buying/Selling Composite Days" (Page 185)
- **What it is**: A quick method to assess the market's attempted direction by dividing the day's range into four equal parts and checking where the open falls. Open in the bottom quarter = composite buying day; open in the top quarter = composite selling day; open in the middle half = low directional conviction.
- **Steps**:
  1. Divide the day's range (high - low) into four equal parts.
  2. Check the open location relative to the quarters.
  3. Classify: bottom quarter = buying composite; top quarter = selling composite; middle half = low conviction.
- **Thresholds**: The range is divided into four equal parts (25% each). Classification is purely based on open location.
- **Data Needed**: Open price, day's high and low (or estimated range).
- **Caveats**: Composite analysis does not consider "how good a job is it doing in its attempts." A market can gap higher and auction down all day but still develop higher value. Composite analysis must be used with other measures (value area, TPO count, volume).
- **Quant Status**: `proxy_quantizable_now` — can be computed directly from OHLC data. Very simple but limited information content.

## QUANTIZATION_TABLE

| Concept / Rule | What to Quantify | Feasibility | Proxy Approach | quant_status |
|---|---|---|---|---|
| Day Type Classification | Initial balance width, range extension, TPO count, tail presence, one-timeframe vs two-timeframe | High | Use intraday OHLC (30-min or 1-hour) to compute initial balance, range extension, and TPO count. Classify using decision tree or multi-factor model. | `proxy_quantizable_now` |
| TPO Count | Buyer/seller imbalance ratio within value area | High | Compute TPO count from 30-min intraday data. Exclude single-print tails. Use ratio thresholds (60/40, 70/30) as signals. | `proxy_quantizable_now` |
| Initiative vs Responsive | Binary classification of activity relative to previous day's value area | High | Use previous day's value area boundaries as thresholds. Classify each price level and range extension as initiative or responsive. | `proxy_quantizable_now` |
| Open Type Classification | Pattern of first 1-2 periods relative to opening range and previous day's range | High | Use first 30-60 min OHLC to detect Open-Drive (no return to opening range), Open-Test-Drive (test of reference point then reversal), Open-Rejection-Reverse (return through opening range), Open-Auction (oscillation around open). | `proxy_quantizable_now` |
| Range Estimation | Daily range potential based on opening relationship to previous day | High | Use previous day's range as baseline. Adjust for opening location (in value = ±10%; out of range = unlimited). Update as day develops. | `proxy_quantizable_now` |
| 3-1 Day Identification | Alignment of tail, TPO count, and range extension | Medium | Requires TPO data and tail identification. The 3-1 day is rare. Follow-through statistics (94% / 97%) can be used as priors but must be re-estimated per market. | `proxy_quantizable_now` |
| Neutral-Extreme Day Identification | Both-sided range extension + close on extreme | Medium | Detect from daily TPO data. Follow-through statistics (92% / 64%) can be used as priors but must be re-estimated per market. | `proxy_quantizable_now` |
| Value-Area Rule | Support/resistance at previous day's value area boundaries; acceptance vs rejection | High | Use previous day's value area boundaries as support/resistance. "Double TPO prints" as acceptance trigger. | `proxy_quantizable_now` |
| Spike Identification | Single-print range at extreme in last 1-2 periods | Medium | Requires TPO data. Acceptance/rejection based on next day's open location. | `proxy_quantizable_now` |
| Balance-Area Breakout | Multi-day overlapping value area breakout | Medium | Requires multi-day value area data. Define "overlapping value" as threshold (e.g., 70% overlap over N days). Breakout confirmation = acceptance outside. | `proxy_quantizable_now` |
| Gap Analysis | Overnight gap classification and trading | High | Use overnight gap size relative to previous day's range. Trade with gap direction. Stop at gap erasure point. First-hour fill rule. | `proxy_quantizable_now` |
| Bracketed vs Trending Market | Multi-day value area overlap and volume comparison | Medium | Use multi-day value area overlap detection. Volume comparison (up days vs down days) as trend health indicator. | `proxy_quantizable_now` |
| LDB Volume Dispersion | Buyer/seller imbalance within value area using volume | Low | Requires tick-level volume data and price-level volume aggregation. Can be proxied with intraday volume profile but not exact. | `needs_extra_data` |
| Cti Figures (Participant Classification) | Commercial vs local vs public participation | Very Low | Requires exchange-specific data (CBOT LDB). Not available for most markets. | `future_bucket` |
| Composite Day | Open location relative to day's range quarters | High | Simple OHLC computation. Open in bottom 25% = buying composite; top 25% = selling composite; middle 50% = low conviction. | `proxy_quantizable_now` |
| Trend Health (Volume) | Volume on up days vs down days in a trend | High | Compare volume on up days vs down days within a defined trend period. Increasing volume on counter-trend days = aging signal. | `proxy_quantizable_now` |
| Excess Identification (Short-term) | Tails at extremes indicating responsive activity | High | Single-print tails at extremes. Exclude from TPO count. | `proxy_quantizable_now` |
| Excess Identification (Long-term) | Island days, long-term tails, gaps | Medium | Requires daily bar chart analysis. Island day = gap + close on extreme + next day gap opposite. Long-term tail = close on extreme after probe. Gap = overnight rejection. | `proxy_quantizable_now` |
| Trade Location Quality | Risk/reward assessment based on position within bracket/value area | High | Responsive trades near extremes = good location; Initiative trades in middle = poor location. Can be quantified as distance from extreme / distance from middle. | `proxy_quantizable_now` |

## NOT_QUANT_YET

| Item | Why Not Quantifiable | What Would Make It Quantifiable | Priority |
|---|---|---|---|
| Cti Figures (Commercial/Local/Public) | Requires CBOT LDB data with participant classification. Not available for most markets. | Access to exchange-level volume data with participant type breakdown (e.g., CFFEX data for A-shares). | Low |
| Exact LDB Volume Dispersion | Requires tick-level volume at each price with exact aggregation. Most retail data is time-based, not price-based. | Tick-level volume data with price-level aggregation (e.g., volume profile data). | Medium |
| Island Day Classification | Requires visual confirmation of gap + close on extreme + next day gap opposite. The "extreme" definition is subjective. | Automated detection of island days from daily OHLC with gap and close location thresholds. | Medium |
| Gap Type (Break-away/Acceleration/Exhaustion) | Requires trend context and visual assessment. No mechanical rule provided in the book. | Define trend strength thresholds (e.g., ADX > 25, slope of 20-day MA) and gap location within trend to classify. | Medium |
| Bracket Definition (Timeframe-Dependent) | The number of days and the method for defining bracket extremes (value area vs price extremes) is subjective and timeframe-dependent. | Standardize bracket definition: e.g., N days of overlapping value areas with X% overlap, using value area tops/bottoms as extremes. | Medium |
| "Trade Location" (Qualitative Assessment) | The book describes trade location as "good" or "poor" based on visual assessment of the Profile. No numerical metric is provided. | Define trade location score as distance from extreme / distance from middle, normalized by bracket size. | Low |
| Market Sentiment / "Conviction" | Directional conviction is a qualitative concept described through visual Profile features. No single numerical metric captures it. | Create a composite conviction score combining initial balance width, range extension direction, TPO count, volume trend, and open type. | High |
| "Responsive Activity" vs "Initiative Activity" (Nuanced Cases) | The distinction is clear in extreme cases but ambiguous in the middle of the value area. The book notes that activity within the value area is "initiative but with less conviction." | Create a conviction gradient (e.g., distance from previous day's value area boundary) rather than a binary classification. | Medium |
| Transition Detection (Bracket ↔ Trend) | Transition is described as a gradual process with no fixed rules. The book explicitly states there is no "perfect transition rule." | Use a composite model: consecutive days of non-overlapping value + initiative activity + volume increase + gap/tail formation. | High |
| "Trade Facilitation" (Volume as Quality Metric) | The book states volume is the "best indicator of trade facilitation" but does not provide a mechanical formula for "facilitation quality." | Define facilitation index as volume per unit of range, or volume trend relative to price trend. | Medium |
| Open-Type Classification (Messy Opens) | The book states that "two openings will seldom look alike, and textbook examples are rare." The classification is often ambiguous in the first 2 periods. | Use a probabilistic classifier (e.g., random forest) trained on the first 30-60 min of data with features: return to opening range, test of reference point, direction of range extension, opening location relative to previous day's range. | High |

## NEXT_ACTION
- **Immediate (Week 1-2)**:
  1. Implement TPO count calculation from 30-min intraday data. Validate with a sample of A-share futures (e.g., IF, IC) or indices.
  2. Implement day type classification using a decision tree: initial balance width (vs 5-day average), range extension direction, TPO count, tail presence. Output probability distribution over day types.
  3. Implement open type classification using first 30-60 min OHLC: binary features (returned to opening range? tested reference point? opened within previous day's range?).
  4. Implement range estimation model: previous day's range as baseline, adjusted by opening location (in value = ±10%; out of range = unbounded).
  5. Implement initiative/responsive classification: previous day's value area as threshold, classify each price level and each 30-min period's activity.

- **Short-term (Month 1-2)**:
  6. Implement special situations detection: 3-1 day, Neutral-Extreme, Value-Area Rule, spike, balance-area breakout, gap. For each, define the exact TPO/OHLC conditions and test on historical data.
  7. For 3-1 and Neutral-Extreme days, collect statistics on follow-through behavior for the target market (A-share futures or indices). Do not rely on the 1986-1987 Treasury bond figures.
  8. Implement bracketed vs trending detection using multi-day value area overlap (e.g., 5-day rolling window). Test the 70/30 approximation and the 3-5 tests rule.
  9. Implement volume-based trend health indicator: compare volume on up days vs down days within a 10-day trend window.

- **Medium-term (Month 2-3)**:
  10. Develop a composite "directional conviction score" combining multiple structural elements (initial balance, range extension, TPO count, volume, open type). Use this as a feature for intraday models.
  11. Calibrate the range estimation model using historical data. Replace the fixed ±10% with a data-driven tolerance based on market volatility regime.
  12. Integrate with part2 concepts (from the Chinese book) to create a unified day-type + open-type + special-situation signal generator.
  13. If tick-level volume data is available, attempt to proxy the LDB volume dispersion concept using price-level volume aggregation.

- **Long-term (Ongoing)**:
  14. Develop a full intraday structural model that combines all concepts: day type prediction → open type confirmation → special situation detection → range estimation → trade location quality assessment. Output directional bias, expected range, and key support/resistance levels.
  15. Backtest the complete model on A-share futures (IF, IC) or indices. Report hit rates, profit factors, and drawdowns for each special situation and day type.
  16. Consider ensemble methods: combine Market Profile structural signals with traditional technical indicators (moving averages, momentum) to improve robustness.
