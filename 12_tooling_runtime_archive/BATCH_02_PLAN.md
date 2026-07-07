# Tooling Runtime Archive Batch 02 Plan

## 批次目标

- 继续把旧运行时层中有长期工程价值的 MT 指标家族材料迁入新仓库。
- 本批只处理 `02_MT指标家族_源码与探针` 的最小家族集，不扩到 `03_MT4便携探针实例`。

## 本批范围

- 旧位置：
  - `旧仓库\12_工具运行时_TOOLING_RUNTIME\02_MT指标家族_源码与探针\`
- 首批候选角色：
  - 通用 probe
  - Volty 通道止损
  - XBreaking 突破探针
  - Harmony 谐波
  - ZigZag / ZUP 家族

## 本批判断原则

- 必须能代表“源码可读 / 二进制待 probe / 家族映射可写”的工程边界。
- 不承诺反编译 `ex4/ex5`。
- 不把谐波/ZigZag 直接升级成可交易门控。

## 本批验收

- `12_tooling_runtime_archive` 至少形成一份第二批回顾。
- 至少迁入一组能代表 MT 指标工程化入口的最小家族集。
- 明确家族映射、当前角色和风险边界。
