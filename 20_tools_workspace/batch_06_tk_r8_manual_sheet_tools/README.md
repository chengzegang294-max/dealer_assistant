# TK R8 Manual Sheet Tools Batch 06

## 用途

- 这里放从旧 `tools` 中筛出来、仍有长期复用价值的 `TK-R8` 手工审计表工具。
- 这批脚本不负责交易执行，也不负责回测主流程；它们只负责：
  - 初始化手工标注表
  - 对已填写的手工表生成汇总

## 当前文件

- `tk_r8_make_manual_sheet.py`
- `tk_r8_summarize_manual_sheet.py`

## 当前裁决

- 这 2 个脚本都属于：
  - 输入输出明确
  - 依赖轻，只使用标准库
  - 可脱离旧 `backtest_out` 主流程独立复用
- 当前仍保留的边界：
  - 它们服务的是 `TK-R8` 手工证据壳
  - 不是自动化门控脚本
  - 不是 `TK-R1~R4` 那类强绑定旧回测批次的审计家族

## 备注入口

- 批次备注见：`BATCH_06_TOOL_NOTES.md`
