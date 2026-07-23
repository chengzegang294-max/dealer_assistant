# Batch 149 TDX Custom Terminal External Folder Absorb

更新时间：2026-07-20

## 批次目标

- 把外部文件夹 `羽搧綸巾   经典酷黑   灵动版` 作为一次 `通达信改版终端` 吸收批纳入 repo 可追溯链路。
- 原始外部来源为 `E:\downloads\Desktop\羽搧綸巾   经典酷黑   灵动版`，当前临时吸收位为 `d:\Stock\trading_assistant\暂时存放\羽搧綸巾   经典酷黑   灵动版`。
- 当前只吸收最关键入口层，不盲目镜像整包可执行终端。
- 先把“它到底是什么”讲清，再决定哪些部分值得后续量化重做或页面复刻。

## 收口裁决

- 本批次确认这不是“几条孤立指标公式”，而是：
  - `通达信终端底座`
  - `UI/菜单/路由配置壳`
  - `本地页面聚合层`
  - `公式索引与交易脚本层`
  - `插件注册与插件样式层`
- `00_raw_snapshot/` 只保留为阶段性追溯位，不作为默认 first-hop。
- 当前 first-hop 入口应转到：
  - `01_index/family_entry_map_v1.tsv`
  - `BATCH_149_EXECUTION_CARD.md`
  - `BATCH_149_ARTIFACT_INDEX_v1.md`
  - `02_absorb_index/tdx_custom_terminal_layered_absorb_index_v1.md`
- 若未来要重开后台补采顺序，直接看：
  - `00_entry/全库资料整理收口__20260713/A5_batch149方案A最终补采优先级与停止规则页__20260723.md`
- 当前明确不宣称：
  - 已拿到全部可编辑指标源码
  - 已完成整包反编译
  - 已证明每个图示效果都来自通达信公式而非网页/API 组件

## 批次结构

- `00_raw_snapshot/`
  - 已吸收代表性入口文件，按 `config / pages / formula / f11 / plugin / formula_export_samples` 分层保存
- `01_index/`
  - 当前批次导航与 first-hop 入口
- `02_absorb_index/`
  - 分层吸收结论、可重做对象判断、与我方体系的拟合说明
  - 以及 `可见效果 -> 来源三分表`
- `03_quantize/`
  - 预留给后续对象化、字段化、重做实现
- `04_runtime/`
  - 预留给后续最小复刻验证或页面效果复现

## 当前产物

- `README.md`
- `provenance.md`
- `manifest_v1.tsv`
- `BATCH_149_EXECUTION_CARD.md`
- `BATCH_149_ARTIFACT_INDEX_v1.md`
- `01_index/family_entry_map_v1.tsv`
- `02_absorb_index/tdx_custom_terminal_layered_absorb_index_v1.md`
- `02_absorb_index/tdx_custom_terminal_rebuild_fit_notes_v1.md`
- `02_absorb_index/tdx_custom_terminal_visible_effect_source_triage_v1.md`
- `02_absorb_index/tdx_custom_terminal_formula_export_sample_index_v1.md`
- `02_absorb_index/tdx_custom_terminal_formula_to_investment_cockpit_mapping_v1.md`
- `03_quantize/README.md`
- `03_quantize/batch149_formula_semantics_to_batch1_field_bridge_v1.md`
- `03_quantize/batch149_object_card_沪深涨跌停__20260720.md`
- `03_quantize/batch149_object_card_打板资金__20260720.md`
- `03_quantize/batch149_object_card_上榜资金__20260720.md`
- `03_quantize/batch149_object_card_HYDB行业对比__20260720.md`
- `03_quantize/batch149_object_card_ZSDB指数对比__20260720.md`
- `03_quantize/batch149_object_card_启动点__20260720.md`
- `03_quantize/batch149_six_card_event_field_bundle_v1.md`
- `03_quantize/batch149_page_to_six_card_crossmap_v1.md`

## 默认阅读顺序

- 1. 先看本 `README.md`
- 2. 再看 `BATCH_149_EXECUTION_CARD.md`
- 3. 再看 `02_absorb_index/tdx_custom_terminal_layered_absorb_index_v1.md`
- 4. 再看 `02_absorb_index/tdx_custom_terminal_visible_effect_source_triage_v1.md`
- 5. 再看 `02_absorb_index/tdx_custom_terminal_formula_export_sample_index_v1.md`
- 6. 再看 `02_absorb_index/tdx_custom_terminal_formula_to_investment_cockpit_mapping_v1.md`
- 7. 再看 `03_quantize/README.md`
- 8. 再看 `03_quantize/batch149_formula_semantics_to_batch1_field_bridge_v1.md`
- 9. 再看 `03_quantize/` 下的 `6` 张核心对象卡
- 10. 再看 `03_quantize/batch149_six_card_event_field_bundle_v1.md`
- 11. 再看 `03_quantize/batch149_page_to_six_card_crossmap_v1.md`
- 12. 需要核对原件时，再回到 `BATCH_149_ARTIFACT_INDEX_v1.md` 与 `00_raw_snapshot/`
- 13. 若要给实现侧衔接，直接看：
  - `00_entry/全库资料整理收口__20260713/A5_A股P0首页工作台Batch1开工手令__20260720.md`
