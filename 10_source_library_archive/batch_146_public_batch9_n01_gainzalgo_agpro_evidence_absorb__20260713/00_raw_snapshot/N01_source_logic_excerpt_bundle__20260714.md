# N01 Source Logic Excerpt Bundle

更新时间：2026-07-14

## 文件类型

- `ARTIFACT`

## 原路径

- `https://www.tradingview.com/script/2z7JVYdK-Volatility-Regimes-GainzAlgo/`
- `https://www.tradingview.com/script/nCbbDHVD-AG-Pro-ATR-Compression-Map-AGPro-Series/`

## 新路径

- `batch_146/00_raw_snapshot/N01_source_logic_excerpt_bundle__20260714.md`

## 生成入口

- `manual_source_capture`

## 适用对象

- `Batch9 N01 GainzAlgo / AG Pro`

## 当前作用

- 把 `N01` 当前最有价值的源码逻辑摘录单独收成一页。
- 与参数字典不同，这页只保留：
  - 阈值
  - 核心状态判断
  - 风控/TP
  - 告警
  - proof
- 本页已在 `fresh session` 中再次复核连续源码窗口，不再只依赖零散参数行。

## GainzAlgo 阈值与 regime 逻辑

```pine
float compressionThresholdInput = input.float(0.70, "Compression Threshold", minval=0.3, maxval=0.9, step=0.05, group=G8, tooltip="ATR ratio below this = COMPRESSION phase. 0.70 = ATR is 30% below baseline (tight consolidation)")
float expansionThresholdInput   = input.float(1.15, "Expansion Threshold", minval=1.0, maxval=1.5, step=0.05, group=G8, tooltip="ATR ratio above this = EXPANSION phase. 1.15 = ATR is 15% above baseline (breakout starting)")
float highVolThresholdInput     = input.float(1.40, "High Volatility Threshold", minval=1.2, maxval=2.0, step=0.05, group=G8, tooltip="ATR ratio above this = HIGH VOLATILITY. 1.40 = ATR is 40% above baseline (strong trend)")
int   exhaustionLookbackInput   = input.int(5, "Exhaustion Lookback", minval=3, maxval=20, group=G8, tooltip="Bars required to confirm declining ATR after high volatility = EXHAUSTION phase")

detectVolatilityRegime(float atrRatio, float atrValue, float compressionThreshold, float expansionThreshold, float highVolThreshold, int exhaustionLookback) =>
    int regime = 0
    bool wasRecentlyHighVol = false
    for i = 1 to 10
        if atrValue[i] / ta.sma(atrValue[i], 50) >= highVolThreshold
            wasRecentlyHighVol := true
            break
    if atrRatio >= highVolThreshold
        regime := 3
    else if atrRatio >= expansionThreshold
        regime := 2
    else if atrRatio < compressionThreshold
        regime := 1
    else if wasRecentlyHighVol and isATRDeclining(atrValue, exhaustionLookback)
        regime := 4
    else
        regime := 2
```

## GainzAlgo 连续源码窗口

```pine
getATRRatio(float atrValue, float atrBaseline) =>
    atrBaseline > 0 ? atrValue / atrBaseline : 1.0

isATRDeclining(float atrValue, int lookback) =>
    declined = true
    for i = 1 to lookback
        if atrValue[i] <= atrValue[i + 1]
            declined := false
            break
    declined

detectVolatilityRegime(float atrRatio, float atrValue, float compressionThreshold, float expansionThreshold, float highVolThreshold, int exhaustionLookback) =>
    int regime = 0
    bool wasRecentlyHighVol = false
    for i = 1 to 10
        if atrValue[i] / ta.sma(atrValue[i], 50) >= highVolThreshold
            wasRecentlyHighVol := true
            break
    if atrRatio >= highVolThreshold
        regime := 3
    else if atrRatio >= expansionThreshold
        regime := 2
    else if atrRatio < compressionThreshold
        regime := 1
    else if wasRecentlyHighVol and isATRDeclining(atrValue, exhaustionLookback)
        regime := 4
    else
        regime := 2
    regime

getRegimeName(int regime) =>
    switch regime
        1 => "COMPRESSION"
        2 => "EXPANSION"
        3 => "HIGH VOLATILITY"
        4 => "EXHAUSTION"
        => "NEUTRAL"
```

## GainzAlgo 更长连续窗口

