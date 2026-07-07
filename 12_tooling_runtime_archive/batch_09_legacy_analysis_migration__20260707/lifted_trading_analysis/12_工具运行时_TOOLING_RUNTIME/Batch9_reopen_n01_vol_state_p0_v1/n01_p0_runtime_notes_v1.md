# n01_p0_runtime_notes v1

## 角色

- 这份文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `REOPEN_B9_N01_VOL_STATE_P0` 真实运行产物的当前运行口径。

## 当前状态

- 当前目录已创建。
- 当前主 CSV 已不再只是示例行。
- 已通过：
  - `real_input_samples\n01_proof_of_mapping_output_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xauusd_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_eurusd_m15_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xauusd_m15_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_eurusd_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xauusd_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xbrusd_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xbrusd_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_aapl_nas_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_aapl_nas_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_ustec_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_ustec_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_us500_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_us500_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_de40_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_de40_h4_v1.csv`
  - `n01_p0_runtime_append_from_proof_v1.py`
  把第一批真实 proof 行正式 append 到：
  - `n01_p0_fields_runtime_v1.csv`
- 当前 runtime csv 中为：
  - 真实 `EURUSD H1`
  - 真实 `EURUSD M15`
  - 真实 `EURUSD H4`
  - 真实 `XAUUSD H1`
  - 真实 `XAUUSD M15`
  - 真实 `XAUUSD H4`
  - 真实 `XBRUSD H1`
  - 真实 `XBRUSD H4`
  - 真实 `AAPL.NAS H1`
  - 真实 `AAPL.NAS H4`
  - 真实 `USTEC H1`
  - 真实 `USTEC H4`
  - 真实 `US500 H1`
  - 真实 `US500 H4`
  - 真实 `DE40 H1`
  - 真实 `DE40 H4`
  - 首批跨品种 + 多周期 + 多资产类别（含指数分支）ATR / ratio / percentile_regime / squeeze 输出行
- 当前仍不应把本目录内容描述为“已跑完”或“已有回测结论”。

## 当前固定表头

- `symbol`
- `timeframe`
- `bar_time`
- `atr_value`
- `atr_ratio`
- `atr_percentile`
- `atr_percentile_regime`
- `squeeze_is_on`
- `squeeze_tier`
- `squeeze_fired`
- `compression_quality_score`

## 当前固定边界

- 只覆盖 `N01 P0` 的 `8` 个字段。
- 当前不含：
  - `atr_baseline_value`
  - `compression_state`
  - `vol_regime_code`
  - `vol_breakout_signal`
  - `trend_confirmation_after_vol_breakout`
  - 四项 compression 子评分

## 运行时默认口径

- `atr_percentile`：当前固定为 `0-100`。
- `atr_percentile_regime`：当前枚举只允许 `extreme / elevated / normal / calm / squeeze / unknown`。
- `squeeze_tier`：当前枚举只允许 `high / medium / low / off`。
- `squeeze_fired`：当前仍只保留 `0/1` 结果位。
- `compression_quality_score`：当前为 `AG-Pro-like` 最小可复现连续分数（仍允许 `na`）。

## `compression_quality_score` 源码等价矩阵

- 已对齐（当前可写成“有来源页支撑”）：
  - 参数窗口：
    - `atrLen = 14`
    - `baselineLen = 50`
    - `rangeWindow = 20`
    - `noiseWindow = 10`
    - `containmentWindow = 24`
  - 权重：
    - `atr = 30`
    - `range = 30`
    - `noise = 20`
    - `containment = 20`
  - 状态阈值骨架：
    - `compressionThreshold = 62`
    - `matureThreshold = 80`
  - 状态枚举骨架：
    - `Loose / Building / Tight / Mature`
- 半对齐（当前只到“语义相似”，不能写成源码等价）：
  - `atrScore`
    - 当前实现：`current_atr / baseline_atr` 的收缩评分
    - 与来源摘要一致，但尚未拿到 AG Pro 核心公式段逐字校对
  - `rangeScore`
    - 当前实现：`recent_range / sum(tr_window)` 的收缩评分
    - 已完成去退化修正，但仍不能证明与 AG Pro 原公式逐项相同
  - `noiseScore`
    - 当前实现：实体占比 + 方向翻转混合评分
    - 与“wick / flips / drift”语义接近，但仍缺精确公式
  - `containmentScore`
    - 当前实现：价格落在内层 pocket 的收盘占比
    - 与“contained volatility pocket”语义接近，但仍缺精确公式
  - `compression_quality_score`
    - 当前实现：四项子评分按 `30/30/20/20` 加权合成
    - 结构级对齐已完成，但核心计算段仍未逐项等价
