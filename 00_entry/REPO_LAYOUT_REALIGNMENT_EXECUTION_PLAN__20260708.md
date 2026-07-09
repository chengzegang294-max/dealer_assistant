# Repo Layout Realignment Execution Plan

更新时间：2026-07-09

## 目标

- 把当前仍不符合 `DIRECTORY_ROLE_CONTRACT_v1.md` 的大块目录，按“可执行批次”拆成归位清单。
- 先收最确定、最不会引起语义歧义的部分，再处理需要拆分判定的大块。

## P1 目录

- `00_assets/`
  - 问题：合同外顶层目录，内部混装来源快照、原始数据、运行产物、导出物。
  - 处理原则：
    - `ashare_clean`、`ashare_watchlist/kline_1d` 这类真实行情样本，归 `02_runtime/.../acceptance_samples` 或 `02_runtime/.../data/raw`
    - 外部资料快照、HAR、网页素材，归 `10_source_library_archive/<batch>/00_raw_snapshot`
    - 旧导出、探针、运行结果、网页壳运行时，归 `12_tooling_runtime_archive/<batch>`
  - 第一批优先：
    - `00_assets/_raw_snapshot_batch09/ashare_clean`
    - `00_assets/_raw_snapshot_batch09/ashare_watchlist/kline_1d`
    - 其余先做目录台账，不直接整包搬
  - 当前进度：
    - 已完成 `ashare_clean` -> `02_runtime/.../data/raw/daily_ohlcv/batch09_promoted/ashare_clean`
    - 已完成 `ashare_watchlist/kline_1d` -> `02_runtime/.../data/raw/daily_ohlcv/batch09_promoted/watchlist_kline_1d`
    - 已完成 `ashare_watchlist` 剩余非 `kline_1d` 三分流：
      - `topN_day/week`、`focus_pool`、`core_pool`、`watchlist_screen`、`factors_ladder` -> `02_runtime/.../data/raw/watchlist_inputs/`
      - 对应 `.txt` 文本快照 -> `10_source_library_archive/.../ashare_watchlist_text_snapshot/`
      - `blogroom_* / mx2025_summary_*` -> `12_tooling_runtime_archive/.../batch_09_watchlist_ocr_artifacts__20260708/`

- `20_tools_workspace/`
  - 问题：合同外顶层目录，当前混放在维护工具、历史脚本、临时材料。
  - 处理原则：
    - 仍在维护且直接服务主线的脚本，归 `02_runtime/`
    - 历史工具运行时、历史脚本快照，归 `12_tooling_runtime_archive/<batch>`
    - 临时材料或会话剪贴，按主题落 `10_source_library_archive/<batch>/00_raw_snapshot`
  - 第一批优先：
    - `20_tools_workspace/smoke_validation`
    - `20_tools_workspace/_raw_snapshot_batch09`
    - `20_tools_workspace/session_clip`
  - 当前进度：
    - 已完成 `session_clip/临时粘贴区__20260708.md` -> `10_source_library_archive/batch_120_tools_workspace_absorb__20260709/00_raw_snapshot/session_clip/`
    - 已完成 `BATCH_01_PLAN/REVIEW`、`BATCH_02_PLAN/REVIEW` -> `00_entry/TOOLS_WORKSPACE_BATCH_*`
    - 已完成 `batch_04~06` 下 `smoke_validation/20260703Tsmoke` -> `12_tooling_runtime_archive/batch_120_tk_manual_sheet_smoke__20260709/artifacts/{tkr6,tkr7,tkr8}/`
    - `20_tools_workspace/_raw_snapshot_batch09` 仍待下一轮按 archive-only 口径整体吸收

- `21_trae_system_archive/`
  - 问题：合同外顶层目录，整体属于系统材料与 AI 产物归档层。
  - 处理原则：
    - skills/router/prompt/history 等整体按批次归 `10_source_library_archive/<batch_trae_system_absorb>`
    - 若有已冻结裁决或阶段性总结，再二次筛入 `11_frozen_summaries_archive`
    - 若是当前仍有效的仓库级治理文档，再回到 `00_entry/`
  - 第一批优先：
    - `SKILLS_INDEX.md`
    - `SKILLS_GROUP_VIEW.md`
    - `recover_*`

## P2 目录与文件

- `04_active_main_docs/BATCH_01_PLAN.md`
- `04_active_main_docs/BATCH_01_REVIEW.md`
  - 问题：迁移台账误放在日常入口层
  - 处理：已回收到 `00_entry/BATCH_01_PLAN.md` 与 `00_entry/BATCH_01_REVIEW.md`

- `ROOT_NOTES.md`
- `ROOT_VSCODE_SETTINGS_TEMPLATE.jsonc`
  - 问题：根目录散放说明卡和配置模板
  - 建议：合并进 `00_entry/` 或并入根 `README.md`

## 执行顺序

1. 先做 `README` 与全局入口口径收敛，避免继续按旧骨架入库
2. 再拆 `00_assets` 的最确定样本块
3. 再拆 `20_tools_workspace`
4. 最后处理 `21_trae_system_archive`

## 已完成

- `04_active_main_docs/BATCH_01_PLAN.md` -> `00_entry/BATCH_01_PLAN.md`
- `04_active_main_docs/BATCH_01_REVIEW.md` -> `00_entry/BATCH_01_REVIEW.md`
- `00_assets/_raw_snapshot_batch09/ashare_clean` -> `02_runtime/butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv/batch09_promoted/ashare_clean`
- `00_assets/_raw_snapshot_batch09/ashare_watchlist/kline_1d` -> `02_runtime/butler_r0_ohlcv_object_cards/data/raw/daily_ohlcv/batch09_promoted/watchlist_kline_1d`
- `00_assets/_raw_snapshot_batch09/ashare_watchlist` 剩余非 `kline_1d` 文件已按 runtime structured inputs / source text snapshot / tooling OCR artifacts 三分流归位
- `20_tools_workspace/session_clip/临时粘贴区__20260708.md` -> `10_source_library_archive/batch_120_tools_workspace_absorb__20260709/00_raw_snapshot/session_clip/`
- `20_tools_workspace/BATCH_01_PLAN.md`、`BATCH_01_REVIEW.md`、`BATCH_02_PLAN.md`、`BATCH_02_REVIEW.md` -> `00_entry/TOOLS_WORKSPACE_BATCH_*`
- `20_tools_workspace/batch_04~06/*/smoke_validation/20260703Tsmoke` -> `12_tooling_runtime_archive/batch_120_tk_manual_sheet_smoke__20260709/artifacts/{tkr6,tkr7,tkr8}/`

## 本轮不直接动的内容

- 需要逐文件判定角色的大杂烩目录
- 尚未确认是否为当前主线活跃资产的脚本/配置
- 任何会影响现有可跑入口的路径，先补回链与索引，再移动
