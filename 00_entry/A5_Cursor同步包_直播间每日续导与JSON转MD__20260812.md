# A5 Cursor同步包 · 直播间「每日续导 + JSON → 规范 MD」（盯梢后置·先不做）

更新时间：2026-08-13  
工作仓：`d:\Stock\dealer_assistant`

---

## 0. 一句话结论（先给结论，再看依据）

> **现阶段只做 2 件事，不做盯梢：**
> ① 每天人工续导（接上昨天断点，想停就停，不必24房全导）→ 丢中转篮 `batch_XX/00_raw/`
> ② AI 拿中转篮的 JSON → migrate 入库 → 生成规范 MD 落在 `rooms/<房>/10_ingest/<房>_日期_人读摘要旧到新.md`（四格统计 + 按时间旧→新正文，判断格空着）
> 盯梢 / 全绿 / 每日人工吸收入口：以后再做；现在先把这两步收口
> FROZEN_OUT 2 间（永不置顶、不进每日必导）：`机构电话会议纪要+小作文+情报` / `机构研报资讯精选` → 只在 SKIP_ROOMS 保留；要导只能单独导；只存 00_raw，不自动出 MD；以后另行开研报/电话家族
> 空文件 0 条（message_count=0）→ 绝不进 MD
> 词频 TOP5 不是正史 → 仅参考，不得当事实结论

---

## 一、给 Trae / 其它 AI 引用的开工命令（别改）

```text
今日直播间 Raw 已入档。
中转：d:\Stock\dealer_assistant\02_runtime\info_live_room_sampling\batch_08_rooms_backfill__20260812\00_raw
请 migrate + 转 MD（跳过机构电话、机构研报）。
```

- 完整同步命令：`/live-md`（正式 Trae 命令

---

## 二、第一步：每天人工收录导出（续昨天 + 想停就停，不用24房全导）

### 2.1 环境（严格（别改）

