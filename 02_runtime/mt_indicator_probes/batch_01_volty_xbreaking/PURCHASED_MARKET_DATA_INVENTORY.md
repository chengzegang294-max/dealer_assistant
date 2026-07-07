# Purchased Market Data Inventory

## 当前结论

- 用户已明确确认：外汇、股指、黄金都买过并补充过历史数据。
- 当前“已购数据”在仓库中已经确认有两条证据链：
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\VTMarkets-Live 2\` 下的 `HST` 历史文件
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` 根目录本层的 `CSV/XLSX` 文件
- 当前没有一套全仓统一的 `paid_data` 或 `purchased` 元数据标签。
- 当前最稳定的文件级特殊标记是：
  - 外汇/贵金属历史文件大量使用 `VIP*.hst`
  - 股指历史文件位于同一目录，但多数采用 `指数代码.周期.hst` 命名，而不是 `VIP` 前缀
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` 根目录本层的直购文件则主要依靠“位于 data 根目录 + csv/xlsx 格式 + 用户明确确认”来识别
- 当前对 `C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\` 的补充扫描未发现 `VIP` 命名文件，因此“已购数据”的强证据根仍以旧仓 `VTMarkets-Live 2` 历史目录和旧仓 `data` 根目录为准

## 扫描摘要

- 扫描时间：`2026-07-02`
- 扫描范围 A：`12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\VTMarkets-Live 2\*.hst`
- 扫描结果：
  - `vip_total = 137`
  - `fx_vip_count = 113`
  - `metal_vip_count = 17`
  - `index_count = 28`
- 扫描范围 B：`12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` 根目录本层 `*.csv / *.xls / *.xlsx`
- 扫描结果：
  - `root_total = 41`
  - `root_fx_count = 19`
  - `root_metal_count = 3`
  - `root_index_count = 6`
  - `root_commodity_count = 5`
  - `root_macro_count = 8`

## 资产分类表

| 资产类 | 特别标记 | 证据路径 | 代表文件 | 当前判断 |
| --- | --- | --- | --- | --- |
| 外汇 | `VIP*.hst` | `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\VTMarkets-Live 2\` | `EURUSD-VIP60.hst`, `GBPUSD-VIP60.hst`, `USDJPY-VIP60.hst`, `AUDUSD-VIP60.hst` | 属于已购买/已补充的外汇历史数据主证据 |
| 黄金/白银 | `VIP*.hst` | `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\VTMarkets-Live 2\` | `XAUUSD-VIP60.hst`, `XAUUSD-VIP240.hst`, `XAGUSD-VIP60.hst`, `XAGUSD-VIP240.hst` | 属于已购买/已补充的贵金属历史数据主证据 |
| 股指 | 同目录但多为 `代码.周期.hst` | `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\VTMarkets-Live 2\` | `DJ30.60.hst`, `NAS100.60.hst`, `SP500.60.hst`, `US2000.60.hst`, `CHINA50.60.hst` | 位于同一历史数据根目录，当前可视为同批补充的数据资产 |
| 外汇 | `data` 根目录 `CSV` | `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` | `eurusd_1h.csv`, `gbpusd_1h.csv`, `usdjpy_1h.csv`, `audusd_1h.csv` | 用户已确认这些根目录 `csv` 属于直购数据，当前作为第二条外汇已购证据链 |
| 黄金/白银 | `data` 根目录 `CSV` | `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` | `xauusd_1h.csv`, `xagusd_1h.csv`, `_xau_test_1h.csv` | 用户已明确确认 `_xau_test_1h.csv` 属于买过的数据；同目录同批金银 `csv` 视为同类已购资产 |
| 股指 | `data` 根目录 `CSV` | `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` | `US30_1h.csv`, `nas100_1h.csv`, `us500_1h.csv`, `GER30_1h.csv` | 用户已确认 data 根目录的 `csv/xlsx` 是买过的数据，当前可视为第二条股指已购证据链 |
| 宏观/附加 | `data` 根目录 `CSV/XLSX` | `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` | `macro_1h_20240101_20260525.csv`, `econ_calendar_utc.csv`, `标普500波动率指数_VIX_day.xlsx`, `美国国债收益率2年+10年期.xlsx` | 这些也位于用户确认的已购 data 根目录内，当前先登记为已购研究数据补充层 |

## 已被工程链消费的硬证据

- 当前最直接被脚本实际消费的已购数据文件是：
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\03_MT4便携探针实例\history\VTMarkets-Live 2\EURUSD-VIP60.hst`
- 它已被 `fill_mt4_eurusd_h1_history_v1.py` 用于给旧 MT4 实例补 `EURUSD60.hst` 缺失 bar，证据见：
  - `artifacts\volty\history_patch\fill_mt4_eurusd_h1_history_latest.json`
