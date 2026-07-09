# Cross-Line Frozen 链路清单验收 v1

- ARCHIVE_ONLY: 本文件保留旧 `cross_line_frozen` 的历史总链验收壳，不作为默认入口。
- 当前入口先看：`cross_line_frozen_current_manifest_v1.md`
- super27 收口入口：`cross_line_frozen_chain_entry_super27_v1.md`

## 目的

- 记录根层 `cross-line frozen chain manifest acceptance` 第一版的历史通过结果。
- 当前目标不是扩新对象，而是把“历史总链索引 + 总链 compare + 根层 manifest acceptance”再收成更高一层的跨线总链冻结验收。

## 本次验收对象

- chain index：
  - `cross_line_frozen_acceptance_chain_index_v1.md`
- chain acceptance compare：
  - `cross_line_frozen_chain_acceptance_compare_v1.md`
- root manifest acceptance：
  - `cross_line_frozen_manifest_acceptance_v1.md`
- manifest acceptance validator：
  - `cross_line_frozen_chain_manifest_acceptance_v1.py`

## 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python 旧仓库\12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_chain_manifest_acceptance_v1.py
```

## 校验结果

- validation 输出确认：
  - `validation_mode = cross_line_frozen_chain_manifest_acceptance`
  - `artifact_count = 3`
  - `all_artifacts_exist = True`
  - `candidate_count = 2`
  - `rows_match = true`
  - `write_attempted = false`
  - `cross_line_frozen_chain_manifest_acceptance_passed = true`

## 历史可接受结论

- 跨线历史总链索引、跨线总链 compare、根层 manifest acceptance 当前一致且全部存在。
- 历史上仍不能宣称：
  - 已接 live binding
  - 已进入 repo-first 历史 runtime append
