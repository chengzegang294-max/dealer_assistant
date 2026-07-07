# Kimi 拆书待入库 批次检查 v1

## 本轮检查范围

- 目录：
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库`
- 已看到的落地文件包括：
  - `GROUP_01_microstructure_master_part_01/02/03.md`
  - `GROUP_02_options_volatility_master_part_01/02/03.md`
  - `GROUP_03_portfolio_risk_master_part_01/02/03.md`
  - `GROUP_04_stat_arb_research_master_part_01/02/03.md`
  - `GROUP_05_trend_system_trading_STATE_TEMPLATE.md`
  - `GROUP_05_trend_systematic_trading.md`
  - `GROUP_06_market_profile_price_action.md`
  - `GROUP_06_market_profile_price_action_DEFINITIONS.md`
  - `GROUP_07_quant_history_index.md`
  - `GROUP_08_A股量化_数据研究\01_62份研究PDF\*.md`
  - `GROUP_08_A股量化_数据研究\02_pdf入门书\*.md`
  - `GROUP_08_A股量化_数据研究\03_txt标题聚类\A股_txt标题聚类与内容保留_v1.md`
  - `GROUP_08_A股量化_数据研究\04_epub目录粗切\A股_epub_保留型粗切_v1.md`

## 当前检查结论

- 这批文件整体不是乱稿，已经具备“待入库区”应有的基本结构：
  - 有分组
  - 有主文件名
  - 多数组按 `part_01/02/03` 或主题文件拆分
  - 内容明显是结构化整理稿，不是聊天碎片
- 当前可以继续维持：
  - `secondary_structured_note`
  - `inbox_only`
  - 不直接当源码级/原书原文证据

## 分组检查

### Group 01 微观结构 / 交易所 / HFT

- 当前状态：可入库候选，结构完整。
- 已见特点：
  - 有总览
  - 有统一术语表
  - 有字段清单
  - 有模型族与执行 checklist
- 价值判断：
  - 对执行层、滑点、微观结构字段扩展价值高
  - 但数据需求大量超出当前纯 OHLC 主线
- 当前建议：
  - 先吸收术语、成本分层、失败模式
  - 字段部分只做候选，不直接落盘

### Group 02 期权 / 波动率 / 波动率微笑

- 当前状态：结构完整，但和当前主线距离较远。
- 已见特点：
  - 公式表
  - 策略模板
  - 曲面建模条目
- 价值判断：
  - 适合中长期来源库扩展
  - 不属于当前 Batch9 / MT5 / 现货主线第一优先
- 当前建议：
  - 暂列第三优先吸收
  - 先保留，不急着拆字段

### Group 03 组合管理 / 风险模型 / 交易成本

- 当前状态：结构完整，可作为研究与组合层方法库。
- 已见特点：
  - 组合构建 pipeline
  - 风险模型公式
  - 偏差检查清单
- 价值判断：
  - 对组合层和评估层有用
  - 对当前单指标来源库主线不是第一优先
- 当前建议：
  - 先吸收偏差检查与组合约束条目
  - 字段清单延后

### Group 04 统计套利 / 研究方法 / ML

- 当前状态：结构完整，方法论价值高。
- 已见特点：
  - 研究 SOP
  - 偏差与过拟合防线
  - 审计清单
- 价值判断：
  - 对仓库的“研究流程护栏”和回测偏差控制很有用
  - 不一定直接产当前字段，但很适合补通用方法库
- 当前建议：
  - 放第二优先吸收
  - 先吸收 checklist / bias guard / validation rules

### Group 05 趋势 / 系统交易

- 当前状态：当前最值得优先吃的一组之一。
- 已见特点：
  - 已有 `STATE_TEMPLATE` 风格文件
  - 四轴状态、参数表、禁止跑偏规则、跨书裁决都比较贴近当前仓库表达方式
- 价值判断：
  - 和当前状态模板、执行清单、规则化语言最接近
  - 可直接服务后续状态模板化整理
- 当前建议：
  - 列第一优先吸收
  - 先做结构/风险/禁止跑偏规则的最小吸收

### Group 06 Auction / Market Profile / 价格行为

- 当前状态：当前最值得优先吃的一组之一。
- 已见特点：
  - 有 `DEFINITIONS` 版
  - 有统一对象定义
  - 有判定树
  - 有 N02 / 结构标签映射
- 价值判断：
  - 对 `N02`、结构定义、价格行为对象化非常有帮助
  - 比很多纯叙述性书稿更接近“可编程定义”
- 当前建议：
  - 列第一优先吸收
  - 先吸收对象定义、判定树、仓库标签映射

### Group 07 传记 / 行业史 / 故事

- 当前状态：索引式入库，符合预期。
- 已见特点：
  - 术语索引
  - 方法论提炼
  - 风险与失败模式
  - 二次精读清单
- 价值判断：
  - 适合做研究文化、失败案例、术语补充
  - 不适合当前主线直接拆字段
- 当前建议：
  - 继续只做索引保留
  - 不列入第一轮精吸收

### Group 08 A股量化 / 数据研究

- 当前状态：首轮切分已实际落地，但目前更像“待入库结构化整理区”，还不能当成 coverage 已完全对齐。
- 已见特点：
  - `01_62份研究PDF` 已形成 `5` 个 `md`
  - `02_pdf入门书` 已形成 `2` 个 `md`
  - `03_txt标题聚类` 已形成 `1` 个保留型聚类稿
  - `04_epub目录粗切` 已形成 `1` 个保留型粗切稿
- 当前真值对账：
  - 源目录 `新的参考书` 实际为：
    - `99 txt`
    - `61 pdf`
    - `2 epub`
  - 但 `GROUP_08` 内部仍有自报口径冲突：
    - `txt` 稿仍写成“实际收到 `97` 份、缺 `2` 份”
    - `量化选股` 稿仍写成“本组 `41` 份，缺 `1` 份”
  - 因此当前不能把 `GROUP_08` 视为“已完成 coverage 审计”
- 价值判断：
  - 这批材料已经足够证明上传结果到位，不是空目录
  - 对 `A股 future research/data capability` 很有价值
  - 但当前仍属于：
    - `secondary_structured_note`
    - 待入库区
    - 不等同于原源文件可立即删除
- 当前四分流（v0）：
  - 已吸收：
    - `GROUP_08` 的目录结构、命名口径、首轮 `md` 产物已落地
  - 可重开：
    - 研究 `pdf` 中的事件驱动 / 行业轮动 / 因子研究候选
    - `pdf` 入门书中的数据获取 / 清洗 / 回测工具章节
    - `txt` 中少数可复用规则壳样本
  - future bucket：
    - 大量社区练习型 `txt`
    - 老旧或强案例化的策略讲义
    - `epub` 里偏案例展示的部分
  - 仅来源库保留：
    - 当前 coverage 未对齐前，源目录已迁移为 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书`，继续作为真值锚点
