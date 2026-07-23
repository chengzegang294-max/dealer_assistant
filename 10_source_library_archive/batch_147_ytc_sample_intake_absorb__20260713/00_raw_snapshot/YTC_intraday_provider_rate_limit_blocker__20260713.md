# YTC 分钟样本 provider 限频阻塞说明

更新时间：2026-07-14

## 文件类型

- `INDEX_NOTE`

## 原路径

- `terminal live fetch attempt`

## 新路径

- `batch_147/00_raw_snapshot/YTC_intraday_provider_rate_limit_blocker__20260713.md`

## 生成入口

- `manual_terminal_blocker_note`

## 适用对象

- `YTC`

## 当前作用

- 固定为什么本轮已经找到可用 provider，却仍未把 `60m/5m` 完整 csv 一次落盘。
- 防止后续误判成“没想到 provider”或“还没开始试”。

## 当前已确认事实

- `Tushare` token 在当前环境可用。
- 本轮已成功拉到：
  - `601991.SH`
  - `60min`
  的 live probe 结果。
- 随后继续请求 `stk_mins` 时，接口返回：
  - `频率超限`
  - 日志中同时出现：
    - `1次/分钟`
    - `1次/小时`
- 本轮已额外等待约 `75s` 后再次请求：
  - `5min`
  - 仍然返回：
    - `频率超限`
- 因而当前不能把阻塞简单写成：
  - `再等一分钟即可`
- `2026-07-14` 再次直接执行单次 `5min` 抓取并尝试本地聚合 `60m`：
  - 仍然失败
  - 日志中再次同时出现：
    - `1次/小时`
    - `1次/分钟`
  - 且本轮没有生成：
    - `601991_SH_5m.csv`
    - `601991_SH_60m.csv`

## 当前阻塞判断

- 当前阻塞不是：
  - symbol 不存在
  - provider 不可用
  - 字段合同没定
- 当前真正阻塞是：
  - provider 频率限制导致同轮无法继续把完整 `60m/5m` csv 一口气落完

## 当前裁决

- `60m`
  - 已有 live probe 强化证据
  - 但完整 csv 仍待 provider 窗口释放后正式落盘
- `5m`
  - 当前仍未拿到 live probe 结果
  - 原因同样属于 provider 限频阻塞
  - 且当前更像：
    - `hour-window blocked`

## 后续最小动作

- 等下一次允许窗口到达后，优先执行：
  - `601991_SH_60m.csv`
  - `601991_SH_5m.csv`
- 然后立刻补：
  - 对应 provenance note
  - `BATCH_147_ARTIFACT_INDEX_v1.md`
  - `YTC_SAMPLE_REQUIREMENT_v1.tsv`

## 当前结论

- `batch_147` 这条线已经不再缺判断、模板和 provider 方向。
- `2026-07-14` 已改由项目外外部历史分钟数据仓完成补件：
  - `601991_SH_5m.csv`
  - `601991_SH_60m.csv`
- 因而本页当前只保留为：
  - `Tushare stk_mins` 路线的历史阻塞记录
  - 不再作为 `batch_147` 未闭合的唯一依据