- 未对齐 / 缺源码无法判定：
  - `strictMode`
    - 已知来源页确认存在开关
    - 已知作用方向：`applies tighter score gates for more selective compression pockets`
    - 新增公开页正文证据：advanced options 还允许 `stricter filtering`，并对 `wick behavior`、`close-overlap behavior` 提供额外敏感度控制
    - 当前仓库仍未实现，但现在不能再写成“完全未知”
    - 当前仍没有足够证据冻结它到底收紧：
      - 总分门槛
      - 子评分下限
      - pocket 资格
      - 还是状态机分支
  - `compression_state`
    - 已完成影子分箱审计，但在核心公式未逐项等价前仍不正式落盘
  - `Action Engine`
    - 已知输出属于建议层（如 `Review Upside / Wait Setup`）
    - 当前不应误解为交易指令，也不进入 P0 runtime 字段
  - Pocket 视觉层 / archive / ribbon / labels
    - 明确不属于当前 P0 runtime 主字段范围

## `compression_quality_score` 核心计算段细化审计清单

- `atrScore`
  - 当前实现：
    - 先算 `atr_ratio = current_atr / baseline_atr`
    - 再用 `good_at=0.60 / bad_at=1.10` 做线性归一化
  - 来源摘要语义：
    - 已确认是 `ATR contraction`
    - 已确认核心输入是 `current ATR vs baseline ATR`
  - 已锁定一致项：
    - 输入骨架一致：都在比较“当前波动”相对“基线波动”的收缩程度
    - 方向一致：`ratio` 越低，得分越高
  - 已锁定不等价项：
    - 当前 `0.60 / 1.10` 属于工程冻结阈值，不是来源页直接给出的源码阈值
    - 当前归一化函数是线性 piecewise clamp，尚不能证明 AG Pro 也是同型函数
  - 当前裁决：
    - `高语义对齐 / 非源码等价`
- `rangeScore`
  - 当前实现：
    - 先算 `recent_range = rolling high-low span`
    - 再算 `baseline_range = sum(tr_window)`
    - 再用 `recent_range / baseline_range` 与 `0.17 / 0.34` 做线性归一化
  - 来源摘要语义：
    - 已确认是 `Range tightness`
    - 已确认在比较 `recent_range / baseline_range`
  - 已锁定一致项：
    - 方向一致：结构越收敛、`ratio` 越低，得分越高
    - 窗口骨架一致：当前使用 `rangeWindow = 20`
  - 已锁定不等价项：
    - `baseline_range` 的精确定义仍缺源码；当前用 `sum(tr_window)` 只是同尺度修正后的工程代理
    - `0.17 / 0.34` 是去退化修正后的人工作业阈值，不是来源绑定阈值
  - 当前裁决：
    - `中语义对齐 / 已修退化 / 仍非源码等价`
- `noiseScore`
  - 当前实现：
    - `body_quality = avg(abs(close-open)/(high-low))`
    - `flip_ratio = direction sign flips / close-to-close changes`
    - 合成：`0.70 * body_quality + 0.30 * (1 - flip_ratio)`
  - 来源摘要语义：
    - 已确认是 `Noise evaluation`
    - 已明确提到 `wick behavior / direction flips / close-to-close drift`
  - 已锁定一致项：
    - 当前已覆盖“实体占比”和“方向翻转”两类噪声因子
    - 方向一致：越干净、越少噪声，得分越高
  - 已锁定不等价项：
    - 当前没有单独实现 `drift` 项
    - 当前也没有把 `wick`、`flip`、`drift` 拆成独立子项再聚合
    - `0.70 / 0.30` 权重属于当前工程近似，不是来源页直给权重
  - 当前裁决：
    - `中低语义对齐 / 非源码等价`
- `containmentScore`
  - 当前实现：
    - 先用 `containmentWindow = 24` 求窗口总区间
    - 再取内层 `25%-75%` pocket
    - 统计收盘价落入 pocket 的占比
  - 来源摘要语义：
    - 已确认是 `Containment structure`
    - 已确认在看价格是否聚集于 `contained volatility pocket`
  - 已锁定一致项：
    - 当前已覆盖“价格是否集中在内层窄区间”的核心语义
    - 方向一致：contained 越强，得分越高
  - 已锁定不等价项：
    - 当前 pocket 取法是静态内四分位，不足以证明与 AG Pro 的 pocket 轮廓完全一致
    - 当前只看 `close`，不能证明源码是否也要求 `high/low/wick/body` 共同受限
  - 当前裁决：
    - `中语义对齐 / 非源码等价`
- `compression_quality_score`
  - 当前实现：
    - 四项子评分按 `30 / 30 / 20 / 20` 加权合成，再 clamp 到 `0-100`
  - 来源摘要语义：
    - 已确认四项组成、权重结构、总分归一化、状态阈值骨架
  - 已锁定一致项：
    - 结构级骨架已对齐
  - 已锁定不等价项：
    - 只要 `range/noise/containment` 中任一项尚非源码等价，总分也不能写成源码等价
  - 当前裁决：
    - `结构对齐 / 核心公式未等价`

## `compression_state` 不等价项清单

