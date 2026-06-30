# KD MTF P0 目录索引卡 v1

## 用途

- 这张卡只负责说明 `DY-R1 / KD_MTF_P0` 在 `trading_assistant` 里的对象结构怎么读。
- 当前对象不再放在单一旧目录中，而是拆成对象层、运行时层、文档层三部分。

## 三层结构

### A. 对象层

- 位置：
  - `01_active_objects\dy_r1_kd_mtf_p0\`
- 作用：
  - 放最短入口
  - 放对象职责
  - 放目录索引

### B. 运行时层

- 位置：
  - `02_runtime\dy_r1_kd_mtf_p0\`
- 作用：
  - 放 `append stub`
  - 放参数合同
  - 放表头合同
  - 放 runtime csv
  - 放 proof 样本
  - 放上游 canonical bars 样本
  - 放 runtime notes / gaps / protocol / acceptance

### C. 文档层

- 位置：
  - `03_docs\dy_r1_kd_mtf_p0\`
- 作用：
  - 放主线长稿
  - 放 `b` 阻塞说明

## 当前文件分工

- 本目录：
  - `kd_mtf_p0_directory_index_card_v1.md`
  - `kd_mtf_p0_quick_entry_card_v1.md`
  - `kd_mtf_p0_object_responsibility_card_v1.md`
- 运行时层：
  - `kd_mtf_p0_runtime_notes_v1.md`
  - `kd_mtf_p0_runtime_gaps_v1.md`
  - `kd_mtf_p0_runtime_append_protocol_v1.md`
  - `kd_mtf_p0_runtime_append_acceptance_v1.md`
  - `kd_mtf_p0_runtime_append_stub_v1.py`
  - `kd_mtf_p0_runtime_params_template_v1.json`
  - `kd_mtf_p0_fields_runtime_header_v1.txt`
  - `kd_mtf_p0_fields_runtime_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
  - `upstream_samples\n01_first_real_input_bars_v1.csv`
  - `upstream_samples\README.md`
- 文档层：
  - `kd_mtf_p0_real_input_mapping_draft_v1.md`
  - `kd_mtf_p0_b_blocker_note_v1.md`

## 推荐读法

### 路线 1：想快速续跑

1. `kd_mtf_p0_directory_index_card_v1.md`
2. `kd_mtf_p0_quick_entry_card_v1.md`
3. `kd_mtf_p0_object_responsibility_card_v1.md`
4. `03_docs\dy_r1_kd_mtf_p0\kd_mtf_p0_b_blocker_note_v1.md`
5. `03_docs\dy_r1_kd_mtf_p0\kd_mtf_p0_real_input_mapping_draft_v1.md`

### 路线 2：想判断当前状态

1. `kd_mtf_p0_directory_index_card_v1.md`
2. `02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_notes_v1.md`
3. `02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_gaps_v1.md`
4. `kd_mtf_p0_object_responsibility_card_v1.md`

### 路线 3：准备碰 append

1. `kd_mtf_p0_directory_index_card_v1.md`
2. `02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_append_protocol_v1.md`
3. `02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_append_acceptance_v1.md`
4. `02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_append_stub_v1.py`

## 当前停点

- 真实 proof 输入链已打通
- 最新真实 `7` 行 proof 已在新运行时层完成一次 `--persist`
- 当前 runtime csv 已是 `12` 行
- `b` 仍无真实样本

## 当前不要误读

- 新对象已经迁入 `trading_assistant`，但旧仓库仍保留作历史冻结对照。
- 当前运行时层已独立可跑，不应继续把旧目录当成活跃维护位置。
- 当前 `proof -> runtime` 已独立可跑，且完整 canonical H1 bars 大样本也已在新目录运行时层落地。