- 当前建议：
  - 先不要删源目录
  - 先补：
    - `GROUP_08` 与源目录的 coverage 对账
    - 冲突数字回查
    - 产物与源目录映射清单
  - 对账完成后，再决定是否删 `新的参考书`

## 当前吸收优先级

- 第一优先：
  - `GROUP_05_趋势_系统交易`
  - `GROUP_06_Auction_MarketProfile_价格行为`
- 第二优先：
  - `GROUP_01_微观结构_交易所_HFT`
  - `GROUP_04_统计套利_研究方法_ML`
- 第三优先：
  - `GROUP_03_组合管理_风险模型_交易成本`
  - `GROUP_02_期权_波动率_波动率微笑`
- 索引保留：
  - `GROUP_07_传记_行业史_故事`

## 当前不做的事

- 不把这批稿件直接写成正式来源库正文
- 不把 Kimi 稿直接当原书原文
- 不把其中候选字段直接落盘到现有 CSV 合约

## 下一步建议

- 先从 `GROUP_05 + GROUP_06` 做最小吸收：
  - 提炼通用对象
  - 提炼状态模板
  - 提炼禁止跑偏规则
  - 提炼仓库标签映射
- 再从 `GROUP_01 + GROUP_04` 提炼：
  - 执行成本
  - 微观结构风险
  - 研究偏差/验证清单

