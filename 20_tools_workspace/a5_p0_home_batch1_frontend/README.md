# A股 P0 首页工作台 / 标的页 前端

## 用途

- 这是 `A股 P0` 前台实现工作区。
- 当前已实现：
  - `Batch1` 首页工作台最小闭环
  - `Batch2` 标的页最小壳
  - `Batch2` 问答下钻占位页
  - `Batch2` 问答结果样式层
- 当前首页闭环包括：
  - `今日事件流`
  - `解释卡`
  - `决策记录草稿`
  - `提交回显`
  - `待处理摘要`
  - `最近记录区`

## 当前口径

- 首页唯一主轴仍是：
  - `今日事件流`
- 当前实现只认以下上游真值：
  - `A5_A股P0首页工作台Batch1实现映射页__20260719.md`
  - `A5_A股P0首页事件卡模板与事件摘要字段层__20260719.md`
  - `batch149_formula_semantics_to_batch1_field_bridge_v1.md`
  - `batch149_six_card_event_field_bundle_v1.md`
  - `A5_A股P0首页工作台Batch1开工手令__20260720.md`

## 当前已实现

- 首页状态：
  - `selectedEventId`
  - `homeWorkspaceState`
  - `homeRecordDraft`
  - `latestSubmitEcho`
  - `searchDraft`
- 关键交互：
  - 事件流选中
  - 解释卡加载
  - 决策草稿编辑
  - 提交成功回显
  - 待处理摘要回流
  - 搜索打开动作回显
- 已写死实现不变量：
  - 切事件时强制重置 `homeRecordDraft`
  - 切事件时清空 `latestSubmitEcho`
- 已补最小自动化护栏：
  - `applySelectEvent(...)` 下沉到 `workspaceModel.ts`
  - `workspaceModel.test.ts` 锁住切事件重建草稿、清空回显/表单错误、更新选中事件
  - `buildSubmitDecisionResult(...)` 已补最小成功 / 失败分支测试，锁住提交报错、进入 `editing`、生成记录与回显、事件置 `done`
  - `getWorkspaceStateAfterRetry(...)` 已补最小状态回退测试，锁住重试后回到 `editing / empty`
  - `applyDecisionDraftChange(...)` 已补最小测试，锁住草稿字段更新与 `selectedEventId` 对齐
  - `buildSearchActionEcho(...)` 已补最小测试，锁住空输入失败与有效输入成功提示
  - `useHomeWorkspace.test.tsx` 已补最小 hook 测试，锁住失败提交、成功提交、重试回退与切事件清空回显的真实串接
  - `useHomePage.test.tsx` 已补最小编排层测试，锁住 section props 绑定一致、选中事件后 props 更新、财务披露滚动动作

## 当前结构

- `src/features/home/fixtures/sixCardEvents.ts`
  - 首页披露文案与摘要常量
- `src/features/home/api/homeApi.ts`
  - 异步数据源桩入口，当前只负责从 `api/mock` 取 bootstrap payload
- `src/features/home/api/mock/homeBootstrapMock.ts`
  - Batch1 独立 mock 载荷，承接事件与记录样本；后续替换真实数据时只改 API 层
- `src/features/home/hooks/useHomeWorkspace.ts`
  - 首页状态机与关键不变量
- `src/features/home/hooks/useHomePage.ts`
  - 首页页面级装配 hook，负责消费 workspace、生成 view model 并挂接页面级动作/标的页跳转
- `src/features/stock/adapters/stockPageViewModel.ts`
  - 标的页最小壳 view model 装配
- `src/features/stock/hooks/useStockPage.ts`
  - 标的页最小状态与相关事件/解释/记录切换，以及补充记录入口壳
- `src/features/stock/hooks/useStockQaPage.ts`
  - 问答下钻占位页状态，负责三组推荐问题、五段式结果 view model 与返回标的页回链
- `src/features/home/contracts/homeSectionProps.ts`
  - 首页 section-level props 共享 contract，统一页面 hook 与 section 组件的入参出口
- `src/features/home/components/EventStreamPanel.tsx`
  - 左栏今日事件流
- `src/features/home/components/MainWorkspacePanel.tsx`
  - 中栏主工作区编排层
- `src/features/home/components/workspace/`
  - 主工作区内部子组件：选中事件摘要、解释卡、决策草稿表单、提交回显
