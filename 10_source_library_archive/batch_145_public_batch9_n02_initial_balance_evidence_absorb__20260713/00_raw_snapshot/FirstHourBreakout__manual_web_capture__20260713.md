# FirstHourBreakout 手动网页摘录

更新时间：2026-07-14

## 文件类型

- `ARTIFACT`

## 原路径

- `https://toslc.thinkorswim.com/center/reference/Tech-Indicators/strategies/E-K/FirstHourBreakout.html`

## 新路径

- `batch_145/00_raw_snapshot/FirstHourBreakout__manual_web_capture__20260713.md`

## 生成入口

- `manual_webpage_capture`

## 适用对象

- `Batch9 N02 Initial Balance`

## 当前作用

- 作为 `Initial Balance` 相邻平台定义页的网页正文证据。
- 补强“首小时区间如何注册、何时检查突破”的完整上下文。

## 证据强度

- `weak_evidence`

## 状态

- `active`

## 边界说明

- 这不是 `Market Profile / Initial Balance` 原始术语页。
- 它是 `thinkorswim` 的 `FirstHourBreakout` 策略说明页。
- 当前只把它当作：
  - `first hour range` 的平台化定义参考
  - breakout 时间窗与触发逻辑参考
- 当前不把它冒充为：
  - `IB 2 periods outside` 的原始出处
  - `N02` 的最终硬证据

## 网页正文摘录

- 页面说明：
  - `The First-Hour Breakout strategy adds simulated orders based on the price range calculated for the first hour of the regular trading session.`
- 页面算法前置条件：
  - `the strategy compares the total volume traded last night to the average nightly volume over the last five days`
- 时间窗与触发：
  - `At 9:30 am ... compare overnight volume`
- 算法步骤：
  - `At 10:30 am EST, the strategy registers the price range of the first hour of the trading day.`
  - `If the price rises above or falls below this range at any moment from 10:45 am EST to 3:45 pm EST, the strategy will add a simulated order`
  - `All open simulated positions will be closed ... at 4:15 pm EST.`
- 可选过滤：
  - `You can turn off the overnight volume check by setting the use filter parameter to no`

## 当前可确认的最小计算口径

- `first_hour_high`
  - 首小时最高价
- `first_hour_low`
  - 首小时最低价
- `first_hour_range`
  - `first_hour_high - first_hour_low`
- `up_breakout`
  - `price > first_hour_high`
- `down_breakout`
  - `price < first_hour_low`
- `breakout_window`
  - `10:45 EST -> 15:45 EST`
- `close_all_window`
  - `16:15 EST`

## 对 N02 的当前可用价值

- 可补：
  - `definition_page` 的完整网页上下文
  - `usage_note` 的时间窗提示
  - `computation_snippet` 的最小区间注册逻辑和时间窗
- 仍不能补：
  - `IB sustain outside for 2 periods` 的原始出处
  - 更强源码级实现证据

## 缺口

- 仍缺：
  - 更贴近 `Initial Balance / Market Profile` 原始命名的定义页
  - 更强源码段或图例
