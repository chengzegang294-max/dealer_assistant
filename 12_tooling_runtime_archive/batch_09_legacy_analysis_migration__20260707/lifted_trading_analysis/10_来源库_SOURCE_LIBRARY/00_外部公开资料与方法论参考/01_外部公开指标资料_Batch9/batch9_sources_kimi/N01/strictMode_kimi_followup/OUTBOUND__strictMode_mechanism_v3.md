# OUTBOUND: strictMode mechanism v3

## TASK

- 只基于 EVIDENCE PACK，继续把 `strictMode` 的“具体机制”压窄。
- 这次不要重复讨论：
  - `strictMode != close-overlap sensitivity`
  - `close-overlap = feature-level sensitivity`
  - `strictMode = policy-level gating`
- 这些已经是当前前提。
- 这次只判断：
  - `strictMode` 更像抬阈值
  - 还是加额外 qualify 条件
  - 还是改 `compressionScore` 合成/权重

## HARD RULES

- 只能使用 EVIDENCE PACK。
- 不允许编造源码、函数、变量名、公式。
- 若证据不足，必须写 `NEED_EVIDENCE`。
- 不允许把 `releaseUp / releaseDown` 倒推成状态机前置条件。

## EVIDENCE PACK

### Evidence 1

Path:
- `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\N01_波动率状态机\AG_Pro_ATR_Compression_Map__page_excerpt.md`

Quoted lines:

```text
The script combines four internal components into a unified compression score
1) ATR contraction
2) Range tightness
3) Noise evaluation
4) Containment structure

Advanced options allow stricter filtering and additional sensitivity controls for wick behavior and close-overlap behavior
```

### Evidence 2

Path:
- `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\batch9_sources_kimi\N01\03_ag_pro_atr_compression_map_tradingview.md`

Quoted lines:

```text
- compressionThreshold: 62.0
  - Minimum score required for qualified compression state

- matureThreshold: 80.0
  - Higher score for mature compression when noise and containment confirm

- strictMode: false
  - Applies tighter score gates for more selective compression pockets

- atrWeight: 30.0
- rangeWeight: 30.0
- noiseWeight: 20.0
- containmentWeight: 20.0
```

### Evidence 3

Current accepted intermediate conclusion:

```text
close-overlap = feature-level sensitivity
strictMode = policy-level gating / qualify strictness
close-overlap(feature sensitivity) + strictMode(policy gating) -> shared pocket qualify -> contained pocket -> Mature
```

## QUESTIONS

Q1:
- 当前更优先的机制是什么？
  - A = `strictMode` 更像 threshold shift（先抬 `compressionThreshold`，也可能连带更严 `matureThreshold`）
  - B = `strictMode` 更像 additional qualify conditions（在既有阈值外再加条件）
  - C = `strictMode` 更像 score formula / weights rewrite
  - D = NEED_EVIDENCE，当前还不能排出 A/B/C

Q2:
- 仅凭现有证据，哪种最不优先？
  - A = threshold shift
  - B = additional qualify conditions
  - C = score formula / weights rewrite
  - D = NEED_EVIDENCE

Q3:
- 当前最稳的保守写法是什么？
  - A = `strictMode` 更像 pocket/state qualify strictness，上游于 `Mature`
  - B = `strictMode` 主要改四项权重
  - C = `strictMode` 主要改 Action labels

## OUTPUT CONTRACT

先输出一行：

```text
VOTE: Q1=<A/B/C/D>; Q2=<A/B/C/D>; Q3=<A/B/C>
```

然后输出 3-6 条 bullets：
- 每条必须引用 EVIDENCE PACK 的原句或路径
- 若证据不足，明确写：
  - `NEED_EVIDENCE: <缺什么>`

最后输出：

```text
NEXT_ACTIONS:
- <最多 2 条可验证动作>
```
