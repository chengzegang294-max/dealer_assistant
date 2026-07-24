import { describe, expect, it } from "vitest";

import { createHomeHeroViewModel } from "@/features/home/adapters/homeTopSectionViewModel";
import type { EventItem } from "@/features/home/types";
import { buildStockPageViewModels } from "@/features/stock/adapters/stockPageViewModel";
import {
  buildIndicatorSemanticRoleSummaries,
  getIndicatorSemanticGroupHint,
} from "@/features/indicator/utils/semanticGroups";
import { buildIndicatorContextSummary, createIndicatorContextTag } from "@/features/indicator/utils/contextPriority";

function makeEvent(args: {
  eventId: string;
  title: string;
  subject: string;
  occurredAt: string;
  holdingRelation: EventItem["summary"]["holdingRelation"];
  processStatus: EventItem["summary"]["processStatus"];
  disclosureFlag: string;
  sourceCard: string;
  group: EventItem["group"];
  stockCode?: string;
}): EventItem {
  return {
    summary: {
      eventId: args.eventId,
      title: args.title,
      subject: args.subject,
      occurredAt: args.occurredAt,
      holdingRelation: args.holdingRelation,
      processStatus: args.processStatus,
      disclosureFlag: args.disclosureFlag,
    },
    explanation: {
      eventId: args.eventId,
      title: args.title,
      subject: args.subject,
      logic: "只做解释增强，不做交易判断。",
      impact: "只做解释增强，不做交易判断。",
      historyAnalogy: "只做解释增强，不做交易判断。",
      nextReviewPoint: "只做解释增强，不做交易判断。",
    },
    sourceCard: args.sourceCard,
    stockCode: args.stockCode,
    group: args.group,
  };
}

describe("semanticGroups cross-page contract", () => {
  it("home market width hint comes from shared semantic group helper", () => {
    const heroViewModel = createHomeHeroViewModel({
      totalEvents: 6,
      queuedEventCount: 2,
      marketSummary: "热度抬升，指数顺风，行业共振开始增强",
      holdingRiskHint: "只做解释增强，不做交易判断",
      disclosureLabel: "still_need_evidence",
    });

    expect(heroViewModel.statusMetrics[0]?.title).toBe("市场宽度");
    expect(heroViewModel.statusMetrics[0]?.hint).toBe(getIndicatorSemanticGroupHint("market_width"));
  });

  it("context summary group label is aligned with role summaries", () => {
    const tag = createIndicatorContextTag("ZSDB指数对比");
    const contextSummary = buildIndicatorContextSummary("当前回答优先回链", tag);
    const roleSummaries = buildIndicatorSemanticRoleSummaries([tag.detail]);

    expect(contextSummary).toBe("当前回答优先回链：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照");
    expect(roleSummaries).toEqual(["当前解释骨架：行业 / 指数参照"]);
  });

  it("stock role summaries are ordered as industry skeleton then funding support", () => {
    const relatedEvents: EventItem[] = [
      makeEvent({
        eventId: "stock-funding-20260720",
        title: "资金活跃出现增强",
        subject: "宁德时代",
        occurredAt: "10:55",
        holdingRelation: "持仓相关",
        processStatus: "pending",
        disclosureFlag: "still_need_evidence",
        sourceCard: "上榜资金",
        group: "持仓相关",
        stockCode: "300750",
      }),
      makeEvent({
        eventId: "market-industry-context-20260720",
        title: "行业相对强弱发生变化",
        subject: "全市场行业环境",
        occurredAt: "10:30",
        holdingRelation: "其它",
        processStatus: "pending",
        disclosureFlag: "still_need_evidence",
        sourceCard: "HYDB行业对比",
        group: "其它",
      }),
      makeEvent({
        eventId: "market-index-context-20260720",
        title: "指数环境强弱发生变化",
        subject: "全市场指数环境",
        occurredAt: "10:20",
        holdingRelation: "其它",
        processStatus: "pending",
        disclosureFlag: "still_need_evidence",
        sourceCard: "ZSDB指数对比",
        group: "其它",
      }),
    ];

    const viewModels = buildStockPageViewModels({
      stockCode: "300750",
      stockName: "宁德时代",
      relatedEvents,
      selectedEvent: relatedEvents[0] ?? null,
      latestRecord: null,
    });

    expect(viewModels.explanationViewModel?.indicatorRoleSummaries).toEqual([
      "当前解释骨架：行业 / 指数参照",
      "当前事件说明补强：资金活跃",
    ]);
  });

  it("qa funding context summary is aligned with funding role summary", () => {
    const tag = createIndicatorContextTag("上榜资金");
    const contextSummary = buildIndicatorContextSummary("当前回答优先回链", tag);
    const roleSummaries = buildIndicatorSemanticRoleSummaries([tag.detail]);

    expect(contextSummary).toBe("当前回答优先回链：技术指标语义源 / 上榜资金 · 语义组：资金活跃");
    expect(roleSummaries).toEqual(["当前事件说明补强：资金活跃"]);
  });

  it("home explanation context summary keeps the same shared output format", () => {
    const tag = createIndicatorContextTag("沪深涨跌停");
    const contextSummary = buildIndicatorContextSummary("当前优先回链", tag);

    expect(contextSummary).toBe("当前优先回链：技术指标语义源 / 沪深涨跌停 · 语义组：市场宽度");
  });
});