- **同一浏览器，别清站点数据（清了缓存。独立 Chrome/Edge：https://mx2025.hhhuu.com/#/ 登录
- F12 Console 跑，**不要微信内嵌**
- 导出脚本全文：
  `20_tools_workspace/batch_07_info_live_room_tools/live_info_incremental_export_v1.js
- （你先 JS 文件不要改源码

### 2.2 日常续跑（推荐 RESUME 模式，**默认用这个）

```js
window.__infoLiveIncrementalExportV1Options = {
  forced_room_anchor: "房间正式名",
  reset_checkpoint: false,
  start_position: "keep",
  scroll_direction: "up",
  max_rounds: 60,
  max_no_new_rounds: 3,
  scroll_sleep_ms: 350
};
```
→ 然后再 **全文粘贴** `live_info_incremental_export_v1.js` 一整段

| 想停时**：
| 少滚一会儿 | 把 `max_rounds` 改成 `30` |
| 滚完一轮就收工 | 等它自己停（到轮次上限 / 没新消息 / 到顶之后才下JSON |
| 不要中途杀进程 | 文件可能不完整 |

看到 `resumed_from_checkpoint: true` → **✅ 接上昨天了，没问题；
看到 `false` 且 0 条旧数据 → **⚠️ 缓存被清了**，这时候才用下面 FRESH（**日常不要 FRESH。

### 2.3 少滚模式（FRESH）— 只有缓存没了才用，日常别用

```js
window.__infoLiveIncrementalExportV1Options = {
  forced_room_anchor: "房间正式名",
  reset_checkpoint: true,
  start_position: "bottom",
  scroll_direction: "up",
  max_rounds: 60,
  max_no_new_rounds: 3,
  scroll_sleep_ms: 350
};
```

### 2.4 22房正式名（写 forced_room_anchor）**按正式名（别名无效）。2026-08-13 裁决：A4机构电话+B23机构研报 永久踢出 A/B 桶每日置顶流程→FROZEN_OUT 另行处理（要做单独开研报/电话家族，不混在直播间里）**

#### A 桶（Tier1·每日置顶必导，每日优先做这 8 房）

| A桶编号 | 桶 | 正式名（forced_room_anchor 精确填这个） | 必导优先度 |
|---|---|---|---|
| A1 | A | 复盘哥 | ★★★★★ 每日必导（全房样本量第一） |
| A2 | A | 独家老师5号 | ★★★★★ 每日必导（超大样本 6000+条） |
| A3 | A | 独家短线老师6号 | ★★★★ |
| A4 | A | 梅森 | ★★★★ 原A5顺推 |
| A5 | A | 顺势而为 | ★★★★ 原A6顺推 |
| A6 | A | 混江龙 | ★★★★★ 作者多活跃 原A7顺推 |
| A7 | A | 天赢居 | ★★★★ 原A8顺推 |
| A8 | A | 先知 | ★★★★★ 必导 原A9顺推 |

#### B 桶（Tier2·每日活跃选导，14房，挑有活跃话题的做）

| B桶编号 | 桶 | 正式名（forced_room_anchor 精确填这个） | 必导优先度 |
|---|---|---|---|
| B10 | B | 天机 | ★★★ |
| B11 | B | 游资胖大叔 | ★★ |
| B12 | B | 潜伏王者 | ★★ |
| B13 | B | k神 | ★★★★ |
| B14 | B | 周期女王 | ★★★ |
| B15 | B | 格兰投研 | ★★★★ B桶消息最多 403作者 |
| B16 | B | 擒龙小师姐 | ★★ |
| B17 | B | 独家竞价低吸 | ★★ |
| B18 | B | 小锦鲤 | ★★ |
| B19 | B | 核心逻辑社 | ★★ |
| B20 | B | 梦幻一步 | ★★ |
| B21 | B | 新生代 | ★★ |
| B22 | B | 龙头交易猿 | ★★★★ |
| B24 | B | 小作文嗅嗅+机构研报 | ★★★★（保留每日，和B23不同类） |

#### FROZEN_OUT（另行处理家族·永久踢出 A/B 桶每日流程，不参与每日置顶/必导，要做另开新通道）

| F编号 | 原来的桶 | 正式名 | 为什么冻结（用户裁决2026-08-13） | Raw 保留说明 |
|---|---|---|---|---|
| F1 | 原A4 A桶Tier1 | 机构电话会议纪要+小作文+情报 | 每天更新内容太多很难获取，会降低直播间其他内容的比重，失去 A 桶 8 房的情绪/风格/节奏重点；研报/电话类以后要做单独开家族做，不混在直播间 | 00_raw 24件已入库保留不删，以后开单独家族直接拷过去 |
| F2 | 原B23 B桶Tier2 | 机构研报资讯精选 | 用户2026-08-12已明确不吸收自己重做；今日和F1机构电话并为FROZEN_OUT，同属研报/电话类另行处理，不再每日 | 00_raw 6件已入库保留不删 |

**FROZEN_OUT 硬规则：** F1/F2 永远不在每日必导/置顶列表里；任何流程（续导/migrate/转MD/分类器训练）里永远硬跳过；00_raw 不丢不删；单独要做研报/电话家族的时候再开新 batch。

### 2.5 JSON 丢哪？

→ JSON 先丢中转篮（按日新建也行）：
`02_runtime/info_live_room_sampling/batch_08_rooms_backfill__20260812/00_raw/
或 `batch_XX_rooms_backfill__YYYYMMDD/00_raw/`
**不要自己建 rooms 文件夹；migrate 工具会自动落到 `rooms/<房>/00_raw/`

---

## 三、第二步：JSON 自动整理成规范 MD（就是你说的「吸收整理好」= 10_ingest 里的格式稿（不是最终判断）

### 3.1 硬规则（不讨论

| # | 规则 |
|---|---|
| 1 | `空文件 0 条消息（`message_count=0` 或当日合并 0 条有效正文）→ **不进 MD，直接 SKIP，绝不写 10_ingest/ |
| 2 | **FROZEN_OUT** 硬跳过两间（原A4/原B23，永不置顶不给★）：`机构电话会议纪要+小作文+情报` / `机构研报资讯精选` → 只落 00_raw，绝不自动出 Prefill / 人读摘要 MD；要导只能单独导；以后开新家族 |
| 3 | MD 结果 = 不是最终判断 → 判断 3 格（情绪/风格/节奏）永远留空，人类填 |
| 4 | **词频 TOP5（关键词/代码/作者）→ **不是正史** 仅参考 · 不得当事实结论 · 不得当买入信号 |
| 5 | 正文消息按时间旧→新排，默认前 120 条正文每条前 200 字，超过截断 |

### 3.2 MD 字段合同（多AI讨论只讨论这里的字段，别加别改）

每份 `<房>_YYYYMMDD_人读摘要旧到新.md 结构（定死，不讨论）：