## 2026-06-21 第二轮收口补记

- 本轮按目录级重扫后，`01_Kimi拆书待入库` 当前为 `420` 文件，其中根目录 `13` 文件，主要扩展名为：
  - `.md = 399`
  - `.tsv = 17`
  - `.json = 4`
- 当前大头组别已明确：
  - `GROUP_08_A股量化_数据研究`：`178` 文件
  - `GROUP_10_A5_财报_估值_组合管理`：`113` 文件
  - `GROUP_09_完善体系书库_切割产物`：`56` 文件
  - `GROUP_06_Auction_MarketProfile_价格行为`：`22` 文件
  - `GROUP_01_微观结构_交易所_HFT`：`15` 文件
  - `GROUP_05_趋势_系统交易`：`13` 文件

## 第二轮四分流（v1.1）

- `已吸收 / 稳定入口`
  - `GROUP_09_完善体系书库_切割产物`
    - 已有 `*_final` 稳定入口，根层重复副本已被明确标成历史层候选。
  - `GROUP_10_A5_财报_估值_组合管理`
    - 已通过严格复审，当前按正式通过口径使用。
- `可重开`
  - `GROUP_05_趋势_系统交易`
    - 最适合提炼 `state template / risk rules / no-drift rules`。
  - `GROUP_06_Auction_MarketProfile_价格行为`
    - 最适合提炼 `对象定义 / 判定树 / N02 标签映射`。
  - `GROUP_01_微观结构_交易所_HFT`
    - 适合提炼 `执行成本 / 流动性 / 微观结构风险`，但大量定义超出当前纯 OHLC。
  - `GROUP_04_统计套利_研究方法_ML`
    - 适合提炼 `研究 SOP / bias guard / validation rules`。
  - `GROUP_08_A股量化_数据研究`
    - 有候选价值，但当前先受 `coverage` 对账约束，不宜直接当成已完成吸收。
- `future bucket`
  - `GROUP_02_期权_波动率_波动率微笑`
  - `GROUP_03_组合管理_风险模型_交易成本`
- `仅来源库保留 / 索引保留`
  - `GROUP_07_传记_行业史_故事`
  - `GROUP_08_A股量化_数据研究__SOURCE_RAW`
  - `GROUP_09` 根层重复副本与旧版目录，当前保留，后续统一 freeze/archive 再处理。

## 第二轮首批重开项

- 第一重开：`GROUP_06_Auction_MarketProfile_价格行为`
  - 进入条件：已存在 `DEFINITIONS`、对象定义、`GROUP_06 -> N02` 候选入口。
  - 退出条件：提炼出最小对象表、判定树和仓库标签映射，不继续扩成整组重写。
- 第二重开：`GROUP_05_趋势_系统交易`
  - 进入条件：已有 `STATE_TEMPLATE` 风格文件，和仓库状态模板语言最接近。
  - 退出条件：提炼出四轴状态模板、风险规则、禁止跑偏规则，不直接落盘新字段。

## 第二轮当前不做

- 不重扫整个 `S桶` 原始 PDF。
- 不把 `GROUP_08` 直接判成“可删源完成”。
- 不把 `GROUP_01/04` 直接升级成首批硬门控对象。

## 第二轮首批重开落地：GROUP_06 最小吸收

- 已新增：
  - `GROUP_06_Auction_MarketProfile_价格行为\GROUP_06_最小吸收包_v1.md`