- 当前影子分箱：
  - `Loose < 62`
  - `Building 62-70`
  - `Tight 70-80`
  - `Mature >= 80`
- 已锁定一致项：
  - 状态枚举骨架一致
  - `compressionThreshold = 62`
  - `matureThreshold = 80`
- 已新增来源绑定语义：
  - `matureThreshold = 80` 的来源说明不是单纯“>=80 即 Mature”
  - 来源摘要明确写到：`Higher score for mature compression when noise and containment confirm`
- 已锁定不等价项：
  - `Building / Tight` 的中间切点 `70` 目前只是影子诊断切点，不是来源绑定阈值
  - `Mature` 需要“noise and containment confirm”；当前影子分箱只看总分，没有单独确认门槛
  - `strictMode` 已知会收紧 score gates，但当前未实现，故状态机仍缺一整层 gating
  - `nearEdge / releaseUp / releaseDown` 已确认存在于 `Action Engine` 分支，但当前未实现
- 当前裁决：
  - 可以写成“当前存在稳定 shadow state distribution”
  - 不能写成“已完成 AG Pro 原状态机实现”

## `Action Engine` 已知分支边界

- 已知建议层分支：
  - `releaseUp -> Review Upside`
  - `releaseDown -> Review Downside`
  - `isMature and nearEdge -> Watch Edge`
  - `isMature -> Monitor Mature`
  - `isTight -> Track Compression`
  - `isBuilding -> Build Context`
  - `else -> Wait Setup`
- 当前可确认：
  - 这些分支证明 `compression_state` 后面还有一层“状态 + 位置”解释层
  - 它不是 P0 必须落盘字段，但对 `compression_state` 语义审计有帮助
  - 公开页正文还确认存在：
    - `Compression Active` alert
    - `Compression Mature` alert
    - `Compression State Change` alert
  - 这说明：
    - active qualification
    - mature qualification
    - state transition
    至少都被当作稳定事件暴露给告警层
  - 公开页还把以下内容作为常规展示层直接暴露：
    - active compression zone
    - mini panel 中的 `active state`
    - `compression window length`
  - 因而 `active pocket / active state` 当前更应视为主状态层的一部分，而不是 Action Engine 的附属文案
  - 更新日志还单独提到：
    - `resolved compression areas`
  - 这说明脚本内部至少存在 active / resolved 两类压缩区域概念
  - `batch9_sources_kimi` 还明确列出：
    - `archivePockets: true`
    - `archiveCount`
    - `projectPocketBars`
  - 因而当前更应优先把 `resolved compression areas` 视为 pocket/归档展示链路的一部分
  - 它未必是新的主状态分箱，更可能是 active pocket 结束后的历史可视化层
  - `projectPocketBars` 也更像 pocket 展示延伸，而不是 `releaseUp / releaseDown` 的直接触发条件
  - 更新日志还明确写到：
    - 非 active 时 preview labels 仍可见
    - preview labels 不能视为 active compression state confirmation
  - 因而当前更应把：
    - preview / label visibility
    - active pocket / active state
    明确拆成两层
  - `batch9_sources_kimi` 的源码结构拆解还给出：
    - `Lines 201-300: Pocket detection + Archive management`
    - `Lines 426-540: Ribbon + Action Engine + Event Labels`
  - 因而当前更应把 `nearEdge / releaseUp / releaseDown` 视为“pocket/位置事件层”候选，而不是四项核心评分的一部分
  - `Action Engine` 的条件优先级已知：
    - `releaseUp / releaseDown` 排在最前
    - `isMature and nearEdge` 排在其后
    - 再往后才是 `isMature / isTight / isBuilding`
  - 这说明：
    - `releaseUp / releaseDown` 更像状态后的事件覆盖分支
    - `nearEdge` 不是通用位置标记，当前至少只在 `Mature` 分支中参与建议层输出
  - `Compression State Change` 是独立告警语义，而 `releaseUp / releaseDown` 是独立 action 分支
  - 因而当前更应把 `releaseUp / releaseDown` 视为“状态机之后的额外事件标签”，而不是通用 state change 的别名
  - 公开 alerts 里没有 `Review Upside / Review Downside`
  - 因而当前更不应把 `releaseUp / releaseDown` 视为主告警层；它们更像 panel / action 建议标签
- 当前不可确认：
  - `nearEdge / releaseUp / releaseDown` 的精确判定公式
  - `strictMode` 是否会影响这些建议层分支

## `strictMode` 优先核对清单

