# TK-R8 ABC 结构失效 最小条件 v1

## 作用

- 作为 `TK-R8` 的第二份最小条件草案。
- 用于先回答：
  - 什么情况下不能再把当前回撤继续视为有效 `ABC` 结构的一部分
  - 从而让 `qualified_b_zone` 与 `not_b_zone` 的分界更清楚

## 适用对象

- 上游入口：
  - `TK-R8_B区域qualify壳_后续对象定义入口_v1.md`
- 配套判据草案：
  - `TK-R8_B区域_最小判据草案_v1.md`

## 当前目标

- 先把 `ABC` 结构失效写成最小三类条件，而不是一开始就冻结完整波浪规则。
- 当前最小三类：
  - `structure_break`
  - `b_zone_miss`
  - `continuation_lost`

## 最小失效条件

### 1. `structure_break`

- 含义：
  - 当前价格行为已经明显破坏原 `A-B-C` 的基本结构关系
- 当前作用：
  - 一旦出现，优先降为 `not_b_zone`

#### `structure_break` 的最小可见价格行为特征

- 当前先不冻结完整波浪或 fib 数值。
- 当前先冻结最小可见特征：
  - `breaks_prior_structure_pivot`
  - `fails_to_hold_expected_reaction_zone`
  - `reversal_leg_overrides_original_path`

##### 1. `breaks_prior_structure_pivot`

- 含义：
  - 当前价格已经明显破坏原本作为 `ABC` 骨架的关键摆点
- 当前角色：
  - 是最直接的 `structure_break` 信号

##### 2. `fails_to_hold_expected_reaction_zone`

- 含义：
  - 价格虽然一度接近理论 `B` 区或反应区
  - 但没有在该区形成应有的停顿/反应/收回
- 当前角色：
  - 用于区分“只是到位”与“结构仍成立”

##### 3. `reversal_leg_overrides_original_path`

- 含义：
  - 回撤腿已经发展成反向主导腿
  - 不再像原 `ABC` 框架里的正常回撤
- 当前角色：
  - 用来防止把明显反转段仍误记为 `weak_b_zone`

### 2. `b_zone_miss`

- 含义：
  - 当前回撤虽然存在
  - 但已经偏离理论 `B` 区过远
- 当前作用：
  - 说明“这次回撤不是在做 `B` 区 qualify”

### 3. `continuation_lost`

- 含义：
  - 原本应当延续的主方向环境已经不清晰
  - 即使位置接近 `B` 区，也不宜继续当作合格 `B` 区
- 当前作用：
  - 用来防止把“接近位置”误写成“结构仍有效”

#### `continuation_lost` 的最小可见环境特征

- 当前先不冻结完整趋势过滤器或多指标确认。
- 当前先冻结最小可见环境特征：
  - `impulse_followthrough_missing`
  - `reaction_reclaims_fail`
  - `context_flattens_or_reverses`

##### 1. `impulse_followthrough_missing`

- 含义：
  - 原方向本应继续推进
  - 但后续没有出现应有的延续性跟进
- 当前角色：
  - 提醒“原趋势延续环境已变弱”

##### 2. `reaction_reclaims_fail`

- 含义：
  - 回撤后的反应段没能有效收回关键位置或维持原方向优势
- 当前角色：
  - 用来区分“正常回撤后续强”与“回撤后续接不上”

##### 3. `context_flattens_or_reverses`

- 含义：
  - 当前价格环境已经从原方向推进，转成横向钝化或反向主导
- 当前角色：
  - 说明即使位置还接近 `B` 区，也不宜继续视作 `qualified_b_zone`

## 当前保守裁决补充

- 当前更稳的最小写法是：
  - `continuation_lost` 不要求先看到明显 `structure_break`
  - 只要原方向延续环境已经明显接不上，就应降低 `B` 区合格度
- 因而当前：
  - `near_b_zone + continuation_lost`
  也更优先落到：
  - `weak_b_zone`
  - 或直接 `not_b_zone`

## 当前保守顺序

- 现在先不冻结精确波段数值。
- 当前先冻结判断顺序：
  - 先看是否发生 `structure_break`
  - 再看是否出现 `b_zone_miss`
  - 再看是否已经 `continuation_lost`
- 只要任一项明显成立：
  - 当前就更优先降为 `not_b_zone`

## 与 TK-R8 判据草案的关系

- `qualified_b_zone`
  - 默认要求：
    - 没有明显 `structure_break`
    - 没有明显 `b_zone_miss`
    - 没有明显 `continuation_lost`
- `weak_b_zone`
  - 更像：
    - 还没明确失效
    - 但也还不够干净
- `not_b_zone`
  - 更像：
    - 已经触发至少一项最小失效条件

## 当前不做的事

- 不直接把某一根 K 线机械定义成：
  - `ABC 失效`
- 不直接冻结：
  - 具体 fib 比例
  - 具体波段长度阈值
  - 具体 bars 数
- 不直接把失效条件升级成：
  - 自动挂单否决门
  - 已验证统计优势结论

## 下一步

- 若继续推进：
  - 再补 `weak_b_zone` 与 `qualified_b_zone` 的更细判别
  - 再补 `reaction_reclaims_fail` 的更细价格行为提示
