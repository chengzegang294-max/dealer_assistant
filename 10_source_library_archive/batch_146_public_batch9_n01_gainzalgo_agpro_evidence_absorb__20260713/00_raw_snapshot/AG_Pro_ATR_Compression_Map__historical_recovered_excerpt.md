# AG Pro ATR Compression Map Historical Recovered Excerpt

更新时间：2026-07-13

- 文件类型：`ARTIFACT`
- 原路径：`10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N01_波动率状态机/AG_Pro_ATR_Compression_Map__page_excerpt.md`
- 新路径：`10_source_library_archive/batch_146_public_batch9_n01_gainzalgo_agpro_evidence_absorb__20260713/00_raw_snapshot/AG_Pro_ATR_Compression_Map__historical_recovered_excerpt.md`
- 生成入口：`historical_recovered_excerpt`
- 适用对象：`Batch9 N01 AG Pro`
- 当前作用：定义 `compression_quality_score / compression_state / 4项子评分`
- 证据强度：`historical_recovered`
- 缺口：仍缺核心计算段源码

## 核心回收摘录

- `It does not attempt to forecast direction`
- `The script combines four internal components into a unified compression score`
- 四项组成：
  - `ATR contraction`
  - `Range tightness`
  - `Noise evaluation`
  - `Containment structure`
- Kimi 二次整理补充：
  - 状态枚举：`Loose / Building / Tight / Mature`
  - 权重：`atr=30 / range=30 / noise=20 / containment=20`
  - 阈值：`compressionThreshold = 62`、`matureThreshold = 80`

## 当前判断

- 这份历史摘录已足够支撑 `compression_quality_score / compression_state / sub-scores` 的定义层与解释层。
- 当前仍不能证明 `strictMode / releaseUp / releaseDown / nearEdge` 的精确公式。