```pine
getATRBaseline(float atrValue, int length, string baselineType) =>
    baselineType == "EMA" ? ta.ema(atrValue, length) : ta.sma(atrValue, length)

getATRRatio(float atrValue, float atrBaseline) =>
    atrBaseline > 0 ? atrValue / atrBaseline : 1.0

isATRDeclining(float atrValue, int lookback) =>
    declined = true
    for i = 1 to lookback
        if atrValue[i] <= atrValue[i + 1]
            declined := false
            break
    declined

detectVolatilityRegime(float atrRatio, float atrValue, float compressionThreshold, float expansionThreshold, float highVolThreshold, int exhaustionLookback) =>
    int regime = 0
    bool wasRecentlyHighVol = false
    for i = 1 to 10
        if atrValue[i] / ta.sma(atrValue[i], 50) >= highVolThreshold
            wasRecentlyHighVol := true
            break
    if atrRatio >= highVolThreshold
        regime := 3
    else if atrRatio >= expansionThreshold
        regime := 2
    else if atrRatio < compressionThreshold
        regime := 1
    else if wasRecentlyHighVol and isATRDeclining(atrValue, exhaustionLookback)
        regime := 4
    else
        regime := 2
    regime

getRegimeName(int regime) =>
    switch regime
        1 => "COMPRESSION"
        2 => "EXPANSION"
        3 => "HIGH VOLATILITY"
        4 => "EXHAUSTION"
        => "NEUTRAL"

getRegimeColor(int regime) =>
    switch regime
        1 => compressionBgColorInput
        2 => expansionBgColorInput
        3 => highVolBgColorInput
        4 => exhaustionBgColorInput
        => color(na)
```

## GainzAlgo TP 与风险逻辑

```pine
float tp1MultiplierInput   = input.float(1.5, "TP1 Multiplier", minval=0.5, maxval=5.0, step=0.1, group=G11, tooltip="First take profit target. 1.5 = 1.5x ATR from entry. Use for partial profit taking (e.g., 33% position)")
float tp2MultiplierInput   = input.float(2.5, "TP2 Multiplier", minval=1.0, maxval=10.0, step=0.5, group=G11, tooltip="Second take profit target. 2.5 = 2.5x ATR from entry. Use for additional scaling (e.g., another 33%)")
float tp3MultiplierInput   = input.float(4.0, "TP3 Multiplier", minval=2.0, maxval=15.0, step=0.5, group=G11, tooltip="Final take profit target. 4.0 = 4x ATR from entry. Use for remaining position or runners")

getTakeProfitLevels(float entryPrice, float atrValue, bool isBullish) =>
    tp1 = isBullish ? entryPrice + (atrValue * tp1MultiplierInput) : entryPrice - (atrValue * tp1MultiplierInput)
    tp2 = isBullish ? entryPrice + (atrValue * tp2MultiplierInput) : entryPrice - (atrValue * tp2MultiplierInput)
    tp3 = isBullish ? entryPrice + (atrValue * tp3MultiplierInput) : entryPrice - (atrValue * tp3MultiplierInput)

calculatePositionSize(float accountSize, float riskPercent, float entryPrice, float stopLoss) =>
    riskAmount = accountSize * (riskPercent / 100)
    stopDistance = math.abs(entryPrice - stopLoss)
    positionSize = stopDistance > 0 ? riskAmount / stopDistance : 0
```

## GainzAlgo TP / 风险连续窗口

```pine
getDynamicStopLoss(float entryPrice, float atrValue, float multiplier, bool isBullish) =>
    if isBullish
        entryPrice - (atrValue * multiplier)
    else
        entryPrice + (atrValue * multiplier)

getTakeProfitLevels(float entryPrice, float atrValue, bool isBullish) =>
    tp1 = isBullish ? entryPrice + (atrValue * tp1MultiplierInput) : entryPrice - (atrValue * tp1MultiplierInput)
    tp2 = isBullish ? entryPrice + (atrValue * tp2MultiplierInput) : entryPrice - (atrValue * tp2MultiplierInput)
    tp3 = isBullish ? entryPrice + (atrValue * tp3MultiplierInput) : entryPrice - (atrValue * tp3MultiplierInput)
    [tp1, tp2, tp3]

findSupportResistance(float atrValue, float strength, int lookback) =>
    highestHigh = ta.highest(high, lookback)
    lowestLow = ta.lowest(low, lookback)
    resistance = highestHigh
    support = lowestLow
    [support, resistance]

calculatePositionSize(float accountSize, float riskPercent, float entryPrice, float stopLoss) =>
    riskAmount = accountSize * (riskPercent / 100)
    stopDistance = math.abs(entryPrice - stopLoss)
    positionSize = stopDistance > 0 ? riskAmount / stopDistance : 0
    positionSize

float bullStopLoss = enableDynamicSL ? getDynamicStopLoss(close, atrValue, slMultiplierInput, true) : na
float bearStopLoss = enableDynamicSL ? getDynamicStopLoss(close, atrValue, slMultiplierInput, false) : na
float positionSize = enableRiskCalc ? calculatePositionSize(accountSizeInput, riskPercentInput, close, bullStopLoss) : na
```

