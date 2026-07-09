# N02 IB 合同说明 v1

## 目的

- 这份说明用于把 `IB` 从“对象入口”推进到“可复现映射证据 + 可复述合同口径”的下一层。
- 当前只做 `IB proof-of-mapping` 与合同口径说明，不写入 `N02 P0` 的 runtime 主 CSV。

## 配套文件（proof 三件套）

- `real_input_csv`：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_first_real_input_bars_v1.csv`
  - 可选补样本（按 session 定向补覆盖，避免互相制造 `ib_defined=0` 噪音）：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_london_spring_20260327_20260331_bars.csv`
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_dst_newyork_spring_20260306_20260310_bars.csv`
- `proof_script_py`：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_v1.py`
- `proof_output_csv`：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_ib_proof_of_mapping_output_v1.csv`
- `object_build_py`：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_build_v1.py`
- `object_sample_csv`：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_sample_v1.csv`
- `object_summary_json`：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_object_p0_summary_v1.json`

## 当前口径

- `IB` 处于 `N02` 后续对象层，不属于当前 `N02 P0` 字段合同。
- `ib_window_minutes` v1 默认固定为 `60`，用于生成最小 IB 区间。
- session 的时区与本地开盘锚点来自：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\real_input_samples\n02_or_proof_config_v1.json`
- 输出的 `session_local_date` 必须按 `session_timezone` 的本地日历解释，不允许手写固定 UTC 偏移。

## 输出字段（proof 输出）

每行代表：

- 某个 `session_id`
- 某个 `session_local_date`
- 在该本地日期下的 `IB window` 计算结果

字段固定为：

- `symbol`
- `timeframe`
- `session_id`
- `session_timezone`
- `session_local_date`
- `ib_window_minutes`
- `ib_start_utc`
- `ib_end_utc`
- `ib_high`
- `ib_low`
- `ib_range`
- `ib_mid`
- `bars_in_ib_window`
- `ib_defined`

## 空值与未定义

- 若 `bars_in_ib_window = 0`：
  - `ib_defined = 0`
  - `ib_high/ib_low/ib_range/ib_mid` 为空
- 这类行不代表 IB 口径错误，只表示当前样本在该本地日期没有覆盖到所需窗口。

## OBJECT_P0 派生口径

- `IB_OBJECT_P0` 不直接改写 `n02_p0_fields_runtime_v2.csv`，而是从 `n02_ib_fields_runtime_v1.csv` 派生独立对象样本。
- `n02_ib_object_p0_build_v1.py` 只收 `ib_defined = 1` 的行，生成：
  - `n02_ib_object_p0_sample_v1.csv`
  - `n02_ib_object_p0_summary_v1.json`
- 对象样本的最小身份键固定为：
  - `object_id = IB|symbol|timeframe|session_id|session_local_date|ib_window_minutes`
- `object_summary_json` 必须显式记录：
  - `producer`
  - `scope`
  - `evidence_mode`
  - `source_path`
  - `repo_path`
  - 当前边界布尔项（不含 acceptance / failed breakout / retest-reject / day type）

## 当前明确不含

- `IB acceptance`
- `IB failed breakout`
- `IB retest/reject`
- `day type`
- 任何把 `IB` 写回 `n02_p0_fields_runtime_v2.csv` 的升级动作

## runtime notes

- `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_runtime_notes_v1.md`
- `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_fields_runtime_v1.csv`
- `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_ib_runtime_append_from_proof_v1.py`

## 当前结论

- `IB` 已具备可复现的 proof 输出与字段口径。
- `IB runtime CSV` 已独立落盘，可在不污染 `N02 P0` 的前提下累积对象证据行。
- `2026-07-03` 已补出 `IB_OBJECT_P0 sample + summary`，对象层最小证据链现已独立可复现。
- `2026-07-03` 已继续补出 `IB vs OR relation sample + summary`，说明对象层已能向下游关系层稳定扩展。
- 仍不引入 `IB acceptance` 等行为标签。
