# MT Indicator Probes Runtime

## 用途

- 这里放 `MT4 / MT5` 指标 probe 的运行时批次包。
- 当前只负责收纳 probe 产物、执行口径和批次索引。
- 这里不是默认交易执行链路，也不是策略门控目录。

## 当前批次

- `batch_01_volty_xbreaking`
  - 用于 `Volty / XBreaking` 首批 probe 落盘与证据收口。
  - 已含 `ingest + acceptance` 双脚本与批次级验收单。

## 产物要求

- 每个批次至少要留下：
  - 执行卡
  - 产物索引
  - `csv` 路径
  - `log` 或 tester report 路径
- 证据不足时可以先写 `pending`，但不能伪造“已跑通”。

## 当前边界

- 允许：
  - `iCustom / CopyBuffer / mode scan` 级 probe 证据
  - 参数快照
  - 文件落盘路径
  - 语义观察与字段映射裁决
- 不允许：
  - 直接把 probe 结果升级为默认交易门控
  - 未经验证就宣称某个 buffer 等于买卖信号