## GainzAlgo 更长 TP / 风险 / 告警窗口

```pine
getDynamicStopLoss(float entryPrice, float atrValue, float multiplier, bool isBullish) =>
    if isBullish
        entryPrice - (atrValue * multiplier)
    else
        entryPrice + (atrValue * multiplier)

getTakeProfitLevels(float entryPrice, float atrValue, bool isBullish) =>
    tp1 = isBullish ? entryPrice + (atrValue * tp1MultiplierInput) : entryPrice - (atrValue * tp1MultiplierInput)
    tp2 = isBullish ? entryPrice + (atrValue * tp2MultiplierInput) : entryPrice - (atrValue * tp2MultiplierInput)
    tp3 = isBullish ? entryPrice + (atrValue * tp3MultiplierInput) : entryPrice - (atrValue * tp3MultiplierInput)
    [tp1, tp2, tp3]

findSupportResistance(float atrValue, float strength, int lookback) =>
    highestHigh = ta.highest(high, lookback)
    lowestLow = ta.lowest(low, lookback)
    resistance = highestHigh
    support = lowestLow
    [support, resistance]

calculatePositionSize(float accountSize, float riskPercent, float entryPrice, float stopLoss) =>
    riskAmount = accountSize * (riskPercent / 100)
    stopDistance = math.abs(entryPrice - stopLoss)
    positionSize = stopDistance > 0 ? riskAmount / stopDistance : 0
    positionSize

getATRPercentile(float currentATR, int lookback) =>
    float sum = 0
    int count = 0
    for i = 0 to lookback - 1
        if not na(ta.atr(atrLengthInput)[i])
            if ta.atr(atrLengthInput)[i] < currentATR
                count := count + 1
            sum := sum + 1
    percentile = sum > 0 ? (count / sum) * 100 : 50
    percentile

isVolatilityContraction(float atrValue, int bars, float threshold) =>
    contracted = true
    avgATR = ta.sma(atrValue, bars * 2)
    for i = 0 to bars - 1
        if atrValue[i] > avgATR * threshold
            contracted := false
            break
    contracted

float atrValue = ta.atr(atrLengthInput)
float atrSma = ta.sma(atrValue, atrLengthInput)
bool volBreakout = isVolatilityBreakout(atrValue, atrSma, volThresholdInput)
bool volSignal = volBreakout and not volBreakout[1]
float atrBaseline = getATRBaseline(atrValue, regimeBaselineLengthInput, regimeBaselineTypeInput)
float atrRatio = getATRRatio(atrValue, atrBaseline)
int currentRegime = enableRegimeDetection ? detectVolatilityRegime(atrRatio, atrValue, compressionThresholdInput, expansionThresholdInput, highVolThresholdInput, exhaustionLookbackInput) : 0
float bullStopLoss = enableDynamicSL ? getDynamicStopLoss(close, atrValue, slMultiplierInput, true) : na
float bearStopLoss = enableDynamicSL ? getDynamicStopLoss(close, atrValue, slMultiplierInput, false) : na
[bullTP1_calc, bullTP2_calc, bullTP3_calc] = getTakeProfitLevels(close, atrValue, true)
[bearTP1_calc, bearTP2_calc, bearTP3_calc] = getTakeProfitLevels(close, atrValue, false)
float positionSize = enableRiskCalc ? calculatePositionSize(accountSizeInput, riskPercentInput, close, bullStopLoss) : na
float atrPercentile = enableATRPercentile ? getATRPercentile(atrValue, percentileLookback) : na
bool contractionPattern = enableVolContraction ? isVolatilityContraction(atrValue, contractionBars, contractionThreshold) : false
bool contractionSignal = contractionPattern and not contractionPattern[1]

if volSignal
    alert("ATR Volatility Breakout", alert.freq_once_per_bar_close)
if bullishTrend
    alert("ATR Bullish Trend Signal", alert.freq_once_per_bar_close)
if bearishTrend
    alert("ATR Bearish Trend Signal", alert.freq_once_per_bar_close)
if atrCrossover
    alert("Price Above ATR Band 1", alert.freq_once_per_bar_close)
if atrCrossunder
    alert("Price Below ATR Band 1", alert.freq_once_per_bar_close)
if enableRegimeDetection and currentRegime == 1 and currentRegime[1] != 1
    alert("Volatility Regime: COMPRESSION", alert.freq_once_per_bar_close)
if enableRegimeDetection and currentRegime == 2 and currentRegime[1] != 2
    alert("Volatility Regime: EXPANSION", alert.freq_once_per_bar_close)
if enableRegimeDetection and currentRegime == 3 and currentRegime[1] != 3
    alert("Volatility Regime: HIGH VOLATILITY", alert.freq_once_per_bar_close)
if enableRegimeDetection and currentRegime == 4 and currentRegime[1] != 4
    alert("Volatility Regime: EXHAUSTION", alert.freq_once_per_bar_close)
if enableVolContraction and contractionSignal
    alert("Volatility Contraction Pattern Detected - Breakout Imminent", alert.freq_once_per_bar_close)
```

