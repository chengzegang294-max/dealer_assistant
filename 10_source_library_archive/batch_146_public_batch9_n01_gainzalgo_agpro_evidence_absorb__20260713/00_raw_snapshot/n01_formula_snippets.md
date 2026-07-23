# N01 Formula Snippets

更新时间：2026-07-14

## 文件类型

- `ARTIFACT`

## 原路径

- `00_raw_snapshot/Volatility_Regimes__GainzAlgo__historical_recovered_excerpt.md`
- `00_raw_snapshot/Volatility_Regimes__GainzAlgo__manual_web_capture__20260713.md`
- `00_raw_snapshot/AG_Pro_ATR_Compression_Map__historical_recovered_excerpt.md`
- `00_raw_snapshot/AG_Pro_ATR_Compression_Map__manual_web_capture__20260713.md`

## 新路径

- `batch_146/00_raw_snapshot/n01_formula_snippets.md`

## 生成入口

- `manual_excerpt_capture`

## 适用对象

- `Batch9 N01 GainzAlgo / AG Pro`

## 当前作用

- 把 `GainzAlgo` 与 `AG Pro` 目前能确认的最小计算口径收成一页结构化摘录。
- 让 `N01` 现阶段至少具备“参数、阈值、状态切换、四因子”可回链的半硬证据页。

## GainzAlgo 最小公式口径

- `tr`
  - `max(high - low, abs(high - prev_close), abs(low - prev_close))`
- `atr`
  - `sma(tr, 14)`
- `baseline_atr`
  - `sma_or_ema(atr, 50)`
- `atr_ratio`
  - `atr / baseline_atr`
- `compression`
  - `atr_ratio < 0.70`
- `expansion`
  - `1.15 <= atr_ratio <= 1.40`
- `high_volatility`
  - `atr_ratio > 1.40`
- `exhaustion`
  - `prior_high_volatility_seen and atr_declining_for_x_bars`

## AG Pro 最小公式口径

- `compression_score`
  - `0..100`
- 当前四个子维度：
  - `atr_contraction`
  - `range_tightness`
  - `noise_level`
  - `containment_quality`
- 当前阶段枚举：
  - `Loose`
  - `Building`
  - `Tight`
  - `Mature`
- 当前二次整理可回链口径：
  - 权重参考：`atr=30 / range=30 / noise=20 / containment=20`
  - 阈值参考：`compressionThreshold = 62`
  - 阈值参考：`matureThreshold = 80`

## 最小伪代码摘录

```text
tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
atr = sma(tr, 14)
baseline_atr = sma_or_ema(atr, 50)
atr_ratio = atr / baseline_atr

if atr_ratio < 0.70:
    regime = COMPRESSION
elif 1.15 <= atr_ratio <= 1.40:
    regime = EXPANSION
elif atr_ratio > 1.40:
    regime = HIGH_VOLATILITY
elif prior_high_ratio_present and atr_declining_for_x_bars:
    regime = EXHAUSTION

compression_score = combine(
    atr_contraction,
    range_tightness,
    noise_level,
    containment_quality
)
compression_state = classify(compression_score)
```

## 当前源码位新增证据

- `GainzAlgo`
  - 已见原作者页源码首屏：
    - `//@version=6`
    - `indicator("Volatility Regimes | GainzAlgo", overlay=true)`
    - `var G5 = "Visual Settings"`
    - 多个 `input.color(..., group=G5)` 行
- `AG Pro`
  - 已见原作者页源码首屏：
    - `//@version=6`
    - `indicator("ATR Compression Map [AGPro Series]", ... )`
    - `shorttitle = "AG Pro ATR"`
    - `max_labels_count / max_lines_count / max_boxes_count`
    - `Inputs / Core Engine / Scoring / Compression Pocket / Visuals / Panel / Alerts`

## 当前能支撑的证据位

- `definition_page`
  - 已能站住 `ATR / baseline / atr_ratio / compression_score / 4阶段`
- `computation_snippet`
  - 已能站住 `GainzAlgo` 的最小公式口径
  - 已能站住 `AG Pro` 的四因子组合框架与阈值参考
- `source_code_snippet`
  - 已能站住两边原作者页都存在可读源码首屏与 input 定义入口
- `regime_interpretation`
  - 已能站住 `COMPRESSION / EXPANSION / HIGH VOLATILITY / EXHAUSTION`
  - 已能站住 `Loose / Building / Tight / Mature`

## 当前不能宣称的内容

- `GainzAlgo` 不再缺原作者源码首屏证据，但仍缺更完整代码段。
- `AG Pro` 不再缺原作者源码首屏证据，但仍缺四因子精确公式与更完整代码段。
- 当前不能写成：
  - `source_code_hard_evidence_ready`
  - `full_input_output_formula_verified`

## 当前结论

- `batch_146` 现在已经不只是：
  - 历史回收摘录
  - 网页正文
- 当前还多了一层：
  - `结构化公式摘录页`
- 但它仍然只到“源码首屏可见 + 半硬证据”，还没有升到完整源码级证据。
