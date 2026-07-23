# Initial Balance 手动网页摘录

更新时间：2026-07-14

## 文件类型

- `ARTIFACT`

## 原路径

- `https://futuresindicators.com/learn/initial-balance-basics`
- `https://www.investing.com/analysis/how-to-trade-the-initial-balance-like-a-pro-200678607`

## 新路径

- `batch_145/00_raw_snapshot/Initial_Balance__manual_web_capture__20260714.md`

## 生成入口

- `manual_webpage_capture`

## 适用对象

- `Batch9 N02 Initial Balance`

## 当前作用

- 补入更贴近 `Initial Balance / Market Profile` 原始术语的同主题网页证据。
- 把 `IB` 的定义页、失败突破页和范围扩展页从“相邻平台页”推进到“同主题硬页”。

## 证据强度

- `manual_webpage_capture`

## 状态

- `active`

## 页面定义摘录

- `The Initial Balance (IB) is the highest and lowest prices reached during the first hour of RTH`
- `RTH opens at 9:30 AM ET`
- `RTH's first hour ends at 10:30 AM ET`
- `Whatever high and low price formed between those two times is the Initial Balance`
- `IB High` / `IB Low`
  - `the highest / lowest price reached in the first hour of RTH`

## 同主题使用口径摘录

- `The concept comes from Market Profile methodology and defines the first hour of trading as the market's initial consensus of value`
- `Break above IB high -> bullish bias`
- `Break below IB low -> bearish bias`
- `once price breaks one side of the Initial Balance, it often continues in that direction`

## 范围扩展与失败突破摘录

- `Price breaks out of the IB (Range Extension)`
- `A common target traders watch for after a range extension is the 1x target: add the full IB range to the breakout point`
- `Sometimes price pokes above IB High ... but cannot hold. Within a few minutes it slides back inside the IB. This is a failed breakout`
- `The first retest after a failed breakout is one of the most-watched setups in futures trading`

## 当前可确认的最小计算口径

- `ib_high`
  - `highest price reached during 9:30-10:30 ET`
- `ib_low`
  - `lowest price reached during 9:30-10:30 ET`
- `ib_range`
  - `ib_high - ib_low`
- `range_extension_up_target`
  - `ib_high + ib_range`
- `range_extension_down_target`
  - `ib_low - ib_range`
- `failed_breakout`
  - `price breaks outside IB and then returns inside`
- `first_retest_setup`
  - `after failed breakout, first retest of failed level is the key setup`

## 对 N02 的当前可用价值

- 可补：
  - `definition_page`
  - `usage_note`
  - 一部分 `computation_snippet`
- 相比 `FirstHourBreakout` 的新增价值：
  - 这里直接使用 `Initial Balance / IB High / IB Low / range extension / failed breakout` 术语
  - 更贴近 `Market Profile` 语义
- 当前仍不能补：
  - `2 periods outside IB` 的原始出处
  - 平台源码级实现证据

## 缺口

- 仍缺：
  - 更硬的源码段或图例
  - `2 periods outside IB` 的更原始同名出处
