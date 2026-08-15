# 信息直播间 C/D 桶动作表（候选，非删房）

- 更新时间：2026-08-08
- 口径：只补 `retention_action` / 原因 / 降权形态；不碰 A/B 最终裁决
- C 桶：`6` | D 桶：`1`

## C_downgrade

- `孙悟空金牌` | action=`summary_only` | freq=`偶发抽检` | msgs=`663` | 模板房，抓取已够，不再全文常更
- `上海老梁` | action=`summary_only` | freq=`低频抽检` | msgs=`119` | 轻量历史，旧 tier 偏低
- `七龙珠` | action=`summary_only` | freq=`低频抽检` | msgs=`113` | 轻量历史，旧 tier 偏低
- `兄安` | action=`summary_only` | freq=`低频抽检` | msgs=`113` | 轻量历史，独特性待证实
- `浮光` | action=`summary_only` | freq=`偶发抽检` | msgs=`94` | 轻量历史，先降权
- `大师兄擒妖` | action=`summary_only` | freq=`偶发抽检` | msgs=`72` | 轻量历史，先降权

## D_score_only_or_archive

- `招财大师姐` | action=`score_only` | freq=`不常更` | msgs=`18` | 短留存，全文价值低

## 机器可读

- [info_live_room_cd_bucket_actions__20260808.tsv](file:///d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/batch_06_rating_inventory__20260808/derived/info_live_room_cd_bucket_actions__20260808.tsv)

## 一句话

- C 先降摘要/偶发抽检，D 只保评分；本轮不删房、不删 runtime。
