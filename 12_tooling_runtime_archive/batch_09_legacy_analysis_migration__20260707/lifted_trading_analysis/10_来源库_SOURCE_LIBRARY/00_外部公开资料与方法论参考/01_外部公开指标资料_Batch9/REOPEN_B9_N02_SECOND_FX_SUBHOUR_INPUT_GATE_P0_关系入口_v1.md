# REOPEN_B9_N02 SECOND_FX_SUBHOUR_INPUT_GATE_P0 关系入口 v1

## 作用

- 对 `second FX sub-hour input` 做 inventory gate 级验证。
- 当前只确认 `data` 根目录下是否已存在第二个 FX symbol 的 `M1/M5/M15/M30` 原始输入。

## 当前边界（写死）

- 不写入：
  - `n02_p0_fields_runtime_v2.csv`
  - `n02_ib_fields_runtime_v1.csv`
  - `EURUSD/M1` 主行为链下的 sample/card/summary
- 当前只新增：
  - `second FX sub-hour input gate` 的 inventory summary
- 当前不把：
  - 只有 `EURUSD` 的 sub-hour 文件
  - 伪装成第二个 FX sub-hour validation 成功样本

## 当前真值组成（v1）

- `entry_md`：`REOPEN_B9_N02_SECOND_FX_SUBHOUR_INPUT_GATE_P0_关系入口_v1.md`
- `runtime_notes_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_gate_runtime_notes_v1.md`
- `acceptance_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_gate_acceptance_v1.md`
- `build_py`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_gate_build_v1.py`
- `summary_md`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_gate_summary_v1.md`
- `summary_json`：`12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_second_fx_subhour_input_gate_summary_v1.json`

## 最小验收（关系开题级）

- input gate summary 必须显式记录：
  - `fx_subhour_file_count`
  - `fx_subhour_symbols`
  - `fx_subhour_timeframes`
  - `second_fx_subhour_symbol_count`
  - `gate_status`
- 所有输出都必须显式保留：
  - `writes_main_m1_runtime=false`
  - `is_input_gate_only=true`

## 2026-07-05 fresh-run

- 运行入口：
  - `python n02_second_fx_subhour_input_gate_build_v1.py`
- 关键统计：
  - `fx_subhour_file_count=11`
  - `fx_subhour_symbols=["EURUSD"]`
  - `fx_subhour_timeframes=["M1","M5","M15"]`
  - `second_fx_subhour_symbol_count=0`
  - `gate_status=blocked_by_missing_second_fx_subhour_input`
- 当前裁决：
  - 当前 `data` 根目录里确实有 `FX + sub-hour` 文件，但它们仍只覆盖 `EURUSD`。
  - 第二个 FX symbol 的 sub-hour 输入样本尚未出现。
  - 因此这层当前收口为 `input gate`，下一步切到 `second FX sub-hour input acquisition`。

## provenance 说明

- 当前 gate 基于旧仓 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data` 真实文件盘点。
- 本目录及同名产物承担新仓镜像回填与主线索引职责。

## 下一步最顺动作

- 若继续沿同一条线推进，优先补：
  - 第二个 FX symbol 的 `sub-hour` 原始输入样本
