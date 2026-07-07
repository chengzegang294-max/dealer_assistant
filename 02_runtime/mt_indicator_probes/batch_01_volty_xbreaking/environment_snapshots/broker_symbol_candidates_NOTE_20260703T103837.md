# MT5 Broker Symbol Candidate Extraction Note

- stamp: `20260703T103837`
- input_kind: `MetaQuotes Terminal bases/*/symbols/*.dat`
- method: `ASCII + UTF-16LE string scan -> symbol-like regex filter`
- caveat: 这些 `.dat` 不是公开文档格式，输出是“候选 symbol 字符串集合”，更接近 MarketWatch/selected 的近似，不等同于 broker 全量可交易品种清单。

## Inputs / Outputs
- `ICMarketsSC-Demo__52886989_selected`
  - input: `C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\AC48B16F101CC6359ADC4B870ED6B744\bases\ICMarketsSC-Demo\symbols\selected-52886989.dat`
  - output: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\environment_snapshots\broker_symbol_candidates_ICMarketsSC-Demo__52886989_selected_20260703T103837.txt`
  - candidate_count: `29`
- `ICMarketsSC-Demo__52886989_symbols`
  - input: `C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\AC48B16F101CC6359ADC4B870ED6B744\bases\ICMarketsSC-Demo\symbols\symbols-52886989.dat`
  - output: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\environment_snapshots\broker_symbol_candidates_ICMarketsSC-Demo__52886989_symbols_20260703T103837.txt`
  - candidate_count: `1742`
- `TradeMaxGlobal-Demo__60088394_selected`
  - input: `C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\C9F9BDDC460DF35F331B73B79A3DD57C\bases\TradeMaxGlobal-Demo\symbols\selected-60088394.dat`
  - output: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\environment_snapshots\broker_symbol_candidates_TradeMaxGlobal-Demo__60088394_selected_20260703T103837.txt`
  - candidate_count: `39`
- `TradeMaxGlobal-Demo__60088394_symbols`
  - input: `C:\Users\91883\AppData\Roaming\MetaQuotes\Terminal\C9F9BDDC460DF35F331B73B79A3DD57C\bases\TradeMaxGlobal-Demo\symbols\symbols-60088394.dat`
  - output: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\environment_snapshots\broker_symbol_candidates_TradeMaxGlobal-Demo__60088394_symbols_20260703T103837.txt`
  - candidate_count: `185`

## Suggested Next Step (if needs exact list)
- 在 MT5 端通过脚本导出 `SymbolsTotal/SymbolName` 得到全量 MarketWatch 与全量 Symbols 列表（需要 MT5 端执行权限与脚本落盘）。
