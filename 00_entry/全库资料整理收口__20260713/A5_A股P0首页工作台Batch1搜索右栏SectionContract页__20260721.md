# A5 A股 P0 首页工作台 Batch1 搜索右栏 Section Contract 页

更新时间：2026-07-21

## 一、这页用途

- 本页只做：
  - 冻结 `A股 P0 Batch1` 当前对 `StockSearchBar` 与 `HomeSidebar` section contract 的继续收口口径
  - 说明为什么当前最值钱的一步是把这两块从“半平铺 props”继续收成更稳定的结构
  - 写死本轮允许调整与不允许扩展的边界
- 本页不做：
  - 重开产品方向
  - 重开字段合同
  - 新页面功能
  - 新页面跳转协议

## 二、当前主线与当前不是

- 当前主线：
  - `A股 P0 Batch1` 首页工作台实现线
- 当前不是：
  - `batch_149` 新吸收线
  - 新功能扩展线
  - 多市场与技术栈讨论

## 三、为什么这一手最值钱

- 到当前为止：
  - 页面级 hook 已形成
  - section-level props 已有共享出口
  - `MainWorkspacePanel` 已收成 `viewModel + content + actions`
- 但：
  - `StockSearchBar` 仍直接平铺感知 `searchDraft / searchActionEcho`
  - `HomeSidebar` 仍只停在 `viewModel + onSelectEvent`
- 这意味着首页各 section contract 仍不完全一致，后续维护时容易重新出现“局部例外口径”。

## 四、本轮允许继续收口的范围

- 允许继续收口：
  - `StockSearchBar` props 结构
  - `HomeSidebar` props 结构
  - `homeSectionProps.ts` 中对应 contract
  - `useHomePage.ts` 对这两块的组装方式
- 允许新增：
  - `content / actions` 分组
  - sidebar action contract
- 不允许借机扩展：
  - 新状态字段
  - 新业务逻辑
  - 新功能入口
  - 新数据协议

## 五、当前目标边界

- `StockSearchBar`
  - 继续只服务搜索草稿、打开动作回显与披露入口
  - 不新增真实跳转逻辑
- `HomeSidebar`
  - 继续只服务待处理摘要、最近记录区与披露层
  - 不新增新的交互块
- `useHomePage`
  - 负责把这两块收成更稳定的 section contract

## 六、本轮停止规则

- 满足以下四项即可视为这一小段收口：
  1. `StockSearchBar` 不再平铺接收 `searchDraft / searchActionEcho`
  2. `HomeSidebar` 已明确为 `viewModel + actions` 或等价稳定结构
  3. `npm run build` 通过
  4. `npm run lint` 通过

## 七、下一手

- 先更新：
  - `homeSectionProps.ts`
  - `StockSearchBar.tsx`
  - `HomeSidebar.tsx`
  - `useHomePage.ts`
- 再回填：
  - `README`
  - `Cursor 同步包`
- 若通过，再补一轮轻量回归检查

## 八、后续执行回填

- 当前 `StockSearchBar` 已改为：
  - `viewModel`
  - `content`
  - `actions`
- 当前 `HomeSidebar` 已改为：
  - `viewModel`
  - `actions`
- 当前其含义是：
  - 搜索区不再平铺感知 `searchDraft / searchActionEcho`
  - 右栏点击回流动作被明确收进 action contract
- 当前验证结果：
  - `npm run build` 通过
  - `npm run lint` 通过
- 当前轻量回归结果：
  - 空态通过
  - 选中事件通过
  - 提交记录通过
  - 待处理回流通过
  - 搜索动作回显通过
  - 披露入口滚动通过
- 当前未发现搜索区与右栏 contract 收口后的明显回归
