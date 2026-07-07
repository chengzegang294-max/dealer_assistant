# KD MTF P0 目录索引卡 v1

- ARCHIVE_ONLY_RUNTIME_MIRROR: 本卡只用于说明旧 `DY_R1_KD_MTF_P0` 独立包的历史结构，不作为当前目录级总入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 用途

- 这张卡只负责说明 `DY_R1_KD_MTF_P0` 独立包里每份文件当时做什么、先读什么、哪些先不要碰。
- 目标是保留旧独立包的追溯关系，不再把本目录当成当前默认进入 `DY-R1` 的第一跳。

## 目录内文件怎么分

### A. 先读入口

- `kd_mtf_p0_directory_index_card_v1.md`
  - 历史目录级索引壳
  - 负责说明目录职责、阅读顺序、停点和下一跳
- `kd_mtf_p0_object_responsibility_card_v1.md`
  - 历史对象级入口壳
  - 负责说明代码/合同/产物对象现在各自做什么
- `kd_mtf_p0_quick_entry_card_v1.md`
  - 历史最短入口镜像
  - 仅供追溯，不作为当前默认续跑入口

### B. 当前主线长稿

- `kd_mtf_p0_real_input_mapping_draft_v1.md`
  - 当前最完整的主线映射与转换链长稿
  - 负责记录：
    - 上游样本
    - `H1 -> 4h/day/week -> proof_input -> proof_output`
    - 输入输出映射
    - 已闭合规则
    - proof 落点与当前边界

### C. 当前状态与缺口

- `kd_mtf_p0_runtime_notes_v1.md`
  - 当前状态日志
  - 用来判断“现在做到了哪、不能宣称什么”
- `kd_mtf_p0_runtime_gaps_v1.md`
  - 当前缺口清单
  - 用来判断“下一刀最顺做什么”
- `kd_mtf_p0_b_blocker_note_v1.md`
  - 当前 `b` 为什么补不出来的独立阻塞页
  - 适合在继续扫样本前先看，避免重复劳动

### D. append 相关

- `kd_mtf_p0_runtime_append_protocol_v1.md`
  - append 规则和边界
  - 只在准备碰 append 时才需要读
- `kd_mtf_p0_runtime_append_acceptance_v1.md`
  - append 历史验收记录
  - 只说明旧手工 proof 的 dry-run / persist 结论
  - 不能读成“最新真实 proof 已 append”
- `kd_mtf_p0_runtime_append_stub_v1.py`
  - append stub 本体
  - 当前仍不是 broker 原始 bars 入口

### E. 合同与产物

- `kd_mtf_p0_runtime_params_template_v1.json`
  - 参数与枚举合同
- `kd_mtf_p0_fields_runtime_header_v1.txt`
  - runtime 表头合同
- `kd_mtf_p0_fields_runtime_v1.csv`
  - 当前 runtime 落盘文件
  - 目前还是历史手工 proof persist 结果，不是最新真实 proof append 结果
- `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - 当前真实 proof 输入样本
- `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
  - 当前真实 proof 输出样本

## 推荐读法

### 路线 1：想追溯旧续跑路径

1. `kd_mtf_p0_directory_index_card_v1.md`
2. `kd_mtf_p0_quick_entry_card_v1.md`
3. `kd_mtf_p0_object_responsibility_card_v1.md`
4. `kd_mtf_p0_b_blocker_note_v1.md`
5. `kd_mtf_p0_real_input_mapping_draft_v1.md`

### 路线 2：想判断现在缺什么

1. `kd_mtf_p0_directory_index_card_v1.md`
2. `kd_mtf_p0_runtime_notes_v1.md`
3. `kd_mtf_p0_runtime_gaps_v1.md`
4. `kd_mtf_p0_object_responsibility_card_v1.md`
5. `kd_mtf_p0_b_blocker_note_v1.md`

### 路线 3：准备碰 append

1. `kd_mtf_p0_directory_index_card_v1.md`
2. `kd_mtf_p0_runtime_append_protocol_v1.md`
3. `kd_mtf_p0_runtime_append_acceptance_v1.md`
4. `kd_mtf_p0_runtime_append_stub_v1.py`

## Repo-First 入口声明

- 目录级读法、停点和下一跳：
  - 以本文件为准
- 默认阅读顺序：
  - 先看 `kd_mtf_p0_directory_index_card_v1.md`
  - 再看 `kd_mtf_p0_quick_entry_card_v1.md`
  - 再看 `kd_mtf_p0_object_responsibility_card_v1.md`
  - 再看 `kd_mtf_p0_b_blocker_note_v1.md`
  - 最后回到 `kd_mtf_p0_real_input_mapping_draft_v1.md`
- 当前停点：
  - 真实 proof 输入链已打通
  - `a / s / conflict` 已有真实样本
  - `b` 仍无真实样本
- 当前不要停错到：
  - `kd_mtf_p0_runtime_append_acceptance_v1.md`
  - `kd_mtf_p0_fields_runtime_v1.csv`
- 当前不要误读：
  - `append_acceptance` 只覆盖历史手工 proof persist
  - `runtime csv` 仍是旧的 `5` 行手工 persist 样本
  - `params template` 不是完整真实链路入口
- 当前按职责分层：
  - `index = 怎么读`
  - `quick_entry = 怎么续跑`
  - `object = 对象干什么`
  - `notes = 当前状态`
  - `gaps = 还缺什么`
  - `blocker = 为什么卡住`
  - `mapping_draft = 完整主线长稿`
- 当前下一跳：
  - 新样本到位后，先读 `quick_entry + blocker`
  - 继续整理时，先回 `mapping_draft`
  - 准备碰 append 时，先读 `runtime_append_protocol`
