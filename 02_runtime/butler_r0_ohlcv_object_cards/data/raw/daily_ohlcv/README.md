# Online Daily OHLCV

## 用途

- 存放已经通过最小在线 probe 验证、允许进入 runtime 正式输入面的日线 OHLCV 数据。
- 当前目录只收“可追溯提升”的在线日线数据，不直接混放 `probe_outputs/` 原始探测证据。

## 入口规则

- `GENERATOR`:
  - `02_runtime/butler_r0_ohlcv_object_cards/tushare_daily_probe_v1.py`
  - `02_runtime/butler_r0_ohlcv_object_cards/akshare_daily_probe_v1.py`
  - `02_runtime/butler_r0_ohlcv_object_cards/baostock_daily_probe_v1.py`
  - `02_runtime/butler_r0_ohlcv_object_cards/baostock_daily_fetch_to_raw_v1.py`
- `INDEX_NOTE`:
  - 当前文件
  - `catalog_v1.tsv`

## 当前口径

- 顶层目录合同不允许仓库根层随手新开 `data/`，所以正式数据入口挂在 `02_runtime/butler_r0_ohlcv_object_cards/` 下。
- `probe_outputs/` 保留“当前终端实跑证据”。
- 当前目录保留“允许被后续 runtime 引用的正式输入副本”。

## 当前内容

- 首个提升样本来自 `Baostock` 成功探测：
  - `300302_SZ__1d__baostock__20240101_20240131.csv`
- 后续新增标的优先通过 `baostock_daily_fetch_to_raw_v1.py` 正式写入，并自动更新 `catalog_v1.tsv`
- 历史 `batch09` 的两批 A 股日线已归位到：
  - `batch09_promoted/ashare_clean/`
  - `batch09_promoted/watchlist_kline_1d/`
- 历史归位与正式在线拉取共用 `catalog_v1.tsv`，但用不同 `source_type / evidence_mode` 区分。
- 当前仍是最小正式入口，不等于完整主数据仓。

## 证据强度

- `probe_outputs/*.json` 与 probe 原始 csv：`hard`
- 当前目录内由 probe 提升的正式输入副本：`hard_promoted_from_probe`
- 当前目录内由正式 fetch 直接生成的 csv 与 metadata：`hard`
- 当前目录内由 `batch09` 归位提升的历史 csv：`historical_recovered`
