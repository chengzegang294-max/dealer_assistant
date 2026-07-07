# GROUP_08 — pdf 保留型切割 v2（删源可用）

目标：
- 从 `GROUP_08_A股量化_数据研究__SOURCE_RAW` 重新切割 pdf，生成“删源也可用”的 md。
- 本目录只放 v2 的最终 md 产物。

合同：
- `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\CUT_CONTRACT__Kimi_全文保留优先_v1.md`
- `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\CUT_CONTRACT__Kimi_保留型切割_v2.md`

切割策略（拍板）：
- 对本组 61 个研究 pdf：默认走 `全文保留优先` 合同
  - 小文件（<=5MB）优先 `FULL_TEXT_RETAIN`
  - 否则 `EXCERPT_RETAIN`（25–60 条原文保留卡片）
- 每个 pdf 至少产出 1 个 md。若 md 过长，允许拆成：
  - `_part1`
  - `_part2`
  - `_part3`

命名约定：
- `CUTPACK__G08__<BUCKET>__<TITLE_SHORT>__v2.md`
- BUCKET 建议取：
  - `择时`
  - `资产配置`
  - `选股`

验收：
- 每个 pdf 都有对应的 v2 md
- 每份 v2 md 都包含：
  - `QUANTIZATION_TABLE`
  - `FULL_TEXT` 或 `RETAINED_EXCERPTS`
- 验收通过后可删除：
  - `GROUP_08_A股量化_数据研究__SOURCE_RAW\《Python股票量化交易从入门到实践》完整版`