- 当前该历史补丁的关键事实包括：
  - `source_record_count = 27518`
  - `inserted_records = 23974`
  - `window = 2025-01-02 ~ 2025-01-15`
- 当前 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\_xau_test_1h.csv` 也已被明确识别为用户买过的数据样本；当前它尚未直接并入 `XBreaking` 主线默认输入，但已经作为迁移清单中的强提示样本固定下来

## 特别标记说明

- 若后续再问“哪些是之前买的数据”，当前最实用的判断顺序是：
  1. 先看是否位于 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` 根目录本层，且为 `csv/xls/xlsx`
  2. 再看是否位于 `VTMarkets-Live 2` 目录
  3. 若位于 `VTMarkets-Live 2`，优先看是否带 `VIP` 命名
  4. 若不带 `VIP`，但属于同目录下的 `DJ30 / NAS100 / SP500 / US2000 / CHINA50` 这类指数 `.hst` 文件，也应视为同批历史数据资产
- 因此：
  - 外汇、黄金在 `VTMarkets-Live 2` 里的特别标记非常明显，主要就是 `VIP*.hst`
  - 股指在 `VTMarkets-Live 2` 里的特别标记不在文件名，而在“与 VIP 文件同目录、同批出现”的目录级证据
  - `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` 根目录这批已购文件的特别标记不在文件名，而在“根目录本层 csv/xlsx + 用户明确确认”的仓内事实

## 当前作用

