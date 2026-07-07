# NFTRADEZ KIMI Batch README v1

## 当前批次

- 本层只收：`包级角色 / 主合同字段 / 扩展附注`
- 固定阅读顺序：`包级角色 -> repo 默认入口 -> repo 真值文件 -> repo 回帖副本 -> 外部目录 -> 附注（若有）`
- 包级固定顺序：`concept_glossary -> premarket_template`

- `concept_glossary`
  - 包级角色：术语真值收缩包；用于统一概念定义与回帖收缩结果
  - repo 默认入口：`NFTRADEZ_KIMI_batch_README_v1.md`
  - repo 真值文件：`NFTRADEZ_KIMI_concept_glossary_manifest_v1.tsv`、`NFTRADEZ_KIMI_concept_glossary_prompt_v1.txt`、`NFTRADEZ_KIMI_concept_glossary_direct_message_v2__agentA.txt`
  - repo 回帖副本：`NFTRADEZ_KIMI_concept_glossary_shrink_v1__imported.md`
  - 外部 PDF 读取目录：`D:\Stock\cut_file\诺曼NFTRADEZ`
  - 外部目录角色：仅作为历史来源追溯位，不作为默认入口
  - 包级目标：把 `ICT` 的基础概念收成最小词典条目
  - 包级真值组成：`manifest_tsv + prompt_txt + direct_message_txt + batch_readme_md + imported_reply_md`
  - 包级回收结果：`imported_reply_in_repo`
  - 包级回收入口：`NFTRADEZ_KIMI_concept_glossary_shrink_v1__imported.md`
  - 包级回收来源：`Kimi Agent A` 回帖导入
  - 扩展字段附注：`goal=min_concept_glossary；result=imported_reply_in_repo；boundary=concept_only_not_entry_signal`
- `premarket_template`
  - 包级角色：盘前模板收缩包；用于统一模板要素与回帖收缩结果
  - repo 默认入口：`NFTRADEZ_KIMI_batch_README_v1.md`
  - repo 真值文件：`NFTRADEZ_KIMI_premarket_template_manifest_v1.tsv`、`NFTRADEZ_KIMI_premarket_template_prompt_v1.txt`、`NFTRADEZ_KIMI_premarket_template_direct_message_v2__agentB.txt`
  - repo 回帖副本：`NFTRADEZ_KIMI_premarket_template_v1__imported.md`
  - 外部 PDF 读取目录：`D:\Stock\cut_file\诺曼NFTRADEZ`
  - 外部目录角色：仅作为历史来源追溯位，不作为默认入口
  - 包级目标：把盘前偏见 / DOL / If-Then / 事件日边界收成模板骨架
  - 包级真值组成：`manifest_tsv + prompt_txt + direct_message_txt + batch_readme_md + imported_reply_md`
  - 包级回收结果：`imported_reply_in_repo`
  - 包级回收入口：`NFTRADEZ_KIMI_premarket_template_v1__imported.md`
  - 包级回收来源：`Kimi Agent B` 回帖导入
  - 扩展字段附注：`goal=premarket_template_shell；result=imported_reply_in_repo；boundary=bias_template_not_strategy_validation`

## 当前边界

- 本节定位：边界入口；用于锁定方法论层边界与禁止误写口径
- 这两批都属于 `method_reference`，不是策略验证。
- 不允许把视频里的胜率、个别案例收益、主观叙事写成“已验证结论”。
- 不允许把 `FOMC` 模板泛化到所有交易日。
- 不允许把 `SMT / FVG / OB` 直接写成入场信号。

## 推荐使用方式

- 本节定位：发包入口；用于固定单 agent / 双 agent 的发送顺序
- 单 agent 串行模式：
  - 先发 `concept_glossary`
  - 回帖收口后，再发 `premarket_template`
  - 两轮之间不要换目录，也不要让 `Kimi` 自己扩展到其他不在 manifest 里的文件
- 双 agent 并行模式：
  - Agent A 只发 `NFTRADEZ_KIMI_concept_glossary_direct_message_v2__agentA.txt`
  - Agent B 只发 `NFTRADEZ_KIMI_premarket_template_direct_message_v2__agentB.txt`
  - 两个 agent 不要互相读取对方任务
  - 一旦启用双 agent，就不要再混发 `v1` 单 agent 口径

## 当前最顺动作

- 本节定位：执行入口；用于给出当前默认下一跳
- 直接发送：
  - `NFTRADEZ_KIMI_concept_glossary_direct_message_v1.txt`
  - 回帖后再发送 `NFTRADEZ_KIMI_premarket_template_direct_message_v1.txt`
- 若已启用双 agent：
  - 直接发送 `NFTRADEZ_KIMI_concept_glossary_direct_message_v2__agentA.txt`
  - 直接发送 `NFTRADEZ_KIMI_premarket_template_direct_message_v2__agentB.txt`
  - 不要再回切到 `v1` 单 agent 消息
- 所有入口合同固定按以下字段顺序阅读：
  - `repo 默认入口`
  - `repo 真值文件`
  - `repo 回帖副本`
  - `外部 PDF 读取目录`
  - `外部目录角色`

## 补充入口

- 本层只收：`总览 / 证据 / 交接`
- 固定顺序：`总览 -> 证据 -> 交接`
- 总览入口：`README总览`
- 证据入口：`吸收与分流`
- 交接入口：`Agent Status`

## 当前回收状态

- 本节定位：回收入口；用于记录回帖导入状态与当前结论
- `Agent A / concept_glossary`
  - 已回帖
  - repo 导入文件：`NFTRADEZ_KIMI_concept_glossary_shrink_v1__imported.md`
  - 当前结论：`6` 个对象全部保留为解释层 / 偏见辅助层，不直接入场
- `Agent B / premarket_template`
  - 已回帖
  - repo 导入文件：`NFTRADEZ_KIMI_premarket_template_v1__imported.md`
  - 当前结论：保留为盘前模板 / 事件日例外 / 纪律辅助层，不直接入场
- 当前精确交接文件：
  - `NFTRADEZ_AGENT_STATUS__2026-06-23.md`