- 基于当前公开页正文，`strictMode` 最可能优先影响的不是四项权重本身，而是过滤与资格层：
  - `noiseScore`：
    - 来源直接提到 `wick behavior`
    - 当前实现只覆盖 `body_quality + flip_ratio`
    - 因此后续若接 `strictMode`，优先检查是否需要把 wick 相关噪声门槛单独收紧
  - `containmentScore` / pocket 资格：
    - 来源直接提到 `close-overlap behavior`
    - 当前实现是 `25%-75% close-only pocket`
    - 公开页开头还强调：
      - `separates loose and unstable contraction from cleaner, more contained compression conditions`
    - `matureThreshold` 描述还直接写到：
      - `Higher score for mature compression when noise and containment confirm`
    - 因此后续若接 `strictMode`，优先检查是否需要对 close overlap / pocket contained 条件做额外资格过滤
    - `strictMode` 的参数描述还直接写到：
      - `more selective compression pockets`
    - 因而当前更应优先怀疑它不仅收紧 active/mature gating，也会前移到 contained pocket / pocket qualify 本身；因为 mature confirm 本身就是 noise+containment 的下游结果
  - `compression_active / Mature gating`：
    - 来源写的是 `stricter filtering`
    - 这更像 activation / mature qualification 的收紧，而不只是总分重新缩放
    - 公开页又单独暴露了 `Compression Active` 与 `Compression Mature` alerts
    - 因而当前更优先怀疑 `strictMode` 影响的是 active/mature qualification，而不是 Action Engine 文案层
- 基于当前证据，`strictMode` 的 first landing 还可再缩一层：
  - 第一优先不是 `Mature` 末端 gating，而是 `pocket qualify`
  - 而在 `pocket qualify` 内部，又更优先怀疑：
    - `close-overlap behavior` 的敏感度收紧
    - 再影响 `contained pocket` 的资格通过率
  - 原因是：
    - `advanced options` 直接点名 `close-overlap behavior`
    - 参数描述直接写 `more selective compression pockets`
    - `Mature` 则被描述为 `noise and containment confirm` 的下游结果
    - 原始页面 `Methodology` 还把：
      - `local overlap behavior`
      放在 `Noise evaluation`
      - 而把 `Structural containment`
      单列为后一项
    - `Key Inputs` 还把这层关系说得更像“参数入口”而不是“资格定义本身”：
      - `Advanced options allow stricter filtering and additional sensitivity controls for wick behavior and close-overlap behavior`
      - 这更像：
        - `strictMode` 负责更总括的 filtering 收紧
        - `close-overlap behavior` 属于同组 advanced options 中的可调 sensitivity 输入
      - 当前更保守的理解应是：
        - 公开页没有把 `strictMode` 直接写成 `close-overlap` 旋钮本身
        - 也没有把 `close-overlap` 直接写成 `strictMode` 的唯一落点
        - 更像 `strictMode` 与 `close-overlap behavior sensitivity` 同属 advanced filtering family
      - 从句式本身看也更支持这种拆分：
        - `stricter filtering`
        - `and additional sensitivity controls for wick behavior and close-overlap behavior`
      - 这更像在描述两类并列能力：
        - 一类是更总括的 filtering
        - 一类是针对 wick / close-overlap 的局部 sensitivity controls
      - 因而当前更优先怀疑：
        - `strictMode` 不只是 `close-overlap sensitivity` 的别名
        - 而是与 `close-overlap sensitivity` 并列、并可能共同进入 `pocket qualify` 的一组 advanced options
      - 因而当前不能直接写成：
        - `strictMode == close-overlap sensitivity`
      - 更应写成：
        - `strictMode` 是更总括的 filtering/gating 开关
        - `close-overlap behavior` 是同组但相对独立的 sensitivity control
      - 若再细一层，当前更像：
        - `close-overlap behavior` 调的是 feature-level sensitivity
        - `strictMode` 调的是 policy-level gating / qualify strictness
      - 因而当前最稳的中间判断不是“二选一谁先谁后”，而是：
        - 二者可能分别作用在不同层
        - 但会在 `pocket qualify` 一侧汇合
      - 公开页也没有直接把 `close-overlap` 写成独立的 `qualified pocket = true/false` 条件名
    - 因而当前更像：
      - `close-overlap` 是更前面的敏感度/洁净度输入
      - `strictMode` 更可能在 `pocket qualify` 一侧做 policy-level filtering/gating 收紧
      - `pocket qualify` 是中间资格层
      - `contained pocket` 是通过该类过滤后更容易留下的结构结果
  - 因而当前更窄的排序是：
    - `close-overlap feature-level sensitivity`
    - `strictMode policy-level filtering/gating`
    - `shared pocket qualify`
    - `contained pocket / containment quality`
    - `active/Mature gating`
    - `Action Engine`
- 参数面板分层本身也补到一层证据：
  - `strictMode` 被列在 `Core Engine`
  - `showPocket / showPocketText / showPocketMidline / showPocketQuarters / projectPocketBars / archivePockets / archiveCount` 被列在 `Compression Pocket Visuals`
  - 因而当前更不应把 `strictMode` 视为 pocket/archive 展示开关
  - 它更像核心状态资格或过滤层输入
  - 公开页总述还把：
    - `zone visibility / labels / panel position / theme mode / text sizing / label offset`
    归到 `display controls`
  - 而把 `stricter filtering + wick behavior + close-overlap behavior sensitivity`
    归到 `advanced options`
  - 因而当前没有证据表明 `strictMode` 与 labels/visuals 共用同一套展示开关链