- 这份清单的作用不是把所有旧历史数据立刻并入当前主线默认输入，而是先把“你买过什么、现在仓库里能证明什么”固定成可回溯事实。
- 当前主线真正已经消费并形成工程闭环的，是 `EURUSD-VIP60.hst -> fill_mt4_eurusd_h1_history_v1.py -> history_patch artifact` 这一条。
- 其余 `VTMarkets-Live 2` 历史文件以及 `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data\` 根目录直购 `csv/xlsx` 当前先记录为：
  - `historical_recovered`
  - `inventory_evidence`
  - `not_yet_consumed_by_current_xbreaking_mainline`

## 消费状态映射

| 证据链 | 资产组 | 代表文件 | 当前新仓消费状态 | 当前消费者/证据 | 下一步迁移动作 |
| --- | --- | --- | --- | --- | --- |
| `VTMarkets-Live 2` HST | 外汇 | `EURUSD-VIP60.hst` | 已被新仓脚本实际消费 | `fill_mt4_eurusd_h1_history_v1.py` -> `artifacts\volty\history_patch\fill_mt4_eurusd_h1_history_latest.json` | 继续梳理其余 `VIP*.hst` 是否需要进入 MT4/MT5 历史补丁链 |
| `VTMarkets-Live 2` HST | 其余外汇 | `GBPUSD-VIP60.hst`, `USDJPY-VIP60.hst`, `AUDUSD-VIP60.hst` | 已登记，尚未发现当前新仓自动消费者 | 当前仅在本清单与溯源文档中固化 | 评估是否需要为非 EURUSD 品种增加 history patch 或导入链 |
| `VTMarkets-Live 2` HST | 黄金/白银 | `XAUUSD-VIP60.hst`, `XAGUSD-VIP60.hst` | 已登记，尚未发现当前新仓自动消费者 | 当前仅在本清单与溯源文档中固化 | 评估是否需要转入黄金/白银历史补丁或对照数据入口 |
| `VTMarkets-Live 2` HST | 股指 | `DJ30.60.hst`, `NAS100.60.hst`, `SP500.60.hst` | 已登记，尚未发现当前新仓自动消费者 | 当前仅在本清单与溯源文档中固化 | 评估是否需要转为股指历史导入链 |
| `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data` 根目录 CSV | 外汇 | `eurusd_1h.csv`, `gbpusd_1h.csv`, `usdjpy_1h.csv` | 已登记，当前未接入 `XBreaking` 主线默认输入 | 当前仅在本清单中固定为直购数据证据 | 可优先做 `CSV -> 标准化输入契约` 映射 |
| `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data` 根目录 CSV | 黄金/白银 | `xauusd_1h.csv`, `xagusd_1h.csv`, `_xau_test_1h.csv` | 已登记，当前未接入 `XBreaking` 主线默认输入 | `_xau_test_1h.csv` 已被用户明确点名确认为已购样本 | 可优先做黄金 CSV 的字段契约与来源比对 |
| `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data` 根目录 CSV | 股指 | `US30_1h.csv`, `nas100_1h.csv`, `us500_1h.csv`, `GER30_1h.csv`, `ger40_1h.csv` | 已登记，当前未接入 `XBreaking` 主线默认输入 | 当前仅在本清单中固定为直购数据证据 | 后续可与第二环境股指 probe 结果做字段对照 |
| `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data` 根目录 CSV | 股指历史命名 | `GER30_1h.csv` | 已登记，当前已确认不能直接作为 TMGM tester symbol | 当前可作为旧仓德指历史命名证据 | 后续字段对齐与消费者映射应优先收敛到 `GER40` |
| `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data` 根目录 CSV/XLSX | 宏观/附加 | `macro_1h_20240101_20260525.csv`, `econ_calendar_utc.csv`, `标普500波动率指数_VIX_day.xlsx` | 已在旧仓梳理文档出现，但未接入当前 `XBreaking` 主线 | `00_entry\OLD_REPO_FILE_SWEEP_TASKBOARD.md` 等旧仓迁移文档已有 object map 线索 | 后续按旧仓 sweep 文档把宏观族整理进新仓数据契约 |

## 文件级映射

### `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\data` 根目录直购文件

- `P1 / metal`: `_xau_test_1h.csv`, `xauusd_1h.csv`, `xagusd_1h.csv`
- `P1 / fx`: `eurusd_1h.csv`, `gbpusd_1h.csv`, `usdjpy_1h.csv`
- `P1 / index`: `US30_1h.csv`, `nas100_1h.csv`
- `P2 / fx`: `AUDJPY_1h.csv`, `AUDNZD_1h.csv`, `audusd_1h.csv`, `CADJPY_1h.csv`, `CHFJPY_1h.csv`, `EURAUD_1h.csv`, `EURCHF_1h.csv`, `EURGBP_1h.csv`, `eurjpy_1h.csv`, `EURNZD_1h.csv`, `GBPCHF_1h.csv`, `gbpjpy_1h.csv`, `NZDJPY_1h.csv`, `nzdusd_1h.csv`, `usdcad_1h.csv`, `usdchf_1h.csv`
  - 当前已新增第二环境锚点：`audusd_1h.csv <-> AUDUSD/H1/H4`、`usdchf_1h.csv <-> USDCHF/H1/H4`、`usdcad_1h.csv <-> USDCAD/H1/H4`、`nzdusd_1h.csv <-> NZDUSD/H1/H4`、`eurjpy_1h.csv <-> EURJPY/H1/H4`、`gbpjpy_1h.csv <-> GBPJPY/H1/H4`、`EURGBP_1h.csv <-> EURGBP/H1/H4`、`CHFJPY_1h.csv <-> CHFJPY/H1/H4`、`EURCHF_1h.csv <-> EURCHF/H1/H4`、`AUDJPY_1h.csv <-> AUDJPY/H1/H4`、`AUDNZD_1h.csv <-> AUDNZD/H1/H4`、`CADJPY_1h.csv <-> CADJPY/H1/H4`、`EURAUD_1h.csv <-> EURAUD/H1/H4`、`GBPCHF_1h.csv <-> GBPCHF/H1/H4`、`EURNZD_1h.csv <-> EURNZD/H1/H4`、`NZDJPY_1h.csv <-> NZDJPY/H1/H4`
- `P2 / index`: `GBRIDXGBP_1h.csv`, `GER30_1h.csv`, `ger40_1h.csv`, `us500_1h.csv`
  - 当前 index 侧已形成证据分流：`ger40_1h.csv <-> GER40/H1/H4`、`us500_1h.csv <-> US500/H1/H4`、`GBRIDXGBP_1h.csv <-> UK100/H1/H4`；`GER30_1h.csv` 当前仍只形成“旧命名不可直接当 TMGM tester symbol 使用”的失败别名证据
- `P2 / commodity`: `dollaridxusd_1h.csv`, `UKOIL_1h.csv`, `usoil_1h.csv`, `XCUUSD_1h.csv`, `xtiusd_1h.csv`
  - 当前 commodity 侧已形成证据分流：`usoil_1h.csv` 与 `xtiusd_1h.csv` 当前都优先收敛到 `XTIUSD/H1/H4` 对照链，`UKOIL_1h.csv` 当前优先收敛到 `XBRUSD/H1/H4` 对照链，`dollaridxusd_1h.csv` 当前优先收敛到 `USIDX/H1/H4` 对照链；`XCUUSD_1h.csv` 当前除旧命名失败外，还补齐了 `COPPERCMDUSD` 候选 alias 的失败探测证据
- `P2 / macro`: `econ_calendar_1h_flags_20240101_20260525.csv`, `econ_calendar_utc.csv`, `macro_1h_20240101_20260525.csv`, `news_2007-01 to 2026-05 CSV; sorted date, time; UTC.csv`, `us_yield_2y10y_1d.csv`, `vix_1d.csv`, `标普500波动率指数_VIX_day.xlsx`, `美国国债收益率2年+10年期.xlsx`

### 优先级说明

- `P1`：优先与当前主线最相关，适合先做 `CSV -> 标准化输入契约 -> 消费者脚本` 映射
- `P2`：先保留为迁移库存，待 `P1` 完成后再按资产族补消费者与字段契约

## P1 候选消费者映射

| 文件 | 资产组 | 当前状态 | 候选消费者/入口 | 说明 |
| --- | --- | --- | --- | --- |
| `eurusd_1h.csv` | 外汇 | 已购直购 CSV，未接入当前主线 | `XBreaking` 标准化输入契约草案；可与 `run_xbreaking_probe_once.ps1` 的 `EURUSD/H1` 对照样本做字段比对 | 与当前第二环境 `EURUSD/H1` 样本最接近，适合先做字段对齐 |
| `gbpusd_1h.csv` | 外汇 | 已购直购 CSV，未接入当前主线 | `XBreaking` 标准化输入契约草案；可与 `GBPUSD/H1` 对照样本做字段比对 | 当前仓内已有 `GBPUSD/H1` 跨环境硬证据 |
| `usdjpy_1h.csv` | 外汇 | 已购直购 CSV，未接入当前主线 | `XBreaking` 标准化输入契约草案；可与 `USDJPY/H1` 对照样本做字段比对 | 当前仓内已有 `USDJPY/H1` 跨环境硬证据 |
| `audusd_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `AUDUSD/H1` 和 `AUDUSD/H4` 对照样本做字段比对 | 本轮已新增 `AUDUSD/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `usdchf_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `USDCHF/H1` 和 `USDCHF/H4` 对照样本做字段比对 | 本轮已新增 `USDCHF/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `usdcad_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `USDCAD/H1` 和 `USDCAD/H4` 对照样本做字段比对 | 本轮已新增 `USDCAD/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `nzdusd_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `NZDUSD/H1` 和 `NZDUSD/H4` 对照样本做字段比对 | 本轮已新增 `NZDUSD/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `eurjpy_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `EURJPY/H1` 和 `EURJPY/H4` 对照样本做字段比对 | 本轮已新增 `EURJPY/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `gbpjpy_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `GBPJPY/H1` 和 `GBPJPY/H4` 对照样本做字段比对 | 本轮已新增 `GBPJPY/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `EURGBP_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `EURGBP/H1` 和 `EURGBP/H4` 对照样本做字段比对 | 本轮已新增 `EURGBP/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `CHFJPY_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `CHFJPY/H1` 和 `CHFJPY/H4` 对照样本做字段比对 | 本轮已新增 `CHFJPY/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `EURCHF_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `EURCHF/H1` 和 `EURCHF/H4` 对照样本做字段比对 | 本轮已新增 `EURCHF/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `AUDNZD_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `AUDNZD/H1` 和 `AUDNZD/H4` 对照样本做字段比对 | 本轮已新增 `AUDNZD/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `CADJPY_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `CADJPY/H1` 和 `CADJPY/H4` 对照样本做字段比对 | 本轮已新增 `CADJPY/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `EURAUD_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `EURAUD/H1` 和 `EURAUD/H4` 对照样本做字段比对 | 本轮已新增 `EURAUD/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `GBPCHF_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `GBPCHF/H1` 和 `GBPCHF/H4` 对照样本做字段比对 | 本轮已新增 `GBPCHF/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `EURNZD_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `EURNZD/H1` 和 `EURNZD/H4` 对照样本做字段比对 | 本轮已新增 `EURNZD/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `AUDJPY_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `AUDJPY/H1` 和 `AUDJPY/H4` 对照样本做字段比对 | 本轮已新增 `AUDJPY/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `NZDJPY_1h.csv` | 外汇 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 标准化输入契约草案；可与 `NZDJPY/H1` 和 `NZDJPY/H4` 对照样本做字段比对 | 本轮已新增 `NZDJPY/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `xauusd_1h.csv` | 黄金 | 已购直购 CSV，未接入当前主线 | `XBreaking` 标准化输入契约草案；可与 `XAUUSD/H1` 对照样本做字段比对 | 当前仓内已有 `XAUUSD/H1` 跨环境硬证据 |
| `xagusd_1h.csv` | 白银 | 已购直购 CSV，未接入当前主线 | `XBreaking` 标准化输入契约草案；可与 `XAGUSD/H1` 对照样本做字段比对 | 当前仓内已新增 `XAGUSD/H1` 跨环境硬证据 |
| `_xau_test_1h.csv` | 黄金测试样本 | 已购直购 CSV，用户明确点名 | `XBreaking` 黄金 CSV 字段契约入口 | 文件名带 `test`，适合作为旧仓黄金 CSV 的优先解剖样本 |
| `US30_1h.csv` | 股指 | 已购直购 CSV，未接入当前主线 | `XBreaking` 股指 CSV 字段契约草案；可与 `US30/H1` 对照样本做字段比对 | 当前仓内已有 `US30/H1` 跨环境硬证据 |
| `nas100_1h.csv` | 股指 | 已购直购 CSV，未接入当前主线默认输入 | `XBreaking` 指数字段契约草案；可与 `NAS100/H1` 和 `NAS100/H4` 对照样本做字段比对 | 当前仓内已新增 `NAS100/H1/H4` 跨环境硬证据，可从高优先库存推进到字段对齐 |
| `us500_1h.csv` | 股指 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 指数字段契约草案；可与 `US500/H1` 和 `US500/H4` 对照样本做字段比对 | 本轮已新增 `US500/H1/H4` 跨环境硬证据，可把旧仓 `us500_1h.csv` 推进到字段对齐 |
| `ger40_1h.csv` | 股指 | 已购直购 CSV，当前已拥有第二环境对照样本 | `XBreaking` 指数字段契约草案；可与 `GER40/H1` 和 `GER40/H4` 对照样本做字段比对 | 本轮已新增 `GER40/H1/H4` 跨环境硬证据，并接替成为当前 bootstrap seed |
| `GER30_1h.csv` | 股指 | 已购直购 CSV，当前已确认是历史命名别名证据 | `XBreaking` 指数字段契约草案；当前应优先对照 `GER40/H1` 和 `GER40/H4` 样本 | 本轮已确认 `GER30/H1` 在 TMGM 第二环境下会报 `symbol GER30 not exist` |
| `UKOIL_1h.csv` | 商品 | 已购直购 CSV，当前已拥有可用 broker alias 对照样本 | `XBreaking` 商品字段契约草案；当前应优先对照 `XBRUSD/H1` 和 `XBRUSD/H4` 样本 | 本轮已确认 `UKOIL/H1` 是旧命名失败证据，但 `XBRUSD/H1/H4` 可作为 Brent 商品主线别名样本 |
| `dollaridxusd_1h.csv` | 宏观/美元指数 | 已购直购 CSV，当前已拥有可用 broker alias 对照样本 | `XBreaking` 美元指数字段契约草案；当前应优先对照 `USIDX/H1` 和 `USIDX/H4` 样本 | 本轮已确认 `DOLLARIDXUSD/H1` 是旧命名失败证据，`USDX/H1` 与 `DXY/H1` 是候选 alias 失败证据，但 `USIDX/H1/H4` 可作为美元指数主线别名样本 |

