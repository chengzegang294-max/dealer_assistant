# Batch 149 Execution Card

更新时间：2026-07-20

## 批次对象

- `通达信改版终端 external folder absorb`

## 当前目标

- 把外部终端从“看起来有很多指标效果”收成可追溯的分层判断：
  - 它的壳在哪里
  - 页面怎么挂
  - 哪些是公式索引
  - 哪些是真逻辑脚本
  - 哪些只是插件注册或网页图表载体

## 当前入口

- 本批次入口：`README.md`
- 批次导航：`01_index/family_entry_map_v1.tsv`
- 产物索引：`BATCH_149_ARTIFACT_INDEX_v1.md`
- 分层结论：`02_absorb_index/tdx_custom_terminal_layered_absorb_index_v1.md`

## 执行步骤

- 1. 先确认这是一整套终端，而不是单一指标源码包。
- 2. 再按 `config / pages / formula / plugin` 四层选代表文件吸收到 `00_raw_snapshot/`。
- 2. 再按 `config / pages / formula / plugin` 四层选代表文件吸收到 `00_raw_snapshot/`。
- 3. 对 `files/f11` 与 `HGPlugins/JiuCaisd/Config` 这类“原位语义很强”的子家族，额外保留原位目录快照，不只抽象成上层配置结论。
- 4. 对每类文件写清：
  - 原路径
  - repo 路径
  - 当前作用
  - 证据强度
- 5. 把“页面载体”和“公式源码”分开，不混写。
- 6. 把“用户确认可编辑”和“当前已拿到源码”分开，不伪造源码 completeness。
- 7. 给后续 `Cursor` 准备同步包，只让它在吸收结论上继续统领和审校，不让它回到原始猜测阶段。

## 当前状态

- 当前已完成：
  - 批次目录骨架
  - 代表性 raw snapshot
  - 第一组高优先补件：
    - `formula/flatjy/*.lua`
    - `f11/*.xml`
    - `f11/js/*.js`
    - `plugin/JiuCaisd/Config/*.json`
  - 第二组页面样本补件：
    - `pages/市场情绪.html`
    - `pages/热点提醒.html`
    - `pages/龙头股.html`
    - `pages/龙头股1.json`
  - 第三组历史载体补件：
    - `pages/复盘.html`
    - `pages/直播.html`
    - `pages/涨停龙虎.html`
    - `pages/选股宝直播.html`
  - 真实公式样本补件：
    - `formula_export_samples/*.png`
    - `formula_export_samples/*.txt`
    - 当前已稳定吸收 `17` 组
  - `可见效果 -> 来源三分表`
  - `公式导出样本索引`
  - `03_quantize/README.md`
  - `6 张核心对象卡`
  - `公式输出语义 -> Batch1 六卡字段桥`
  - `六卡事件字段总表`
  - `页面 -> 六卡 -> 事件字段总表` 细映射总表
  - README
  - provenance
  - manifest
  - family entry map
  - execution card
  - artifact index
  - layered absorb index
  - rebuild fit notes
- 当前未完成：
  - 全量指标源码导出
  - 二进制数据层解析
  - 系统短公式对应的编辑器截图链补齐
  - `Batch1` 真实代码实现本体

## 当前边界

- 当前不做：
  - 整包反编译
  - 全量缓存/执行体入库
  - 直接重写成我方前端
  - 直接认定“对方指标体系 = 我方体系”
- 当前允许继续做：
  - 补抓更多页面入口
  - 沿 `files/f11` 与 `九菜插件配置层` 继续补原位样本
  - 在三分表基础上继续补 `company/*.html` 高价值页面
  - 继续验证
    `复盘.html / 直播.html`
    是否能稳定回到指定历史日期
  - 用当前 `17` 组公式样本直接进入首轮正式映射
  - 从吸收批进入 `03_quantize/` 做对象卡
  - 当前已按 `方案C` 落 `6` 张对象卡与 `1` 张六卡字段桥
  - 当前已把六卡压成最终事件字段总表
  - 当前已补页面层细映射总表
  - 下一手应直接把 Batch1 切到真实实现
- 当前若未来以 `方案A` 重开后台补采，则正式顺序冻结为：
  - `F11 联动解释`
  - `company 高价值页面补进三分表`
  - `极窄公式截图链补洞`
- 当前若围绕
  `batch150`
  第三手继续推进，
  默认先复用：
  - `pages/复盘.html`
  - `pages/直播.html`
  再决定是否需要
  `pages/涨停龙虎.html / pages/选股宝直播.html`
- 当前明确不作为 `方案A` 默认下一手的，是：
  - `批量源码导出`
  - `DLL 行为深挖`
  - `继续扩对象卡`
