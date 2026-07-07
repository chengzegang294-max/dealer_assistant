# GROUP_08 A股量化 数据研究

## 作用

- 存放这批 `新的参考书` 经过 `Kimi` 切分后的 `md` 产物。
- 当前角色：
  - `A股 future research/data capability` 的待入库区
  - 不直接进入当前 `FX + TK` 主线

## 上传落点

- `01_62份研究PDF`
  - 放研究 `pdf` 三组摘要
- `02_pdf入门书`
  - 放 `pdf` 入门书的总索引与章节卡片
- `03_txt标题聚类`
  - 放 `txt` 的主题聚类与内容保留产物
- `04_epub目录粗切`
  - 放 `epub` 的保留型粗切产物
- `05_txt源码_md归档`
  - 放 `99` 份 `txt` 的“全文保留型 md”（按分桶归类 + 索引）

## 当前已落地文件

- v1 产物（已存在，但将被 v2 重做替换）
- 研究 `pdf`
  - `A股_量化择时_研究PDF_总摘要_v1.md`
  - `A股_量化资产配置_研究PDF_总摘要_v1.md`
  - `A股_量化选股_研究PDF_总摘要_v1_part1.md`
  - `A股_量化选股_研究PDF_总摘要_v1_part2.md`
  - `A股_量化选股_研究PDF_总摘要_v1_index.md`
- `pdf` 入门书
  - `A股_pdf入门书_章节切分总索引_v1.md`
  - `A股_pdf入门书_章节卡片_v1.md`
- `txt`
  - `A股_txt标题聚类与内容保留_v1.md`
- `txt` 源码全文保留（md）
  - `05_txt源码_md归档\README_放这里.md`
  - `05_txt源码_md归档\txt_md_index_v1.tsv`
- `epub`
  - `A股_epub_保留型粗切_v1.md`

## 命名口径

- 这里只保留最终 `md` 产物，不再往这个目录贴原始聊天回复。
- 若输出过长，允许使用：
  - `part1`
  - `part2`
  - `index`
- 若后续有人工复核结论，优先写进长期主文档或专门检查文件，不混进本 `README`。

## 说明

- 这里只放 `md`。
- 原始 `pdf / epub / txt` 不重复放入这里。
- 这里的文件仍属于：
  - `secondary_structured_note`
  - 待入库区
  - 不等同于原书原文或源码级证据
  - 但 `txt` 已额外提供“全文保留型 md”，可用于删源前的覆盖检查

## v2 目标（删源可用）

- v2 不再做“索引型导引”为主的产物，而是输出：
  - `FULL_TEXT`（小文件优先全文保留）或 `RETAINED_EXCERPTS`（高密度原文片段卡片）
  - `QUANTIZATION_TABLE`（可量化映射表）
- v2 产物落点：
  - `06_pdf_retained_cut_v2`
  - 完成后允许删除对应的 `__SOURCE_RAW` 源文件夹
- 当前质量缺口：
  - `量化交易之路：用Python做股票量化分析 - 未知.epub` 属于图片型 epub，无可提取文本层
  - 当前已用可提取的 PDF 版本替代，并拆成 4 个 part（均为 `extract_status: success`）：
    - `CUTPACK__G08__选股（Python量化技术）__量化交易之路Python分析_part1__v2.md`
    - `CUTPACK__G08__选股（Python量化技术）__量化交易之路Python分析_part2__v2.md`
    - `CUTPACK__G08__选股（Python量化技术）__量化交易之路Python分析_part3__v2.md`
    - `CUTPACK__G08__选股（Python量化技术）__量化交易之路Python分析_part4__v2.md`

## 怎么用起来（建议顺序）

- 用来支持“补书/补资料类型”的多 AI 讨论：
  - 这批更偏 `因子/事件/行业轮动` 与 `策略模板池`，不代表已经覆盖了 `A股情绪周期 / Auction / PIT 数据工程` 等方向
- 用来做第一轮“可重开候选”提炼（不进当前 FX+TK 主线）：
  - 从研究 `pdf` 的摘要里，优先抽 `事件驱动 / 行业轮动 / 因子研究` 的候选对象与数据需求
  - 从 `txt` 里只保留少数“规则壳清晰”的模板样本，其余维持模板池定位
  - `epub` 只作为“策略类型与流程壳”的解释层素材，暂不做深切

## 下一步（用来支持删源与后续吸收）

- 先做 coverage 对账：
  - 源目录（已迁移并保留原始 pdf/epub/txt）：`12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书`
  - 产物目录：本 `GROUP_08`
- 再做四分流收口（本组内的 v1 裁决）：
  - 已吸收（结构与目录口径）
  - 可重开（候选对象/字段/数据需求）
  - future bucket（暂不量化的内容）
  - 仅来源库保留（仅保留来源，不做进一步处理）
- 对账通过后，再决定是否删除源目录
  - 当前进度：`txt` 已可做到“删源仍保留全文”；`pdf/epub` 仍建议先保留源目录作为真值锚点
  - v2 完成后：`pdf/epub` 也按“删源可用”口径执行
