# A5 A股 P0 首页工作台 Batch1 最小 Page Hook 护栏页

更新时间：2026-07-22

## 一、这页用途

- 本页只做：
  - 在模型层与 `useHomeWorkspace` 最小护栏已具备后，补 `useHomePage` 的最小编排层护栏
  - 只验证 section props 的真实串接是否保持一致，不做 UI 测试
- 本页不做：
  - 扩成组件级或页面级渲染测试
  - 重开 contract 或 adapter 结构美化
  - 新增功能

## 二、主负责人裁决

- 当前结论：
  - `useHomePage` 是首页“编排层薄壳”的唯一入口，它决定：
    - section props 的绑定是否指向正确的 workspace actions
    - viewModels 是否随 workspace 状态变化而更新
  - 因此应补最小 page-hook 护栏，避免将来编排层重构引入静默回归

## 三、本轮允许范围

- 允许新增：
  - `useHomePage.test.tsx`
- 允许修改：
  - `README.md`
  - `Cursor 同步包`
- 不允许借机扩展：
  - `Home.tsx` 级集成测试
  - 浏览器自动化
  - UI contract 改造

## 四、本轮最小通过条件

- 满足以下四项即可视为本轮收口：
  1. 新增 `useHomePage` 最小测试文件
  2. 至少锁住：
     - `eventStreamPanelProps.selectedEventId` 随选择事件更新
     - `section props` actions 指向正确的 workspace handler（引用一致）
     - `handleOpenFinanceDisclosure` 能触发 `finance-disclosure-note` 的 `scrollIntoView`
  3. `npm run test` 通过
  4. `README` 与 `Cursor 同步包` 已回填

## 五、当前明确不做

- 当前不要求：
  - 组件渲染断言
  - 视觉/UI 结构验证
  - section contract 继续收口

## 六、下一手

- 先补：
  - `useHomePage` 最小 hook 护栏
- 再跑：
  - `npm run test`
- 通过后回填：
  - `README`
  - `Cursor 同步包`
