# cross_line_frozen_chain_acceptance_compare_v1

- ARCHIVE_ONLY: 本文件保留旧 `cross_line_frozen` 的历史总链 compare 壳，不作为默认入口。
- 当前入口先看：`cross_line_frozen_current_manifest_v1.md`
- super27 收口入口：`cross_line_frozen_chain_entry_super27_v1.md`

## 目的

- 记录根层 `cross-line frozen acceptance chain index` 第一版 acceptance compare 的历史通过结果。
- 当前目标不是扩新对象，而是确认历史总链索引文档与实际跨线冻结层级没有漂移。

## 本次验收对象

- chain index：
  - `cross_line_frozen_acceptance_chain_index_v1.md`
- compare validator：
  - `cross_line_frozen_chain_acceptance_compare_v1.py`

## 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python 旧仓库\12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_chain_acceptance_compare_v1.py
```

## 校验结果

- validation 输出确认：
  - `validation_mode = cross_line_frozen_chain_acceptance_compare`
  - `chain_index_md_exists = True`
  - `indexed_stage_count = 3`
  - `expected_stage_count = 3`
  - `rows_match = true`
  - `candidate_ids = ["RSJ_STATE_P0", "PV_CORR_STATE_P0"]`
  - `write_attempted = false`
  - `cross_line_frozen_chain_acceptance_compare_passed = true`

## 历史可接受结论

- 跨线冻结历史总链索引正文与实际冻结层级一致。
- 历史上仍不能宣称：
  - 已接 live binding
  - 已进入 repo-first 历史 runtime append
