# TK-R8 B 区域 最小判据草案 v1

## 作用

- 作为 `TK-R8` 的第一份最小判据草案。
- 用于先把“什么才算有效 `B 区域`”写成结构化判断壳，而不是直接写成自动挂单规则。

## 适用对象

- 上游入口：
  - `TK-R8_B区域qualify壳_后续对象定义入口_v1.md`
- 当前只服务于：
  - `ABC / B 位挂单` 的 qualify 壳

## 判据目标

- 先把当前回撤区分成 3 类：
  - `not_b_zone`
  - `weak_b_zone`
  - `qualified_b_zone`

## 最小输入

- `ABC` 基本结构：
  - 能判断当前是否仍在原 `ABC` 框架内
- 回撤位置：
  - 能判断当前回撤是否接近理论 `B` 区
- 主方向环境：
  - 能判断原趋势/原波段是否仍在延续

## 最小判据

### 1. `not_b_zone`

- 含义：
  - 当前回撤虽然存在，但不能视为有效 `B 区域`
- 常见原因：
  - 已明显破坏原 `ABC` 结构
  - 回撤位置偏离 `B` 区太远
  - 原主方向延续环境已不清晰

### 2. `weak_b_zone`

- 含义：
  - 当前回撤接近 `B` 区
  - 但结构不够干净或确认度不够
- 常见特征：
  - 位置接近
  - 但 `ABC` 结构略松
  - 或当前价格行为还没给出足够支持

### 3. `qualified_b_zone`

- 含义：
  - 当前回撤既接近 `B` 区
  - 又没有破坏原 `ABC` 结构
  - 且原方向延续环境仍成立
- 当前保守理解：
  - 它代表“可继续关注的结构合格区”
  - 不等于“必须入场”

## `weak_b_zone` 与 `qualified_b_zone` 的更细判别

- 当前先不冻结完整 fib 数值和多周期确认。
- 当前先按三块最小条件判别：
  - `zone_alignment`
  - `abc_integrity`
  - `continuation_quality`

### 1. `weak_b_zone`

- 更常见于：
  - `near_b_zone`
  - 或虽然 `aligned_to_b_zone`
  - 但 `ABC` 结构不够干净
  - 或 `continuation_lost` 已开始出现
- 当前角色：
  - 表示“位置还可以，但结构/环境还不够稳”

### 2. `qualified_b_zone`

- 更常见于：
  - `aligned_to_b_zone`
  - 且没有明显 `structure_break`
  - 且没有明显 `b_zone_miss`
  - 且没有明显 `continuation_lost`
- 当前角色：
  - 表示“位置、结构、环境三者都还过得去”

## 当前保守裁决补充

- 当前更稳的最小写法是：
  - `zone_alignment` 只是第一层
  - `abc_integrity` 与 `continuation_quality` 共同决定：
    - 是 `weak`
    - 还是 `qualified`
- 因而当前：
  - `aligned_to_b_zone`
  也不自动等于：
  - `qualified_b_zone`
- 如果出现以下任一情况，当前更优先降到 `weak_b_zone`：
  - 结构略松
  - 反应段收回不够
  - 原方向延续环境开始变弱

## 最小辅助标签

- `abc_structure_valid`
  - `0 / 1`
- `b_zone_distance_note`
  - `far / near / aligned`
- `b_zone_quality_note`
  - `not_b_zone / weak_b_zone / qualified_b_zone`

## `b_zone_miss` 的最小距离口径

- 当前先不冻结精确 fib、点数或 ATR 比例。
- 当前先冻结最小三档：
  - `aligned_to_b_zone`
  - `near_b_zone`
  - `missed_b_zone`

### 1. `aligned_to_b_zone`

- 含义：
  - 当前回撤位置与理论 `B` 区基本对齐
- 当前角色：
  - 才更适合作为 `qualified_b_zone` 的位置基础

### 2. `near_b_zone`

- 含义：
  - 当前回撤接近 `B` 区
  - 但还不能说已经很好对齐
- 当前角色：
  - 更适合保守记为：
    - `weak_b_zone`

### 3. `missed_b_zone`

- 含义：
  - 当前回撤位置已经明显偏离理论 `B` 区
- 当前角色：
  - 对应：
    - `b_zone_miss`
  - 并更优先降到：
    - `not_b_zone`

## 当前保守裁决

