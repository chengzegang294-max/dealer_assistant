# Batch 23 - TOOLING_RUNTIME mt4_probe_instance config text recovered batch1 - EVAL - 2026-06-24

## 目标

- land the readable text recovery pack for the `mt4_probe_instance` config snapshot as auditable inspection evidence
- keep the batch limited to the recovered text directory plus batch docs/scripts

## 范围

- target root:
  - `12_工具运行时_TOOLING_RUNTIME/mt4_probe_instance/config/00_text_recovered_batch1`

## 阅读结果

- `README_batch1.md` defines the directory as readable text exports only
- `servers.ini` is decoded as `latin-1` and re-saved as `utf-8` for inspection
- other exported files are normalized readable copies, while private or binary-like configs are intentionally skipped
- this makes the directory a clean frozen inspection slice and avoids mixing original MT4 runtime state into the repo

## 四分流裁决

- absorbed now:
  - `mt4_probe_instance/config/00_text_recovered_batch1`
- reopen later:
  - only if a future recovered batch is exported
- future bucket:
  - original binary/private configs and any broader MT4 probe runtime tree
- source-only for this cut:
  - parallel duplicate or alternate export locations outside this exact target path

## 裁决

- `Batch 23` should contain only `mt4_probe_instance/config/00_text_recovered_batch1` plus the batch docs/scripts
- do not widen this cut to the full `mt4_probe_instance` tree or any alternate duplicate recovery directory
- do not mix any other runtime snapshot or the large `03_Kimi拆书待入库` deletion cluster into this cut
