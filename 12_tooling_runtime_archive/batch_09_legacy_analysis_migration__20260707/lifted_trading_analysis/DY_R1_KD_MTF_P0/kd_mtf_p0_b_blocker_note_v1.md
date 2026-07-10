# KD MTF P0 B 位阻塞说明 v1

## 目的

- 把 `DY-R1 / KD_MTF_P0` 当前为什么长期补不出真实 `b` 样本写成独立阻塞页。
- 避免后续重复在同一批样本上盲扫。
- 为下一次接入新的真实 `M1/M15` 长窗口留一份直接可续跑的说明。

## 当前口径

- 本页只记录现行口径下的阻塞证据，不修改任何逻辑。
- 当前 `b` 的判定仍是：
  - `day_signal` 有主信号：`golden_cross` 或 `death_cross`
  - `h4_confirm = none`
- 当前 `h4_confirm` 的实现仍是：
  - `h4_k > h4_d -> confirm_up`
  - `h4_k < h4_d -> confirm_down`
  - 其余才记为 `none`

## 当前工程结论

- 在现行实现下，`h4_confirm = none` 实际只会落在 `h4_k == h4_d` 的精确相等情形。
- 当前已扫真实浮点样本里，没有自然出现 `h4_k == h4_d`。
- 因此当前 `b = 0` 不是单纯“还没挑到合适 bar_time”，而是现行定义在真实样本里缺自然落点。

## 已扫样本边界

### 1. 主样本

- `n01_first_real_input_bars_v1.csv`
  - `EURUSD H1`
  - 结果：`s=368 / a=216 / b=0 / conflict=792 / unknown=7600`

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

- 不修改 `b` 的定义。
- 不修改 `h4_confirm` 的定义。
- 不把 `confirm_up/down` 改写成别的宽松语义。
- 不因为补不出 `b` 就回头碰策略门控。

## 回滚说明

- 本文件是只读阻塞说明页。
- 若后续拿到新的真实样本并补出第一条真实 `b`，本页应更新为：
  - 保留历史阻塞证据
  - 追加“首次真实 `b` 出现于哪份样本、哪根 `bar_time`”
