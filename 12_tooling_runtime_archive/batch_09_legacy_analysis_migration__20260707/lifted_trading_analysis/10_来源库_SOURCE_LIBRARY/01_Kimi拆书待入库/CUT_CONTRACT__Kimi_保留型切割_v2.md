# CUT_CONTRACT__Kimi_保留型切割_v2

目标：把一本书/一份资料切成“删掉原文后仍可用”的 md 资产，且尽量可量化映射。

适用：pdf / epub / 长文档。对超大文件先拆分或转格式后再执行本合同。

## 硬规则

1) 产物必须包含“原文保留块”，不能只做目录索引或纯摘要。
2) 不允许把“概念”直接写成“已可量化信号”。必须区分：
   - `proxy_quantizable_now`
   - `needs_extra_data`
   - `shell_only`
   - `future_bucket`
3) 依赖 `Level2 / orderbook / DOM / 逐笔成交 / 席位 / 付费终端` 的内容，默认标注 `needs_extra_data` 或 `future_bucket`。
4) 输出为 Markdown；不输出长论文；每段结论都要能落到可执行下一步。

## 输出合同（必须严格按此结构输出）

### MATERIAL_CARD
- title:
- author_or_source:
- material_type: 书 / 研报 / 课程讲义 / 帖子集 / 其他
- domain_tags:
- file_scope: 本次切割覆盖的文件范围（例如：全书 / 第1-3章 / 本分册）

### ROUTING_DECISION
- current_repo_role: 只能从下面选：
  - DATA_ENGINEERING_GUARD
  - STATE_TEMPLATE_SHELL
  - OBJECT_DEFINITION_SHELL
  - SOURCE_LIBRARY_ONLY
  - A_SHARES_FUTURE_BUCKET
  - ORDERFLOW_FUTURE_BUCKET
- is_worth_deep_cut_now: yes/no
- deep_cut_priority: P0/P1/P2
- reason:

### CONTENT_CLUSTERS
切成 3-10 个主题簇。每簇写：
- cluster_name:
- what_it_is:
- keep_level: 高/中/低
- repo_mapping: 对象层/状态层/护栏层/future bucket/索引层

### QUANTIZATION_TABLE
Markdown 表格，至少 12 行。表头必须是：
`concept | type | minimal_definition | observable_proxy | min_data_requirement | confirmation_timing | quant_status | repo_target | leakage_risk | notes`

约束：
- type: `state/object/feature/label/filter/risk_guard/execution_rule`
- min_data_requirement: `OHLCV/session_calendar/cross_section/PIT_fundamental/tick_trade/level2_orderbook/news_event/subjective_only`
- quant_status: `proxy_quantizable_now/needs_extra_data/shell_only/future_bucket/index_only`
- repo_target: `data_engineering_guard/state_template_shell/object_definition_shell/source_library_only/A_shares_only_future_bucket/orderflow_future_bucket`
- leakage_risk: `low/med/high`

### RETAINED_EXCERPTS
这部分是“删源后还能用”的关键。

要求：
- 12–25 条“原文保留卡片”
- 每条包含：
  - excerpt_id: EX-01...
  - source_hint: 章节/主题（无法确认页码可不写页码）
  - quote: 直接保留原文片段（建议 200–800 字之间；过长分拆为多条）
  - why_kept: 这一段为什么必须保留（定义/边界条件/公式/陷阱/反例）
  - quant_link: 链接到 QUANTIZATION_TABLE 中的 concept（写 concept 名称）

### FORMULAS_AND_ALGOS
如果书中有公式/算法/步骤，必须抽出：
- 公式（用 Markdown 公式或代码块表示）
- 变量定义表
- 适用条件与失效条件

### NOT_QUANT_YET
列出 3–10 条“现在不该强行量化”的点，并给原因。

### NEXT_ACTION
3–8 条动作，必须可执行，例如：
- 继续切哪一章/哪一簇
- 需要补哪类数据（PIT、交易规则、L2、逐笔等）
- 要生成哪个对象/状态壳的草案

## 输出格式要求

- 全中文
- 多表格
- 短句
- 不写“这本书很好”
- 不写泛泛背景
