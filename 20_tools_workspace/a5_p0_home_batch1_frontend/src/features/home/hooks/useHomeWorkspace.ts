import { useEffect, useMemo, useState } from "react";

import { fetchHomeBootstrap } from "@/features/home/api/homeApi";
import {
  applyDecisionDraftChange,
  applySelectEvent,
  buildDraft,
  buildSearchActionEcho,
  buildSubmitDecisionResult,
  getWorkspaceStateAfterRetry,
} from "@/features/home/model/workspaceModel";
import type {
  DecisionDraft,
  DecisionRecord,
  EventItem,
  HomeWorkspaceState,
  SubmitEcho,
} from "@/features/home/types";

function formatNow() {
  return new Date().toLocaleString("zh-CN", { hour12: false });
}

export function useHomeWorkspace(requestedEventId: string | null = null) {
  const [eventList, setEventList] = useState<EventItem[]>([]);
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);
  const [homeWorkspaceState, setHomeWorkspaceState] = useState<HomeWorkspaceState>("empty");
  const [homeRecordDraft, setHomeRecordDraft] = useState<DecisionDraft>(buildDraft(null));
  const [latestSubmitEcho, setLatestSubmitEcho] = useState<SubmitEcho | null>(null);
  const [searchDraft, setSearchDraft] = useState("");
  const [searchActionEcho, setSearchActionEcho] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [recentDecisionRecords, setRecentDecisionRecords] = useState<DecisionRecord[]>([]);

  useEffect(() => {
    let cancelled = false;

    fetchHomeBootstrap().then((payload) => {
      if (cancelled) {
        return;
      }
      setEventList(payload.events);
      setRecentDecisionRecords(payload.decisionRecords);
    });

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!requestedEventId || eventList.length === 0 || selectedEventId === requestedEventId) {
      return;
    }

    const matchedEvent = eventList.find((event) => event.summary.eventId === requestedEventId);
    if (!matchedEvent) {
      return;
    }

    const result = applySelectEvent(matchedEvent.summary.eventId);
    setSelectedEventId(result.nextSelectedEventId);
    setHomeWorkspaceState(result.nextWorkspaceState);
    setHomeRecordDraft(result.nextDraft);
    setLatestSubmitEcho(result.nextSubmitEcho);
    setFormError(result.nextFormError);
  }, [eventList, requestedEventId, selectedEventId]);

  const selectedEvent = useMemo(
    () => eventList.find((event) => event.summary.eventId === selectedEventId) ?? null,
    [eventList, selectedEventId],
  );

  const queuedEvents = useMemo(
    () => eventList.filter((event) => event.summary.processStatus === "pending"),
    [eventList],
  );

  function handleSelectEvent(eventId: string) {
    // Batch 1 invariant: switching events always rebuilds the draft and clears stale submit echo.
    const result = applySelectEvent(eventId);
    setSelectedEventId(result.nextSelectedEventId);
    setHomeWorkspaceState(result.nextWorkspaceState);
    setHomeRecordDraft(result.nextDraft);
    setLatestSubmitEcho(result.nextSubmitEcho);
    setFormError(result.nextFormError);
  }

  function handleChangeDecisionDraft<K extends keyof DecisionDraft>(key: K, value: DecisionDraft[K]) {
    setHomeRecordDraft((draft) => applyDecisionDraftChange(draft, selectedEventId, key, value));
    setHomeWorkspaceState("editing");
    setFormError(null);
  }

  function handleSubmitDecision() {
    const result = buildSubmitDecisionResult({
      selectedEvent,
      draft: homeRecordDraft,
      submittedAt: formatNow(),
      recordId: `${selectedEvent?.summary.eventId ?? "unknown"}-${Date.now()}`,
      eventList,
    });

    if (result.ok === false) {
      setFormError(result.formError);
      if (result.nextWorkspaceState) {
        setHomeWorkspaceState(result.nextWorkspaceState);
      }
      return;
    }

    setRecentDecisionRecords((records) => [result.record, ...records].slice(0, 6));
    setLatestSubmitEcho(result.submitEcho);
    setHomeWorkspaceState(result.nextWorkspaceState);
    setEventList(result.nextEventList);
    setFormError(null);
  }

  function handleRetrySubmitDecision() {
    setLatestSubmitEcho(null);
    setHomeWorkspaceState(getWorkspaceStateAfterRetry(selectedEventId));
  }

  function handleOpenStockPage(stockCode: string) {
    const result = buildSearchActionEcho(stockCode);
    setSearchActionEcho(result.message);
  }

  return {
    eventList,
    selectedEventId,
    selectedEvent,
    homeWorkspaceState,
    homeRecordDraft,
    latestSubmitEcho,
    searchDraft,
    searchActionEcho,
    formError,
    recentDecisionRecords,
    queuedEvents,
    setSearchDraft,
    handleSelectEvent,
    handleChangeDecisionDraft,
    handleSubmitDecision,
    handleRetrySubmitDecision,
    handleOpenStockPage,
  };
}
