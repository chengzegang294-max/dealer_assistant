# TDX Custom Terminal Layered Absorb Index v1

更新时间：2026-07-20

## 一、当前判断

- 这批材料最重要的价值不是“抄几个指标名”，而是识别这套终端的真实分层。
- 当前已能稳定区分出 5 层：
  - `配置壳`
  - `页面聚合层`
  - `公式索引 / 交易脚本层`
  - `插件注册 / 插件样式层`
  - `用户态 / 运行态数据层`

## 二、配置壳

### 2.1 关键入口

- `00_raw_snapshot/config/embui.cfg`
- `00_raw_snapshot/config/Connect.cfg`
- `00_raw_snapshot/config/tdxf11_cfg.xml`
- `00_raw_snapshot/f11/tdxf11_cfg.xml`
- `00_raw_snapshot/config/serverconfig.js`

### 2.2 当前结论

- `embui.cfg`
  - 管顶栏按钮、侧栏、附加菜单、本地页挂载与个股页入口
  - 典型特征是大量 `http://www.treeid/...` 与 `dlglocalurl##homepath##...`
- `Connect.cfg`
  - 管行情主机、资讯主机、网页入口和若干云端服务
  - 它是配置控制中枢，不是单纯联网参数表
- `tdxf11_cfg.xml`
  - 属于 F10/F11 服务配置层
  - 当前保留了“配置层视角”和“原位 files/f11 视角”两份快照，避免把它误写成普通散落配置
- `serverconfig.js`
  - 说明这包里还有较新的前端页面层，不止传统 html 聚合页

## 三、页面聚合层

### 3.1 关键入口

- `00_raw_snapshot/pages/Page.html`
- `00_raw_snapshot/pages/index.html`
- `00_raw_snapshot/pages/通达信F11.html`
- `00_raw_snapshot/f11/js/f10_main.js`
- `00_raw_snapshot/f11/js/f10_main_input.js`
- `00_raw_snapshot/pages/kpl-K线图.txt`
- `00_raw_snapshot/pages/kpl-K线图.html`
- `00_raw_snapshot/pages/东财K线+资金图.txt`
- `00_raw_snapshot/pages/东财K线+资金图.html`

### 3.2 当前结论

- `Page.html`
  - 是典型的个股聚合页
  - 通过 `##xxxxxx## / ##SC## / ##STOCKNAME##` 这类占位符做页面重写
  - 通过 `iframe` 混排本地页与外部站点
- `kpl-K线图.txt` / `东财K线+资金图.txt`
  - 只是“页面指针”
  - 不能把它们误当成指标公式文本
- `kpl-K线图.html`
  - 依赖 `ECharts`
  - 直接拉 `Longhuvip` API
  - 本质是网页图表载体
- `东财K线+资金图.html`
  - 依赖 `ECharts`
  - 直接拉 `Eastmoney` API
  - 本质也是网页图表载体
- `通达信F11.html` + `f10_main.js` + `f10_main_input.js`
  - 共同证明 F10/F11 不是“一个静态 html 页面”
  - 而是 `入口页 + 配置地址 + 主页面脚本 + 股票输入匹配脚本` 的运行组合

## 四、公式索引与交易脚本层

### 4.1 关键入口

- `00_raw_snapshot/formula/funcs_std.ini`
- `00_raw_snapshot/formula/funcs_jy.ini`
- `00_raw_snapshot/formula/flatjy.lua`
- `00_raw_snapshot/formula/flatjy/netbuy.lua`
- `00_raw_snapshot/formula/flatjy/jy_xgsg_dzh.lua`

### 4.2 当前结论

- `funcs_std.ini`
  - 更像标准功能/公式入口索引
  - 当前批次还不能把它等同于“公式源码库”
- `funcs_jy.ini`
  - 明确有 `PadCode / FeatureID / OutlookBarIndex` 这类功能映射
  - 属于交易面板功能索引，不只是一般公式名册
- `flatjy.lua`
  - 含真实逻辑函数，如买卖量和市场映射
  - 说明终端里至少局部存在脚本逻辑层
- `netbuy.lua`
  - 延续交易买卖量和市场标志判断
  - 说明交易逻辑脚本并非单文件孤例
- `jy_xgsg_dzh.lua`
  - 提供股东代码字段映射
  - 说明交易脚本层里还存在面向具体业务字段的轻量函数

## 五、插件层

### 5.1 关键入口

- `00_raw_snapshot/plugin/OtherPlu.cfg`
- `00_raw_snapshot/plugin/duilibstyle.xml`
- `00_raw_snapshot/plugin/JiuCaisd/Config/rvaConfig.json`
- `00_raw_snapshot/plugin/JiuCaisd/Config/patchList.json`
- `00_raw_snapshot/plugin/JiuCaisd/Config/hotkey.json`
- `00_raw_snapshot/plugin/JiuCaisd/Config/Menu/TradeSingleMenu.json`

### 5.2 当前结论

- `OtherPlu.cfg`
  - 是第三方 DLL 插件注册入口
- `duilibstyle.xml`
  - 是插件 UI 样式层
- `rvaConfig.json`
  - 显示插件会维护地址特征、函数入口和 treeid hook
- `patchList.json`
  - 显示插件补丁写入存在明确“时机合同”
- `hotkey.json`
  - 显示插件支持接管或叠加原始快捷键
- `TradeSingleMenu.json`
  - 显示插件还会直接定义交易菜单元素与命令映射
- 因此“某些效果来自插件”是一个真实分支，不能全压到公式层解释

## 六、用户态 / 运行态数据层

### 6.1 当前入口

- `00_raw_snapshot/config/T0002_user.ini`
- `00_raw_snapshot/config/T0002_user_def.ini`

### 6.2 当前结论

- 这些文件只证明终端存在用户态配置与自定义状态。
- 当前批次没有把大量 `T0002/*.dat` 一并吸收进来，因为那会把批次拖成二进制镜像，不符合当前入库边界。

## 七、最重要的不要误判

- 不要把 `网页图表页面` 误写成 `通达信公式源码`。
- 不要把 `功能索引 ini` 误写成 `完整指标源码集合`。
- 不要把 `插件注册` 误写成 `指标参数合同`。
- 不要把 `用户口头确认可编辑` 误写成 `当前仓内已具备全部源码`。

## 八、当前最适合后续提升的对象

- `可复刻页面壳`
  - 页面聚合、占位符替换、事件页分发
- `可借鉴的图表呈现`
  - K 线图 + 资金图这类网页视图
- `可抽象的功能入口`
  - `FeatureID / PadCode / MenuCommand / treeid`
- `可拆出来复核的真实脚本`
  - `flatjy.lua`
  - `netbuy.lua`
  - `jy_xgsg_dzh.lua`

## 九、当前仍缺的关键补件

- 代表性“可编辑指标”源码导出文本
- 公式参数区与公式画图语法样本
- `dat` 层或终端内部数据库对公式存储的说明
- 页面效果与我方体系对象卡的一一对应关系
