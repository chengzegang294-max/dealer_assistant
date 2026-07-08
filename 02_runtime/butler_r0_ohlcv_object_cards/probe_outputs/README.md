# Probe Outputs

## 用途

- 存放 `tushare_daily_probe_v1.py` 的最小探测产物。
- 成功时应包含：
  - `csv`
  - `metadata.json`
- 失败时至少保留：
  - `metadata.json`

## 生成入口

- `GENERATOR`: `02_runtime/butler_r0_ohlcv_object_cards/tushare_daily_probe_v1.py`

## 当前作用

- 用极短日期区间验证 `Tushare Pro` 是否可用。
- 先探测，再决定是否正式创建 `data/raw/daily_ohlcv/` 与 catalog 入口。

## 当前结果

- 已对 `300302.SZ / 20240101-20240131` 执行一次探测。
- 当前失败原因：`tushare_token_missing`
