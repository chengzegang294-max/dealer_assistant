# Commit Ready Batch 7C - auction rule local evidence - 2026-06-23

## 目标

- remove project-external evidence dependency from the `A股竞价规则` cards
- move the minimal text evidence anchors into the repository
- rewrite the card source paths to repo-local anchors

## 精确暂存文件

- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R01_9点15到9点20可撤单与假单诱导_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R02_9点20到9点25不可撤单与挂单更真实_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R03_白点未匹配量与红绿柱观察卡_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R04_9点25真实成交与9点25前飙升片段卡_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R21_9点20前涨停封单可撤单片段卡_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R22_9点20前后可信度分界_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R23_白点多与量能活跃不等于直接涨停片段卡_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/A股竞价规则_R25_撮合量放大与抛压变化片段卡_v1.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/README.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/manifest_v1.tsv`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/06.张馨元《集合竞价实战培训》共3集__01.集合竞价规则及异动.mp4_导出.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/08.范博《主力行为集合竞价》共3集__02.集合竞价（二）.flv_导出.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/09.戴强《屠龙战法破解集合竞价》共6集__02.主力是如何通过集合竞价来骗散户的？.mp4_导出.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/09.戴强《屠龙战法破解集合竞价》共6集__06.三大涨停模型中集合竞价的实战.mp4_导出.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/10.首板《涨停板集合竞价》共3集__01.集合竞价买入：如何看竞价.mp4_导出.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/11.百家争鸣《集合竞价视频》共10集__姜灵海《主控思维集合竞价选股实战》.mp4_导出.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/11.百家争鸣《集合竞价视频》共10集__田渊公《集合竞价选股方法及实战应用》.mp4_导出.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/11.百家争鸣《集合竞价视频》共10集__白泽哥《集合竞价分析》.mkv_导出.md`
- `10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/00_本地证据锚点__集合竞价教程/11.百家争鸣《集合竞价视频》共10集__龙头泰山《手把手教你集合竞价抓涨停》.avi_导出.md`
- `docs/COMMIT_READY__BATCH_7C__auction_rule_local_evidence__2026-06-23.md`
- `docs/commit_ready_batch_7C__auction_rule_local_evidence__paths.txt`
- `docs/commit_ready_stage_batch_7C__auction_rule_local_evidence__2026-06-23.ps1`

## 结果边界

- after this batch, the `A股竞价规则` cards no longer depend on default project-external file paths for their primary source anchors
- original external paths are retained only as mapping history in `manifest_v1.tsv`

## 建议提交信息

- `docs: localize auction rule evidence anchors into repo`