- 本轮已把 `GROUP_06` 的首批重开范围收紧为三件事：
  - 最小对象表
  - 最小判定树
  - `N02` 标签映射草案
- 当前明确顺序：
  - 先 `Opening Type + Initial Balance`
  - 再 `POC + Value Area`
  - 最后 `Balance vs Imbalance + Day Type`
- 当前冻结区：
  - `TPO` 精细字母矩阵
  - `Single Prints / Tails / Excess` 严格识别
  - `DOM / Level2 / Order Book`
  - Brooks 主观信号条目字段化

## 第二轮首批重开落地：GROUP_05 最小吸收

- 已新增：
  - `GROUP_05_趋势_系统交易\GROUP_05_最小吸收包_v1.md`
- 本轮已把 `GROUP_05` 的首批重开范围收紧为四件事：
  - 最小状态模板
  - 最小风险规则
  - 最小禁止跑偏规则
  - 仓库映射草案
- 当前明确顺序：
  - 先四轴状态模板
  - 再风险与摩擦护栏
  - 最后才讨论是否有对象继续下沉
- 当前冻结区：
  - `70-tick` 图专属 setup 细则
  - `10 pip / 10 pip OCO` 固定止盈止损
  - `Trader Effect Density` / `COT / CTA AUM`
  - `Tipping Point` 主观退出法

## 第二轮后续对账：GROUP_08 coverage

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_coverage_对账_v1.md`
- 本轮当前裁决：
  - `txt` 线已基本对齐，`txt_md_index_v1.tsv` 可作为源到产物映射锚点
  - `量化选股 research pdf` 的旧“缺 1 份”口径已修正为“源目录对账后无缺失”
  - `pdf/epub` 当前只能算局部删源可用，不能把整组判成 coverage 完成
- 当前不变结论：
  - `GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书` 继续保留为真值锚点
  - 当前不删源

## 第二轮后续对账：GROUP_08 逐源 coverage 总表

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_逐源coverage总表_v1.md`
- 本轮进一步收口为两层：
  - `txt` 线：通过 `txt_md_index_v1.tsv` 做逐源精确回指
  - `pdf/epub` 线：先收成源线级总表，不假装整组逐源审计已完成
- 当前意义：
  - 已把 `SOURCE_RAW -> 现有产物 -> 当前删源边界` 固定成可复用骨架
  - 下一轮若继续，只需要把 `pdf/epub` 从源线级补成逐源级

## 第二轮后续对账：GROUP_08 research pdf 逐条映射

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_research_pdf_逐条映射清单_v1.md`
- 当前进一步明确：
  - `research pdf` 已从“源线级总表”推进到“逐条标题锚点 -> v2 md”清单
  - 但当前仍不是“删源已完成”
- 当前新增外部真值源约束：
  - `D:\Stock\cut_file\S` 必须继续作为这批 `research pdf` 的外部真值锚点之一
  - 后续凡是要说“整理后可删”，必须同时通过：
    - 仓库内 `GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书`
    - 外部 `D:\Stock\cut_file\S`
    - 两侧删除验收

## 第二轮后续对账：GROUP_08 双侧删除验收

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_双侧删除验收表_v1.md`
- 当前正式裁决：
  - 仓库内侧：`PARTIAL_DELETE_READY`
  - 外部侧 `D:\Stock\cut_file\S`：`NOT_DELETE_READY`
- 当前明确：
  - `txt` 线可进入删源候选
  - `research pdf` 还需逐文件删除勾验
  - `pdf 入门书 / epub` 当前不删
  - `D:\Stock\cut_file\S` 整目录当前不可删，只能未来考虑 `03_券商研报` 下与 `GROUP_08` 对应的局部子集

