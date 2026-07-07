# cross_line_frozen_acceptance_chain_index_v1

- ARCHIVE_ONLY: 本文件保留旧 `cross_line_frozen` 的历史总链索引壳，不作为默认入口。
- 当前入口先看：`cross_line_frozen_current_manifest_v1.md`
- super27 收口入口：`cross_line_frozen_chain_entry_super27_v1.md`

## 目的

- 记录根层 `cross-line frozen acceptance chain index` 第一版的历史通过结果。
- 当前目标不是扩新对象，而是把根层 `manifest index / acceptance compare / manifest acceptance` 三层再收成一份更清晰的跨线历史总链索引。

## 本次验收对象

- root manifest index：
  - `cross_line_frozen_manifest_index_v1.md`
- root acceptance compare：
  - `cross_line_frozen_acceptance_compare_v1.md`
- root manifest acceptance：
  - `cross_line_frozen_manifest_acceptance_v1.md`
- chain index exporter：
  - `cross_line_frozen_acceptance_chain_index_v1.py`

## 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python 旧仓库\12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_chain_index_v1.py
```

## 导出结果

- `index_mode = cross_line_frozen_acceptance_chain_index`
- `stage_count = 3`
- `all_stage_files_exist = True`
- `candidate_count = 2`
- `artifact_count = 4`
- `candidate_ids = ["RSJ_STATE_P0", "PV_CORR_STATE_P0"]`
- `write_attempted = false`
- `cross_line_frozen_acceptance_chain_index_passed = true`

## 历史总链索引

- `cross_line_frozen_manifest_index_v1.md`
- `cross_line_frozen_acceptance_compare_v1.md`
- `cross_line_frozen_manifest_acceptance_v1.md`

## 历史可接受结论

- 根层跨线冻结证据链已经具备单一历史总链入口。
- 历史上仍不能宣称：
  - 已接 live binding
  - 已进入 repo-first 历史 runtime append
