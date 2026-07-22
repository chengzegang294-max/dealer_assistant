import { describe, expect, it } from "vitest";

import { homeBootstrapMockEvents } from "@/features/home/api/mock/homeBootstrapMock";
import {
  applyDecisionDraftChange,
  applySelectEvent,
  buildSearchActionEcho,
  buildDraft,
  buildSubmitDecisionResult,
  getWorkspaceStateAfterRetry,
} from "@/features/home/model/workspaceModel";

describe("applySelectEvent", () => {
  it("切事件时重建草稿并清空回显与表单错误", () => {
    const result = applySelectEvent("market-index-context-20260720");

    expect(result.nextSelectedEventId).toBe("market-index-context-20260720");
    expect(result.nextWorkspaceState).toBe("selected");
    expect(result.nextDraft).toEqual(buildDraft("market-index-context-20260720"));
    expect(result.nextSubmitEcho).toBeNull();
    expect(result.nextFormError).toBeNull();
  });

  it("切到新事件时不会沿用上一事件草稿内容", () => {
    const result = applySelectEvent("stock-trigger-point-20260720-300750");

    expect(result.nextDraft).toEqual({
      eventId: "stock-trigger-point-20260720-300750",
      action: "",
      reasonTag: "",
      horizon: "",
      note: "",
    });
  });
});

describe("buildSubmitDecisionResult", () => {
  it("未选中事件时返回表单错误", () => {
    const result = buildSubmitDecisionResult({
      selectedEvent: null,
      draft: buildDraft(null),
      submittedAt: "2026/07/22 03:40:00",
      recordId: "record-null-event",
      eventList: homeBootstrapMockEvents,
    });

    expect(result).toEqual({
      ok: false,
      formError: "请先从今日事件流里选中一条事件。",
    });
  });

  it("字段未补全时返回错误并要求进入 editing", () => {
    const selectedEvent = homeBootstrapMockEvents[0];
    const result = buildSubmitDecisionResult({
      selectedEvent,
      draft: {
        eventId: selectedEvent.summary.eventId,
        action: "继续观察",
        reasonTag: "",
        horizon: "",
        note: "先留痕",
      },
      submittedAt: "2026/07/22 03:41:00",
      recordId: "record-missing-fields",
      eventList: homeBootstrapMockEvents,
    });

    expect(result).toEqual({
      ok: false,
      formError: "请先补全动作、原因标签和观察周期。",
      nextWorkspaceState: "editing",
    });
  });

  it("提交成功时生成记录与回显，并将对应事件标记为 done", () => {
    const selectedEvent = homeBootstrapMockEvents[0];
    const untouchedEvent = homeBootstrapMockEvents[1];
    const result = buildSubmitDecisionResult({
      selectedEvent,
      draft: {
        eventId: selectedEvent.summary.eventId,
        action: "继续观察",
        reasonTag: "环境顺风",
        horizon: "1-3天",
        note: "  等收盘前再复核一次  ",
      },
      submittedAt: "2026/07/22 03:42:00",
      recordId: "record-submit-success",
      eventList: homeBootstrapMockEvents,
    });

    expect(result.ok).toBe(true);

    if (result.ok) {
      expect(result.nextWorkspaceState).toBe("submitted");
      expect(result.record).toEqual({
        id: "record-submit-success",
        eventId: selectedEvent.summary.eventId,
        title: selectedEvent.summary.title,
        action: "继续观察",
        reasonTag: "环境顺风",
        horizon: "1-3天",
        note: "等收盘前再复核一次",
        submittedAt: "2026/07/22 03:42:00",
      });
      expect(result.submitEcho).toEqual({
        eventId: selectedEvent.summary.eventId,
        title: selectedEvent.summary.title,
        action: "继续观察",
        submittedAt: "2026/07/22 03:42:00",
        summary: "继续观察 / 环境顺风 / 1-3天",
      });
      expect(result.nextEventList[0]?.summary.processStatus).toBe("done");
      expect(result.nextEventList[1]).toEqual(untouchedEvent);
    }
  });
});

describe("getWorkspaceStateAfterRetry", () => {
  it("存在选中事件时回到 editing", () => {
    expect(getWorkspaceStateAfterRetry("market-index-context-20260720")).toBe("editing");
  });

  it("没有选中事件时回到 empty", () => {
    expect(getWorkspaceStateAfterRetry(null)).toBe("empty");
  });
});

describe("applyDecisionDraftChange", () => {
  it("修改字段时同步写入当前 selectedEventId", () => {
    const result = applyDecisionDraftChange(buildDraft(null), "market-index-context-20260720", "action", "继续观察");

    expect(result).toEqual({
      eventId: "market-index-context-20260720",
      action: "继续观察",
      reasonTag: "",
      horizon: "",
      note: "",
    });
  });

  it("只覆盖目标字段，不污染其他草稿字段", () => {
    const result = applyDecisionDraftChange(
      {
        eventId: "market-index-context-20260720",
        action: "继续观察",
        reasonTag: "环境顺风",
        horizon: "1-3天",
        note: "",
      },
      "market-index-context-20260720",
      "note",
      "保持观察",
    );

    expect(result).toEqual({
      eventId: "market-index-context-20260720",
      action: "继续观察",
      reasonTag: "环境顺风",
      horizon: "1-3天",
      note: "保持观察",
    });
  });
});

describe("buildSearchActionEcho", () => {
  it("空输入时返回失败提示", () => {
    expect(buildSearchActionEcho("   ")).toEqual({
      ok: false,
      message: "请输入标的代码后再发出打开动作。",
    });
  });

  it("有效输入时裁剪空白并返回成功提示", () => {
    expect(buildSearchActionEcho(" 300750 ")).toEqual({
      ok: true,
      message: "已发出打开标的页动作：300750",
    });
  });
});
