# CUTPACK: Forex Price Action Scalping — Bob Volman

## BASIC_INFO

| Attribute | Value |
|-----------|-------|
| **Title** | Forex Price Action Scalping |
| **Author** | Bob Volman |
| **Publisher** | Light Tower Publishing (2011) |
| **Core Domain** | F1 / Forex — Professional Scalping, Price Action, Tick-Chart Microstructure |
| **Primary Instrument** | EUR/USD exclusively |
| **Chart** | 70-tick chart (x-tick) |
| **Only Indicator** | 20-period Exponential Moving Average (20ema) |
| **Target/Stop** | Fixed 10-pip target / 10-pip stop on every trade |
| **Order Type** | Market-order entry; OCO (One-Cancels-the-Other) bracket |
| **retain_mode** | RETAINED_EXCERPTS |
| **current_repo_role** | SECONDARY_STRUCTURED_NOTE |
| **Data Dependency** | 70-tick OHLC, 20ema, spread, execution quality; tick-chart data is non-standard vs. time-based bars |
| **Quant Priority** | Medium-High — all seven setups are rule-based and pattern-defined; but the 70-tick chart and the "Tipping Point" subjective exit are non-trivial to replicate on standard time-based data |

---

## RETAINED_EXCERPTS (Original Text Excerpts)

### 1. Chart and Instrument Selection
> "The contract of focus in all of the coming chapters will be the eur/usd currency pair. To a nimble scalper, this instrument is an absolute delight. It offers highly repetitive intraday characteristics, a low dealing spread and is accessible to even the smallest of traders." (Preface, p. vii)
>
> "The best chart is the 70-tick chart. This is the only chart we will use in all coming chapters. In a general sense, it is not a time frame. This chart prints a new candle after every 70 trades — regardless of the volume involved in these trades." (Chapter 2, p. 7)
>
> "Note: Not all charting packages provide this x-tick setting, so it is recommended to ask before subscribing. The actual trade count also depends on the data feed connected to the chart. Since the forex has no central exchange, a full trade count cannot be achieved, and volume data from different providers may differ." (Chapter 2, p. 7)

### 2. The 20ema and Minimalist Approach
> "Bear in mind that this 20ema should always act as a guide, not a law." (Section 1, p. 13)
>
> "Apart from an exponential moving average, the 20ema, there is nothing on the screen but price." (Chapter 5, p. 27)
>
> "The 20ema is just a tweaked moving average of the last 20 closing prices and does not in any way offer support or resistance to the market on account of its presence. It does point out a dynamic visual level of where prices tend to stall when countering a particular trend." (Chapter 7, p. 43)

### 3. Fixed Target and Stop; OCO Bracket
> "Since we already decided on a 10 pip target and a 10 pip stop, it will be instantly bracketed by a 10 pip stop above the entry price and a 10 pip target below it." (Chapter 7, p. 43)
>
> "The trade setups have stood the test of time and are used without exception in all cases of this scalping method. The profit target of every trade is fixed and set to 10 pips. Likewise, the stop is also set to 10 pips, although this stop can be adjusted in the direction of the target (trailing stop)." (Chapter 4, p. 19)
>
> "When expecting prices to rise and thus taking a long position, the profit order is automatically set 10 pips above the entry price, and the stop order is set 10 pips below it. Conversely, when expecting prices to fall and thus taking a short position, the profit order is automatically set 10 pips below the entry price, and the stop order is set 10 pips above it. If either order is hit, the other is automatically cancelled. This order is also known as a One-Cancels-the-Other (OCO)." (Chapter 4, p. 19)

### 4. The Seven Setups — Overview
> "1. DD. Double Doji Break
> 2. FB. First Break
> 3. SB. Second Break
> 4. BB. Block Break
> 5. RB. Range Break
> 6. IRB. Inside Range Break
> 7. ARB. Advanced Range Break." (Chapter 6, p. 33)
>
> "The DD, the FB and the SB are unmistakably with-trend ventures. The BB is seen in all markets, trending and ranging, topping and bottoming. The RB, IRB and ARB are setups that appear in sideways markets as well as in topping and bottoming ones." (Chapter 6, p. 33)

### 5. Double Doji Break (DD)
> "The Double Doji Break (DD) is the most straightforward setup in the method and is just as easy to identify as it is to trade. A doji is a price bar with more or less the same opening price as closing price. These bars are essentially a sign of market indecision. When the chart prints another doji next to the first, the temporary indecision obviously builds up. In most instances, however, a brief stalling of prices bears little significance; but when two or more dojis appear in what might be the end of a pullback to a nice trend, somewhere in the 20ema zone, a trader better place his finger on the trigger." (Chapter 7, p. 39)
>
> "The dojis in this setup do not have to be dojis in the absolute sense. Small candles, usually no more than 3 pip in length, are best considered to express similar indecision." (Chapter 7, p. 41)
>
> "The most important candle to watch in the DD setup is the one with the highest high — for possible long trades — or the one with the lowest low — for possible shorts. This bar is called the signal bar. The moment its trend-side extreme gets taken out by another bar, we got ourselves a signal to trade. The bar that takes out the high or low of this signal bar is called the entry bar. By definition, the high of any signal bar is taken out when the current price bar goes exactly one pip above it." (Chapter 7, p. 41-42)
>
> "The DD trade should only be taken in the absence of immediate chart resistance, meaning the path to the 10 pip target should not be blocked by visible clustering price action not far to the left of the setup." (Chapter 7, p. 40)

