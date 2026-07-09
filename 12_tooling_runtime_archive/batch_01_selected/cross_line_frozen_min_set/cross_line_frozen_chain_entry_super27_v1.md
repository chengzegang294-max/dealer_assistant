# Cross-Line Frozen 链路入口（super27）

更新时间：2026-07-07

## 目的

- 把旧库 `cross_line_frozen` 的 `super*` 长尾命名与重复壳，压成单一可读入口。
- 默认只做“维护态抽查”：不写入，不回流默认入口，不把旧链路描述成可续跑工作流。

## 当前停点

- `super27`
- `candidate_count = 2`：`RSJ_STATE_P0`、`PV_CORR_STATE_P0`
- `write_attempted = false`

## 当前跨线入口（唯一）

- 旧库跨线入口：`12_tooling_runtime_archive/batch_09_legacy_analysis_migration__20260707/lifted_trading_analysis/12_工具运行时_TOOLING_RUNTIME/cross_line_frozen_manifest_index_v1.md`

## 旧链路映射（ARCHIVE_ONLY）

- 旧库 super* 长文件名与本镜像包的映射：`12_tooling_runtime_archive/batch_01_selected/cross_line_frozen_min_set/cross_line_frozen_super27_legacy_file_map_v1.tsv`
- 长文件名只允许留在这张映射表里，禁止回流到默认入口正文。

## 旧链路 super* 证据（ARCHIVE_ONLY）

- 只在需要追溯历史链路模板时阅读；不作为默认入口。
- super27 六步证据（短命名镜像包）：
  - `12_tooling_runtime_archive/batch_01_selected/cross_line_frozen_min_set/cross_line_frozen_super27_index_v1.md`
  - `12_tooling_runtime_archive/batch_01_selected/cross_line_frozen_min_set/cross_line_frozen_super27_acceptance_compare_v1.md`
  - `12_tooling_runtime_archive/batch_01_selected/cross_line_frozen_min_set/cross_line_frozen_super27_manifest_acceptance_v1.md`
  - `12_tooling_runtime_archive/batch_01_selected/cross_line_frozen_min_set/cross_line_frozen_super27_chain_index_v1.md`
  - `12_tooling_runtime_archive/batch_01_selected/cross_line_frozen_min_set/cross_line_frozen_super27_chain_acceptance_compare_v1.md`
  - `12_tooling_runtime_archive/batch_01_selected/cross_line_frozen_min_set/cross_line_frozen_super27_chain_manifest_acceptance_v1.md`
