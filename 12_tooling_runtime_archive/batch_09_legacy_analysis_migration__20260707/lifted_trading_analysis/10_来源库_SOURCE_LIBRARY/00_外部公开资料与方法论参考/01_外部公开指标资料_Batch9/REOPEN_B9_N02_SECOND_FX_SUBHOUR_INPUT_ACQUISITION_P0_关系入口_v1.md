# REOPEN_B9_N02 SECOND_FX_SUBHOUR_INPUT_ACQUISITION_P0 关系入口 v1

## 作用

- 对 `second FX sub-hour input acquisition` 做已知源盘点级验证。
- 当前只确认 `data + MT4 history` 已知源里是否已经存在第二个 FX symbol 的 `M1/M5/M15/M30` 原始输入。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `EURUSD/M1` 主行为链下的 sample/card/summary
- 当前只新增：
  - `second FX sub-hour input acquisition` 的 inventory/acquisition summary
- 当前不把：
  - 只有 `EURUSD` 的 sub-hour 实源
  - 伪装成第二个 FX sub-hour validation 成功样本

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_ACQUISITION_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_acquisition_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_acquisition_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_acquisition_build_v1.py`
- `summary_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_acquisition_summary_v1.md`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_acquisition_summary_v1.json`

## 最小验收（关系开题级）

- acquisition summary 必须显式记录：
  - `data_subhour_file_count`
  - `mt4_subhour_file_count`
  - `combined_second_fx_subhour_symbol_count`
  - `known_higher_tf_fx_symbols_without_subhour`
  - `recommended_target`
  - `acquisition_status`
- 所有输出都必须显式保留：
  - `writes_main_m1_runtime=false`
  - `is_acquisition_only=true`

## 2026-07-05 fresh-run

- 运行入口：
  - `python n02_second_fx_subhour_input_acquisition_build_v1.py`
- 关键统计：
  - `data_subhour_file_count=11`
  - `mt4_subhour_file_count=8`
  - `combined_second_fx_subhour_symbol_count=0`
  - `known_higher_tf_fx_symbols_without_subhour=["GBPUSD","USDCHF","USDJPY"]`
  - `recommended_target=GBPUSD/M15`
  - `acquisition_status=blocked_by_missing_second_fx_subhour_across_known_sources`
- 当前裁决：
  - 当前已知 `data + MT4 history` 源整体没有第二个 FX symbol 的 `sub-hour` 输入。
  - 第二个 FX 的最顺补样本目标固定为：`GBPUSD/M15`
  - 因此这层当前收口为 `acquisition`，下一步切到 `GBPUSD/M15 cache recovery ready -> terminal export -> n02_mt5_export_ingest_v1`。

## provenance 说明

- 当前 acquisition 基于旧仓 `data` 与两套 `MT4 history` 真实文件盘点。
- 本目录及同名产物承担新仓镜像回填与主线索引职责。
