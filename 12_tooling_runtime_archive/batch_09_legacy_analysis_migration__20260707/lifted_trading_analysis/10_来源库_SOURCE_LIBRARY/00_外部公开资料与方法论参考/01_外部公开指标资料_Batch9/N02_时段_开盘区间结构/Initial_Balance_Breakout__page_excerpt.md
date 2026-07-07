# Initial Balance Breakout 页面摘录

- source_url: https://marketprofile.info/articles/initial-balance-breakout-strategy
- source_kind: Public article
- capture_method: WebFetch
- capture_date: 2026-06-12

## 关键原文摘录

- `The Initial Balance (IB) ... capitalizes on the principle that when the market breaks decisively above or below the first hour's trading range and sustains that move, it signals directional conviction`
- `The Initial Balance is formed by the first two 30-minute periods (A and B periods) of the trading session`
- `IB High` = first hour high; `IB Low` = first hour low
- 推荐的确认入场：`Price breaks IB boundary AND sustains outside IB for 2+ time periods (1 hour) without returning into the IB`
- `The most reliable IB breakouts sustain for at least two 30-minute periods outside the IB without returning`

## 当前判断

- 这页非常适合做 N02 定义说明，因为它把 `IB 定义`、`acceptance outside range`、`2 period rule` 讲得很清楚。
- 对本仓库最有价值的是：
  - IB high / low / range
  - breakout vs confirmation entry
  - acceptance outside IB
  - narrow IB / wide IB 的上下文解释

## 适合吸收的最小字段

- ib_high
- ib_low
- ib_range
- ib_break_direction
- ib_accept_2period
- ib_regime_narrow_or_wide

## Kimi 二次整理稿补充

- `batch9_sources_kimi` 已补到比当前摘录更完整的文章结构，可补强以下定义层信息：
  - breakout 类型被分成 `Open-Drive / Rotational / Expansion / Gap Reversal`
  - `Open-Drive` 与 `Expansion` 都再次强调：要等 `2+ periods outside IB`
  - `failed breakout = price returns into IB`
  - `narrow IB` 更容易带来后续扩张
- 这对当前 N02 的价值在于：
  - `ib_accept_2period` 不再只是孤立一句规则，而是贯穿多个 breakout 场景的主确认口径
  - `ib_regime_narrow_or_wide` 有了更清楚的上下文解释
  - `failed breakout` 可以先记为后续对象级字段候选
- 还补到一层风险管理语义：
  - 初始止损常放在对侧 IB 边界
  - 目标可按 `1x / 2x / 2-3x IB range` 讨论
  - 这些适合作为解释层，不直接进入当前 P0 字段

## 备注

- 这是定义/交易说明页，不是源码文件。
- 目前这份正文已叠加 Kimi 的较完整二次整理稿，适合做 N02 文义说明与字段草案，但仍不直接当实现证据。
