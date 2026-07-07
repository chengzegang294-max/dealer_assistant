# GROUP_08 外部执行 Runbook v1

本 runbook 只覆盖 `GROUP_08` 的外部文件“移动/删除候选”执行链路，默认不触发真实删除；所有动作必须以台账与清单为准。

## 输入与真值

- 可直接使用的材料目录（staging 入口）：
  - `GROUP_08_materials_catalog_v1.md`
  - `GROUP_08_materials_catalog_v1.tsv`
- 条目级最终删除勾选清单：
  - `GROUP_08_research_pdf_最终删除勾选_逐条清单_v1.tsv`
- 外部执行总计划（带引用扫描摘要）：
  - `GROUP_08_external_ops_plan_v1.tsv`
- 外部移动计划（不删）：
  - `GROUP_08_external_move_plan_v1.tsv`
- 外部删除候选计划（候选，默认不执行）：
  - `GROUP_08_external_delete_candidate_plan_v1.tsv`
- 执行前引用扫描入口（看 `outside_group08_count`）：
  - `GROUP_08_repo_refscan_summary_v1.tsv`
- 删除候选“清引用清单”（进入真删除窗口前清理）：
  - `GROUP_08_delete_candidates_ref_cleanup_list_v1.md`
  - `GROUP_08_delete_candidates_ref_cleanup_list_v1.tsv`

## 预检（强制）

1. 生成预检表（会计算 sha256，对齐 source 与 staging 是否一致）：
   - 运行：`python tools/group08_external_ops_preflight.py`
   - 输出：`GROUP_08_external_ops_preflight_v1.tsv`
2. 预检通过条件（建议）：
   - `source_exists=1`
   - `staging_exists=1`
   - `sha256_match=1`
3. 对删除候选额外门槛：
   - `outside_refs_basename=0` 且 `outside_refs_fullpath=0` 才允许进入真执行窗口
4. 删除候选在进入真删除前，必须完成：
  - 清引用清单中 `fix_action=REPLACE_WITH_STAGING` 的条目清零

## Dry-run（默认只打印）

- 外部移动 dry-run：
  - `GROUP_08_external_move_plan_dryrun_v1.ps1`
- 外部删除候选 dry-run：
  - `GROUP_08_external_delete_candidate_dryrun_v1.ps1`

这两份脚本默认只做 `-WhatIf` 预演。

## 真执行（需要显式开关）

- 外部移动真执行：
  - `.\GROUP_08_external_move_plan_dryrun_v1.ps1 -Execute`
- 外部删除候选真执行：
  - `.\GROUP_08_external_delete_candidate_dryrun_v1.ps1 -Execute`

## 执行后复核

- 外部移动执行后复核（确认 src 消失、dest 存在）：
  - 运行：`python tools/group08_external_move_postcheck.py`
  - 输出：
    - `GROUP_08_external_move_postcheck_v1.tsv`
    - `GROUP_08_external_move_postcheck_v1.md`

## 重要边界

- `MOVE_READY_NOT_DELETE`：表示“可以整理移动，但不删源”；优先保证 staging 副本与 sha256 对齐。
- `DELETE_EXTERNAL_SUBSET_CANDIDATE`：仅表示“候选”；除非你明确进入删除窗口，否则保持 dry-run。
- 外部目标目录默认规划为：
  - `D:\Stock\cut_file\__GROUP_08_sorted\...`
  - 若要改目标根目录，先改 `tools/group08_split_external_ops_plan.py` 的 `DEFAULT_MOVE_DEST_ROOT` 并重新生成计划与 dry-run 脚本。
