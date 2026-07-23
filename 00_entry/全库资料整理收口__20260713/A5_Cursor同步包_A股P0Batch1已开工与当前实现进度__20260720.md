# A5 Cursor 同步包 A股 P0 Batch1 已开工与当前实现进度

更新时间：2026-07-23

## 一、这页用途

- 本页只做：
  - 把 `A股 P0 Batch1` 已从“实现前准备”切到“真实代码已开工”的最新进度同步给 `Cursor`
- 本页不做：
  - 重开产品方向
  - 重开 `batch_149` 是否值得继续深挖的旧讨论
  - 重开 `A5` 合同层

## 二、当前三条主线状态

| 主线 | 状态 | 当前口径 |
|---|---|---|
| `主线A：batch_149 终端吸收/映射线` | `已收口，转后台供血/维护态` | 已收成 `6` 张对象卡、字段桥、事件字段总表、页面到六卡的细映射总表；当前主要作为 `Batch1` 的上游真值来源，若未来重开 `方案A` 已冻结为 `F11 联动解释 -> company 高价值页面三分表 -> 极窄公式截图链补洞` |
| `主线B：A股 P0 前台实现线` | `Batch1 已冻结，Batch2 已开工` | 首页工作台最小闭环已冻结为可交付基线；当前继续推进到“标的页 Batch2 最小壳” |
| `主线C：原始源目录保留/删除线` | `暂留` | 当前仍不删源目录，但它已不是继续推进 `Batch1` 的阻塞点 |

## 三、Trae 已经实际推进到哪里

- `batch_149` 侧已完成：
  - `17` 组真实公式样本
  - `6` 张核心对象卡
  - `batch149_formula_semantics_to_batch1_field_bridge_v1.md`
  - `batch149_six_card_event_field_bundle_v1.md`
  - `batch149_page_to_six_card_crossmap_v1.md`