## P1 字段契约草案入口

- 目标：先把 `P1` 直购 `csv` 收敛到一套最小可比对字段，再决定是否接成新仓默认输入
- 首批优先字段：
  - 时间锚点：`time/timestamp/datetime`
  - K 线数值：`open/high/low/close`
  - 辅助量列：`tick_volume/volume`，若存在则保留
  - 来源补充：`symbol/timeframe` 优先由文件名与目录上下文补齐
- 当前对照锚点：
  - `eurusd_1h.csv` <-> `EURUSD/H1`
  - `gbpusd_1h.csv` <-> `GBPUSD/H1`
  - `usdjpy_1h.csv` <-> `USDJPY/H1`
  - `audusd_1h.csv` <-> `AUDUSD/H1` 与 `AUDUSD/H4`
  - `usdchf_1h.csv` <-> `USDCHF/H1` 与 `USDCHF/H4`
  - `usdcad_1h.csv` <-> `USDCAD/H1` 与 `USDCAD/H4`
  - `nzdusd_1h.csv` <-> `NZDUSD/H1` 与 `NZDUSD/H4`
  - `eurjpy_1h.csv` <-> `EURJPY/H1` 与 `EURJPY/H4`
  - `gbpjpy_1h.csv` <-> `GBPJPY/H1` 与 `GBPJPY/H4`
  - `EURGBP_1h.csv` <-> `EURGBP/H1` 与 `EURGBP/H4`
  - `CHFJPY_1h.csv` <-> `CHFJPY/H1` 与 `CHFJPY/H4`
  - `EURCHF_1h.csv` <-> `EURCHF/H1` 与 `EURCHF/H4`
  - `AUDJPY_1h.csv` <-> `AUDJPY/H1` 与 `AUDJPY/H4`
  - `AUDNZD_1h.csv` <-> `AUDNZD/H1` 与 `AUDNZD/H4`
  - `CADJPY_1h.csv` <-> `CADJPY/H1` 与 `CADJPY/H4`
  - `EURAUD_1h.csv` <-> `EURAUD/H1` 与 `EURAUD/H4`
  - `GBPCHF_1h.csv` <-> `GBPCHF/H1` 与 `GBPCHF/H4`
  - `EURNZD_1h.csv` <-> `EURNZD/H1` 与 `EURNZD/H4`
  - `NZDJPY_1h.csv` <-> `NZDJPY/H1` 与 `NZDJPY/H4`
  - `xauusd_1h.csv` <-> `XAUUSD/H1`
  - `xagusd_1h.csv` <-> `XAGUSD/H1`
  - `US30_1h.csv` <-> `US30/H1`
  - `nas100_1h.csv` <-> `NAS100/H1` 与 `NAS100/H4`
  - `us500_1h.csv` <-> `US500/H1` 与 `US500/H4`
  - `ger40_1h.csv` <-> `GER40/H1` 与 `GER40/H4`
  - `GER30_1h.csv` <-> 旧命名别名证据（当前优先转向 `GER40/H1` 与 `GER40/H4`）
  - `UKOIL_1h.csv` <-> `XBRUSD/H1` 与 `XBRUSD/H4`
  - `dollaridxusd_1h.csv` <-> `USIDX/H1` 与 `USIDX/H4`
  - `usoil_1h.csv` <-> `XTIUSD/H1` 与 `XTIUSD/H4`
  - `xtiusd_1h.csv` <-> `XTIUSD/H1` 与 `XTIUSD/H4`