### 6. First Break (FB)
> "The First Break setup (FB) provides an alternative way to pick up the trend at the end of a pullback. Whereas the DD setup requires at least two neighboring bars to identify a possible turning point, the FB setup can be regarded as a powerful signal to trade the break without further confirmation." (Chapter 8, p. 61)
>
> "When choosing to trade the FB setup, we need to see the pullback presented in a mature manner. The best is that the bars in the pullback all close in one direction, and they should certainly not be a feeble attempt." (Chapter 8, p. 61)
>
> "The candle that needs to be broken (the signal bar) should not be longer than 7 pips (7 pips for the candle, 2 pips for the break, 1 pip for the spread)." (Chapter 8, p. 61)
>
> "Should a signal bar be exceptionally tiny, as is sometimes the case in a very fast market, the opening of the entry bar may coincide with the level of the extreme of the signal bar, resulting in a 1 pip gap. A gap is the difference between the close of one bar and the open of the next." (Chapter 8, p. 79)

### 7. Second Break (SB)
> "The Second Break (SB) is one more chart pattern to trade the reversal of a pullback in the 20ema zone. But this time, a little more price action is needed to pinpoint the exact entry. It can be seen as two FB setups appearing in succession." (Chapter 9, p. 79)
>
> "Reliable FB trades are few and far between; it is advised to wait for special circumstances. This can be interpreted to mean that the FB setup is a lesser choice under normal market conditions. If a setup cannot deliver handsome profits over time, the only correct thing to do is to abandon it. The good news is that abandoning the FB does not mean the opportunity to trade in the direction of the trend is fully lost. On the contrary, should the FB fail, it can actually play an important part in a much better setup: the Second Break." (Chapter 9, p. 79)
>
> "If the with-trend traders are strong enough to push prices through the low of the signal bar, the first break is established. As stated before, we would not take action on this first break under normal market conditions. Nevertheless, the market has sent a signal that the countertrend party may be nearing exhaustion. Not all participants will notice this signal. In fact, fresh countertrend traders may see this with-trend push as an opportunity to enter at a better price. Should they do so, prices may be pushed back again to the 20ema zone." (Chapter 9, p. 79)

### 8. Block Break (BB)
> "A most simplistic description would be to characterize the pattern as a cluster of price bars tightly grouped together in a narrow vertical span. Preferably, the barriers of this block of bars are made up of several touches each, meaning that the top and bottom side of the pattern clearly represent resistance and support. On occasion, this group of bars could appear and be broken in a matter of seconds, but the formation itself could best be seen as a miniature trading range." (Chapter 10, p. 109)
>
> "If we were to draw a rectangular box around all the bars that make up this pattern, what should emerge is a distinctive block of price action in which a relatively large amount of contracts changed hands without price being really affected. But the tension within should almost be tangible, like that of a coil being suppressed. If prices eventually break free in the direction of the path of least resistance, we immediately enter the market on a break of the box." (Chapter 10, p. 109)
>
> "There are only three most likely places for this setup to show up. 1: As a block of bars in the end of a pullback. 2: As a horizontal pullback in a strong trend. 3: As a block of bars in a non-trending market." (Chapter 10, p. 110)

### 9. Range Break (RB)
> "For our purposes, a range could be defined as a somewhat extended sideways market phase in which prices seem to be contained between a horizontal top level and a horizontal bottom level. Ideally, these barriers are very straightforward, with at least two equal tops and two equal bottoms touching them. A range by itself should be easy to spot, its main characteristic being a lacking of trend. On a 70-tick chart, range formations usually last anywhere from around 15 minutes to a couple of hours, with the best part of an hour being a very good average." (Chapter 11, p. 137)
>
> "Its most splendid characteristic, and the one a scalper should try to exploit to the fullest, is the simple fact that the range will ultimately crack. The longer it lasts and the more defined the barriers can be drawn, the more players will spot the same break, which will enhance the likelihood of necessary follow-through." (Chapter 11, p. 138)
>
> "We may have to apply similar flexibility when it comes to drawing the smartest barriers. It is not uncommon for the range box to show the majority of equal highs at a level one or two pip below the absolute highs; or show the majority of equal lows at a level one or two pip above the absolute lows." (Chapter 11, p. 138)

### 10. Inside Range Break (IRB)
> "One of the functions of the IRB setup is to capitalize on the tendency of prices to bounce back and forth between the top and bottom barrier of a well-established range. If we were to subtract the average width of a setup from the total span of the range and still have adequate room left for a 10 pip ride, then we are easily talking ranges of close to twenty pip and up." (Chapter 12, p. 175)
>
> "Another way to use the IRB setup is to play the pattern as a regular BB trade and not be too concerned with the barriers on either side. Quite often we can see a familiar cluster of bars take shape somewhere halfway or thereabouts. When this pattern is carefully built up and supported by underlying forces, a scalper could wrap a box around it and trade it just like any other BB setup." (Chapter 12, p. 176)
>
> "A third and much used function of this splendid little setup is to anticipate an actual range barrier break, not from the position of one of the barrier levels, but from somewhere inside the range itself. By definition, this means that prices will have to clear the barrier resistance on their path to the profit target." (Chapter 12, p. 176)

### 11. Advanced Range Break (ARB)
> "The first type of ARB is as a clustering number of bars stagnating around the broken barrier level, but resilient enough to not prove the initial break false. The cluster basically hangs around the barrier, either on top of it (for possible longs) or below it (for possible shorts). Once this cluster of price bars, often resembling a BB setup, eventually sees its signal line broken, a scalper could enter at the market just like he would on any other trade. The main distinction between the RB and this type of ARB is that the signal line of the latter setup is not equal to the barrier; it lies outside of the range." (Chapter 13, p. 209)
>
> "The second type of ARB is more of the pullback variety. Once again we see a range get broken, with the RB not being able to catch the move. Range breakouts can be very powerful, with prices simply shooting out way beyond the barriers. However, this does not have to mean the opportunity for a trade is fully lost. The more the buildup to the break originates from somewhere deep inside the range, the bigger the possibility that prices at some point after the breakout will need to take a breather and thus come to a halt. If they do, and provided they do not fall back all the way into the range, a scalper may have a second shot at entering the market in the direction of the break." (Chapter 13, p. 210)

