# 系统吸收对象入口 v1

## 适用问题

- 想直接看系统正文吸收后的 family index
- 想快速区分 family index、promotion map 与 raw snapshot 正文
- 不想先从批次 README 再判断下一跳

## first-hop 入口

- `../../batch_131_trae_system_selected_absorb__20260709/01_index/trae_system_selected_family_index_v1.tsv`

## 默认阅读顺序

- 先看 family index：
  - `../../batch_131_trae_system_selected_absorb__20260709/01_index/trae_system_selected_family_index_v1.tsv`
- 再看 promotion map：
  - `../../batch_131_trae_system_selected_absorb__20260709/01_index/trae_system_selected_promotion_map_v1.tsv`
- 只有在需要正文实体时，再回：
  - `../../batch_131_trae_system_selected_absorb__20260709/00_raw_snapshot/recover_selected/`
  - `../../batch_131_trae_system_selected_absorb__20260709/00_raw_snapshot/prompt_selected/`

## 当前边界

- 这是“系统吸收对象”的快入口，不替代 `21_trae_system_archive` 的 router 层。
- 若要看批次边界与用途说明，再回批次 README。

## 回链

- 上层主题入口：
  - `../trae_system_absorb_topic_entry_v1.md`
