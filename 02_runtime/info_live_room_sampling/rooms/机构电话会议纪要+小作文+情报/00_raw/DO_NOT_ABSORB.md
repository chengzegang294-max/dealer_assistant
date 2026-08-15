# 本房 raw 说明（机构电话会议纪要+小作文+情报）

**状态：FROZEN_OUT F1（2026-08-13）** — 永久踢出 A 桶每日置顶/必导；不参与直播间每日流程；以后另行开研报/电话家族。

- 00_raw **保留不删**；migrate 仍可入库
- **永不**自动出 Prefill / 人读摘要 MD（`SKIP_ROOMS_USER_SAID_REDO_LATER`）
- 要导只能单独 `forced_room_anchor`，不进每日必导、不给★

历史备注：
- 2026-08-12 曾标误跑勿吸收；同日夜间重导后 raw 入库保留
- 引用时优先最大 `message_count` 的 incremental；跳过 current 0 条空壳
