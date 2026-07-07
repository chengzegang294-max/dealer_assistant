# TK-R6 诊断壳（手工标注证据）

## 作用

- 把 `TK-R6 = IB 回撤阻挡 -> TP3 概率增强` 的 proof-of-mapping 做成可审计证据表。
- 当前只做：
  - 分桶一致性
  - 证据可追溯
- 当前不做：
  - 自动化硬门控
  - 统计显著性宣称

## 文件

- `tkr6_manual_audit_sheet_v1.tsv`
  - 手工标注表（用于把图表/回放观察落成结构化证据）
- `tkr6_manual_audit_summary_v1.md`
  - 汇总（由脚本从 `tkr6_manual_audit_sheet_v1.tsv` 自动生成）
- `tkr6_manual_audit_summary_v1.tsv`
  - 汇总（可用于后续再加工）

## 填写口径（最小）

- `ib_retest_present`
  - `0/1`
- `ib_retest_quality`
  - `no_retest`
  - `retest_touch_only`
  - `retest_reject_weak`
  - `retest_reject_clear`
- `visible_rejection_hint`
  - `none`
  - `wick_reject`
  - `strong_reclaim`
- `tp3_extension_bias`
  - `none`
  - `weak`
  - `strong`
- `evidence_ref`
  - 允许填图表截图路径/回放片段时间戳/交易记录 id

## 复现口径

- 生成汇总：
  - `python tools\tk_r6_summarize_manual_sheet.py --sheet "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R6\tkr6_manual_audit_sheet_v1.tsv" --out-dir "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R6"`
- 追加空行（方便你快速填样本）：
  - `python tools\tk_manual_append_rows.py --sheet "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R6\tkr6_manual_audit_sheet_v1.tsv" --n 10 --date-tag 20260615`
