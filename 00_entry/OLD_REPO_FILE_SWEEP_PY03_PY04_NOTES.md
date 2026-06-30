# Old Repo File Sweep PY03 PY04 Notes

## 目的

- 这份备注只记录本轮对 `PY-03` 和 `PY-04` 的代表脚本扫描结论。
- 目标不是迁文件，而是先把“谁是什么、该怎么处理”说清楚。

## 扫描范围

### PY-03 通用维护与整理脚本

- `tools\s_bucketize.py`
- `tools\ingest_ashare_txt_to_md.py`
- `tools\kimi_cutpack_manifest.py`
- `tools\group08_generate_delete_refs_cleanup.py`
- `tools\group08_split_external_ops_plan.py`
- `tools\group08_refscan_final_delete_list.py`
- `tools\group08_sync_final_delete_list.py`
- `tools\group08_batch5_bookdir_autoresolve.py`

### PY-04 TK-R1 ~ TK-R8 家族

- `tools\tk_r2_tradelevel_audit.py`
- `tools\tk_r3_rr_minwin_audit.py`
- `tools\tk_r4_risk_corr_audit.py`
- `tools\tk_r6_make_manual_sheet.py`
- `tools\tk_r7_make_manual_sheet.py`
- `tools\tk_r8_make_manual_sheet.py`
- 外加目录级快扫：
  - `tools\tk_r1_*`
  - `tools\tk_r2_*`
  - `tools\tk_r3_*`
  - `tools\tk_r4_*`
  - `tools\tk_r6_*`
  - `tools\tk_r7_*`
  - `tools\tk_r8_*`

## PY-03 当前结论

### A. 可复用整理工具

- `s_bucketize.py`
  - 作用：对 `S桶 / 研报 / 待归类` 材料做一级归类、信息密度判断、下一步动作判断
  - 输入：目录、inventory 行
  - 输出：staging 子集与分桶结果
  - 当前处理动作：`COPY_WITH_NOTE`
  - 当前判断：属于“通用整理能力”，不只是一次性脚本

- `ingest_ashare_txt_to_md.py`
  - 作用：把 A 股策略 `.txt` 样本按编码识别、按主题聚类、转成带元信息的 `.md`
  - 输入：`src_dir`
  - 输出：`out_dir` + `txt_md_index`
  - 当前处理动作：`COPY_WITH_NOTE`
  - 当前判断：是明显可复用的“外部文本入库工具”

- `kimi_cutpack_manifest.py`
  - 作用：遍历 `CUTPACK__*.md`，抽取 bucket / version / retain_mode / current_repo_role / quant_rows
  - 输入：`--root`
  - 输出：`--out` manifest tsv
  - 当前处理动作：`COPY_WITH_NOTE`
  - 当前判断：属于“清点现有 cutpack 资产”的元数据工具

### B. GROUP_08 专用批处理脚本

- `group08_split_external_ops_plan.py`
  - 作用：把外部操作计划拆成 `move` 与 `delete candidate`
  - 当前处理动作：`MOVE_LATER_AFTER_REF_CHECK`
  - 当前判断：强绑定 `GROUP_08` 路径结构和外部书目录

- `group08_generate_delete_refs_cleanup.py`
  - 作用：基于删除候选计划，扫描 repo 内引用并生成清理清单
  - 当前处理动作：`MOVE_LATER_AFTER_REF_CHECK`
  - 当前判断：强绑定 `GROUP_08`，但仍有长期参考价值

- `group08_refscan_final_delete_list.py`
  - 作用：对最终删除勾选清单做 repo 引用扫描
  - 当前处理动作：`KEEP_OLD_FROZEN`
  - 当前判断：更像“删除窗口前的最后一次审计脚本”

- `group08_sync_final_delete_list.py`
  - 作用：把路径台账同步回最终删除清单
  - 当前处理动作：`KEEP_OLD_FROZEN`
  - 当前判断：是批次专用同步脚本，不是通用工具

- `group08_batch5_bookdir_autoresolve.py`
  - 作用：从外部书目录自动匹配 PDF，复制到 repo staging，并回写 audit/ledger
  - 当前处理动作：`MOVE_LATER_AFTER_REF_CHECK`
  - 当前判断：路径依赖极强，但方法有价值

### PY-03 小结

- 当前可以优先考虑迁入新仓库的，不是全部 `group08_*`，而是三类：
  - `s_bucketize.py`
  - `ingest_ashare_txt_to_md.py`
  - `kimi_cutpack_manifest.py`
- `group08_*` 当前应继续分成：
  - 已在新仓库维护的主流水线
  - 仅旧批次专用的删除/台账/自动解析脚本

## PY-04 当前结论

### A. trade-level / stage2 审计家族

- `tk_r2_tradelevel_audit.py`
  - 作用：对 `trade_level_csv` 做 stage split、profile x symbol 稳定性审计
  - 输入：`backtest_out/stage2/indicator_audit/.../b115_trade_level...csv`
  - 输出：多份审计 csv
  - 当前处理动作：`KEEP_OLD_FROZEN`
  - 当前判断：强绑定旧 `backtest_out` 产物与 `TK-R2` 语义

- `tk_r3_rr_minwin_audit.py`
  - 作用：对 baseline trades 做 `R multiple / breakeven win rate` 审计
  - 输入：`backtest_out/p0_sweep`
  - 输出：`b116_*`
  - 当前处理动作：`KEEP_OLD_FROZEN`
  - 当前判断：是特定回测批的二次审计脚本

