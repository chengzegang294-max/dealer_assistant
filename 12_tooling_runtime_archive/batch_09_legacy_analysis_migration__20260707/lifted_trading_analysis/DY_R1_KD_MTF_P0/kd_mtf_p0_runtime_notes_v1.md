# kd_mtf_p0_runtime_notes_v1

- ARCHIVE_ONLY_RUNTIME_MIRROR: 本文件记录旧独立包 `DY_R1_KD_MTF_P0` 的历史状态快照，不作为当前主线状态入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 角色

- 这份文件属于 `DY_R1_KD_MTF_P0` 独立包。
- 作用是记录 `多周期KD P0` 的当前状态日志。
- 历史阅读顺序、覆盖关系、停点与下一跳：
  - 以 `kd_mtf_p0_directory_index_card_v1.md` 为准

## 当前状态

- 当前目录已创建：
  - `DY_R1_KD_MTF_P0\`
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
    - `upstream_samples\n01_first_real_input_bars_v1.csv`
  - 当前总 proof 行数：
    - `7`
  - 当前真实覆盖：
    - `a(up) / a(down) / s(up) / s(down) / conflict`
  - 当前真实样本仍未补出：
    - `b`
- 当前 `b` 状态日志：
  - 已完成主样本、横向样本、`M15/M1 -> H1` 样本和全 runtime raw bars 样本池扩扫
  - 当前主样本总扫描统计：
    - `s = 3587`
    - `a = 1856`
    - `b = 0`
    - `conflict = 8318`
    - `unknown = 73438`
  - 当前工程阻塞：
    - `h4_confirm = none` 只会落在 `h4_k == h4_d`
    - 当前已扫真实浮点样本中没有自然出现这种精确相等
  - 当前仓库外扩搜状态：
    - `d:\Stock` 范围内仍未发现新的更长 `M1/M15` 连续窗口
  - 当前阻塞详见：
    - `kd_mtf_p0_b_blocker_note_v1.md`
- append stub 当前状态：
  - 已对早先的手工 proof 样本完成过 dry-run / `--persist`
  - 当前 `kd_mtf_p0_fields_runtime_v1.csv` 仍保留那批历史 `5` 行手工样本
  - 已对最新真实 `EURUSD H1` 驱动的 `7` 行 proof 再次执行 dry-run
  - 最新 dry-run 结果：
    - `rows_before_cleanup = 5`
    - `proof_rows_loaded = 7`
    - `rows_before_append = 5`
    - `rows_after_append = 12`
    - `dry_run_only = true`
  - 当前已确认：
    - stub 能正常读取这批最新真实 `7` 行 proof
    - 当前只完成内存态追加验证，尚未重新 `--persist`
    - `kd_mtf_p0_fields_runtime_v1.csv` 仍未被这轮 dry-run 改写
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
- 已完成最新真实 `7` 行 proof 的 append stub dry-run。
- 当前 runtime csv 行数：
  - `5`

## 当前不可宣称

- 不可宣称已接入 broker 原始链路重建的真实 runtime 数据。
- 不可宣称 `week/day/4h` 重建逻辑已经过真实链路验证。
- 不可宣称最新真实 `proof_output_v1.csv` 已经 append 进 `kd_mtf_p0_fields_runtime_v1.csv`。
- 不可宣称最新真实 `7` 行 proof 已完成 `--persist`。
- 不可宣称 `多周期KD` 已成为交易门控或仓位引擎。
- 不可宣称 `kd_mtf_p0_runtime_append_stub_v1.py` 已支持直接读取 broker bar 导出。