### 12. Tipping Point Technique (Exit Management)
> "The Tipping Point Technique is an exit technique, not an entry technique. It allows us to time our exit with the same precision as our entry." (Chapter 14, p. 241)
>
> "There is a much better way to manage a trade than to just set a bracket and let the market decide. A better way is to track price action closely from the moment of entry, looking for technical clues on the chart that could negate the validity of the trade." (Chapter 4, p. 19)
>
> "When a trade is no longer valid, it should be exited immediately, even if this means taking a loss smaller than the full 10-pip stop." (Chapter 14, p. 241)

### 13. Probability Principle and Psychology
> "A trader should understand that trading is a probability game, not a win-or-lose game. The goal of trading is not to get a winning trade or to beat another trader. In fact, the outcome of any single trade is irrelevant." (Chapter 5, p. 27)
>
> "The true edge in the market is the trader's ability to recognize and exploit the irrational behavior of others." (Chapter 5, p. 27)
>
> "The smart scalper is more of an observer than a participant. Regardless of market conditions, he will remain neutral and keenly observant, allocating equal attention to the forces in the market pushing in the direction of a potential trade and to the forces pushing in the opposite direction." (Chapter 5, p. 27)

### 14. Unfavorable Conditions
> "The typical pullback is ideally running diagonally against the trend and pretty much one-directional. When it presents itself as a block of clustering and sideways trailing price bars, it could seriously cut short a future advance or decline." (Chapter 7, p. 40)
>
> "Not uncommonly, it is the pullback itself that obstructs the path to target." (Chapter 7, p. 40)
>
> "When the average bar in the trend is small, the DD setup, with similar small bars, will not stand out among the rest. It is not uncommon, in these cases, for the market to show a rather subdued reaction to the break of the DD pattern." (Chapter 7, p. 41)
>
> "When the setup is currently showing two dojis that have their trend-side extremes more than one pip apart, the pattern has to be judged in relation to the trend before it to see if it is still eligible. In case of a rather weak trend, it may be wise to skip the DD trade altogether when the extremes are more than one, but certainly more than two pip apart." (Chapter 7, p. 41)

---

## CORE_CONCEPTS

### 1. Scalping Framework (The "Operating System")

| Component | Specification |
|-------------|---------------|
| **Chart** | 70-tick chart (x-tick) — new candle every 70 trades, not time-based |
| **Instrument** | EUR/USD exclusively (lowest spread, repetitive intraday behavior) |
| **Indicator** | 20-period EMA only (visual guide, not support/resistance) |
| **Entry** | Market order (one-click) |
| **Target** | Fixed 10 pips |
| **Stop** | Fixed 10 pips (can be trailed toward target) |
| **Order Management** | OCO bracket: entry + 10-pip target + 10-pip stop; one cancels the other |
| **Spread Assumption** | 1 pip (spread must be ≤ 1 pip for method to work) |
| **Typical Bar Size** | 2–4 pips in calm markets; trending bars a few pips taller |
| **Session Avoidance** | Very slow markets (Asian session), news events, chaotic conditions |

### 2. Trend Identification (Pre-Trade Context)

A "firm trend" on the 70-tick chart is characterized by:
- Majority of bars closing in the trend direction (white bodies = up, black bodies = down)
- Trending bars, on average, a few pips taller than bars in non-trending phases
- 20ema sloping in trend direction, with most bars traveling on the trend side of it
- Pullbacks are temporary, single-directional, and ideally diagonal (not sideways blocks)

**Note**: The 20ema is a visual aid, not a barrier. Prices often pierce it during pullbacks. The 20ema catches "the bulk of the pullbacks" but may lag in very strong moves.

### 3. Universal Setup Anatomy

Every setup follows the same structural pattern:
- **Signal bar**: The bar whose extreme (high for longs, low for shorts) defines the breakout level
- **Entry bar**: The bar that breaks the signal bar's extreme by exactly 1 pip
- **Entry trigger**: Market order placed the moment the entry bar takes out the signal bar's extreme
- **Risk management**: 10-pip stop and 10-pip target bracketed immediately upon entry

### 4. The Seven Setups — Structural Rules

#### 4.1 Double Doji Break (DD) — With-Trend Pullback
- **Structure premise**: Trend identified; pullback underway; price approaches 20ema zone
- **Trigger**: Two or more adjacent dojis/small candles (≤3 pips) resting in the 20ema zone; signal bar is the one with the highest high (longs) or lowest low (shorts); entry bar breaks that extreme by 1 pip
- **Invalidation / skip**: 
  - Immediate chart resistance within 10-pip path to target (clustering price action to the left)
  - Pullback is a sideways block instead of a clean diagonal pullback
  - Doji extremes are >1–2 pips apart in a weak trend (>2 pips = skip)
  - Dojis are not compressed relative to surrounding trend bars (i.e., they are the longest bars in the area)
- **Risk control**: 10-pip stop; 10-pip target (OCO)
- **Exit**: Fixed OCO, or manual exit via Tipping Point if trade invalidates before stop/target

#### 4.2 First Break (FB) — With-Trend Pullback (Aggressive)
- **Structure premise**: Trend identified; mature pullback to 20ema zone; pullback bars close in one direction (single-directional)
- **Trigger**: First candle in the pullback that is broken in the trend direction = signal bar; entry bar breaks that signal bar by 1 pip
- **Invalidation / skip**:
  - Signal bar >7 pips (cannot fit 10-pip stop + 2-pip break + 1-pip spread)
  - Weak or immature pullback (feeble attempt, hesitant, not single-directional)
  - Fast market causing 3+ pip slippage on entry (poor risk/reward)
- **Risk control**: 10-pip stop; 10-pip target; if slippage is severe, consider skipping or manual Tipping Point exit
- **Exit**: Fixed OCO, or Tipping Point

#### 4.3 Second Break (SB) — With-Trend Pullback (Conservative After Failed FB)
- **Structure premise**: Pullback to 20ema; first break (FB) occurs but fails to sustain; price pulls back again to 20ema zone forming a new signal bar
- **Trigger**: Second break of a new signal bar in the trend direction by 1 pip
- **Invalidation / skip**: 
  - First break failure is so deep that trend structure is broken
  - Second signal bar is excessively long
  - Market conditions have turned non-trending
