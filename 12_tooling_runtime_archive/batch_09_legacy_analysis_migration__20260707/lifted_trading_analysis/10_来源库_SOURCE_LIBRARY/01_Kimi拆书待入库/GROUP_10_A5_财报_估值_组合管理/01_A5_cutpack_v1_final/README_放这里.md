# A5 cutpack final（财报 / 估值 / 组合管理）

本目录用于承接 `A5` 已完成切分的 md 入口，当前已通过严格复审，可作为库内稳定入口，后续不再依赖 `D:\Stock\cut_file\A5\OUTPUT_MD` 作为唯一入口。

当前稳定入口：

- `5073_Quantitative_Equity_Portfolio_Management\contents.md`
- `Active_Portfolio_Management\INDEX.md`
- `上市公司财报分析与股票估值\INDEX.md`
- `财务报表分析与股票估值_郭永清\INDEX.md`

严格口径：

- `5073_Quantitative_Equity_Portfolio_Management\INDEX.md` 是书末主题索引，不作为本书稳定入口；当前应从 `contents.md` 进入。
- 其余三本书继续以各自目录下的 `INDEX.md` 作为稳定入口。
- 章节级 md 当前已视为通过复审后的稳定子文件。
- `manifest_v2.tsv` 当前记录这 4 个稳定入口。
- 当前目录名保留 `final`，现阶段实际角色是：
  - `stable_split_entry`
  - 当前可视为与 `A1/A2/A3/A4` 同等级的正式 final。

辅助文件说明：

- `Active_Portfolio_Management\.tmp_chapter_boundaries.json`
- `财务报表分析与股票估值_郭永清\.tmp_chapter_map.json`
- `财务报表分析与股票估值_郭永清\.tmp_chapter_map2.json`

当前动作：

- 已复制入来源库，保留为辅助切分痕迹。
- 不作为稳定入口。
- 后续若开始统一 freeze / archive，可单独下沉到辅助层，但当前先保留，不删除。

本轮关键修复项：

- `财务报表分析与股票估值_郭永清\第10章_资产资本表和股权价值增加表的_综合分析.md`
  - 当前正文、公式、表格已可用
  - 当前真值链已改成：
    - `PDF_text_layer` = 主文字源
    - `bycalibre_epub` = 文字校对
    - `EPUB_remake` = 表格结构辅助
  - `表10-6` 已根据图版 + 用户贴回数字手工重排成 md 表格
  - 当前已达到可审查、可入库状态

当前整组 `A5` 已可写成“已正式通过并入库完成”。