- `A股 P0 Batch1` 侧已完成：
  - 正式开工手令：
    - `A5_A股P0首页工作台Batch1开工手令__20260720.md`
  - 真实前端实现已落地：
    - `20_tools_workspace/a5_p0_home_batch1_frontend/src/pages/Home.tsx`
  - 当前结构已继续拆分为：
    - `fixtures`
    - `hook`
    - `panels`
    - `workspace subcomponents`
    - `hero`
    - `search`
    - `adapter`
  - 当前展示层边界已继续收紧：
    - `EventStreamPanel` 与 `HomeSidebar` 不再直接吃整块领域对象
    - 展示字段先经 `homeViewModel` 适配后再进入组件
    - `HomeHero`、`StockSearchBar`、`MainWorkspacePanel` 标题/空态文案也开始转入展示适配层
    - `SelectedEventSummaryCard` 与 `ExplanationCard` 也开始改为接收 adapter 产出的展示字段
    - `DecisionRecordForm` 的标题、字段标签、placeholder 与按钮文案也开始转入展示适配层
  - 当前 adapter 结构已继续拆分为：
    - `homeViewModel.ts` 仅保留 barrel 出口
    - `homeViewModelTypes.ts` 负责 view model 类型
    - `homeTopSectionViewModel.ts` 负责头部/搜索
    - `homeStreamSidebarViewModel.ts` 负责事件流/右栏
    - `homeWorkspaceViewModel.ts` 负责主工作区
    - `homePageViewModels.ts` 负责首页级 view model 汇总装配
  - 当前页面编排层已继续压薄：
    - `useHomePage.ts` 负责首页页面级装配与披露入口动作
    - `Home.tsx` 更接近纯页面壳
  - 当前页面层 section contract 已继续收口：
    - `useHomePage.ts` 已把事件流、搜索区、主工作区、右栏收成 section-level props object
    - `Home.tsx` 不再一项项散传这些字段
  - 当前 section contract 又继续压实为共享出口：
    - `homeSectionProps.ts` 统一页面 hook 与 section 组件的 props 类型
    - `MainWorkspacePanel` 已改为 `viewModel + content + actions`
    - `StockSearchBar` 已改为 `viewModel + content + actions`
    - `HomeSidebar` 已改为 `viewModel + actions`
  - 当前搜索区与右栏 contract 收口后已补做轻量浏览器回归：
    - 空态 / 选中态 / 提交 / 待处理回流 / 搜索动作 / 披露入口滚动未见回归
  - 当前已吸收 `Cursor` 最新实现向审校结论并完成最小护栏：
    - 不再把 `EventStreamPanel` contract 美化作为下一优先
    - 已把切事件状态迁移下沉成 `workspaceModel.ts` 内的 `applySelectEvent(...)` 纯函数
    - 已补 `workspaceModel.test.ts`，锁住切事件后草稿重建、回显清空、表单错误清空与 `selectedEventId` 更新
  - 当前又继续补齐提交路径最小护栏：
    - 已为 `buildSubmitDecisionResult(...)` 补纯模型测试
    - 已锁住无选中事件报错、字段未补全报错并进入 `editing`
    - 已锁住提交成功后生成 `record` / `submitEcho` 并把对应事件标记为 `done`
    - 已为 `getWorkspaceStateAfterRetry(...)` 补纯模型测试，锁住重试后回到 `editing / empty`
  - 当前又继续补齐辅助纯模型护栏：
    - 已为 `applyDecisionDraftChange(...)` 补纯模型测试，锁住草稿字段更新与 `selectedEventId` 对齐
    - 已为 `buildSearchActionEcho(...)` 补纯模型测试，锁住空输入失败与有效输入成功提示
  - 当前又继续补齐最小 hook 护栏：
    - 已新增 `useHomeWorkspace.test.tsx`
    - 已锁住失败提交进入 `editing` 并写入 `formError`
    - 已锁住成功提交后生成回显与记录
    - 已锁住点击重试后清空回显并回到 `editing`
    - 已锁住成功提交后再切事件会重建草稿并清空回显
  - 当前又继续补齐最小 page-hook 护栏：
    - 已新增 `useHomePage.test.tsx`
    - 已锁住 section props actions 引用一致（指向 workspace handlers）
    - 已锁住选中事件后 `eventStreamPanelProps.selectedEventId` 与主工作区 view model 更新
    - 已锁住 `handleOpenFinanceDisclosure` 能触发 `finance-disclosure-note.scrollIntoView`
  - 当前护栏补齐后已完成命令验证：
    - `npm run test`
  - `npm run lint`
  - `npm run build`