## 第二轮后续对账：GROUP_08 逐文件删除勾验行

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_逐文件删除勾验行_v1.md`
- 当前进一步推进为：
  - `2` 条择时候选删除勾验行
  - `1` 条重复源保留行
  - `16` 条资产配置删除勾验行
  - `41` 条选股删除勾验行
- 当前还缺的只剩两类：
  - 仓库内侧最终删除勾选
  - 外部 `D:\Stock\cut_file\S\03_券商研报` 对应子集的精确路径 + 最终删除勾选

## 第二轮后续对账：GROUP_08 最终删除勾选

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_最终删除勾选_v1.md`
- 当前明确回答了两个问题：
  - 为什么前面整理了但文件没大变
  - 外部文件哪些现在能整理移动、哪些必须后置
- 当前正式裁决：
  - 仓库内 `txt` 线：`DELETE_READY`
  - 外部 `D:\Stock\cut_file\S\03_券商研报` 对应子集：`MOVE_READY_NOT_DELETE`
  - 外部 `D:\Stock\cut_file\S` 整目录：`HOLD`
  - 外部 `D:\Stock\cut_file\S\01_集合竞价教程`：`HOLD`

## 第二轮后续对账：GROUP_08 外部精确路径勾验

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_外部精确路径勾验_v1.md`
  - `GROUP_08_A股量化_数据研究\GROUP_08_外部精确路径勾验_v1.tsv`
  - `GROUP_08_A股量化_数据研究\00_external_import_staging\README.md`
- 本轮自动化比对结果：
  - `60` 条标题锚点
  - `477` 份外部 `pdf`
  - `1` 条 `EXACT_LIKE_MATCH`
  - `59` 条 `NO_MATCH`
- 当前正式执行建议：
  - 不按标题盲 move 外部文件
  - 改走“路径驱动复制入库 + 台账核对 + 后删外部”

## 第二轮后续对账：GROUP_08 前后路径台账 + 第一批 staging copy

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_前后路径台账_v1.tsv`
- 本轮真实执行结果：
  - 已写出 `60` 条 `source_path_before -> repo_staging_path_after` 台账记录
  - 已完成 `1` 条 `EXACT_LIKE_MATCH` 的第一批 staging copy
  - 当前已复制样本：
    - `S-009 -> 00_external_import_staging\confirmed_exact\04_多因子\海通选股因子系列研究6：极值视角下的多因子选股策略.pdf`
  - 其余 `59` 条当前保持：
    - `WAIT_MANUAL_PATH`
- 当前执行口径进一步固定为：
  - 先补精确路径
  - 再扩大 staging copy
  - 最后才讨论外部对应子集删除

## 第二轮后续对账：GROUP_08 第二批精确路径补齐 + 第二批 staging copy

- 已新增：
  - `tools\group08_batch2_series_copy.py`
- 本轮真实执行结果：
  - 已基于 `S_BUCKET_INDEX__2026-06-17.tsv` 与 `海通选股因子系列研究1-6` 系列号闭环，新增确认 `S-037 ~ S-041`
  - `GROUP_08_外部精确路径勾验_v1.tsv` 已新增 `5` 条 `SERIES_MANUAL_CONFIRMED`
  - `00_external_import_staging\confirmed_series\04_多因子\` 已新增 `5` 份外部原件副本
  - 当前累计已复制：
    - `1` 条 `EXACT_LIKE_MATCH`
    - `5` 条 `SERIES_MANUAL_CONFIRMED`
    - 合计 `6` 条
  - 当前剩余：
    - `54` 条 `WAIT_MANUAL_PATH`
- 当前执行口径进一步收紧为：
  - 先吃“系列号闭环明确”的子簇
  - 再吃“主题簇明确但仍需二次确认”的条目
  - 不回头按标题盲 move 外部文件

## 第二轮后续对账：GROUP_08 第三批精确路径补齐 + 第三批 staging copy

- 已新增：
  - `tools\group08_batch3_topic_copy.py`
- 本轮真实执行结果：
  - 已新增 `S-003 -> SHARED_SERIES_SOURCE_CONFIRMED`
  - 已新增 `S-010 -> TOPIC_MANUAL_CONFIRMED`
  - `00_external_import_staging\confirmed_topic\04_多因子\` 已新增 `1` 份外部原件副本
  - 当前累计已完成路径确认：
    - `8` 条
  - 当前真实 staging 副本累计：
    - `7` 份
  - 当前剩余：
    - `52` 条 `WAIT_MANUAL_PATH`
- 当前执行口径进一步收紧为：
  - 先吃“系列号闭环明确”的子簇
  - 再吃“共享已确认外部真值源”的条目
  - 再吃“主题簇明确但仍需单条人工确认”的条目

## 第二轮后续对账：GROUP_08 第四批主题锚点补齐（放宽但不污染删源台账）

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_主题锚点勾验_v1.tsv`
  - `tools\group08_batch4_topic_anchor.py`
