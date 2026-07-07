# NFTRADEZ Agent Status 2026-06-23

## 当前定位

- 本文件定位：交接入口；用于统一 lane 状态、回收结果与合并规则
- 交接短名：`Agent Status`
- 本层只收：`交接 / 回收状态 / 合并规则`
- 固定顺序：`交接总览 -> Agent A -> Agent B -> Merge Rule`

## 交接总览

- 当前 truth 目录:
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\02_外部视频与方法论参考\Norman_NFTRADEZ_ICT_Trader_NYC`
- 外部 source 目录:
  - `D:\Stock\cut_file\诺曼NFTRADEZ`
- 外部目录角色:
  - `仅作为历史来源追溯位，不作为默认入口`

## Agent A

- 包级角色：术语真值收缩包；用于统一概念定义与回帖收缩结果
- 当前 lane：`concept_glossary`
- 当前状态：`DONE_AND_IMPORTED`
- repo 默认入口:
  - `NFTRADEZ_KIMI_batch_README_v1.md`
- repo 真值文件:
  - `NFTRADEZ_KIMI_concept_glossary_manifest_v1.tsv`
  - `NFTRADEZ_KIMI_concept_glossary_prompt_v1.txt`
  - `NFTRADEZ_KIMI_concept_glossary_direct_message_v2__agentA.txt`
- repo 回帖副本:
  - `NFTRADEZ_KIMI_concept_glossary_shrink_v1__imported.md`
- 外部 PDF 读取目录:
  - `D:\Stock\cut_file\诺曼NFTRADEZ`
- 外部目录角色:
  - `仅作为历史来源追溯位，不作为默认入口`
- 当前边界:
  - 以 `method_reference` 导入
  - 保留 glossary / explanation / bias-support 角色
  - 不升级为 validated quant objects（已验证量化对象）

## Agent B

- 包级角色：盘前模板收缩包；用于统一模板要素与回帖收缩结果
- 当前 lane：`premarket_template`
- 当前状态：`DONE_AND_IMPORTED`
- repo 默认入口:
  - `NFTRADEZ_KIMI_batch_README_v1.md`
- repo 真值文件:
  - `NFTRADEZ_KIMI_premarket_template_manifest_v1.tsv`
  - `NFTRADEZ_KIMI_premarket_template_prompt_v1.txt`
  - `NFTRADEZ_KIMI_premarket_template_direct_message_v2__agentB.txt`
- repo 回帖副本:
  - `NFTRADEZ_KIMI_premarket_template_v1__imported.md`
- 外部 PDF 读取目录:
  - `D:\Stock\cut_file\诺曼NFTRADEZ`
- 外部目录角色:
  - `仅作为历史来源追溯位，不作为默认入口`
- 当前批次合同:
  - 仅收 `NFTZ_P001`
  - 仅收 `NFTZ_P002`
  - 仅收 `NFTZ_P003`
  - 仅收 `NFTZ_P004`
- copy-paste 交接包:
  - `NFTRADEZ_KIMI_premarket_template_OUTBOUND__agentB__copy_paste_v1.txt`
- 必需输出字段:
  - `bias_check`
  - `dol_check`
  - `timeframe_alignment`
  - `if_then_branches`
  - `do_not_trade_when`
  - `event_day_exception`
- 当前边界:
  - 不输出 concrete trade calls（具体交易指令）
  - 不把 video narratives 升级成 universal rules（通用规则）
  - 不把 `FOMC` template 泛化到 normal trading days（普通交易日）
  - narrative-only 项标记为 `narrative_only`

## 合并规则

- `Agent B` reply 已并回 repo truth layer。
- 当前合并目标:
  - `NFTRADEZ_KIMI_concept_glossary_shrink_v1__imported.md`
  - `NFTRADEZ_KIMI_premarket_template_v1__imported.md`
- `README.md` 与 `NFTRADEZ_KIMI_batch_README_v1.md` 已同步更新导入结果。

## 当前操作短句

- 若有人问“`NFTRADEZ` 现在具体在哪”，先回这份文件。
- 若有人问“`Agent B` 回来了什么”，直接回：
  - `NFTRADEZ_KIMI_premarket_template_v1__imported.md`
  - 外部 save file 当前只作为 `D:\Stock\cut_file\诺曼NFTRADEZ` 下的 trace path（追溯路径），不作为默认入口

## 补充入口镜像

- 本层只收：`总览 / 证据 / 交接`
- 固定顺序：`总览 -> 证据 -> 交接`
- 总览入口：`README总览`
- 证据入口：`吸收与分流`
- 交接入口：`Agent Status`
