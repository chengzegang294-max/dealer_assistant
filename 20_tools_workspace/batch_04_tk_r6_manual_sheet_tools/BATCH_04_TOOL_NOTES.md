# Batch 04 Tool Notes

## 文件 1：`tk_r6_make_manual_sheet.py`

- 文件类型：`GENERATOR`
- 原路径：`旧仓库\tools\tk_r6_make_manual_sheet.py`
- 新路径：`20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\tk_r6_make_manual_sheet.py`
- 当前作用：
  - 生成 `TK-R6` 的手工审计表模板
  - 预置表头和一行示例数据，方便快速开始人工标注
- 主要输入：
  - `--out-dir`
  - 可选：`--name`
- 主要输出：
  - `tkr6_manual_audit_sheet_v1.tsv`
- 当前用途：
  - 用于把 `TK-R6 = IB 回撤阻挡 -> TP3 概率增强` 的图表观察收成结构化手工证据
- 适用边界：
  - 只负责初始化表模板
  - 不负责统计汇总
  - 不负责交易执行或自动门控
- 证据模式：`historical_recovered_then_promoted`

## 文件 2：`tk_r6_summarize_manual_sheet.py`

- 文件类型：`SUMMARIZER`
- 原路径：`旧仓库\tools\tk_r6_summarize_manual_sheet.py`
- 新路径：`20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\tk_r6_summarize_manual_sheet.py`
- 当前作用：
  - 读取 `TK-R6` 手工标注表
  - 按 `ib_retest_quality` 做计数与 `tp3_reached` 汇总
  - 输出一份 `md` 汇总和一份 `tsv` 汇总
- 主要输入：
  - `--sheet`
  - `--out-dir`
  - 可选：`--out-md / --out-tsv`
- 主要输出：
  - `tkr6_manual_audit_summary_v1.md`
  - `tkr6_manual_audit_summary_v1.tsv`
- 当前用途：
  - 把手工证据表快速压成可读汇总，供后续继续判断 `TK-R6` 是否值得重开
- 适用边界：
  - 只做轻量汇总
  - 不做统计显著性宣称
  - 不直接升级成策略门控
- 证据模式：`historical_recovered_then_promoted`

## 当前批次结论

- `TK-R6` 这 2 个脚本适合先作为“手工证据工具”迁入新仓库。
- 当前不把它们归到：
  - `TK-R1~R4` 回测审计家族
  - 自动执行脚本
  - 一次性删除脚本
- 它们进入新仓库后，默认归 `20_tools_workspace` 维护，不混进 `12_tooling_runtime_archive`。

## 2026-07-03 新仓 smoke 验收

- 实跑入口：
  - `python .\20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\tk_r6_make_manual_sheet.py --out-dir .\20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\smoke_validation\20260703Tsmoke`
  - `python .\20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\tk_r6_summarize_manual_sheet.py --sheet .\20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\smoke_validation\20260703Tsmoke\tkr6_manual_audit_sheet_v1.tsv --out-dir .\20_tools_workspace\batch_04_tk_r6_manual_sheet_tools\smoke_validation\20260703Tsmoke`
- 产物回填：
  - `smoke_validation\20260703Tsmoke\tkr6_manual_audit_sheet_v1.tsv`
  - `smoke_validation\20260703Tsmoke\tkr6_manual_audit_summary_v1.md`
  - `smoke_validation\20260703Tsmoke\tkr6_manual_audit_summary_v1.tsv`
- 最小验收：
  - `exit_code=0`
  - `valid_rows=1`
  - `unknown=1`
- 当前结论：
  - 已确认 `TK-R6` 在新仓可独立完成“生成模板表 -> 读取模板表 -> 输出汇总”的最小闭环
