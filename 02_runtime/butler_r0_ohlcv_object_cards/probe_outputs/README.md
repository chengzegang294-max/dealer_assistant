# Probe Outputs

## 用途

- 存放日线拉数 probe 的最小探测产物。
- 成功时应包含：
  - `csv`
  - `metadata.json`
- 失败时至少保留：
  - `metadata.json`

## 生成入口

- `GENERATOR`:
  - `02_runtime/butler_r0_ohlcv_object_cards/tushare_daily_probe_v1.py`
  - `02_runtime/butler_r0_ohlcv_object_cards/akshare_daily_probe_v1.py`
  - `02_runtime/butler_r0_ohlcv_object_cards/baostock_daily_probe_v1.py`

## 当前作用

- 用极短日期区间验证 `Tushare Pro / AkShare / Baostock` 是否可用。
- 这里只保留 probe 证据；正式在线日线入口提升到 `02_runtime/butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv/`。

## 当前结果

- 已对 `300302.SZ / 20240101-20240131` 执行一次探测。
- 当前失败原因：`tushare_token_missing`
- `AkShare` 已安装，但当前探测失败：`RemoteDisconnected`
- `Baostock` 已安装并探测成功，返回 `22` 行日线数据