## GainzAlgo 告警逻辑

```pine
if volSignal
    alert("ATR Volatility Breakout", alert.freq_once_per_bar_close)
if bullishTrend
    alert("ATR Bullish Trend Signal", alert.freq_once_per_bar_close)
if bearishTrend
    alert("ATR Bearish Trend Signal", alert.freq_once_per_bar_close)
if atrCrossover
    alert("Price Above ATR Band 1", alert.freq_once_per_bar_close)
if atrCrossunder
    alert("Price Below ATR Band 1", alert.freq_once_per_bar_close)
if enableRegimeDetection and currentRegime == 1 and currentRegime[1] != 1
    alert("Volatility Regime: COMPRESSION", alert.freq_once_per_bar_close)
if enableRegimeDetection and currentRegime == 2 and currentRegime[1] != 2
    alert("Volatility Regime: EXPANSION", alert.freq_once_per_bar_close)
if enableRegimeDetection and currentRegime == 3 and currentRegime[1] != 3
    alert("Volatility Regime: HIGH VOLATILITY", alert.freq_once_per_bar_close)
if enableRegimeDetection and currentRegime == 4 and currentRegime[1] != 4
    alert("Volatility Regime: EXHAUSTION", alert.freq_once_per_bar_close)
if enableVolContraction and contractionSignal
    alert("Volatility Contraction Pattern Detected - Breakout Imminent", alert.freq_once_per_bar_close)
```

## AG Pro 阈值与评分逻辑

```pine
compressionThreshold = input.float(62.0, "Compression Threshold", minval = 1.0, maxval = 100.0, step = 1.0, group = G_CORE,
     tooltip = "Minimum score required for a qualified compression state.")
matureThreshold = input.float(80.0, "Mature Threshold", minval = 1.0, maxval = 100.0, step = 1.0, group = G_CORE,
     tooltip = "Higher score level required for mature compression when noise and containment also confirm.")
strictMode = input.bool(false, "Strict Mode", group = G_CORE,
     tooltip = "Applies tighter score gates for more selective compression pockets.")

atrWeight = input.float(30.0, "ATR Weight", minval = 0.0, maxval = 100.0, step = 1.0, group = G_SCORE,
     tooltip = "Weight assigned to ATR contraction in the final compression score.")
rangeWeight = input.float(30.0, "Range Weight", minval = 0.0, maxval = 100.0, step = 1.0, group = G_SCORE,
     tooltip = "Weight assigned to recent range contraction in the final compression score.")
noiseWeight = input.float(20.0, "Noise Weight", minval = 0.0, maxval = 100.0, step = 1.0, group = G_SCORE,
     tooltip = "Weight assigned to low-noise behavior, including wick, flip, and close-drift quality.")
containmentWeight = input.float(20.0, "Containment Weight", minval = 0.0, maxval = 100.0, step = 1.0, group = G_SCORE,
     tooltip = "Weight assigned to price clustering and containment quality.")

buildingThreshold = math.max(34.0, compressionThreshold * 0.72)
matureNoiseGate = strictMode ? 62.0 : 52.0
matureContainmentGate = strictMode ? 66.0 : 55.0

isBuilding = compressionScore >= buildingThreshold and atrScore >= 40.0 and rangeScore >= 40.0
isTight = compressionScore >= compressionThreshold and atrScore >= 50.0 and rangeScore >= 50.0
isMature = compressionScore >= matureThreshold and atrScore >= 58.0 and rangeScore >= 58.0 and noiseScore >= matureNoiseGate and containmentScore >= matureContainmentGate
```

