import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";

import Home from "@/pages/Home";

vi.mock("@/features/home/hooks/useHomePage", () => ({
  useHomePage: () => ({
    heroViewModel: {
      eyebrow: "A股 P0 Batch1",
      title: "今日事件流工作台",
      description: "围绕今日事件流展开。",
      axisTitle: "首页唯一主轴：今日事件流",
      axisSummary: "当前事件总数 6 / 待处理 2",
      totalEvents: 6,
      queuedEventCount: 2,
      statusMetrics: [
        {
          title: "市场宽度",
          value: "热度抬升，指数顺风，行业共振开始增强",
          hint: "市场宽度语义组（沪深涨跌停），只做首页轻背景说明",
        },
        {
          title: "待处理事件",
          value: "2 条",
          hint: "点击右侧摘要可回流到主工作区",
        },
        {
          title: "风险提示",
          value: "still_need_evidence",
          hint: "当前只做解释增强，不做交易判断。",
        },
      ],
    },
    eventStreamPanelProps: {
      eventCards: [
        {
          eventId: "market-index-context-20260720",
          title: "指数环境强弱发生变化",
          subject: "全市场指数环境",
          occurredAt: "11:03",
          holdingRelation: "其它",
          disclosureFlag: "still_need_evidence",
          sourceCard: "ZSDB指数对比",
          processStatus: "pending",
        },
      ],
      selectedEventId: "market-index-context-20260720",
      onSelectEvent: vi.fn(),
    },
    stockSearchBarProps: {
      viewModel: {
        entryLabel: "StockSearchEntry",
        placeholder: "输入标的代码，例如 300750",
        openActionLabel: "发出打开动作",
        disclosureButtonLabel: "查看限制说明",
      },
      content: {
        searchDraft: "",
        searchActionEcho: null,
        queryRecoveryNotice: null,
      },
      actions: {
        onSearchDraftChange: vi.fn(),
        onOpenStockPage: vi.fn(),
        onOpenFinanceDisclosure: vi.fn(),
      },
    },
    mainWorkspacePanelProps: {
      viewModel: {
        eyebrow: "MainWorkspacePanel",
        title: "主工作区",
        description: "这里同时承接选中事件摘要、解释卡、决策记录草稿和提交回显。",
        emptyStateTitle: "先从左侧选一条今日事件",
        emptyStateDescription: "空状态不提前展示草稿或旧回显。",
      },
      content: {
        selectedEventSummaryViewModel: {
          eyebrow: "SelectedEventSummaryBar",
          title: "指数环境强弱发生变化",
          metaLine: "全市场指数环境 · 11:03 · 其它",
          processStatus: "pending",
          disclosureFlag: "still_need_evidence",
          workspaceState: "selected",
        },
        explanationCardViewModel: {
          eyebrow: "ExplanationCard",
          sourceTags: [
            {
              label: "背景解释",
              detail: "ZSDB指数对比",
            },
          ],
          sourceSummaryLine: "当前优先回链：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照",
          blocks: [
            {
              title: "触发逻辑",
              content: "指数涨幅转强且分时承接改善。",
            },
          ],
          openStockActionLabel: null,
          stockCode: null,
        },
        decisionRecordFormViewModel: {
          eyebrow: "DecisionRecordForm",
          description: "这里只服务当前事件。",
          draftEventLabel: "draft.eventId = market-index-context-20260720",
          actionField: {
            label: "动作",
            placeholder: "选择动作",
            options: ["继续观察"],
          },
          reasonTagField: {
            label: "原因标签",
            placeholder: "选择原因标签",
            options: ["环境顺风"],
          },
          horizonField: {
            label: "观察周期",
            placeholder: "选择观察周期",
            options: ["1-3天"],
          },
          noteLabel: "备注",
          notePlaceholder: "记录为什么继续观察。",
          submitButtonLabel: "提交记录",
          retryButtonLabel: "清空回显继续编辑",
        },
        homeRecordDraft: {
          eventId: "market-index-context-20260720",
          action: "",
          reasonTag: "",
          horizon: "",
          note: "",
        },
        latestSubmitEcho: null,
        formError: null,
      },
      actions: {
        onChangeDecisionDraft: vi.fn(),
        onSubmitDecision: vi.fn(),
        onRetrySubmitDecision: vi.fn(),
        onOpenStockPage: vi.fn(),
      },
    },
    homeSidebarProps: {
      viewModel: {
        queuedEventCards: [],
        queuedEmptyMessage: "当前没有待处理事件。",
        recentRecordCards: [],
        financeDisclosureLabel: "still_need_evidence",
        financeDisclosureDetail: "当前只做解释增强，不做价格预测。",
      },
      actions: {
        onSelectEvent: vi.fn(),
      },
    },
  }),
}));

describe("Home page", () => {
  it("renders market width hero card together with explanation card summary", () => {
    const markup = renderToStaticMarkup(<Home />);

    const marketWidthTitleIndex = markup.indexOf("市场宽度");
    const marketWidthHintIndex = markup.indexOf("市场宽度语义组（沪深涨跌停），只做首页轻背景说明");
    const explanationSummaryIndex = markup.indexOf("当前优先回链：背景解释 / ZSDB指数对比 · 语义组：行业 / 指数参照");

    expect(marketWidthTitleIndex).toBeGreaterThan(-1);
    expect(marketWidthHintIndex).toBeGreaterThan(-1);
    expect(explanationSummaryIndex).toBeGreaterThan(-1);
    expect(marketWidthTitleIndex).toBeLessThan(explanationSummaryIndex);
    expect(marketWidthHintIndex).toBeLessThan(explanationSummaryIndex);
  });
});
