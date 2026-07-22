// @vitest-environment jsdom

import { act } from "react";
import { createRoot } from "react-dom/client";
import { MemoryRouter, Route, Routes, useLocation } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("@/features/home/api/homeApi", async () => {
  const mockPayload = await import("@/features/home/api/mock/homeBootstrapMock");
  return {
    fetchHomeBootstrap: async () => ({
      events: mockPayload.homeBootstrapMockEvents,
      decisionRecords: mockPayload.homeBootstrapMockDecisionRecords,
    }),
  };
});

import { useHomePage } from "@/features/home/hooks/useHomePage";

type HomePageHookResult = ReturnType<typeof useHomePage>;

let latestHomePage: HomePageHookResult | null = null;
let latestPathname = "";
let latestSearch = "";

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

function HomePageProbe() {
  latestHomePage = useHomePage();
  return null;
}

function LocationProbe() {
  const location = useLocation();
  latestPathname = location.pathname;
  latestSearch = location.search;
  return null;
}

function renderHomePageHook(initialPath = "/") {
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);

  act(() => {
    root.render(
      <MemoryRouter initialEntries={[initialPath]}>
        <Routes>
          <Route path="/" element={<HomePageProbe />} />
          <Route path="/stock/:stockCode" element={<LocationProbe />} />
        </Routes>
      </MemoryRouter>,
    );
  });

  return {
    get result() {
      if (latestHomePage === null) {
        throw new Error("useHomePage result is not ready.");
      }
      return latestHomePage;
    },
    cleanup() {
      act(() => {
        root.unmount();
      });
      container.remove();
      latestHomePage = null;
      latestPathname = "";
      latestSearch = "";
    },
  };
}

async function flushBootstrap() {
  await act(async () => {
    await Promise.resolve();
  });
}

afterEach(() => {
  latestHomePage = null;
  latestPathname = "";
  latestSearch = "";
  vi.restoreAllMocks();
});

describe("useHomePage", () => {
  it("section props actions 指向 workspace handler（引用一致）", async () => {
    const homePage = renderHomePageHook();
    await flushBootstrap();

    expect(homePage.result.eventStreamPanelProps.onSelectEvent).toBe(homePage.result.handleSelectEvent);
    expect(homePage.result.homeSidebarProps.actions.onSelectEvent).toBe(homePage.result.handleSelectEvent);
    expect(homePage.result.mainWorkspacePanelProps.actions.onSubmitDecision).toBe(homePage.result.handleSubmitDecision);
    expect(homePage.result.mainWorkspacePanelProps.actions.onRetrySubmitDecision).toBe(homePage.result.handleRetrySubmitDecision);
    expect(homePage.result.stockSearchBarProps.actions.onSearchDraftChange).toBe(homePage.result.setSearchDraft);

    homePage.cleanup();
  });

  it("eventStreamPanelProps.selectedEventId 随选择事件更新", async () => {
    const homePage = renderHomePageHook();
    await flushBootstrap();

    expect(homePage.result.eventStreamPanelProps.selectedEventId).toBeNull();

    act(() => {
      homePage.result.eventStreamPanelProps.onSelectEvent("market-index-context-20260720");
    });

    expect(homePage.result.eventStreamPanelProps.selectedEventId).toBe("market-index-context-20260720");
    expect(homePage.result.selectedEventId).toBe("market-index-context-20260720");
    expect(homePage.result.mainWorkspacePanelProps.content.selectedEventSummaryViewModel).not.toBeNull();

    homePage.cleanup();
  });

  it("handleOpenFinanceDisclosure 能触发 finance-disclosure-note 的 scrollIntoView", async () => {
    const homePage = renderHomePageHook();
    await flushBootstrap();

    const target = document.createElement("div");
    target.id = "finance-disclosure-note";
    const scrollSpy = vi.fn();
    target.scrollIntoView = scrollSpy;
    document.body.appendChild(target);

    act(() => {
      homePage.result.stockSearchBarProps.actions.onOpenFinanceDisclosure();
    });

    expect(scrollSpy).toHaveBeenCalledTimes(1);

    target.remove();
    homePage.cleanup();
  });

  it("带 eventId 进入首页时会恢复当前事件工作区", async () => {
    const homePage = renderHomePageHook("/?eventId=market-index-context-20260720");
    await flushBootstrap();

    expect(homePage.result.selectedEventId).toBe("market-index-context-20260720");
    expect(homePage.result.mainWorkspacePanelProps.content.selectedEventSummaryViewModel?.title).toBe(
      "指数环境强弱发生变化",
    );
    expect(homePage.result.mainWorkspacePanelProps.content.explanationCardViewModel?.eyebrow).toBe("ExplanationCard");
    expect(homePage.result.mainWorkspacePanelProps.content.explanationCardViewModel?.blocks[0]?.content).toBe(
      "指数涨幅转强且分时承接改善，说明当前事件所处的大盘环境从中性向顺风切换。",
    );

    homePage.cleanup();
  });

  it("从首页打开标的页时会把当前事件 eventId 带入 query", async () => {
    const homePage = renderHomePageHook();
    await flushBootstrap();

    act(() => {
      homePage.result.eventStreamPanelProps.onSelectEvent("market-index-context-20260720");
    });

    act(() => {
      homePage.result.handleOpenStockPage("300750");
    });

    expect(latestPathname).toBe("/stock/300750");
    expect(latestSearch).toBe("?eventId=market-index-context-20260720");

    homePage.cleanup();
  });

  it("带空 eventId 进入首页时会在搜索区给出降级提示", async () => {
    const homePage = renderHomePageHook("/?eventId=");
    await flushBootstrap();

    expect(homePage.result.selectedEventId).toBeNull();
    expect(homePage.result.stockSearchBarProps.content.queryRecoveryNotice).toBe(
      "检测到空 eventId，当前已按首页默认空态降级展示。",
    );
    expect(homePage.result.mainWorkspacePanelProps.content.selectedEventSummaryViewModel).toBeNull();

    homePage.cleanup();
  });

  it("带无效 eventId 进入首页时会保留空态并显示提示", async () => {
    const homePage = renderHomePageHook("/?eventId=unknown-event-id");
    await flushBootstrap();

    expect(homePage.result.selectedEventId).toBeNull();
    expect(homePage.result.stockSearchBarProps.content.queryRecoveryNotice).toBe(
      "未找到 eventId=unknown-event-id 对应的首页事件，当前已回到默认空态。",
    );
    expect(homePage.result.mainWorkspacePanelProps.content.explanationCardViewModel).toBeNull();

    homePage.cleanup();
  });
});