- 当前已完成桌面端第三轮最小走查：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch1桌面端第三轮走查记录__20260722.md`
  - 当前已补齐异步数据源桩（API 层）：
    - 新增 `src/features/home/api/homeApi.ts`
    - 新增 `src/features/home/api/mock/homeBootstrapMock.ts`
    - `useHomeWorkspace` 不再直接引用样本数据初始化事件/记录，而是异步加载 `fetchHomeBootstrap()`
    - 当前 mock 与 API 已完成分离，后续若接真实端，替换点只留在 `homeApi.ts`
  - 当前已把停点冻结为“可交付基线”并落盘：
    - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1可交付基线冻结页__20260722.md`
  - 当前 `Batch2` 已真实开工：
    - 新增 `src/pages/Stock.tsx`
    - 新增 `src/features/stock/adapters/stockPageViewModel.ts`
    - 新增 `src/features/stock/hooks/useStockPage.ts`
    - 新增路由 `/stock/:stockCode`
    - 首页有效标的动作已从“只回显打开动作”推进到“进入标的页最小壳”
  - 当前 `Batch2` 最小壳已具备：
    - 页头摘要区
    - 相关事件区
    - 当前解释区
    - 最近决策记录区
    - 问答下钻入口区（禁用输入占位 + 禁用按钮）
  - 当前 `Batch2` 又继续补到：
    - 最近记录区不再只是只读展示
    - 命中已有记录的事件时，可出现 `补充这次记录`
    - 可在原地填写最小补充备注
    - 空备注提交会失败提示且不清草稿
    - 成功提交后会生成最近一次补充回显
  - 当前已新增 `useStockPage.test.tsx`
    - 锁住默认选中首条相关事件
    - 锁住切换相关事件后解释区更新
    - 锁住已有记录事件的补充入口可达
    - 锁住空备注提交失败
    - 锁住成功提交后补充回显生成
  - 当前命令验证继续全绿：
    - `npm run test`
    - `npm run lint`
    - `npm run build`
  - 当前 `Batch2` 最小壳正式页已落盘：
    - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2最小壳页__20260722.md`
  - 当前 `Batch2` 补充记录入口壳页已落盘：
    - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2补充记录入口壳页__20260722.md`
  - 当前 `Batch2` 又继续把问答入口推进成真实可进入的占位页：
    - 新增 `src/features/stock/hooks/useStockQaPage.ts`
    - 新增 `src/features/stock/hooks/useStockQaPage.test.tsx`
    - 新增 `src/pages/StockQa.tsx`
    - 新增路由 `/stock/:stockCode/qa`
    - 标的页进入问答页时会保留 `eventId`
    - 问答页返回标的页时会保留 `stockCode + selectedEventId`
  - 当前问答下钻占位页已具备：
    - 上下文条（标的 / 当前事件 / `still_need_evidence`）
    - 推荐问题区
    - 五段式占位回答
    - 返回标的页入口
    - 按问题类型切换字段重点的回答分发
  - 当前 `Stock.tsx` 的问答入口文案也已对齐当前能力：
    - 不再展示禁用输入框
    - 改为“先看推荐问题”的能力说明
    - CTA 已改成 `查看推荐问答`
  - 当前 `useStockQaPage.test.tsx` 已锁住：
    - 按 query 中的事件进入问答上下文
    - 切换推荐问题时占位回答更新
    - 不同问题命中不同字段重点
  - 当前问答下钻占位页桌面端走查已通过：
    - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch2问答下钻占位页走查记录__20260723.md`
  - 当前 `Batch2` 又继续把问答页压到结果样式层：
    - 推荐问题已收成 `解释补充组 / 记录复盘组 / 下一步关注组`
    - 结果区已收成 `问题条 / 事件与字段来源条 / 核心回答区 / 下一步动作条 / 金融限制提醒条`
    - `useStockQaPage.ts` 已从平铺 block 改成稳定 view model
    - `StockQa.tsx` 已按五段式结果结构消费
  - 当前问答结果样式层正式页与走查已落盘：
    - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2问答结果样式层页__20260723.md`
    - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch2问答结果样式层走查记录__20260723.md`
  - 当前 `Batch2` 又继续把返回链压到：
    - `Home -> Stock -> QA -> Stock -> Home` 回到首页后不再掉回空态
    - `Home` 已支持按 `eventId` 初始化最近事件上下文
    - `Stock` 返回首页时会带回当前事件 `eventId`
    - `useHomeWorkspace.test.tsx / useHomePage.test.tsx / useStockPage.test.tsx` 已补这一刀的最小护栏
  - 当前首页返回链正式页与走查已落盘：
    - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2首页返回链保留事件上下文页__20260723.md`
    - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch2首页返回链保留事件上下文走查记录__20260723.md`
  - 当前 `Batch2` 又继续把首页恢复能力压到：
    - 首页已选事件时，打开标的页会带当前 `eventId`
    - 直接打开 `/?eventId=...` 时，首页可恢复对应事件工作区
    - 浏览器刷新后，首页仍保留同一事件上下文
  - 当前 `Batch2` 又继续把首页恢复失败口径压到：
    - `/?eventId=` 时，首页会显式降级为空态并提示
    - `/?eventId=<unknown>` 时，首页会显式降级为空态并提示
    - 不再静默 `return`
  - 当前首页 query 直达与刷新恢复正式页与走查已落盘：
    - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2首页query直达与刷新恢复页__20260723.md`
    - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch2首页query直达与刷新恢复走查记录__20260723.md`
  - 当前首页无效 eventId 降级正式页与走查已落盘：
    - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2首页无效eventId降级页__20260723.md`
    - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch2首页无效eventId降级走查记录__20260723.md`
  - 当前 `Batch2` 已完成桌面端最小走查并冻结停点：
    - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch2标的页桌面端最小走查记录__20260722.md`
    - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2停点冻结页__20260722.md`
  - 当前主工作区 section contract 收口后已补做轻量浏览器回归：
    - 空态 / 选中态 / 提交 / 切事件重置 / 待处理回流 / 搜索动作未见回归
  - 当前组件入参收口后已补做轻量浏览器回归：
    - 空态 / 选中态 / 提交 / 切事件重置 / 待处理回流 / 搜索动作未见回归
  - 当前页面编排层压薄后已补做轻量浏览器回归：
    - 空态 / 选中态 / 提交 / 切事件重置 / 搜索动作未见回归
  - 当前页面已具备最小闭环：
    - `今日事件流`
    - `主工作区`
    - `解释卡`
    - `决策记录草稿`
    - `提交回显`
    - `待处理摘要`
    - `最近记录区`
  - 当前构建已通过：
    - `npm run build`
  - 当前本地预览已可打开：
    - `http://localhost:5173/`
  - 当前桌面端首轮最小走查已通过：
    - `A5_A股P0_Batch1桌面端首轮走查记录__20260720.md`
  - 当前桌面端第二轮最小走查已通过：
    - `A5_A股P0_Batch1桌面端第二轮走查记录__20260721.md`

