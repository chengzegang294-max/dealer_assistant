import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";

import Stock from "@/pages/Stock";

const mockUseStockPage = vi.fn(() => ({
  stockCode: "000001",
  hasLoaded: true,
  headerViewModel: {
    stockName: "平安银行",
    stockCode: "000001",
    holdingRelationLabel: "关注相关",
    latestEventStatusLabel: "未处理",
    sourceTags: ["ZSDB指数对比"],
  },
  relatedEventsViewModel: [
    {
      eventId: "event-1",
      title: "指数环境出现改善",
      category: "指数环境",
      occurredAt: "2026-07-24 09:30",
      processStatusLabel: "未处理",
      isSelected: true,
    },
  ],
  explanationViewModel: {
    title: "指数环境改善",
    subject: "平安银行",
    indicatorContextTags: [
      {
        label: "背景解释",
        detail: "ZSDB指数对比",
      },
    ],
    indicatorContextSummary: "当前解释先看：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照",
    indicatorRoleSummaries: ["当前解释骨架：行业 / 指数参照"],
    logic: "指数涨幅转强且承接改善。",
    impact: "当前情绪由中性向顺风切换。",
    historyAnalogy: "历史上类似阶段也先看指数顺风。",
    nextReviewPoint: "关注次日承接是否延续。",
  },
  recentRecordViewModel: null,
  qaEntryViewModel: {
    questions: ["为什么这里先看指数背景"],
    stillNeedEvidenceLabel: "still_need_evidence",
  },
  canSupplementRecord: false,
  isSupplementEditorOpen: false,
  supplementDraft: "",
  supplementError: null,
  latestSupplementEcho: null,
  setSupplementDraft: vi.fn(),
  handleSelectEvent: vi.fn(),
  handleOpenSupplementEditor: vi.fn(),
  handleSubmitSupplement: vi.fn(),
  handleOpenQaPage: vi.fn(),
  handleBackHome: vi.fn(),
}));

vi.mock("@/features/stock/hooks/useStockPage", () => ({
  useStockPage: () => mockUseStockPage(),
}));

describe("Stock page", () => {
  it("renders context summary before tags and explanation blocks", () => {
    const markup = renderToStaticMarkup(<Stock />);

    expect(markup.indexOf("当前解释先看：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照")).toBeGreaterThan(-1);
    expect(markup.indexOf("当前解释骨架：行业 / 指数参照")).toBeGreaterThan(-1);
    expect(markup.indexOf("背景解释 · ZSDB指数对比")).toBeGreaterThan(-1);
    expect(markup.indexOf("触发逻辑")).toBeGreaterThan(-1);
    expect(markup.indexOf("当前解释先看：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照")).toBeLessThan(
      markup.indexOf("当前解释骨架：行业 / 指数参照"),
    );
    expect(markup.indexOf("当前解释骨架：行业 / 指数参照")).toBeLessThan(
      markup.indexOf("背景解释 · ZSDB指数对比"),
    );
    expect(markup.indexOf("背景解释 · ZSDB指数对比")).toBeLessThan(markup.indexOf("触发逻辑"));
  });

  it("renders funding activity role summary after skeleton role", () => {
    mockUseStockPage.mockReturnValueOnce({
      ...mockUseStockPage(),
      explanationViewModel: {
        title: "榜单资金出现异动",
        subject: "平安银行",
        indicatorContextTags: [
          {
            label: "技术指标语义源",
            detail: "上榜资金",
          },
          {
            label: "背景解释",
            detail: "HYDB行业对比",
          },
          {
            label: "背景解释",
            detail: "ZSDB指数对比",
          },
        ],
        indicatorContextSummary: "当前解释先看：技术指标语义源 / 上榜资金 · 语义组：资金活跃",
        indicatorRoleSummaries: ["当前解释骨架：行业 / 指数参照", "当前事件说明补强：资金活跃"],
        logic: "榜单净额显著转强。",
        impact: "存在主动资金背书。",
        historyAnalogy: "更接近强题材扩散前的资金聚焦。",
        nextReviewPoint: "次日复查榜单净额是否延续。",
      },
    });

    const markup = renderToStaticMarkup(<Stock />);

    expect(markup.indexOf("当前解释先看：技术指标语义源 / 上榜资金 · 语义组：资金活跃")).toBeGreaterThan(-1);
    expect(markup.indexOf("当前解释骨架：行业 / 指数参照")).toBeGreaterThan(-1);
    expect(markup.indexOf("当前事件说明补强：资金活跃")).toBeGreaterThan(-1);
    expect(markup.indexOf("当前解释骨架：行业 / 指数参照")).toBeLessThan(
      markup.indexOf("当前事件说明补强：资金活跃"),
    );
    expect(markup.indexOf("当前事件说明补强：资金活跃")).toBeLessThan(
      markup.indexOf("技术指标语义源 · 上榜资金"),
    );
  });
});
