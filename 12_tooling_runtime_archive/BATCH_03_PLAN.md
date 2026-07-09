# Tooling Runtime 归档批次 03 计划

## 批次目标

- 承接旧 `03_MT4便携探针实例` 中对当前 `Volty / probe` 主线最有复用价值的文本配置模板。
- 不迁整包便携终端，不迁账号态与窗口态配置。

## 本批范围

- 旧位置：
  - `旧仓库\12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例\config\00_text_recovered_batch1\`
- 首批候选角色：
  - `Volty portable probe ini`
  - `Moving Average smoke ini`
  - 配置恢复说明

## 本批判断原则

- 只迁可读、可模板化、对当前 probe 主线有帮助的文本配置。
- `servers.ini / terminal.ini` 这类账号态、终端态、环境态配置不直接迁入新仓默认入口。
- 新仓落地时优先做成 `template.ini`，避免把旧环境参数原样继承成默认合同。

## 本批验收

- `12_tooling_runtime_archive` 新增一批 `MT4 portable probe templates`。
- 至少补一份 `Volty` 模板和一份 smoke 模板。
- 明确哪些旧配置仍只保留在旧仓冻结层。