- 当前不应优先假设的方向：
  - 不应先假设 `strictMode` 会改 `30/30/20/20` 权重
  - 不应先假设 `strictMode` 只是单一 `compressionThreshold` 上调
  - 不应先假设它直接改写 `Action Engine` 文案层
  - 不应先假设它只是 `showPocket / archivePockets / projectPocketBars` 一类展示开关
  - 不应先假设它和 `labels / panel / theme / text sizing / label offset` 共用显示链路
  - 不应先把 `releaseUp / releaseDown / nearEdge` 当成总分子项
- 当前裁决：
  - 若后续接代码，第一优先核对位点应是：
    - `noiseScore` 的 wick 相关子项
    - `containment / close-overlap / pocket qualify` 资格层
    - `compression_state` 的 active / mature confirm gating
    - `Pocket detection` 与 `Action Engine` 之间的位置事件连接
  - 在拿到更细源码前，这份清单仍只用于审计优先级，不用于直接实现
  - 当前优先顺序可进一步收紧为：
    - 先追 `close-overlap` 是如何作为 sensitivity input 被调节
    - 再追 `strictMode` 是否在同组 advanced filtering family 中额外收紧 policy-level qualify/gating
    - 再追它们是否共同进入 `shared pocket qualify`
    - 再追 `contained pocket`
    - 再追 `noise + containment -> Mature confirm`
    - 最后再追 `releaseUp / releaseDown` 与 resolved pocket 退出事件
  - `strictMode_kimi_followup` 的 v1 回帖已给出一轮外部裁决：
    - `VOTE: Q1=B; Q2=B; Q3=C`
    - 当前可吸收的部分是：
      - `strictMode` 更像总括 filtering/gating，而不是 `close-overlap sensitivity` 本身
      - `close-overlap sensitivity + strictMode broader gating -> pocket qualify -> contained pocket -> Mature`
      - `strictMode` 不宜锁死为 `Mature` 末端 gating
    - 这与当前仓库内判断一致，并额外补强了一层：
      - `strictMode` 的 `more selective compression pockets`
      - 更像先落在 pocket qualification boundary，而不只是 `matureThreshold=80` 一侧
    - 但当前仍不能直接写成源码等价的部分也被外部回帖再次确认：
      - `strictMode` 到底是调 `compressionThreshold / matureThreshold`
      - 还是加额外必要条件
      - 还是改 `compressionScore` 计算
      - 目前仍属 `NEED_EVIDENCE`
    - 外部回帖还额外点出了一个当前缺口：
      - `close-overlap sensitivity` 的注入位置仍未确定
      - 当前仍不能写死它属于：
        - `Noise evaluation` 子项
        - `Structural containment` 子项
        - 或独立 modifier
  - 基于当前公开页参数描述，注入位点现在可再收紧一层：
    - `noiseWindow` 的说明直接写到：
      - `wick behavior, direction flips, close-to-close noise`
    - 公开页 `advanced options` 又把：
      - `wick behavior`
      - `close-overlap behavior`
      并列暴露为可调 sensitivity controls
    - 因而当前更优先怀疑：
      - `close-overlap sensitivity` 先挂在 `Noise evaluation` 一侧
      - 然后再通过 `shared pocket qualify` 间接影响 `contained pocket / containment quality`
    - 当前较不优先的写法是：
      - 直接把 `close-overlap` 主归属到 `Structural containment`
      - 或把它写成完全独立于四组件之外的第五维主评分
    - 但仍保留 `NEED_EVIDENCE`：
      - 因为公开页没有直接把 `close-overlap behavior` 点名塞进 `noiseScore` 变量名
      - 也没有给出源码级注释或函数名
  - `strictMode_kimi_followup` 的 v2 回帖又把这层口径继续收紧：
    - `VOTE: Q1=B; Q2=A; Q3=A; Q4=C`
    - 当前新增可吸收部分是：
      - `close-overlap = feature-level sensitivity`
      - `strictMode = policy-level gating / qualify strictness`
      - 当前更可能链路：
        - `close-overlap(feature sensitivity) + strictMode(policy gating) -> shared pocket qualify -> contained pocket -> Mature`
    - 这让当前排序比 v1 更窄：
      - `strictMode == close-overlap sensitivity` 可进一步排除
      - `strictMode -> Mature only` 也可进一步排除
      - 当前更优先怀疑它先作用于 `qualified compression state / compression pockets`
    - 但 v2 回帖同时继续保留的缺口是：
      - `strictMode` 具体是：
        - 抬高 `compressionThreshold`
        - 抬高 `matureThreshold`
        - 加额外必要条件
        - 还是改 `compressionScore` 公式/权重
      - 当前仍都属于 `NEED_EVIDENCE`
  - 但在“最不优先机制”这一层，当前可再收紧一格：
    - `score formula / weights rewrite` 当前最不优先
    - 原因不是已被源码否定，而是现有证据支持最弱：
      - 公开页把 `strictMode` 写成 `tighter score gates`
      - 没写成 `alternative scoring model`
      - 没写成 `adaptive weights`
      - 也没写成 `rebalanced components`
    - 同时参数区把：
      - `compressionThreshold`
      - `matureThreshold`
      - `atr/range/noise/containment weights`
      分开列示
    - 因而当前更像：
      - 先怀疑是阈值门/资格门收紧
      - 再考虑是否叠加额外 qualify 条件
      - 最后才考虑改总分合成/权重
    - 当前最稳排序可写成：
      - `threshold shift / qualify strictness`
      - `additional qualify conditions`
      - `score formula / weights rewrite`（least supported）
  - `strictMode_kimi_followup` 的 v3 回帖现已由多 AI 批次收口：
    - 当前多数票型可写成：
      - `Q1 = A`
      - `Q2 = C`
      - `Q3 = A`
    - 其中当前更值得吸收的 stable 部分是：
      - `strictMode` 更优先像：
        - `threshold shift / tighter score gates`
      - `additional qualify conditions` 继续保留为：
        - 次优残余可能
      - `score formula / weights rewrite` 继续是：
        - 最不优先机制
      - 最稳保守写法继续保持：
        - `strictMode = pocket/state qualify strictness`
        - 且上游于 `Mature`
    - 当前多数意见与已知来源语义能对齐的依据是：
      - `tighter score gates`
      - `more selective compression pockets`
      - `strictMode` 位于 `Core Engine`
      - 阈值与权重在参数分组中分开暴露
    - 当前少数保留意见是：
      - `GLM` 仍保留 `B = additional qualify conditions`
      - 因而当前不能把 `B` 彻底删除
      - 但可把优先顺序再收窄为：
        - `threshold shift / tighter score gates`
        - `additional qualify conditions`
        - `score formula / weights rewrite`
    - 当前仍不得写死成源码等价结论的部分是：
      - 具体抬的是：
        - `compressionThreshold`
        - `matureThreshold`
        - 还是两者一起
      - `additional qualify conditions` 是否只是叠加项
      - `delta` 的具体数值与分层方式
    - 当前已把“到底在盯什么”与多 AI 批次收口同时落在：
      - `strictMode_v3_监看清单_v1.md`
      - `临时粘贴区_外部AI与终端输出.md`
  - 结合源码结构顺序：
    - `Lines 121-200: Scoring engine + State machine`
    - `Lines 201-300: Pocket detection + Archive management`
    - `Lines 426-540: Ribbon + Action Engine + Event Labels`
  - 结合 `batch9_sources_kimi` 的章节顺序：
    - `State 判定` 段落写在 `Action Engine 输出` 之前
    - 因而当前更应按 `compressionScore -> state bucket -> isMature/isTight/isBuilding -> actionState` 的先后顺序审计
    - `strictMode` 若要收紧 `Mature` 或 `active` 资格，也更应优先落在 state/qualification 一侧，而不是 action label 文案末端
  - 当前更优先怀疑 `strictMode` 作用在 state/pocket qualify 之前或之内
  - 而不是在 Action Engine/visual label 的末端层才生效