- 当前入口角色：这部分仍是 `draft_contract_entry`，用于指导下一轮实现 `CSV -> 标准化输入契约 -> 消费者脚本`，不是马上替换当前 `XBreaking` 主线默认输入

## 股指历史命名备注

- 当前 `TMGM / TradeMaxGlobal-Demo__60088394` 环境下，`GER30` 直接作为 tester symbol 会报 `symbol GER30 not exist`
- 当前同一环境下，`GBRIDXGBP` 直接作为 tester symbol 也会报 `symbol GBRIDXGBP not exist`
- 当前同一环境下，已确认可用 broker alias 为 `UK100`，且已补齐第二环境跨月长窗口对照归档：`uk100_h1_tmgm_longwin_20260703T111446` 与 `uk100_h4_tmgm_longwin_20260703T111446`
- 同一条德指主线已确认可用 symbol 为 `GER40/H1` 与 `GER40/H4`
- 对旧仓 `GER30_1h.csv` 的迁移含义：
  - 当前不能继续把 `GER30` 当默认 tester symbol
  - 后续字段对齐与消费者映射优先对照 `GER40/H1/H4`
  - `GER30_1h.csv` 可保留为“历史命名证据 + 数据源别名输入”，但运行入口要优先收敛到 `GER40`
- 对旧仓 `GBRIDXGBP_1h.csv` 的迁移含义：
  - 当前不能继续把 `GBRIDXGBP` 当默认 tester symbol
  - 当前已收敛到可用 broker alias：`UK100/H1/H4`（见 `uk100_h1_tmgm_longwin_20260703T111446` / `uk100_h4_tmgm_longwin_20260703T111446`）
  - 后续字段对齐与消费者映射优先对照 `UK100/H1/H4`，同时保留 `GBRIDXGBP_1h.csv` 作为“历史命名证据 + 数据源别名输入”

