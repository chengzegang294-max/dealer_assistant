# TK-R8 诊断壳（手工标注证据）

## 作用

- 把 `TK-R8 = B 区域 qualify 壳` 的 proof-of-mapping 做成可审计证据表。
- 当前只做：
  - `zone_alignment + abc_integrity + continuation_quality -> b_zone_quality_note` 的分桶一致性
- 当前不做：
  - 自动化挂单/硬门控
  - 统计显著性宣称

## 文件

- `tkr8_manual_audit_sheet_v1.tsv`
  - 手工标注表
- `tkr8_manual_audit_summary_v1.md`
  - 汇总（由脚本自动生成）
- `tkr8_manual_audit_summary_v1.tsv`
  - 汇总（可用于后续再加工）

## 填写口径（最小）

- `zone_alignment`
  - `aligned_to_b_zone / near_b_zone / missed_b_zone`
- `abc_integrity`
  - `abc_intact / abc_soft / abc_broken`
- `continuation_quality`
  - `continuation_supportive / continuation_soft_or_mixed / continuation_lost`
- `b_zone_quality_note`
  - `qualified_b_zone / weak_b_zone / not_b_zone`
- `evidence_ref`
  - 允许填图表截图路径/回放片段时间戳/交易记录 id

## 复现口径

- 初始化表：
  - `python tools\tk_r8_make_manual_sheet.py --out-dir "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R8"`
- 生成汇总：
  - `python tools\tk_r8_summarize_manual_sheet.py --sheet "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R8\tkr8_manual_audit_sheet_v1.tsv" --out-dir "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R8"`
- 追加空行（方便你快速填样本）：
  - `python tools\tk_manual_append_rows.py --sheet "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R8\tkr8_manual_audit_sheet_v1.tsv" --n 10 --date-tag 20260615`
