import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";

import StockQa from "@/pages/StockQa";

const mockUseStockQaPage = vi.fn(() => ({
  stockCode: "000001",
  stockName: "平安银行",
  selectedEventTitle: "指数环境出现改善",
  selectedEventSubject: "平安银行",
  hasLoaded: true,
  questionGroups: [
    {
      title: "技术指标释义组",
      description: "解释当前上下文里的指标来源。",
      questions: ["ZSDB指数对比 这里在提示什么"],
    },
  ],
  selectedQuestion: "ZSDB指数对比 这里在提示什么",
  answerViewModel: {
    question: "ZSDB指数对比 这里在提示什么",
    groupTitle: "技术指标释义组",
    contextPrioritySummary: "当前回答优先回链：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照",
    contextRoleSummaries: ["当前解释骨架：行业 / 指数参照"],
    sourceFieldLabels: ["ZSDB指数对比", "触发逻辑", "影响推演"],
    sourceSummary: "当前回答回链到事件字段。",
    coreAnswer: "指数顺风说明当前事件所处环境改善。",
    nextActions: ["回到标的页继续看解释"],
    limitReminder: "当前只解释已有上下文，不做价格预测。",
  },
  latestRecord: null,
  stillNeedEvidenceLabel: "still_need_evidence",
  setSelectedQuestion: vi.fn(),
  handleBackStock: vi.fn(),
}));

vi.mock("@/features/stock/hooks/useStockQaPage", () => ({
  useStockQaPage: () => mockUseStockQaPage(),
}));

describe("StockQa page", () => {
  it("renders context summary before field tags and core answer", () => {
    const markup = renderToStaticMarkup(<StockQa />);
    const sourcePanelIndex = markup.indexOf("事件与字段来源条");
    const sourceSummaryIndex = markup.indexOf("当前回答回链到事件字段。");
    const coreAnswerPanelIndex = markup.lastIndexOf("核心回答区");
    const contextSummaryIndex = markup.indexOf("当前回答优先回链：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照");
    const roleSummaryIndex = markup.indexOf("当前解释骨架：行业 / 指数参照");

    expect(contextSummaryIndex).toBeGreaterThan(-1);
    expect(roleSummaryIndex).toBeGreaterThan(-1);
    expect(sourcePanelIndex).toBeGreaterThan(-1);
    expect(sourceSummaryIndex).toBeGreaterThan(-1);
    expect(coreAnswerPanelIndex).toBeGreaterThan(-1);
    expect(sourcePanelIndex).toBeLessThan(coreAnswerPanelIndex);
    expect(contextSummaryIndex).toBeLessThan(coreAnswerPanelIndex);
    expect(roleSummaryIndex).toBeLessThan(coreAnswerPanelIndex);
    expect(contextSummaryIndex).toBeLessThan(sourceSummaryIndex);
    expect(roleSummaryIndex).toBeLessThan(sourceSummaryIndex);
  });

  it("renders funding activity role summary in source panel", () => {
    mockUseStockQaPage.mockReturnValueOnce({
        stockCode: "000001",
        stockName: "平安银行",
        selectedEventTitle: "榜单资金出现异动",
        selectedEventSubject: "平安银行",
        hasLoaded: true,
        questionGroups: [
          {
            title: "技术指标释义组",
            description: "解释当前上下文里的指标来源。",
            questions: ["上榜资金 这里在提示什么"],
          },
        ],
        selectedQuestion: "上榜资金 这里在提示什么",
        answerViewModel: {
          question: "上榜资金 这里在提示什么",
          groupTitle: "技术指标释义组",
          contextPrioritySummary: "当前回答优先回链：技术指标语义源 / 上榜资金 · 语义组：资金活跃",
          contextRoleSummaries: ["当前事件说明补强：资金活跃"],
          sourceFieldLabels: ["上榜资金", "触发逻辑", "影响推演"],
          sourceSummary: "当前回答回链到事件字段。",
          coreAnswer: "榜单净额显著转强，说明存在主动资金背书。",
          nextActions: ["回到标的页继续看解释"],
          limitReminder: "当前只解释已有上下文，不做价格预测。",
        },
        latestRecord: null,
        stillNeedEvidenceLabel: "still_need_evidence",
        setSelectedQuestion: vi.fn(),
        handleBackStock: vi.fn(),
      });

    const markup = renderToStaticMarkup(<StockQa />);

    expect(markup.indexOf("当前回答优先回链：技术指标语义源 / 上榜资金 · 语义组：资金活跃")).toBeGreaterThan(-1);
    expect(markup.indexOf("当前事件说明补强：资金活跃")).toBeGreaterThan(-1);
    expect(markup.indexOf("当前事件说明补强：资金活跃")).toBeLessThan(markup.indexOf("当前回答回链到事件字段。"));
  });
});
