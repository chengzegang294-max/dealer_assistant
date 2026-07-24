import { describe, expect, it } from "vitest";

import type { EventItem } from "@/features/home/types";
import { buildStockPageViewModels } from "@/features/stock/adapters/stockPageViewModel";

describe("stockPageViewModel", () => {
  it("标的页语义组角色顺序固定为解释骨架在前、事件说明补强在后", () => {
    const selectedEvent: EventItem = {
      sourceCard: "打板资金",
      group: "关注相关",
      summary: {
        eventId: "stock-funding-20260724",
        title: "封板资金强弱发生变化",
        subject: "宁德时代",
        occurredAt: "13:20",
        holdingRelation: "关注相关",
        processStatus: "pending",
        disclosureFlag: "still_need_evidence",
      },
      explanation: {
        eventId: "stock-funding-20260724",
        title: "封板资金强弱发生变化",
        subject: "宁德时代",
        logic: "封板成功资金提升。",
        impact: "承接更稳。",
        historyAnalogy: "更像热点强化日。",
        nextReviewPoint: "复查封板成功资金。",
      },
      stockCode: "300750",
    };

    const relatedEvents: EventItem[] = [
      selectedEvent,
      {
        sourceCard: "ZSDB指数对比",
        group: "其它",
        summary: {
          eventId: "market-index-context-20260724",
          title: "指数环境强弱发生变化",
          subject: "全市场指数环境",
          occurredAt: "11:03",
          holdingRelation: "其它",
          processStatus: "pending",
          disclosureFlag: "still_need_evidence",
        },
        explanation: {
          eventId: "market-index-context-20260724",
          title: "指数环境强弱发生变化",
          subject: "全市场指数环境",
          logic: "指数转强。",
          impact: "更易承接。",
          historyAnalogy: "更接近风险偏好修复日。",
          nextReviewPoint: "复查指数方向。",
        },
      },
      {
        sourceCard: "HYDB行业对比",
        group: "其它",
        summary: {
          eventId: "market-industry-context-20260724",
          title: "所属行业强弱出现明显偏移",
          subject: "算力电源行业",
          occurredAt: "10:52",
          holdingRelation: "其它",
          processStatus: "pending",
          disclosureFlag: "still_need_evidence",
        },
        explanation: {
          eventId: "market-industry-context-20260724",
          title: "所属行业强弱出现明显偏移",
          subject: "算力电源行业",
          logic: "行业走强。",
          impact: "顺风推进。",
          historyAnalogy: "更像行业共振日。",
          nextReviewPoint: "复查行业扩散度。",
        },
      },
    ];

    const viewModels = buildStockPageViewModels({
      stockCode: "300750",
      stockName: "宁德时代",
      relatedEvents,
      selectedEvent,
      latestRecord: null,
    });

    expect(viewModels.explanationViewModel?.indicatorRoleSummaries).toEqual([
      "当前解释骨架：行业 / 指数参照",
      "当前事件说明补强：资金活跃",
    ]);
  });
});

