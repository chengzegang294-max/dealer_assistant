# Volatility Regimes GainzAlgo Historical Recovered Excerpt

更新时间：2026-07-13

- 文件类型：`ARTIFACT`
- 原路径：`10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N01_波动率状态机/Volatility_Regimes__GainzAlgo__page_excerpt.md`
- 新路径：`10_source_library_archive/batch_146_public_batch9_n01_gainzalgo_agpro_evidence_absorb__20260713/00_raw_snapshot/Volatility_Regimes__GainzAlgo__historical_recovered_excerpt.md`
- 生成入口：`historical_recovered_excerpt`
- 适用对象：`Batch9 N01 GainzAlgo`
- 当前作用：定义 `ATR ratio / regime states / breakout threshold`
- 证据强度：`historical_recovered`
- 缺口：仍缺原脚本源码页

## 核心回收摘录

- `ATR = SMA(True Range, default 14)`
- `Baseline ATR = SMA or EMA of ATR over long period (default 50 bars)`
- `ATR Ratio = Current ATR / Baseline ATR`
- 四档 regime：
  - `COMPRESSION: ratio < 0.70`
  - `EXPANSION: ratio between 1.15 and 1.40`
  - `HIGH VOLATILITY: ratio > 1.40`
  - `EXHAUSTION: ATR declines after a prior high-volatility phase`
- `Two-stage signal confirmation`: breakout first, trend confirmation second

## 当前判断

- 这份历史摘录已足够支撑 `vol_regime_code / atr_ratio / baseline_len / breakout_threshold` 的定义层。
- 当前仍不能证明与原始脚本源码完全等价。
