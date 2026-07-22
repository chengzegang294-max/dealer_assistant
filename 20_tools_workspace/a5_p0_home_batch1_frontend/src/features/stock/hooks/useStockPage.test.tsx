// @vitest-environment jsdom

import { act } from "react";
import { createRoot } from "react-dom/client";
import { MemoryRouter, Route, Routes } from "react-router-dom";
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

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

function StockPageProbe() {
  latestStockPage = useStockPage();
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
});
