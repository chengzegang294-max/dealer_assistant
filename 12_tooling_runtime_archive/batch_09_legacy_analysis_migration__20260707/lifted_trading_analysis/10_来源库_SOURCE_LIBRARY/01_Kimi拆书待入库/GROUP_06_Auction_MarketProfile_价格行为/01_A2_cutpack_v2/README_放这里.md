# A2 cutpack v2

本目录用于存放 A2（Auction / Market Profile / 盘中结构）的删源可用切割产物。

文件：

- `BATCH_SUMMARY__A2__v2.md`
- `CUTPACK__A2__Dalton__MindOverMarkets__v2.md`
- `CUTPACK__A2__Dalton__MarketsInProfile__v2.md`
- `CUTPACK__A2__Harris__TradingAndExchanges__v2.md`
- `CUTPACK__A2__CN__市场轮廓理论__part1__v2.md`
- `CUTPACK__A2__CN__市场轮廓理论__part2__v2.md`

当前状态：

- 《市场轮廓理论：价格走势分析的崭新视点》已不再使用旧的扫描版占位 cutpack。
- 正式版本改为基于 `epub` 主文本 + `pdf` 术语/页码交叉核对的 split cutpack（`part1` / `part2`）。
- `part1` 负责：
  - `BASIC_INFO`
  - `BOOK_STRUCTURE`
  - `RETAINED_EXCERPTS`
  - `CORE_CONCEPTS`
- `part2` 负责：
  - `QUANTIZATION_TABLE`
  - `FORMULAS_AND_ALGOS`
  - `NOT_QUANT_YET`
  - `NEXT_ACTION`

验收：

- 每份 cutpack 必须包含：
  - `QUANTIZATION_TABLE`
  - `RETAINED_EXCERPTS` 或 `FULL_TEXT`
- `RETAINED_EXCERPTS.quote` 不允许为空
- 不允许残留 `NEEDS_OCR` / 占位符 / `[原文待提取]`