## 四、当前已写死的实现口径

- 首页唯一主轴仍是：
  - `今日事件流`
- 实现侧当前只认以下上游真值：
  1. `A5_A股P0首页工作台Batch1实现映射页__20260719.md`
  2. `A5_A股P0首页事件卡模板与事件摘要字段层__20260719.md`
  3. `batch149_formula_semantics_to_batch1_field_bridge_v1.md`
  4. `batch149_six_card_event_field_bundle_v1.md`
  5. `A5_A股P0首页工作台Batch1开工手令__20260720.md`
- 已写死实现不变量：
  - 切事件时必须重置 `homeRecordDraft`
  - 切事件时必须清空 `latestSubmitEcho`
- 已补最小自动化护栏：
  - `applySelectEvent(...)` 纯函数负责收口切事件状态迁移
  - `workspaceModel.test.ts` 已锁住切事件不变量最小断言
  - `buildSubmitDecisionResult(...)` 已锁住提交路径最小成功 / 失败分支
  - `getWorkspaceStateAfterRetry(...)` 已锁住重试回退状态最小断言
  - `applyDecisionDraftChange(...)` 与 `buildSearchActionEcho(...)` 已锁住辅助纯模型最小断言
  - `useHomeWorkspace.test.tsx` 已锁住 hook 层最短真实状态串接
  - `useHomePage.test.tsx` 已锁住编排层 section props 的最小一致性

## 五、当前我希望 Cursor 明确不要重开的内容

- 不重开：
  - `A股 P0` 产品方向
  - `A5` 合同补页
  - `batch_149` 是否继续补源码
  - 多市场
  - 新证据类型
  - 本地 AI 技术栈
- 不把：
  - 页面载体
  - `.sp`
  - `.tn6`
  误当成当前实现线的新增输入真值
- 若必须提到 `batch_149`，只允许按当前冻结口径引用：
  - 它是后台维护态供血线
  - 不是前台默认当前刀
  - 其 `方案A` 补采顺序已由 `A5_batch149方案A最终补采优先级与停止规则页__20260723.md` 写死

## 六、这轮 Cursor 审校已被吸收后的当前停点

- `Cursor` 本轮已明确：
  - `可继续推进`
  - 无硬阻塞
  - 当前最值钱的是切事件不变量测试护栏，而不是继续美化 section contract
- `Trae` 已按此落地并验证通过：
  - `applySelectEvent(...)`
  - `workspaceModel.test.ts`
  - `npm run build`
  - `npm run lint`
  - `npm run test`
- 当前进一步吸收实现向核验后的主负责人裁决：
  - 已继续补齐提交路径最小护栏
  - 已顺手锁住重试回退的最小状态切换
  - 已继续补齐草稿修改与搜索动作两条辅助纯模型护栏
  - 已继续补齐 `useHomeWorkspace` 最小 hook 护栏
  - 已继续补齐 `useHomePage` 最小 page-hook 护栏
  - 当前先把 `Batch1` 正式停在模型/WorkspaceHook/PageHook 三层稳定点 + 异步数据源桩