- `src/features/home/components/HomeSidebar.tsx`
  - 右栏待处理摘要、最近记录区、金融披露层
- `src/features/home/components/HomeHero.tsx`
  - 顶部标题区与三张状态指标卡
- `src/features/home/components/StockSearchBar.tsx`
  - 搜索输入、打开动作回显、金融限制入口
- `src/features/home/adapters/homeViewModel.ts`
  - adapter barrel 出口，维持页面与组件层稳定导入路径
- `src/features/home/adapters/homeViewModelTypes.ts`
  - 首页 view model 类型定义
- `src/features/home/adapters/homeTopSectionViewModel.ts`
  - 头部标题/指标、搜索条等顶部区域 adapter
- `src/features/home/adapters/homeStreamSidebarViewModel.ts`
  - 事件流卡片、右栏摘要卡片与披露层 adapter
- `src/features/home/adapters/homeWorkspaceViewModel.ts`
  - 主工作区标题空态、选中事件摘要、解释卡、表单展示文案等 adapter
- `src/features/home/adapters/homePageViewModels.ts`
  - 首页级 view model 汇总入口，供 `Home.tsx` 统一消费
- `src/features/home/model/workspaceModel.ts`
  - 事件切换、草稿修改、提交结果、搜索动作回显等纯状态转换模型
- `src/features/home/model/workspaceModel.test.ts`
  - 切事件不变量的最小自动化测试
- `src/pages/Home.tsx`
  - 页面编排层，只负责把三栏和头部拼起来
- `src/pages/Stock.tsx`
  - `Batch2` 标的页最小壳，承接首页真实跳转
- `src/pages/StockQa.tsx`
  - `Batch2` 问答下钻占位页，承接推荐问题与五段式占位回答展示

## 当前不做

- 标的页深挖实现
- 问答页深挖实现
- 新数据协议
- 多市场扩展
- 自动交易动作

## 运行

```bash
npm install
npm run dev
```

## 构建

```bash
npm run build
```

## 测试

```bash
npm run test
```

## 说明

- 当前页面中的事件与解释数据仍是实现态样本，但字段来源已经对齐 `batch_149` 六卡字段层。
- 当前展示边界继续收紧的正式页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1展示边界继续收紧页__20260721.md`
- 当前表单展示边界继续收紧的正式页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1表单展示边界继续收紧页__20260721.md`
- 当前适配层拆分页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1适配层拆分页__20260721.md`
- 当前页面编排层压薄页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1页面编排层压薄页__20260721.md`
- 当前组件入参收口页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1组件入参收口页__20260721.md`
- 当前主工作区 section contract 页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1主工作区SectionContract页__20260721.md`
- 当前搜索右栏 section contract 页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1搜索右栏SectionContract页__20260721.md`
- 当前主工作区里“选中事件摘要/解释卡”也开始优先接收 adapter 产出的展示字段，而不是直接吃整块领域对象。
- 当前 `DecisionRecordForm` 的标题、描述、字段标签、placeholder、按钮文案也开始优先接收 adapter 产出的展示字段。
- 当前 adapter 已按顶部区、事件流/右栏、主工作区三块拆分，避免 `homeViewModel.ts` 重新长成单文件中心。
- 当前 `Home.tsx` 里的 view model 组装也已收成单入口，页面编排层继续只保留状态接线与布局拼装。
- 当前 `Home.tsx` 已继续通过 `useHomePage` 收走页面级装配与披露入口动作，进一步接近纯页面壳。
- 当前 `useHomePage` 已继续把事件流、搜索区、主工作区、右栏收成 section-level props object，`Home.tsx` 不再一项项散传这些字段。
- 当前 section-level props 已进一步抽成共享 contract；其中 `MainWorkspacePanel` 已改为 `viewModel + content + actions`，不再平铺接收整串字段。
- 当前 `StockSearchBar` 也已改为 `viewModel + content + actions`，`HomeSidebar` 已改为 `viewModel + actions`，首页几块大 section 的 contract 更一致。
- 当前页面编排层压薄后，已补做一轮轻量浏览器回归，空态/选中态/提交/切事件重置/搜索动作未见回归。
- 当前组件入参收口后，也已补做一轮轻量浏览器回归，空态/选中态/提交/切事件重置/待处理回流/搜索动作未见回归。
- 当前主工作区 section contract 收口后，也已补做一轮轻量浏览器回归，空态/选中态/提交/切事件重置/待处理回流/搜索动作未见回归。
- 当前搜索区与右栏 section contract 收口后，也已补做一轮轻量浏览器回归，空态/选中态/提交/待处理回流/搜索动作/披露入口滚动未见回归。
- 当前已按 `Cursor` 审校结论把切事件状态迁移下沉为 `applySelectEvent(...)` 纯函数，并补了最小自动化护栏：
  - `selectedEventId` 更新
  - `homeWorkspaceState` 进入 `selected`
  - `homeRecordDraft` 被重建
  - `latestSubmitEcho` 被清空
  - `formError` 被清空
- 当前切事件不变量护栏页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1切事件不变量测试护栏页__20260721.md`
- 当前这轮护栏补齐后，`npm run build`、`npm run lint`、`npm run test` 已通过。
- 当前 `Batch1` 这一段先正式停在：
  - `首页薄壳 + workspace 不变量 + section props + adapter 分层 + 模型/WorkspaceHook/PageHook 三层最小自动化护栏 + 异步数据源桩`