- **Risk control**: Same 10/10 OCO
- **Exit**: Fixed OCO, or Tipping Point

#### 4.4 Block Break (BB) — Multipurpose (Trend, Range, Top/Bottom)
- **Structure premise**: A cluster of tightly grouped bars in a narrow vertical span, with clear horizontal support/resistance (multiple touches on top and bottom), forming a miniature trading range
- **Three locations**:
  1. End of a pullback (20ema zone) — treated as with-trend continuation
  2. Horizontal pullback in a strong trend — trend pauses sideways, then breaks
  3. Non-trending market — standalone block acting as a range
- **Trigger**: Break of the block's horizontal barrier (signal line) by 1 pip in the direction of the path of least resistance
- **Invalidation / skip**:
  - Block is too wide vertically (not a "narrow span")
  - No clear multiple touches on top/bottom
  - Breaking the less favorable side first (no action; wait for favorable break)
  - No underlying trend direction identified when block is in a trend context
- **Risk control**: 10/10 OCO
- **Exit**: Fixed OCO, or Tipping Point

#### 4.5 Range Break (RB) — Range Continuation/Breakout
- **Structure premise**: Clearly defined horizontal range with at least two equal tops and two equal bottoms; duration typically 15 min – couple of hours on 70-tick chart
- **Trigger**: Break of the horizontal barrier (top or bottom) by 1 pip; prefer breaks with pre-breakout tension (compressed bars near barrier)
- **Barrier drawing flexibility**: 
  - Absolute extremes are first choice
  - If absolute extremes are spiky, use majority line (1–2 pips inside extremes)
  - In slow/compressed ranges, stick to absolute extremes
- **Invalidation / skip**:
  - Range too young or barriers not well-defined
  - Break without pre-breakout tension (low probability)
  - Immediate 1-pip fake-out and reversal (no follow-through)
- **Risk control**: 10/10 OCO
- **Exit**: Fixed OCO, or Tipping Point

#### 4.6 Inside Range Break (IRB) — Range Internal Play
- **Structure premise**: Well-established range with adequate width (≥ ~20 pips total span to allow 10-pip ride after setup width deducted); a miniature block (BB) forms inside the range, near a barrier or mid-range
- **Three functions**:
  1. **Boomerang play**: Block near top barrier → break toward bottom barrier; block near bottom → break toward top. Requires range width ≥ ~20 pips.
  2. **Mid-range BB**: Trade a block inside the range as a regular BB, expecting acceleration toward nearest barrier.
  3. **Anticipate barrier break**: Block inside range breaks in direction of eventual barrier break; target is beyond the barrier, so the barrier must be cleared.
- **Trigger**: Break of the internal block's signal line by 1 pip
- **Invalidation / skip**: Range too narrow; block not well-formed; barrier too strong (clearing it unlikely)
- **Risk control**: 10/10 OCO
- **Exit**: Fixed OCO, or Tipping Point

#### 4.7 Advanced Range Break (ARB) — Post-Breakout Entry
- **Type 1 — Cluster around broken barrier**:
  - Range breaks, but price stalls around the broken barrier (resilient, not falling back into range), forming a cluster (BB-like)
  - Signal line is outside the range (not the barrier itself)
  - Trigger: Break of this new signal line by 1 pip in breakout direction
- **Type 2 — Pullback after powerful breakout**:
  - Range breaks violently, price shoots far beyond barriers, then pulls back to the broken barrier (now support/resistance) or nearby, forming a signal bar
  - Trigger: Break of this pullback signal bar by 1 pip in original breakout direction
- **Invalidation / skip**: Price falls back fully into the range (false breakout); cluster is too loose; pullback is too deep
- **Risk control**: 10/10 OCO
- **Exit**: Fixed OCO, or Tipping Point

---

## QUANTIZATION_TABLE

