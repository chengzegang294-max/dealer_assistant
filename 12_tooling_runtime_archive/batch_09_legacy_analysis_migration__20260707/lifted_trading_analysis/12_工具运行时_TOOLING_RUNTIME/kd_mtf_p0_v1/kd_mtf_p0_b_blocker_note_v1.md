# KD MTF P0 B 位阻塞说明 v1

## 目的

- 把 `DY-R1 / KD_MTF_P0` 当前为什么长期补不出真实 `b` 样本写成独立阻塞页。
- 避免后续重复在同一批样本上盲扫。
- 为下一次接入新的真实 `M1/M15` 长窗口留一份直接可续跑的说明。

## 当前口径

- 本页记录 `b` 从“长期补不出”到“已补出首条真实 b”的口径演化与证据锚点。
- 当前 `b` 的判定仍是：
  - `day_signal` 有主信号：`golden_cross` 或 `death_cross`
  - `h4_confirm = none`
- 当前 `h4_confirm` 的实现为：
  - `h4_k > h4_d -> confirm_up`
  - `h4_k < h4_d -> confirm_down`
  - `abs(h4_k - h4_d) <= h4_confirm_tie_epsilon -> none`
- 当前冻结参数：
  - `h4_confirm_tie_epsilon = 0.01`

## 当前工程结论

- 旧口径（精确相等）下，`h4_confirm = none` 在真实浮点样本中几乎无自然落点，因此长期出现 `b=0`。
- 将 `none` 从“精确相等”升级为“近似相等（epsilon）”后，`b` 在真实样本中出现可重复落点。
- 首条真实 `b` 已落盘在：
  - `EURUSD H1 2026-03-27T16:00:00Z`

## 已扫样本边界

### 1. 主样本

- `n01_first_real_input_bars_v1.csv`
  - `EURUSD H1`
  - 结果（`h4_confirm_tie_epsilon=0.01`）：`s=368 / a=216 / b=4 / conflict=1452 / unknown=6936`

### 2. n01 横向样本

- 已扫 `H1`：
  - `AAPL.NAS / DE40 / EURUSD / HK50 / JP225 / US500 / USTEC / XAUUSD / XBRUSD`
- 已扫 `M15 -> H1`：
  - `n01_eurusd_m15_bars_v1.csv`
  - `n01_xauusd_m15_bars_v1.csv`
- 结论：
  - 所有样本 `b=0`
  - 所有样本 `h4_confirm = none = 0`

### 3. n02 补充样本

- 已扫：
  - `n02_first_real_input_bars_v1.csv`
- 结论：
  - `a` 可出现
  - `b=0`
  - `h4_confirm = none = 0`

### 4. runtime 原始 bars 样本池

- 当前按列合同统一识别：
  - 表头固定为 `symbol,timeframe,bar_time,open,high,low,close`
  - 基础周期只收 `M1 / M15 / H1`
- 当前识别到 `15` 份 raw bars 文件。
- 其中可上卷成 `>=100` 根 H1 的主样本共 `12` 份。
- 主样本总扫描统计：
  - `s=3587 / a=1856 / b=0 / conflict=8318 / unknown=73438`
- 主样本总结论：
  - `b=0`
  - `h4_confirm = none = 0`

### 5. 短窗口旁证

- 以下窗口被识别到，但上卷后不足 `100` 根 H1，不作为主阻塞证据：
  - `n02_dst_london_spring_20260327_20260331_bars.csv`
  - `n02_dst_newyork_spring_20260306_20260310_bars.csv`
  - `n02_real_input_eurusd_m1_20260610_utc_v1.csv`

## 外扩搜索结果

- 已在 `d:\Stock` 范围按以下模式扩扫：
  - `**/*m1*bars*.csv`
  - `**/*m15*bars*.csv`
  - `**/*bars*.csv`
- 当前没有找到仓库外新增的更长 `M1/M15` 连续窗口。
- 也就是说，当前“继续扩真实来源边界”这条线已经推进到：
  - 仓库内现有样本池已扫尽
  - `d:\Stock` 范围内未发现新的可直接接入长窗口

## 后续接入条件

- 若后续继续补 `b`，优先接入新的真实 `M1/M15` 连续窗口，而不是继续扫短 DST 片段。
- 新样本建议至少满足：
  - 连续时间更长
  - 能稳定上卷成大量 `H1` bars
  - 保留原始浮点精度，不做额外四舍五入
- 新样本到位后，继续沿用当前流程：
  - `raw M1/M15 -> H1 -> 4h/day/week`
  - 固定 `13,3,3 + sma + close_close`
  - 固定 `UTC` 分桶
  - 固定“只取已闭合高周期”

## 当前不做的事

- 不继续扩大 `h4_confirm_tie_epsilon` 的默认值。
- 不把 `confirm_up/down` 改写成别的宽松语义。
- 不因为补不出 `b` 就回头碰策略门控。

## 回滚说明

- 该口径回滚只需要把 `h4_confirm_tie_epsilon` 设回 `0.0` 并重新生成 proof。
