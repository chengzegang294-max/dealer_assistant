// @vitest-environment jsdom

import { act } from "react";
import { createRoot } from "react-dom/client";
import { MemoryRouter } from "react-router-dom";
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

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

function HomePageProbe() {
  latestHomePage = useHomePage();
  return null;
}

function renderHomePageHook() {
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);

  act(() => {
    root.render(
      <MemoryRouter>
        <HomePageProbe />
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
});