## AG Pro Proof 与告警逻辑

```pine
showProof = input.bool(true, "Show Proof Layer", group = G_PROOF,
     tooltip = "Shows the confirmation-anchored proof layer in the panel: Follow, Hold, React, and Flip rates measured across pocket releases on the current symbol and timeframe. Follow means price expanded one risk unit in the release direction before giving back the same distance against it. These are historical outcome rates, not predictions.")
proofStopAtr = input.float(1.20, "Proof Risk Unit (ATR)", minval = 0.30, maxval = 5.00, step = 0.10, group = G_PROOF,
     tooltip = "ATR distance used as one risk unit for the proof measurement. The favorable expansion target and the adverse reference are both placed this far from the release close.")
proofHorizonBars = input.int(30, "Proof Horizon Bars", minval = 4, maxval = 300, group = G_PROOF,
     tooltip = "Maximum number of bars each release is tracked for the proof measurement before it resolves at its current outcome.")
reactBars = input.int(3, "Reaction Window Bars", minval = 1, maxval = 40, group = G_PROOF,
     tooltip = "Number of bars after a release used to detect an immediate favorable expansion reaction.")
reactProgressPct = input.float(40.0, "Reaction Progress %", minval = 5.0, maxval = 90.0, step = 1.0, group = G_PROOF,
     tooltip = "Minimum favorable progress toward the risk-unit target, within the reaction window, required to count as an early React.")

alertcondition(alertCompressionReady and enteredCompression, "AG Pro ATR | Compression Ready", "AG Pro ATR Compression Map: compression has reached the ready threshold.")
alertcondition(alertMature and reachedMature, "AG Pro ATR | Mature Compression", "AG Pro ATR Compression Map: compression has reached the mature state.")
alertcondition(alertRelease and releaseUp, "AG Pro ATR | Upside Release", "AG Pro ATR Compression Map: price closed above the active compression pocket.")
alertcondition(alertRelease and releaseDown, "AG Pro ATR | Downside Release", "AG Pro ATR Compression Map: price closed below the active compression pocket.")
```

## AG Pro Proof 面板统计逻辑

```pine
var int proofTotal = 0
var int proofFollow = 0
var int proofHold = 0
var int proofReact = 0
var int proofFlip = 0

bool followNow = hitTarget and not pFlipped
if followNow
    pFollowed := true
bool naturalResolve = pFlipped or followNow or heldBars >= proofHorizonBars
if naturalResolve or releaseAnchor
    proofTotal := proofTotal + 1
    if pFollowed
        proofFollow := proofFollow + 1
    if not pFlipped
        proofHold := proofHold + 1
    if pReacted
        proofReact := proofReact + 1
    if pFlipped
        proofFlip := proofFlip + 1

float followRate = proofTotal > 0 ? proofFollow * 100.0 / proofTotal : 0.0
float holdRate = proofTotal > 0 ? proofHold * 100.0 / proofTotal : 0.0
float reactRate = proofTotal > 0 ? proofReact * 100.0 / proofTotal : 0.0
float proofFlipRate = proofTotal > 0 ? proofFlip * 100.0 / proofTotal : 0.0
```

## 当前结论

- `N01` 现在已经不只是“参数和默认值被看见”。
- 当前还多了：
  - `源码逻辑段`
  - `阈值与状态判断`
  - `风险与 TP 公式`
  - `告警触发文本`
  - `proof 统计逻辑`
- 当前剩余缺口进一步收缩为：
  - 更完整连续 Pine 代码段
  - 参数截图级证据
  - 关键公式上下游联动的更长源码窗口
- 当前状态已可描述为：
  - `源码逻辑层近硬证据`