- 当前 `Batch2` 已推进到：
  - `标的页五段最小壳 + 首页真实跳转 + 同页切事件更新解释/记录 + 最近记录补充入口壳 + 问答下钻占位页 + 问答结果样式层`
- 当前标的页 Batch2 最小壳页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2最小壳页__20260722.md`
- 当前 Batch2 补充记录入口壳页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2补充记录入口壳页__20260722.md`
- 当前 Batch2 桌面端最小走查记录见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch2标的页桌面端最小走查记录__20260722.md`
- 当前 Batch2 停点冻结页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2停点冻结页__20260722.md`
- 当前 Batch2 问答下钻占位页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2问答下钻占位页__20260722.md`
- 当前 Batch2 问答下钻走查记录见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch2问答下钻占位页走查记录__20260723.md`
- 当前 Batch2 问答结果样式层页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0标的页Batch2问答结果样式层页__20260723.md`
- 当前 Batch2 问答结果样式层走查记录见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch2问答结果样式层走查记录__20260723.md`
- 当前可交付基线冻结页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1可交付基线冻结页__20260722.md`
- 当前提交路径最小护栏页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1提交路径最小护栏页__20260722.md`
- 当前辅助纯模型护栏页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1辅助纯模型护栏页__20260722.md`
- 当前最小 hook 护栏页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1最小Hook护栏页__20260722.md`
- 当前最小 page-hook 护栏页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1最小PageHook护栏页__20260722.md`
- 当前桌面端第三轮走查记录见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch1桌面端第三轮走查记录__20260722.md`
- 当前异步数据源桩页见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1异步数据源桩页__20260722.md`
- 当前 mock/API 分离已完成：
  - 事件与记录样本已从 `fixtures` 迁入 `api/mock/homeBootstrapMock.ts`
  - `homeApi.ts` 成为唯一替换点
- 当前测试已扩成：
  - `workspaceModel.test.ts` + `useHomeWorkspace.test.tsx` + `useHomePage.test.tsx` + `useStockPage.test.tsx` + `useStockQaPage.test.tsx`
  - 共 `5` 个测试文件、`25` 个测试用例，均已通过
- 当前明确暂缓：
  - `latestSubmitEcho` 重试链路全覆盖
  - `EventStreamPanel` contract 统一化
  - 新一轮 adapter / section 美化
- 后续若字段需要继续收紧，优先回指 `batch149_six_card_event_field_bundle_v1.md`，不要重开新合同页。
- 当前首页有效标的动作已进入真实标的页最小壳；问答下钻已推进到真实占位页，当前只开放三组推荐问题、五段式结果与下一步动作条，不开放自由输入。
- 当前最近记录区已不再只是只读展示；当事件命中已有记录时，可原地进入“补充这次记录”最小入口壳，提交后本地回显最近一次补充备注。
- 当前桌面端首轮走查已通过，见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch1桌面端首轮走查记录__20260720.md`
- 当前桌面端第二轮走查也已通过，见：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0_Batch1桌面端第二轮走查记录__20260721.md`
