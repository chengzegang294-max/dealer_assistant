# Source Library Backlog 2026-06-23 - 来源层真实迁移

## Scope

- Repository root: `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis`
- Audit target: `10_来源库_SOURCE_LIBRARY`
- This sheet only handles items that are currently classified as `真实迁移 / relayout`, not real loss.

## Current Verdict

- Current deletion total under `10_来源库_SOURCE_LIBRARY`: `334`
- After the path audit in this round, the `334` deletions are fully explainable by `3` migration clusters.
- Current migration split:
  - `03_Kimi拆书待入库 -> 01_Kimi拆书待入库`: `237` deleted
  - `01_外部公开指标资料_Batch9 -> 00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9`: `66` deleted
  - `02_外部视频与方法论参考\Smile_SMC交易系统2_0 -> 00_外部公开资料与方法论参考\02_外部视频与方法论参考\Smile_SMC交易系统2_0`: `31` deleted
- Current conclusion:
  - `334 = 237 + 66 + 31`
  - there is no remaining directory-level deletion cluster outside these migrations

## Cluster 1

- old root: `10_来源库_SOURCE_LIBRARY\03_Kimi拆书待入库`
- current root: `10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库`
- current status:
  - old path deletions: `237`
  - new path untracked truth files: `158`
- paired anchors already visible on both sides:
  - `GROUP_01_微观结构_交易所_HFT`
  - `GROUP_02_期权_波动率_波动率微笑`
  - `GROUP_03_组合管理_风险模型_交易成本`
  - `GROUP_04_统计套利_研究方法_ML`
  - `GROUP_05_趋势_系统交易`
  - `GROUP_06_Auction_MarketProfile_价格行为`
  - `GROUP_07_传记_行业史_故事`
  - `GROUP_08_A股量化_数据研究`
  - `GROUP_09_完善体系书库_切割产物`
  - `GROUP_10_A5_财报_估值_组合管理`
  - `S_BUCKET_SUMMARY__2026-06-17.md`
  - `S_BUCKET_INDEX__2026-06-17.tsv`
  - `S_BUCKET_report_representatives_v1-v52.tsv`
  - `S_BUCKET_stage_proof__03_券商研报__representatives_v1-v52.tsv`
- strongest evidence:
  - `GROUP_08_external_move_postcheck_v1.md` records `move_rows = 52`, `moved_ok = 52`, `still_at_source = 0`, `missing_both = 0`
  - `GROUP_08_external_ops_stats_v1.md` records `MOVE / BOOKDIR = 52`, while the remaining `DELETE_CANDIDATE / S03 = 8` is a later cleanup window inside the new tree
- current verdict: `真实迁移主力`

## Cluster 2

- old root: `10_来源库_SOURCE_LIBRARY\01_外部公开指标资料_Batch9`
- current tracked root: `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9`
- current status:
  - old path deletions: `66`
  - no new untracked mirror is needed, because the current target tree already exists as tracked truth
- current tracked anchors confirmed in the new root:
  - `batch9_source_manifest.csv`
  - `Batch9_批次收口与四分流_v1.md`
  - `N01_波动率状态机\`
  - `N02_时段_开盘区间结构\`
  - `N03_市场结构_突破质量_条件收集\`
  - `REOPEN_B9_N01_VOL_STATE_P0_*`
  - `REOPEN_B9_N02_SESSION_OR_P0_*`
- current verdict:
  - these `66` deletions are old-root cleanup after the directory was absorbed into the `00_外部公开资料与方法论参考` truth lane
  - they should not be treated as accidental loss

## Cluster 3

- old root: `10_来源库_SOURCE_LIBRARY\02_外部视频与方法论参考\Smile_SMC交易系统2_0`
- current tracked root: `10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\02_外部视频与方法论参考\Smile_SMC交易系统2_0`
- current status:
  - old path deletions: `31`
  - no new untracked mirror is needed, because the current target tree already exists as tracked truth
- current tracked anchors confirmed in the new root:
  - `Smile_SMC交易系统2_0_吸收与总纲_v1.md`
  - `Smile_SMC交易系统2_0_逐帧运行过程_文字化_v1.md`
  - `raw_materials\一套完整的加密货币交易系统2.0公开上集.md`
  - `raw_materials\一套完整的加密货币交易系统2.0公开下集.md`
  - `raw_materials\video_screenshots\`
- current verdict:
  - these `31` deletions are old-root cleanup after the material was归位 into the `00_外部公开资料与方法论参考` tree
  - they should not be treated as accidental loss

## Action Contract

- Do not bulk-restore these `334` deletions.
- Review them as `path migration evidence`, not as `missing truth`.
- If a later commit is prepared, the correct framing is:
  - old roots are being retired
  - new roots are already the truth anchors
- Any exception that loses its current tracked counterpart must be removed from this sheet and moved to `误删候选`.
