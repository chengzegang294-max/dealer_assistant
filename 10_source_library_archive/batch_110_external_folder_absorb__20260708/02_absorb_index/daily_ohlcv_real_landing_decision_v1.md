# Daily OHLCV Real Landing Decision v1

更新时间：2026-07-08

## 结论

- `data/raw/daily_ohlcv/` 仍然是未来标准目标路径，但当前仓库并不存在，不能继续把它当成“已经可用”的真实落点。
- 现阶段真正可用的 A 股日线落点有两类：
  - `00_assets/_raw_snapshot_batch09/ashare_clean/*.csv`
  - `00_assets/_raw_snapshot_batch09/ashare_watchlist/kline_1d/*.csv`
- 因此下一阶段应采用“双轨”：
  - **轨道 A（立即可用）**：从 `00_assets` 复制最小样本到 `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/`
  - **轨道 B（标准目标）**：等 `Tushare/AkShare/Baostock` 主备源拍板后，再正式创建 `data/raw/daily_ohlcv/`

## 当前最顺动作

1. 用 `ashare_clean` + `watchlist/kline_1d` 先喂通 `VOLFAC/BPB/VP/TKR7/VOLTARGET/PERIOD_QUEEN` 的最小验收样本。
2. 同时把 `Tushare/AkShare/Baostock` 的主备源裁决写成数据源合同，不再继续假设旧目录存在。
