# kd_mtf_p0_runtime_append_protocol_v1

## 目的

- 规定当前脚本向 `kd_mtf_p0_fields_runtime_v1.csv` 追加真实 proof 时应遵守的最小流程。

## 当前前提

- 当前运行时目录已固定为：
  - `02_runtime\dy_r1_kd_mtf_p0`
- 当前 CSV 已有：
  - `1` 行表头
  - `12` 行 runtime 数据
- 当前 proof 样本已在本目录就位：
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`

## append stub 当前使用边界

- `kd_mtf_p0_runtime_append_stub_v1.py` 当前只负责：
  - 读取 `proof_output_csv`
  - 校验 runtime 表头
  - 去掉重复 proof 主键
  - 把 proof 行写入 `kd_mtf_p0_fields_runtime_v1.csv`
- 当前不负责：
  - 读取 broker 原始导出
  - 时区归一化
  - 从 bar 数据重建 `week/day/4h`
  - 直接把原始 bar 算成 KD 字段

## 追加真实数据前先做什么

1. 检查表头仍与 `kd_mtf_p0_fields_runtime_header_v1.txt` 一致
2. 确认 proof 输出仍只覆盖当前 `KD P0` 字段族
3. 确认参数合同仍固定：
   - `13,3,3 + sma + close_close`
4. 确认 proof 样本没有被误写成 broker 原始 bars
5. 再决定是否执行 `--persist`

## 当前上游样本边界

- 第一份完整 canonical H1 bars 大样本已落在：
  - `upstream_samples\n01_first_real_input_bars_v1.csv`
- 当前 append 可独立运行
- 后续若补 proof 重建脚本，应优先直接引用本目录这份上游样本

## 不允许

- 不允许偷偷加入：
  - `kd_month_bias`
  - `kd_1h_entry_refine`
  - `kd_divergence_flag`
  - `kd_perfect_state_flag`
  - `kd_dispersion_state`
  - `kd_position_size_multiplier`
- 不允许改表头却还沿用 `v1` 文件名
- 不允许对同一个 `kd_mtf_p0_fields_runtime_v1.csv` 做并发 append
- 不允许把 proof 文件的更新直接写成“broker 原始链路已完成”