## 商品 Broker Alias 备注

- 当前 `TMGM / TradeMaxGlobal-Demo__60088394` 环境下，`USOIL` 直接作为 tester symbol 会报 `symbol USOIL not exist`
- 当前同一环境下，`UKOIL` 直接作为 tester symbol 也会报 `symbol UKOIL not exist`
- 当前同一环境下，`XCUUSD` 直接作为 tester symbol 也会报 `symbol XCUUSD not exist`
- 当前同一环境下，`DOLLARIDXUSD` 直接作为 tester symbol 也会报 `symbol DOLLARIDXUSD not exist`
- 当前同一环境下，`COPPERCMDUSD`、`USDX` 与 `DXY` 作为候选 alias 也都会报 `symbol not exist`
- 当前公开 `TMGM Trading Hours / Swap Free Account` 页面把 `CHCUSD` 明确列为 `CHINA A50`，而不是铜类 instrument；当前公开 `Precious Metals` 页面只列 `XAUUSD / XAGUSD / XPTUSD`
- 同一轮商品主线复跑已确认可用别名是 `XTIUSD/H1` 与 `XTIUSD/H4`、`XBRUSD/H1` 与 `XBRUSD/H4`，以及 `USIDX/H1` 与 `USIDX/H4`
- 对旧仓 `data` 根目录商品 CSV 的迁移含义：
  - `usoil_1h.csv` 当前优先对照 `XTIUSD/H1` 与 `XTIUSD/H4`
  - `xtiusd_1h.csv` 当前也优先对照 `XTIUSD/H1` 与 `XTIUSD/H4`
  - `UKOIL_1h.csv` 已完成一次第二环境实际 symbol 探测，虽然 `UKOIL` 本身在 TMGM 下不可直接使用，但当前已识别并实跑通过可用 broker alias `XBRUSD/H1/H4`
  - `XCUUSD_1h.csv` 已完成一次第二环境实际 symbol 探测，且候选 alias `COPPERCMDUSD` 也已探测失败；同时公共产品面已排除 `CHCUSD` 这条 `CHINA A50` 假候选，并且截至当前公开金属列表仍未发现 TMGM 对外暴露的铜类 instrument ticker；后续不要继续把 `XCUUSD / COPPERCMDUSD / CHCUSD` 当默认 symbol
  - `dollaridxusd_1h.csv` 已完成一次第二环境实际 symbol 探测，虽然 `DOLLARIDXUSD` 本身在 TMGM 下不可直接使用，且候选 alias `USDX / DXY` 也已探测失败，但当前已识别并实跑通过可用 broker alias `USIDX/H1/H4`

