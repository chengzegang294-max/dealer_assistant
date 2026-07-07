## 用途

- 这里保留 `XBreaking` 的 `tester report` 回收件。
- 当前目录作为占位落盘，避免默认回收目录只存在于文档里、不存在于仓库树中。

## 当前状态

- `status`: `pending`
- `expected_producer`: `MT5 strategy tester` 或 `MT4 strategy tester`
- `expected_files`: `.htm / .html`

## 规则

- 进入本目录的报告必须能回指到 `XBreakingProbe.ini` 或 `MT4Probe_XBreaking.ini`。
- 回收后同步更新上层批次索引、语义日志和备注总表。