| Concept | Raw Rule from Text | Observable Proxy | Data Needed | Quant Status | Implementation Hint | Notes |
|---------|-------------------|------------------|-------------|--------------|---------------------|-------|
| 70-tick chart | New candle every 70 trades | None on standard time-based data | Tick/trade count per candle | needs_extra_data | Need tick-data feed or approximate with 15–30 sec bars on EUR/USD | Core chart type; cannot replicate exactly with time-based OHLC |
| 20ema slope | Up = bullish context, down = bearish context | EMA(20) slope sign | 70-tick OHLC | proxy_quantizable_now | Calculate EMA(20) on tick-bar closes | Straightforward on any bar series |
| Trend identification | Majority of bars close in trend direction; bars taller than non-trend | % bars closing bull/bear; average bar height vs baseline | 70-tick OHLC | proxy_quantizable_now | Count body direction; compare ATR-like measure | Approximate on time-based bars |
| DD setup — doji detection | Body ≤ 3 pips; 2+ adjacent; resting in 20ema zone | Body size filter; proximity to EMA(20) | 70-tick OHLC | proxy_quantizable_now | Body = |close-open| ≤ 3 pips; count consecutive; check EMA distance | Simple candle math |
| DD setup — signal bar | Highest high (longs) or lowest low (shorts) of the doji group | Max high / min low in group | 70-tick OHLC | proxy_quantizable_now | Standard min/max on window | Trivial |
| DD setup — entry trigger | Break of signal bar extreme by 1 pip | Price crosses signal bar high + 1 pip | 70-tick OHLC + live price | proxy_quantizable_now | On next bar, check if price ≥ signal_high + 1 pip | Can be implemented as alert/order |
| DD setup — path clearance | No immediate resistance within 10 pips to the left | Scan left 10–20 bars for clustering near target path | 70-tick OHLC | proxy_quantizable_now | Check if price action in [entry, entry+10] is clear | Requires "clustering" definition proxy |
| FB setup — mature pullback | Pullback bars close in one direction; not feeble; reaches 20ema zone | All pullback bars same body direction; pullback length/depth | 70-tick OHLC | proxy_quantizable_now | Count consecutive same-color bars; measure retracement | Approximate |
| FB setup — signal bar length | Signal bar ≤ 7 pips (to fit 10-pip stop + break + spread) | Bar height (high-low) | 70-tick OHLC | proxy_quantizable_now | Filter: (high-low) ≤ 7 pips | Hard threshold |
| SB setup — second break | First break fails; price returns to 20ema; new signal bar broken | Detect first break, then failure, then second signal bar | 70-tick OHLC | proxy_quantizable_now | State machine: trend → pullback → first break → failure → second break | More complex but rule-based |
| BB setup — block detection | Cluster of bars in narrow vertical span; multiple touches on top/bottom | Horizontal box detection; support/resistance touch count | 70-tick OHLC | proxy_quantizable_now | Algorithm: find tight consolidation zones; count touches on boundaries | Requires zone detection algorithm |
| BB setup — path of least resistance | Break in direction of trend (if in trend) or away from last push | Trend direction from EMA; last momentum direction | 70-tick OHLC | proxy_quantizable_now | Use EMA slope + last 3-bar momentum | Context-dependent |
| RB setup — range detection | Extended sideways; horizontal top/bottom; 2+ equal tops/bottoms | Flat EMA; multiple equal highs/lows; bounded price action | 70-tick OHLC | proxy_quantizable_now | Detect equal highs/lows within 1–2 pips; measure duration | Classic range detection |
| RB setup — barrier flexibility | Absolute extremes vs 1–2 pip inside majority line | Mode of highs/lows; outlier detection | 70-tick OHLC | proxy_quantizable_now | Use mode or cluster center instead of strict max/min | Minor optimization |
| RB setup — pre-breakout tension | Compressed bars near barrier before break | ATR contraction near barrier; doji cluster near barrier | 70-tick OHLC | proxy_quantizable_now | ATR(3–5) near barrier < threshold | Tension proxy |
| IRB setup — range width | Total span − setup width ≥ 10 pips | Range height (top-bottom) minus block height | 70-tick OHLC | proxy_quantizable_now | Calculate range and block heights; subtract | Simple arithmetic filter |
| IRB setup — boomerang direction | Block near top → break down; near bottom → break up | Block center position relative to range | 70-tick OHLC | proxy_quantizable_now | If block center in upper/lower third of range, expect opposite break | Spatial logic |
| ARB Type 1 — cluster outside barrier | Price breaks range, stalls near barrier, forms BB-like cluster | Post-breakout consolidation near broken level | 70-tick OHLC | proxy_quantizable_now | Detect consolidation after breakout; signal line outside original range | Event + pattern detection |
| ARB Type 2 — pullback to broken barrier | Violent breakout; pullback to barrier; signal bar forms | Deep breakout; retracement to barrier; new signal | 70-tick OHLC | proxy_quantizable_now | Measure breakout depth; detect pullback to barrier level; signal bar formation | Multi-stage pattern |
| 10-pip fixed target/stop | Every trade: 10-pip target, 10-pip stop | Fixed offset from entry | Entry price | proxy_quantizable_now | Entry ± 0.0010 (for EUR/USD) | Hard rule; trivial |
| OCO bracket | If target hit, stop cancels; if stop hit, target cancels | Order management logic | Broker API | proxy_quantizable_now | Most brokers support OCO natively | Execution layer |
| Spread filter | Trade only if spread ≤ 1 pip (ideally) | Real-time spread | Tick data / broker feed | needs_extra_data | Need bid-ask data; skip if spread > 1 pip | Critical for profitability |
| Slippage filter | Skip if slippage > 2–3 pips on entry | Entry fill vs signal bar extreme | Execution data | needs_extra_data | Need execution reporting; not pre-trade | Execution quality filter |
| Tipping Point exit | Manual exit when trade invalidates before stop/target | Subjective price-action invalidation | 70-tick OHLC + human judgment | shell_only | Cannot be fully automated; requires discretion | Core skill but not quantifiable |
| Unfavorable conditions — slow market | Very low volatility; bars barely moving | ATR extremely low; bar count per minute low | 70-tick OHLC | proxy_quantizable_now | ATR(10) < 2 pips; or bar frequency < threshold | Can be used as session filter |
| Unfavorable conditions — chaotic market | No structure; random price action | Frequent EMA crossings; no directional persistence | 70-tick OHLC | proxy_quantizable_now | Measure directional persistence (consecutive same-body bars) | Context filter |
| Unfavorable conditions — news/event | Major news releases; spread widening | Economic calendar; spread spike | News calendar + tick data | needs_extra_data | Filter by news calendar; skip NFP, FOMC, etc. | External data needed |
| Round-number interference | Prices hesitate at 00 and 50 levels | Price proximity to round numbers | 70-tick OHLC | proxy_quantizable_now | Check if entry or target is within 2–3 pips of round 00/50 | Minor filter |
| Session time — Asian slow | Low activity, fewer bars, less follow-through | Bar count per hour; volume proxy | 70-tick OHLC | proxy_quantizable_now | Bar frequency < threshold during 02:00–10:00 GMT | Session filter |
| Probability principle | Edge is small; play the long game; single trade irrelevant | Win rate over large sample; expectancy | Trade history | proxy_quantizable_now | Track win rate, expectancy, R-multiple distribution | Performance tracking |
| Trend pullback depth | Ideal pullback 40–60% of recent swing | Measure retracement % of last swing | 70-tick OHLC | proxy_quantizable_now | Fibonacci-like retracement on swing high/low | Optional context filter |

---

## FORMULAS_AND_ALGOS (Minimal Proxy Definitions)

> All formulas are approximations for the 70-tick chart on standard time-based bars. The 70-tick chart itself is the core data requirement; these proxies work on 15-sec or 30-sec bars as a fallback.