- 14. 若要给 `Cursor` 衔接，直接看：
  - `00_entry/全库资料整理收口__20260713/A5_Cursor同步包_通达信改版终端吸收批次与使用方式__20260720.md`

## 当前已冻结结论

- `embui.cfg` 证明该包有强定制的顶栏、侧栏、菜单、页面路由和本地页面挂载能力。
- `Connect.cfg` 证明该包不是单机静态皮肤，而是把行情站点、资讯/服务页、工具页、网页入口绑进统一配置中心。
- `company/Page.html` 证明其个股工作台大量依赖：
  - 占位符替换
  - iframe 聚合
  - 本地页与外部页混排
- `company/kpl-K线图.html` 与 `company/东财K线+资金图.html` 证明一部分“像指标的效果”其实是网页图表载体，依赖 `ECharts + 外部 API`，不是纯公式画线。
- `funcs_std.ini` / `funcs_jy.ini` 证明存在公式/功能索引层，但当前批次只看到了索引入口，没有成规模的明文指标源码导出。
- `flatjy.lua` 证明至少交易面板一侧存在真实逻辑脚本，而不只是配置枚举。
- `netbuy.lua` / `jy_xgsg_dzh.lua` 进一步证明交易面板并非纯配置壳，存在可读的业务脚本补件。
- `用户公式名称截图/` 中已导出 `9` 组真实公式样本，证明当前批次已经拿到一批：
  - `终端公式编辑器截图`
  - `公式正文 txt`
  不再只是页面壳、脚本壳和插件配置壳。
- `系统公式` 本轮又补回 `8` 组正文 txt，当前已经直接命中：
  - `板块联动`
  - `热点涨停/连板`
  - `龙虎榜/资金异动`
  - `指数/情绪强弱`
  - `个股异动/预警`
  这五类代表样本。
- `files/f11/tdxf11_cfg.xml`、`f10_main.js`、`f10_main_input.js` 证明 F10/F11 不只是一个静态 html 入口，而是 `配置地址 + 主页面脚本 + 输入匹配脚本` 的运行组合。
- `OtherPlu.cfg` 与 `duilibstyle.xml` 证明插件注册与插件 UI 样式是独立分层，不应混写进指标层。
- `HGPlugins/JiuCaisd/Config/*.json` 证明至少 `九菜插件` 一侧还存在：
  - 地址特征与 treeid hook 配置
  - 补丁写入时机合同
  - 快捷键合同
  - 单窗交易菜单合同
- 本轮已新增一张：
  - `可见效果 -> 来源三分表`
  - 用来把 `页面 / 插件编排 / 真公式候选` 三层先分开，再决定源码导出顺序
- 本轮还新增一张：
  - `公式导出样本索引`
  - 用来标记哪些五类样本已经命中、哪些类仍缺直接公式证据
  - 当前该页已更新为 `17` 组样本总表
- 本轮继续新增一张：
  - `公式到我方驾驶舱闭环映射页`
  - 用来决定这些公式更适合落在 `提醒 / 解释 / 记录 / 回看` 哪一层
- 本轮已按 `方案C` 进入 `03_quantize/`：
  - 已落 `6` 张核心对象卡
  - 已落 `1` 张极短字段桥，并扩到六卡闭环
  - 已落 `1` 张六卡事件字段总表
  - 已落 `1` 张页面到六卡的细映射总表
  - 不继续盲导源码
  - 当前已具备切回 Batch1 写业务代码的条件

## 当前缺口

- 还没有拿到“全部可编辑指标”的批量源码导出文件。
- 还没有定位所有指标公式的真实磁盘存储方式；部分内容可能在 `dat` / 二进制索引 / 终端内部数据库里。
- 还没有把 `files/f11` 全家桶与 `company/通达信F11.html` 做到逐项联读，只完成了入口层吸收。
- 还没有把 `HGPlugins/JiuCaisd/Config` 与对应 DLL 行为做联动解释，只确认了配置合同层存在。
- 还没有把第二组 `company/*.html` 高价值页面补进三分表，当前三分表仍是 v1。
- 系统公式这批当前多数只有 `txt`，还缺对应的编辑器截图链。
- 当前若未来按 `方案A` 重开补采，优先顺序已冻结为：
  - `F11 联动解释 -> company 高价值页面补进三分表 -> 极窄公式截图链补洞`
  - `DLL 行为` 继续保持 `NEED_EVIDENCE`

## 当前边界

- 本批次当前不做：
  - 整包终端复制入库
  - 可执行程序与大体积缓存全量镜像
  - 反编译二进制文件
  - 直接宣称“可完整复制对方指标体系”
- 本批次当前只做：
  - 关键入口吸收
  - 分层识别
  - 证据追溯
  - 后续复刻与体系映射的起点准备