## 可执行入口草案

- 当前已实现入口：`normalize_purchased_csv_contract_v1.py`
- 目标：把旧仓已购 `csv` 统一标准化成新仓可消费的最小输入层，而不是直接把原始 CSV 硬接到主线脚本
- 当前已内置批量入口：`--preset p1_core`
  - 作用：不再依赖手工逐条传 `--input`，可直接按 `P1` 核心集合批量生成 preview contract 归档
  - 当前预设覆盖：`eurusd_1h / gbpusd_1h / usdjpy_1h / xauusd_1h / xagusd_1h / _xau_test_1h / US30_1h / nas100_1h / usoil_1h / xtiusd_1h`
- 当前已扩展 `P2` 批量入口（均为“OHLC + volume”类型 CSV；不包含 `econ_calendar / news / yield / vix` 这类非 OHLC 契约文件）：
  - `--preset p2_ohlc_fx`：`audusd_1h / nzdusd_1h / usdcad_1h / usdchf_1h / eurjpy_1h / gbpjpy_1h / AUDJPY_1h / AUDNZD_1h / CADJPY_1h / CHFJPY_1h / EURAUD_1h / EURCHF_1h / EURGBP_1h / EURNZD_1h / GBPCHF_1h / NZDJPY_1h`
  - `--preset p2_ohlc_indices`：`ger40_1h / us500_1h / GER30_1h / GBRIDXGBP_1h`
  - `--preset p2_ohlc_commodity_macro`：`UKOIL_1h / XCUUSD_1h / dollaridxusd_1h`
  - `--preset p2_ohlc_all`：以上三组的并集
