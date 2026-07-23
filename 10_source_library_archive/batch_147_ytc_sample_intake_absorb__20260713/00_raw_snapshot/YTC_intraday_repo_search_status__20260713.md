# YTC 分钟样本仓内搜索状态

更新时间：2026-07-13

## 文件类型

- `INDEX_NOTE`

## 原路径

- 搜索范围：
  - `d:/Stock/trading_assistant/02_runtime`
  - `d:/Stock/trading_assistant/12_tooling_runtime_archive`

## 新路径

- `batch_147/00_raw_snapshot/YTC_intraday_repo_search_status__20260713.md`

## 生成入口

- `manual_repo_search_note`

## 适用对象

- `YTC`

## 当前作用

- 固定本轮针对 `YTC 60m/5m` 真样本的仓内搜索结论。
- 防止后续重复重搜同一遍目录。

## 证据强度

- `weak_evidence`

## 本轮搜索结论

- 已确认仓内存在：
  - `601991_SH_1d.csv`
  - `601991_SH_1w.csv`
  - `ytc_601991_sh_daily_weekly_output.json`
- 已确认 `02_runtime/butler_r0_ohlcv_object_cards` 存在的正式 fetch/probe 入口只有：
  - `baostock_daily_fetch_to_raw_v1.py`
  - `baostock_daily_probe_v1.py`
  - `akshare_daily_probe_v1.py`
  - `tushare_daily_probe_v1.py`
- 本轮没有找到：
  - `601991.SH` 的 `60m` 样本实物
  - `601991.SH` 的 `5m` 样本实物
  - `300302.SZ` 的 `60m/5m` 样本实物
  - A 股分钟级正式 fetch 结果

## 当前阻塞点

- 不是 `YTC` 对象口径没定。
- 也不是 repo 没有样本目录。
- 当前真正缺的是：
  - A 股分钟级样本实物本体
  - 对应 provider 执行结果

## 与 legacy 分钟脚本的关系

- `12_tooling_runtime_archive` 里能看到：
  - `m5`
  - `m15`
  - `aggregate_bars_to_m5`
  这类脚本与样本
- 但当前都属于：
  - `FX / subhour / proof-of-mapping` 背景
- 当前不能直接拿来冒充：
  - `A股 60m/5m` 真样本

## 当前结论

- `batch_147` 现在已经不是“没搜过”。
- 当前状态应写成：
  - `repo_search_done__intraday_artifact_missing`

## 下一刀

- 继续补：
  - provider 候选矩阵
  - 最小分钟样本补采路径