### F1. Double Doji Break (DD) Detection
Input: 70-tick OHLC series (or proxy 15-sec bars), EMA(20)
1. Identify trend: EMA slope > 0 (uptrend) or < 0 (downtrend)
2. Detect pullback: price crosses from trend side to opposite side of EMA, then returns
3. Scan for 2+ consecutive bars in EMA zone where |body| ≤ 3 pips:
   body_i = |close_i - open_i| ≤ 0.0003 (for EUR/USD)
4. Signal bar (longs): bar with max(high) in the doji group
   Signal bar (shorts): bar with min(low) in the doji group
5. Entry trigger (next bar): price ≥ signal_high + 0.0001 (longs) or price ≤ signal_low - 0.0001 (shorts)
6. Path clearance: in [entry, entry+10pips], no cluster of 3+ bars with overlapping bodies within 5-pip span (left lookback 20 bars)
7. Stop: entry - 0.0010; Target: entry + 0.0010
**Approximation note**: "Resting on 20ema" is approximated as price within 2–3 pips of EMA. "Path clearance" is a heuristic proxy for "no visible clustering resistance."

### F2. First Break (FB) Detection
Input: 70-tick OHLC, EMA(20)
1. Trend identified; pullback underway; pullback reaches EMA zone
2. Maturity filter: last 3+ pullback bars have same body direction (e.g., all bearish in uptrend pullback)
3. Signal bar: first bar in pullback whose high (longs) or low (shorts) is broken by a subsequent bar in trend direction
4. Signal bar size: (high - low) ≤ 0.0007
5. Entry trigger: break of signal bar extreme by 1 pip
6. Stop/Target: entry ± 0.0010
**Approximation note**: "Mature pullback" is proxied by 3+ consecutive same-direction bars. The "first candle broken in trend direction" is event-based.

### F3. Second Break (SB) Detection
Input: 70-tick OHLC, EMA(20)
1. Detect FB event (signal bar broken by 1 pip)
2. Check if price fails to reach target and reverses back into EMA zone within 5–10 bars
3. Detect new signal bar in EMA zone (same criteria as FB)
4. Entry trigger: second break of new signal bar by 1 pip
5. Stop/Target: entry ± 0.0010
**Approximation note**: "Failure" is defined as price not reaching target and reversing past entry. This is a state-machine pattern.

### F4. Block Break (BB) Detection
Input: 70-tick OHLC
1. Detect consolidation zone (block): 
   - Vertical span ≤ 4 pips (high_max - low_min ≤ 0.0004)
   - Duration ≥ 3 bars
   - At least 2 bars touching near the top and 2 bars touching near the bottom (within 1 pip)
2. Determine direction:
   - If block is in pullback of uptrend: long on break of top
   - If block is horizontal pullback in strong trend: long on break of top (uptrend) or bottom (downtrend)
   - If block in non-trending market: break in direction of last momentum push (path of least resistance)
3. Entry trigger: break of block top + 1 pip or block bottom - 1 pip
4. Stop/Target: entry ± 0.0010
**Approximation note**: "Touches" are approximated by highs/lows within 1 pip of a level. "Path of least resistance" in non-trending markets is the weakest heuristic.

### F5. Range Break (RB) Detection
Input: 70-tick OHLC, EMA(20) (flat = ranging)
1. Detect range: 
   - EMA slope near zero (|slope| < threshold) for 10+ bars
   - At least 2 equal highs within 1 pip (top barrier)
   - At least 2 equal lows within 1 pip (bottom barrier)
   - Range height: top - bottom ≥ 6 pips (practical minimum)
2. Pre-breakout tension: ATR(3) near barrier < 1.5 pips (compressed bars)
3. Entry trigger: break of top + 1 pip (long) or bottom - 1 pip (short)
4. Stop/Target: entry ± 0.0010
**Approximation note**: Range detection on 70-tick is more precise than on time bars because ranges compress/expand in tick-space differently.

### F6. Inside Range Break (IRB) Detection
Input: 70-tick OHLC, detected range (from F5)
1. Require range height ≥ 0.0020 (20 pips) for boomerang play
2. Detect internal block (BB criteria) near top third or bottom third of range
3. Boomerang direction: block near top → short break of block bottom; block near bottom → long break of block top
4. Ensure range width - block height ≥ 0.0010 (10 pips room)
5. Entry trigger: break of block signal line by 1 pip
6. Stop/Target: entry ± 0.0010
**Approximation note**: The 20-pip range minimum is a proxy for the book's "close to twenty pip and up" guideline.

### F7. Advanced Range Break (ARB) Detection
Input: 70-tick OHLC, detected range (from F5)
Type 1 (Cluster outside barrier):
1. Detect range breakout (price closes beyond barrier by 2+ pips)
2. Detect post-breakout consolidation (BB-like block) within 3 pips of broken barrier, outside original range
3. Signal line = new top/bottom of consolidation block
4. Entry trigger: break of consolidation signal line by 1 pip in breakout direction

Type 2 (Pullback to barrier):
1. Detect violent breakout (price moves 10+ pips beyond barrier in 3–5 bars)
2. Detect pullback to original barrier level (or within 2 pips)
3. Detect signal bar formation at barrier (FB/DD-like)
4. Entry trigger: break of signal bar by 1 pip in original breakout direction
5. Stop/Target: entry ± 0.0010
**Approximation note**: "Violent breakout" is defined as rapid 10-pip extension; "pullback to barrier" is price returning within 2 pips of original barrier.

---

## NOT_QUANT_YET (Trading Language Assets)

