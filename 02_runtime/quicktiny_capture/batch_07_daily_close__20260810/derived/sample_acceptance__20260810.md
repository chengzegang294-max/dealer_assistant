# sample_acceptance__20260810

- date: `20260810`
- passed: `True`
- ladder_source: `refetch:https://stock.quicktiny.cn/api/ladder/day/20260810`
- sector_source: `refetch:https://stock.quicktiny.cn/api/sector-capital-flow/snapshot?tradeDate=20260810&universe=featured&order=desc&limit=500`
- ladder_totalStocks / rows: `99` / `99`
- sector_returned / rows: `271` / `271`
- plate_join_overlap: `39` (ratio=`1.0`)

## checks

- [PASS] `ladder_dates_non_empty` — dates_len=1
- [PASS] `ladder_date_match` — got=20260810
- [PASS] `ladder_boards_non_empty` — boards_len=4
- [PASS] `ladder_stocks_non_empty` — stock_rows=99
- [PASS] `ladder_totalStocks_vs_rows` — totalStocks=99 rows=99
- [PASS] `ladder_required_fields` — stocks_with_required_missing=0
- [PASS] `sector_success` — success=True
- [PASS] `sector_actualTradeDate_match` — got=20260810
- [PASS] `sector_rows_non_empty` — rows=271
- [PASS] `sector_returned_vs_rows` — returned=271 rows=271
- [PASS] `no_third_endpoint` — only ladder/day + sector-capital-flow/snapshot

## outputs

- ladder_raw: [ladder_day__20260810.json](file:///d:/Stock/dealer_assistant/02_runtime/quicktiny_capture/batch_07_daily_close__20260810/00_raw/ladder_day__20260810.json)
- sector_raw: [sector_capital_flow_snapshot__20260810.json](file:///d:/Stock/dealer_assistant/02_runtime/quicktiny_capture/batch_07_daily_close__20260810/00_raw/sector_capital_flow_snapshot__20260810.json)
- ladder_min_json: [ladder_day_min__20260810.json](file:///d:/Stock/dealer_assistant/02_runtime/quicktiny_capture/batch_07_daily_close__20260810/derived/ladder_day_min__20260810.json)
- ladder_min_tsv: [ladder_day_min__20260810.tsv](file:///d:/Stock/dealer_assistant/02_runtime/quicktiny_capture/batch_07_daily_close__20260810/derived/ladder_day_min__20260810.tsv)
- sector_min_json: [sector_capital_flow_min__20260810.json](file:///d:/Stock/dealer_assistant/02_runtime/quicktiny_capture/batch_07_daily_close__20260810/derived/sector_capital_flow_min__20260810.json)
- sector_min_tsv: [sector_capital_flow_min__20260810.tsv](file:///d:/Stock/dealer_assistant/02_runtime/quicktiny_capture/batch_07_daily_close__20260810/derived/sector_capital_flow_min__20260810.tsv)
- sample_acceptance_md: [sample_acceptance__20260810.md](file:///d:/Stock/dealer_assistant/02_runtime/quicktiny_capture/batch_07_daily_close__20260810/derived/sample_acceptance__20260810.md)
- sample_acceptance_json: [sample_acceptance__20260810.json](file:///d:/Stock/dealer_assistant/02_runtime/quicktiny_capture/batch_07_daily_close__20260810/derived/sample_acceptance__20260810.json)

## 一句话

- 本样本只裁 `ladder/day` 与 `sector-capital-flow/snapshot`，按最小字段合同输出 min json/tsv 并验收。
