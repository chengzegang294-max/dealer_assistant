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

import { useStockQaPage } from "@/features/stock/hooks/useStockQaPage";

type StockQaHookResult = ReturnType<typeof useStockQaPage>;

let latestStockQa: StockQaHookResult | null = null;

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

function StockQaProbe() {
  latestStockQa = useStockQaPage();
  return null;
}

function renderStockQaHook(initialPath = "/stock/300750/qa?eventId=market-index-context-20260720") {
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);

  act(() => {
    root.render(
      <MemoryRouter initialEntries={[initialPath]}>
        <Routes>
          <Route path="/stock/:stockCode/qa" element={<StockQaProbe />} />
        </Routes>
      </MemoryRouter>,
    );
  });

  return {
    get result() {
      if (latestStockQa === null) {
        throw new Error("useStockQaPage result is not ready.");
      }
      return latestStockQa;
    },
    cleanup() {
      act(() => {
        root.unmount();
      });
      container.remove();
      latestStockQa = null;
    },
  };
}

async function flushBootstrap() {
  await act(async () => {
    await Promise.resolve();
  });
}

afterEach(() => {
  latestStockQa = null;
  vi.restoreAllMocks();
});

describe("useStockQaPage", () => {
  it("默认按 query 中的事件进入问答上下文", async () => {
    const qaPage = renderStockQaHook();
    await flushBootstrap();

    expect(qaPage.result.stockName).toBe("宁德时代");
    expect(qaPage.result.selectedEventTitle).toBe("指数环境强弱发生变化");
    expect(qaPage.result.selectedQuestion).toBe("这次事件为什么触发");
    expect(qaPage.result.answerBlocks).toHaveLength(5);

    qaPage.cleanup();
  });

  it("切换推荐问题时会更新占位回答", async () => {
    const qaPage = renderStockQaHook();
    await flushBootstrap();

    act(() => {
      qaPage.result.setSelectedQuestion("上次为什么这样记录");
    });

    expect(qaPage.result.selectedQuestion).toBe("上次为什么这样记录");
    expect(qaPage.result.answerBlocks[0]?.content).toContain("上次为什么这样记录");
    expect(qaPage.result.answerBlocks[2]?.content).toContain("继续观察");

    qaPage.cleanup();
  });

  it("不同问题会命中不同字段重点", async () => {
    const qaPage = renderStockQaHook();
    await flushBootstrap();

    const defaultExplanation = qaPage.result.answerBlocks[2]?.content;

    act(() => {
      qaPage.result.setSelectedQuestion("历史类比对应了哪段过去情况");
    });

    const historyExplanation = qaPage.result.answerBlocks[2]?.content;

    act(() => {
      qaPage.result.setSelectedQuestion("下一次复查点要看什么");
    });

    const reviewExplanation = qaPage.result.answerBlocks[2]?.content;

    expect(defaultExplanation).toBe("指数涨幅转强且分时承接改善，说明当前事件所处的大盘环境从中性向顺风切换。");
    expect(historyExplanation).toBe("更接近风险偏好修复日，而不是单边风险释放日。");
    expect(reviewExplanation).toBe("复查指数方向、成交延续与事件热度是否同向。");

    qaPage.cleanup();
  });
});
