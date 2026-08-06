# Info Live Room Tools Batch 07

## 用途

- 这里放 `信息直播间` 的最小工具脚本。
- 当前目标是：
  - 自动采集房间列表
  - 生成房间评分卡
  - 对默认置顶房间做“历史记录页”半自动导出与入档草稿

## 当前文件

- `live_info_room_list_extract_v1.js`
  - 自动滚动左侧房间列表并采集房间标题
  - 导出 `info_live_room_list__*.json`

- `build_info_live_room_scorecard_v1.py`
  - 输入：房间列表 JSON
  - 输出：评分卡 tsv + 摘要 md

- `build_info_live_room_review_table_v1.py`
  - 输入：增强后的房间列表 JSON
  - 输出：包含 `房间名 / 最近预览 / 最近时间 / 内容形态提示 / 通知提示` 的复核表 tsv

- `live_info_current_page_export_v1.js`
  - 在已登录且停在目标历史记录页时，对当前页做半自动导出
  - 导出 `info_live_export__*.json`
  - 当前版本：`v1.5`
  - 关键口径：去广告壳抓核心正文；优先房抗混标签；超长粘连卡按时间拆分；`forced_room_anchor` 可强制纠偏
  - 别名：`至尊宝→孙悟空金牌` / `陈子瞻→龙头交易猿`；`天机短线试更新→天机`

- `live_info_incremental_export_v1.js`
  - 增量滚动导出（checkpoint / 去重）
  - 当前版本：`v1.3`（跟随当前页 v1.5；同步优先房 / 漂移降权 / forced_room_anchor）
  - 孙悟空金牌：工作脚本已推到通过条件，活跃 runtime 证据已补吸收

- `live_info_message_card_probe_v1.js`
  - 在目标历史记录页输出：
    - 当前内容根节点
    - 当前可见时间标题
    - 每个时间标题对应的卡片根候选
  - 导出 `info_live_message_card_probe__*.json`

- 房间状态总表：
  - `00_entry/全库资料整理收口__20260713/A5_信息直播间房间状态总表__20260806.md`

- `ingest_info_live_export_v1.py`
  - 把 `info_live_export__*.json` 转成 md 草稿

## 使用顺序（默认）

1. 登录态下打开直播间主页面，跑 `live_info_room_list_extract_v1.js`
2. 用 `build_info_live_room_review_table_v1.py` 先生成“房间复核表”
3. 用 `build_info_live_room_scorecard_v1.py` 生成评分卡
4. 选默认置顶房间，进入对应的历史记录页，跑 `live_info_current_page_export_v1.js`
5. 用 `ingest_info_live_export_v1.py` 把导出 JSON 转成 md 草稿

## 稳定抓取补充顺序（当前）

当发现 `display_date / display_time / topic_anchor / excerpt`
与当前屏幕可见消息不一致时，按下面顺序走：

1. 先在目标历史记录页跑 `live_info_message_card_probe_v1.js`
2. 检查 probe 里：
   - `content_root_path`
   - `visible_time_anchor_count`
   - `time_anchors[].card_path`
3. 再跑 `live_info_current_page_export_v1.js`
4. 只要导出结果仍与当前视口不一致，就继续以 probe 结果收紧脚本主链

## 孙悟空金牌固定复测顺序（当前主线）

目标：

1. 先把新版当前页真值补回活跃 runtime
2. 再复测增量滚动是否真实发生

执行顺序：

1. 进入 `孙悟空金牌` 历史记录页，保持倒序观看
2. 先跑 `live_info_current_page_export_v1.js`
3. 把导出的新版 `info_live_export__*.json` 吸收到：
   - [batch_05 / 孙悟空金牌](file:///d:/Stock/trading_assistant/02_runtime/info_live_room_sampling/batch_05__20260803_20260805_priority_room_history_rerun/00_raw/priority_rooms/孙悟空金牌)
4. 再设置：

```js
window.__infoLiveIncrementalExportV1Options = {
  reset_checkpoint: true,
  start_position: "bottom",
  scroll_direction: "up"
};
```

5. 跑 `live_info_incremental_export_v1.js`
6. 观察两件事：
   - 左侧页面是否真实上滚
   - 导出结果是否继续并入更早消息，而不是只在原地刷日志

当前冻结口径：

- 没有把新版当前页真值吸收到 `batch_05` 之前，不写“runtime 已验收通过”
- `孙悟空金牌` 的正式状态仍是：
  - 脚本已修到位
  - runtime 证据待补
  - 增量未收口
