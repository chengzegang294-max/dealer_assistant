# Provenance

更新时间：2026-07-14

## 来源与范围

- 对象：`YTC`
- 目标：补 `60m/5m` 小样本入口
- 证据模式：
  - `sample_data_snapshot`
  - `external_vendor_package_snapshot`
  - `provider_note`
- 当前证据强度：
  - `active`

## 当前来源

- 当前已纳入的分钟样本来源：
  - 外部数据仓：`E:\股票历史数据`
  - 包路径：`E:\股票历史数据\分钟K线-股票241\2000-2025\按年\5分钟\2024.zip`
  - 包内条目：`2024/sh601991.csv`
  - 下载方式：`百度网盘`
  - 淘宝店铺：`INJOY杂货铺`
- 生成方式：
  - `601991_SH_5m.csv`
    - 由外部历史分钟包按窗口 `2024-03-01 09:30:00` 到 `2024-04-10 15:00:00` 截取得到
  - `601991_SH_60m.csv`
    - 由 `601991_SH_5m.csv` 按 session bucket `10:30 / 11:30 / 14:00 / 15:00` 本地聚合得到
- producer：
  - `external_vendor_package_user_downloaded`
- 说明：
  - 当前已确认资料主要来自 `百度网盘`
  - 当前已确认淘宝真实店铺应为 `INJOY杂货铺`
  - 当前仍未确认具体商品标题与分享链接，先按外部下载包吸收，不伪装成当前终端从官方 provider 直连生成

## 当前缺口

- 当前已纳入：
  - `daily+weekly` 历史锚点
  - 外部历史分钟包裁切得到的 `5m` 实物样本
  - 由 `5m` 聚合得到的 `60m` 实物样本
  - 分钟样本 provider 与降级口径说明
  - 仓内搜索状态
  - provider 候选矩阵
  - 最小补采路径
  - 接收合同
  - provenance 模板
  - `60m` live probe 摘录
  - provider 限频阻塞说明
- 当前仍缺：
  - 外部卖家元信息若后续可补，则补进 provenance note
  - 更大时间窗或更多 symbol 的统一吸收策略暂不在本批次内展开
- 缺口以 `YTC_SAMPLE_REQUIREMENT_v1.tsv` 为准。