### NQ1. Tipping Point Technique (Discretionary Exit)
- **What it is**: The manual exit technique used when a trade is technically invalidating before the 10-pip stop or 10-pip target is hit. It allows the scalper to exit with a smaller loss (or even a small profit) rather than letting the full stop get hit.
- **Why not quantifiable**: The decision to "tip out" is based on real-time pattern recognition: the shape of the current bar, the speed of the move, the behavior around the 20ema, and the "feel" of the market. The text explicitly states it is an "exit technique" that requires the same "precision as entry" — this is a human skill developed through thousands of hours of screen time.
- **How to preserve**: As a trading language asset, the Tipping Point is the bridge between mechanical rules and discretionary mastery. It teaches that "not all trades that hit the stop were meant to be stopped out." In a quant system, this can be partially proxied by a "time stop" or an "adverse excursion" filter, but the true Tipping Point is a human judgment call.
- **Text reference**: "A better way is to track price action closely from the moment of entry, looking for technical clues on the chart that could negate the validity of the trade. When a trade is no longer valid, it should be exited immediately." (Chapter 4, p. 19; Chapter 14, p. 241)

### NQ2. The "Mature Pullback" Assessment (FB Context)
- **What it is**: The FB setup requires the pullback to be "mature" — not feeble, single-directional, and ideally reaching the 20ema zone. This is a qualitative judgment of pullback quality.
- **Why not quantifiable**: Terms like "mature," "feeble," and "hesitant" are subjective. A "mature pullback" in a fast market looks different from one in a slow market. The 20ema itself is "a guide, not a law," so the pullback may not always reach it. The text warns that a "weak trend" may not produce valid FB setups even if the bars look correct.
- **How to preserve**: As a context filter. A quant system can proxy "mature" by "3+ consecutive same-direction bars" and "reaches within 2 pips of EMA," but the final judgment is human.
- **Text reference**: "When choosing to trade the FB setup, we need to see the pullback presented in a mature manner. The best is that the bars in the pullback all close in one direction, and they should certainly not be a feeble attempt." (Chapter 8, p. 61)

### NQ3. Path Clearance / Chart Resistance (DD Context)
- **What it is**: The DD setup should only be taken if there is no "immediate chart resistance" blocking the 10-pip path to target. This means scanning left on the chart for clustering price action near the target zone.
- **Why not quantifiable**: "Clustering price action" and "visible resistance" are visual-pattern concepts. What counts as "not far to the left" depends on the chart's compression and recent history. A tight cluster 8 pips away might block a target; a loose cluster 5 pips away might not. The text gives no hard distance rule.
- **How to preserve**: As a pre-trade visual checklist. In a quant system, this can be proxied by a " congestion detector" (e.g., high-density price zone within 10 pips of target), but the original concept is a discretionary eyeball check.
- **Text reference**: "The DD trade should only be taken in the absence of immediate chart resistance, meaning the path to the 10 pip target should not be blocked by visible clustering price action not far to the left of the setup." (Chapter 7, p. 40)

### NQ4. Block Break — "Path of Least Resistance" (Non-Trending Context)
- **What it is**: When a BB forms in a non-trending market, the direction of the break is determined by the "path of least resistance." This is a market-reading judgment.
- **Why not quantifiable**: In a non-trending market, there is no EMA slope to guide direction. The text does not provide a mechanical rule for picking the break direction in a flat market; it relies on the scalper's reading of pressure, recent momentum, and barrier strength.
- **How to preserve**: As a discretionary trading skill. In a quant system, one can use a momentum proxy (last 3-bar impulse direction), but this is not the same as the human judgment of "least resistance."
- **Text reference**: "If prices eventually break free in the direction of the path of least resistance, we immediately enter the market on a break of the box." (Chapter 10, p. 109)

### NQ5. Unfavorable Conditions — "Feel" and "Chaos"
- **What it is**: The text identifies many unfavorable conditions: very slow markets, chaotic markets, news events, overextended trends, pullbacks that are 100% retracements, signal bars that are too long, and round-number interference. Many of these are qualitative.
- **Why not quantifiable**: "Chaotic" and "feel" are not algorithmic. A market can look chaotic to a human but have a valid mechanical pattern. The text warns that "no two situations are exactly alike" and that the scalper must develop a "feel" for when to skip.
- **How to preserve**: As a risk-management mindset. The chapter on Unfavorable Conditions (Chapter 15) is a psychological and experiential guide, not a rule set. Some conditions (e.g., spread > 1 pip, news event) can be quantified, but the overall "feel" cannot.
- **Text reference**: "When the average bar in the trend is small, the DD setup, with similar small bars, will not stand out among the rest." (Chapter 7, p. 41) and full Chapter 15.

### NQ6. 70-Tick Chart vs. Time-Based Chart Philosophy
- **What it is**: The entire method is built around the 70-tick chart, which compresses slow periods and expands fast periods. The author argues that this reveals patterns more clearly than time-based charts.
- **Why not quantifiable as a proxy**: While one can approximate 70-tick on 15-sec or 30-sec bars, the text explicitly warns that "not all charting packages provide this x-tick setting" and that "the actual trade count depends on the data feed." The 70-tick chart is not a "setting" that can be perfectly replicated with a time frame; it is a different way of slicing the market. The method's edge may partially come from the tick-chart's unique compression/expansion properties.
- **How to preserve**: As a data-source specification. Any quant system attempting to replicate this must either use tick data or acknowledge that time-based bars are a degraded proxy.
- **Text reference**: "Note: Not all charting packages provide this x-tick setting... Since the forex has no central exchange, a full trade count cannot be achieved, and volume data from different providers may differ." (Chapter 2, p. 7)

### NQ7. The Probability Mindset and Emotional Neutrality
- **What it is**: The book's philosophical core: trading is a probability game, not a win/loss game. The scalper must be an observer, not a participant. He must not try to predict, but to exploit repetition.
- **Why not quantifiable**: This is a psychological and philosophical framework. It cannot be encoded as an algorithm. It is the "operating system" of the trader, not a trading rule.
- **How to preserve**: As a trading language asset that underpins all mechanical rules. It is the reason why the 10-pip fixed target and stop exist: to remove emotion and let probability work over a large sample.
- **Text reference**: "The smart scalper is more of an observer than a participant... The true edge in the market is the trader's ability to recognize and exploit the irrational behavior of others." (Chapter 5, p. 27)

