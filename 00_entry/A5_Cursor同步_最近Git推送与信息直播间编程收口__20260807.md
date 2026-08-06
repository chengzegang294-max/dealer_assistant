# A5 Cursor同步 最近Git推送与信息直播间编程收口

更新时间：2026-08-07

## 这页用途

- 给 `Cursor` 一页可直接接手的同步说明。
- 说明最近几轮里：
  - 哪些已经推上 GitHub
  - 哪些临时目录已经可以退场
  - clean 工作线当前该从哪里继续

## 当前结论

### 1. 远端主线已经打通并切到 `master`

- 新远端：
  - `https://github.com/chengzegang294-max/trading_assistant.git`
- 远端默认分支：
  - `master`

### 2. clean 线当前远端头已经前进到

- `8588a5d4`
- 提交主题：
  - `feat(info-live): harden core text capture and close 龙头 spot-check`

### 3. 原工作仓最新明确结果已完成吸收

原工作仓：

- `d:\Stock\trading_assistant`

其中 `Cursor` 主推、且结果已明确的那颗提交：

- `e86dade5`
- 提交主题：
  - `feat(info-live): harden core text capture and close 龙头 spot-check`

已经吸收到 clean 线并推上远端。

## 这几次 Cursor 主要推进了什么

最近这几轮，`Cursor` 主要推动的是信息直播间抓取链路的编程内容，而不是仓库治理文书。

本轮明确归因到 `Cursor` 主推的代码向收口，至少包括：

1. `live_info_current_page_export_v1.js`
   - 强化正文抓取
   - 加入 priority room / drift anchor 纠偏
   - 去广告壳、超长粘连卡拆分
2. `live_info_incremental_export_v1.js`
   - 跟随当前页逻辑同步 alias / forced room / priority room 口径
3. `20_tools_workspace/batch_07_info_live_room_tools/README.md`
   - 工具使用说明同步更新
4. `龙头交易猿` 抽检收口
   - 新增导出 JSON
   - 新增增量导出 JSON
5. 配套状态页回填
   - 房间状态总表
   - 阶段 A 抽检执行页
   - 文字抓取与核心留存优化页

## 当前分线状态

### A. 原工作仓

路径：

- `d:\Stock\trading_assistant`

特征：

- 仍保留旧历史上下文
- 适合回看最初治理和迁移过程
- 不再建议作为最终 Git 主工作线继续推进

### B. clean 工作线

路径：

- `d:\ta`

特征：

- 基于已经瘦身并成功推送的历史
- 当前是最适合继续作为 Git 主工作线的目录
- 已经成功推到：
  - `origin/master`
- 当前还剩入口层少量待提交文档，主要是：
  - `00_entry/README.md`
  - `00_entry/A5_GitHub推送失败_大文件历史清理与新远程推送方案__20260807.md`
  - 本页同步稿

## 临时目录去留口径

### 应继续保留

1. `d:\ta`
   - 文件类型：`WORKING`
   - 原因：当前 clean 主工作线
   - 是否允许放根目录：`yes`
   - 是否需要后续迁移：`no`

### 已可删除 / 正在退场

1. `d:\Stock\trading_assistant_clean`
   - 文件类型：`TEMPORARY`
   - 原因：早期 clean clone 尝试，已被 `d:\ta` 替代
   - 是否允许放根目录：`no`
   - 是否需要后续迁移：`no`

2. `d:\Stock\trading_assistant_push_stage`
   - 文件类型：`TEMPORARY`
   - 原因：早期 staging clone 尝试，且曾因长路径失败
   - 是否允许放根目录：`no`
   - 是否需要后续迁移：`no`

3. `d:\Stock\trading_assistant_push_mirror.git`
   - 文件类型：`TEMPORARY`
   - 原因：历史瘦身中转镜像
   - 是否允许放根目录：`no`
   - 是否需要后续迁移：`no`

4. `d:\Stock\trading_assistant__ce10da4e.patch`
   - 文件类型：`TEMPORARY`
   - 原因：迁移中间产物
   - 是否允许放根目录：`no`
   - 是否需要后续迁移：`no`

5. `d:\Stock\trading_assistant__working_readme.patch`
   - 文件类型：`TEMPORARY`
   - 原因：迁移中间产物
   - 是否允许放根目录：`no`
   - 是否需要后续迁移：`no`

## Cursor 下一手最值得做什么

如果 `Cursor` 还有额度，而且要继续优先投到编程相关内容，建议顺序如下：

1. 在 `d:\ta` 上继续做信息直播间主线，不再回到旧仓发散
2. 优先围绕活跃脚本和活跃 runtime 证据继续推进：
   - `20_tools_workspace/batch_07_info_live_room_tools/`
   - `02_runtime/info_live_room_sampling/`
3. 新增正式结论时，优先回填：
   - 房间状态总表
   - 阶段 A 执行页
   - `00_entry/README.md`

## 主负责人裁决

当前选：

- 继续以 `d:\ta` 作为 clean 主工作线
- 已把 `Cursor` 主推、结果明确的代码与证据吸收进远端 `master`
- 后续继续清理中转目录，不长期保留

当前不选：

- 回到旧仓继续把它当最终 Git 主仓
- 让 `trading_assistant_push_mirror.git` 之类中间目录长期留下
- 在 clean 线之外再维持第二套命名体系
