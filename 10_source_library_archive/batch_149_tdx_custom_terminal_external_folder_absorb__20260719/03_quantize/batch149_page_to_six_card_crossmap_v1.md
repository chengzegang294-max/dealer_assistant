# Batch149 Page To Six Card Crossmap v1

更新时间：2026-07-20

## 一、用途

- 这页把：
  - `页面层 / 网页载体`
  - `六张核心对象卡`
  - `Batch1 事件字段总表`
  三者压成一张细映射总表。
- 这页的目标只有一个：
  - 证明当前 `Batch1` 可以不靠新 mock，而靠 `batch_149` 的正式吸收物开写。

## 二、当前映射边界

- 当前只映射：
  - 已有代表性页面证据
  - 已落 `6` 张对象卡
  - 已落 `六卡字段桥`
  - 已落 `六卡事件字段总表`
- 当前不映射：
  - 复杂图表样式
  - 页面微交互
  - 多 iframe 布局细节
  - F10/F11 的全量子页

## 三、页面层 -> 六卡 -> 事件字段总表

| 页面/原位证据 | 当前主来源层 | 对应对象卡 | 进入 Batch1 的主要字段 | 当前作用 | 禁止照搬项 |
|---|---|---|---|---|---|
| `pages/市场情绪.html` | 页面/网页载体 | `沪深涨跌停` | `EventSummary.title` / `ExplanationPayload.logic` / `impact` | 提供市场热度、风险偏好、分化环境 | 不搬 ECharts 样式、不搬远端图表 |
| `pages/热点提醒.html` | 页面/网页载体 | `打板资金` | `EventSummary.title` / `ExplanationPayload.logic` / `nextReviewPoint` | 提供封板承接、炸板压力、热点持续性解释 | 不搬 iframe 聚合布局、不搬远端提醒面板 |
| `pages/龙头股.html` + `龙头股1.json` | 页面/网页载体 + 页面数据 | `打板资金` + `上榜资金` | `ExplanationPayload.impact` / `historyAnalogy` | 提供热点龙头与资金背书的轻辅助语境 | 不把页面榜单直接当公式输出 |
| `pages/Page.html` | 页面/网页载体 | `HYDB行业对比` + `ZSDB指数对比` + `启动点` | `subject` / `logic` / `impact` | 证明个股工作台本来就是“环境 + 个股触发”联合解释，不是纯单点公式页 | 不搬多标签 iframe 容器本身 |
| `pages/通达信F11.html` + `f11/tdxf11_cfg.xml` + `f10_main.js` | 页面/网页载体 | `上榜资金` + `HYDB行业对比` + `ZSDB指数对比` | `subject` / `historyAnalogy` / `nextReviewPoint` | 提供 F10/F11 研究入口的背景解释层 | 不把 F10/F11 分类树当事件字段 |
| `formula_export_samples/沪深涨跌停__副图__系统公式.txt` | 真公式候选 | `沪深涨跌停` | `title` / `logic` / `nextReviewPoint` | 提供热度变化的直接公式证据 | 不把原始统计变量整段塞卡片 |
| `formula_export_samples/打板资金__副图__系统公式.txt` | 真公式候选 | `打板资金` | `title` / `logic` / `impact` | 提供封板资金与炸板压力的直接公式证据 | 不直接给打板动作建议 |
| `formula_export_samples/上榜资金__副图__系统公式.txt` | 真公式候选 | `上榜资金` | `title` / `impact` / `nextReviewPoint` | 提供资金背书与榜单异动证据 | 不写成跟榜建议 |
| `formula_export_samples/HYDB_行业对比...` | 真公式候选 | `HYDB行业对比` | `subject` / `logic` | 提供行业顺风/逆风环境 | 不扩成板块轮动引擎 |
| `formula_export_samples/ZSDB_指数对比...` | 真公式候选 | `ZSDB指数对比` | `subject` / `impact` | 提供指数顺风/逆风环境 | 不扩成择时系统 |
| `formula_export_samples/启动点...` | 真公式候选 | `启动点` | `title` / `holdingRelation` / `logic` | 提供个股启动候选与观察动作 | 不写成买入指令 |

## 四、对 Batch1 的直接意义

- `EventStreamPanel`
  - 现在可以直接消费：
    - 六卡压缩后的 `EventSummary`
- `MainWorkspacePanel`
  - 现在可以直接消费：
    - 六卡压缩后的 `selectedExplanationPayload`
- `DecisionRecordForm`
  - 现在可以直接基于：
    - `启动点`
    - `行业/指数环境`
    - `市场热度/资金背书`
    形成“继续观察 / 跟踪 / 暂缓”的解释前情
- `GlobalStatusBar`
  - 不直接吃公式对象卡
  - 继续保留首页壳角色

## 五、页面层与字段层的最终关系

- 页面层的价值：
  - 给我们提供产品终版中间态的交互组织灵感
- 六卡的价值：
  - 给我们提供可下沉到 `Batch1` 的稳定解释对象
- 事件字段总表的价值：
  - 把页面灵感和公式样本压成可直接实现的最小字段真值

## 六、主负责人裁决

- 到当前为止，`batch_149` 这条线已经完成：
  - 页面层证据
  - 公式样本证据
  - 对象卡
  - 字段桥
  - 事件字段总表
  - 页面到六卡的细映射总表
- 因此下一手继续留在这条线的边际价值已经明显下降。
- 更值钱的下一手应切回：
  - `A股 P0 Batch1` 真实代码实现
