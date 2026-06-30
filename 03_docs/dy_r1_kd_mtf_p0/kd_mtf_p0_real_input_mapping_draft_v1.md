# kd_mtf_p0_real_input_mapping_draft_v1

## 目的

- 这份文件记录 `DY-R1 / KD_MTF_P0` 当前从真实 H1 bars 到 `proof_input / proof_output / runtime` 的最小映射链。
- 当前在新目录里只保留主线必要说明，不重复旧仓库背景叙述。

## 当前对象结构

- 对象层：
  - `01_active_objects\dy_r1_kd_mtf_p0\`
- 运行时层：
  - `02_runtime\dy_r1_kd_mtf_p0\`
- 文档层：
  - `03_docs\dy_r1_kd_mtf_p0\`

## 当前本地已就位对象

- `..\..\02_runtime\dy_r1_kd_mtf_p0\real_input_samples\kd_mtf_p0_proof_input_v1.csv`
- `..\..\02_runtime\dy_r1_kd_mtf_p0\real_input_samples\kd_mtf_p0_proof_output_v1.csv`
- `..\..\02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_fields_runtime_v1.csv`
- `..\..\02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_append_stub_v1.py`
- `..\..\02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_proof_builder_v1.py`

## 当前本地上游样本

- 第一份完整 canonical H1 bars 大样本已在新目录正式导入：
  - `..\..\02_runtime\dy_r1_kd_mtf_p0\upstream_samples\n01_first_real_input_bars_v1.csv`

## 已知真实映射链

- 当前主链仍是：
  - `raw H1 canonical bars -> proof_input_v1.csv -> proof_output_v1.csv -> runtime csv`
- 当前 `proof_input_v1.csv` 保存：
  - `week_k`
  - `week_d`
  - `day_k_prev`
  - `day_d_prev`
  - `day_k`
  - `day_d`
  - `h4_k`
  - `h4_d`
- 当前 `proof_output_v1.csv` 再派生：
  - `kd_week_bias`
  - `kd_day_signal`
  - `kd_4h_confirm`
  - `kd_alignment_tier`
  - `kd_direction_filter`
  - `kd_week_extreme_zone`

## 当前固定口径

- 固定基础周期：
  - `H1`
- 固定高周期重建：
  - `4h / day / week`
- 固定参数：
  - `13,3,3 + sma + close_close`
- 固定分桶：
  - `UTC`
- 固定取值边界：
  - 只取目标 `bar_time` 之前最近的已闭合高周期

## 当前 proof 覆盖

- 当前总 proof 行数：
  - `7`
- 当前已覆盖：
  - `a(up)`
  - `a(down)`
  - `s(up)`
  - `s(down)`
  - `conflict`
- 当前仍未覆盖：
  - `b`

## 当前 runtime 状态

- 当前 runtime csv 行数：
  - `12`
- 当前组成：
  - 历史 `5` 行手工 persist 样本
  - 最新真实 `7` 行 proof

## 当前边界

- 新目录当前已经独立覆盖：
  - `proof -> runtime`
  - 上游 canonical H1 bars 的本地持有
  - `raw H1 bars -> proof_input / proof_output` 的最小脚本化实现
- 新目录当前还未独立覆盖：
  - 多样本、多目标批次的 proof builder 工程化入口
- 因此当前不能把新目录写成“完整工程化原始链路已全部迁入”

## 下一步

1. 继续把相关路径全部收口到本地上游样本路径
2. 继续在新目录里推进 proof 重建与 `b` 补样
3. 若需要，再把 `proof builder` 扩成多样本批次入口
