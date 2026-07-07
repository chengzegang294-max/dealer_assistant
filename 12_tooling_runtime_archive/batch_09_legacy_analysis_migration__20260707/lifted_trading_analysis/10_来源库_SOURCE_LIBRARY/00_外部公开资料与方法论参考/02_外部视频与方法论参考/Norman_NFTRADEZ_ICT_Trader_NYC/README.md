# Norman NFTRADEZ ICT Trader NYC

## 当前定位

- 这是外部视频导出型方法论资料，不是已验证量化策略库。
- 当前更适合作为：
  - 价格行为 / ICT 概念词典来源
  - 盘前偏见与事件日剧本参考
  - 执行分级与交易纪律参考
- 当前不应直接当成：
  - 已验证 alpha
  - 可直接上线的执行系统
  - 已完成字段化的量化对象

## 当前产物

- 原始导出副本：本目录下 `26` 个 `*_导出.md`
- 目录清单：`Norman_NFTRADEZ_manifest_v1.tsv`
- 吸收结论：`Norman_NFTRADEZ_吸收与分流_v1.md`
- `Kimi` 默认批次入口：`NFTRADEZ_KIMI_batch_README_v1.md`
- `Kimi` 概念词典回帖导入：`NFTRADEZ_KIMI_concept_glossary_shrink_v1__imported.md`
- `Kimi` 盘前模板回帖导入：`NFTRADEZ_KIMI_premarket_template_v1__imported.md`

## 当前分流

- `INGEST_AS_METHOD_REFERENCE`
  - 适合后续抽成：
    - 术语词典
    - 盘前偏见模板
    - 事件日剧本模板
    - 执行分级框架
    - 纪律与停手机制
- `REFERENCE_ONLY`
  - 先保留为案例回放或辅助理解材料
  - 不直接进入量化对象层

## 当前边界

- repo 内目录是当前默认 truth 入口：
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\02_外部视频与方法论参考\Norman_NFTRADEZ_ICT_Trader_NYC`
- 外部目录 `D:\Stock\cut_file\诺曼NFTRADEZ` 当前只保留为历史来源追溯位，不作为默认入口
- 若后续需要回看项目外保存位置，只用于来源追溯；默认使用、抽读、引用都应优先指向 repo 内副本
- 若后续继续吸收，优先抽：
  - `Daily Bias / 开盘前剧本`
  - `OB / FVG / Liquidity / SMT`
  - `FOMC 三段式`
  - `交易评级体系`
  - `情绪失控与停手规则`
- 当前最新状态：
  - `Agent A` 的 `concept_glossary` 已回帖并导入 repo
  - `Agent B` 的 `premarket_template` 已回帖并导入 repo
  - 明确交接说明见：`NFTRADEZ_AGENT_STATUS__2026-06-23.md`

## 当前合同层

- 本层只收：`当前生效入口 / 包级角色 / 固定顺序 / 扩展附注`
- 当前合同层固定顺序：`concept_glossary -> premarket_template`
- `concept_glossary` 包级角色：术语真值收缩包；用于统一概念定义与回帖收缩结果
- `concept_glossary` 包级目标：把 `ICT` 的基础概念收成最小词典条目
- `concept_glossary` 包级真值组成：`manifest_tsv + prompt_txt + direct_message_txt + batch_readme_md + imported_reply_md`
- `premarket_template` 包级角色：盘前模板收缩包；用于统一模板要素与回帖收缩结果
- `premarket_template` 包级目标：把盘前偏见 / DOL / If-Then / 事件日边界收成模板骨架
- `premarket_template` 包级真值组成：`manifest_tsv + prompt_txt + direct_message_txt + batch_readme_md + imported_reply_md`

## 补充入口

- 本层只收：`总览 / 证据 / 交接`
- 固定顺序：`总览 -> 证据 -> 交接`
- 总览短名：`README总览`
- 总览入口：`README总览`
- 证据入口：`吸收与分流`
- 交接入口：`Agent Status`
