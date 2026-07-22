// @vitest-environment jsdom

import { act } from "react";
import { createRoot } from "react-dom/client";
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

import { useHomeWorkspace } from "@/features/home/hooks/useHomeWorkspace";

type WorkspaceHookResult = ReturnType<typeof useHomeWorkspace>;

let latestWorkspace: WorkspaceHookResult | null = null;

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

function WorkspaceProbe() {
  latestWorkspace = useHomeWorkspace(currentRequestedEventId);
  return null;
}

let currentRequestedEventId: string | null = null;

function renderWorkspaceHook(requestedEventId: string | null = null) {
  currentRequestedEventId = requestedEventId;
  const container = document.createElement("div");
  document.body.appendChild(container);
  const root = createRoot(container);

  act(() => {
    root.render(<WorkspaceProbe />);
  });

  return {
    get result() {
      if (latestWorkspace === null) {
        throw new Error("useHomeWorkspace result is not ready.");
      }
      return latestWorkspace;
    },
    cleanup() {
      act(() => {
        root.unmount();
      });
      container.remove();
      latestWorkspace = null;
    },
  };
}

async function flushBootstrap() {
  await act(async () => {
    await Promise.resolve();
  });
}

function fillRequiredDraft(workspace: ReturnType<typeof renderWorkspaceHook>) {
  act(() => {
    workspace.result.handleChangeDecisionDraft("action", "继续观察");
  });

  act(() => {
    workspace.result.handleChangeDecisionDraft("reasonTag", "环境顺风");
  });

  act(() => {
    workspace.result.handleChangeDecisionDraft("horizon", "1-3天");
  });
}

afterEach(() => {
  latestWorkspace = null;
  currentRequestedEventId = null;
  vi.restoreAllMocks();
});

describe("useHomeWorkspace", () => {
  it("提交失败时进入 editing 并写入表单错误", async () => {
    const workspace = renderWorkspaceHook();
    await flushBootstrap();

    act(() => {
      workspace.result.handleSelectEvent("market-index-context-20260720");
    });

    act(() => {
      workspace.result.handleChangeDecisionDraft("action", "继续观察");
    });

    act(() => {
      workspace.result.handleSubmitDecision();
    });

    expect(workspace.result.homeWorkspaceState).toBe("editing");
    expect(workspace.result.formError).toBe("请先补全动作、原因标签和观察周期。");
    expect(workspace.result.latestSubmitEcho).toBeNull();

    workspace.cleanup();
  });

  it("提交成功后生成回显与记录，重试后清空回显并回到 editing", async () => {
    vi.spyOn(Date.prototype, "toLocaleString").mockReturnValue("2026/07/22 04:15:00");
    vi.spyOn(Date, "now").mockReturnValue(1721592900000);

    const workspace = renderWorkspaceHook();
    await flushBootstrap();

    act(() => {
      workspace.result.handleSelectEvent("market-index-context-20260720");
    });

    fillRequiredDraft(workspace);

    act(() => {
      workspace.result.handleChangeDecisionDraft("note", "等待收盘前复核");
    });

    act(() => {
      workspace.result.handleSubmitDecision();
    });

    expect(workspace.result.homeWorkspaceState).toBe("submitted");
    expect(workspace.result.latestSubmitEcho?.eventId).toBe("market-index-context-20260720");
    expect(workspace.result.recentDecisionRecords[0]?.id).toBe("market-index-context-20260720-1721592900000");
    expect(workspace.result.eventList[4]?.summary.processStatus).toBe("done");

    act(() => {
      workspace.result.handleRetrySubmitDecision();
    });

    expect(workspace.result.latestSubmitEcho).toBeNull();
    expect(workspace.result.homeWorkspaceState).toBe("editing");

    workspace.cleanup();
  });

  it("成功提交后再切事件会重建草稿并清空回显", async () => {
    vi.spyOn(Date.prototype, "toLocaleString").mockReturnValue("2026/07/22 04:16:00");
    vi.spyOn(Date, "now").mockReturnValue(1721592960000);

    const workspace = renderWorkspaceHook();
    await flushBootstrap();

    act(() => {
      workspace.result.handleSelectEvent("market-index-context-20260720");
    });

    fillRequiredDraft(workspace);

    act(() => {
      workspace.result.handleChangeDecisionDraft("note", "旧事件草稿内容");
    });

    act(() => {
      workspace.result.handleSubmitDecision();
    });

    expect(workspace.result.latestSubmitEcho?.eventId).toBe("market-index-context-20260720");

    act(() => {
      workspace.result.handleSelectEvent("stock-trigger-point-20260720-300750");
    });

    expect(workspace.result.selectedEventId).toBe("stock-trigger-point-20260720-300750");
    expect(workspace.result.homeWorkspaceState).toBe("selected");
    expect(workspace.result.latestSubmitEcho).toBeNull();
    expect(workspace.result.homeRecordDraft).toEqual({
      eventId: "stock-trigger-point-20260720-300750",
      action: "",
      reasonTag: "",
      horizon: "",
      note: "",
    });

    workspace.cleanup();
  });

  it("带 eventId 回到首页时会自动恢复对应事件上下文", async () => {
    const workspace = renderWorkspaceHook("market-index-context-20260720");
    await flushBootstrap();

    expect(workspace.result.selectedEventId).toBe("market-index-context-20260720");
    expect(workspace.result.homeWorkspaceState).toBe("selected");
    expect(workspace.result.homeRecordDraft).toEqual({
      eventId: "market-index-context-20260720",
      action: "",
      reasonTag: "",
      horizon: "",
      note: "",
    });
    expect(workspace.result.latestSubmitEcho).toBeNull();

    workspace.cleanup();
  });

  it("带空 eventId 进入首页时会降级为空态并给出提示", async () => {
    const workspace = renderWorkspaceHook("   ");
    await flushBootstrap();

    expect(workspace.result.selectedEventId).toBeNull();
    expect(workspace.result.homeWorkspaceState).toBe("empty");
    expect(workspace.result.queryRecoveryNotice).toBe("检测到空 eventId，当前已按首页默认空态降级展示。");

    workspace.cleanup();
  });

  it("带不存在的 eventId 进入首页时会降级为空态并给出提示", async () => {
    const workspace = renderWorkspaceHook("unknown-event-id");
    await flushBootstrap();

    expect(workspace.result.selectedEventId).toBeNull();
    expect(workspace.result.homeWorkspaceState).toBe("empty");
    expect(workspace.result.queryRecoveryNotice).toBe(
      "未找到 eventId=unknown-event-id 对应的首页事件，当前已回到默认空态。",
    );

    workspace.cleanup();
  });
});