- 当前继续把前台主线推进到：
  - `Batch2 标的页最小壳 + 问答下钻占位页 + 问答结果样式层 + 首页返回链保留最近事件上下文 + 首页query直达与刷新恢复 + 首页无效/空eventId显式降级（已完成桌面端走查并冻结）`
- 当前前台主线停在：
  - `Batch1 首页薄壳 + workspace 不变量 + section props + adapter 分层 + 模型/WorkspaceHook/PageHook 三层最小自动化护栏 + 异步数据源桩`
  - `Batch2 标的页五段最小壳 + 首页真实跳转 + 同页切事件更新解释/记录 + 最近记录补充入口壳 + 问答下钻占位页 + 问答结果样式层 + 标的页/问答页返回链 + 首页返回链保留最近事件上下文 + 首页query直达与刷新恢复 + 首页无效/空eventId显式降级`
- 当前明确暂缓：
  - `latestSubmitEcho` 重试链路全覆盖
  - `EventStreamPanel` contract 统一化
  - 新一轮 adapter / section 美化

## 七、若下一轮还需要 Cursor，只允许看的唯一问题

- 不是请 `Cursor` 再判断：
  - 要不要开工
  - 方向对不对
  - 字段合同是否要重写
- 而是请 `Cursor` 只做一轮实现向审校，并回答：
  - 当前这版 `Home.tsx + useHomeWorkspace + useHomePage + fixtures/panels/workspace/hero/search/sidebar + adapter + homeSectionProps` 的实现结构，是否已经满足继续推进条件
  - 如果没有，请只指出：
    - `硬阻塞`
    - `高风险回归点`
    - `最值得立刻拆出的下一层结构`
    - `是否应该把 EventStreamPanel 也继续统一成更稳定的 section contract`

## 八、建议 Cursor 阅读顺序

1. `A5_A股P0首页工作台Batch1开工手令__20260720.md`
2. `10_source_library_archive/batch_149_tdx_custom_terminal_external_folder_absorb__20260719/03_quantize/batch149_six_card_event_field_bundle_v1.md`
3. `10_source_library_archive/batch_149_tdx_custom_terminal_external_folder_absorb__20260719/03_quantize/batch149_page_to_six_card_crossmap_v1.md`
4. `20_tools_workspace/a5_p0_home_batch1_frontend/src/pages/Home.tsx`
5. `20_tools_workspace/a5_p0_home_batch1_frontend/src/features/home/hooks/useHomeWorkspace.ts`
6. `20_tools_workspace/a5_p0_home_batch1_frontend/src/features/home/model/workspaceModel.ts`
7. `20_tools_workspace/a5_p0_home_batch1_frontend/src/features/home/model/workspaceModel.test.ts`
8. `20_tools_workspace/a5_p0_home_batch1_frontend/src/features/home/hooks/useHomePage.ts`
9. `20_tools_workspace/a5_p0_home_batch1_frontend/src/features/home/contracts/homeSectionProps.ts`
10. `20_tools_workspace/a5_p0_home_batch1_frontend/src/features/home/fixtures/sixCardEvents.ts`
11. `20_tools_workspace/a5_p0_home_batch1_frontend/src/features/home/components/`
12. `20_tools_workspace/a5_p0_home_batch1_frontend/src/features/home/adapters/homeViewModel.ts`

## 九、输出合同

- 若下一轮仍请求 `Cursor` 审校，继续只按下面结构回答：
  1. `结论`
  2. `发现的硬阻塞 / 高风险点`
  3. `当前实现中最该马上拆出的结构`
  4. `EventStreamPanel` 是否建议继续做 contract 收口`
  5. `如果继续推进，唯一下一手是什么`
- 若无硬阻塞，仍要求明确写：
  - `可继续推进`

## 十、一句话同步口径

- 当前最准确的一句话是：
  - `Trae` 已把 `batch_149` 吸收线收成 `Batch1` 可消费字段真值，并已把 `A股 P0 Batch1` 首页工作台最小闭环落进真实前端代码；当前已把纯模型层、workspace hook 串接层与 page hook 编排层都补上最小自动化护栏，并先把 Batch1 正式停在当前稳定点。`
