# Tooling Runtime Archive Batch 03 Template Acceptance Check

## 目的

- 这份文件用于证明 `batch_03_mt4_portable_probe_templates` 的模板不是随手重写，而是基于旧配置做过字段级裁剪校验。

## 校验范围

- 旧来源：
  - `旧仓库\12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例\config\00_text_recovered_batch1\`
- 新位置：
  - `12_tooling_runtime_archive\batch_03_mt4_portable_probe_templates\`

## 校验方法

- 将旧 `ini` 与新 `.template.ini` 解析成 `key=value` 字段集合
- 检查：
  - 是否保留所有当前 probe 需要的 tester 字段
  - 是否只裁掉账号态/环境态字段
  - 是否新增了未知字段

## Volty 模板

- 旧文件：
  - `mt4probe_volty_portable.ini`
- 新文件：
  - `mt4probe_volty_portable.template.ini`
- 保持一致的字段：
  - `EnableNews`
  - `ExpertsEnable`
  - `ExpertsDllImport`
  - `ExpertsExpImport`
  - `ExpertsTrades`
  - `TestExpert`
  - `TestExpertParameters`
  - `TestSymbol`
  - `TestPeriod`
  - `TestModel`
  - `TestOptimization`
  - `TestDateEnable`
  - `TestFromDate`
  - `TestToDate`
  - `TestVisualEnable`
  - `TestReplaceReport`
  - `TestReport`
  - `TestShutdownTerminal`
- 裁掉的字段：
  - `Login`
  - `Server`
- 新增字段：
  - `none`

## Smoke 模板

- 旧文件：
  - `smoke_moving_average_portable.ini`
- 新文件：
  - `smoke_moving_average_portable.template.ini`
- 保持一致的字段：
  - `EnableNews`
  - `ExpertsEnable`
  - `ExpertsDllImport`
  - `ExpertsExpImport`
  - `ExpertsTrades`
  - `TestExpert`
  - `TestExpertParameters`
  - `TestSymbol`
  - `TestPeriod`
  - `TestModel`
  - `TestOptimization`
  - `TestDateEnable`
  - `TestFromDate`
  - `TestToDate`
  - `TestVisualEnable`
  - `TestReplaceReport`
  - `TestReport`
  - `TestShutdownTerminal`
- 裁掉的字段：
  - `Login`
  - `Server`
- 新增字段：
  - `none`

## 当前裁决

- 本批模板达到：
  - `template_fields_preserved_for_tester_flow`
  - `account_server_fields_intentionally_removed`
  - `no_unknown_added_fields`
- 这说明 `batch_03` 的模板化不是信息丢失，而是受控脱敏和边界化。
