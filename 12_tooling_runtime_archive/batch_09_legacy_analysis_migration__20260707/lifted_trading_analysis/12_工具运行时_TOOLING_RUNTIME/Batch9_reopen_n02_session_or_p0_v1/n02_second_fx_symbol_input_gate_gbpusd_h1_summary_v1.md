# N02 GBPUSD H1 第二 FX 品种输入闸口总览 v1

## 作用

- 对 `GBPUSD/H1` 做 `second fx symbol input gate` 级验证。
- 当前只确认第二个 FX 原始输入是否存在、是否能 ingest、以及是否满足当前 `30m OR` 粒度要求。

## 2026-07-05 fresh-run

- 发现的 `FX H1` 原始样本：`["AUDJPY", "AUDNZD", "AUDUSD", "CADJPY", "CHFJPY", "EURAUD", "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURUSD", "GBPCHF", "GBPJPY", "GBPUSD", "NZDJPY", "NZDUSD", "USDCAD", "USDCHF", "USDJPY"]`
- 第二个 FX 候选（排除 `EURUSD`）：`["AUDJPY", "AUDNZD", "AUDUSD", "CADJPY", "CHFJPY", "EURAUD", "EURCHF", "EURGBP", "EURJPY", "EURNZD", "GBPCHF", "GBPJPY", "GBPUSD", "NZDJPY", "NZDUSD", "USDCAD", "USDCHF", "USDJPY"]`
- 当前选定样本：`GBPUSD/H1`
- bars 行数：`64897`
- bars 时间范围：`2016-01-03T22:00:00Z` -> `2026-06-10T00:00:00Z`
- timezone heuristic：`first_bar_utc_like_sunday_reopen`
- IB proof 行数：`5414`
- IB defined：`5412` / `5414`
- OR gate 状态：`blocked_by_timeframe_granularity`
- OR 观察到的命令失败：`ValueError: max() iterable argument is empty`

## 当前裁决

- 第二个 FX 原始输入已经存在，且不止一个候选；当前首个落地样本固定为 `GBPUSD/H1`。
- `GBPUSD/H1` 的 ingest 与 IB proof 可跑，但当前 `H1` 粒度不满足 `30m opening range` 口径。
- 因此这层当前收口为 `input gate`，下一步应切到 `second FX sub-hour input validation`，不把 `H1` 强行写成 OR validation 成功。