- 当前更稳的最小写法是：
  - `aligned_to_b_zone` 才能支撑 `qualified_b_zone`
  - `near_b_zone` 最多先支撑 `weak_b_zone`
  - `missed_b_zone` 就更优先进入 `not_b_zone`
- 因而当前不建议把：
  - “大概接近”
  直接写成有效 `B` 区

## `zone_alignment + abc_integrity + continuation_quality` 的最小组合映射

- 当前先不冻结更细 fib、回撤百分比、速度阈值或多周期确认。
- 当前先把三块条件收成最小组合映射：
  - `zone_alignment`
  - `abc_integrity`
  - `continuation_quality`
- 当前默认理解：
  - 先看位置
  - 再看结构
  - 最后看延续环境
  - 三者一起决定：
    - `not_b_zone`
    - `weak_b_zone`
    - `qualified_b_zone`

### 1. `qualified_b_zone` 的最小组合

- 当前最稳组合是：
  - `aligned_to_b_zone`
  - `abc_intact`
  - `continuation_supportive`
- 当前角色：
  - 代表位置、结构、环境三者都还在支持原 `ABC` 的 `B` 区判断
- 当前保守写法：
  - 只有 `zone_alignment` 对齐还不够
  - 还要看：
    - `structure_break` 没明显出现
    - `continuation_lost` 没明显出现

### 2. `weak_b_zone` 的最小组合

- 当前更常见于以下两类：
  - `near_b_zone + abc_intact + continuation_soft`
  - `aligned_to_b_zone + abc_soft + continuation_soft_or_mixed`
- 当前角色：
  - 表示“还像 B 区，但不够干净，不宜直接当强 qualify”
- 当前保守理解：
  - 只要三块里有一块开始变弱
  - 但还没弱到：
    - `missed_b_zone`
    - `structure_break`
    - `continuation_lost`
  - 就更适合先落在：
    - `weak_b_zone`

### 3. `not_b_zone` 的最小组合

- 当前更常见于以下三类：
  - `missed_b_zone + any + any`
  - `any + abc_broken + any`
  - `any + any + continuation_lost`
- 当前角色：
  - 表示三块里只要有一块已经明显失效
  - 就优先退出有效 `B` 区判断
- 当前保守理解：
  - `zone_alignment` 再好
  - 也不能覆盖：
    - `ABC` 已破
    - 或原主方向环境已丢

### 4. 当前推荐的最小映射表

- `aligned_to_b_zone + abc_intact + continuation_supportive -> qualified_b_zone`
- `near_b_zone + abc_intact + continuation_supportive -> weak_b_zone`
- `aligned_to_b_zone + abc_soft + continuation_supportive -> weak_b_zone`
- `aligned_to_b_zone + abc_intact + continuation_soft -> weak_b_zone`
- `near_b_zone + abc_soft + continuation_soft_or_mixed -> weak_b_zone`
- `missed_b_zone + any + any -> not_b_zone`
- `any + abc_broken + any -> not_b_zone`
- `any + any + continuation_lost -> not_b_zone`

### 5. 当前保守裁决补充

- 当前更稳的最小收口是：
  - `qualified`
    - 需要三块同时站得住
  - `weak`
    - 允许一块偏软，但不允许明显失效
  - `not_b_zone`
    - 只要一块已明显失效，就优先退出
- 因而当前最不建议的写法是：
  - `只要接近 B 就算有效 B`
  - 或：
  - `只要位置对齐就直接升级 qualified`

## 当前保守顺序

- 现在先不冻结精确价格百分比或 fib 数值。
- 当前先冻结判断顺序：
  - 先看 `ABC` 结构是否还成立
  - 再看回撤是否接近理论 `B` 区
  - 再看原方向延续环境是否仍成立
  - 最后才把它归到 `weak/qualified`

## 当前不做的事

- 不直接写：
  - `接近 B = 必挂单`
- 不直接写：
  - `qualified_b_zone = 一定高胜率`
- 不直接把它升级成：
  - 硬门控
  - 独立策略
  - 已验证统计优势

## 下一步

- 若继续推进：
  - 再补 `reaction_reclaims_fail` 的更细价格行为提示
  - 再补 `zone_alignment`、`abc_integrity`、`continuation_quality` 各自的更细示例
- 当前已补：
  - `TK-R8_ABC结构失效_最小条件_v1.md`
