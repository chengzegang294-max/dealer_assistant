# 收口前裁决包 MFLOW provider 与样本可得性审计页

更新时间：2026-07-14

## 用途

- 这份审计页只回答一件事：
  - `MFLOW` 现在是否已经具备“值得优先审、且能较低成本形成最小审计闭环”的条件。
- 当前不回答：
  - 指标正式实现
  - 默认执行链接线
  - 第二批新批次是否立即创建

## 当前对象定位

- 对象：
  - `MFLOW`
- 当前深度：
  - `sample_contract_ready`
- 当前推荐动作：
  - 先做 provider 与样本可得性审计
- 当前不做：
  - 不直接升格为首批补采
  - 不直接进入 runtime 新开发

## 最小样本合同

- 当前仓内最小样本形状：
  - `daily_symbol_date_plus_net_inflow_buy_sell_buckets`
- 当前样本合同入口：
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/object_cards_aux_input_sample_contract_v1.tsv`
- 当前字段合同入口：
  - `01_active_objects/butler_r0_object_cards_p0/mflow_p0_a_field_contract_v1.tsv`
- 当前必须关注的核心字段：
  - `mflow_sellord_ratio`
  - `mflow_inflow_ratio`
  - `mflow_open_intent`
  - `mflow_divergence_score`
  - `mflow_net_inflow`
  - `mflow_data_mode`

## provider 候选矩阵

| provider | 当前角色 | 当前证据 | 优点 | 风险 | 当前判断 |
|---|---|---|---|---|---|
| `Tushare moneyflow + daily` | 当前仓内最接近可审计实证的路线 | 已有真实抓取脚手架、metadata、批量样本 CSV、宽表 join 结果 | 现成可跑、已在本机验证、最容易复用到审计页 | 与对象卡原始 `Wind 50因子` 口径不完全同构；部分字段需要 proxy 映射 | `首选审计入口` |
| `AkShare fund flow` | 免费替代路线 | 在文档中被列为首要免费备选，但仓内缺同等级 fresh-run 实证 | 免费、便于外部验证 | 接口稳定性和字段定义更脆弱 | `备用审计入口` |
| `Wind / iFinD` | 理想高质量路线 | 文档层强推荐，但仓内无当前用户可直接复用的实证入口 | 数据质量高、字段更完整 | 成本高、当前个人环境不现实 | `理想参考，不作当前第一刀` |

## 当前已知实证

- 仓内已经存在 `T02` 资金流验证链的真实入口与结果：
  - `fetch_t02_moneyflow_tushare_v1.py`
  - `fetch_t02_moneyflow_batch_tushare_v1.py`
  - `build_t02_real_input_v1.py`
  - `run_t02_fund_flow_scan_v1.py`
- 当前已知实跑结果包括：
  - 单标的 `moneyflow` 抓取成功
  - `sample5 / sample10 / sample20 / sample20_q2` 批量 `moneyflow` 抓取成功
  - `northbound / regime / industry` 三条辅助源抓取成功
  - `T02` 候选宽表已成功构建，且 `northbound / regime / industry` join 已命中
- 当前实证强度说明：
  - 这说明 `MFLOW` 已不再停留在“只有概念合同”的阶段
  - 但仍未证明：
    - `Tushare moneyflow` 可完整映射全部 `MFLOW` 冻结字段
    - 全市场、长时间窗、稳定字段的一致性

## 当前缺口

- `NEED_EVIDENCE: canonical provider`
  - 当前还没最终拍板：
    - `Tushare` 是否可作为 `MFLOW` 审计页的 canonical provider
    - 还是只作为当前可用 proxy 路线
- `NEED_EVIDENCE: 字段映射`
  - 当前已补字段映射与派生审计：
    - `mflow_net_inflow / mflow_inflow_ratio` 已可 `direct/proxy` 站住
    - `mflow_divergence_score` 已通过 `v0` 派生审计
  - 当前仍属硬缺口：
    - `mflow_sellord_ratio`
    - `mflow_open_intent`
  - 当前新增判断页已固定：
    - 这两个字段属于 `historical_contract_defined__current_real_source_missing`
    - 当前只有对象卡定义与 `SBKT_F014` mapping proof
    - 还不能写成当前仓内低成本可接入替代源
- `NEED_EVIDENCE: 覆盖范围`
  - 当前已有 `20` 标的跨月样本实证
  - 但还不足以直接外推成“全市场长期稳定可得”
- `NEED_EVIDENCE: 多源一致性`
  - 若未来要把 `AkShare` 作为 fallback，需要确认其字段语义与 `Tushare`/对象卡合同是否足够接近

## 当前字段映射补充

- 当前已新增一页专门的字段映射审计：
  - `收口前裁决包__MFLOW_字段映射审计页__20260714.md`
- 当前补充结论：
  - `mflow_net_inflow`
  - `mflow_inflow_ratio`
  已能由现有 `T02` 真实源直接站住
- 当前仍属硬缺口的字段主要是：
  - `mflow_sellord_ratio`
  - `mflow_open_intent`
- 当前更精确的判断不是“缺两个字段待补”这么简单，而是：
  - 这两个字段只有：
    - `历史定义层`
    - `mapping proof 层`
  - 没有：
    - `当前仓内真实抓取链`
- 因而当前最准确口径不是：
  - `MFLOW` 已完成完整字段审计
- 而是：
  - `MFLOW` 已形成可接受的 proxy 审计入口，并值得继续前推

## 风险与降级

- 当前最大风险不是“完全拿不到数据”。
- 当前最大风险是：
  - 拿得到 `moneyflow`
  - 但字段语义与对象卡原始设计不完全同构
  - 最后把 `proxy` 误写成“完全等价真值”
- 当前可接受降级口径：
  - 允许先把 `Tushare moneyflow` 视为 `审计级 proxy`
  - 不允许直接把它包装成 `Wind 50因子` 等价替身
- 若后续字段映射不能成立：
  - `MFLOW` 保持 `sample_contract_ready`
  - 不升格，不开第二批新批次

## 主负责人裁决

- 当前裁决：
  - `MFLOW` 值得先审
- 裁决原因：
  - 相比 `INSTB`，`MFLOW` 已经更接近形成最小可审计闭环
  - 仓内现有 `T02` 路线已经提供了真实抓取脚手架与批量样本证据
  - 即使最终只成立 `proxy` 版本，它对解释链和过滤层的贴合度也高于 `INSTB`
- 当前不做：
  - 不把这页等同于“MFLOW 已通过最终审计”
  - 不把这页等同于“MFLOW 已正式进入第二批新批次”
- 当前可新增的一步判断是：
  - 允许把 `MFLOW` 收口为“第二批观察中的优先审计对象”
  - 但仍不写成“字段已齐全”
  - 且不把 `sellord_ratio / open_intent` 当前缺口写成先审阻塞

## 当前最小下一步

- 1. 当前 provider / 字段映射 / divergence v0 派生审计均已补出。
- 2. 当前更顺的下一刀是二选一：
  - `收口型`：把 `MFLOW` 固定为“第二批观察中的优先审计对象”，保持 `proxy` 边界，不急着进入实现
  - `增强型`：在 `daily_tushare` 底表已就绪的前提下，把 divergence 派生链正式接入 `T02 real_input` runner 并产出 `mflow_divergence_score_v0`
- 3. 若后续仍想追求更强版本：
  - 再单独判断是否需要更高质量 provider 来补齐 `sellord_ratio / open_intent`
  - 当前对应判断页：
    - `收口前裁决包__MFLOW_sellord_open_intent_NEED_EVIDENCE与替代源判断页__20260714.md`

## 回链

- `参考交易系统补采优先级表__20260713.md`
- `收口前裁决包__MFLOW_vs_INSTB_多AI讨论前情提要与裁决框架__20260714.md`
- `收口前裁决包__MFLOW_字段映射审计页__20260714.md`
- `收口前裁决包__MFLOW_divergence_score_派生审计页__20260714.md`
- `收口前裁决包__MFLOW_sellord_open_intent_NEED_EVIDENCE与替代源判断页__20260714.md`
- `10_source_library_archive/batch_110_external_folder_absorb__20260708/00_raw_snapshot/DATA_AVAILABILITY_AUDIT_v1.0.md`
- `10_source_library_archive/batch_110_external_folder_absorb__20260708/00_raw_snapshot/DATA_PROVIDER_GUIDE_v1.0.md`
- `10_source_library_archive/batch_110_external_folder_absorb__20260708/00_raw_snapshot/OBJECT_CARD_MFLOW_P0_A__MoneyFlow_v1.0.md`
- `02_runtime/ashare_p0_first_round_validation/runtime_execution_card_v1.md`
- `02_runtime/ashare_p0_first_round_validation/runtime_provenance_note_v1.md`
