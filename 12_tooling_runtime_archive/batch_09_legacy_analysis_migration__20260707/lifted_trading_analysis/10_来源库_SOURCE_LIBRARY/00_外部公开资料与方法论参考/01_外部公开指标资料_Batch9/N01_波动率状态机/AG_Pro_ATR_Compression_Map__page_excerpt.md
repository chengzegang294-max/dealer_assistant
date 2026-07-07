# AG Pro ATR Compression Map 页面摘录

- source_url: https://il.tradingview.com/script/nCbbDHVD-AG-Pro-ATR-Compression-Map-AGPro-Series/
- source_kind: TradingView open-source page
- author: AGPro Series
- capture_method: WebSearch indexed page body
- capture_date: 2026-06-12

## 关键原文摘录

- `chart-first compression analysis tool designed to evaluate how organized a low-volatility phase is and how structurally developed that contraction has become`
- `Instead of treating every quiet market phase as equally meaningful, the script separates loose and unstable contraction from cleaner, more contained compression conditions.`
- `highlights active compression zones, assigns a normalized compression score, classifies the current state of contraction, and summarizes the condition through a compact on-chart panel`
- `It does not attempt to forecast direction`
- `The script combines four internal components into a unified compression score`
- `1) ATR contraction`
- `2) Range tightness`
- `3) Noise evaluation`
- `4) Containment structure`
- `Advanced options allow stricter filtering and additional sensitivity controls for wick behavior and close-overlap behavior`
- `A shaded chart area is displayed when compression conditions are active`
- `A small panel summarizes ATR state, range state, noise condition, containment quality, overall compression score, active state, and current compression window length`
- `Compression Active` alert is triggered when compression conditions become active according to the script's scoring logic
- `Compression Mature` alert is triggered when the current state reaches Mature
- `Compression State Change` alert is triggered when the internal compression state changes
- `Improved the visual handling of resolved compression areas so the active structure remains easier to read`
- `When compression is not currently active, optional preview labels can still remain visible in a softer style`
- `Preview labels are informational only and should not be read as confirmation of an active compression state by themselves`

## 当前判断

- 这条比普通 squeeze 页更适合补 `compression quality` 这一层。
- 它不是只回答“有没有 squeeze”，而是在做：
  - 压缩是否存在
  - 压缩是否干净
  - 压缩是否逐步收敛
  - 当前压缩质量处于什么等级
- 这非常适合本仓库后续把 N01 从二元 `squeeze_on` 升级成 `compression_quality_score + compression_state`。

## 可保留细节清单

- source: TradingView indexed page body / 2026-06-12
  what: 用 normalized compression score 对压缩质量打分
  why: 适合做连续变量，不局限于二元 squeeze
  repo_mapping: N01 诊断标签候选
- source: TradingView indexed page body / 2026-06-12
  what: 四个内部组成包括 ATR contraction / range tightness / noise / containment
  why: 这是一套清晰的质量分解框架
  repo_mapping: N01 字段拆解备注
- source: TradingView indexed page body / 2026-06-12
  what: 明确声明不预测方向，只做 compression monitoring
  why: 与当前主线“先做状态机和诊断标签”高度一致
  repo_mapping: N01 定义层说明

## Kimi 二次整理稿补充

- `batch9_sources_kimi` 已补到一批对落字段很有价值的实现级细节：
  - 状态枚举：`Loose / Building / Tight / Mature`
  - 权重：`atr=30 / range=30 / noise=20 / containment=20`
  - 阈值：`compressionThreshold = 62`、`matureThreshold = 80`
  - 关键窗口：`atrLen=14`、`baselineLen=50`、`rangeWindow=20`、`noiseWindow=10`、`containmentWindow=24`
- 这让我们可以把当前理解从“有 compression score”推进到：
  - 有可落地的状态分箱
  - 有四维子评分框架
  - 有参数默认值骨架
- 同时也补到了一个有用边界：
  - `Action Engine` 更像观察建议层，如 `Review Upside / Monitor Mature / Wait Setup`
  - 不应误解成直接买卖指令
- 这轮公开页正文还补强了两个关键点：
  - `strictMode` 不应再只写成“存在一个开关”，至少可以确认它和 `stricter filtering + wick/close-overlap sensitivity` 同方向
  - `Compression Active / Compression Mature / Compression State Change` 警报说明：
    - active qualification
    - mature qualification
    - state transition
    都属于脚本内稳定暴露的分析事件层
  - 公开页同时把：
    - active compression zone
    - mini panel 的 `active state`
    - `compression window length`
    作为常规展示层暴露
  - 这进一步说明 active pocket / active state 是主状态层的一部分，不是 Action Engine 附属文案
  - 更新日志还单独提到 `resolved compression areas`
  - 这说明脚本内部至少区分：
    - active compression
    - resolved compression
    两类阶段/区域
  - 因而 `releaseUp / releaseDown` 更值得优先怀疑与 resolved/exit 事件相关，而不只是任意 state 变化
  - 更新日志还明确写出：
    - 非 active 时 preview labels 仍可见
    - 且 preview labels 不能被当成 active confirmation
  - 这进一步说明：
    - 展示标签层
    - active 状态层
    是两套不同语义，不能混写
  - 同时因为公开页没有把 `Review Upside / Review Downside` 作为 alerts 暴露，所以它们更像 Action Engine 建议标签，而不是主告警语义
- 基于当前证据，后续源码追索的优先顺序可进一步收紧为：
  - 先追 `strictMode` 是否前移到 `contained pocket / close-overlap / pocket qualify`
  - 再追 `noise/containment confirm` 如何进入 `Mature`
  - 再追 `releaseUp / releaseDown` 是否属于 resolved pocket 退出后的复核标签
- 当前仍不能直接写成已知公式的部分：
  - `strictMode` 的精确 gating 规则
  - `releaseUp / releaseDown` 的精确触发条件
  - `nearEdge` 的精确边界定义
- 对当前 N01 最有帮助的是：
  - `compression_state`
  - `compression_quality_score`
  - 后续 P1 的四项子评分候选

## 最小字段映射建议

- compression_quality_score
- compression_state
- atr_contraction_score
- range_tightness_score
- noise_cleanliness_score
- containment_score

## 抓取局限

- 当前正文文件本身仍不是原始 Pine Editor 导出，而是“索引正文 + Kimi 二次整理参数/阈值稿”的组合证据。
- 若后续用户能补源码页，优先核对：状态分箱规则、四项得分权重、panel 输出字段。
