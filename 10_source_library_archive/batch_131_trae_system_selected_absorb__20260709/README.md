# Batch 131 Trae System Selected Absorb

## 用途

- 吸收 `21_trae_system_archive/batch_01_selected` 与 `batch_02_selected` 中边界最清楚的正文实体。
- 让 `21_trae_system_archive` 更收敛成 router 与 pointer 层，同时把 recover/prompt 正文放回 `10_source_library_archive` 的批次化来源层。

## 入口

- `INDEX_NOTE`:
  - 当前文件
  - `01_index/family_entry_map_v1.tsv`
  - `01_index/trae_system_selected_family_index_v1.tsv`
  - `01_index/trae_system_selected_promotion_map_v1.tsv`

## 当前口径

- 当前批次吸收的是 recover 正文与 archive-only prompt mirror 正文
- 旧路径仍保留可读正文与 README 回指，本轮先不做全量指针化，避免打断现有引用

## 默认阅读顺序

- 先看当前 README，确认它的作用是把 `21_trae_system_archive` 的正文吸回 `10_source_library_archive`。
- 再看 `01_index/family_entry_map_v1.tsv`，决定是要看：
  - 家族级索引
  - promotion map
  - 还是 raw snapshot 正文
- 需要正文实体时，再进入 `00_raw_snapshot/recover_selected/` 或 `00_raw_snapshot/prompt_selected/`。
