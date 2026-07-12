# 系统吸收与正文回收主题入口 v1

## 适用问题

- 想知道 `21_trae_system_archive` 的正文哪些已经吸回来源层
- 想快速找到 `family index / promotion map / raw snapshot 正文`
- 想区分系统正文吸收批和 archive-only raw snapshot 批

## first-hop 入口

- `../batch_131_trae_system_selected_absorb__20260709/README.md`

## 最顺阅读顺序

- 第一步：
  - 先看 `../batch_131_trae_system_selected_absorb__20260709/01_index/family_entry_map_v1.tsv`
- 第二步：
  - 若想看家族级目录，进入 `01_index/trae_system_selected_family_index_v1.tsv`
  - 若想看旧路径到新批次的提升映射，进入 `01_index/trae_system_selected_promotion_map_v1.tsv`
- 第三步：
  - 只有在需要正文实体时，再进入 `00_raw_snapshot/recover_selected/` 或 `00_raw_snapshot/prompt_selected/`

## 当前边界

- 当前主题入口主要服务：
  - 系统正文吸回来源层后的导航
  - family index / promotion map / recover 正文之间的阅读路线
- 当前不承担：
  - `21_trae_system_archive` 的 router 入口替代
  - archive-only raw snapshot 的默认 first-hop

## 配套说明

- 正文吸收批：
  - `batch_131_trae_system_selected_absorb__20260709`
- archive-only raw snapshot 批：
  - `batch_132_trae_system_raw_snapshot_batch09_absorb__20260709`

## 回链

- 来源库根入口：
  - `../README.md`
- 批次家族入口：
  - `../batch_131_trae_system_selected_absorb__20260709/01_index/family_entry_map_v1.tsv`