- `tk_r4_risk_corr_audit.py`
  - 作用：做固定风险与跨品种相关性重叠审计
  - 输入：`backtest_out/p0_sweep`
  - 输出：`b118_*`
  - 当前处理动作：`KEEP_OLD_FROZEN`
  - 当前判断：强依赖旧 `P0 sweep` 与 `backtest_p0`

### B. 手工审计表家族

- `tk_r6_make_manual_sheet.py`
  - 作用：生成 `R6` 手工审计表模板
  - 输出：`tkr6_manual_audit_sheet_v1.tsv`
  - 当前处理动作：`MOVE_LATER_AFTER_REF_CHECK`
  - 当前判断：脚本本身很轻，但依附于 `TK-R6` 旧审计流程

- `tk_r7_make_manual_sheet.py`
  - 作用：生成 `R7` AO 背离手工审计表模板
  - 当前处理动作：`MOVE_LATER_AFTER_REF_CHECK`
  - 当前判断：可复用性比 `trade-level audit` 高，但仍需要补用途说明

- `tk_r8_make_manual_sheet.py`
  - 作用：生成 `R8` B 区域手工审计表模板
  - 当前处理动作：`MOVE_LATER_AFTER_REF_CHECK`
  - 当前判断：同上

### C. 目录级快扫结论

- `tk_r1_* ~ tk_r4_*`
  - 绝大多数都依赖：
    - `backtest_out/p0_sweep`
    - `backtest_out/stage2/indicator_audit`
    - `backtest_p0`
  - 当前处理动作：`KEEP_OLD_FROZEN`

- `tk_r6_* / tk_r7_* / tk_r8_*`
  - 以“生成手工表 + 汇总手工表”为主
  - 当前处理动作：`MOVE_LATER_AFTER_REF_CHECK`
  - 当前判断：如果未来真的重开 `TK-R6 / R7 / R8`，这组比 `R1-R4` 更值得先迁

### PY-04 小结

- 当前不建议直接把 `TK-R1 ~ TK-R4` 审计家族整体搬进新仓库
- 当前更适合优先保留候选的是：
  - `tk_r6_make_manual_sheet.py`
  - `tk_r6_summarize_manual_sheet.py`
  - `tk_r7_make_manual_sheet.py`
  - `tk_r7_summarize_manual_sheet.py`
  - `tk_r8_make_manual_sheet.py`
  - `tk_r8_summarize_manual_sheet.py`
- 当前已正式把 `R6` 首批迁入新仓库：
  - `20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\tk_r6_make_manual_sheet.py`
  - `20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\tk_r6_summarize_manual_sheet.py`
  - 同批备注：`20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\BATCH_04_TOOL_NOTES.md`
- 当前已正式把 `R7` 首批迁入新仓库：
  - `20_tools_workspace\batch_05_tk_r7_manual_sheet_tools\tk_r7_make_manual_sheet.py`
  - `20_tools_workspace\batch_05_tk_r7_manual_sheet_tools\tk_r7_summarize_manual_sheet.py`
  - 同批备注：`20_tools_workspace\batch_05_tk_r7_manual_sheet_tools\BATCH_05_TOOL_NOTES.md`
- 当前已正式把 `R8` 首批迁入新仓库：
  - `20_tools_workspace\batch_06_tk_r8_manual_sheet_tools\tk_r8_make_manual_sheet.py`
  - `20_tools_workspace\batch_06_tk_r8_manual_sheet_tools\tk_r8_summarize_manual_sheet.py`
  - 同批备注：`20_tools_workspace\batch_06_tk_r8_manual_sheet_tools\BATCH_06_TOOL_NOTES.md`
- 当前裁决进一步收紧为：
  - `R6`：已从候选进入首批正式迁入
  - `R7`：已从候选进入首批正式迁入
  - `R8`：已从候选进入首批正式迁入

## 当前迁移裁决

### 本轮建议进入新仓库候选清单

- `tools\s_bucketize.py`
- `tools\ingest_ashare_txt_to_md.py`
- `tools\kimi_cutpack_manifest.py`
- `tools\tk_r6_make_manual_sheet.py`
- `tools\tk_r6_summarize_manual_sheet.py`
- `tools\tk_r7_make_manual_sheet.py`
- `tools\tk_r7_summarize_manual_sheet.py`
- `tools\tk_r8_make_manual_sheet.py`
- `tools\tk_r8_summarize_manual_sheet.py`

### 本轮建议继续留旧仓库冻结

- `group08_generate_delete_refs_cleanup.py`
- `group08_split_external_ops_plan.py`
- `group08_refscan_final_delete_list.py`
- `group08_sync_final_delete_list.py`
- `group08_batch5_bookdir_autoresolve.py`
- `tk_r1_*`
- `tk_r2_*`
- `tk_r3_*`
- `tk_r4_*`

## 下一步

1. 先给“建议进入新仓库候选清单”补最小作用卡
2. 再决定它们分别进入：
  - `20_tools_workspace`
  - 还是 `12_tooling_runtime_archive`
3. `group08 删除/台账` 与 `TK-R1~R4 审计家族` 当前不做整组迁移

## 一句话记忆

- `PY-03` 先迁通用整理工具，不迁整组 `group08 删除脚本`；`PY-04` 先保留 `R6~R8` 手工表候选，不迁 `R1~R4` 回测审计家族。
