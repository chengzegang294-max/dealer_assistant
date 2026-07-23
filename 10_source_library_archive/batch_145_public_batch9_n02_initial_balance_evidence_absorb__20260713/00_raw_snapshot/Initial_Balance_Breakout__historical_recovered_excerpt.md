# Initial Balance Breakout Historical Recovered Excerpt

更新时间：2026-07-14

- 文件类型：`ARTIFACT`
- 原路径：`10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N02_时段_开盘区间结构/Initial_Balance_Breakout__page_excerpt.md`
- 新路径：`10_source_library_archive/batch_145_public_batch9_n02_initial_balance_evidence_absorb__20260713/00_raw_snapshot/Initial_Balance_Breakout__historical_recovered_excerpt.md`
- 生成入口：`historical_recovered_excerpt`
- 适用对象：`Batch9 N02 Initial Balance`
- 当前作用：定义说明、确认 `ib_high / ib_low / ib_range / ib_accept_2period`
- 证据强度：`historical_recovered`
- 缺口：仍缺源码段与图表示例；当前已确认这是 `2 periods outside IB` 的最强原始 phrasing

## 核心回收摘录

- `The Initial Balance is formed by the first two 30-minute periods (A and B periods) of the trading session`
- `IB High = first hour high; IB Low = first hour low`
- `Price breaks IB boundary AND sustains outside IB for 2+ time periods (1 hour) without returning into the IB`
- `The most reliable IB breakouts sustain for at least two 30-minute periods outside the IB without returning`

## 当前判断

- 这份历史摘录已经足够支撑：
  - `IB` 定义
  - `2 period acceptance` 语义
  - `failed breakout = returns into IB`
- 当前仍只能作为定义层证据，不能当源码级实现证据。