---

## NEXT_ACTION

### 1. Directly Quantizable Fields (proxy_quantizable_now)

These fields can be computed from standard OHLC + EMA and fed into a rule engine:

| Field Name | Type | Description | Setup Link |
|------------|------|-------------|------------|
| `ema20_slope` | float | Slope of EMA(20) | All setups |
| `bar_body` | float | |close - open| | Doji detection, FB maturity |
| `bar_range` | float | high - low | Signal bar size filter |
| `consecutive_bull_bars` | int | Count of bull-body bars | Trend, FB maturity |
| `consecutive_bear_bars` | int | Count of bear-body bars | Trend, FB maturity |
| `doji_count` | int | Consecutive bars with body ≤ 3 pips | DD setup |
| `max_high_window` | float | Max high in N-bar window | DD signal bar |
| `min_low_window` | float | Min low in N-bar window | DD signal bar |
| `signal_bar_break` | bool | Current bar broke signal bar extreme by 1 pip | Universal entry trigger |
| `retracement_pct` | float | Pullback depth vs prior swing | Context filter |
| `range_top` | float | Detected horizontal resistance | RB, IRB, ARB |
| `range_bottom` | float | Detected horizontal support | RB, IRB, ARB |
| `range_height` | float | range_top - range_bottom | IRB width filter |
| `block_span` | float | Vertical span of detected block | BB, IRB |
| `block_touches_top` | int | Count of bars touching block top | BB validity |
| `block_touches_bottom` | int | Count of bars touching block bottom | BB validity |
| `atr_5` | float | 5-bar ATR | Tension, volatility filter |
| `round_00_dist` | float | Distance to nearest .00 | Round-number filter |
| `round_50_dist` | float | Distance to nearest .50 | Round-number filter |
| `time_since_ema_cross` | int | Bars since price crossed EMA | Pullback maturity |
| `session_label` | string | Asian / London / NY / overlap | Session filter |
| `bar_frequency_1h` | int | Number of bars in last hour | Market speed proxy |

### 2. Needs Extra Data

| Need | Source | Purpose |
|------|--------|---------|
| **70-tick OHLC** | Tick-data aggregator or broker API that supports x-tick charts | Core chart type; all patterns are designed for 70-tick |
| **Real-time spread** | Broker API (bid/ask) | Skip if spread > 1 pip; critical for edge |
| **Slippage reporting** | Execution logs | Filter out brokers/platforms with excessive slippage |
| **Economic calendar** | ForexFactory / Investing.com / Bloomberg | Skip trades around major news (NFP, FOMC, ECB) |
| **Tick-level data** | Exchange or ECN feed | Exact 1-pip break detection; gap detection on entry bar open |

### 3. Shell-Only (Trading Language Assets)

| Asset | Role in System |
|-------|----------------|
| Tipping Point Technique | Discretionary override layer; can be approximated by time-stop or adverse-excursion hard-stop, but true Tipping Point is human-only |
| "Mature pullback" feel | Context filter; use proxy rules (3+ same-color bars, EMA reach) but accept human override |
| "Path clearance" eyeball | Pre-trade visual check; congestion detector as proxy |
| "Path of least resistance" in flat market | Directional bias in non-trending BB; use momentum proxy or skip entirely |
| Unfavorable conditions judgment | Market environment filter; quantifiable parts (slow ATR, news, spread) can be automated, but "chaos" and "feel" remain human |
| 70-tick philosophy | Data architecture decision: commit to tick-chart infrastructure or accept time-bar degradation |
| Probability mindset / emotional neutrality | Trader education and discipline; not a system component |

### 4. Implementation Roadmap

**Phase 1 — Time-Bar Proxy (Immediate, using 15-sec or 1-min EUR/USD)**
- Implement EMA(20) slope and trend context
- Implement DD, FB, SB detection on time-based bars with body/range filters
- Implement BB detection via consolidation-zone algorithm
- Implement RB detection via horizontal range algorithm
- Implement IRB and ARB as extensions of BB/RB
- Use fixed 10-pip OCO bracket for all entries
- Apply session filter (skip Asian slow) and ATR filter (skip very low volatility)

**Phase 2 — Tick-Chart Upgrade (Requires data infrastructure)**
- Build or subscribe to 70-tick (or 50–100 tick) OHLC feed for EUR/USD
- Re-calibrate all pattern detection on tick-chart data
- Validate that time-bar proxies from Phase 1 correlate with tick-chart signals
- Integrate real-time spread filter

**Phase 3 — Execution & Monitoring (Requires broker integration)**
- Integrate one-click market-order entry with OCO bracket
- Log slippage and execution quality per setup type
- Build performance dashboard: win rate, expectancy, R-multiple per setup (DD, FB, SB, BB, RB, IRB, ARB)
- Apply economic calendar filter to auto-pause trading

**Phase 4 — Discretionary Overlay (Human-in-the-loop)**
- Build "Tipping Point" alert: when a trade is 3+ pips adverse and showing invalidation patterns, alert trader to consider manual exit
- Build "Unfavorable Conditions" dashboard: ATR, spread, bar frequency, news countdown
- Allow trader to "veto" any automated signal based on qualitative judgment

---

## Version & Status

- **Cutpack Version**: v2
- **Created**: 2024-01-18
- **Source Pages**: 359 (PDF)
- **Extracted Characters**: 702,664
- **Core Chapters**: 6 (Setups Overview), 7 (DD), 8 (FB), 9 (SB), 10 (BB), 11 (RB), 12 (IRB), 13 (ARB), 14 (Tipping Point), 15 (Unfavorable Conditions)
- **Quantization Assessment**: ~70% of rules are directly quantifiable on 70-tick OHLC; ~20% need extra data (tick chart, spread, news); ~10% are shell-only (Tipping Point, subjective context)
- **Retention Status**: All seven setups fully rule-documented; Tipping Point preserved as discretionary asset; 20ema philosophy and probability mindset retained as language assets


