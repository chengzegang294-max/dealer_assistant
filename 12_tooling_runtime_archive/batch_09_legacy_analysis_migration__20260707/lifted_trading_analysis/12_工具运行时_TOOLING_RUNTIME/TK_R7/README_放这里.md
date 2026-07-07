# TK-R7 诊断壳（手工标注证据）

## 作用

- 把 `TK-R7 = AO divergence 风险调整标签` 的 proof-of-mapping 做成可审计证据表。
- 当前只做：
  - `ao_divergence_present/side/note` 的一致性分桶
- 当前不做：
  - 自动化硬门控
  - 统计显著性宣称

## 文件

- `tkr7_manual_audit_sheet_v1.tsv`
  - 手工标注表
- `tkr7_manual_audit_summary_v1.md`
  - 汇总（由脚本自动生成）
- `tkr7_manual_audit_summary_v1.tsv`
  - 汇总（可用于后续再加工）

## 填写口径（最小）

- `ao_divergence_present`
  - `0/1`
- `ao_divergence_side`
  - `bullish / bearish / none`
- `ao_risk_adjust_note`
  - `no_divergence`
  - `divergence_watch`
  - `divergence_against_main_signal`
- `tp_context`
  - `pre_tp1 / near_tp1 / near_tp2 / near_tp3 / post_tp3 / unknown`
- `evidence_ref`
  - 允许填图表截图路径/回放片段时间戳/交易记录 id

## 复现口径

- 初始化表：
  - `python tools\tk_r7_make_manual_sheet.py --out-dir "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R7"`
- 生成汇总：
  - `python tools\tk_r7_summarize_manual_sheet.py --sheet "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R7\tkr7_manual_audit_sheet_v1.tsv" --out-dir "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R7"`
- 追加空行（方便你快速填样本）：
  - `python tools\tk_manual_append_rows.py --sheet "12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\TK_R7\tkr7_manual_audit_sheet_v1.tsv" --n 10 --date-tag 20260615`