## `nearEdge / releaseUp / releaseDown` 当前层级裁决

- 当前可确认：
  - `Action Engine` 是根据 `state + price position` 生成 action 标签
  - `nearEdge` 与 `releaseUp / releaseDown` 直接驱动的是建议层输出，不是四项子评分名称
  - 条件优先级还说明：
    - `releaseUp / releaseDown` 会覆盖 `Watch Edge / Monitor Mature / Track Compression / Build Context`
    - `nearEdge` 当前只在 `isMature` 前提下参与分支，不是 Loose/Tight/Building 的通用标签
  - `Compression State Change` 告警的单独存在说明：
    - `releaseUp / releaseDown` 不宜直接等同于“任意 state 发生变化”
    - 更可能是 state 之后叠加的方向性/边界事件标签
  - 页面还直接声明：
    - `It does not attempt to forecast direction`
  - 因而 `releaseUp / releaseDown` 更不应被解释成 breakout direction prediction
  - 它们更合理的定位仍是 resolved/exit 之后的复核建议标签
  - `Compression Active / Mature` alerts 的单独存在说明：
    - Action Engine 标签不是唯一的状态暴露渠道
    - `releaseUp / releaseDown` 更像告警层之后的附加解释，而不是 active/mature 的官方告警同义词
  - active zone / active state / compression window length 的直接展示也说明：
    - `active pocket` 本身就是 first-class 状态输出
    - `releaseUp / releaseDown` 更像在 active/state 基础上的后处理标签
  - `resolved compression areas` 的独立存在又补到一层边界：
    - `releaseUp / releaseDown` 更值得优先怀疑与 resolved/exit 事件相关
    - 而不只是任意 state change 的同义表达
  - `archivePockets` 的存在又说明：
    - resolved 区域很可能与 archived pockets / historical pocket display 同链路
    - 因而 `releaseUp / releaseDown` 更像 pocket 结束后的事件解释，而不一定属于主状态分箱本身
  - `projectPocketBars` 的存在又说明：
    - pocket 在图上存在向右投影/延伸展示
    - 这更像区域可视化长度控制，而不是 `releaseUp / releaseDown` 的触发信号
  - preview labels 的单独说明又补到一层边界：
    - 标签可见不等于 active confirmation
    - 因而 `releaseUp / releaseDown / Watch Edge` 这类标签也不应先被抬升为主状态成立条件
  - 结合源码结构拆解，它们更可能位于：
    - `Pocket detection + Archive management`
    - `Ribbon + Action Engine + Event Labels`
    两层的连接处
  - 而从源码顺序看：
    - `Scoring engine + State machine` 在前
    - `Action Engine + Event Labels` 在后
  - `batch9_sources_kimi` 还把：
    - `State 判定`
    - `Action Engine 输出`
    明确分成前后两个段落
  - 因而当前更应先承认：
    - 先有 `compressionScore` 与 state bucket
    - 再有 `isMature / isTight / isBuilding`
    - 最后才有 `releaseUp / releaseDown / nearEdge` 驱动的 action labels
  - 这也进一步说明：
    - `noise + containment -> Mature confirm` 应位于 `release/nearEdge` 之前
    - `releaseUp / releaseDown` 不宜倒推成 `Mature` 的前置成立条件
  - 因而 `releaseUp / releaseDown` 当前更应视为状态机之后的下游输出
  - 不应先倒推成 `compression_state` 或 pocket qualify 的前置成立条件
