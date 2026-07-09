# Cross-Line Frozen 清单索引 v1

- ARCHIVE_ONLY: 本文件保留旧 `cross_line_frozen` 的历史索引壳，不作为默认入口。
- 当前入口先看：`cross_line_frozen_current_manifest_v1.md`
- super27 收口入口：`cross_line_frozen_chain_entry_super27_v1.md`

## 目的

- 作为 `RSJ State P0 / PV Corr State P0` 两条旧链路冻结清单层的跨线历史索引壳。
- 把两条线各自的 `manifest freeze` 再收成一个根层历史索引，方便后续在跨线层做统一复核追溯。

## 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python 旧仓库\12_工具运行时_TOOLING_RUNTIME\cross_line_frozen_manifest_index_v1.py
```

## 导出结果

- `index_mode = cross_line_frozen_manifest_index`
- `runtime_root_exists = True`
- `candidate_count = 2`
- `all_candidates_manifest_frozen = True`
- `candidate_ids = ["RSJ_STATE_P0", "PV_CORR_STATE_P0"]`
- `write_attempted = false`
- `cross_line_frozen_manifest_index_passed = true`

## 历史跨线索引

- `RSJ_STATE_P0`
  - `manifest_count = 12`
  - `all_manifest_files_exist = True`
  - `manifest_freeze = rsj_state_p0_manifest_freeze_v1.md`
- `PV_CORR_STATE_P0`
  - `manifest_count = 12`
  - `all_manifest_files_exist = True`
  - `manifest_freeze = pv_corr_state_p0_manifest_freeze_v1.md`

## 历史可接受结论

- `RSJ / PV Corr` 两条旧链路都已进入跨线统一可复核入口。
- 历史上仍不能宣称：
  - 已接 live binding
  - 已进入 repo-first 历史 runtime append
