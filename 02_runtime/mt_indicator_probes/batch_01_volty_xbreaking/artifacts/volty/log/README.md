## 用途

- 这里保留 `Volty` 的 `tester log / journal` 回收件。
- 当前目录作为占位落盘，避免 `csv / report` 已在仓库、但 `log` 目录实际缺失。

## 当前状态

- `status`: `pending`
- `expected_producer`: `MT4 strategy tester / terminal journal`
- `evidence_mode_on_first_arrival`: `fresh_run` 或 `historical_recovered`

## 规则

- 不把无关键词命中的通用日志直接当 `Volty` 强证据。
- 回收后同步更新上层批次索引与备注总表。
