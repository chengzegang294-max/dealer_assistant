# KD MTF P0 运行说明 v1

- ARCHIVE_ONLY_RUNTIME_MIRROR: 本文件记录旧 `kd_mtf_p0_v1` 运行时快照，不作为当前主线状态入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 角色

- 这份文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `多周期KD P0` 的当前状态日志。
- 历史阅读顺序、覆盖关系、停点与下一跳：
  - 以 `kd_mtf_p0_directory_index_card_v1.md` 为准

## 当前状态

- 当前目录已创建：
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\`
- 当前目录内历史入口壳已保留：
  - `kd_mtf_p0_directory_index_card_v1.md`
  - `kd_mtf_p0_object_responsibility_card_v1.md`
  - `kd_mtf_p0_quick_entry_card_v1.md`
  - `kd_mtf_p0_b_blocker_note_v1.md`
- 当前目录内历史对象快照已保留：
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
  - `kd_mtf_p0_runtime_params_template_v1.json`
  - `kd_mtf_p0_fields_runtime_header_v1.txt`
  - `kd_mtf_p0_runtime_append_stub_v1.py`
  - `kd_mtf_p0_runtime_append_acceptance_v1.md`
- 当前 proof 样本状态：
  - 当前 `proof_input / proof_output` 已替换为第一份真实 `EURUSD H1` 驱动的 proof 样本
  - 上游输入固定引用：
    - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_first_real_input_bars_v1.csv`
  - 当前总 proof 行数：
    - `8`
  - 当前真实覆盖：
    - `a(up) / a(down) / s(up) / s(down) / conflict / b(down)`
  - 当前首条真实 `b`：
    - `EURUSD H1 2026-03-27T16:00:00Z`
- 当前 `b` 状态日志：
  - 已完成主样本、横向样本、`M15/M1 -> H1` 样本和全 runtime raw bars 样本池扩扫
  - 当前口径修正：
    - 将 `h4_confirm = none` 的判定从“精确相等”改为 `abs(h4_k - h4_d) <= h4_confirm_tie_epsilon`
    - 当前冻结参数：`h4_confirm_tie_epsilon = 0.01`
  - 当前主样本在上述 epsilon 下的扫描统计：
    - `s=368 / a=216 / b=4 / conflict=1452 / unknown=6936`
  - 当前仓库外扩搜状态：
    - `d:\Stock` 范围内仍未发现新的更长 `M1/M15` 连续窗口
  - 当前阻塞详见：
    - `kd_mtf_p0_b_blocker_note_v1.md`
- append stub 当前状态：
  - 已对早先的手工 proof 样本完成过 dry-run / `--persist`
  - 当前已完成对最新真实 `8` 行 proof 的 `--persist`
  - 本轮 persist 记录：
    - `rows_before_cleanup = 5`
    - `proof_rows_loaded = 8`
    - `rows_before_append = 5`
    - `rows_after_append = 13`
  - 当前 runtime csv 行数：
    - `13`
- 当前详细口径、字段边界、对象职责与阅读顺序：
  - `kd_mtf_p0_directory_index_card_v1.md`
  - `kd_mtf_p0_object_responsibility_card_v1.md`
  - `kd_mtf_p0_quick_entry_card_v1.md`
  - `kd_mtf_p0_real_input_mapping_draft_v1.md`

## 当前可宣称

- 已进入工具运行时准备阶段。
- 已固定运行时目录。
- 已冻结第一版 runtime 表头。
- 已固定第一版 proof-of-mapping 草案。
- 已完成首批手工 proof 的 persist 验证。
- 已完成第二批手工 proof 的补样与 dry-run 复核。
- 已完成第二批手工 proof 的 persist 收口。
- 已完成第一份真实 `H1 -> week/day/4h -> proof_input/proof_output` 输入链。
- 已完成最新真实 `8` 行 proof 的 `--persist` 落盘。
- 已完成首条真实 `b` 的落盘（由 `h4_confirm_tie_epsilon=0.01` 支持）。
- 当前 runtime csv 行数：
  - `13`

## 当前不可宣称

- 不可宣称已接入 broker 原始链路重建的真实 runtime 数据。
- 不可宣称 `week/day/4h` 重建逻辑已经过真实链路验证。
- 不可宣称 `多周期KD` 已成为交易门控或仓位引擎。
- 不可宣称 `kd_mtf_p0_runtime_append_stub_v1.py` 已支持直接读取 broker bar 导出。
