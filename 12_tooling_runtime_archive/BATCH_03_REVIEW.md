# Tooling Runtime Archive Batch 03 Review

## 批次结论

- 本批已把旧 `03_MT4便携探针实例` 中最小可复用的文本配置模板承接到新仓库。
- 当前新增位置：
  - `12_tooling_runtime_archive\batch_03_mt4_portable_probe_templates\`
- 这一步的目标不是复制旧终端，而是把 `MT4 portable probe` 的最小可复用配置口径落到新仓。

## 本批迁入方式

- 未直接复制旧 `ini` 为默认执行稿。
- 改为在新仓生成：
  - `mt4probe_volty_portable.template.ini`
  - `smoke_moving_average_portable.template.ini`
- 同时补一份批次 README，说明旧来源、当前作用和未迁部分。

## 为什么这样做

- 旧 `00_text_recovered_batch1` 中有账号态与终端态信息，不适合直接当新仓默认合同。
- 当前真正需要的是：
  - `TestExpert`
  - `TestSymbol`
  - `TestPeriod`
  - `TestModel`
  - `TestDateEnable`
  - `TestReport`
- 这些字段已经足够支撑后续 probe 实跑前的配置参考。

## 明确未迁

- `servers.ini`
  - 原因：账号 / 服务端环境态配置
- `terminal.ini`
  - 原因：窗口态 / 本机终端状态配置
- 原始 `Login / Server`
  - 原因：不应作为新仓默认模板字段

## 验收校验

- 模板字段裁剪校验见：
  - `BATCH_03_TEMPLATE_ACCEPTANCE_CHECK.md`
- 当前结论：
  - 两份模板均保留全部 tester 主字段
  - 仅裁掉 `Login / Server`
  - 未引入未知新增字段

## 下一步建议

1. 在 `MT4_MT5_FIRST_RUN_PLAYBOOK.md` 中优先引用新仓模板路径
2. 继续推进 `Volty DumpSeries=1` 的 fresh-run 证据
3. 等 `XBreaking tester report` 回收后，再决定是否需要补 `MT5` 侧模板批次
