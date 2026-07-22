# A5 A股 P0 Batch2 首页无效 eventId 降级走查记录

更新时间：2026-07-23

## 一、走查范围

- 只验证首页恢复链最后一刀：
  - `/?eventId=`
  - `/?eventId=unknown-event-id`
  - `/?eventId=market-index-context-20260720`

## 二、走查结果

### 1. 空 `eventId`

- 访问：
  - `/?eventId=`
- 结果：
  - 首页保留默认空态
  - 搜索区出现提示：
    - `检测到空 eventId，当前已按首页默认空态降级展示。`
  - 主工作区标题仍为：
    - `先从左侧选一条今日事件`

### 2. 无效 `eventId`

- 访问：
  - `/?eventId=unknown-event-id`
- 结果：
  - 首页保留默认空态
  - 搜索区出现提示：
    - `未找到 eventId=unknown-event-id 对应的首页事件，当前已回到默认空态。`
  - 主工作区标题仍为：
    - `先从左侧选一条今日事件`

### 3. 有效 `eventId`

- 访问：
  - `/?eventId=market-index-context-20260720`
- 结果：
  - 首页成功恢复到对应事件工作区
  - 主工作区标题为：
    - `指数环境强弱发生变化`
  - 解释卡文案正常展示

## 三、结论

- 本轮走查通过。
- `Batch2` 首页恢复链最后一个硬缺口已收口：
  - 空值会降级
  - 无效值会降级
  - 有效值会恢复
