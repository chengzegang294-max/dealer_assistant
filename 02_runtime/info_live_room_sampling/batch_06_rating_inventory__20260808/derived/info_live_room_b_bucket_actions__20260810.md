# 信息直播间 B 桶动作表（首轮落地，非删房）

- 更新时间：2026-08-10
- 口径：只处理 `B_observe` 共 `15` 房；默认 `keep_fragments`；不碰 A 最终名次，不重开 C/D
- 机器可读：[info_live_room_b_bucket_actions__20260810.tsv](file:///d:/Stock/dealer_assistant/02_runtime/info_live_room_sampling/batch_06_rating_inventory__20260808/derived/info_live_room_b_bucket_actions__20260810.tsv)

## 默认冻结

1. B 桶默认动作：`keep_fragments`（继续看，不保全文）
2. 不作默认全文扩档
3. 不删房、不删 runtime 证据
4. 升 A / 降 C 只允许按「例外房间」单独说明

## 按子类

### 1. `anchor_high_overlap` / 已进片段短名单

- `天机` | `keep_fragments` | 偶发抽检 | msgs=`517` | sample12 高重叠
- `k神` | `keep_fragments` | 偶发抽检 | msgs=`293` | sample12 高重叠

### 2. `anchor_template`

- `周期女王` | `keep_fragments` | 低频抽检 | msgs=`267`
- `格兰投研` | `keep_fragments` | 低频抽检 | msgs=`259`
- `龙头交易猿` | `keep_fragments` | 低频抽检 | msgs=`149`

### 3. `style_shortchat`

- `梦幻一步` | `keep_fragments` | 偶发抽检 | msgs=`156`

### 4. `mid_depth_observe`

- `游资胖大叔` | msgs=`360`
- `潜伏王者` | msgs=`351`
- `擒龙小师姐` | msgs=`256`
- `独家竞价低吸` | msgs=`247`
- `小锦鲤` | msgs=`229`
- `核心逻辑社` | msgs=`217`
- `新生代` | msgs=`150`

以上统一：常规观察 + 只保关键片段。

### 5. `research_short_history`

- `机构研报资讯精选` | msgs=`70` | 先看是否能常更
- `小作文嗅嗅+机构研报` | msgs=`40` | 先看是否与长研报房重复

## 一句话

- B 桶先统一「片段优先、不扩全文」；研究短史两房单独盯升降前提，天机/k神已进正式片段短名单。
