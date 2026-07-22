import type {
  DecisionDraft,
  DecisionRecord,
  EventItem,
  HomeWorkspaceState,
  SubmitEcho,
} from "@/features/home/types";

export interface SubmitDecisionSuccessResult {
  ok: true;
  nextWorkspaceState: HomeWorkspaceState;
  record: DecisionRecord;
  submitEcho: SubmitEcho;
  nextEventList: EventItem[];
}

export interface SubmitDecisionFailureResult {
  ok: false;
  formError: string;
  nextWorkspaceState?: HomeWorkspaceState;
}

export type SubmitDecisionResult = SubmitDecisionSuccessResult | SubmitDecisionFailureResult;

export interface SelectEventResult {
  nextSelectedEventId: string;
  nextWorkspaceState: HomeWorkspaceState;
  nextDraft: DecisionDraft;
  nextSubmitEcho: null;
  nextFormError: null;
}

export function buildDraft(eventId: string | null): DecisionDraft {
  return {
    eventId,
    action: "",
    reasonTag: "",
    horizon: "",
    note: "",
  };
}

export function applyDecisionDraftChange<K extends keyof DecisionDraft>(
  draft: DecisionDraft,
  selectedEventId: string | null,
  key: K,
  value: DecisionDraft[K],
) {
  return {
    ...draft,
    [key]: value,
    eventId: selectedEventId,
  };
}

export function applySelectEvent(eventId: string): SelectEventResult {
  return {
    nextSelectedEventId: eventId,
    nextWorkspaceState: "selected",
    nextDraft: buildDraft(eventId),
    nextSubmitEcho: null,
    nextFormError: null,
  };
}

export function getWorkspaceStateAfterRetry(selectedEventId: string | null): HomeWorkspaceState {
  return selectedEventId ? "editing" : "empty";
}

export function buildSearchActionEcho(stockCode: string) {
  const code = stockCode.trim();

  if (!code) {
    return {
      ok: false as const,
      message: "请输入标的代码后再发出打开动作。",
    };
  }

  return {
    ok: true as const,
    message: `已发出打开标的页动作：${code}`,
  };
}

export function buildSubmitDecisionResult(params: {
  selectedEvent: EventItem | null;
  draft: DecisionDraft;
  submittedAt: string;
  recordId: string;
  eventList: EventItem[];
}): SubmitDecisionResult {
  const { selectedEvent, draft, submittedAt, recordId, eventList } = params;

  if (!selectedEvent) {
    return {
      ok: false,
      formError: "请先从今日事件流里选中一条事件。",
    };
  }

  if (!draft.action || !draft.reasonTag || !draft.horizon) {
    return {
      ok: false,
      formError: "请先补全动作、原因标签和观察周期。",
      nextWorkspaceState: "editing",
    };
  }

  const record: DecisionRecord = {
    id: recordId,
    eventId: selectedEvent.summary.eventId,
    title: selectedEvent.summary.title,
    action: draft.action,
    reasonTag: draft.reasonTag,
    horizon: draft.horizon,
    note: draft.note.trim(),
    submittedAt,
  };

  const submitEcho: SubmitEcho = {
    eventId: selectedEvent.summary.eventId,
    title: selectedEvent.summary.title,
    action: draft.action,
    submittedAt,
    summary: `${draft.action} / ${draft.reasonTag} / ${draft.horizon}`,
  };

  const nextEventList: EventItem[] = eventList.map((event) =>
    event.summary.eventId === selectedEvent.summary.eventId
      ? {
          ...event,
          summary: {
            ...event.summary,
            processStatus: "done",
          },
        }
      : event,
  );

  return {
    ok: true,
    nextWorkspaceState: "submitted",
    record,
    submitEcho,
    nextEventList,
  };
}
