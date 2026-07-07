# cross_line_frozen_acceptance_compare_v1

- ARCHIVE_ONLY: 本文件保留旧 `cross_line_frozen` 的历史 compare 壳，不作为默认入口。
- 当前入口先看：`cross_line_frozen_current_manifest_v1.md`
- super27 收口入口：`cross_line_frozen_chain_entry_super27_v1.md`

## 目的

- 记录根层 `cross_line frozen manifest index` 第一版 acceptance compare 的历史通过结果。
- 当前目标不是扩新入口，而是确认根层历史索引正文中的两条 candidate block 与实际冻结状态完全一致。

## 本次验收对象

- cross-line index：
  - `cross_line_frozen_manifest_index_v1.md`
- compare validator：
  - `cross_line_frozen_acceptance_compare_v1.py`

## 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python 旧仓库\12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_acceptance_compare_v1.py
```

## 校验结果

- validation 输出确认：
  - `validation_mode = cross_line_frozen_acceptance_compare`
  - `index_md_exists = True`
  - `indexed_candidate_count = 2`
  - `expected_candidate_count = 2`
  - `rows_match = true`
  - `candidate_ids = ["RSJ_STATE_P0", "PV_CORR_STATE_P0"]`
  - `write_attempted = false`
  - `cross_line_frozen_acceptance_compare_passed = true`

## 历史可接受结论

- 根层跨线历史索引正文与实际冻结状态一致。
- 历史上仍不能宣称：
  - 已接 live binding
  - 已进入 repo-first 历史 runtime append