- 当前不可确认：
  - `nearEdge` 是否定义为价格贴近 pocket 上下沿、右侧边缘，还是别的结构边界
  - `releaseUp / releaseDown` 是否要求先处于 active pocket / mature state / state transition / resolved compression / archived pocket transition
  - preview/action labels 与 `releaseUp / releaseDown` 是否共享同一套展示开关或可见性条件
- 当前裁决：
  - 后续若继续追源码，应先把它们当成“位置事件 + 状态后处理分支”去找
  - 当前不把它们并入 `compression_quality_score` 或 `compression_state` 的核心计算段
  - 当前也不把 `releaseUp / releaseDown` 直接解释成 breakout 交易信号
  - 当前优先怀疑它们依赖：
    - `active/mature state`
    - `resolved/archived pocket transition`
    - 以及某种边界/退出事件

## `compression_state` 影子分箱口径

- 当前只做 diagnostic-only，不写入 `n01_p0_fields_runtime_v1.csv`。
- 当前影子分箱规则：
  - `Loose`: `< 62`
  - `Building`: `62-70`
  - `Tight`: `70-80`
  - `Mature`: `>= 80`
- 当前 20 组样本总分布：
  - `Loose = 118973`
  - `Building = 18035`
  - `Tight = 13851`
  - `Mature = 4201`
- 当前结论：
  - 说明“修正后的 `compression_quality_score` + 已绑定阈值骨架”具备可分箱性
  - 但不说明“已完成源码逐项等价”
  - 因此当前仍维持：只审计，不落盘

## 参数来源收严版

- 当前 `n01_p0_runtime_params_template_v1.json` 已新增：
  - `parameter_source_contract`
  - `parameter_source_detail`
- 当前按四类来源层级记录参数：
  - `source_excerpt_or_open_source`
  - `project_contract_default`
  - `stub_only_default`
  - `pending_real_binding`
- `atr_length`
  - 当前值：`14`
  - 当前层级：`source_excerpt_or_open_source`
  - 含义：已由 GainzAlgo 补充证据明确到 `ATR = SMA(True Range, default 14)`，当前可作为 v1 冻结 ATR 输入长度
- `atr_baseline_length`
  - 当前值：`50`
  - 当前层级：`source_excerpt_or_open_source`
  - 含义：已由 GainzAlgo 补充证据明确到 `default 50 bars`，当前可作为 v1 冻结 baseline 口径
- `atr_percentile_window`
  - 当前值：`252`
  - 当前层级：`project_contract_default`
  - 含义：来源页确认必须使用 rolling window，但未冻结唯一默认长度；因此 Batch9 v1 先把 `252` 冻结成比较窗口口径
- `squeeze_mode`
  - 当前值：`ttm_pro_like`
  - 当前层级：`source_excerpt_or_open_source`
  - 含义：明确表达“受 TTM Pro 类来源启发”，但不宣称已经等同于某个完整源码实现
- 当前约束：
  - 只有写清 `source_tier + source_basis + evidence_anchor + upgrade_rule` 的参数，才允许进入更严格的运行口径说明
  - 已升级为 `source_excerpt_or_open_source` 的参数，可写成“已有来源页支撑”
  - 已升级为 `project_contract_default` 的参数，可写成“Batch9 v1 冻结默认口径”