- 本轮真实执行结果：
  - 用户已允许第四批先放宽到“主题锚点”
  - 已登记 `S-005 -> METHOD_THEME_ANCHOR -> 海通选股因子系列研究6`
  - 已登记 `S-012 -> UPSTREAM_CITATION_ANCHOR -> 海通选股因子系列研究1`
  - 这 `2` 条当前只记为 `TOPIC_ANCHOR_ONLY`
  - 只复用既有 staging 副本路径，不新增真实复制
  - 删除级别统计当前保持不变：
    - `8` 条已完成路径确认
    - `7` 份真实 staging 副本
    - `52` 条 `WAIT_MANUAL_PATH`
- 当前执行口径进一步固定为：
  - 允许把“主题框架明确 / 已确认上游研究引用”的条目先收成辅助锚点
  - 但辅助锚点不能替代真实外部原件路径
  - 后续仍要继续收紧回删除级别精确路径

## 第二轮后续对账：GROUP_08 第四批主题锚点收紧复核

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_第四批主题锚点收紧核查_v1.md`
- 本轮真实执行结果：
  - `S-005` 经复核后仍只能保持 `METHOD_THEME_ANCHOR`
  - `S-012` 经复核后仍只能保持 `UPSTREAM_CITATION_ANCHOR`
  - 补查外部树后，没有出现更贴题的 `短线反弹` / `超跌反弹` / `换手率上的实证` 原件名
  - 因此这两条都不能升级为删除级别精确路径
  - 删除级别统计继续保持：
    - `8` 条已完成路径确认
    - `7` 份真实 staging 副本
    - `52` 条 `WAIT_MANUAL_PATH`
- 当前执行口径继续固定为：
  - `TOPIC_ANCHOR_ONLY` 允许收窄候选
  - 但收紧失败后必须显式保留负结论
  - 不能因为“主题很像”就写进删除级别路径台账

## 第二轮后续对账：GROUP_08 第五批极值簇 / 反转簇候选扫描

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_第五批极值反转候选扫描_v1.md`
- 本轮真实执行结果：
  - 反转簇中 `选股因子_动量反转效应__v2.md` 复核后确认只是已落盘的 `S-037`
  - `S-012 / S-014` 没有补出新的外部原件
  - 极值簇当前真正仍待补的核心对象只剩 `S-027`
  - 当前 `03_券商研报` 真值树内，这一小簇没有新增删除级别精确路径
  - 删除级别统计继续保持：
    - `8` 条已完成路径确认
    - `7` 份真实 staging 副本
    - `52` 条 `WAIT_MANUAL_PATH`
- 当前执行口径进一步固定为：
  - 对小簇复扫时，要先剔除“其实已经被旧批次确认掉的对象”
  - 没有同题外部原件时，不能为了推进而重复写锚点

