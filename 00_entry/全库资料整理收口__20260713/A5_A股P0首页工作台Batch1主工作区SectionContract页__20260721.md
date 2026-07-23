# A5 A股 P0 首页工作台 Batch1 主工作区 Section Contract 页

更新时间：2026-07-21

## 一、这页用途

- 本页只做：
  - 冻结 `A股 P0 Batch1` 当前对 `MainWorkspacePanel` section contract 的继续收口口径
  - 说明为什么当前最值钱的一步是把主工作区从“平铺一串字段”收成更稳定的 `content + actions` 结构
  - 写死本轮允许调整与不允许扩展的边界
- 本页不做：
  - 重开产品方向
  - 重开字段合同
  - 新交互功能
  - 新页面跳转

## 二、当前主线与当前不是

- 当前主线：
  - `A股 P0 Batch1` 首页工作台实现线
- 当前不是：
  - `batch_149` 新吸收线
  - 功能扩展线
  - 多市场与技术栈讨论

## 三、为什么这一手最值钱

- 到当前为止，页面层已经把：
  - 事件流
  - 搜索区
  - 主工作区
  - 右栏
  收成了 section-level props object。
- 但 `MainWorkspacePanel` 内部仍直接感知：
  - `selectedEventSummaryViewModel`
  - `explanationCardViewModel`
  - `decisionRecordFormViewModel`
  - `homeRecordDraft`
  - `latestSubmitEcho`
  - `formError`
  - 多个提交与编辑动作
- 这让主工作区 contract 仍偏平铺，不利于后续长期维持稳定边界。

## 四、本轮允许继续收口的范围

- 允许继续收口：
  - `MainWorkspacePanel` props 结构
  - 首页 section props 共享类型出口
  - `useHomePage` 对主工作区 section props 的组装方式
- 允许新增：
  - section props 共享类型文件
  - `content / actions` 分组结构
- 不允许借机扩展：
  - 新状态字段
  - 新业务逻辑
  - 新功能入口
  - 新协议页

## 五、当前目标边界

- `MainWorkspacePanel`
  - 继续只吃 section contract
  - 不重新理解状态机
- `useHomePage`
  - 负责组装主工作区 `content + actions`
- `DecisionRecordForm`
  - 继续只服务当前事件的记录表单，不改变提交语义

## 六、本轮停止规则

- 满足以下四项即可视为这一小段收口：
  1. `MainWorkspacePanel` 不再平铺接收大串字段
  2. section props 共享类型已抽成稳定出口
  3. `npm run build` 通过
  4. `npm run lint` 通过

## 七、下一手

- 先抽主工作区与 section props 的共享类型
- 再更新：
  - `MainWorkspacePanel.tsx`
  - `useHomePage.ts`
  - `README`
  - `Cursor 同步包`
- 若通过，再补一轮轻量回归检查

## 八、后续执行回填

- 当前已新增：
  - `src/features/home/contracts/homeSectionProps.ts`
- 当前其作用是：
  - 统一页面 hook 与 section 组件的入参 contract
  - 避免两边各自重复定义一套同名接口
- 当前 `MainWorkspacePanel` 已改为：
  - `viewModel`
  - `content`
  - `actions`
  三段结构
- 当前验证结果：
  - `npm run build` 通过
  - `npm run lint` 通过
- 当前轻量回归结果：
  - 空态通过
  - 选中事件通过
  - 提交记录通过
  - 切事件重置通过
  - 待处理回流通过
  - 搜索动作回显通过
- 当前未发现主工作区 contract 收口后的明显回归
