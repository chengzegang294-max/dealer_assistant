# IB Formula Or Chart Example

更新时间：2026-07-14

## 文件类型

- `ARTIFACT`

## 原路径

- `00_raw_snapshot/Initial_Balance_Breakout__historical_recovered_excerpt.md`
- `00_raw_snapshot/FirstHourBreakout__manual_web_capture__20260713.md`
- `00_raw_snapshot/Initial_Balance__manual_web_capture__20260714.md`

## 新路径

- `batch_145/00_raw_snapshot/ib_formula_or_chart_example.md`

## 生成入口

- `manual_excerpt_capture`

## 适用对象

- `Batch9 N02 Initial Balance`

## 当前作用

- 把现有 `historical_recovered + manual_web_capture` 里的可计算口径收成一页结构化公式摘录。
- 让后续重开线至少有一份“输入/边界/失败模式”可直接引用的整理页。

## 当前可确认的最小公式口径

- `ib_high`
  - `first hour high`
- `ib_low`
  - `first hour low`
- `ib_range`
  - `ib_high - ib_low`
- `up_breakout`
  - `price > ib_high`
- `down_breakout`
  - `price < ib_low`
- `ib_accept_2period`
  - `price breaks IB boundary and sustains outside IB for 2+ time periods (1 hour) without returning into IB`
- `failed_breakout`
  - `returns into IB after breakout`

## 最小伪代码摘录

```text
first_hour_window = session_open -> session_open_plus_60m
ib_high = max(high within first_hour_window)
ib_low = min(low within first_hour_window)
ib_range = ib_high - ib_low

if price > ib_high:
    breakout_side = up
elif price < ib_low:
    breakout_side = down

accept_breakout_only_if:
    price stays outside IB for >= 2 periods

invalidate_if:
    price returns into IB
```

## 当前能支撑的证据位

- `definition_page`
  - 已能站住 `IB first hour range` 与 `2 period acceptance`
- `computation_snippet`
  - 已能站住 `ib_high / ib_low / ib_range / breakout / failed_breakout / 1x range extension`
- `usage_note`
  - 已能站住“不是所有突破都有效，回到 IB 视为失败”的最小失败模式

## 当前不能宣称的内容

- 这不是 `Market Profile / Initial Balance` 原始源码段。
- 这不是原作者图表示例。
- 当前不能写成：
  - `source_code_hard_evidence_ready`

## 当前结论

- `batch_145` 现在已经不是“只有网页正文和零散摘录”。
- 当前至少已有：
  - `定义摘录`
  - `平台化网页正文`
  - `同主题 Initial Balance 定义页`
  - `结构化最小公式页`
- 但更强的原始命名页、源码段或图表示例仍然缺失。
