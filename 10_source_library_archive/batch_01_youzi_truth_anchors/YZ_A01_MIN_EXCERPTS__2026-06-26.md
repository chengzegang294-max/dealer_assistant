# YZ A01 Min Excerpts

## 对象信息

- `anchor_id`: `YZ-A01`
- `title`: `退学炒股_一万到千万的蜕变`
- `source_path`: `10_source_library_archive\raw_assets\S\02_游资悟道交割单\28位游资悟道心法\03、退学炒股心法_一万到千万的蜕变\退学炒股_一万到千万的蜕变.pdf`
- `preferred_format`: `pdf`
- `current_role`: `FIRST_PRIORITY_CANDIDATE`

## 当前结论

- 已完成首批 `3` 条最小摘录卡。
- 当前证据只支持：
  - 方法论方向
  - 纪律与回撤控制
  - 行为偏差约束
- 当前还不支持：
  - 直接升级成硬交易规则
  - 直接映射到某个既有 `Mxx` 卡号

## 摘录卡 1

- `anchor_id`: `YZ-A01`
- `page_or_loc`: `p3`
- `theme_tag`: `plan_discipline`
- `evidence_level`: `excerpt_support_but_not_full_rule`
- `quote_or_paraphrase`:
  - `不管其他股涨不涨，没有自己的标的就不买，瞎买一个就会使自己陷入被动，今天复盘做好计划明天出击。`
- `why_it_matters`:
  - 这条支持“先计划、再出击、无标的不交易”的纪律框架。
  - 可作为后续方法论卡里的“计划先于临盘冲动”证据，但还不足以单独推出完整执行门控。

## 摘录卡 2

- `anchor_id`: `YZ-A01`
- `page_or_loc`: `p4`
- `theme_tag`: `slow_down_and_reflect`
- `evidence_level`: `excerpt_support_but_not_full_rule`
- `quote_or_paraphrase`:
  - `第一步，放慢自己的脚步。第二步，保持一个平和的心态。第三步，理智思考每一个决定。第四步，学习反思提高。`
- `why_it_matters`:
  - 这条直接支持“慢即是快、先稳心态、再做决策、持续复盘”的过程性方法论。
  - 更适合归入行为与流程层，而不是具体买卖点规则。

## 摘录卡 3

- `anchor_id`: `YZ-A01`
- `page_or_loc`: `p7`
- `theme_tag`: `operation_vs_profit`
- `evidence_level`: `excerpt_support_but_not_full_rule`
- `quote_or_paraphrase`:
  - `错了就割，千万不要抱有任何幻想，将操作和盈利分别看待，它们两者没有必然联系。操作只有对错，盈利交给市场。`
- `why_it_matters`:
  - 这条支持“执行对错”和“结果盈亏”分离的思维框架，也支持止损/去幻想的基本纪律。
  - 适合作为后续风险控制类方法论卡的稳定摘录依据。

## 当前最小缺口

- 还缺：
  - `YZ-A` 主题簇与旧冻结层的行号证据继续加厚
  - `YZ-A01/A02/A03` 与旧冻结层 `Mxx` 的显式映射仍未出现

## 下一步

1. 当前继续维持 `YZ-A01` 的对象级真值锚点，不强行并旧 `Mxx` 卡号。
2. 若继续增强证据，优先补 `YZ_A_OLD_FROZEN_THEME_EVIDENCE__2026-06-26.tsv` 的行号证据。
3. 每次增强后，同步回写 `youzi_truth_anchor_manifest_v1.tsv`、批次 `README.md` 与 `S_BUCKET_02` 顶层入口。
