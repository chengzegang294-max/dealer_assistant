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

import { useStockPage } from "@/features/stock/hooks/useStockPage";

type StockPageHookResult = ReturnType<typeof useStockPage>;

let latestStockPage: StockPageHookResult | null = null;
let latestPathname = "";
let latestSearch = "";

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

function StockPageProbe() {
  latestStockPage = useStockPage();
  return null;
}

function LocationProbe() {
  const location = useLocation();
  latestPathname = location.pathname;
  latestSearch = location.search;
  return null;
}

function renderStockPageHook(initialPath = "/stock/300750") {
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);

  act(() => {
    root.render(
      <MemoryRouter initialEntries={[initialPath]}>
        <Routes>
          <Route path="/stock/:stockCode" element={<StockPageProbe />} />
          <Route path="/" element={<LocationProbe />} />
        </Routes>
      </MemoryRouter>,
    );
  });

  return {
    get result() {
      if (latestStockPage === null) {
        throw new Error("useStockPage result is not ready.");
      }
      return latestStockPage;
    },
    cleanup() {
      act(() => {
        root.unmount();
      });
      container.remove();
      latestStockPage = null;
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
  latestStockPage = null;
  latestPathname = "";
  latestSearch = "";
  vi.restoreAllMocks();
});

describe("useStockPage", () => {
  it("默认加载标的直接相关事件并选中第一条", async () => {
    const stockPage = renderStockPageHook();
    await flushBootstrap();

    expect(stockPage.result.headerViewModel.stockCode).toBe("300750");
    expect(stockPage.result.headerViewModel.stockName).toBe("宁德时代");
    expect(stockPage.result.relatedEventsViewModel).toHaveLength(3);
    expect(stockPage.result.selectedEventId).toBe("stock-trigger-point-20260720-300750");
    expect(stockPage.result.explanationViewModel?.title).toBe("个股出现启动候选信号");

    stockPage.cleanup();
  });

  it("切换相关事件后会同步更新解释区", async () => {
    const stockPage = renderStockPageHook();
    await flushBootstrap();

    act(() => {
      stockPage.result.handleSelectEvent("market-index-context-20260720");
    });

    expect(stockPage.result.selectedEventId).toBe("market-index-context-20260720");
    expect(stockPage.result.explanationViewModel?.title).toBe("指数环境强弱发生变化");

    stockPage.cleanup();
  });

  it("命中已有记录的事件时允许进入补充记录入口", async () => {
    const stockPage = renderStockPageHook();
    await flushBootstrap();

    act(() => {
      stockPage.result.handleSelectEvent("market-index-context-20260720");
    });

    expect(stockPage.result.canSupplementRecord).toBe(true);
    expect(stockPage.result.recentRecordViewModel?.action).toBe("继续观察");

    act(() => {
      stockPage.result.handleOpenSupplementEditor();
    });

    expect(stockPage.result.isSupplementEditorOpen).toBe(true);

    stockPage.cleanup();
  });

  it("空备注提交时保留草稿并给出失败提示", async () => {
    const stockPage = renderStockPageHook();
    await flushBootstrap();

    act(() => {
      stockPage.result.handleSelectEvent("market-index-context-20260720");
    });
    act(() => {
      stockPage.result.handleOpenSupplementEditor();
    });
    act(() => {
      stockPage.result.setSupplementDraft("   ");
    });
    act(() => {
      stockPage.result.handleSubmitSupplement();
    });

    expect(stockPage.result.isSupplementEditorOpen).toBe(true);
    expect(stockPage.result.supplementError).toBe("请先填写补充备注，再提交。");
    expect(stockPage.result.latestSupplementEcho).toBeNull();

    stockPage.cleanup();
  });

  it("补充记录成功后会生成最近一次补充回显", async () => {
    vi.spyOn(Date.prototype, "toLocaleString").mockReturnValue("2026/07/22 01:08:00");

    const stockPage = renderStockPageHook();
    await flushBootstrap();

    act(() => {
      stockPage.result.handleSelectEvent("market-index-context-20260720");
    });
    act(() => {
      stockPage.result.handleOpenSupplementEditor();
    });
    act(() => {
      stockPage.result.setSupplementDraft("补充：指数环境转强后，先继续观察量能延续。");
    });
    act(() => {
      stockPage.result.handleSubmitSupplement();
    });

    expect(stockPage.result.isSupplementEditorOpen).toBe(false);
    expect(stockPage.result.supplementError).toBeNull();
    expect(stockPage.result.latestSupplementEcho).toEqual({
      note: "补充：指数环境转强后，先继续观察量能延续。",
      submittedAt: "2026/07/22 01:08:00",
    });

    stockPage.cleanup();
  });

  it("返回首页时会把当前事件上下文带回首页 query", async () => {
    const stockPage = renderStockPageHook();
    await flushBootstrap();

    act(() => {
      stockPage.result.handleSelectEvent("market-index-context-20260720");
    });

    act(() => {
      stockPage.result.handleBackHome();
    });

    expect(latestPathname).toBe("/");
    expect(latestSearch).toBe("?eventId=market-index-context-20260720");

    stockPage.cleanup();
  });
});
