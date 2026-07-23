# A5 A股 P0 首页工作台 Batch1 最小 Hook 护栏页

更新时间：2026-07-22

## 一、这页用途

- 本页只做：
  - 在纯模型护栏已补齐后，判断 `useHomeWorkspace` 是否还需要最小 hook 级护栏
  - 将本轮范围收窄到最短真实链路验证
- 本页不做：
  - 扩成页面级或浏览器级测试
  - 重开 UI 结构讨论
  - 为测试而改动业务合同

## 二、主负责人裁决

- 当前结论：
  - 纯模型层已经覆盖核心状态迁移与辅助纯函数
  - 剩余最值钱的缺口不在更多纯函数，而在 `useHomeWorkspace` 是否真实把这些纯函数串起来
  - 因此当前下一刀应补最小 hook 护栏，而不是继续空扩低价值模型测试
- 当前决定：
  - 只给 `useHomeWorkspace` 补最短真实链路测试
  - 只验证最关键的状态串接，不追求 hook 全覆盖

## 三、本轮允许范围

- 允许修改：
  - `package.json`
  - `useHomeWorkspace.test.tsx`
  - `README.md`
  - `Cursor 同步包`
- 允许新增：
  - 最小 hook 测试文件
- 不允许借机扩展：
  - `useHomePage` 测试
  - 组件级测试
  - 页面级测试

## 四、本轮最小通过条件

- 满足以下四项即可视为本轮收口：
  1. 新增 `useHomeWorkspace` 最小 hook 测试文件
  2. 至少锁住：
     - 提交失败后进入 `editing` 并写入 `formError`
     - 提交成功后生成回显并写入记录
     - 点击重试后清空回显并回到 `editing`
     - 成功提交后再切事件会重建草稿并清空回显
  3. `npm run test` 通过
  4. `README` 与 `Cursor 同步包` 已回填

## 五、本轮结果

- 当前已新增：
  - `src/features/home/hooks/useHomeWorkspace.test.tsx`
- 当前最小 hook 护栏已锁住：
  - 提交失败后进入 `editing` 并写入 `formError`
  - 提交成功后生成回显与记录
  - 点击重试后清空回显并回到 `editing`
  - 成功提交后再切事件会重建草稿并清空回显
- 当前 `npm run test` 已通过：
  - `2` 个测试文件
  - `14` 个测试用例
- 当前 `Batch1` 前台停点更新为：
  - `首页薄壳 + workspace 不变量 + section props + adapter 分层 + 模型/Hook 双层最小自动化护栏`

## 六、当前明确不做

- 当前不要求：
  - hook 全路径覆盖
  - `useHomePage` 集成测试
  - 浏览器走查自动化

## 七、下一手

- 先补：
  - `useHomeWorkspace` 最小 hook 护栏
- 再跑：
  - `npm run test`
- 通过后回填：
  - `README`
  - `Cursor 同步包`
