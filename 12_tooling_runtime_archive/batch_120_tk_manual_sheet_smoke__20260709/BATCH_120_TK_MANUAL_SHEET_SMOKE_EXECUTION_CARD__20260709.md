# 批次 120 TK Manual Sheet Smoke 执行卡

## 生成入口

- `GENERATOR`: `historical_recovered_manual_move_20260709`
- `SOURCE`:
  - `20_tools_workspace/batch_04_tk_r6_manual_sheet_tools/smoke_validation/20260703Tsmoke/`
  - `20_tools_workspace/batch_05_tk_r7_manual_sheet_tools/smoke_validation/20260703Tsmoke/`
  - `20_tools_workspace/batch_06_tk_r8_manual_sheet_tools/smoke_validation/20260703Tsmoke/`

## 当前作用

- 把 `tkr6 / tkr7 / tkr8` 的 `20260703Tsmoke` 手工审单产物从合同外工作区回收到 tooling runtime archive。
- 保留这些 TSV/MD 作为历史 smoke 验收证据，不把它们误当成当前主线的默认运行输入。