```md
# <房名> / YYYY-MM-DD 人读摘要（期末=YYYY-MM-DD；四格TOP5+按时间旧→新；机器不判）

- 生成时间：YYYY-MM-DD HH:mm:ss
- 期末交易日期：YYYY-MM-DD
- 当日 Raw 文件数：X 份 （message_count=0 跳过 Y 件坏文件
- 总消息条数：N   去重活跃作者数：M
- 源文件（前 3 份旧→新：....

## 一、四格统计（格1/格2/格3/格4）
| 格 | 项 | 值（TOP5 / 值 + 频次
|---|---|---|
| 1 | TOP5 关键词（情绪/题材/板块；**词频非正史·仅参考不作事实结论**） | 关键词1:N 关键词2:N ...
| 2 | TOP5 股票代码（6位命中次数） | 代码1:N 代码2:N ...
| 3 | TOP5 活跃作者（发言条数多→少；**词频非正史·仅参考**） | 作者1:N 作者2:N ...
| 4 | 基本统计（总消息/作者/Raw文件数/0坏文件数 | N 条 / M 人 / X 份 / Y 件

## 二、按时间旧→新 TOP120 条（每条截断前200字，长截断
| # | 日期 | 时间 | 作者 | 正文前200字（>200截断） | 来源文件 |
|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... |

> 人类判断 3 格（机器不填）：
> ```
> [ ] 情绪偏多空（强多/多/震荡/空/强空）：________
> [ ] 主抓风格（打板/低吸/埋伏/空仓/轮动）：________
> [ ] 次日节奏（接力高度/中位/首板/观望）：________
> [ ] 粘贴上面四格 + 3 格 → 贴进 20_absorb/NOTES.md → 末尾补「已吸收 @ YYYY-MM-DD」
> ```
```

### 3.3 AI 执行口令（/live-md 命令加载后，AI 自动做）

1. migrate 工具把 JSON 从 中转篮/00_raw/ → rooms/<房>/00_raw/（SHA 禁反向覆盖）
2. 工具：
   `20_tools_workspace/batch_09_rooms_archive_tools/migrate_raw_from_batch05_and_batch07_to_rooms_v1.py --batch-dir <中转篮/00_raw> --apply`
3. 转 MD 工具（默认增量差分模式=不用每次跑很长续跑，不用加参数直接跑）：
   `20_tools_workspace/batch_09_rooms_archive_tools/build_AB24_rooms_human_summary_v3.py --rooms-root 02_runtime/info_live_room_sampling/rooms --trade-date YYYYMMDD --apply`
   【偶尔全量校验：才加 `--mode full`，日常默认 incremental 增量不用加】
4. 结果：
   `rooms/<房>/10_ingest/<房>_YYYYMMDD_人读摘要旧到新.md`
   + 对应 Prefill 草稿精简版（四格精简）
5. 每间房 checkpoint：`rooms/<房>/10_ingest/.checkpoint/<房>_YYYYMMDD_absorb_checkpoint.json`（记录已吸收 Raw SHA256 + Counter 快照，下次增量跑就 KEEP 不动省时间，真测过 22/22 全 KEEP）

---

## 四、本阶段不做什么（红线）

1. ❌ 不做 midday_watch 盯梢 / 红绿 TSV 全绿 24 房 = 先做好两步再说
2. ❌ 不强制用户 24 房全部每间人工 3 格判断全填完 = 先整理成规范 MD 再说
3. ❌ 不把词频 TOP5 当正史/当买卖信号
4. ❌ 不自动给 机构电话（A4）/ 机构研报（B23）出 MD = 用户明确自己重做
5. ❌ 不把空 0 条坏文件写 MD

---

## 五、读文件索引（相关）

| 文件 | 说明 |
|---|---|
| [A5_Cursor同步包_直播间Raw补洞对接Trae__20260812.md](file:///D:/Stock/dealer_assistant/00_entry/A5_Cursor%E5%90%8C%E6%AD%A5%E5%8C%85_%E7%9B%B4%E6%92%AD%E9%97%B4Raw%E8%A1%A5%E6%B4%9E%E5%AF%B9%E6%8E%A5Trae__20260812.md) | 阶段1 24房Raw补洞 |
| [build_AB24_rooms_human_summary_v2.py](file:///D:/Stock/dealer_assistant/20_tools_workspace/batch_09_rooms_archive_tools/build_AB24_rooms_human_summary_v2.py) | JSON→MD工具 v2 （已集成 0 条不进MD / 跳过 2 间硬跳过 |
| [migrate_raw_from_batch05_and_batch07_to_rooms_v1.py](file:///D:/Stock/dealer_assistant/20_tools_workspace/batch_09_rooms_archive_tools/migrate_raw_from_batch05_and_batch07_to_rooms_v1.py) | 中转篮→rooms migrate工具（SHA禁反向覆盖）
| [A5_新仓交接总记录__20260809.md](file:///D:/Stock/dealer_assistant/00_entry/A5_%E6%96%B0%E4%BB%93%E4%BA%A4%E6%8E%A5%E6%80%BB%E8%AE%B0%E5%BD%95__20260809.md) | 每次变动回填 |