## 第二轮后续对账：GROUP_08 第六批遗漏目录与旧原题反查

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_第六批遗漏目录与旧原题反查_v1.md`
- 本轮真实执行结果：
  - `S-027` 仓库内原题与 `Cfmv` 公式锚点更硬，但在 `D:\Stock\cut_file\S` 全目录内仍未找到同题原件
  - `S-014` 没有补出更完整旧原题，且其相邻“行业内识别度”系列在当前 `S` 真值树里也整体缺席
  - `D:\Stock\cut_file\S\券商研报` 旧重复目录只补出了重复件线索，没有补出 `S-027 / S-014` 的新原件
  - 当前没有新增删除级别精确路径
  - 删除级别统计继续保持：
    - `8` 条已完成路径确认
    - `7` 份真实 staging 副本
    - `52` 条 `WAIT_MANUAL_PATH`
- 当前执行口径进一步固定为：
  - 当单条对象在当前 `S` 真值树中多轮反查仍无果时，要优先判断“源本身不在当前树里”
  - 不能继续在主题近邻文件之间做低置信硬挂接

## 第二轮后续对账：GROUP_08 第七批树外目录与旧来源层反查

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_第七批树外目录与旧来源层反查_v1.md`
- 本轮真实执行结果：
  - `S-027` 在 `D:\Stock` 全盘范围内仍未找到树外同名或近名原件
  - `S-014` 在旧来源目录层没有补出真实文件实体，只剩摘要与残留 `origin_path` 文字锚点
  - 文档多次引用的 `GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书` 当前并不在磁盘上
  - 当前没有新增删除级别精确路径
  - 删除级别统计继续保持：
    - `8` 条已完成路径确认
    - `7` 份真实 staging 副本
    - `52` 条 `WAIT_MANUAL_PATH`
- 当前执行口径进一步固定为：
  - 若旧来源层真值目录实体已缺失，则该对象不能再依赖“回原文件名核对”推进
  - 后续若还要追这批对象，应优先找历史备份或已删前快照

## 第二轮后续对账：GROUP_08 SOURCE_RAW 回找清单与缺失 manifest

- 已新增：
  - `GROUP_08_A股量化_数据研究\GROUP_08_SOURCE_RAW_可回找书名与包名清单_v1.md`
  - `GROUP_08_A股量化_数据研究\GROUP_08_SOURCE_RAW_回找执行记录_v1.md`
  - `GROUP_08_A股量化_数据研究\GROUP_08_SOURCE_RAW_missing_manifest_v1.tsv`
  - `GROUP_08_A股量化_数据研究\GROUP_08_SOURCE_RAW_需要你找回的源头书本_v1.md`
  - `tools\group08_sourceraw_missing_manifest.py`
- 本轮真实执行结果（基于 `txt_md_index_v1.tsv`）：
  - `rows_total=99`
  - `src_existing=0`
  - `src_missing=99`
- 当前执行口径进一步固定为：
  - `txt_md_index_v1.tsv` 只能证明“曾经存在过哪些 src_path”，不能证明“磁盘现在还在”
  - 回源优先靠书名/包名找回 `SOURCE_RAW` 历史副本，再用缺失 manifest 复核回源是否成功

## 第二轮后续对账：GROUP_08 SOURCE_RAW 已恢复接回

- 本轮真实执行结果：
  - 用户已找回 `D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版`
  - 已复制回项目 `GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书\`
  - 已复跑 `tools\group08_sourceraw_missing_manifest.py`
  - 当前结果：
    - `rows_total=99`
    - `src_existing=99`
    - `src_missing=0`
- 当前新增硬结论：
  - `txt_md_index_v1.tsv` 对应的 `99` 条 `src_path` 已全部恢复
  - `research pdf` 的原始承载父目录已确认是：
    - `2.其他量化资料(62份)（赠品）`
  - `S-014 / S-027 / S-012 / S-005` 的关键原始 PDF 已能在项目内直接定位
- 当前执行口径进一步固定为：
  - 这本核心源头书已不再属于“待你找回”
  - 后续重心改为：
    - 基于恢复后的原始 PDF，继续补逐条审计
    - 继续推进删除级别对象重核
