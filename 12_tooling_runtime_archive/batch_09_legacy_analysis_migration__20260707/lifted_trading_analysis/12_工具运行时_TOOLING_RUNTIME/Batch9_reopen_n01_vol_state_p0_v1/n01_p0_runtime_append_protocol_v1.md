# n01_p0_runtime_append_protocol v1

## 目的

- 规定未来脚本向 `n01_p0_fields_runtime_v1.csv` 追加第一批真实数据时应遵守的最小流程。
- 避免把占位样本行、真实运行行和后续版本升级混在一起。

## 当前前提

- 当前 CSV 已有：
  - `1` 行表头
  - 已 append 的第一批真实 proof 行
- 当前真实行来自：
  - `real_input_samples\n01_proof_of_mapping_output_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xauusd_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_eurusd_m15_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xauusd_m15_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_eurusd_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xauusd_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xbrusd_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xbrusd_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_aapl_nas_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_aapl_nas_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_ustec_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_ustec_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_us500_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_us500_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_de40_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_de40_h4_v1.csv`
- 当前 append 动作通过：
  - `n01_p0_runtime_append_from_proof_v1.py`
  已完成一次正式 persist 证据。
- 当前运行时目录还已新增：
  - `n01_p0_runtime_notes_v1.md`
  - `n01_p0_runtime_gaps_v1.md`
- 当前还已新增：
  - `n01_p0_runtime_params_template_v1.json`
  - `n01_p0_runtime_append_stub_v1.py`
  - `n01_p0_runtime_append_from_proof_v1.py`

## 追加真实数据前先做什么

1. 检查表头是否仍与 `n01_p0_fields_runtime_header_v1.txt` 一致
2. 检查本次仍只输出 `N01 P0` 的 `8` 个字段
3. 删除或覆盖当前占位样本行
4. 在 `n01_p0_runtime_notes_v1.md` 记录本次参数来源
5. 先固定 `atr_length / atr_baseline_length / atr_percentile_window / squeeze_mode`
6. 对上述关键参数逐项检查：
   - `source_tier`
   - `source_basis`
   - `evidence_anchor`
   - `upgrade_rule`
7. 当前 v1 追加前要特别确认：
   - `atr_length = 14` 是否继续沿用 GainzAlgo 补充证据中的 ATR 默认长度
   - `atr_baseline_length = 50` 是否继续沿用 GainzAlgo 补充证据口径
   - `atr_percentile_window = 252` 是否继续沿用 Batch9 v1 冻结比较窗口
8. 若未来更换 baseline 或 percentile window，不得直接覆盖 v1，必须新开版本并补来源说明
9. 真正接第一份数据前，先逐项过一遍：
   - `n01_p0_runtime_atr_calculation_checklist_v1.md`
10. 再核对真实输入是否符合：
   - `n01_p0_real_input_mapping_draft_v1.md`
11. 若本次是多份 proof 一起扩样：
   - 不并发对同一个 runtime csv 做 `--persist`
   - 统一按 proof 清单重建 `n01_p0_fields_runtime_v1.csv`

## 第一批真实数据最小要求

- 至少有：
  - `symbol`
  - `timeframe`
  - `bar_time`
  - `atr_percentile_regime`
  - `squeeze_is_on`
  - `squeeze_tier`
  - `squeeze_fired`
- 对历史不足或条件不足的 bar：
  - 允许 `atr_value = na`
  - 允许 `atr_ratio = na`
  - 允许 `atr_percentile = na`
  - 允许 `compression_quality_score = na`
  - `atr_percentile_regime = unknown`

## 不允许

- 不允许保留 `__PLACEHOLDER__` 并同时写入真实数据
- 不允许偷偷加入 `compression_state` 或 `vol_regime_code`
- 不允许改表头却还沿用 `v1` 文件名
- 不允许把参数未冻结的结果写成“已完成”
- 不允许对同一个 `n01_p0_fields_runtime_v1.csv` 做并发 append

## 若需要升级到 v2

- 触发条件示例：
  - 表头变更
  - 新增运行时主键列
  - 新增经过正式裁决的字段
- 升级动作：
  - 新建 `n01_p0_fields_runtime_v2.csv`
  - 新建对应 `header / notes / gaps / append_protocol`
  - 保留 `v1` 不覆盖

## 当前结论

- 这份协议落地后，`REOPEN_B9_N01_VOL_STATE_P0` 已不仅有运行时空壳，还具备了“如何从占位过渡到真实追加”的最小执行约束。
- 当前再往前一步后，已经具备：
  - 参数模板
  - 追加脚本 stub
  - 从 proof 正式 append 到 runtime csv 的脚本
  - dry-run 可复现验证入口
  - 可选 `--persist` 示例行验证入口
  - persist 到 runtime csv 的正式证据