- 首批输入范围：
  - `eurusd_1h.csv`
  - `gbpusd_1h.csv`
  - `usdjpy_1h.csv`
  - `xauusd_1h.csv`
  - `xagusd_1h.csv`
  - `_xau_test_1h.csv`
  - `US30_1h.csv`
  - `nas100_1h.csv`
  - `usoil_1h.csv`
  - `xtiusd_1h.csv`
- 首批输出契约：
  - 必含 `time, open, high, low, close`
  - 可选 `tick_volume` 或 `volume`
  - 由标准化层补齐 `symbol` 与 `timeframe`
  - 商品别名通过映射表统一，例如 `usoil_1h.csv -> XTIUSD`
- 当前角色：`implementation_entry_ready`，已把“已购 CSV 清单”推进到“可执行标准化脚本入口”
- 当前预览归档：
  - `artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T0428\`（首份小样本）
    - `xauusd_1h.csv -> xauusd_1h__normalized.csv`，`row_count = 60969`
    - `nas100_1h.csv -> nas100_1h__normalized.csv`，`row_count = 68961`
    - `usoil_1h.csv -> usoil_1h__normalized.csv`，当前已按 broker alias 归一到 `symbol = XTIUSD`，`row_count = 13933`
  - `artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T0702\`（扩容到 P1 核心集合，`sample_count = 10`）
    - `eurusd_1h.csv`：`row_count = 64699`
    - `gbpusd_1h.csv`：`row_count = 64897`
    - `usdjpy_1h.csv`：`row_count = 64897`
    - `xagusd_1h.csv`：`row_count = 61417`
    - `US30_1h.csv`：`row_count = 77149`
    - `_xau_test_1h.csv`：`row_count = 512`
    - `xtiusd_1h.csv`：`row_count = 83535`
  - `artifacts\purchased_csv_contract_preview\p1_contract_preview_20260702T1730\`（`--preset p1_core` 首次实跑归档，`sample_count = 10`）
    - `_xau_test_1h.csv -> _xau_test_1h__normalized.csv`，当前已显式归一到 `symbol = XAUUSD`，`row_count = 512`
    - `usoil_1h.csv -> usoil_1h__normalized.csv`，当前仍按 broker alias 归一到 `symbol = XTIUSD`
    - 其余 `P1` 样本与 `p1_contract_preview_20260702T0702` 保持同口径批量输出
  - `artifacts\purchased_csv_contract_preview\p2_contract_preview_20260703T1115\`（`--preset p2_ohlc_all` 首次批量入口实跑，`sample_count = 23`）
    - `UKOIL_1h.csv` 当前在标准化层按 broker alias 归一到 `symbol = XBRUSD`（与第二环境 alias 结论一致）
    - `dollaridxusd_1h.csv` 当前在标准化层按 broker alias 归一到 `symbol = USIDX`（与第二环境 alias 结论一致）
    - `GER30_1h.csv` 当前在标准化层按 broker alias 归一到 `symbol = GER40`（与第二环境 alias 结论一致）
- 当前索引与验收入口：
  - 索引：`artifacts\purchased_csv_contract_preview\purchased_csv_contract_preview_index_latest.json`（latest=`p2_contract_preview_20260703T1115`）
  - 验收：`acceptance_snapshots\purchased_csv_contract_preview_acceptance_latest.json`（`next_actions=[]`）