## 当前脚本接入前置件

- 当前已新增：
  - `n01_p0_fields_runtime_v1.csv`
  - `n01_p0_fields_runtime_header_v1.txt`
  - `n01_p0_runtime_gaps_v1.md`
  - `n01_p0_runtime_append_protocol_v1.md`
- 当前已新增：
  - `n01_p0_runtime_params_template_v1.json`
  - `n01_p0_runtime_append_stub_v1.py`
  - `n01_p0_runtime_append_from_proof_v1.py`
  - `n01_p0_runtime_atr_calculation_checklist_v1.md`
  - `n01_p0_real_input_mapping_draft_v1.md`
  - `real_input_samples\`
- 当前仍不代表：
  - 已接入主项目执行链路
  - 已进入策略 gate / 自动执行链路

## 当前真实 append 证据

- 当前 proof 输入：
  - `real_input_samples\n01_proof_of_mapping_output_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xauusd_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_eurusd_m15_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xauusd_m15_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_eurusd_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xauusd_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xbrusd_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_xbrusd_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_aapl_nas_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_aapl_nas_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_ustec_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_ustec_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_us500_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_us500_h4_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_de40_h1_v1.csv`
  - `real_input_samples\n01_proof_of_mapping_output_de40_h4_v1.csv`
- 当前 append 脚本：
  - `n01_p0_runtime_append_from_proof_v1.py`
- 当前 append 后主 CSV：
  - `n01_p0_fields_runtime_v1.csv`
- 当前结果摘要：
  - `EURUSD H1 proof_rows = 8976`
  - `EURUSD M15 proof_rows = 35954`
  - `EURUSD H4 proof_rows = 2248`
  - `XAUUSD H1 proof_rows = 8537`
  - `XAUUSD M15 proof_rows = 34142`
  - `XAUUSD H4 proof_rows = 2235`
  - `XBRUSD H1 proof_rows = 8016`
  - `XBRUSD H4 proof_rows = 2236`
  - `AAPL.NAS H1 proof_rows = 2517`
  - `AAPL.NAS H4 proof_rows = 719`
  - `USTEC H1 proof_rows = 8524`
  - `USTEC H4 proof_rows = 2230`
  - `US500 H1 proof_rows = 8525`
  - `US500 H4 proof_rows = 2230`
  - `DE40 H1 proof_rows = 8357`
  - `DE40 H4 proof_rows = 2194`
  - `runtime_rows_after_append = 137640`
  - `runtime_groups = AAPL.NAS H1 / AAPL.NAS H4 / DE40 H1 / DE40 H4 / EURUSD H1 / EURUSD M15 / EURUSD H4 / US500 H1 / US500 H4 / USTEC H1 / USTEC H4 / XAUUSD H1 / XAUUSD M15 / XAUUSD H4 / XBRUSD H1 / XBRUSD H4`
  - 示例行已移除

## 多 proof 收口规则

- 当一次扩样涉及多份 proof 时：
  - 不并发对同一个 `n01_p0_fields_runtime_v1.csv` 做 `--persist`
  - 统一以“proof 集合重建 runtime csv”为准
- 当前原因：
  - 并发 append 会造成读写竞争，导致 runtime 行被部分覆盖
- 当前 v1 安全口径：
  - 先分别生成 proof
  - 再按 proof 清单顺序重建 `n01_p0_fields_runtime_v1.csv`

## 历史可复现 dry-run 样例

- 历史命令样例：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_append_stub_v1.py
```

- 当前预期：
  - 只打印示例行
  - 不写回 CSV

## 历史可复现 persist 示例行

- 历史命令样例：

```powershell
python 12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\n01_p0_runtime_append_stub_v1.py --persist
```

- 历史预期：
  - 先清理占位行
  - 再清理同一条示例行的旧副本
  - 最后只保留 `1` 条示例行写回 CSV
- 这一步仍然只是脚本骨架验证，不代表当前 repo 的真实运行数据入口；仅保留历史追溯价值。

## 占位样本行规则

- 当前占位行使用：
  - `symbol = __PLACEHOLDER__`
  - `timeframe = NA`
  - `bar_time = 1970-01-01T00:00:00Z`
- 这行的作用是：
  - 验证列顺序
  - 验证 `na` 写法
  - 验证默认枚举写法
- 当第一份真实运行数据准备写入时：
  - 优先删除或覆盖这行占位数据
  - 不要把占位行和真实行长期混放

## 下一步

- 真正接入脚本或运行链路时：
  - 先处理当前占位行
  - 再往 `n01_p0_fields_runtime_v1.csv` 追加真实数据行
  - 多 proof 扩样时优先走“整包重建 runtime”而不是并发 append
  - 优先补第三周期以外的更广市场或跨变体审计，而不是继续停留在当前样本网格
  - 若表头变更，必须新增 `v2`，不覆盖 `v1`
